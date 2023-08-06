from time import time
from .graphs import Graph, ConnectedComponents

# shows the execution time of the function object passed
def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'{func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func

# distance between two points defined as tuples or lists (vectors)
# ...or use math.dist(a, b) or numpy: np.linalg.norm(a-b) or scipy.spatial: distance.euclidean(a, b)
def euclidean_distance(a:tuple, b:tuple):
    if not hasattr(a, '__len__'):
        return ((b-a)*(b-a))**0.5
    if len(a) != len(b):
        raise Exception("Point dimensions doesn't match")
    dist = sum((z[1]-z[0])*(z[1]-z[0]) for z in zip(a,b))**0.5
    return dist

def matrix_mul(A,B):
    if not isinstance(A, list) and not isinstance(B,list):
        raise Exception("argument error")
    try:
        len(A[0])
    except:
        A = [A]
    try:
         len(B[0])
    except:
        B = [[i] for i in B]

    if len(A[0]) != len(B):
        raise Exception("matrix dimensions must be m*n and n*m")
        
    ret = [[sum(a*b for a,b in zip(A_row,B_col)) for B_col in zip(*B)] for A_row in A]

    if len(ret)==1:
        return ret[0]
    else:
        return ret
    
# returns 
def dbscan(db:list, min_pts, eps = 1e-16):
    labels = [0]*len(db)
    g = Graph(len(db))
    for i in db:
        for j in range(i+1,len(db)):
            d = euclidean_distance(db[i],db[j])
            if d <= eps: # density check
                g.add_edge(i,j) # connect points
    
    cc = ConnectedComponents(g)
    outliers = []
    for i, lb in enumerate(labels):
        n = len(g.adjacency_list[i])
        if n == 0:
            lb = -2 # noise
        elif n < min_pts:
            lb = -1 # outlier
            outliers.append(i)
        else:
            lb = cc.id(i)
    
    return (outliers, labels)

"""
def main():


   outlers, lables = dbscan([1,20,3,4,5,99,5,2,77,4,3000000], 5, 0.1)

   print(outlers)
   print(lables)
   
if __name__ == "__main__":
    main()
"""