```bash
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter

def isStraight(l):
    ''' 1 - 13 (不考虑花色)
    1 3 5 7 9 顺子 Y/N 
    1 2 3 4 5 Y
    8 9 10 11 12 Y
    1 3 4 5 6  N
    13 1 2 3 4 N

    0 - Magic Card
    0 0 1 3 5 -> 2 4 1 3 5 -> Y
    a = [0,0,1,3,5] => True
    a = [1,3,5,7,9] => False
    a = [2,3,4,1,5] => True
    a = [2,2,3,4,5] => False
    '''
    print 'l: ', l
    l_sorted = sorted(l)
    print 'l_sorted: ', l_sorted
    l_count = Counter(l_sorted)
    count_0 = l_count.get(0, 0)
    if count_0 > 3:
        return True
    else:
        diff = l_sorted[-1] - l_sorted[count_0]
        if diff > 4:
            return False
        else:
            return True

def isAllStraight(l):
    ''' 判断任意数量的扑克牌是否是顺子
    在 1-13 中挑选不大于13的任意张扑克牌，可以出任意次数的 0
    '''
    print 'l: ', l
    count = len(l)
    l_sorted = sorted(l)
    print 'l_sorted: ', l_sorted
    l_count = Counter(l_sorted)
    count_0 = l_count.get(0, 0)
    if count_0 > count - 2:
        return True
    else:
        diff = l_sorted[-1] - l_sorted[count_0]
        if diff > count - 1:
            return False
        else:
            return True


if __name__ == "__main__":
    print isStraight([1, 3, 5, 7, 9])
    print isStraight([1, 2, 3, 4, 5])
    print isStraight([8, 9, 10, 11, 12])
    print isStraight([1, 3, 5, 2, 6])
    print isStraight([13, 1, 2, 3, 4])
    print isStraight([0, 0, 1, 3, 5])
    print isStraight([0, 0, 1, 3, 8])
    print isStraight([0, 0, 0, 0, 0])
    print '***' * 10
    print isAllStraight([1, 3, 5, 7, 9])
    print isAllStraight([1, 2, 3, 4, 5])
    print isAllStraight([8, 9, 10, 11, 12])
    print isAllStraight([1, 3, 5, 2, 6])
    print isAllStraight([13, 1, 2, 3, 4])
    print isAllStraight([0, 0, 1, 3, 5])
    print isAllStraight([0, 0, 1, 3, 8])
    print isAllStraight([0, 0, 0, 0, 0])
    print '***' * 10
    print isAllStraight([0])
    print isAllStraight([1])
    print isAllStraight([1, 6])
    print isAllStraight([5, 0])
    print isAllStraight([0, 0, 2, 4, 5, 3, 8])
```

