"""
    文本工具
    @author tinaroot.cn
    @time 2022/6/11 0:15
"""

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import jieba


def cutWord(sen):
    """
            切词
            @author tinaroot
            @since 2022-6-11 0:29
            @param data 列表数据
            @return list
    """
    return " ".join((jieba.cut(sen)))


def participle(data):
    """
        分词
        @author tinaroot
        @since 2022-6-11 0:29
        @param data 列表数据
        @return list
    """
    txtList = []

    for a in data:
        txtList.append(cutWord(a))

    transfer = TfidfVectorizer()
    transfer_data = transfer.fit_transform(txtList)

    print(type(transfer.get_feature_names()))
    # print(transfer.get_feature_names())
    # print(transfer_data.toarray())
    return transfer.get_feature_names()
