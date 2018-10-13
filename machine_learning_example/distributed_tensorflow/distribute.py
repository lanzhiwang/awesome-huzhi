import tensorflow as tf
from tensorflow.contrib import slim
from tensorflow.examples.tutorials.mnist import input_data


BATCH_SIZE = 50  # 每个小批量训练中使用的示例数量
TRAINING_STEPS = 5000  # 训练期间使用的小批量数量
PRINT_EVERY = 100  # 多久打印一次诊断信息
LOG_DIR = "/tmp/log"  # master Supervisor 节点存放日志和临时信息的目录，应该在程序再次运行之前清空它，因为旧信息可能导致下一次会话崩溃

# 集群定义
parameter_servers = ["localhost:2222"]  # 参数服务器
workers = ["localhost:2223", "localhost:2224", "localhost:2225"]  # 工作节点
cluster = tf.train.ClusterSpec({"ps": parameter_servers, "worker": workers})

# tf.app.flags 是 Python argparse 模块的封装
# tf.app.flags.FLAGS 包含从命令行输入解析的所有参数的值的结构
tf.app.flags.DEFINE_string("job_name", "", "'ps' / 'worker'")
tf.app.flags.DEFINE_integer("task_index", 0, "Index of task")
FLAGS = tf.app.flags.FLAGS

# 启动集群，也就是在服务器集群中使用当前任务的标识
'''
(job_name, task_index)
(ps, 0)
(worker, 0)
(worker, 1)
(worker, 2)
'''
server = tf.train.Server(cluster, job_name=FLAGS.job_name, task_index=FLAGS.task_index)

# 加载 MNIST 数据，定义卷积网络
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# 使用 TF-Slim 定义卷积网络
def net(x):
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    net = slim.layers.conv2d(x_image, 32, [5, 5], scope='conv1')
    net = slim.layers.max_pool2d(net, [2, 2], scope='pool1')
    net = slim.layers.conv2d(net, 64, [5, 5], scope='conv2')
    net = slim.layers.max_pool2d(net, [2, 2], scope='pool2')
    net = slim.layers.flatten(net, scope='flatten')
    net = slim.layers.fully_connected(net, 500, scope='fully_connected')
    net = slim.layers.fully_connected(net, 10, activation_fn=None, scope='pred')
    return net


if FLAGS.job_name == "ps":
    '''
    参数服务器不构建模型
    server.join() 使参数服务器在并行计算期间保持存活状态
    '''
    server.join()

elif FLAGS.job_name == "worker":
    '''在每个工作任务中，定义相同的计算图
    '''

    '''
    tf.train.replica_device_setter() 在每个节点上复制模型(计算图), worker_device 参数指向集群中的当前任务
    将 TensorFlow 变量通过参数服务器同步到worker节点
    '''
    with tf.device(tf.train.replica_device_setter(worker_device="/job:worker/task:%d" % FLAGS.task_index, cluster=cluster)):

        # global_step变量将保存训练期间的步骤总数(每个步骤引发在单个任务上)
        global_step = tf.get_variable('global_step', [], initializer=tf.constant_initializer(0), trainable=False)

        x = tf.placeholder(tf.float32, shape=[None, 784], name="x-input")
        y_ = tf.placeholder(tf.float32, shape=[None, 10], name="y-input")
        y = net(x)

        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y,
                                                                               labels=y_))

        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy,
                                                           global_step=global_step)

        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        init_op = tf.global_variables_initializer()

    # 定义 Supervisor 用来监督训练，并提供一些并行化设置必须的工具
    sv = tf.train.Supervisor(is_chief=(FLAGS.task_index == 0),  # 负责初始化等工作的"master Supervisor"
                             logdir=LOG_DIR,  # 存放日志的目录
                             global_step=global_step,  # TensorFlow 变量，它将在训练过程中保存当前的全局步骤
                             init_op=init_op)  # 用于初始化模型的 TensorFlow 操作

    # 启动实际会话，这时，"master Supervisor" 初始化变量，其他任务等待它完成
    with sv.managed_session(server.target) as sess:
        step = 0

        while not sv.should_stop() and step <= TRAINING_STEPS:

            batch_x, batch_y = mnist.train.next_batch(BATCH_SIZE)

            _, acc, step = sess.run([train_step, accuracy, global_step],
                                    feed_dict={x: batch_x, y_: batch_y})

            if step % PRINT_EVERY == 0:
                print("Worker : {}, Step: {}, Accuracy (batch): {}".
                      format(FLAGS.task_index, step, acc))

        test_acc = sess.run(accuracy,
                            feed_dict={x: mnist.test.images, y_: mnist.test.labels})
        print("Test-Accuracy: {}".format(test_acc))

    sv.stop()
