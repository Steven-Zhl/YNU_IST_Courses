import pickle
from collections import Counter
from configs import PYTHON_PATHS, SQL_PATHS


# staqc：把语料中的单候选和多候选分隔开
def dataStaqcProcessing(filepath, save_single_path, save_multiple_path):
    with open(filepath, 'r') as f:
        total_data = eval(f.read())
        f.close()

    result = Counter([total_data[i][0][0] for i in range(len(total_data))])
    total_data_single = [total_data[i] for i in range(len(total_data)) if result[total_data[i][0][0]] == 1]
    total_data_multiple = [total_data[i] for i in range(len(total_data)) if result[total_data[i][0][0]] != 1]

    with open(save_single_path, "w") as f:
        f.write(str(total_data_single))
    with open(save_multiple_path, "w") as f:
        f.write(str(total_data_multiple))


def dataLargeProcessing(filepath, save_single_path, save_multiple_path):  # large:把语料中的但候选和多候选分隔开
    total_data = pickle.load(open(filepath, 'rb'), encoding='iso-8859-1')
    print(len(total_data))
    qids = [total_data[i][0][0] for i in range(len(total_data))]
    result = Counter(qids)
    print(len(qids))

    total_data_single = [total_data[i] for i in range(len(total_data)) if result[total_data[i][0][0]] == 1]
    print(len(total_data_single))
    total_data_multiple = [total_data[i] for i in range(len(total_data)) if result[total_data[i][0][0]] != 1]

    with open(save_single_path, 'wb') as f:
        pickle.dump(total_data_single, f)
    with open(save_multiple_path, 'wb') as f:
        pickle.dump(total_data_multiple, f)


def singleUnlabeled2label(input_path, save_path):  # 把单候选只保留其qid
    total_data = pickle.load(open(input_path, 'rb'), encoding='iso-8859-1')
    labels = [[total_data[i][0], 1] for i in range(len(total_data))]

    total_data_sort = sorted(labels, key=lambda x: (x[0], x[1]))
    with open(save_path, "w") as f:
        f.write(str(total_data_sort))


if __name__ == "__main__":
    """地狱绘卷....这里就算了"""
    # 将staqc_python中的单候选和多候选分开
    staqc_python_path = '../hnn_process/ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_single_save = '../hnn_process/ulabel_data/staqc/single/python_staqc_single.txt'
    staqc_python_multiple_save = '../hnn_process/ulabel_data/staqc/multiple/python_staqc_multiple.txt'
    dataStaqcProcessing(staqc_python_path, staqc_python_single_save, staqc_python_multiple_save)

    # 将staqc_sql中的单候选和多候选分开
    staqc_sql_path = '../hnn_process/ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_single_save = '../hnn_process/ulabel_data/staqc/single/sql_staqc_single.txt'
    staqc_sql_multiple_save = '../hnn_process/ulabel_data/staqc/multiple/sql_staqc_multiple.txt'
    dataStaqcProcessing(staqc_sql_path, staqc_sql_single_save, staqc_sql_multiple_save)

    # 将large_python中的单候选和多候选分开
    large_python_path = '../hnn_process/ulabel_data/python_codedb_qid2index_blocks_unlabeled.pickle'
    large_python_single_save = '../hnn_process/ulabel_data/large_corpus/single/python_large_single.pickle'
    large_python_multiple_save = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    dataLargeProcessing(large_python_path, large_python_single_save, large_python_multiple_save)

    # 将large_sql中的单候选和多候选分开
    large_sql_path = '../hnn_process/ulabel_data/sql_codedb_qid2index_blocks_unlabeled.pickle'
    large_sql_single_save = '../hnn_process/ulabel_data/large_corpus/single/sql_large_single.pickle'
    large_sql_multiple_save = '../hnn_process/ulabel_data/large_corpus/multiple/sql_large_multiple.pickle'
    dataLargeProcessing(large_sql_path, large_sql_single_save, large_sql_multiple_save)

    large_sql_single_label_save = '../hnn_process/ulabel_data/large_corpus/single/sql_large_single_label.txt'
    large_python_single_label_save = '../hnn_process/ulabel_data/large_corpus/single/python_large_single_label.txt'
    singleUnlabeled2label(large_sql_single_save, large_sql_single_label_save)
    singleUnlabeled2label(large_python_single_save, large_python_single_label_save)
