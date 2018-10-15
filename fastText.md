

```bash
# 安装 fasttext 到当前目录

# fasttext 命令帮助
$ ./fasttext
usage: fasttext <command> <args>

The commands supported by fasttext are:

  supervised              train a supervised classifier(训练有监督的分类器)
  quantize                quantize a model to reduce the memory usage(量化模型以减少内存使用量)
  test                    evaluate a supervised classifier
  predict                 predict most likely labels(预测最可能的标签)
  predict-prob            predict most likely labels with probabilities(用可能性预测最可能的标签)
  skipgram                train a skipgram model(训练一个skipgram模型)
  cbow                    train a cbow model(训练一个cbow模型)
  print-word-vectors      print word vectors given a trained model
  print-sentence-vectors  print sentence vectors given a trained model
  nn                      query for nearest neighbors(查询最近邻居)
  analogies               query for analogies(查询类比)

# 下载、解压数据
$ wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/cooking.stackexchange.tar.gz
$ tar -zxvf cooking.stackexchange.tar.gz
cooking.stackexchange.id
cooking.stackexchange.txt
readme.txt
# 观察数据结构
$ head cooking.stackexchange.txt
__label__sauce __label__cheese How much does potato starch affect a cheese sauce recipe?
__label__food-safety __label__acidity Dangerous pathogens capable of growing in acidic environments
__label__cast-iron __label__stove How do I cover up the white spots on my cast iron stove?
__label__restaurant Michelin Three Star Restaurant; but if the chef is not there
__label__knife-skills __label__dicing Without knife skills, how can I quickly and accurately dice vegetables?
__label__storage-method __label__equipment __label__bread What's the purpose of a bread box?
__label__baking __label__food-safety __label__substitutions __label__peanuts how to seperate peanut oil from roasted peanuts at home?
__label__chocolate American equivalent for British chocolate terms
__label__baking __label__oven __label__convection Fan bake vs bake
__label__sauce __label__storage-lifetime __label__acidity __label__mayonnaise Regulation and balancing of readymade packed mayonnaise and other sauces
# 统计数据行数
$ wc cooking.stackexchange.txt
  15404  169582 1401900 cooking.stackexchange.txt
# 生成测试数据和验证数据
$ head -n 12404 cooking.stackexchange.txt > cooking.train
$ tail -n 3000 cooking.stackexchange.txt > cooking.valid
# 训练有监督分类器
$ ./fastText-0.1.0/fasttext supervised -input cooking.train -output model_cooking
Read 0M words
Number of words:  14543
Number of labels: 735
Progress: 100.0%  words/sec/thread: 50001  lr: 0.000000  loss: 10.196953  eta: 0h0m
$ ll model_cooking.*
-rw-rw-r-- 1 lanzhiwang lanzhiwang  6382062 10月 15 19:44 model_cooking.bin
-rw-rw-r-- 1 lanzhiwang lanzhiwang 15192790 10月 15 19:44 model_cooking.vec
# 用交互式方式预测文本
$ ./fastText-0.1.0/fasttext predict model_cooking.bin -
Which baking dish is best to bake a banana bread ?
__label__baking
Why not put knives in the dishwasher?
__label__food-safety
# 验证模型
$ ./fastText-0.1.0/fasttext test model_cooking.bin cooking.valid
N	3000
P@1	0.136
R@1	0.0587
Number of examples: 3000
$ ./fastText-0.1.0/fasttext test model_cooking.bin cooking.valid 5
N	3000
P@5	0.0677
R@5	0.146
Number of examples: 3000
$
# 输出文本的前5个标签
$ ./fastText-0.1.0/fasttext predict model_cooking.bin -
Why not put knives in the dishwasher?
__label__food-safety

$ ./fastText-0.1.0/fasttext predict model_cooking.bin - 5
Why not put knives in the dishwasher?
__label__food-safety __label__baking __label__bread __label__equipment __label__substitutions

$
# 优化模型
$ cat cooking.stackexchange.txt | sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" > cooking.preprocessed.txt
$ head -n 12404 cooking.preprocessed.txt > cooking.train
$ tail -n 3000 cooking.preprocessed.txt > cooking.valid
$ ./fastText-0.1.0/fasttext supervised -input cooking.train -output model_cooking
Read 0M words
Number of words:  8952
Number of labels: 735
Progress: 100.0%  words/sec/thread: 52856  lr: 0.000000  loss: 10.107295  eta: 0h0m
$ ./fastText-0.1.0/fasttext test model_cooking.bin cooking.valid
N	3000
P@1	0.169
R@1	0.0732
Number of examples: 3000
$ ./fastText-0.1.0/fasttext supervised -input cooking.train -output model_cooking -epoch 25
$ ./fastText-0.1.0/fasttext supervised -input cooking.train -output model_cooking -lr 1.0
$ ./fastText-0.1.0/fasttext supervised -input cooking.train -output model_cooking -lr 1.0 -epoch 25
$ ./fastText-0.1.0/fasttext supervised -input cooking.train -output model_cooking -lr 1.0 -epoch 25 -wordNgrams 2
$ ./fastText-0.1.0/fasttext supervised -input cooking.train -output model_cooking -lr 1.0 -epoch 25 -wordNgrams 2 -bucket 200000 -dim 50 -loss hs
$

```