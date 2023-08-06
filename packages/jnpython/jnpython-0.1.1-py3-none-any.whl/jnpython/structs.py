from math import copysign, exp, sqrt
from random import randint

# Knuth / Fisher–Yates shuffle
def shuffle(arr:list):
    for i in range(len(arr)-1, 0, -1): # for (int i = v.Length - 1; i >= 0; i--)
        # Swap element "i" with a random earlier element it (or itself)
        # ... except we don't really need to swap it fully, as we can
        # return it immediately, and afterwards it's irrelevant.
        swapIndex = randint(0,i) 
        yield arr[swapIndex]
        arr[swapIndex] = arr[i]

class Point:
    def __init__(self, v:list) -> None:
        self.v = [x for x in v]

    def distance_to(self, other):
        if len(self.v) != len(other.v):
            raise Exception("Point dimensions doesn't match")
        dist = 0.0
        for i, x in enumerate(self.v):
            dist += (other.v[i] - x) * (other.v[i] - x)
        return sqrt(dist)


####################### Single linked stack and queue ##########################

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Bag:
    def __init__(self):
        self.head:Node = None
        self.size:int = 0
    
    def __str__(self):
        return "bag of " + str(self.size)

    def size(self): return self.size
    
    def is_empty(self): return self.size == 0

    def peek(self):
        if self.is_empty():
            return None
        node = self.head
        n = randint(0,self.size-1)
        for i in range(0,n):
            node = node.next
        return node.value

    def add(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        self.size += 1

    def remove(self):
        if self.is_empty():
            raise Exception("Empty bag")
        if self.size == 1:
            val = self.head.value
            self.head = None
        else:
            n = randint(0,self.size-1)
            node = self.head
            for i in range(0,n):
                node = node.next
            
            if n < self.size -1:
                val = node.next.value
                node.next = node.next.next
            else: # last node, use first node as "next"
                val = self.head.value
                self.head = self.head.next

        self.size -= 1
        return val
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.size > 0:
            return self.remove()
        raise StopIteration

class Stack:
    def __init__(self):
        self.__set_head(None)
        self.__set_size(0)

    def __get_head(self):
        return self.__head

    def __set_head(self, val:Node):
        self.__head = val

    def __get_size(self):
        return self.__size

    def __set_size(self, val:int):
        self.__size = val

    size = property(__get_size)
    head = property(__get_head)
    
    def __str__(self):
        cur = self.head
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-2]

    def __iter__(self):
        return self

    def __next__(self):
        if self.size > 0:
            return self.pop()
        raise StopIteration

    def __len__(self): return self.__size

    def copy(self): return self.reverse_copy().reverse_copy()

    def reverse_copy(self):
        res = Stack()
        cur = self.head
        while cur:
            res.push(cur.value)
            cur = cur.next
        return res

    def is_empty(self): return self.size == 0

    def peek(self):
        if self.is_empty():
            return None
        return self.head.value

    def push(self, value):
        node = Node(value)
        node.next = self.head
        self.__set_head(node)
        self.__set_size(self.size + 1)
 
    def pop(self):
        if self.is_empty():
            raise Exception("Empty stack")
        remove = self.head
        self.__set_head(self.head.next)
        self.__set_size(self.size - 1)
        return remove.value
    
class Queue:
    def __init__(self):
        self.head = None
        self.last = None
        self.size = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.size > 0:
            return self.dequeue()
        raise StopIteration
    
    def __str__(self):
        cur = self.head
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-2]

    def __len__(self): return self.size

    def copy(self):
        res = Queue()
        cur = self.head
        while cur:
            res.enqueue(cur.value)
            cur = cur.next
        return res

    def reverse_copy(self):
        res = Queue()
        stack = Stack()
        cur = self.head
        while cur:
            stack.push(cur.value)
            cur = cur.next
        for v in stack:
            res.enqueue(v)
        return res

    def is_empty(self): return self.size == 0

    def peek(self):
        if self.is_empty():
            return None
        return self.head.next.value

    def enqueue(self, value):
        old_last = self.last
        self.last = Node(value)
        if self.is_empty():
            self.head = self.last
        else:
          old_last.next = self.last
        self.size += 1
 
    def dequeue(self):
        if self.is_empty():
            raise Exception("Empty queue")
        remove = self.head
        self.head = self.head.next
        self.size -= 1
        if self.is_empty():
            self.last = None
        return remove.value
    
############################## Priority queues #################################

class __PQ:
    def __init__(self, initial_capacity:int=16):
        self.pq = [None]*(initial_capacity+1) # elements
        self.capacity = initial_capacity # 
        self.size = 0 # number of elements

    def is_empty(self): return self.size == 0

    def peek(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.pq[1]

    def __len__(self): return self.size

    def __getitem__(self, i): return self.pq[i+1]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.size:
            self.n +=1
            return self.pq[self.n]
        raise StopIteration

    def less(self, i, j):
        return self.pq[i] < self.pq[j]

    def greater(self, i, j):
        return self.pq[i] > self.pq[j]

    def exch(self, i , j): self.pq[i], self.pq[j] = self.pq[j], self.pq[i]

    def double_capacity(self):
        self.pq = self.pq + [None] * self.capacity
        self.capacity = self.capacity * 2

    def halve_capacity(self):
        self.pq = self.pq[:self.capacity // 2]
        self.capacity = self.capacity // 2

class MinPQ(__PQ):
    def __init__(self, initial_capacity:int=16):
        super().__init__(initial_capacity)

    def insert(self, x):
        if self.size == self.capacity:
            self.double_capacity()
        self.size +=1
        self.pq[self.size] = x
        self.__swim(self.size)

    def remove(self, x)->bool:
        if not x in self.pq:
            return False
        else:
            i = self.pq.index(x)
            self.exch(i,self.size)
            self.size -=1
            self.__swim(i)
            self.__sink(i)
            return True

    def del_min(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        self.exch(1, self.size)
        min = self.pq[self.size]
        self.size -=1
        self.__sink(1)
        self.pq[self.size+1] = None # no loitering
        return min

    # heap helper functions

    def __swim(self, k:int):
        while k > 1 and self.greater(k//2,k):
            self.exch(k, k//2) # parent of node at k is at k/2
            k = k //2
    
    def __sink(self, k:int):
        while 2 * k <= self.size:
            j = 2 * k
            if j < self.size and self.greater(j, j+1):
                j +=1
            if not self.greater(k, j):
                break
            self.exch(k, j)
            k = j

class MaxPQ(__PQ):
    def __init__(self, initial_capacity:int=16):
        super().__init__(initial_capacity)

    def insert(self, x):
        if self.size == self.capacity:
            self.double_capacity()
        self.size +=1
        self.pq[self.size] = x
        self.__swim(self.size)
        
    def remove(self, x)->bool:
        if not x in self.pq:
            return False
        else:
            i = self.pq.index(x)
            self.exch(i,self.size)
            self.size -=1
            self.__swim(i)
            self.__sink(i)
            return True

    def del_max(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        max = self.pq[1]
        self.exch(1, self.size)
        self.size -=1
        self.__sink(1)
        self.pq[self.size+1] = None # no loitering
        return max

    # heap helper functions

    def __swim(self, k:int):
        while k > 1 and self.less(k//2,k):
            self.exch(k, k//2) # parent of node at k is at k/2
            k = k //2
    
    def __sink(self, k:int):
        while 2 * k <= self.size:
            j = 2 * k
            if j < self.size and self.less(j, j+1):
                j +=1
            if not self.less(k, j):
                break
            self.exch(k, j)
            k = j

# indexed priority queue with indices between 0 and NMAX-1 (allows client to refer to items in PQ)
class __IndexPQ:
    def __init__(self, max_capacity):
        self.__nmax = max_capacity
        self.size = 0
        self.__keys = [None] * (max_capacity +1) # keys[i] = priority of i
        self.__pq = [-1]*(max_capacity +1) # binary heap using 1-based indexing
        self.__qp = [-1]*(max_capacity +1) # inverse of pq - qp[pq[i]] = pq[qp[i]] = i

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.size:
            self.n +=1
            return self.__keys[self.n]
        raise StopIteration


    def is_empty(self): return self.size == 0

    # is an index on the priority queue?
    def contains(self, i:int):
        if i < 0 or i > self.__nmax:
            return False
        return self.__qp[i] != -1

    # Returns the key associated with index i
    def key_of(self, i:int):
        if i < 0 or i > self.__nmax:
            raise Exception("Index is not in the priority queue")
        else:
            return self.__keys[i]
 
     # array helpers
    def less(self, i, j): return self._IndexPQ__keys[self._IndexPQ__pq[i]] < self._IndexPQ__keys[self._IndexPQ__pq[j]]

    def greater(self, i, j): return self._IndexPQ__keys[self._IndexPQ__pq[i]] > self._IndexPQ__keys[self._IndexPQ__pq[j]]

    def exch(self, i, j): 
        self.__pq[i], self.__pq[j] = self.__pq[j], self.__pq[i]
        self.__qp[self.__pq[i]] = i
        self.__qp[self.__pq[j]] = j

class MinIndexPQ(__IndexPQ):
    def __init__(self, max_capacity:int):
        super().__init__(max_capacity)

    def insert(self, i:int, key):
        if self.contains(i):
            raise Exception("Index is already in the priority queue")
        self.size +=1
        self._IndexPQ__qp[i] = self.size
        self._IndexPQ__pq[self.size] = i
        self._IndexPQ__keys[i] = key
        self.__swim(self.size)

    # Returns an index associated with a minimum key
    # size must be > 0
    def min_index(self): return self._IndexPQ__pq[1]

    # Returns a minimum key
    def min_key(self): return self._IndexPQ__keys[self._IndexPQ__pq[1]]

    # Removes a minimum key and returns its associated index
    def del_min(self)->int:
        if self.size == 0:
            raise Exception("Priority queue underflow")
        min = self._IndexPQ__pq[1]
        self.exch(1, self.size)
        self.size -=1
        self.__sink(1)
        self._IndexPQ__qp[min] = -1
        self._IndexPQ__keys[self._IndexPQ__pq[self.size + 1]] = None # no loitering
        self._IndexPQ__pq[self.size +1] = -1
        return min
    
    # Change the key associated with index i to the specified value
    def change_key(self, i:int, key):
        if not self.contains(i):
            raise Exception("Index is not in the priority queue")
        self._IndexPQ__keys[i] = key
        self.__swim(self._IndexPQ__qp[i])
        self.__sink(self._IndexPQ__qp[i])

    # Decrease the key associated with index i to the specified value
    def decrease_key(self, i:int, key):
        if not self.contains(i):
            raise Exception("Index is not in the priority queue")
        if self._IndexPQ__keys[i] <= key:
            raise Exception("Calling decrease_key() with given argument would not strictly decrease the key")
        self._IndexPQ__keys[i] = key
        self.__sink(self._IndexPQ__qp[i])

    def increase_key(self, i:int, key):
        if not self.contains(i):
            raise Exception("Index is not in the priority queue")
        if self._IndexPQ__keys[i] >= key:
            raise Exception("Calling increas_key() with given argument would not strictly increase the key")
        self._IndexPQ__keys[i] = key
        self.__swim(self._IndexPQ__qp[i])

    # remove the key associated with index i
    def delete(self, i:int):
        if not self.contains(i):
            raise Exception("Index is not in the priority queue")
        index = self._IndexPQ__qp[i]
        self.exch(index, self.size)
        self.size -=1
        self.__swim(index)
        self.__sink(index)
        self._IndexPQ__keys[i] = None
        self._IndexPQ__qp[i] = -1

    # heap helpers
    def __swim(self, k):
        while k > 1 and self.greater(k // 2, k):
            self.exch(k, k // 2)
            k = k // 2
    
    def __sink(self, k):
        while 2 * k <= self.size:
            j = 2 * k
            if j < self.size and self.greater(j, j + 1):
                j +=1
            if not self.greater(k, j):
                break
            self.exch(k, j)
            k = j

class MaxIndexPQ(__IndexPQ):
    def __init__(self, max_capacity:int):
        super().__init__(max_capacity)

    def insert(self, i:int, key):
        if self.contains(i):
            raise Exception("Index is already in the priority queue")
        self.size +=1
        self._IndexPQ__qp[i] = self.size
        self._IndexPQ__pq[self.size] = i
        self._IndexPQ__keys[i] = key
        self.__swim(self.size)
    
    # Returns an index associated with a maximum key
    # size must be > 0
    def max_index(self): return self._IndexPQ__pq[1]

    # Returns a maximum key
    def max_key(self): return self.__keys[self._IndexPQ__pq[1]]

    # Removes a maximum key and returns its associated index
    def del_max(self)->int:
        if self.size == 0:
            raise Exception("Priority queue underflow")
        max = self._IndexPQ__pq[1]
        self.exch(1, self.size)
        self.size -=1
        self.__sink(1)
        self._IndexPQ__qp[max] = -1 # delete
        self._IndexPQ__keys[self._IndexPQ__pq[self.size + 1]] = None # no loitering
        self._IndexPQ__pq[self.size +1] = -1
        return max
    
    # Change the key associated with index i to the specified value
    def change_key(self, i:int, key):
        if not self.contains(i):
            raise Exception("Index is not in the priority queue")
        self._IndexPQ__keys[i] = key
        self.__swim(self._IndexPQ__qp[i])
        self.__sink(self._IndexPQ__qp[i])

    # Decrease the key associated with index i to the specified value
    def decrease_key(self, i:int, key):
        if not self.contains(i):
            raise Exception("Index is not in the priority queue")
        if self.__keys[i] <= key:
            raise Exception("Calling decrease_key() with given argument would not strictly decrease the key")
        self._IndexPQ__keys[i] = key
        self.__sink(self._IndexPQ__qp[i])

    def increase_key(self, i:int, key):
        if not self.contains(i):
            raise Exception("Index is not in the priority queue")
        if self._IndexPQ__keys[i] >= key:
            raise Exception("Calling increas_key() with given argument would not strictly increase the key")
        self._IndexPQ__keys[i] = key
        self.__swim(self._IndexPQ__qp[i])

    # remove the key associated with index i
    def delete(self, i:int):
        if not self.contains(i):
            raise Exception("Index is not in the priority queue")
        index = self._IndexPQ__qp[i]
        self.exch(index, self.size)
        self.size -=1
        self.__swim(index)
        self.__sink(index)
        self._IndexPQ__keys[i] = None
        self._IndexPQ__qp[i] = -1

    # heap helpers
    def __swim(self, k):
        while k > 1 and self.less(k // 2, k):
            self.exch(k, k // 2)
            k = k // 2
    
    def __sink(self, k):
        while 2 * k <= self.size:
            j = 2 * k
            if j < self.size and self.less(j, j + 1):
                j +=1
            if not self.less(k, j):
                break
            self.exch(k, j)
            k = j

# Union find data type (disjoint set data type)
class UF:
    def __init__(self, n:int):
        self.count = n # number of components
        self.id = list(range(0,n+1)) # id[i] = parent of i
        self.rank = [0] * n # rank[i] = rank of subtree rooted at i (cannot be more than 31)

    def find(self, p:int):
        if p <0 or p >= len(self.id):
            raise Exception("Out of range")
        while p != self.id[p]:
            self.id[p] = self.id[self.id[p]] # path comression by halving
            p = self.id[p]
        return p

    def connected(self, p:int, q:int): return self.find(p) == self.find(q)

    def union(self, p:int, q:int):
        i = self.find(p)
        j = self.find(q)
        if i == j:
            return
        # make root of smaller rank point to root of larger rank
        if self.rank[i] < self.rank[j]:
            self.id[i] = j
        elif self.rank[i] > self.rank[j]:
            self.id[j] = i
        else:
            self.id[j] = i
            self.rank[i] +=1
        self.count -=1

####################### Trees ##########################

class RedBlackNode:
    def __init__(self, key, value, color:bool, size:int):
        self.key = key
        self.value = value
        self.left:RedBlackNode = None
        self.right:RedBlackNode = None
        self.color:bool = color # RED = True, BLACK = False
        self.size:int = size
      
# A 2-3 tree encoded with red link leaning left if 3-node.
class RedBlackBST:
    def __init__(self):
        self.root:RedBlackNode = None

    def __len__(self): return self.size()

    def __getitem__(self, i): return self.select(i)

    # used with "in",  if key in tree...
    def __contains__(self, key): return self.__contains(self.root, key)
    
    def __str__(self):
        return "LLRBT of size " + str(self.size())

    def pretty_print(self):
        nodes = []
        nodes.append(self.root)
        lines = []
        self.__print_row(nodes, lines)

        for line in lines:
            print(line)
       # print("\n".join(lines))

    def __print_row(self, nodes, lines:list):
        if len(nodes)==0:
            return
        s = ""
        next_row = []
        for i in range(0,len(nodes)):
            s += '*'
            if nodes[i].left != None:
                next_row.append(nodes[i].left)
            if nodes[i].right != None:
                next_row.append(nodes[i].right)
         
        lines.append(s)
        self.__print_row(next_row, lines)

        
    
    
    def __print_row2(self, nodes, indent=50, penalty = 0):
        if len(nodes)==0:
            return
        s = ""
        _penalty = penalty
        space =4
        next_row = []
        penalty = 0
        for i in range(0,len(nodes)):
            s += nodes[i].value
            if i < len(nodes) -1:
                s += " " * max((indent*2-space),2)
            if nodes[i].left != None:
                next_row.append(nodes[i].left)
            else:
                penalty += 2
            if nodes[i].right != None:
                next_row.append(nodes[i].right)
            else:
                penalty += 2
        print(" " * (indent + _penalty), s)
        if penalty > 0:
            penalty += 5 
        self.__print_row(next_row, indent - (indent//2), penalty)

    # number of key-value pairs in this symbol table
    def size(self): return self.__node_size(self.root)

    def height(self): return self.__node_height(self.root)

    def is_empty(self): return self.root == None

    # node helpers:

    def __is_red(self, node:RedBlackNode):
        if node == None:
            return False
        return node.color

    def __node_size(self, node:RedBlackNode):
        if node == None:
            return 0
        return node.size

    def __node_height(self, node:RedBlackNode):
        if node == None:
            return -1
        return 1+ max(self.__node_height(node.left), self.__node_height(node.right))

    # basic operations:

    def get(self,key):  return self.__get(self.root, key)

    def __get(self,node:RedBlackNode, key):
        while node != None:
            if(key < node.key):
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        raise Exception("Key not found!")

    def contains(self,key):  return self.__contains(self.root, key)

    def __contains(self,node:RedBlackNode, key):
        while node != None:
            if(key < node.key):
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return True
        return False

    def put(self, key, value):  
        self.root = self.__put(self.root, key, value)
        self.root.color = False

    def __put(self, node: RedBlackNode, key, value): 
        if node == None:
            return RedBlackNode(key, value, True, 1)
        if key < node.key:
            node.left = self.__put(node.left, key, value)
        elif key > node.key:
            node.right = self.__put(node.right, key, value)
        else:
            node.value = value

        # fix-up any right-leaning links
        if self.__is_red(node.right) and not self.__is_red(node.left):
            node = self.__rotate_left(node)
        if self.__is_red(node.left) and self.__is_red(node.left.left): 
            node = self.__rotate_right(node)
        if self.__is_red(node.left) and self.__is_red(node.right): 
            self.__flip_colors(node)
        node.size = self.__node_size(node.left) + self.__node_size(node.right) + 1

        return node

    # delete the key-value pair with the given key
    def delete(self, key):
        if not self.contains(key):
            return None
        # if both children of root are black, set root to red
        if not self.__is_red(self.root.left) and not self.__is_red(self.root.right):
            self.root.color = True # RED
        self.root = self.__delete(self.root, key)
        if not self.is_empty():
            self.root.color = False # BLACK

    def __delete(self, h:RedBlackNode, key):
        if key < h.key:
            if not self.__is_red(h.left) and not self.__is_red(h.left.left):
                h = self.__move_red_left(h)
            h.left = self.__delete(h.left, key)
        else:
            if self.__is_red(h.left):
                h = self.__rotate_right(h)
            if key == h.key and h.right == None:
                return None
            if not self.__is_red(h.right) and not self.__is_red(h.right.left):
                h = self.__move_red_right(h)
            if key == h.key:
                x = self.__min(h.right)
                h.key = x.key
                h.value = x.value
                h.right = self.__delete_min(h.right)
            else:
                h.right = self.__delete(h.right, key)
        return self.__balance(h)

    # delete the key-value pair with the minimum key
    def delete_min(self):
        if self.is_empty():
            raise Exception("BST underflow")
        # if both children of root are black, set root to red
        if self.root.left.color and not self.root.right.color:
            self.root.color = True # (True = RED)
        self.__delete_min(self.root)
        if not self.is_empty():
            self.root.color = False # (False = BLACK)

    def __delete_min(self, h:RedBlackNode):
        if h.left == None:
            return None
        if not self.__is_red(h.left) and h.left.left != None and not h.left.left.color:
            h = self.__move_red_left(h)
        h.left = self.__delete_min(h.left)
        return self.__balance(h)

    def delete_max(self):
        if self.is_empty():
            raise Exception("BST underflow")
        # if both children of root are black, set root to red
        if self.root.left.color and not self.root.right.color:
            self.root.color = True # (True = RED)
        self.__delete_max(self.root)
        if not self.is_empty():
            self.root.color = False # (False = BLACK)

    def __delete_max(self, h:RedBlackNode):
        if h.left.color:
            h =  self.__rotate_right(h)
        if h.right == None:
            return None
        if not h.right.color and not h.right.left.color:
            h = self.__move_red_right(h)
        h.right = self.delete_min(h.right)
        return self.__balance(h)

    def copy(self):
        copy = RedBlackBST()
        for key in self.keys():
            copy.put(key, self.get(key))
        return copy

    # Red black helpers

    # make a left-leaning link lean to the right
    def __rotate_right(self, h: RedBlackNode):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = x.right.color
        x.right.color = True
        x.size = h.size
        h.size = self.__node_size(h.left) + self.__node_size(h.right) + 1
        return x
    
    # make a right-leaning link lean to the left
    def __rotate_left(self, h:RedBlackNode):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = x.left.color
        x.left.color = True
        x.size = h.size
        h.size = self.__node_size(h.left) + self.__node_size(h.right) + 1
        return x

    # flip the colors of a node and its two children
    def __flip_colors(self, h:RedBlackNode):
        if h != None and h.left != None and h.right != None:
            if (not h.color and h.left.color and h.right.color) or (h.color and not h.left.color and not h.right.color):
                h.color = not h.color # h must have opposite color of its two children    
                h.left.color = not h.left.color
                h.right.color = not h.right.color

    # assuming h is red and both h.left and h.left.left are black, 
    # make h.left or one of its children red
    def __move_red_left(self, h:RedBlackNode):
        self.__flip_colors(h)
        if self.__is_red(h.right.left):
            h.right = self.__rotate_right(h.right)
            h = self.__rotate_left(h)
        return h

    # assuming h is red and both h.right and h.right.left are black, 
    # make h.right or one of its children red
    def __move_red_right(self, h:RedBlackNode):
        self.__flip_colors(h)
        if h.left != None and self.__is_red(h.left.left):
            h.right = self.__rotate_right(h)
        return h
    
    # restore red-black tree invariant
    def __balance(self, h:RedBlackNode):
        if self.__is_red(h.right):
            h =self.__rotate_left(h)
        if self.__is_red(h.left) and self.__is_red(h.left.left):
            h = self.__rotate_right(h)
        if self.__is_red(h.left) and self.__is_red(h.right):
            self.__flip_colors(h)
        h.size = 1 + self.__node_size(h.left) + self.__node_size(h.right)
        return h

    # ordered symbol table methods

    # the smallest key
    def min_key(self):
        if self.is_empty():
            return None
        return self.__min(self.root).key

    def __min(self, x:RedBlackNode = None):
        if x.left == None:
            return x
        else:
            return self.__min(x.left)
    
    # the largest key
    def max_key(self):
        if self.is_empty():
            return None
        return self.__max(self.root).key

    def __max(self, x:RedBlackNode = None):
        if x.right == None:
            return x
        else:
            return self.__max(x.right)

    # the largest key less than or equal to the given key
    def floor_key(self, key):
        x = self.__floor(self.root, key)
        if x == None:
            return None
        else:
            return x.key

    def __floor(self, x:RedBlackNode, key):
        if x == None:
            return None
        if key == x.key:
            return x
        if key < x.key:
            return self.__floor(x.left, key)
        t = self.__floor(x.right, key)
        if t != None:
            return t
        else:
            return x

    # the smallest key greater than or equal to the given key
    def cieling_key(self, key):
        x = self.__cieling(self.root, key)
        if x == None:
            return None
        else:
            return x.key

    def __cieling(self, x:RedBlackNode, key):
        if x == None:
            return None
        if key == x.key:
            return x
        if key > x.key:
            return self.__cieling(x.left, key)
        t = self.__ceiling(x.left, key)
        if not t == None:
            return t
        else:
            return x
    
    # the key of rank k
    def select(self, k:int):
        if k < 0 or k >= self.size():
            return None
        x = self.__select(self.root, k)
        return x.key

    def __select(self, x:RedBlackNode, k:int):
        t = self.__node_size(x.left)
        if t > k:
            return self.__select(x.left, k)
        elif t < k:
            return self.__select(x.right, k-t -1)
        else:
            return x

    # number of keys less than key
    def rank(self, key): return self.__rank(key, self.root)

    def __rank(self, key, x:RedBlackNode = None):
        if x == None:
            return 0
        if key < x.key:
            return self.__rank(key, x.left)
        elif key > x.key:
            return 1 + self.__node_size(x.left) + self.__rank(key, x.right)
        else:
            return self.__node_size(x.left) 
    
    # number of keys between lo and hi   
    def rank_span(self, lo, hi):
        if lo > hi:
            return 0
        if self.contains(hi):
            return self.rank(hi) - self.rank(lo) + 1
        else:
            return self.rank(hi) - self.rank(lo)

    # Enumeration:

    def keys(self):
        q = Queue()
        self.__keys(self.root, q, self.min_key(), self.max_key())
        return q

    # add the keys between lo and hi in the subtree rooted at x to the queue
    def __keys(self, x:RedBlackNode, q:Queue, lo, hi):
        if x == None:
            return
        if lo < x.key:
            self.__keys(x.left, q, lo, hi)
        if lo <= x.key and hi >= x.key:
            q.enqueue(x.key)
        if hi > x.key:
            self.__keys(x.right, q, lo, hi)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.size():
            self.n +=1
            return self[self.n-1]
        raise StopIteration

    # self check functions:

    # does this binary tree satisfy symmetric order?
    # this test also ensures that data structure is a binary tree since order is strict
    def check(self) -> bool:
        is_ok = True
        is_ok &= self.__is_bst(self.root)
        is_ok &= self.__is_size_consistent(self.root)
        is_ok &= self.__is_rank_consistent()
        is_ok &= self.__is_23(self.root)
        is_ok &= self.__is_balanced()
        return is_ok

    # is the tree rooted at node a BST with all keys strictly between min and max
    # (if min or max is null, treat as empty constraint)
    # Credit: Bob Dondero's elegant solution
    def __is_bst(self, node:RedBlackNode, min=None, max = None):
        if node == None:
            return True
        if min != None and node.key <= min:
            return False
        if max != None and node.key >= max:
            return False
        return self.__is_bst(node.left, min, node.key) and self.__is_bst(node.right, node.key, max)

    # are the size fields correct?
    def __is_size_consistent(self, node:RedBlackNode):
        if node == None:
            return True
        #if node.size != node.left.size + node.right.size + 1:
        if node.size != (0 if node.left == None else node.left.size) + (0 if node.right == None else node.right.size) + 1:
            return False
        return self.__is_size_consistent(node.left) and self.__is_size_consistent(node.right)

    def __is_rank_consistent(self):
        for i in range(0,self.size()):
            if i != self.rank(self.select(i)):
                return False
        for k in self.keys():
            if k != self.select(self.rank(k)):
                return False
        return True

    # Does the tree have no red right links, and at most one (left) red links in a row on any path?
    def __is_23(self, x:RedBlackNode):
        if x == None:
            return True
        if x.right != None and x.right.color: # True = RED, False = BLACK
            return False
        if x != self.root and x.color and x.left != None and x.left.color:
            return False
        return self.__is_23(x.left) and self.__is_23(x.right)

    # do all paths from root to leaf have same number of black edges?
    def __is_balanced(self):
        black = 0 # number of black links on path from root to min
        x = self.root
        while x != None:
            if not self.__is_red(x):
                black += 1
            x = x.left
        return self.__is_node_balanced(self.root, black)

    def __is_node_balanced(self, x:RedBlackNode, black:int):
        if x == None:
            return black == 0
        if not self.__is_red(x):
            black -= 1
        return self.__is_node_balanced(x.left, black) and self.__is_node_balanced(x.right, black)

def main():

   
    pass
  


   
if __name__ == "__main__":
    #sys.exit(main())
    main()


