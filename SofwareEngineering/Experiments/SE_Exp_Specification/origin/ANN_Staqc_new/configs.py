#跑模型运行的配置
def get_config(train):
    conf = {
        'workdir': '../train_data/new/origin_model/'+train+'/',
        'buckets':[(2, 10, 22, 72), (2, 20, 34, 102), (2, 40, 34, 202), (2, 100, 34, 302)],
        'data_params':{
            #training data
            "train_path":'../data/new_data_hnn/'+train+'/hnn_'+train+'_train_f.pkl',
            #valid data
            'valid_path':'../data/new_data_hnn/'+train+'/hnn_'+train+'_dev_f.pkl',
            #test data
            'test_path':'../data/new_data_hnn/'+train+'/hnn_'+train+'_test_f.pkl',

            'code_pretrain_emb_path':'../data/new_data_hnn/'+train+'/'+train+'_word_vocab_final.pkl',
            'text_pretrain_emb_path': '../data/new_data_hnn/' + train + '/'+train+'_word_vocab_final.pkl'
        },               
        'training_params': {           
            'batch_size': 100,
            'nb_epoch':150,
            # 'optimizer':5 'adam',
            #'optimizer': Adam(clip_norm=0.1),

            'n_eval': 100,
            'evaluate_all_threshold': {
                'mode': 'all',
                'top1': 0.4,
            },
            'reload':0, #epoch that the model is reloaded from . If reload=0, 然后从头开始训练
            'dropout1': 0,
            'dropout2': 0,
            'dropout3': 0,
            'dropout4': 0,
            'dropout5': 0,
            'regularizer': 0,

        },

        'model_params': {
            'model_name':'CodeMF',
        }        
    }
    return conf



#打标签运行的配置
def get_config_u2l(train):
    conf = {
        'workdir': '../train_data/new/fianl/code_sa/'+train+'/',
        #'workdir': '../train_data/new/fianl/text_sa/'+train+'/',
        #'workdir': '../train_data/new/fianl/SACodeMF/'+train+'/',
        'buckets':[(2, 10, 22, 72), (2, 20, 34, 102), (2, 40, 34, 202), (2, 100, 34, 302)],
        'data_params':{
            #training data
            "train_path":'../data/new_data_hnn/'+train+'/hnn_'+train+'_train_f.pkl',
            #valid data
            'valid_path':'../data/new_data_hnn/'+train+'/hnn_'+train+'_dev_f.pkl',
            #test data
            'test_path':'../data/new_data_hnn/'+train+'/hnn_'+train+'_test_f.pkl',

            #原始Staqc打标签的词向量地址
            #'code_pretrain_emb_path':'../data/new_data_hnn/'+train+'/'+train+'_word_vocab_final.pkl',
            #'text_pretrain_emb_path': '/home/gpu/RenQ/stqac/data/new_data_hnn/' + train + '/'+train+'_word_vocab_final.pkl',

            #SQL：最后的大语料-打标签的词向量地址
            #'code_pretrain_emb_path':'../data_processing/hnn_process/ulabel_data/large_corpus/sql_word_vocab_final.pkl',
            #'text_pretrain_emb_path':'../data_processing/hnn_process/ulabel_data/large_corpus/sql_word_vocab_final.pkl'

            #Python：最后的大语料-打标签的词向量地址
            'code_pretrain_emb_path':'../data_processing/hnn_process/ulabel_data/large_corpus/python_word_vocab_final.pkl',
            'text_pretrain_emb_path':'../data_processing/hnn_process/ulabel_data/large_corpus/python_word_vocab_final.pkl'

        },
        'training_params': {
            'batch_size': 100,
            'nb_epoch':150,
            # 'optimizer':5 'adam',
            #'optimizer': Adam(clip_norm=0.1),

            'n_eval': 100,
            'evaluate_all_threshold': {
                'mode': 'all',
                'top1': 0.4,
            },
            'reload':0, #epoch that the model is reloaded from . If reload=0, 然后从头开始训练
            'dropout1': 0,
            'dropout2': 0,
            'dropout3': 0,
            'dropout4': 0,
            'dropout5': 0,
            'regularizer': 0,

        },

        'model_params': {
            'model_name':'CodeMF',
        }
    }
    return conf




