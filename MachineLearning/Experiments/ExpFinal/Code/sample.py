__doc__ = """辅助函数，用于数据集的预处理和采样，如果显存足够的话可以不用"""

import pandas as pd

from configs import RATING_PATH, ANIME_PATH


def dispItmeNum():
    """
    查看数据集中的用户数量和动漫数量
    :return: None
    """
    user_id = pd.read_csv(RATING_PATH, usecols=['user_id'])
    print("用户数量：", len(set(user_id['user_id'])))
    anime_id = pd.read_csv(ANIME_PATH, usecols=['anime_id'])
    print("动漫数量：", len(set(anime_id['anime_id'])))


def dispRatingNum():
    """
    查看数据集中的评分数量
    :return: None
    """
    rating = pd.read_csv(RATING_PATH)
    print("评分数量：", len(rating))


def datasetPretreatment(rating_path=RATING_PATH, anime_path=ANIME_PATH):
    """
    由于原始数据集中，有些动漫有评分但不在anime的csv中，也有可能有的动漫没有评分数据；所以需要预处理数据集
    :return: None
    """
    rating = pd.read_csv(rating_path)
    anime = pd.read_csv(anime_path)
    print("--------------------原始数据--------------------")
    print("评分条目数：", len(rating))
    print("评分用户数：", len(set(rating['user_id'])))
    print("动漫条目数：", len(anime))
    print("动漫条目数(去重)：", len(set(anime['anime_id'])))

    # 处理
    anime = anime.drop_duplicates(subset=['anime_id'])  # 去除anime中的重复项
    rating = rating.dropna(axis=0, how='any')  # 去除rating中的空值
    rating = rating[rating['anime_id'].isin(anime['anime_id'])]  # 去除rating中anime_id不在anime中的项

    print("--------------------处理后数据--------------------")
    print("评分条目数：", len(rating))
    print("评分用户数：", len(set(rating['user_id'])))
    print("动漫条目数：", len(anime))
    print("动漫条目数(去重)：", len(set(anime['anime_id'])))

    return rating, anime


def datasetSampling(sample_rate: float):
    """
    由于原本数据量太大，完全使用原始数据需要约14GB显存，因此需要下采样
    :param sample_rate: 采样比例
    :return:
    """
    pre_rating, pre_anime = datasetPretreatment()  # 采样，从pre_anime中随机抽取sample_rate比例的样本
    sample_anime = pre_anime.sample(frac=sample_rate, replace=False, random_state=1)  # 选取在sample_anime中出现的rating
    sample_rating = pre_rating[pre_rating['anime_id'].isin(sample_anime['anime_id'])]
    return sample_rating, sample_anime


if __name__ == '__main__':
    SAMPLE_RATE = 0.4
    sample_rating, sample_anime = datasetSampling(sample_rate=SAMPLE_RATE)
    sample_rating.to_csv(f'/home/steven/Anime_LightGCN/mal-anime/ratings_anime_sample{SAMPLE_RATE}.csv', index=False)
    sample_anime.to_csv(f'/home/steven/Anime_LightGCN/mal-anime/animes_sample{SAMPLE_RATE}.csv', index=False)
