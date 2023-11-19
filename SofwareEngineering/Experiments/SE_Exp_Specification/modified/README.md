# Codecs

> 该项目是软件工程课程中，针对“软件开发规则”这一主题的实践项目，主要内容是重构原始项目的代码，使其符合所学的开发规则。
>
> 原始项目(不含数据文件)，放在了[`/origin`](../origin/)路径中；
>
> 修改后的项目放在了[`/modified`](../modified/)路径中。

## 专有名词

* corpus: 语料库
* dict/word dict: 词典
* embedding: 嵌入，可简单理解为特征向量(不严谨的话)
* pad: 即padding，填充操作
* wv: word vector，词向量
* final: "最终"后缀，但带该后缀的变量通常用于保存

## 大致修改思路

* 调整代码格式(PyCharm中`Ctrl+Alt+L`自动优化格式)
* 使用reStructuredText格式编写函数注释
* 删除无用的import和函数
* 删除`from XX import *`的引用语句，显式指明引用
* 删除无用的初始化(有些显式设置的初始值与不设置时的默认值相同，即无用初始化)
* 删除某些旧时代的残余(比如为了兼容Python 2.X的`print`而引用的`__future__.print_function`)
* 删除仅定义无调用的函数(比如[getStru2Vec.py](./data_processing/hnn_process/getStru2Vec.py)中的`parse`,`parsePython`和`parseSqlang`函数，后两者和`parse`几乎完全相同且没有被调用过，遂直接删去)
* 将到处乱扔的常量放到`config.py`中，比如哪里都是的重复的路径声明(作者不会引用常量吗)
  * 附：尝试后放弃了....因为这些到处乱扔的路径几乎都存在细微差别(命名真是随心所欲啊)，只在[embeddingsProcess](data_processing/hnn_process/embeddingsProcess.py)中实现了这一设想，可以看看效果
* 将[models_biv_hnn](ANN_Staqc_new/models_biv_hnn.py), [models_text](ANN_Staqc_new/models_text.py)
  和[models_code](ANN_Staqc_new/models_code.py)中的`CodeMF`类修改为[models.`CodeMF`](ANN_Staqc_new/models.py)的子类
  * 因为它们除了`build`方法别的完全一样
* 将[main](ANN_Staqc_new/main.py)中的`StandoneCode`
  类修改为[unlabel2label_final.`StandoneCode`](ANN_Staqc_new/unlabel2label_final.py)的子类
* 将错误单词修改为正确的单词(如$bais\rightarrow bias;lable\rightarrow label;sigle\rightarrow single$等)
* 在构造函数中显式声明部分属性的初始值
* 命名规则
  * 类名：大驼峰
  * 函数名：小驼峰(特殊情况除外，如子类重写时)
  * 变量名：小写单词，下划线分隔
  * 常量名：大写单词，下划线分隔
* 可能有争议的两处改动：
  * 将简单的`for list.append`改为列表推导式
  * 将简单的`if else`改为三元表达式
  * > 列表推导式相较于`for list.append`效率更高(能够更快地构造`list`)，三元表达式能够更短地表达`if else`。但相比于传统写法，难免降低一些可读性。

## 文件名改动

> 左侧为原始文件名，右侧为修改后的文件名

| [origin](https://github.com/Steven-Zhl/SE_Exp_Specification/tree/origin)                                                                                                     | [new](https://github.com/Steven-Zhl/SE_Exp_Specification)                                                                                                             |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [/ANN_Staqc_new/LayerNormalization.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/LayerNormalization.py)                                   | [/ANN_Staqc_new/LayerNormalization.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/LayerNormalization.py)                               |
| [/ANN_Staqc_new/MultiHeadAttention.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/MultiHeadAttention.py)                                   | [/ANN_Staqc_new/MultiHeadAttention.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/MultiHeadAttention.py)                               |
| [/ANN_Staqc_new/PositionWiseFeedForward.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/PositionWiseFeedForward.py)                         | [/ANN_Staqc_new/PositionWiseFeedForward.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/PositionWiseFeedForward.py)                     |
| [/ANN_Staqc_new/Position_Embedding.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/Position_Embedding.py)                                   | [/ANN_Staqc_new/PositionEmbedding.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/PositionEmbedding.py)                                 |
| [/ANN_Staqc_new/attention_layer.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/attention_layer.py)                                         | [/ANN_Staqc_new/AttentionLayer.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/AttentionLayer.py)                                       |
| [/ANN_Staqc_new/concactLayer.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/concactLayer.py)                                               | [/ANN_Staqc_new/ConcactLayer.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/ConcactLayer.py)                                           |
| [/ANN_Staqc_new/configs.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/configs.py)                                                         | [/configs.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/configs.py)                                                                                 |
| [/ANN_Staqc_new/main.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/main.py)                                                               | [/ANN_Staqc_new/main.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/main.py)                                                           |
| [/ANN_Staqc_new/mediumlayer.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/mediumlayer.py)                                                 | [/ANN_Staqc_new/MediumLayer.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/MediumLayer.py)                                             |
| [/ANN_Staqc_new/models.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/models.py)                                                           | [/ANN_Staqc_new/models.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/models.py)                                                       |
| [/ANN_Staqc_new/models_biv_hnn.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/models_biv_hnn.py)                                           | [/ANN_Staqc_new/models_biv_hnn.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/models_biv_hnn.py)                                       |
| [/ANN_Staqc_new/models_code.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/models_code.py)                                                 | [/ANN_Staqc_new/models_code.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/models_code.py)                                             |
| [/ANN_Staqc_new/models_text.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/models_text.py)                                                 | [/ANN_Staqc_new/models_text.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/models_text.py)                                             |
| [/ANN_Staqc_new/selfattention.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/selfattention.py)                                             | [/ANN_Staqc_new/SelfAttention.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/SelfAttention.py)                                         |
| [/ANN_Staqc_new/unlable2lable_final.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/ANN_Staqc_new/unlable2lable_final.py)                                 | [/ANN_Staqc_new/unlabel2label_final.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/ANN_Staqc_new/unlable2lable_final.py)                             |
| [/data_processing/hnn_process/embddings_process.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/data_processing/hnn_process/embddings_process.py)         | [/data_processing/hnn_process/embeddingsProcess.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/data_processing/hnn_process/embeddingsProcess.py)     |
| [/data_processing/hnn_process/getStru2Vec.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/data_processing/hnn_process/getStru2Vec.py)                     | [/data_processing/hnn_process/getStru2Vec.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/data_processing/hnn_process/getStru2Vec.py)                 |
| [/data_processing/hnn_process/process_single_corpus.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/data_processing/hnn_process/process_single_corpus.py) | [/data_processing/hnn_process/processSingleCorpus.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/data_processing/hnn_process/processSingleCorpus.py) |
| [/data_processing/hnn_process/python_structured.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/data_processing/hnn_process/python_structured.py)         | [/data_processing/hnn_process/pythonStructured.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/data_processing/hnn_process/pythonStructured.py)       |
| [/data_processing/hnn_process/sqlang_structured.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/data_processing/hnn_process/sqlang_structured.py)         | [/data_processing/hnn_process/sqlangStructured.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/data_processing/hnn_process/sqlangStructured.py)       |
| [/data_processing/hnn_process/word_dict.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/origin/data_processing/hnn_process/word_dict.py)                         | [/data_processing/hnn_process/wordDict.py](https://github.com/Steven-Zhl/SE_Exp_Specification/blob/new/data_processing/hnn_process/wordDict.py)                       |

## 附加说明

* ChatGPT对于本项目的分析结果：[ChatGPT分析结果](./ChatGPT分析报告.md)
  * Powered by：
    * [GPT 学术优化 (GPT Academic)](https://github.com/binary-husky/gpt_academic)
    * ChatGPT 3.5 turbo API
