import random
from collections import defaultdict
from dataclasses import dataclass

import pandas as pd
from munch import Munch

from hawa.config import project
from hawa.paper.health import HealthReportData
from hawa.paper.mht import MhtWebData


@dataclass
class SchoolMixin:
    """为了在 __mro__ 中有更高的优先级， mixin 在继承时，应该放在最前"""
    meta_unit_type: str = 'school'


@dataclass
class SchoolHealthReportData(SchoolMixin, HealthReportData):
    grade_gender_distribution = None
    grade_score = None  # 年级最高、最低、平均分
    grade_rank_dis = None  # 年级、性别、水平学生分布占比
    grade_reverse_rank_dis = None  # 占比由高到低的年级分布水平
    grade_code_score = None  # 健康素养水平 所需数据
    compare_grade_year_school = None  # 比较学校与去年维度领域
    compare_all_total = None  # 比照去年数据和学校数据的全年级平均数

    def _to_count_k_grade_reverse_rank_dis(self):
        records = {}
        rank_dis = self.grade_rank_dis
        for g in self.grade.grades:
            here = rank_dis[g].total
            base = [(v, k) for k, v in here.items()]
            records[g] = [b for b in sorted(base, key=lambda x: x[0], reverse=True)]
        self.grade_reverse_rank_dis = records

    def _to_count_l_grade_code_score(self):
        """健康素养水平 所需数据"""
        records = {}
        scores = self.code_scores
        for grade in self.grade.grades:
            base: pd.DataFrame = scores.loc[scores.grade == grade, :]
            base_dimensions = base.loc[base.category == 'dimension', ['code', 'total']]
            base_fields = base.loc[base.category == 'field', ['code', 'total']]

            dimensions = self._count_df_reverse(first_col='code', second_col='total', data=base_dimensions)
            fields = self._count_df_reverse(first_col='code', second_col='total', data=base_fields)

            a = base.loc[base.category == 'field', ['code', 'F']].mean().mean()
            b = base.loc[base.category == 'field', ['code', 'M']].mean().mean()
            records[grade] = {
                'dimension': dimensions, 'field': fields,
                'cond': self.count_cond(a, b)
            }
        self.grade_code_score = records

    def _to_count_n_compare_grade_year_school(self):
        if not self.is_load_last:
            return
        res = defaultdict(dict)
        cols = ['total', 'M', 'F']
        for grade in self.grade.grades:
            for col in cols:
                res[grade][col] = self._count_dim_field_diff(grade=grade, key=col)
        self.compare_grade_year_school = res

    def _to_count_o_compare_all_total(self):
        if not self.is_load_last:
            return
        data = []
        for grade in self.grade.grades:
            sch = self.grade_score[grade].avg
            year = self.last_year[str(grade)]['score']['total']
            data.append(sch - year)
        self.compare_all_total = self.count_cond(a=sum(data) / len(data), b=0)

    # property 数据
    @property
    def gender_count(self) -> Munch:
        r = self.students.gender.value_counts()
        return Munch({'M': 0, 'F': 0} | r.to_dict())

    # 工具函数

    def _count_df_reverse(self, first_col: str, second_col: str, data: pd.DataFrame):
        base = data.to_dict(orient='record')
        middle = {d[first_col]: d[second_col] / 100 for d in base}
        reverse_middle = {v: k for k, v in middle.items()}
        res = [(self._retain_prec(k), reverse_middle[k]) for k in sorted(reverse_middle.keys(), reverse=True)]
        return res

    def count_cond(self, a: float, b: float):
        if a == b:
            conditions = '等于'.split()
        elif a - b >= 5:
            conditions = '明显高于'.split()
        elif abs(a - b) < 5:
            conditions = '差异不明显于'.split()
        elif a - b <= -5:
            conditions = '明显低于'.split()
        else:
            raise
        return random.choice(conditions)

    def _count_dim_field_diff(self, grade: int, key: str):
        """计算学校与全国对比的维度、领域高低
        :param key: 比较的项：total/M/F
        """
        data = self._build_one_data(grade=grade)
        key_col = f'{key}_y_s'
        data[key_col] = data[f"{key}_sch"] - data[f"{key}_year"]
        cols = ['category_sch', 'code', key_col, f'{key}_year', f'{key}_sch']
        compare = data.sort_values(['category_sch', key_col]).loc[:, cols]
        dim_compare = compare.loc[compare.category_sch == 'dimension', :]
        field_compare = compare.loc[compare.category_sch == 'field', :]
        dim_low, dim_high = dim_compare.head(n=1), dim_compare.tail(n=1)
        field_low, field_high = field_compare.head(n=1), field_compare.tail(n=1)
        return {
            'dim_low': dim_low.code.values[0] if dim_low[key_col].values[0] < 0 else '',
            'field_low': field_low.code.values[0] if field_low[key_col].values[0] < 0 else '',
            'dim_high': dim_high.code.values[0] if dim_high[key_col].values[0] > 0 else '',
            'field_high': field_high.code.values[0] if field_high[key_col].values[0] > 0 else '',
        }

    def _build_one_data(self, grade: int):
        """抽象某个构建数据的逻辑"""
        year_scores = self.last_year_code_scores
        sch_scores = self.code_scores
        year_code_score = year_scores.loc[year_scores.grade == grade, :]
        school_code_score = sch_scores.loc[sch_scores.grade == grade, :]
        data = pd.merge(
            year_code_score, school_code_score, left_on='code', right_on='code',
            suffixes=['_year', '_sch']
        )
        return data

    def build_code_gender_data(self, category: str, g: int):
        data = self._build_one_data(grade=g)
        use_cols = [f'{category}_year', f"{category}_sch", 'code', 'category_sch']
        data = data.loc[:, use_cols].sort_values(['category_sch', 'code'])
        del data['category_sch']
        return data

    def compare_gender_text(self, grade: int):
        grade_rank_dis_m = self.grade_rank_dis[grade].M
        grade_rank_dis_f = self.grade_rank_dis[grade].F
        level_m = round(sum([grade_rank_dis_m['优秀'], grade_rank_dis_m['良好']]), 1)
        level_f = round(sum([grade_rank_dis_f['优秀'], grade_rank_dis_f['良好']]), 1)
        if level_m - level_f >= 5:
            return '男生明显大于女生'
        elif level_m - level_f <= -5:
            return '男生明显小于女生'
        else:
            return '男生与女生不存在明显差异'

    def low_high_code_text(self, grade: int, gender: str):
        """相对最高、相对最低文本
        :param grade: total/M/F
        :param gender: total/M/F
        """
        if not self.is_load_last:
            return
        data = self.build_code_gender_data(category=gender, g=grade)
        data['diff'] = data[f"{gender}_sch"] - data[f"{gender}_year"]
        bigger = data.loc[data['diff'] >= 5, :].code.to_list()
        smaller = data.loc[data['diff'] <= -5, :].code.to_list()
        res = ''
        if bigger:
            local_codes = self._build_codes(bigger)
            res += f"{local_codes}{self.meta_unit.short_name}{project.category_map[gender]}分数" \
                   f"明显高于全国{project.grade_simple[grade]}年级{project.category_map[gender]}平均分数，"
        if smaller:
            local_codes = self._build_codes(smaller)
            res += f"{local_codes}{self.meta_unit.short_name}{project.category_map[gender]}分数" \
                   f"明显低于全国{project.grade_simple[grade]}年级{project.category_map[gender]}平均分数，"
        if not bigger and not smaller:
            res += '所有维度和领域都没有明显差异。'
        else:
            res += '其余维度和领域没有明显差异。'
        return res

    def _build_codes(self, codes: list[str]):
        if len(codes) == 1:
            return f'“{codes[0]}”'
        elif len(codes) > 1:
            return '、'.join([f'“{i}”' for i in codes[:-1]]) + f'和“{codes[-1]}”'
        else:
            return ''

    def compare_grade_gen_text(self):
        """生成整体分析标题及一句分析文本。"""
        data = {}
        for grade in self.grade.grades:
            sch = self.grade_score[grade].avg
            year = self.last_year[str(grade)]['score']['total']
            data[grade] = sch - year
        total_dif = sum(data.values()) / len(data)
        diff = []
        if total_dif > 0:
            for k, v in data.items():
                if v < 0:
                    diff.append(k)
        elif total_dif < 0:
            for k, v in data.items():
                if v > 0:
                    diff.append(k)
        else:
            pass
        cond = self.compare_all_total
        if diff:
            grade_text = '除' + '、'.join([project.grade_simple[g] for g in diff]) + '年级外，'
        else:
            grade_text = ''
        title_text = f"{grade_text}各年级生命与健康素养{cond}全国平均水平"
        describe_text = f"{grade_text}{self.meta_unit.short_name}各年级的健康素养水平{cond}{self.last_year_num}年的全国平均水平"
        return title_text, describe_text

    def describe_grade_text(self, category: str):
        """描述全年级对比情况
        :param category: total/gender  total：总体比全国 / gender：男生比女生。
        """
        bigger, smaller = [], []
        for grade in self.grade.grades:
            if category == 'total':
                first = self.grade_score[grade].avg
                second = self.last_year[str(grade)]['score']['total']
            else:
                first = self.summary_scores[grade]['M']
                second = self.summary_scores[grade]['F']
            if first - second >= 5:
                bigger.append(f"{project.grade_simple[grade]}年级")
            elif first - second <= -5:
                smaller.append(f"{project.grade_simple[grade]}年级")
        res = ''
        if bigger:
            local_codes = self._build_codes(bigger)
            res += f"{self.meta_unit.short_name}{local_codes}分数"
            match category:
                case 'total':
                    res += '明显高于全国平均分数，'
                case 'gender':
                    res += '男生明显高于女生，'

        if smaller:
            local_codes = self._build_codes(smaller)
            res += f"{self.meta_unit.short_name}{local_codes}分数"
            match category:
                case 'total':
                    res += "明显低于全国平均分数，"
                case 'gender':
                    res += "男生明显低于女生，"
        if (bigger or smaller) and len(bigger) + len(smaller) < len(self.grade.grades):
            res += '其他年级没有明显差异。'
        if not bigger and not smaller:
            res = f'{self.meta_unit.short_name}分数对比无明显差异。'
        return res

    def replace_hai(self, text: str, condition: list):
        if condition:
            return text
        else:
            return text.replace('还', '')


@dataclass
class SchoolMhtWebData(SchoolMixin, MhtWebData):
    meta_unit_type: str = 'school'
    pass
