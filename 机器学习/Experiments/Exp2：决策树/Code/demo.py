import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV
import sklearn.ensemble as ensemble
from sklearn import tree
import numpy as np

# PassengerId（乘客ID），Name（姓名），Ticket（船票信息）存在唯一性，三类意义不大，可以考虑不加入后续的分析；
# Survived（获救情况）变量为因变量，其值只有两类1或0，代表着获救或未获救；
# Pclass（乘客等级），Sex（性别），Embarked（登船港口）是明显的类别型数据，而Age（年龄），SibSp（堂兄弟妹个数），Parch（父母与小孩的个数）则是隐性的类别型数据；Fare（票价）是数值型数据；Cabin（船舱）则为文本型数据；
# Age（年龄），Cabin（船舱）和Embarked（登船港口）信息存在缺失数据。

#数据预处理
def loaddata(path):
    data=pd.read_csv(path,index_col=None)
    #数据预处理
    return data

if __name__=='__main__':


    #决策树相关参数
    clf = DecisionTreeClassifier()
    # criterion：特征选择标准，【entropy, gini】。默认gini，即CART算法。
    # splitter：特征划分标准，【best, random】。best在特征的所有划分点中找出最优的划分点，random随机的在部分划分点中找局部最优的划分点。默认的‘best’适合样本量不大的时候，而如果样本数据量非常大，此时决策树构建推荐‘random’。
    # max_depth：决策树最大深度，【int,  None】。默认值是‘None’。一般数据比较少或者特征少的时候可以不用管这个值，如果模型样本数量多，特征也多时，推荐限制这个最大深度，具体取值取决于数据的分布。常用的可以取值10-100之间，常用来解决过拟合。
    # min_samples_split：内部节点（即判断条件）再划分所需最小样本数，【int, float】。默认值为2。如果是int，则取传入值本身作为最小样本数；如果是float，则取ceil(min_samples_split*样本数量)作为最小样本数。（向上取整）
    # min_samples_leaf：叶子节点（即分类）最少样本数。如果是int，则取传入值本身作为最小样本数；如果是float，则取ceil(min_samples_leaf*样本数量)的值作为最小样本数。这个值限制了叶子节点最少的样本数，如果某叶子节点数目小于样本数，则会和兄弟节点一起被剪枝。
    # min_weight_fraction_leaf：叶子节点（即分类）最小的样本权重和，【float】。这个值限制了叶子节点所有样本权重和的最小值，如果小于这个值，则会和兄弟节点一起被剪枝。默认是0，就是不考虑权重问题，所有样本的权重相同。一般来说如果我们有较多样本有缺失值或者分类树样本的分布类别偏差很大，就会引入样本权重，这时就要注意此值。
    # max_features：在划分数据集时考虑的最多的特征值数量，【int值】。在每次split时最大特征数；【float值】表示百分数，即（max_features*n_features）
    # random_state：【int, randomSate instance, None】，默认是None
    # max_leaf_nodes：最大叶子节点数。【int, None】，通过设置最大叶子节点数，可以防止过拟合。默认值None，默认情况下不设置最大叶子节点数。如果加了限制，算法会建立在最大叶子节点数内最优的决策树。如果特征不多，可以不考虑这个值，但是如果特征多，可以加限制，具体的值可以通过交叉验证得到。
    # min_impurity_decrease：节点划分最小不纯度，【float】。默认值为‘0’。限制决策树的增长，节点的不纯度（基尼系数，信息增益，均方差，绝对差）必须大于这个阈值，否则该节点不再生成子节点。
    # min_impurity_split（已弃用）：信息增益的阀值。决策树在创建分支时，信息增益必须大于这个阈值，否则不分裂。（从版本0.19开始不推荐使用：min_impurity_split已被弃用，以0.19版本中的min_impurity_decrease取代。 min_impurity_split的默认值将在0.23版本中从1e-7变为0，并且将在0.25版本中删除。 请改用min_impurity_decrease。）
    # class_weight：类别权重，【dict, list of dicts, balanced】，默认为None。（不适用于回归树，sklearn.tree.DecisionTreeRegressor）指定样本各类别的权重，主要是为了防止训练集某些类别的样本过多，导致训练的决策树过于偏向这些类别。balanced，算法自己计算权重，样本量少的类别所对应的样本权重会更高。如果样本类别分布没有明显的偏倚，则可以不管这个参数。
    # presort：bool，默认是False，表示在进行拟合之前，是否预分数据来加快树的构建。对于数据集非常庞大的分类，presort=true将导致整个分类变得缓慢；当数据集较小，且树的深度有限制，presort=true才会加速分类。
    # ccp_alpha：将选择成本复杂度最大且小于ccp_alpha的子树。默认情况下，不执行修剪。

    #随机森林相关参数
    rfc=ensemble.RandomForestClassifier()
    # n_estimators：森林中决策树的数量。默认100，表示这是森林中树木的数量，即基基评估器的数量。这个参数对随机森林模型的精确性影响是单调的，n_estimators越大，模型的效果往往越好。但是相应的，任何模型都有决策边界，n_estimators达到一定的程度之后，随机森林的精确性往往不在上升或开始波动，并且，n_estimators越大，需要的计算量和内存也越大，训练的时间也会越来越长。对于这个参数，我们是渴望在训练难度和模型效果之间取得平衡。
    # criterion：分裂节点所用的标准，可选“gini”, “entropy”，默认“gini”。
    # max_depth：树的最大深度。如果为None，则将节点展开，直到所有叶子都是纯净的(只有一个类)，或者直到所有叶子都包含少于min_samples_split个样本。默认是None。
    # min_samples_split：拆分内部节点所需的最少样本数：如果为int，则将min_samples_split视为最小值。如果为float，则min_samples_split是一个分数，而ceil（min_samples_split * n_samples）是每个拆分的最小样本数。默认是2。
    # min_samples_leaf：在叶节点处需要的最小样本数。仅在任何深度的分割点在左分支和右分支中的每个分支上至少留下min_samples_leaf个训练样本时，才考虑。这可能具有平滑模型的效果，尤其是在回归中。如果为int，则将min_samples_leaf视为最小值。如果为float，则min_samples_leaf是分数，而ceil（min_samples_leaf * n_samples）是每个节点的最小样本数。默认是1。
    # min_weight_fraction_leaf：在所有叶节点处（所有输入样本）的权重总和中的最小加权分数。如果未提供sample_weight，则样本的权重相等。
    # max_features：寻找最佳分割时要考虑的特征数量：如果为int，则在每个拆分中考虑max_features个特征。如果为float，则max_features是一个分数，并在每次拆分时考虑int（max_features * n_features）个特征。如果为“auto”，则max_features = sqrt（n_features）。如果为“ sqrt”，则max_features = sqrt（n_features）。如果为“ log2”，则max_features = log2（n_features）。如果为None，则max_features = n_features。注意：在找到至少一个有效的节点样本分区之前，分割的搜索不会停止，即使它需要有效检查多个max_features功能也是如此。
    # max_leaf_nodes：最大叶子节点数，整数，默认为None
    # min_impurity_decrease：如果分裂指标的减少量大于该值，则进行分裂。
    # min_impurity_split：决策树生长的最小纯净度。默认是0。自版本0.19起不推荐使用：不推荐使用min_impurity_split，而建议使用0.19中的min_impurity_decrease。min_impurity_split的默认值在0.23中已从1e-7更改为0，并将在0.25中删除。
    # bootstrap：是否进行bootstrap操作，bool。默认True。如果bootstrap==True，将每次有放回地随机选取样本，只有在extra-trees中，bootstrap=False
    # oob_score：是否使用袋外样本来估计泛化精度。默认False。
    # n_jobs：并行计算数。默认是None。
    # random_state：控制bootstrap的随机性以及选择样本的随机性。
    # verbose：在拟合和预测时控制详细程度。默认是0。
    # class_weight：每个类的权重，可以用字典的形式传入{class_label: weight}。如果选择了“balanced”，则输入的权重为n_samples / (n_classes * np.bincount(y))。
    # ccp_alpha：将选择成本复杂度最大且小于ccp_alpha的子树。默认情况下，不执行修剪。
    # max_samples：如果bootstrap为True，则从X抽取以训练每个基本分类器的样本数。如果为None（默认），则抽取X.shape [0]样本。如果为int，则抽取max_samples样本。如果为float，则抽取max_samples * X.shape [0]个样本。因此，max_samples应该在（0，1）中。是0.22版中的新功能。

    #网格搜索相关参数
    gf=GridSearchCV()
    # estimator选择使用的分类器，并且传入除需要确定最佳的参数之外的其他参数。
    # param_grid 需要最优化的参数的取值，值为字典或者列表。
    # scoring = None 默认使用estimator的误差估计函数
    # n_jobs = 1进程个数，默认为1。
    #refit=True 默认为True,程序将会以交叉验证训练集得到的最佳参数，重新对所有可用的训练集与开发集进行，作为最终用于性能评估的最佳模型参数。
    # cv = None 交叉验证参数，默认None，使用三折交叉验证。
    #verbose = 0,日志冗长度0：不输出训练过程，1：偶尔输出， > 1：对每个子模型都输出。
    #pre_dispatch =‘2 * n_jobs’，指定总共分发的并行任务数。
