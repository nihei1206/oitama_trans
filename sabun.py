# -*- coding: utf-8 -
import pandas as pd

def execute():
    df1 = pd.read_csv('sudachi_oitama_dict_verbs_1.0.csv')
    df2 = pd.read_csv('sudachi_oitama_dict_verbs_1.2.csv')
    diff_df = dataframe_difference(df1, df2)
    diff_df.to_csv('./outputCSV/diff_verbs.csv')

def dataframe_difference(df1, df2, which=None):
    """Find rows which are different between two DataFrames."""
    comparison_df = df1.merge(df2,
                              indicator=True,
                              how='outer')
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    return diff_df
    # return comparison_df

if __name__ == '__main__':
    execute()