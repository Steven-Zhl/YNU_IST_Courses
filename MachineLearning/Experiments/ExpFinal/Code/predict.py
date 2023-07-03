import pandas as pd
import torch
from tabulate import tabulate

import utils
from configs import RATING_PATH, ANIME_PATH

USER_ID = 52  # 被推荐的用户ID
NUM_RECS = 10  # 推荐的数量


def predict(user_id, num_recs, model_file: str = "./model/LightGCN_8000.pth"):
    model = torch.load(model_file)
    model.eval()

    anime = pd.read_csv(ANIME_PATH)
    anime_id_title = pd.Series(anime.title.values, index=anime.anime_id).to_dict()
    anime_id_genres = pd.Series(anime.genres.values, index=anime.anime_id).to_dict()

    user_mapping = utils.loadNodes(RATING_PATH, index_col='user_id')
    anime_mapping = utils.loadNodes(ANIME_PATH, index_col='anime_id')
    edge_index = utils.loadEdges(RATING_PATH, user_mapping=user_mapping, anime_mapping=anime_mapping,
                                 user_id_col='user_id', anime_index_col='anime_id', link_index_col='rating')
    user_pos_items = utils.getUserPositiveItems(edge_index)
    user = user_mapping[user_id]
    e_u = model.users_emb.weight[user]
    scores = model.items_emb.weight @ e_u

    values, indices = torch.topk(scores, k=len(user_pos_items[user]) + num_recs)

    animes = [index.cpu().item() for index in indices if index in user_pos_items[user]][:num_recs]
    anime_ids = [list(anime_mapping.keys())[list(anime_mapping.values()).index(anime)] for anime in animes]
    titles = [anime_id_title[id] for id in anime_ids]
    genres = [anime_id_genres[id] for id in anime_ids]

    print(f"以下是针对用户{user_id}，最推荐的{num_recs}部动画")
    print(tabulate(list(zip(titles, genres)), headers=["Title", "Genres"]))


predict(USER_ID, NUM_RECS)
