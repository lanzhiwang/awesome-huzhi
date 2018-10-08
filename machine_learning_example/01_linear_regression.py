# -*- coding: utf-8 -*-

''' 利用 tensorflow 实现线性回归模型
基本原理：y = (wx + b) + noise
其中：
x - x 输入
y - y 输出
w - 权重
b - 偏差
noise - 噪声

参考：
https://github.com/Hezi-Resheff/Oreilly-Learning-TensorFlow/blob/master/03__tensorflow_basics/Chapter3.ipynb
'''
import tensorflow as tf
import numpy as np

# 定义一组输入
x_data = np.random.randn(2000,3)
# 定义真实的权重
w_real = [0.3,0.5,0.1]
# 定义真实的偏差
b_real = -0.2

# 定义一组随机噪声
noise = np.random.randn(1,2000)*0.1
# 通过输入、真实权重、真实偏差、随机噪声计算真实输出
y_data = np.matmul(w_real,x_data.T) + b_real + noise

NUM_STEPS = 10

g = tf.Graph()
wb_ = []
with g.as_default():
    # 定义真实输入占位符
    x = tf.placeholder(tf.float32,shape=[None,3])
    # 定义真实输出占位符
    y_true = tf.placeholder(tf.float32,shape=None)

    with tf.name_scope('inference') as scope:
        # 定义训练权重变量
        w = tf.Variable([[0,0,0]],dtype=tf.float32,name='weights')
        # 定义训练偏差变量
        b = tf.Variable(0,dtype=tf.float32,name='bias')
        # 定义训练得到的输出
        y_pred = tf.matmul(w,tf.transpose(x)) + b

    with tf.name_scope('loss') as scope:
        # 定义损失函数
        # 使用 MSE(均方误差) 作为损失函数
        # 计算真实输出和训练输出的均方误差
        loss = tf.reduce_mean(tf.square(y_true-y_pred))

    with tf.name_scope('train') as scope:
        # 定义学习速率
        learning_rate = 0.5
        # 定义优化器，使用随机梯度下降
        optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        train = optimizer.minimize(loss)

    # 开始训练
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        for step in range(NUM_STEPS):
            # 计算最小误差值
            sess.run(train,{x: x_data, y_true: y_data})
            if (step % 5 == 0):
                print(step, sess.run([w,b]))
                wb_.append(sess.run([w,b]))

        print(10, sess.run([w,b]))

'''
训练过程中的输出
(0, [array([[ 0.30298612,  0.48779276,  0.0716765 ]], dtype=float32), -0.18869072])
(5, [array([[ 0.3005667 ,  0.50066561,  0.09561971]], dtype=float32), -0.19749904])

训练的最后结果
(10, [array([[ 0.3005667 ,  0.50066561,  0.0956197 ]], dtype=float32), -0.19749907])

真实结果
w_real = [0.3,0.5,0.1]
b_real = -0.2
'''
