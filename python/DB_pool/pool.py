# -*- coding: utf-8 -*-

import multiprocessing, time, psycopg2

class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        # todo 使用连接池
        self.pyConn = psycopg2.connect("dbname='geobase_1' host = 'localhost'")
        self.pyConn.set_isolation_level(0)


    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                print 'Tasks Complete'
                self.task_queue.task_done()
                break
            answer = next_task(connection=self.pyConn)
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    def __init__(self, a):
        self.a = a

    def __call__(self, connection=None):
        pyConn = connection
        pyCursor1 = pyConn.cursor()

        # todo 数据库的具体操作不要写死，通过参数传递
        procQuery = 'UPDATE city SET gid_fkey = gid FROM country  WHERE ST_within((SELECT the_geom FROM city WHERE city_id = %s), country.the_geom) AND city_id = %s' % (self.a, self.a)
        pyCursor1.execute(procQuery)
        print 'What is self?'
        print self.a

        return self.a

        # todo 任务是否是同一类型，要么全部是查询，要么全部是插入，要么全部是更新，要么全部是删除
        # todo 不同类型的任务怎么办
        # todo 数据库客户端是否是异步的

    def __str__(self):
        return 'ARC'

    def run(self):
        print 'IN'


if __name__ == '__main__':
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    num_consumers = multiprocessing.cpu_count() * 2
    consumers = [Consumer(tasks, results) for i in xrange(num_consumers)]
    for w in consumers:
        w.start()

    pyConnX = psycopg2.connect("dbname='geobase_1' host = 'localhost'")
    pyConnX.set_isolation_level(0)
    pyCursorX = pyConnX.cursor()

    pyCursorX.execute('SELECT count(*) FROM cities WHERE gid_fkey IS NULL')
    temp = pyCursorX.fetchall()
    num_job = temp[0]
    num_jobs = num_job[0]

    pyCursorX.execute('SELECT city_id FROM city WHERE gid_fkey IS NULL')
    cityIdListTuple = pyCursorX.fetchall()

    cityIdListList = []

    for x in cityIdListTuple:
        cityIdList.append(x[0])


    for i in xrange(num_jobs):
        tasks.put(Task(cityIdList[i - 1]))

    for i in xrange(num_consumers):
        tasks.put(None)

    while num_jobs:
        result = results.get()
        print result
        num_jobs -= 1
