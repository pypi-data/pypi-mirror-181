from random import randint, seed
import pytest
from structs import MaxIndexPQ, MaxPQ, MinIndexPQ, MinPQ, RedBlackBST, Bag, Stack, Queue

def test_bag():
    b = Bag()
    for i in range(0,50):
        b.add(i)
    assert b.size == 50
    item1 = b.remove()
    for i in b:
        assert i != item1
    assert b.size == 0

def test_stack():
    s = Stack()
    assert s.is_empty()
    assert s.peek() == None
    len = 3
    for i in range(0,len):
        s.push(i)
    assert s.size == len
    t = s.peek()
    assert s.size == len
    t2 = s.pop()
    assert s.size == len -1
    for i in s:
        s.pop()
    assert s.size == 0

def test_stack_copy():
    s = Stack()
    for v in range(0,150):
        s.push(randint(0,100))
    s2 = s.copy()
    s3 = s.reverse_copy().reverse_copy()
    assert s.size == s2.size
    assert s2.size == s3.size
    assert s.peek() == s2.peek()
    assert s2.peek() == s3.peek()
    assert str(s) == str(s2)
    assert str(s2) == str(s3)

def test_queue():
    q = Queue()
    assert q.is_empty()
    assert q.peek() == None
    len = 3
    for i in range(0,len):
        q.enqueue(i)
    assert q.size == len
    t = q.peek()
    assert q.size == len
    t2 = q.dequeue()
    assert q.size == len -1
    for i in q:
        q.dequeue()
    assert q.size == 0

def test_queue_copy():
    q = Queue()
    for v in range(0,150):
        q.enqueue(randint(0,100))
    q2 = q.copy()
    q3 = q.reverse_copy().reverse_copy()
    assert q.size == q2.size
    assert q2.size == q3.size
    assert q.peek() == q2.peek()
    assert q2.peek() == q3.peek()
    assert str(q) == str(q2)
    assert str(q2) == str(q3)

def test_min_pq():
    pq = MinPQ(4)
    seed(2)
    for _ in range(0,148):
        v = randint(0,50000)
        pq.insert(v)
    pq.insert(-1)
    pq.insert(51000)
    
    assert pq.capacity == 256
    assert pq.size == 150
    v = pq.peek()
    pq.remove(v)
    v2 = pq.peek()
    assert v == -1
    assert v2 != -1

def test_max_pq():
    pq = MaxPQ(4)
    seed(2)
    for _ in range(0,148):
        v = randint(0,50000)
        pq.insert(v)
    pq.insert(-1)
    pq.insert(51000)
    
    assert pq.capacity == 256
    assert pq.size == 150
    v = pq.peek()
    pq.remove(v)
    v2 = pq.peek()
    assert v == 51000
    assert v2 != 51000

def test_min_index_pq():
    pq = MinIndexPQ(150)
    seed(2)
    for i in range(0,148):
        v = randint(0,50000)
        pq.insert(i,v)
    pq.insert(149,-1)
    pq.insert(150, 51000)
    
    assert pq._IndexPQ__nmax == 150
    assert pq.size == 150
    pq.change_key(0,1)
    pq.min_index()
    ix = pq.del_min()

def test_max_index_pq():
    pq = MaxIndexPQ(150)
    seed(2)
    for i in range(0,148):
        v = randint(0,50000)
        pq.insert(i,v)
    pq.insert(149,-1)
    pq.insert(150, 51000)
    
    assert pq._IndexPQ__nmax == 150
    assert pq.size == 150
    pq.change_key(0,1)
    pq.max_index()
    ix = pq.del_max()

# Arrange:
@pytest.fixture
def red_black_tree():
    t = RedBlackBST()
    assert t.root == None
    len = 50
    for i in range(0,len):
        t.put(i, str(i))
    for i in range(len,len*2):
        t.put(i, str(randint(0,100000)))
    assert t.root != None
    assert t.size() == len * 2
    return t

def test_red_black_tree(red_black_tree):
    # Act:
    # Assert:
    assert red_black_tree.check()

def main():
    pass

if __name__ == "__main__":
    #sys.exit(main())
    main()









