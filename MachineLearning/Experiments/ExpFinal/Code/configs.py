# 文件位置
ANIME_PATH = './mal-anime/animes_sample0.4.csv'
RATING_PATH = './mal-anime/ratings_anime_sample0.4.csv'
MODEL_PATH = './model'
# 训练用超参数
ITERATIONS = 8000  # 迭代次数
BATCH_SIZE = 1024
LR = 1e-2  # 初始LR
ITERS_PER_EVAL = 200
ITERS_PER_LR_DECAY = 200
K = 20
LAMBDA = 1e-6
