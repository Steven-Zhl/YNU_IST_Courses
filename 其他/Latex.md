# LaTeX

> 什么是LaTeX：LaTeX是一个高质量的文档排版系统，它支持一系列的符号的渲染，效果美观，语法简单且符合编程习惯，常被用于公式的编辑与渲染，Markdown和Microsoft Word都已经全面支持LaTeX渲染。
>
> LaTeX本质上更接近于HTML或Markdown，是一种标记语言。
>
> 本篇记录一些常用的LaTeX语法，以及一些大型公式的组织方法，由于我也是边学边记录的，所以本文应该会长期更新。

## 目录

* [LaTeX](#latex)
  * [目录](#目录)
  * [运算符](#运算符)
    * [基本代数运算符](#基本代数运算符)
    * [大型运算符](#大型运算符)
    * [关系代数运算符](#关系代数运算符)
    * [集合运算符](#集合运算符)
  * [希腊字母](#希腊字母)
  * [版式控制](#版式控制)
    * [1. 如何设置下标/上标](#1-如何设置下标上标)
    * [2. 如何让下标/上标置于正上方/正下方](#2-如何让下标上标置于正上方正下方)
  * [References](#references)

## 运算符

### 基本代数运算符

|运算符|LaTeX|备注|
|:--:|:--:|:--:|
|$+$|+|加|
|$-$|-|减|
|$\times$|\times|乘|
|$\div$|\div|除|
|$\cdot$|\cdot|点乘|
|$\pm$|\pm|正负号|
|$\mp$|\mp|负正号|
|$\ast$|\ast|星号|

### 大型运算符

|运算符|LaTeX|备注|
|:--:|:--:|:--:|
|$\sum$|\sum|求和|
|$\prod$|\prod|虽然$\Pi$和它很像，但毕竟不一样，这个表示的是连乘，$\Pi$表示的是关系运算的投影|

### 关系代数运算符

> (离散数学与数据库常用)

|运算符|LaTeX|备注|
|:--:|:--:|:--:|
|$\bigvee$|\bigvee|析取(离散数学)/并(数据库)，等价于自然语言的“或”|
|$\bigwedge$|\bigwedge|合取(离散数学)/差(数据库)，等价于自然语言的“与”|
|$\times$|\times|笛卡尔积|
|$\Pi$|\Pi|投影|
|$\sigma$|\sigma|选择|
|$\bowtie$|\bowtie|连接|

### 集合运算符

|运算符|LaTeX|备注|
|:--:|:--:|:--:|
|$\bigcap$|\bigcap|交集|
|$\bigcup$|\bigcup|并集|
|$-$|-|差集|
|$\complement_UA$|\complement_UA|A相对于U的补集|
|$\subset$|\subset|子集|
|$\subseteq$|\subseteq|真子集|
|$\supset$|\supset|超集|
|$\supseteq$|\supseteq|真超集|
|$\in$|\in|属于(注意，$\in$是表示元素和集合之间的关系的)|
|$\notin$|\notin|不属于|

## 希腊字母

|小写字母|LaTeX|大写字母|LaTeX|发音|备注|
|:--:|:--:|:--:|:--:|:--:|:--:|
|$\alpha$|\alpha|$\Alpha$|\Alpha|/ˈælfə/||
|$\beta$|\beta|$\Beta$|\Beta|/ˈbiːtə/||
|$\gamma$|\gamma|$\Gamma$|\Gamma|/ˈɡæmə/||
|$\delta$|\delta|$\Delta$|\Delta|/ˈdɛltə/||
|$\epsilon$|\epsilon|$\Epsilon$|\Epsilon|/ˈɛpsɪlɒn/||
|$\eta$|\eta|$\Eta$|\Eta|/ˈiːtə/||
|$\zeta$|\zeta|$\Zeta$|\Zeta|/ˈziːtə/||
|$\theta$|\theta|$\Theta$|\Theta|/ˈθiːtə/||
|$\vartheta$|\vartheta|$\varTheta$|\varTheta|/ˈθiːtə/||
|$\iota$|\iota|$\Iota$|\Iota|/ˈaɪətə/||
|$\kappa$|\kappa|$\Kappa$|\Kappa|/ˈkæpə/||
|$\lambda$|\lambda|$\Lambda$|\Lambda|/ˈlæmbdə/||
|$\mu$|\mu|$\Mu$|\Mu|/ˈmjuː/||
|$\nu$|\nu|$\Nu$|\Nu|/ˈnjuː/||
|$\xi$|\xi|$\Xi$|\Xi|/ˈzaɪ/||
|$\omicron$|\omicron|$\Omicron$|\Omicron|/ˈɒmɪkrɒn/||
|$\pi$|\pi|$\Pi$|\Pi|/ˈpaɪ/||
|$\rho$|\rho|$\Rho$|\Rho|/ˈroʊ/||
|$\sigma$|\sigma|$\Sigma$|\Sigma|/ˈsɪɡmə/||
|$\tau$|\tau|$\Tau$|\Tau|/ˈtɔː/||
|$\upsilon$|\upsilon|$\Upsilon$|\Upsilon|/ˈʌpsɪlɒn/||
|$\phi$|\phi|$\Phi$|\Phi|/ˈfaɪ/||
|$\varphi$|\varphi|$\varPhi$|\varPhi|/ˈfaɪ/||
|$\chi$|\chi|$\Chi$|\Chi|/ˈkaɪ/||
|$\psi$|\psi|$\Psi$|\Psi|/ˈsaɪ/||
|$\omega$|\omega|$\Omega$|\Omega|/ˈoʊmɪɡə/||

## 版式控制

> 本部分的内容以问题导向的方式记录

### 1. 如何设置下标/上标

* 上标：使用`^`表示其之后的内容为上标内容。
  * 如果上标内容仅是1个符号(1个数字、字母、希腊符号等)，可以直接使用`^`，如`$x^2$` ($x^2$)。
  * 如果上标内容包括多个符号，需要使用`{}`将其括起来，如`$x^{2n}$` ($x^{2n}$)。
* 下标：使用`_`表示其之后的内容为下标内容。
  * 如果下标内容仅是1个符号(1个数字、字母、希腊符号等)，可以直接使用`_`，如`$x_2$` ($x_2$)。
  * 如果下标内容包括多个符号，需要使用`{}`将其括起来，如`$x_{2n}$` ($x_{2n}$)。

### 2. 如何让下标/上标置于正上方/正下方

> 这部分相当于上一条的延伸，上一条的方法，下标/上标会置于右上方/右下方的位置，但对于有些大型运算符(如$\sum$)来说，上/下标置于正上方/正下方更为常用，这时候就需要使用`\limits`。

* 在上标/下标符号前加上`\limits`，如`$\sum\limits_{i=1}\limits^{n}$` ($\sum\limits_{i=1}\limits^{n}$)。
* 此外，当被加上/下标的符号不是数学符号时，则需要为其嵌套上`\mathop{}`，如`$\mathop{A}\limits_{a\in B}$` ($\mathop{A}\limits_{a\in B}$)。`A`不是数学符号，所以需要嵌套上`\mathop{}`才能正确渲染。

## References

* [【数据库】关系运算的符号表示 - 知乎](https://zhuanlan.zhihu.com/p/122926731)
* [LaTex中把下标置于文本正下方的方法_latex 下方_da_kao_la的博客-CSDN博客](https://blog.csdn.net/da_kao_la/article/details/84836098)
