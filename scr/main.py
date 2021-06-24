from stats_can import StatsCan
import pandas as pd
import sys
if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile


def get_stats_can_data(table: str):
    """

    :param sc: statscan instance
    :param table: (str) contains the table number associated with
                    table in Statistics Canada
    :return: stats_df: (dataframe object) dataframe returned after
                    downloading data
    """
    # Initialize StatsCan instance
    sc = StatsCan()
    stats_df = sc.table_to_df(table)
    print(sc.downloaded_tables)

    return stats_df


def main():
    """
    Main program
    :return:
    """
    # Sample getting data with StatsCan -
    # https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810020502
    table = "46-10-0043-01"
    housing_price_index = get_stats_can_data(table)
    print(housing_price_index.head())

    # Sample reading data from downloaded file
    #relative_path_sm_res = "./ExploringHousingData/data/46100038.csv"
    #single_multiple_residence_df = pd.read_csv(relative_path_sm_res)
    #print(single_multiple_residence_df.head())


if __name__ == '__main__':
    pass
