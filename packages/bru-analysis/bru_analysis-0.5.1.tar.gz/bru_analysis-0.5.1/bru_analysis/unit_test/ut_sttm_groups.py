import unittest
import pandas as pd
from bru_analysis.sttm_groups import sttm
from bru_analysis.common.nlp_utils import CleanText

FOLDER_DATA = '/home/oscar/Labs'
FILE = '/bru_analysis/bru_analysis/ft_test/data/Facebook/facebook_lib_facebook_comments.csv'
SAMPLE = 500


class TestSttm(unittest.TestCase):
    """
    This unit test emotion and sentiment calcule in bru_analytis and bru_models
    """

    def setUp(self):
        """
        This function prepare data to analysis and test
        """
        print('Setup')

        self.df_e = pd.read_csv(f'{FOLDER_DATA}{FILE}')
        self.df_e = self.df_e.sample(n=SAMPLE)

        self.df_e['clean_text'] = self.df_e['message'].apply(lambda x: CleanText(x).process_text())

        print('Ok')
        print(''.center(60, '-'))

    def test_normal(self):
        """
        This test dataframe output length is equal input dataframe
        """

        print('Test normal data')

        df_sttm = sttm(df_p=self.df_e,
                       batch=50).sttm_groups()

        self.assertEqual(len(df_sttm.columns), 3)
        self.assertEqual(len(df_sttm), len(self.df_e))

        print('Ok')
        print(''.center(60, '-'))

    def test_empty(self):
        """
        This test generate a exception if input dataframe is empty but return length = 0 dataframe output
        """

        print('Test empty data')

        df_empty = pd.DataFrame(columns=self.df_e.columns)

        df_sttm = sttm(df_p=df_empty,
                       batch=5).sttm_groups()

        self.assertEqual(len(df_sttm), 0)

        print('Ok')
        print(''.center(60, '-'))


if __name__ == "__main__":
    unittest.main()
