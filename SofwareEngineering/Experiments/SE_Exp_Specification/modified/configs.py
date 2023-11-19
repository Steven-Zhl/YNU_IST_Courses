__doc__ = """跑模型运行的配置"""
# getConfig_u2l内部改不了，似乎是通过手动注释的方式来修改workdir、code_pretrain_emb_path和text_pretrain_emb_path的。这里一旦改名后，
# 由于对应的被调部分不会随着更改，一定会跑不起来的。
# 一些路径常量(注：从data_processing.hnn_process.embeddings_process.py中整理复制而来)
PYTHON_PATHS = {
    'PYTHON_WORD': 'data_processing/hnn_process/data/word_dict/python_word_vocab_dict.txt',
    'WV': 'data_processing/hnn_process/embeddings/python/python_word_vocab_final.pkl',
    'WORD': 'data_processing/hnn_process/embeddings/python/python_word_dict_final.pkl',
    # python 待处理语料地址
    'STAQC_NEW': 'data_processing/hnn_process/ulabel_data/staqc/python_staqc_unlabeled_data.txt',
    'STAQC_DICT': 'data_processing/hnn_process/ulabel_data/staqc/python_word_dict.txt',
    'LARGE_NEW': 'data_processing/hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlabeled.txt',
    'LARGE_DICT': 'data_processing/hnn_process/ulabel_data/large_corpus/python_word_dict.txt',
    # python最后的词典
    'WV_SAVE': 'data_processing/hnn_process/ulabel_data/python_word_vocab_final.pkl',
    'WORD_SAVE': 'data_processing/hnn_process/ulabel_data/python_word_dict.txt',  # python最后的词典和对应的词向量
    # 处理成打标签的形式
    'STAQC_F': 'data_processing/hnn_process/ulabel_data/staqc/seri_python_staqc_unlabeled_data.pkl',
    'LARGE_F': 'data_processing/hnn_process/ulabel_data/large_corpus/multiple/seri_python_large_multiple_unlabeled.pkl'
}
SQL_PATHS = {
    'SQL_WORD': 'data_processing/hnn_process/data/word_dict/sql_word_vocab_dict.txt',
    'WV': 'data_processing/hnn_process/embeddings/sql/sql_word_vocab_final.pkl',
    'WORD': 'data_processing/hnn_process/embeddings/sql/sql_word_dict_final.pkl',
    # sql 待处理语料地址
    'STAQC_NEW': 'data_processing/hnn_process/ulabel_data/staqc/sql_staqc_unlabeled_data.txt',
    'STAQC_DICT': 'data_processing/hnn_process/ulabel_data/staqc/sql_word_dict.txt',
    'LARGE_NEW': 'data_processing/hnn_process/ulabel_data/large_corpus/multiple/sql_large_multiple_unlabeled.txt',
    'LARGE_DICT': 'data_processing/hnn_process/ulabel_data/large_corpus/sql_word_dict.txt',  # sql大语料最后的词典
    # sql最后的词典和对应的词向量
    'WV_SAVE': 'data_processing/hnn_process/ulabel_data/sql_word_vocab_final.pkl',
    'WORD_SAVE': 'data_processing/hnn_process/ulabel_data/sql_word_dict_final.pkl',
    # 处理成打标签的形式
    'STAQC_F': 'data_processing/hnn_process/ulabel_data/staqc/seri_sql_staqc_unlabeled_data.pkl',
    'LARGE_F': 'data_processing/hnn_process/ulabel_data/large_corpus/multiple/seri_ql_large_multiple_unlabeled.pkl'
}
PATHS = {
    'PS': 'data_processing/hnn_process/embeddings/10_10/python_struc2vec1/data/python_struc2vec.txt',
    'PS_BIN': 'data_processing/hnn_process/embeddings/10_10/python_struc2vec.bin',
    'SQL': 'data_processing/hnn_process/embeddings/10_8_embeddings/sql_struc2vec.txt',
    'SQL_BIN': 'data_processing/hnn_process/embeddings/10_8_embeddings/sql_struc2vec.bin',
    'LARGE_SINGLE': 'data_processing/hnn_process/ulabel_data/large_corpus/single/sql_large_single_label.txt'
}

RANDOM_SEED = 42  # 发现虽然很多文件中都声明了seed，但都统一为42，所以统一放在这里
CODE_LENGTH = 350  # (也许是)语料长度阈值
TEXT_LENGTH = 100  # (也许是)文本长度阈值
QUERIES_LENGTH = 25  # 问题长度阈值
TEXT_BLOCK_LENGTH = 2  # 文本块长度阈值
WORDS_TOP = 100  # 从getStru2Vec中引入的常量
SPLIT_NUM = 1000


def getConfig(train):
    conf = {
        'workdir': '../train_data/new/origin_model/' + train + '/',
        'buckets': [(2, 10, 22, 72), (2, 20, 34, 102), (2, 40, 34, 202), (2, 100, 34, 302)],
        'data_params': {
            "train_path": 'ANN_Staqc_new/data/new_data_hnn/' + train + '/hnn_' + train + '_train_f.pkl',
            'valid_path': 'ANN_Staqc_new/data/new_data_hnn/' + train + '/hnn_' + train + '_dev_f.pkl',
            'test_path': 'ANN_Staqc_new/data/new_data_hnn/' + train + '/hnn_' + train + '_test_f.pkl',

            'code_pretrain_emb_path': 'ANN_Staqc_new/data/new_data_hnn/' + train + '/' + train + '_word_vocab_final.pkl',
            'text_pretrain_emb_path': 'ANN_Staqc_new/data/new_data_hnn/' + train + '/' + train + '_word_vocab_final.pkl'
        },
        'training_params': {
            'batch_size': 100,
            'nb_epoch': 150,
            # 'optimizer':5 'adam',
            # 'optimizer': Adam(clip_norm=0.1),

            'n_eval': 100,
            'evaluate_all_threshold': {
                'mode': 'all',
                'top1': 0.4,
            },
            'reload': 0,  # epoch that the model is reloaded from . If reload=0, 然后从头开始训练
            'dropout1': 0,
            'dropout2': 0,
            'dropout3': 0,
            'dropout4': 0,
            'dropout5': 0,
            'regularizer': 0,

        },

        'model_params': {
            'model_name': 'CodeMF',
        }
    }
    return conf


# 打标签运行的配置
def getConfig_u2l(train):
    conf = {
        'workdir': '../train_data/new/final/code_sa/' + train + '/',
        # 'workdir': '../train_data/new/final/text_sa/'+train+'/',
        # 'workdir': '../train_data/new/final/SACodeMF/'+train+'/',
        'buckets': [(2, 10, 22, 72), (2, 20, 34, 102), (2, 40, 34, 202), (2, 100, 34, 302)],
        'data_params': {
            "train_path": 'ANN_Staqc_new/data/new_data_hnn/' + train + '/hnn_' + train + '_train_f.pkl',
            'valid_path': 'ANN_Staqc_new/data/new_data_hnn/' + train + '/hnn_' + train + '_dev_f.pkl',
            'test_path': 'ANN_Staqc_new/data/new_data_hnn/' + train + '/hnn_' + train + '_test_f.pkl',

            # 原始Staqc打标签的词向量地址
            # 'code_pretrain_emb_path':'ANN_Staqc_new/data/new_data_hnn/'+train+'/'+train+'_word_vocab_final.pkl',
            # 'text_pretrain_emb_path': '/home/gpu/RenQ/staqc/data/new_data_hnn/' + train + '/'+train+'_word_vocab_final.pkl',

            # SQL：最后的大语料-打标签的词向量地址
            # 'code_pretrain_emb_path':'ANN_Staqc_new/data_processing/hnn_process/ulabel_data/large_corpus/sql_word_vocab_final.pkl',
            # 'text_pretrain_emb_path':'ANN_Staqc_new/data_processing/hnn_process/ulabel_data/large_corpus/sql_word_vocab_final.pkl'

            # Python：最后的大语料-打标签的词向量地址
            'code_pretrain_emb_path': 'data_processing/hnn_process/ulabel_data/large_corpus/python_word_vocab_final.pkl',
            'text_pretrain_emb_path': 'data_processing/hnn_process/ulabel_data/large_corpus/python_word_vocab_final.pkl'
        },
        'training_params': {
            'batch_size': 100,
            'nb_epoch': 150,
            # 'optimizer':5 'adam',
            # 'optimizer': Adam(clip_norm=0.1),

            'n_eval': 100,
            'evaluate_all_threshold': {
                'mode': 'all',
                'top1': 0.4,
            },
            'reload': 0,  # epoch that the model is reloaded from . If reload=0, 然后从头开始训练
            'dropout1': 0,
            'dropout2': 0,
            'dropout3': 0,
            'dropout4': 0,
            'dropout5': 0,
            'regularizer': 0,

        },

        'model_params': {
            'model_name': 'CodeMF',
        }
    }
    return conf
