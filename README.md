该文件是基于tensorflow训练好的网络模型对选中图片进行色情图片预测的小项目,就是色情图片鉴别.该项目主要使用socket进行数据的传输,使用tornado进行图片选择和结果展示,
Tensorflow模型里只有5个分类，分别是sexy（性感）、porn（真人淫秽）、hentai（卡通淫秽）、neutral（中性事物）、drawing（手绘漫画）,预测结果为可能属于这几类的概率值.

有一点要强调的是我的python解释器是3.8版,所以添加了一些代码才能使程序正常运行,版本比较低的需要改动才能成功运行
