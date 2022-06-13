"""
    情绪推理接口

   @author TinaRoot
   @since 2022/6/13 下午3:09
"""

# 加载模型
modelPath = "/Users/tina/PycharmProjects/机器学习/tinaroot-ai/aiapp/file/mood.kpl"

from joblib import load
from aiapp import setting

logger = setting.LogConfig.logger
import jieba

model = load(modelPath)


def chinese_word_cut(mytext):
    """
        使用分词
   """
    data = " ".join(jieba.cut(mytext))
    logger.info('分词后的结果:{}', data)
    return data


def mood(txt):
    """
        推理情绪
    """
    data = chinese_word_cut(txt)
    list = [data]
    # 4和5星可以看作正向情绪，1和2是负向情绪
    #  正向情绪 1，0负向情绪
    result = model.predict(list)
    logger.info("推理文字情绪:{}", result)
    if result[0] == 0:
        return '你的情绪很不稳！请保持乐观哦'

    return '看起来你很开心，请继续保持哦！！！'


if __name__ == '__main__':
    print(mood('难过'))
