# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow.contrib import learn

"""使用线性回归模型预测波士顿房价
"""
from sklearn import datasets, metrics, preprocessing

boston = datasets.load_boston()
x_data = preprocessing.StandardScaler().fit_transform(boston.data)
y_data = boston.target

"""使用原生的 TensorFlow 方法实现
"""
x = tf.placeholder(tf.float64, shape=(None, 13))
y_true = tf.placeholder(tf.float64, shape=(None))

with tf.name_scope("inference") as scope:
    w = tf.Variable(tf.zeros([1, 13], dtype=tf.float64, name="weights"))
    b = tf.Variable(0, dtype=tf.float64, name="bias")
    y_pred = tf.matmul(w, tf.transpose(x)) + b

with tf.name_scope("loss") as scope:
    loss = tf.reduce_mean(tf.square(y_true - y_pred))

with tf.name_scope("train") as scope:
    learning_rate = 0.1
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train = optimizer.minimize(loss)

# Before starting, initialize the variables.  We will 'run' this first.
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    for step in range(200):
        sess.run(train, {x: x_data, y_true: y_data})

    MSE = sess.run(loss, {x: x_data, y_true: y_data})
print(MSE)

"""使用 contirb.learn 实现
"""
NUM_STEPS = 200
MINIBATCH_SIZE = 506

# 使用 learn.LinearRegressor() 实例化线性回归模型，并提供关于数据表征和优化器类型的知识
feature_columns = learn.infer_real_valued_columns_from_input(x_data)

reg = learn.LinearRegressor(
    feature_columns=feature_columns,
    optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.1),
)
# 使用.fit() 对回归器regressor对象进行训练。向它传递协变量和目标变量，并设置步数和批量大小
reg.fit(x_data, boston.target, steps=NUM_STEPS, batch_size=MINIBATCH_SIZE)

# 使用.evaluate() 计算MSE
MSE = reg.evaluate(x_data, boston.target, steps=1)

print(MSE)
