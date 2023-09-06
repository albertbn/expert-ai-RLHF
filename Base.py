import pandas as pd
from typing import Union
import random
import traceback


# DATASET_URL = 'https://expert-ai-files.ams3.digitaloceanspaces.com/expert-ai-text-vs-graph-comparison2.csv'
DATASET_URL = 'https://expert-ai-files.ams3.digitaloceanspaces.com/expert-ai-text-vs-graph-comparison-russia-ukraine-energy.csv'
COL_DID, COL_OPTION1, COL_OPTION2, COL_OPTION1_COPY = 'did', 'option1', 'option2', 'option1_copy'
COL_OPTION_ORDER = 'option_order'
HUMAN_BURNOUT_THRESHOLD = 10
# HACKED_SAMPLE_IDS = [1, 2, 23, 29]  # !
HACKED_SAMPLE_IDS = []  # !


class Base:

    def __init__(self):
        super().__init__()
        self.df: pd.DataFrame = self.load_dataframe()
        # self.df_sample = self.get_df_sample()

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

    def get_hacked_sample(self, n: int = HUMAN_BURNOUT_THRESHOLD,
                          exclude_indices: list[int] = None,
                          hacked_indices: list[int] = HACKED_SAMPLE_IDS) -> Union[None, pd.DataFrame]:
        df = self.df

        # Handle default arguments for exclude_indices and hacked_indices
        if exclude_indices is None:
            exclude_indices = []
        if hacked_indices is None:
            hacked_indices = []

        # Remove elements from hacked_indices that are also in exclude_indices
        hacked_indices = [idx for idx in hacked_indices if idx not in exclude_indices]

        # Exclude the rows with indices in exclude_indices when sampling
        available_indices = df.index.difference(exclude_indices + hacked_indices)
        # DONE - handle case when there is no more data to vote on
        if not available_indices.shape[0]:
            return None
        sampled_df = df.loc[available_indices].sample(
            n=min(available_indices.shape[0], n - len(hacked_indices))).copy()

        # If hacked_indices is not empty, shuffle them and include them in the sampled_df
        if hacked_indices:
            random.shuffle(hacked_indices)
            where = df[COL_DID].isin(hacked_indices)
            hacked_df = df.loc[where]
            sampled_df = pd.concat([hacked_df, sampled_df])

        # Shuffle the sampled_df and reset index, keeping hacked_indices on top if any
        sampled_df = sampled_df.sample(frac=1).reset_index(drop=True)
        if hacked_indices:
            where = sampled_df[COL_DID].isin(hacked_indices)
            hacked_df = sampled_df[where].copy().reset_index(drop=True)
            # sort by shuffled hacked indices
            hacked_df['sort_order'] = hacked_df[COL_DID].apply(lambda x: hacked_indices.index(x))
            hacked_df = hacked_df.sort_values('sort_order').drop(columns=['sort_order']).reset_index(drop=True)
            non_hacked_df = sampled_df[~where]
            sampled_df = pd.concat([hacked_df, non_hacked_df]).reset_index(drop=True)

        return sampled_df

    def get_df_sample(self, n: int = HUMAN_BURNOUT_THRESHOLD,
                      exclude_indices: list[int] = None,
                      hacked_indices: list[int] = HACKED_SAMPLE_IDS
                      ) -> Union[None, pd.DataFrame]:

        """
        sample N records, according to OpenAI's recommendation to not burn out human evaluators
        swap content of part of the columns
        :return:
        """

        sampled_df = self.get_hacked_sample(n, exclude_indices, hacked_indices)
        if sampled_df is None:
            return sampled_df

        # options order
        sampled_df[COL_OPTION_ORDER] = [[0, 1] for _ in range(len(sampled_df))]

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
        # sampled_df.loc[where_filter, COL_OPTION_ORDER] = [[1, 0] for _ in range(sum(where_filter))]
        sampled_df.loc[where_filter, COL_OPTION_ORDER] = (
            sampled_df.loc[where_filter, COL_OPTION_ORDER].apply(lambda x: [(~i + 2) for i in x]))

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
