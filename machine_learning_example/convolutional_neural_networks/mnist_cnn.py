from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import numpy as np

from layers import conv_layer, max_pool_2x2, full_layer

DATA_DIR = '/tmp/data'
MINIBATCH_SIZE = 50
STEPS = 5000


# 查看原始数据
# http://yann.lecun.com/exdb/mnist/
'''
>>> from tensorflow.examples.tutorials.mnist import input_data
>>> import numpy as np
>>> mnist = input_data.read_data_sets('/home/lanzhiwang/rzx_project/awesome-huzhi/machine_learning_example/data', one_hot=True)
>>> print mnist
Datasets(train=<tensorflow.contrib.learn.python.learn.datasets.mnist.DataSet object at 0x7f000f9b0d10>, validation=<tensorflow.contrib.learn.python.learn.datasets.mnist.DataSet object at 0x7f000f70c090>, test=<tensorflow.contrib.learn.python.learn.datasets.mnist.DataSet object at 0x7f000f70c0d0>)
>>> X = mnist.test.images.reshape(10, 1000, 784)
>>> print type(X)
<type 'numpy.ndarray'>
>>> print X.dtype
float32
>>> print X.shape
(10, 1000, 784)
>>>
>>> np.set_printoptions(threshold='nan')
>>> print x
 [ 0.         0.         0.         0.         0.         0.
   0.         0.         0.         0.01960784 0.34901962 0.6117647
   0.9058824  1.         0.6392157  0.07058824 0.         0.
   0.         0.         0.         0.         0.         0.
   0.         0.         0.         0.         0.         0.
   0.         0.         0.         0.         0.         0.
   0.13725491 0.64705884 0.9921569  0.9921569  0.9921569  0.9960785]

'''

# 图像输入数据，直接使用 MNIST 数据集
mnist = input_data.read_data_sets(DATA_DIR, one_hot=True)

# 定义输入图像变量
x = tf.placeholder(tf.float32, shape=[None, 784])
# 定义正确的分类标签变量
y_ = tf.placeholder(tf.float32, shape=[None, 10])

# 将图像数据转化为2D图像格式
x_image = tf.reshape(x, [-1, 28, 28, 1])

# 第一层卷积操作
conv1 = conv_layer(x_image, shape=[5, 5, 1, 32])
# 将结果池化
conv1_pool = max_pool_2x2(conv1)

# 第二层卷积操作
conv2 = conv_layer(conv1_pool, shape=[5, 5, 32, 64])
# 将结果池化
conv2_pool = max_pool_2x2(conv2)

# 将图像数据平整为一维向量形式
conv2_flat = tf.reshape(conv2_pool, [-1, 7*7*64])
# 进行全连接操作
full_1 = tf.nn.relu(full_layer(conv2_flat, 1024))

# 进行随机丢弃操作
keep_prob = tf.placeholder(tf.float32)
# tf.nn.dropout 随机丢弃操作
full1_drop = tf.nn.dropout(full_1, keep_prob=keep_prob)

# 得到训练结果
y_conv = full_layer(full1_drop, 10)

# 定义损失函数
# 使用交叉熵作为损失函数
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_conv, labels=y_))
# 使用梯度下降法定义训练过程
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
# 定义评估步骤，用来测试模型的准确率
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    # 开始训练
    sess.run(tf.global_variables_initializer())

    for i in range(STEPS):
        batch = mnist.train.next_batch(MINIBATCH_SIZE)

        if i % 100 == 0:
            train_accuracy = sess.run(accuracy, feed_dict={x: batch[0], y_: batch[1],
                                                           keep_prob: 1.0})
            print("step {}, training accuracy {}".format(i, train_accuracy))

        sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    X = mnist.test.images.reshape(10, 1000, 784)
    Y = mnist.test.labels.reshape(10, 1000, 10)
    # 计算准确率
    test_accuracy = np.mean(
        [sess.run(accuracy, feed_dict={x: X[i], y_: Y[i], keep_prob: 1.0}) for i in range(10)])

print("test accuracy: {}".format(test_accuracy))
