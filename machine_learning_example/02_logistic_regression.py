# -*- coding: utf-8 -*-

"""利用 tensorflow 实现逻辑回归模型
基本原理：y = wx + b
其中：
x - x 输入
y - y 输出
w - 权重
b - 偏差

参考：
https://github.com/Hezi-Resheff/Oreilly-Learning-TensorFlow/blob/master/03__tensorflow_basics/Chapter3.ipynb
"""
import tensorflow as tf
import numpy as np


# 定义归一化逻辑函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# 定义一组输入
x_data = np.random.randn(20000, 3)
# 定义真实的权重
w_real = [0.3, 0.5, 0.1]
# 定义真实的偏差
b_real = -0.2
# 通过输入、真实权重、真实偏差计算真实输出
wxb = np.matmul(w_real, x_data.T) + b_real

# 计算输出归一化后的输出结果
y_data_pre_noise = sigmoid(wxb)
y_data = np.random.binomial(1, y_data_pre_noise)

NUM_STEPS = 50
g = tf.Graph()
wb_ = []
with g.as_default():
    # 定义真实输入占位符
    x = tf.placeholder(tf.float32, shape=[None, 3])
    # 定义真实输出占位符
    y_true = tf.placeholder(tf.float32, shape=None)

    with tf.name_scope("inference") as scope:
        # 定义训练权重变量
        w = tf.Variable([[0, 0, 0]], dtype=tf.float32, name="weights")
        # 定义训练偏差变量
        b = tf.Variable(0, dtype=tf.float32, name="bias")
        # 定义训练得到的输出
        y_pred = tf.matmul(w, tf.transpose(x)) + b

    with tf.name_scope("loss") as scope:
        # 定义损失函数
        # 使用交叉熵作为损失函数
        loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=y_true, logits=y_pred)
        loss = tf.reduce_mean(loss)

    with tf.name_scope("train") as scope:
        # 定义学习速率
        learning_rate = 0.5
        # 定义优化器，使用随机梯度下降
        optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        train = optimizer.minimize(loss)

    # Before starting, initialize the variables.  We will 'run' this first.
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        for step in range(NUM_STEPS):
            # 计算最小误差值
            sess.run(train, {x: x_data, y_true: y_data})
            if step % 5 == 0:
                print(step, sess.run([w, b]))
                wb_.append(sess.run([w, b]))

        print(50, sess.run([w, b]))

"""
训练过程中的输出
(0, [array([[ 0.03320302,  0.05792972,  0.01119308]], dtype=float32), -0.020700064])
(5, [array([[ 0.14649118,  0.2548342 ,  0.04982107]], dtype=float32), -0.091209568])
(10, [array([[ 0.20652841,  0.35850295,  0.07069619]], dtype=float32), -0.12844093])
(15, [array([[ 0.23972291,  0.41549107,  0.08243967]], dtype=float32), -0.14894117])
(20, [array([[ 0.25859103,  0.44772011,  0.08921722]], dtype=float32), -0.16054493])
(25, [array([[ 0.26949188,  0.4662571 ,  0.09318593]], dtype=float32), -0.16722204])
(30, [array([[ 0.27584928,  0.47702512,  0.09552839]], dtype=float32), -0.17110163])
(35, [array([[ 0.27957708,  0.48331678,  0.09691675]], dtype=float32), -0.17336872])
(40, [array([[ 0.28176975,  0.48700568,  0.09774131]], dtype=float32), -0.17469805])
(45, [array([[ 0.28306174,  0.48917308,  0.09823143]], dtype=float32), -0.17547914])

训练的最后结果
(50, [array([[ 0.28370172,  0.49024412,  0.09847598]], dtype=float32), -0.17586514])

真实结果
w_real = [0.3,0.5,0.1]
b_real = -0.2
"""
