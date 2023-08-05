"""健康测评数据"""
import itertools
import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Union, Set

import pandas as pd
from munch import Munch

from hawa.common.data import CommonData
from hawa.config import project


@dataclass
class HealthData(CommonData):
    """健康测评数据，不应直接使用，应向下继承 city/district/school 等"""
    test_types: list[str] = field(default_factory=lambda: ['publicWelfare', 'ZjpublicWelfare'])
    code_word_list: Set[str] = field(default_factory=lambda: {'dimension', 'field'})


@dataclass
class HealthReportData(HealthData):
    # 计算数据
    code_scores: pd.DataFrame = pd.DataFrame()
    summary_scores: dict = field(default_factory=dict)
    grade_good_bad = None  # 优势 优先关注点

    def _to_count_a0_last_year_data(self):
        if not self.is_load_last:
            return
        key = f'{project.REDIS_PREFIX}{self.last_year_num}:data'
        if not self.redis.conn.exists(key):
            raise ValueError(f'last year data not exists: {key}')
        self.last_year = json.loads(self.redis.conn.get(key))
        res = []
        for grade in self.grade.grades:
            year_code_score = pd.DataFrame(self.last_year[str(grade)]['code']).T
            year_code_score['i'] = [int(grade) * 10 + i for i in range(1, 11)]
            year_code_score.set_index('i', inplace=True)
            res.append(year_code_score)
        self.last_year_code_scores = pd.concat(res)

    def _to_count_c_code_scores(self):
        records = []
        for grade in self.grade.grades:
            for code in self.measurement.dimensions:
                record = self._count_grade_code_score(grade=grade, code=code, category='dimension')
                records.append(record)
            for code in self.measurement.fields:
                record = self._count_grade_code_score(grade=grade, code=code, category='field')
                records.append(record)
        self.code_scores = pd.DataFrame.from_records(records)

    def _to_count_d_summary_scores(self):
        records = defaultdict(dict)
        for grade, group in self.code_scores.groupby('grade'):
            for gender in project.gender_map.keys():
                records[grade][gender] = round(self._count_school_score(group, key=gender), 1)
        self.summary_scores = records

    def _to_count_e_grade_good_bad(self):
        records = defaultdict(dict)
        for g, group in self.code_scores.groupby('grade'):
            for gender in project.gender_map.keys():
                records[g][gender] = {
                    'dimension': {'good': [], 'bad': []},
                    'field': {'good': [], 'bad': []}
                }
            for _, row in group.iterrows():
                for gender in project.gender_map.keys():
                    if row[gender] >= 80:
                        if row['category'] == 'dimension':
                            records[g][gender]['dimension']['good'].append(row['code'])
                        if row['category'] == 'field':
                            records[g][gender]['field']['good'].append(row['code'])
                    elif row[gender] < 60:
                        if row['category'] == 'dimension':
                            records[g][gender]['dimension']['bad'].append(row['code'])
                        if row['category'] == 'field':
                            records[g][gender]['field']['bad'].append(row['code'])
                    else:
                        pass
                else:
                    for code in itertools.chain(self.measurement.dimensions, self.measurement.fields):
                        for ccc in ['dimension', 'field']:
                            if code in records[g]['total'][ccc]['bad']:
                                for ggg in 'MF':
                                    try:
                                        records[g][ggg][ccc]['bad'].remove(code)
                                    except ValueError:
                                        pass

        self.grade_good_bad = records

    def _to_count_f_case_gender_counts(self):
        """单年级，各班级性别数据；多年级，各年级性别数据。"""
        ans = self.final_answers.drop_duplicates(subset=['student_id'])
        data = ans.loc[:, ['grade', 'cls', 'gender', 'student_id']]
        # 年级 班级 男生数 女生数 总人数
        # 班级 男生数 女生数 总人数
        records = []
        for grade, grade_group in data.groupby(by=['grade']):
            for cls, cls_group in grade_group.groupby('cls'):
                grade_cls = Munch(grade=grade, cls=cls)
                cls_total = Munch(total=len(cls_group))
                cls_gender = cls_group.gender.value_counts().to_dict()
                records.append(grade_cls | cls_total | cls_gender)
            grade_total = Munch(total=len(grade_group))
            grade_gender = grade_group.gender.value_counts().to_dict()
            records.append({'grade': grade, 'cls': 0, 'F': 0, 'M': 0} | grade_total | grade_gender)
        records = pd.DataFrame.from_records(records).fillna(0)
        records['M'] = records.M.astype('int')
        records['F'] = records.F.astype('int')
        if len(self.case_ids) == 1:
            records['cls'] = records.apply(self._count_cls, axis=1)
        else:
            records['grade'] = records.grade.apply(lambda x: f"{project.grade_simple[x]}年级")
            records = records.loc[records.cls == 0, :]
        self.case_gender_counts = records.to_dict(orient='records')

    def _to_count_g_cronbach_alpha(self):
        import pingouin as pg
        cols = ['student_id', 'item_id', 'score']
        res = []
        for grade, group in self.final_answers.groupby('grade'):
            base = group.loc[:, cols]
            data = pd.pivot_table(base, index='item_id', columns='student_id', values='score')
            c: tuple = pg.cronbach_alpha(data)
            res.append(c[0])
        self.cronbach_alpha = [round(i, 3) for i in res]

    def _to_count_h_grade_gender_distribution(self):
        """年级性别分布"""
        data = self.case_gender_counts
        records = {}
        if len(self.case_ids) == 1:
            for row in data:
                if '年级' in row['cls']:
                    records[row['cls']] = Munch(row)
        for row in data:
            records[row['grade']] = Munch(row)
        self.grade_gender_distribution = records

    def _to_count_i_grade_score(self):
        """年级最高、最低、平均分"""
        records = Munch()
        for grade in self.grade.grades:
            ans = self.final_answers.loc[self.final_answers.grade == grade, :]
            score = ans.groupby('student_id').score
            record = Munch(
                avg=self._retain_prec(score.mean().mean()),
                min=self._retain_prec(score.mean().min()),
                max=self._retain_prec(score.mean().max()))
            records[grade] = record
        self.grade_score = records

    def _to_count_j_grade_rank_dis(self):
        records = {}
        base = dict(
            zip(project.ranks['FEEDBACK_LEVEL'].values(),
                [0] * len(project.ranks['FEEDBACK_LEVEL'])))
        for grade, group in self.final_scores.groupby('grade'):
            count = base | group.level.value_counts().to_dict()
            records[grade] = Munch()
            for gender, g in group.groupby('gender'):
                gender_count = base | g.level.value_counts().to_dict()
                records[grade][gender] = \
                    {k: self._retain_prec(v / sum(gender_count.values()))
                     for k, v in gender_count.items()}
            records[grade].total = {k: self._retain_prec(v / sum(count.values())) for k, v in count.items()}
        self.grade_rank_dis = records

    def cache_year_data(self, year: int):
        """缓存年数据"""
        project.logger.info(f"缓存年数据 {year=}")
        key = f'{project.REDIS_PREFIX}{self.last_year_num}:data'

        res = defaultdict(dict)
        tool = self.__class__(meta_unit_type='country', meta_unit_id=0, target_year=year, is_load_last=False)
        project.logger.debug('after init data')

        for grade, value in zip(tool.grade.grades, tool.grade_gender_distribution.values()):
            res[grade]['people'] = value
        for grade, group in tool.code_scores.groupby(['grade']):
            res[grade]['code'] = {}
            for r in group.to_dict(orient='record'):
                res[grade]['code'][r['code']] = r
        for grade, value in tool.grade_rank_dis.items():
            res[grade]['rank'] = value
        score_dict = defaultdict(dict)
        # 计算年级、性别 平均分
        for grade, first_value in res.items():
            for second_key, second_value in first_value.items():
                if second_key == 'code':
                    total_score = self._count_year_score('total', second_value)
                    f_score = self._count_year_score('F', second_value)
                    m_score = self._count_year_score('M', second_value)
                    score_dict[grade] = {
                        'total': total_score, 'F': f_score, 'M': m_score
                    }
        for grade, value in score_dict.items():
            res[grade]['score'] = value
        # 计算总人数
        res['total'] = defaultdict(dict)
        res['total']['total'] = sum([self._get_value(v, 'total') for v in res.values()])
        res['total']['M'] = sum([self._get_value(v, 'M') for v in res.values()])
        res['total']['F'] = sum([self._get_value(v, 'F') for v in res.values()])
        self.redis.conn.set(key, json.dumps(res))

    def _count_grade_code_score(self, code: str, grade: int, category: str):
        """计算指定年级、指定维度、领域的分数"""
        ans = self.final_answers
        local_ans = ans.loc[(ans.grade == grade) & (ans[category] == code), :]
        student_score = local_ans.groupby('student_id').score.mean().mean() * 100
        gender_score = local_ans.groupby(['gender', 'student_id']) \
                           .score.mean().reset_index().groupby(
            'gender').score.mean() * 100
        res = Munch(
            total=student_score, grade=grade, code=code, category=category,
            **gender_score.to_dict())
        return res

    @staticmethod
    def _count_school_score(group, key: str):
        """计算学校的维度、领域性别分数"""
        dim_score = group.loc[group.category == 'dimension', :][key].mean()
        field_score = group.loc[group.category == 'field', :][key].mean()
        return (dim_score + field_score) / 2

    def _count_cls(self, row):
        if row['cls']:
            return f"{project.grade_simple[row['grade']]}({int(row['cls'])})班"
        else:
            return f"{project.grade_simple[row['grade']]}年级"

    def _retain_prec(self, n: float, prec: int = 1):
        n = n * 100
        return int(n) if n in (0, 0.0, 100.0, 100) else round(n, prec)

    def _get_value(self, v, k):
        """计算去年数据中的总人数"""
        base: Union[dict, int] = dict(v).get('people', 0)
        if base:
            return base[k]
        else:
            return 0

    @staticmethod
    def _count_year_score(category: str, data: dict):
        """
        :param category: total/M/F
        :param data: 需计算数据
        """
        dim_score = sum([dict(v)[category] for v in list(data.values()) if v['category'] == 'dimension']) / 4
        field_score = sum([dict(v)[category] for v in list(data.values()) if v['category'] == 'field']) / 6
        score = (dim_score + field_score) / 2
        return score
