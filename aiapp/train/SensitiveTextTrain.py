"""
    敏感文本模型训练
    @author tinaroot
    @since 2022/6/12 14:21
    @version 9999
"""
import pandas as pd


def linear():
    """
        使用岭回归训练模型
    """
    df = pd.read_csv('../file/敏感检测词汇.csv', encoding='gb18030')
    print(df.head())
    print(df.shape)

    def make_label(df):
        df["sentiment"] = df["star"].apply(lambda x: 1 if x > 3 else 0)


if __name__ == '__main__':
    linear()
