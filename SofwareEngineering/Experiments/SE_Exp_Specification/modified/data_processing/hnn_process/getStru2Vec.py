__doc__ = """并行分词"""

import pickle
import sys
from multiprocessing import Pool as ThreadPool  # 多进程

from configs import PYTHON_PATHS, SQL_PATHS, SPLIT_NUM
from pythonStructured import pythonCodeParse, pythonContextParse, pythonQueryParse  # 解析结构
from sqlangStructured import sqlangCodeParse, sqlangContextParse, sqlangQueryParse

sys.path.append("..")


class MultiPro:
    def query(self, data_list: list, lang: str):
        if lang == 'python':
            return [pythonQueryParse(line) for line in data_list]
        elif lang == 'sql':
            return [sqlangQueryParse(line) for line in data_list]
        else:
            raise ValueError('lang must be python or sql')

    def code(self, data_list: list, lang: str):
        if lang == 'python':
            return [pythonCodeParse(line) for line in data_list]
        elif lang == 'sql':
            return [sqlangCodeParse(line) for line in data_list]
        else:
            raise ValueError('lang must be python or sql')

    def context(self, data_list: list, lang: str):
        if lang == 'python':
            return [line if line == '-10000' else pythonContextParse(line) for line in data_list]
        elif lang == 'sql':
            return [line if line == '-10000' else sqlangContextParse(line) for line in data_list]
        else:
            raise ValueError('lang must be python or sql')


def parse(lang_type: str, data: list):
    def dataProcess(data: list, lang_type: str, data_type: str):
        """
        内部函数，对于4类数据进行处理
        :param data:待处理数据
        :param lang_type:语言类型,可选 'python','sql'
        :param data_type:数据类型,可选 'context','query','code'
        """
        if lang_type != 'python' and lang_type != 'sql':
            raise Exception('lang_type Error')
        multiPro = MultiPro()
        data_split_list = [data[i:i + SPLIT_NUM] for i in range(0, len(data), SPLIT_NUM)]
        pool = ThreadPool(10)
        if data_type == 'context':
            data_list = pool.map(multiPro.context(data_split_list, lang_type))
        elif data_type == 'query':
            data_list = pool.map(multiPro.query(data_split_list, lang_type))
        elif data_type == 'code':
            data_list = pool.map(multiPro.code(data_split_list, lang_type))
        else:
            raise Exception('data_type Error')
        pool.close()
        pool.join()
        return data_list

    if lang_type != 'python' and lang_type != 'sql':
        raise 'type error'

    acont1_data = [i[1][0][0] for i in data]
    acont2_data = [i[1][1][0] for i in data]
    query_data = [i[3][0] for i in data]
    code_data = [i[2][0][0] for i in data]

    acont1_cut = dataProcess(acont1_data, lang_type, 'context')
    acont2_cut = dataProcess(acont2_data, lang_type, 'context')
    query_cut = dataProcess(query_data, lang_type, 'query')
    code_cut = dataProcess(code_data, lang_type, 'code')
    qids = [i[0] for i in data]
    print('acont1条数：%d' % len(acont1_cut))
    print('acont2条数：%d' % len(acont2_cut))
    print('query条数：%d' % len(query_cut))
    print('code条数：%d' % len(code_cut))
    print('qids条数：%d' % len(qids), 'qids[0]:', qids[0])

    return acont1_cut, acont2_cut, query_cut, code_cut, qids


if __name__ == '__main__':
    """测试用"""
    lang_type = 'python'
    if lang_type == 'python':
        source_path = PYTHON_PATHS['LARGE_DICT']
        save_path = PYTHON_PATHS['LARGE_NEW']
    elif lang_type == 'sql':
        source_path = SQL_PATHS['LARGE_DICT']
        save_path = SQL_PATHS['LARGE_NEW']
    else:
        raise 'lang_type error'

    with open(source_path, "rb") as f:  # 存储为字典 有序
        corpus_lis = pickle.load(f)  # pickle
        parse_acont1, parse_acont2, parse_query, parse_code, qids = parse(lang_type, corpus_lis)
        total_data = [[qids[i], [parse_acont1[i], parse_acont2[i]], [parse_code[i]], parse_query[i]]
                      for i in range(len(qids))]
    with open(save_path, 'w') as f:
        f.write(str(total_data))
