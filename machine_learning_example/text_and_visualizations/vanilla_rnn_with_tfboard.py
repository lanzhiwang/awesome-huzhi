# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 17:34:43 2016

@author: tomhope
"""
from __future__ import print_function
import tensorflow as tf

# Import MINST data
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

# Define some parameters
"""
MNIST数据序列化就是将28*28像素的图像看做是一个长度为28的序列
序列中的每个元素都是一个28像素的向量
"""
element_size = 28  # element_size 是序列中每个向量的维数
time_steps = 28  # time_steps 是序列中元素的数量
num_classes = 10
batch_size = 128
hidden_layer_size = 128

# Where to save TensorBoard model summaries
LOG_DIR = "logs/RNN_with_summaries"

# Create placeholders for inputs, labels
_inputs = tf.placeholder(
    tf.float32, shape=[None, time_steps, element_size], name="inputs"
)
y = tf.placeholder(tf.float32, shape=[None, num_classes], name="labels")


# 用于记录汇总的函数，后续会使用这个函数对模型和训练过程进行可视化
def variable_summaries(var):
    with tf.name_scope("summaries"):
        mean = tf.reduce_mean(var)
        tf.summary.scalar("mean", mean)
        with tf.name_scope("stddev"):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar("stddev", stddev)
        tf.summary.scalar("max", tf.reduce_max(var))
        tf.summary.scalar("min", tf.reduce_min(var))
        tf.summary.histogram("histogram", var)


# 将RNN步骤中用到的权重和偏差创建为变量
with tf.name_scope("rnn_weights"):
    with tf.name_scope("W_x"):
        Wx = tf.Variable(tf.zeros([element_size, hidden_layer_size]))
        variable_summaries(Wx)
    with tf.name_scope("W_h"):
        Wh = tf.Variable(tf.zeros([hidden_layer_size, hidden_layer_size]))
        variable_summaries(Wh)
    with tf.name_scope("Bias"):
        b_rnn = tf.Variable(tf.zeros([hidden_layer_size]))
        variable_summaries(b_rnn)


# 双曲正切函数
def rnn_step(previous_hidden_state, x):

    current_hidden_state = tf.tanh(
        tf.matmul(previous_hidden_state, Wh) + tf.matmul(x, Wx) + b_rnn
    )

    return current_hidden_state


# Processing inputs to work with scan function
# Current input shape: (batch_size, time_steps, element_size)
processed_input = tf.transpose(_inputs, perm=[1, 0, 2])
# Current input shape now: (time_steps,batch_size, element_size)


initial_hidden = tf.zeros([batch_size, hidden_layer_size])
# 使用 tf.scan 方法实现RNN网络训练
all_hidden_states = tf.scan(
    rnn_step, processed_input, initializer=initial_hidden, name="states"
)


# Weights for output layers
with tf.name_scope("linear_layer_weights") as scope:
    with tf.name_scope("W_linear"):
        # 定义线性层的权重变量
        Wl = tf.Variable(
            tf.truncated_normal([hidden_layer_size, num_classes], mean=0, stddev=0.01)
        )
        variable_summaries(Wl)
    with tf.name_scope("Bias_linear"):
        # 定义线性层的偏差变量
        bl = tf.Variable(tf.truncated_normal([num_classes], mean=0, stddev=0.01))
        variable_summaries(bl)


# Apply linear layer to state vector
def get_linear_layer(hidden_state):

    return tf.matmul(hidden_state, Wl) + bl


with tf.name_scope("linear_layer_weights") as scope:
    # Iterate across time, apply linear layer to all RNN outputs
    all_outputs = tf.map_fn(get_linear_layer, all_hidden_states)
    # Get Last output -- h_28
    output = all_outputs[-1]
    tf.summary.histogram("outputs", output)

with tf.name_scope("cross_entropy"):
    # 定义损失函数
    # 使用交叉熵作为损失函数
    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=y)
    )
    tf.summary.scalar("cross_entropy", cross_entropy)

with tf.name_scope("train"):
    # Using RMSPropOptimizer
    # RMSPropOptimizer优化器，使用梯度下降法定义训练过程
    train_step = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cross_entropy)

with tf.name_scope("accuracy"):
    # 定义评估步骤，用来测试模型的准确率
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(output, 1))

    accuracy = (tf.reduce_mean(tf.cast(correct_prediction, tf.float32))) * 100
    tf.summary.scalar("accuracy", accuracy)

# Merge all the summaries
merged = tf.summary.merge_all()


# Get a small test set
test_data = mnist.test.images[:batch_size].reshape((-1, time_steps, element_size))
test_label = mnist.test.labels[:batch_size]

with tf.Session() as sess:
    # Write summaries to LOG_DIR -- used by TensorBoard
    # 用 TensorBoard 对模型进行可视化 tensorboard --logdir=LOG_DIR
    train_writer = tf.summary.FileWriter(
        LOG_DIR + "/train", graph=tf.get_default_graph()
    )
    test_writer = tf.summary.FileWriter(LOG_DIR + "/test", graph=tf.get_default_graph())

    sess.run(tf.global_variables_initializer())

    for i in range(10000):

        batch_x, batch_y = mnist.train.next_batch(batch_size)
        # Reshape data to get 28 sequences of 28 pixels
        batch_x = batch_x.reshape((batch_size, time_steps, element_size))
        summary, _ = sess.run(
            [merged, train_step], feed_dict={_inputs: batch_x, y: batch_y}
        )
        # Add to summaries
        train_writer.add_summary(summary, i)

        if i % 1000 == 0:
            (
                acc,
                loss,
            ) = sess.run(
                [accuracy, cross_entropy], feed_dict={_inputs: batch_x, y: batch_y}
            )
            print(
                "Iter "
                + str(i)
                + ", Minibatch Loss= "
                + "{:.6f}".format(loss)
                + ", Training Accuracy= "
                + "{:.5f}".format(acc)
            )
        if i % 100 == 0:
            # Calculate accuracy for 128 mnist test images and
            # add to summaries
            summary, acc = sess.run(
                [merged, accuracy], feed_dict={_inputs: test_data, y: test_label}
            )
            test_writer.add_summary(summary, i)

    test_acc = sess.run(accuracy, feed_dict={_inputs: test_data, y: test_label})
    print("Test Accuracy:", test_acc)
