import csv
import os

from pandas import read_csv
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel

CSV_PATH = "comments.csv"
PREDICT_CSV_PATH = "ChatGLM_int4_predict.csv"
CHATGLM_MODEL_PATH = "ChatGLM-6B-INT4"


class ChatGLM6B:
    def __init__(self, dataPath: str, modelPath: str, resultPath: str):
        """
        ChatGLM调用类
        :param modelPath: ChatGLM-6B项目路径(含模型)
        """
        self.originData = read_csv(dataPath)  # 原始数据集
        if not os.path.exists(resultPath):
            with open(resultPath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["comments", "label", "ChatGLM_predict", "label_predict"])
        self.predictedData = read_csv(resultPath)  # 已判断的数据
        self.unpredictedData = self.originData[~self.originData.isin(self.predictedData)].dropna()  # 未判断的数据
        # 实例化模型
        self.tokenizer = AutoTokenizer.from_pretrained(modelPath, trust_remote_code=True, revision="")
        self.model = (AutoModel.from_pretrained(modelPath, trust_remote_code=True, revision="").half().cuda())

    def answer(self):
        """
        要求ChatGLM判断对话的情感极性
        :return: ChatGLM的回答(自然语言)
        """
        results = []
        prefix = "对于下面这段话，请判断其情感是积极还是消极，直接给出判断结果，不要做出任何分析"
        try:
            for i in tqdm(range(len(self.unpredictedData))):
                comment, label = self.unpredictedData.iloc[i]
                self.model = self.model.eval()
                ans, _ = self.model.chat(self.tokenizer, f"{prefix}：“{comment}”", [])
                results.append([comment, int(label), ans, self.analysisAns(ans)])
        except KeyboardInterrupt:
            dumpCsv(results)
            print(f"本次处理数据已保存至{PREDICT_CSV_PATH}")
            accuracy = len([i for i in results if i[1] == i[3]]) / len(results)
            print("本次判断%d条数据，准确率为%.2f%%" % (len(results), accuracy * 100))
            dispAccuracy()
            exit(0)

    @staticmethod
    def analysisAns(ans: str) -> int:
        if "积极" in ans[:15]:
            return 1
        elif "消极" in ans[:15]:
            return 0
        else:
            return -1


def dispAccuracy() -> float:
    """计算并显示ChatGLM的总准确率"""
    data = read_csv(PREDICT_CSV_PATH)
    validData = data[data["label_predict"] != -1]  # 扔掉label_predict为-1的数据
    correctData = validData[validData['label'] == validData['label_predict']]
    accuracy = len(correctData) / len(validData)
    print("当前共有%d条数据，其中有效数据%d条，判断正确%d条，总准确率为%.2f%%。" % (
        len(data), len(validData), len(correctData), accuracy * 100))
    return accuracy


def dumpCsv(data: list[list], fileName: str = PREDICT_CSV_PATH):
    """
    将数据写入csv文件
    :param data: 数据，格式为[[comments, label, ChatGLM_predict, label_predict], ...]
    :param fileName: 文件名
    :return: None
    """
    with open(fileName, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    chatGLM = ChatGLM6B(CSV_PATH, CHATGLM_MODEL_PATH, PREDICT_CSV_PATH)
    chatGLM.answer()
