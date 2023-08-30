import pandas as pd
import random
import traceback


DATASET_URL = 'https://expert-ai-files.ams3.digitaloceanspaces.com/expert-ai-text-vs-graph-comparison2.csv'
COL_DID, COL_OPTION1, COL_OPTION2, COL_OPTION1_COPY = 'did', 'option1', 'option2', 'option1_copy'
COL_OPTION_ORDER = 'option_order'
HUMAN_BURNOUT_THRESHOLD = 10


class Base:

    def __init__(self):
        super().__init__()
        self.df: pd.DataFrame = self.load_dataframe()
        self.df_sample = self.get_df_sample()

    @staticmethod
    def load_dataframe() -> pd.DataFrame:
        """
        columns = (category, option1, option2) (1-2 words, long text with line breaks, long text with line breaks)
        :return:
        """
        df = pd.read_csv(DATASET_URL)
        # save data index as a copy of the original ordered index - will be later used to identify answers (options)
        df[COL_DID] = df.index
        return df

    def get_df_sample(self, n: int = HUMAN_BURNOUT_THRESHOLD) -> pd.DataFrame:

        """
        sample N records, according to OpenAI's recommendation to not burn out human evaluators
        swap content of part of the columns
        :return:
        """

        df = self.df

        # Sample N rows from a copy of the dataframe
        sampled_df = df.sample(n=n).copy()

        # options order
        sampled_df[COL_OPTION_ORDER] = [[0, 1] for _ in range(len(sampled_df))]

        # Shuffle the selection and reset index
        sampled_df = sampled_df.sample(frac=1).reset_index(drop=True)

        # Select a random number K around the middle of N
        k = random.randint(n // 2 - 1, n // 2 + 1)

        # Create a new column 'option1_copy' with a copy of 'option1'
        sampled_df[COL_OPTION1_COPY] = sampled_df[COL_OPTION1]

        # Create a 'where' filter
        where_filter = sampled_df.index.isin(random.sample(range(n), k))

        # Swap the contents of COL_OPTION1 and 'option2' without looping
        sampled_df.loc[where_filter, COL_OPTION1] = sampled_df.loc[where_filter, COL_OPTION2]
        sampled_df.loc[where_filter, COL_OPTION2] = sampled_df.loc[where_filter, COL_OPTION1_COPY]
        # reverse options order
        sampled_df.loc[where_filter, COL_OPTION_ORDER] = [[1, 0] for _ in range(sum(where_filter))]

        # Drop the COL_OPTION1_COPY column as it's no longer needed
        sampled_df.drop(columns=[COL_OPTION1_COPY], inplace=True)

        return sampled_df


    # region boiler
    def __del__(self):
        try:
            pass
        except:
            # print(traceback.format_exc())
            traceback.format_exc()
            pass

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback_):
        self.__del__()

    # endregion boiler
