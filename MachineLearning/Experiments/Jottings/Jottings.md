# 《机器学习》实验中的一些问题与技巧

> 这些问题和技巧主要与Python的特性相关。

## Matplotlib

### 1. `MatplotlibDeprecationWarning`

> 2023-03-10 记录

* 提示内容：
  * `MatplotlibDeprecationWarning: Support for FigureCanvases without a required_interactive_framework attribute was deprecated in Matplotlib 3.6 and will be removed two minor releases later.`
* 原因：
  * 较为新版的`matplotlib`支持并建议使用交互式绘图（类似于Matlab中，生成一个可交互的窗口Figure用于展示图片/模型并交互）
  * 此外，上文还提到将在Matplotlib 3.6的两个小版本更新后移除对于非交互式绘图的支持。
  * 但是，目前在网上找到的大多数教程都忽略了这一点，仍然抱着“能用就行，Warning无用”的态度因循守旧，这是非常偷懒的一种行为。
* 解决方法：
  * 启用交互式绘图只需要给matplotlib指定绘图后端即可，如下所示：

    ```python
    import matplotlib
    
    matplotlib.use('TkAgg')
    # 'TkAgg'使用的是Tkinter，Python自带GUI，免安装。也可以使用'Qt5Agg'，但是需要当前环境中已经安装PyQt5
    ```

* 效果展示
  * 非交互式绘图
    * ![非交互式绘图](./IMG/MatplotlibDeprecationWarning_1.png)
  * TkAgg交互式绘图
    * ![TkAgg交互式绘图](./IMG/MatplotlibDeprecationWarning_2.png)
  * PyQt5交互式绘图
    * ![PyQt5交互式绘图](./IMG/MatplotlibDeprecationWarning_3.png)
  * 二者没有太大区别，但理论上PyQt5的性能应当优于Tkinter。

## graphviz

> graphviz是一个相较于Matplotlib性能更高的绘图工具(似乎叫引擎更合适)，唯一不好的一点是需要安装。

### 1. `graphviz.backend.ExecutableNotFound`

* 原因：
  * 未安装graphviz(它除了pip库，还需要额外安装后端)或未将安装路径的bin目录添加到环境变量中
* 解决方法：
  * 没安装就去安装，安装了检查环境变量中是否包含了graphviz的bin目录路径

## pandas

### 1. `UserWarning`

* 提示内容：
  * `UserWarning: X does not have valid feature names, but * was fitted with feature names`
* 原因：
  * 在使用机器学习/深度学习相关库时，由于Python本身弱数据类型的特点以及`pandas`、`numpy`和`matplotlib`三者之间良好的兼容性，我们经常会忽视掉数据类型的问题，但这个问题就是因为数据类型的差异导致的。
  * 这个Warning的意思是某个变量`X`没有`feature names`，但你调用的某个模型却是根据有`feature names`的数据训练的。
  * 这个问题经常出现在机器学习中，比如使用`sklearn`训练模型时，数据直接使用了`pandas`的`DataFrame`类型，但之后的一些运算(如`sklearn.svm.SVC.score()`)的输入却是`numpy.ndarray`类型，这就导致了这个Warning。
  * 不过注意到，这个问题只是一个Warning，并不会影响程序的运行，但即使这样，放任Warning也是个很不好的习惯。
* 解决方法：
  * 很简单，只需要在数据预处理的过程中额外添加一步，将`DataFrame`转换为`numpy.ndarray`，(通常直接套一个`numpy.array()`即可)。
    * > 不建议将`numpy.ndarray`转换为`DataFrame`，因为`DataFrame`中有`feature name`属性，这么转换会增加很多无谓的麻烦。

## gensim

> gensim是一个自然语言处理的工具包，能够从原始的非结构化的文本中，无监督地学习到文本隐层的主题向量表达。通常用于语料处理。

### 1.  `AttributeError`

* 提示内容：
  * `AttributeError: The vocab attribute was removed from KeyedVector in Gensim 4.0.0.`
  * `Use KeyedVector's .key_to_index dict, .index_to_key list, and methods .get_vecattr(key, attr) and .set_vecattr(key, attr, new_val) instead.`
* 原因：
  * 说的很明白了，在Gensim 4.0.0之后，`Word2Vec.wv.vocab`已被移除，需要用提供的几种方法替换。
  * 那么如何确定该换用哪个方法呢？建议debug看看这几种方法的返回值，确定哪个是自己需要的。

## Tensorboard

> Tensorboard是Tensorflow的可视化工具，谷歌出品，流畅且美观，秒杀plt和graphviz。
>
> 但稍微有些小坑

### 1. 代码中调用Tensorflow

> 下面给出在两个主流框架中，调用Tensorboard的示例代码

* PyTorch+Tensorboard

```python
from torch.utils.tensorboard import SummaryWriter

......

writer = SummaryWriter(log_dir='AlexNet_Logs') # 数据log的输出路径，该路径是相对于当前文件而言的
for epoch in range(EPOCHS):
    ......
    loss = criterion(outputs, labels) # 计算损失
    accuracy = (outputs.argmax(1) == labels).sum().item() / BATCH_SIZE # 计算准确率
    ...... # 更新权重之类的
    writer.add_scalar('Train/Loss', loss.item(), global_step=step)
    writer.add_scalar('Train/Accuracy', accuracy, global_step=step)
```

* Tensorflow+Tensorboard

```python
from keras.callbacks import TensorBoard
import tensorflow as tf

......

writer = tf.summary.create_file_writer(log_dir='LSTM_Logs') # 数据log的输出路径，该路径是相对于当前文件而言的
tb_callback = TensorBoard(log_dir='LSTM_Logs', histogram_freq=1, write_graph=True, write_images=True) # 创建一个回调，用于提供Tensorboard数据
model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, callbacks=[tb_callback]) # 在fit中指定回调

......

```

### 2. 命令行启动tensorboard

> 注意，请保证完整路径中不包含中文、特殊符号等。

```shell
# 先cd到执行的代码的目录
cd /home/Experiments/Code
tensorboard --logdir="AlexNet_Logs" # 指定数据log的路径
```

随后就可以在浏览器中打开[`http://localhost:6006/`](http://localhost:6006/)查看数据了。
