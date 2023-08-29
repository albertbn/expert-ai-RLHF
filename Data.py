import re
from Base import Base, COL_OPTION1, COL_OPTION2, COL_DID  # don't remove unused imports


r_newline = re.compile('\n')
r_outline = re.compile(r'^(Title|Summary|Capabilities|Strategy|Objectives|Evaluation)\b', re.M)


class Data(Base):

    def __init__(self):
        super().__init__()

    def get_pairs(self) -> list:
        df_sample = self.df_sample.copy()

        df_sample[COL_OPTION1] = df_sample[COL_OPTION1].str.replace(r_outline, r'<b>\1</b>', regex=True)
        df_sample[COL_OPTION1] = df_sample[COL_OPTION1].str.replace(r_newline, '<br>', regex=True)

        df_sample[COL_OPTION2] = df_sample[COL_OPTION2].str.replace(r_outline, r'<b>\1</b>', regex=True)
        df_sample[COL_OPTION2] = df_sample[COL_OPTION2].str.replace(r_newline, '<br>', regex=True)

        return df_sample.to_dict('records')
