__doc__ = """构建初步词典的具体步骤1"""


def getVocab(corpus1, corpus2):  # 使用列表生成式优化先前繁琐的嵌套循环
    word_vocab = set()
    word_vocab.update([word for _, (_, words1, words2), words3, words4 in corpus1 for word in
                       words1[0] + words1[1] + words2[0] + words3 + words4])
    word_vocab.update([word for _, (_, words1, words2), words3, words4 in corpus2 for word in
                       words1[0] + words1[1] + words2[0] + words3 + words4])

    print(len(word_vocab))
    return word_vocab


# 构建初步词典
def vocabProcessing(filepath1, filepath2, save_path):
    with open(filepath1, 'r') as f:
        total_data1 = eval(f.read())
        f.close()

    with open(filepath2, 'r') as f:
        total_data2 = eval(f.read())
        f.close()

    x1 = getVocab(total_data2, total_data2)
    total_data_sort = sorted(x1, key=lambda x: (x[0], x[1]))
    f = open(save_path, "w")
    f.write(str(x1))
    f.close()


def finalVocabProcessing(filepath1, filepath2, save_path):
    word_set = set()
    with open(filepath1, 'r') as f:
        total_data1 = set(eval(f.read()))
        f.close()
    with open(filepath2, 'r') as f:
        total_data2 = eval(f.read())
        f.close()
    total_data1 = list(total_data1)
    x1 = getVocab(total_data2, total_data2)

    word_set = set([x for x in x1 if x not in total_data1])
    print(len(total_data1))
    print(len(word_set))

    with open(save_path, "w") as f:
        f.write(str(word_set))


if __name__ == "__main__":
    # ====================获取staqc的词语集合===============
    python_hnn = '/home/gpu/RenQ/staqc/data_processing/hnn_process/data/python_hnn_data_teacher.txt'
    python_staqc = '/home/gpu/RenQ/staqc/data_processing/hnn_process/data/staqc/python_staqc_data.txt'
    python_word_dict = '/home/gpu/RenQ/staqc/data_processing/hnn_process/data/word_dict/python_word_vocab_dict.txt'

    sql_hnn = '/home/gpu/RenQ/staqc/data_processing/hnn_process/data/sql_hnn_data_teacher.txt'
    sql_staqc = '/home/gpu/RenQ/staqc/data_processing/hnn_process/data/staqc/sql_staqc_data.txt'
    sql_word_dict = '/home/gpu/RenQ/staqc/data_processing/hnn_process/data/word_dict/sql_word_vocab_dict.txt'

    # vocab_processing(python_hnn,python_staqc,python_word_dict)
    # vocab_processing(sql_hnn,sql_staqc,sql_word_dict)
    # ====================获取最后大语料的词语集合的词语集合===============
    new_sql_staqc = '../hnn_process/ulabel_data/staqc/sql_staqc_unlabeled_data.txt'
    new_sql_large = '../hnn_process/ulabel_data/large_corpus/multiple/sql_large_multiple_unsalable.txt'
    large_word_dict_sql = '../hnn_process/ulabel_data/sql_word_dict.txt'
    finalVocabProcessing(sql_word_dict, new_sql_large, large_word_dict_sql)
    # vocab_processing(new_sql_staqc,new_sql_large,final_word_dict_sql)

    new_python_staqc = '../hnn_process/ulabel_data/staqc/python_staqc_unlabeled_data.txt'
    new_python_large = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlabeled.txt'
    large_word_dict_python = '../hnn_process/ulabel_data/python_word_dict.txt'
    # final_vocab_processing(python_word_dict, new_python_large, large_word_dict_python)
    # vocab_processing(new_python_staqc,new_python_large,final_word_dict_python)
