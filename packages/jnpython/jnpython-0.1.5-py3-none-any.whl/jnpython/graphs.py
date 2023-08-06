from functools import reduce
from math import inf
from structs import MinIndexPQ, MinPQ, Queue, RedBlackBST, Stack, UF
from random import randint, random, seed

class Graph:
    def __init__(self, v:int): # v=number of verticies
        if v<0:
            raise Exception("Number of vertices must be nonnegative")
        self.V = v
        self.E = 0
        self.adjacency_list = [[] for _ in range(v)]

    def __str__(self):
        c = sum(len(x) for x in self.adjacency_list) // 2
        return "graph: " + str(self.V) + " vertices, " + str(c) + " edges"
    
    def pretty_print(self):
        lines = []
        lines.append(str(self.V))
        lines.append(str(self.E))
        for i in range(0, self.V):
            for w in self.adjacency_list[i]:
                lines.append(str(i) + " " + str(w))
        return '\n'.join(lines)


    # add an edge v-w
    def add_edge(self, v:int, w:int):
        self.E +=1
        self.adjacency_list[v].append(w); # add an edge v->w
        self.adjacency_list[w].append(v); # add an edge v<-w 

    def copy(self):
        g = Graph(self.V)
        for v in range(0,self.V):
            # reverse so that adjacency list is in same order as original
            reverse = Stack()
            for w in self.adjacency_list[v]:
                reverse.push(w)
            for w in reverse:
                g.adjacency_list[v].append(w)
        return g

    @staticmethod
    def degree(g, v:int):
        return len(g.adjacency_list[v])

    @staticmethod
    def max_degree(g):
        max = 0
        deg = 0
        for i in range(0,g.V):
            deg = Graph.degree(g, i)
            if deg > max:
                max = deg
        return max

    @staticmethod
    def avg_degree(g): return 2.0 * g.E / g.V

    @staticmethod
    def number_of_self_loops(g): 
        c = 0
        for i in range(0,g.V):
            for w in g.adjacency_list[i]:
                if(i==w):
                    c +=1
        return c//2

# Directed graph
class Digraph:
    def __init__(self, v:int): # v=number of verticies
        if v<0:
            raise Exception("Number of vertices must be nonnegative")
        self.V = v
        self.E = 0
        self.adjacency_list = [[] for _ in range(v)]

    def __str__(self):
        c = sum(len(x) for x in self.adjacency_list)
        return "directed graph: " + str(self.V) + " vertices, " + str(c) + " edges"
    
    def pretty_print(self):
        lines = []
        lines.append(str(self.V))
        lines.append(str(self.E))
        for i in range(0, self.V):
            for w in self.adjacency_list[i]:
                lines.append(str(i) + " " + str(w))
        return '\n'.join(lines)


    # add an edge v-w
    def add_edge(self, v:int, w:int):
        self.E +=1
        self.adjacency_list[v].append(w); # add an edge v->w

    def remove_edge(self, v:int, w:int):
        if self.E == 0:
            raise Exception("No edges to remove")
        elif not w in self.adjacency_list[v]:
            raise Exception("Unknown edge " + str(v) + " to " + str(w))
        else:
            self.adjacency_list[v].remove(w)
            self.E -=1
        
    def reverse(self):
        g = Digraph(self.V)
        for v in range(0,self.V):
            for w in self.adjacency_list[v]:
                g.add_edge(w,v)
        return g


    def copy(self):
        g = Digraph(self.V)
        for v in range(0,self.V):
            reverse = Stack()
            for w in self.adjacency_list[v]:
                reverse.push(w)
            for w in reverse:
                g.adjacency_list[v].append(w)
        return g

    @staticmethod
    def degree(g, v:int):
        return Graph.degree(g,v)

    @staticmethod
    def max_degree(g):
        return Graph.max_degree(g)

    @staticmethod
    def avg_degree(g): return Graph.avg_degree(g)

    @staticmethod
    def number_of_self_loops(g): 
        return Graph.number_of_self_loops(g)

    @staticmethod
    def from_graph(g:Graph): 
        dg = Digraph(g.V)
        for v in range(g.V):
            for _, w in enumerate(g.adjacency_list[v]):
                dg.add_edge(v, w)
        return dg

# builds graph from strings instead of integers for vertices (wrapper for regular graph)  
# example input: MovieName1/Actor1/Actor2/Actor3\nMovieName2/Actor4/Actor5/Actor2\n... (delimeter = '/')
class SymbolGraph:
    def __init__(self, input:str, delimeter:str): 
        self.st = RedBlackBST() # string -> index
        self.keys = [] # index -> string

        # First pass builds the symbol table by reading strings to associate distinct strings with an index
        str_rows = input.splitlines()
        for row in str_rows:
            cols = row.split(delimeter)
            for col in cols:
                if not self.st.contains(col):
                    self.st.put(col, self.st.size())

        # inverted index to get string keys in an array 
        self.keys = [""] * self.st.size()
        for name in self.st.keys():
            self.keys[self.st.get(name)] = name

        # second pass builds the graph by connecting first vertex on each line to all others
        self.g = Graph(self.st.size())
        for row in str_rows:
            cols = row.split(delimeter)
            v = self.st.get(cols[0])
            for col in cols:
                w = self.st.get(col)
                self.g.add_edge(v,w)


    def __str__(self): return "Symbol Graph"

    def contains(self, s:str)->bool: return self.st.contains(s)

    def index(self, s:str): return self.st.get(s)

    def name(self, v:int): return self.keys[v]

    def kevin_bacon_index(self, source:str, sink:str): return self.degrees_of_separation(source, sink, "") // 2

    # degrees_of_separation / 2 = "Kevin Bacon index"
    def degrees_of_separation(self, source:str, sink:str, result):
        result = []
        ret = -1
        if not self.contains(source):
            result.append("Symbol graph does not contain " + source)
        elif not self.contains(sink):
            result.append("Symbol graph does not contain " + sink)
        else:
            ret = 0
            paths = BreadthFirstPaths(self.g, self.index(source))
            t = self.index(sink)
            if paths.has_path_to(t):
                for v in paths.path_to(t):
                    result.append(self.name(v))
                    ret += 1
            else:
                result.append("Not connected")
        result = "\n".join(result)
        return ret

class SymbolDiGraph:
    def __init__(self, input:str, delimeter:str):
        self.st = RedBlackBST() # string -> index
        self.keys = [] # index -> string

        # First pass builds the symbol table by reading strings to associate distinct strings with an index
        str_rows = input.splitlines()
        for row in str_rows:
            cols = row.split(delimeter)
            for col in cols:
                if not self.st.contains(col):
                    self.st.put(col, self.st.size())

        # inverted index to get string keys in an array 
        self.keys = [""] * self.st.size()
        for name in self.st.keys():
            self.keys[self.st.get(name)] = name

        # second pass builds the graph by connecting first vertex on each line to all others
        self.g = Digraph(self.st.size())
        for row in str_rows:
            cols = row.split(delimeter)
            v = self.st.get(cols[0])
            for col in cols:
                w = self.st.get(col)
                self.g.add_edge(v,w)


    def __str__(self): return "Directed Symbol Graph"

    def contains(self, s:str)->bool: return self.st.contains(s)

    def index(self, s:str): return self.st.get(s)

    def name(self, v:int): return self.keys[v]

class Edge:
    def __init__(self, v:int, w:int, weight:float):
        if v < 0:
            raise Exception("start vertex must be in range [0,n]")
        if w < 0:
            raise Exception("end vertex must be in range [0,n]")

        self.v = v # from
        self.w = w # to
        self.weight = weight

    def __str__(self):
        return str(self.v) +  "-" + str(self.w) + " " + str(self.weight)

    def __cmp__(self,other):
        if self.weight < other.weight:
            return -1
        elif self.weight > other.weight:
            return 1
        else:
            return 0

    def __lt__(self,other): return self.__cmp__(other) == -1
        
    def __gt__(self,other): return self.__cmp__(other) == 1

    def __eq__(self,other): return self.__cmp__(other) == 0

    def either(self): return self.v

    def other(self, vertex:int):
        if vertex == self.v:
            return self.w
        elif vertex == self.w:
            return self.v
        else:
            raise Exception("Illegal endpoint")

    def compare_to(this, that): return this.__cmp__(that)

class EdgeWeightedGraph:
    def __init__(self, v:int):
        self.V = v
        self.E = 0
        self.adjacency_list = []
        for _ in range(0,v):
            self.adjacency_list.append([])
        
    def __str__(self):
        res = []
        res.append(str(self.V))
        res.append(str(self.E))
        for e in self.edges():
            res.append(str(e))
        return "\n".join(res)

    def add_edge(self, e:Edge):
        v = e.either()
        w = e.other(v)
        self.adjacency_list[v].append(e)
        self.adjacency_list[w].append(e)
        self.E +=1

    def add_random_edge(self):
        v = randint(0,v)
        w = randint(0,v)
        weight = random
        self.add_edge(Edge(v,w,weight))

    def copy(self):
        taken = set()
        g = EdgeWeightedGraph(self.V)
        for v in range(0,self.V):
            reverse = Stack()
            list(map(lambda x: reverse.push(x)), self.adjacency_list[v])
        for e in reverse:
            if not e in taken:
                g.add_edge(e)
                taken.add(e)
        return g

    def edges(self):
        edges = []
        for v in range(0, self.V):
            self_loops = 0
            for e in self.adjacency_list[v]:
                if e.other(v) > v:
                    edges.append(e)
                elif e.other(v) == v:
                    if self_loops % 2 == 0:
                        edges.append(e)
                    self_loops +=1
        return edges

    def distance(self, v:int, w:int):
        for e in self.adjacency_list[v]:
            if e.other == w:
                return e.weight
            else:
                raise Exception("No edge found between " + str(v) + " and " + str(w))

    def remove_vertex(self, v:int):
        contain = []
        for i in range(0,len(self.adjacency_list)):
            if i != v:
                E -= len(self.adjacency_list[i])
                contain.append(self.adjacency_list[i])
        for i in range(0,len(contain)):
            for j in len(contain[i]):
                if contain[i][j].w == v:
                    contain[i].remove(contain[i][j])
                    self.E -=1
        self.adjacency_list = contain
        self.V -=1

    @staticmethod
    def degree(g, v:int): return len(g.adjacency_list[v])

    @staticmethod
    def from_edge_weighted_digraph(wg):
        g = EdgeWeightedGraph(wg.V)
        for i in range(0,g.V):
            for e in wg.adjacency_list[i]:
                g.add_edge(Edge(e.v, e.w, e.weight))
        return g

class EdgeWeightedDigraph:
    def __init__(self, v:int):
        self.V = v
        self.E = 0
        self.adjacency_list = []
        for _ in range(0,v):
            self.adjacency_list.append([])
        
    def __str__(self):
        res = []
        res.append(str(self.V))
        res.append(str(self.E))
        for e in self.edges():
            res.append(str(e))
        return "\n".join(res)

    def add_edge(self, e:Edge):
        if e.v > self.V-1 or e.w > self.V-1:
            raise Exception("Edge must be between vertices in range [0..V-1]")

        self.adjacency_list[e.v].append(e)
        self.E +=1

    def add_random_edge(self):
        v = randint(0,v)
        w = randint(0,v)
        weight = random
        self.add_edge(Edge(v,w,weight))

    def edges(self):
        edges = []
        for v in range(0, self.V):
            for e in self.adjacency_list[v]:
                edges.append(e)
        return edges

    # number of directed edges incident from vertex
    def outdegree(self, v:int):
        if v < 0 or v >= self.V:
            raise Exception("Index out of range")
        return len(self.adjacency_list[v])

    def copy(self):
        g = EdgeWeightedGraph(self.V)
        for v in range(0,self.V):
            reverse = Stack()
            list(map(lambda x: reverse.push(x), self.adjacency_list[v]))
        for e in reverse:
            g.add_edge(e)
        return g

    def to_digraph(self):
        g = Digraph(self.V)
        for v in range(0,self.V):
            for e in self.adjacency_list[v]:
                g.add_edge(e.v, e.w)
        return g

class AdjMatrixEdgeWeightedDigraph:
    def __init__(self, v:int):
        self.V = v
        self.E = 0
        # [[None]*v]*v created shallow 1-d array where all indices pointing to None
        self.adj_matrix = [[None for i in range(v)] for j in range(v)]
        
    def __str__(self):
        res = []
        res.append(str(self.V) + " " + str(self.E))
        for v in range(0,self.V):
            res.append(str(v)+ ": ")
            t = ""
            for e in self.adj_matrix[v]:
                t += str(e) + " "
            res.append(t)
        return "\n".join(res)

    def add_edge(self, e:Edge):
        if self.adj_matrix[e.v][e.w] is None:
            self.E += 1
            self.adj_matrix[e.v][e.w] = e

    def adj(self, v):
        for i in range(0, self.V):
            if self.adj_matrix[v][i] is None:
                continue
            yield self.adj_matrix[v][i]

# "find a path" using depth first search
class DepthFirstPaths:
    def __init__(self, g, s:int):
        if not isinstance(g, Graph) and not isinstance(g, Digraph):
            raise Exception("Needs an instance of type Graph or Directed Graph")

        self.source = s
        self.marked = [False] * g.V
        self.edge_to = [False] * g.V
        # find vertices connected to s
        self.__dfs(g, self.source) 
        
    def has_path_to(self, v:int): return self.marked[v]

    def path_to(self, v:int):
        if not self.has_path_to(v):
            return None
        path = Stack()
        i = v
        while i != self.source:
            path.push(i)
            i = self.edge_to[i]
        return path
    
    # recursive depth first search
    def __dfs(self, g, v:int):
        self.marked[v] = True
        for w in g.adjacency_list[v]:
            if not self.marked[w]:
                self.edge_to[w] = v
                self.__dfs(g, w)

# gets number of vertices in graph that are connected to any of the source vertices. Will not compute paths!
class DepthFirstMultiPaths:
    def __init__(self, g, sources:list):
        if not isinstance(g, Graph) and not isinstance(g, Digraph):
            raise Exception("Needs an instance of type Graph or Directed Graph")
        self.marked = [False] * g.V
        self.count == 0
        for v in sources:
            if not self.marked[v]:
                self.__dfs(g, v)
        
    def no_of_vertices_reachable(self): return self.count

    def __dfs(self,g, v:int):
        self.count +=1
        self.marked[v] = True
        for w in g.adjacency_list[v]:
            if not self.marked[w]:
                self.__dfs(g, w)

# "find shortest path" using breadth first search
class BreadthFirstPaths:
    def __init__(self, g, s:int):
        if not isinstance(g, Graph) and not isinstance(g, Digraph):
            raise Exception("Needs an instance of type Graph or Directed Graph")

        self.source = s
        self.marked = [False] * g.V # marked[v] = true if v connects to s
        self.edge_to = [0] * g.V # edgeTo[v] = previous edge on s-v path
        self.dist_to = [inf] * g.V # distTo[v] = number of edges in shortest s-v path
        self.__bfs(g, s) 
    
    # is therer a path s to v?
    def has_path_to(self, v:int): return self.marked[v]

    # no of edges in shortest path s to v
    def dist_to(self, v:int): return self.dist_to[v]

    # shortest path s to v
    def path_to(self, v:int):
        if not self.has_path_to(v):
            return None
        path = Stack()
        i = v
        while i != self.source:
            path.push(i)
            i = self.edge_to[i]
        return path
    
    # breadth-first search from a single source
    def __bfs(self, g, s:int):
        self.dist_to[s] = 0
        self.marked[s] = True
        q = Queue()
        q.enqueue(s)
        while q.size > 0:
            v = q.dequeue()
            for w in g.adjacency_list[v]:
                if not self.marked[w]:
                    self.edge_to[w] = v
                    self.dist_to[w] = self.dist_to[v] + 1
                    self.marked[w] = True
                    q.enqueue(w)

# gets number of vertices in digraph that are connected to any of the source vertices. Will not compute paths!
class BreadthFirstMultiPaths:
    def __init__(self, g, sources:list):
        if not isinstance(g, Graph) and not isinstance(g, Digraph):
            raise Exception("Needs an instance of type Graph or Directed Graph")

        self.marked = [False] * g.V
        self.edge_to = [0] * g.V
        self.dist_to = [inf] * g.V
        self.__bfs(g, sources) 
    
    # is therer a path s to v?
    def has_path_to(self, v:int): return self.marked[v]

    # no of edges in shortest path s to v
    def dist_to(self, v:int): return self.dist_to[v]

    def path_to(self, v:int):
        if not self.has_path_to(v):
            return None
        path = Stack()
        i = v
        while i != self.source:
            path.push(i)
            i = self.edge_to[i]
        return path
    
    # breadth-first search from multiple sources
    def __bfs(self, g, sources:list):
        q = Queue()
        for s in sources:
            self.marked[s] = True
            self.dist_to[s] = 0
            q.enqueue(s)
        
        while q.size() > 0:
            v = q.dequeue()
            for w in g.adjacency_list[v]:
                if not self.marked[w]:
                    self.edge_to[w] = v
                    self.dist_to[w] = self.dist_to[v] + 1
                    self.marked[w] = True
                    q.enqueue(w)

# find connected components in undirected graph using depth-first search
class ConnectedComponents:
    def __init__(self, g:Graph):
        self.__marked = [False] * g.V
        self.__id = [0] * g.V # id[v] = id of component containing v
        self.__size = [0] * g.V # size[id] = number of vertices in given component
        self.count = 0 # no of connected components
        for v in range(g.V):
            if not self.__marked[v]:
                self.__dfs(g,v) # run DFS from one vertex in each component
                self.count += 1
    
    # component id of the connected component containing v
    def id(self, v:int): return self.__id[v]

    # number of vertices in the connected component containing vertex v
    def size(self, v:int): return self.__size[v]

    def are_connected(self, v:int, w:int): return self.__id[v] == self.__id[w]

    def __dfs(self, g:Graph, v:int):
        self.__marked[v] = True
        self.__id[v] = self.count
        self.__size[self.count] += 1
        for w in g.adjacency_list[v]:
            if not self.__marked[w]:
                self.__dfs(g, w)

# strongly connected components (components in directed graph that can be reached from eachother)
class KosarajuSharirSCC:
    def __init__(self, g:Digraph):
        self.count = 0 # no of components
        self.marked = [False] * g.V
        self.id = [0] * g.V 
        dfo = DepthFirstOrder(g.reverse())

        for v in dfo.reverse_post():
            if not self.marked[v]:
                self.__dfs(g,v)
                self.count +=1

    def __dfs(self, g:Digraph, v:int):
        self.marked[v] = True
        self.id[v] = self.count
        for w in g.adjacency_list[v]:
            if not self.marked[w]:
                self.__dfs(g, w)

    def are_strongly_connected(self, v:int, w:int): return self.id[v] == self.id[w]

class TarjanSCC:
    def __init__(self, g:Digraph):
        self.__marked = [False] * g.V
        self.__stack = Stack()
        self.__id = [0] * g.V 
        self.__low = [0] * g.V 
        self.__pre = 0 # preorder number counter
        self.count = 0 # number of strongly-connected components
        for v in range(0,g.V):
            if not self.__marked[v]:
                self.__dfs(g,v)
    
    def are_strongly_connected(self, v:int, w:int): return self.__id[v] == self.__id[w]
        
    def __dfs(self, g:Digraph, v:int):
        self.__marked[v] = True
        self.__low[v] = self.__pre
        self.__pre +=1
        min = self.__low[v]
        self.__stack.push(v)
        for w in g.adjacency_list[v]:
            if not self.__marked[w]:
                self.__dfs(g, w)
            if self.__low[w] < min:
                min = self.__low[w]
        if min < self.__low[v]:
            self.__low[v]= min
            return
        go = True
        while go:
            ww = self.__stack.pop()
            self.__id[ww] = self.count
            self.__low[ww] = g.V
            go = ww != v
        self.count +=1

# depth-first search ordering of the vertices in a digraph or edge-weighted digraph
class DepthFirstOrder:
    def __init__(self, g:Digraph):
        self.__pre = [0] * g.V # pre[v] = preorder  number of v
        self.__post = [0] * g.V # post[v]   = postorder number of v
        self.__postorder = Queue() # vertices in preorder
        self.__preorder = Queue() # vertices in postorder
        self.__marked = [False] * g.V # marked[v] = has v been marked in dfs?
        self.__pre_counter = 0 # counter or preorder numbering
        self.__post_counter = 0 # counter or postorder numbering
        for v in range(0,g.V):
            if not self.__marked[v]:
                self.__dfs(g,v)

    def pre(self, v:int): return self.__pre[v]

    def post(self, v:int): return self.__post[v]

    def reverse_post(self):
        reverse = Stack()
        for v in self.__postorder:
            reverse.push(v)
        return reverse

    def __dfs(self, g:Digraph, v:int):
        self.__marked[v] = True
        self.__pre[v] = self.__pre_counter
        self.__pre_counter +=1
        self.__preorder.enqueue(v)
        for w in g.adjacency_list[v]:
            if not self.__marked[w]:
                self.__dfs(g, w)
        self.__postorder.enqueue(v)
        self.__post[v] == self.__post_counter
        self.__post_counter +=1

    def check(self):
        # check that post(v) is consistent with post()
        r = 0
        for v in self.__postorder:
            if self.post(v) != r:
                return False

        # check that pre(v) is consistent with pre()
        r = 0
        for v in self.__preorder:
            if self.pre(v) != r:
                return False
        
        return True

# determining whether a graph has a cycle, parallell edges or selfloop using depth-first search
class Cycle:
    def __init__(self, g:Graph):
        if isinstance(g, Digraph):
            raise Exception("Use DirectedCycle for Digraphs")
        if not isinstance(g, Graph):
            raise Exception("Graph arguemnt needed")
        self.__cycle = None
        self.__parallell_edges = False
        if self.__find_self_loops(g):
            return
        if self.__find_parallel_edges(g):
            self.__parallell_edges = True
            return
        self.__marked = [False] * g.V
        self.__edge_to = [0] * g.V
        for v in range(0, g.V):
            if not self.__marked[v]:
                self.__dfs(g, -1 , v)

    def has_parallell_edges(self): return self.__parallell_edges

    def has_cycle(self): return self.__cycle is not None

    def get_cycle(self): return self.__cycle.copy()

    # does graph have a self loop (side effect: initialize cycle to be self loop)
    def __find_self_loops(self, g:Graph):
        for v in range(0, g.V):
            for w in g.adjacency_list[v]:
                if v == w:
                    cycle = Stack()
                    cycle.push(v)
                    cycle.push(v)
                    self.__cycle = cycle
                    return True
        return False

    # does graph have two parallel edges (side effect: initialize cycle to be two parallel edges)
    def __find_parallel_edges(self, g:Graph):
        marked = [False] * g.V
        # check for parallel edges incident to v
        for v in range(0,g.V):
            for w in g.adjacency_list[v]:
                if marked[w]:
                    cycle = Stack()
                    cycle.push(v)
                    cycle.push(w)
                    cycle.push(v)
                    return True
                marked[w] = True
            
            # reset marked
            for w in g.adjacency_list[v]:
                marked[w] = False
        return False

    def __dfs(self, g:Graph, u, v):
        self.__marked[v] = True
        for w in g.adjacency_list[v]:
            if self.__cycle is not None:
                return # short circuit if cycle already found
            if not self.__marked[w]:
                self.__edge_to[w] = v
                self.__dfs(g, v, w)
            elif w != u: # check for cycle (but disregard reverse of edge leading to v)
                self.__cycle = Stack()
                x = v
                while x != w:
                    self.__cycle.push(x)
                    x = self.__edge_to[x]
                self.__cycle.push(w)
                self.__cycle.push(v)

class DirectedCycle:
    def __init__(self, g:Digraph):
        self.__cycle = None
        self.__marked = [False] * g.V
        self.__on_stack = [False] * g.V
        self.__edge_to = [0] * g.V
        for v in range(0, g.V):
            if not self.__marked[v]:
                self.__dfs(g, v)

    def has_cycle(self): return self.__cycle is not None

    def get_cycle(self): return self.__cycle.copy() if self.has_cycle() else None

    # check that algorithm computes either the topological order or finds a directed cycle
    def __dfs(self, g:Digraph, v):
        self.__on_stack[v] = True
        self.__marked[v] = True
        for w in g.adjacency_list[v]:
            if self.__cycle != None:
                return # short circuit if cycle already found
            elif not self.__marked[w]: # found new vertex, so recur
                self.__edge_to[w] = v
                self.__dfs(g, w)
            elif self.__on_stack[w]: # trace back directed cycle
                self.__cycle = Stack()
                x = v
                while x != w:
                    self.__cycle.push(x)
                    x = self.__edge_to[x]
                self.__cycle.push(w)
                self.__cycle.push(v)

        self.__on_stack[v] = False

class ShortestDirectedCycle:
    def __init__(self, g:Digraph) -> None:
        raise Exception("Not implemented")

# determinine whether an edge-weighted digraph has a directed cycle
class EdgeWeightedDirectedCycle:
    def __init__(self, g:EdgeWeightedDigraph) -> None:
        self.__marked = [False] * g.V
        self.__edge_to = [None] * g.V
        self.__on_stack = [False] * g.V
        self.__cycle = None

        for v in range(0, g.V):
            if not self.__marked[v]:
                self.__dfs(g,v)

    def has_cycle(self)->bool: return self.__cycle is not None

    def cycle(self)->Stack: 
        if self.has_cycle():
            return self.__cycle.copy()
        else:
            return None

    def check(self)->bool:
        if self.has_cycle():
            first = None
            last = None
            es = self.cycle()
            for e in es:
                if first is None:
                    first = e
                if last is not None:
                    if last.w != e.v:
                        return False # cycle edges {last} and {e} not incident
                last = e
            
            if last.w != first.v:
                return False # cycle edges {last} and {first} not incident
        
        return True





    def __dfs(self, g:EdgeWeightedDigraph, v):
        self.__on_stack[v] = True
        self.__marked[v] = True
        
        for e in g.adjacency_list[v]:
            w = e.w

            if self.__cycle is not None: # directed cycle found
                return

            elif not self.__marked[w]: # found new vertex, recur
                self.__edge_to[w] = e
                self.__dfs(g,w)

            elif self.__on_stack[w]: # trace back directed cycle
                self.__cycle = Stack()
                while e.v != w:
                    self.__cycle.push(e)
                    e = self.__edge_to[e.v]
                self.__cycle.push(e)
        
        self.__on_stack[v] = False

# An Eulerian trail (or Eulerian path) is a trail in a finite graph that visits 
# every edge exactly once (allowing for revisiting vertices)
# An Eulerian circuit or Eulerian cycle is an Eulerian trail that 
# starts and ends on the same vertex
# A connected graph has an Eulerian trail iff zero or two vertices have an odd degree
# A connected graph has an Euler cycle iff every vertex has even degree
# A directed graph has an Eulerian cycle iff every vertex has equal in degree 
# and out degree, and all of its vertices with nonzero degree belong to a 
# single strongly connected component
# A directed graph has an Eulerian trail if and only if at most one vertex has 
# (out-degree) − (in-degree) = 1,  at most one vertex has (in-degree) − (out-degree) = 1
# , every other vertex has equal in-degree and out-degree, and all of its vertices with 
# nonzero degree belong to a single connected component of the underlying undirected graph

class DirectedEulerianCycle:
    def __init__(self, g:Digraph) -> None:
        self.is_eulerian = True # does the digraph have an Eulerian tour?
        self.__cycle = Stack()
        self.__adj = [Queue() for i in range(g.V)] # local view of adjacency lists
        for v,q in enumerate(self.__adj):
            for w in g.adjacency_list[v]:
                q.enqueue(w)
        s = 0 # find vertex with nonzero degree as start of potential Eulerian cycle
        for v in range(g.V):
            if not self.__adj[v].is_empty():
                s = v
                break
        
        # greedily add to cycle, depth-first search style
        stack = Stack()
        stack.push(s)
        while not stack.is_empty():
            v = stack.pop()
            self.__cycle.push(v)
            w = v
            while not self.__adj[w].is_empty():
                stack.push(w)
                w = self.__adj[w].dequeue()
            if w != v:
                self.is_eulerian = False
        # check if all edges have been used
        for v in range(g.V):
            if self.__adj[v].size > 0:
                self.is_eulerian = False

    def eulerian_cycle(self):
        if not self.is_eulerian:
            return None
        return self.__cycle.copy()

# determining whether an undirected graph is bipartite or whether it has an odd-length cycle 
# (can the vertices of a given graph be assigned one of two colors in such a 
# way that no edge connects vertices of the same color?)
class Bipartite:
    def __init__(self, g:Graph) -> None:
        self.is_bipartate = True
        self.__cycle = None
        self.__color = [False] * g.V
        self.__marked = [False] * g.V
        self.__edge_to = [0] * g.V
        for v in range(g.V):
            if not self.__marked[v]:
                self.__dfs(g, v)

    # Returns the side of the bipartite that vertex v is on. (Two verticies are in the same side of the bipartition if and only if they have the same color)
    def color(self, v):
        if not self.is_bipartate:
            raise Exception("Graph is not bipartite")
        return self.__color[v]

    def odd_cycle(self): return None if self.__cycle is None else self.__cycle.copy()

    def __dfs(self, g:Graph, v):
        self.__marked[v] = True
        for w in g.adjacency_list[v]:
            # short circuit if odd-length cycle found
            if self.__cycle is not None:
                return
            # found uncolored vertex, so recur
            if not self.__marked[w]:
                self.__edge_to[w] = v
                self.__color[w] = not self.__color[v]
                self.__dfs(g, w)
            # if v-w create an odd-length cycle, find it
            elif self.__color == self.__color[v]:
                self.is_bipartate == False
                self.__color = Stack()
                self.__cycle.push(w) # don't need this unless you want to include start vertex twice
                x = v
                while x != w:
                    self.__cycle.push(x)
                    x = self.__edge_to[x]
                self.__cycle.push(w)
            
# Identifies articulation points by decomposing a graph into biconnected components
# An articulation vertex (or cut vertex) is a vertex whose removal increases the 
# number of connected components. A graph is biconnected if it has no articulation vertices
class Biconnected:
    def __init__(self, g:Graph) -> None:
        self.__cnt = 0
        self.__low = [-1] * g.V
        self.__pre = [-1] * g.V
        self.articualtion = [False] * g.V
        for v in range(g.V):
            if self.__pre[v] == -1:
                self.__dfs(g, v, v)
    
    # is vertex v an articulation point?
    def is_articualtion(self, v): return self.articualtion[v]

    def is_biconnected(self): return not any(self.articualtion)

    def __dfs(self, g:Graph, u, v):
        children = 0
        self.__pre[v] = self.__cnt
        self.__cnt +=1
        self.__low[v] = self.__pre[v]
        for w in g.adjacency_list[v]:
            if self.__pre[w] == -1:
                children+=1
                self.__dfs(g, v, w)
                # update low number
                self.__low[v] = min(self.__low[v], self.__low[w])
                # non-root of DFS is an articulation point if low[w] >= pre[v]
                if self.__low[w] >= self.__pre[v] and u != v:
                    self.articualtion[v]=True
            elif w != u: # update low number - ignore reverse of edge leading to v
                self.__low[v] = min(self.__low[v], self.__pre[w])
        # root of DFS is an articulation point if it has more than 1 child
        if u == v and children > 1:
            self.articualtion[v] = True

# Identifies bridge edges by decomposing a directed graph into two-edge connected components 
# (assumes no parallel edges)
class Bridge:
    def __init__(self, g) -> None:
        if isinstance(g, Graph):
            if Cycle(g).has_parallell_edges():
                raise Exception("Graph has parallell edges (creating false bridge)")
        self.__cnt = 0
        self.__bridges = []
        self.__low = [-1] * g.V
        self.__pre = [-1] * g.V
        for v in range(g.V):
            if self.__pre[v] == -1:
                self.__dfs(g, v, v)
    
    def components(self): return len(self.__bridges) +1

    def bridges(self): return self.__bridges

    def __dfs(self, g:Graph, u, v):
        self.__pre[v] = self.__cnt
        self.__cnt +=1
        self.__low[v] = self.__pre[v]
        for w in g.adjacency_list[v]:
            if self.__pre[w] == -1:
                self.__dfs(g, v, w)
                self.__low[v] = min(self.__low[v], self.__low[w])
                if self.__low[w] == self.__pre[w]:
                    self.__bridges.append(f"{str(v)}-{str(w)}")
            elif w != u: # update low number - ignore reverse of edge leading to v
                self.__low[v] = min(self.__low[v], self.__pre[w])

# A graph is planar if it can be drawn in the plane such that no edges cross one another
# Hopcroft-Tarjan algorithm is an advanced application of depth-first search that determines 
# # whether a graph is planar in linear time
class Planary:
    def __init__(self, g:Digraph):
        raise Exception("Not implemented")
    
# topological sort, topsort, (works on DAG - directed acyclic graph, no cycles) determines whether 
# the digraph has a topological order and finds such a topological order.
# The canonical application of topological sorting is in scheduling a sequence of 
# jobs or tasks based on their dependencies
class Topological:
    def __init__(self, g):
        if not isinstance(g, Digraph) and not isinstance(g, EdgeWeightedDigraph):
            print(type(g))
            raise Exception("Needs an instance of Digraph or EdgeWeightedDigraph")
        
        self.order = None
        if isinstance(g, EdgeWeightedDigraph):
            g = g.to_digraph()
        
        self.__finder = DirectedCycle(g)
        if not self.__finder.has_cycle():
            dfo = DepthFirstOrder(g)
            self.order = dfo.reverse_post()
    
    def has_order(self): return self.order is not None

# Compute topological ordering of a DAG
class TopologicalQueue:
    def __init__(self, g:Digraph):
        self.__order = Queue() # vertices in topological order
        self.__indegree = [0] * g.V # indegree[v] = indegree of vertex v
        self.__rank = [0] * g.V # rank[v] = order where vertex v appers in order
        self.count = 0 # for computing the ranks

        # compute indegrees
        for v in range(0, g.V):
            for w in g.adjacency_list[v]:
                self.__indegree[w] +=1

        # initialize queue to contain all vertices with indegree = 0
        queue = Queue()
        for v in range(0, g.V):
            if self.__indegree[v] == 0:
                queue.enqueue(v)
        for v in queue:
            self.__order.enqueue(v)
            self.__rank[v] = self.count
            self.count +=1
            for w in g.adjacency_list[v]:
                self.__indegree[w] == 0
                queue.enqueue(w)
    
    # is g a directed acyclic graph?
    def is_dag(self)->bool:
        for v in self.__indegree:
            if v != 0:
                return False
        return True

    # the vertices in topological order
    def order(self):
        if self.is_dag():
            return self.__order.copy()
        else:
            return None
    
    # the rank of vertex v in topological order
    def rank(self, v:int): return self.__rank[v]

# depth-first search from each vertex and storing the results. Works for small or dense digraphs, 
# but not large graphs since the constructor uses space proportional to V^2 and time proportional to V (V + E).
# answer questions like "can one get from node a to node d"
class TransitiveClosure:
    def __init__(self, g:Digraph):
        self.__tc = [None] *  g.V
        for v in range(0, g.V):
            self.__tc[v] = DepthFirstPaths(g, v)

    # Is there a directed path from v to w
    def reachable(self, v:int, w:int): return self.__tc[v].marked[w]

############# MINIMUM SPANNING TREE ALGORITHMS ####################

# compute MST (minmal spanning tree) in E log E
# MST: connects all the vertices together, without any cycles and with the minimum possible total edge weight
class KruskalMST:
    def __init__(self, g:EdgeWeightedGraph):
        self.mst = Queue()
        self.weight = 0 # weight of MST
        self.__pq = MinPQ()
        for e in g.edges():
            self.__pq.insert(e)
        self.__uf = UF(g.V)
        while not self.__pq.is_empty() and self.mst.size < g.V:
            e = self.__pq.del_min()
            v = e.either()
            w = e.other(v)
            if not self.__uf.connected(v,w):
                self.__uf.union(v,w)
                self.mst.enqueue(e)
                self.weight += e.weight

    def edges(self): return self.mst

# minimum spanning forest using a lazy version of Prim's algorithm. Edge weights can be positive, zero, or negative and need not be distinct
# If the graph is not connected, it computes a minimum spanning forest which is the union of minimum spanning trees in each connected component
# Slower than EagerPrim (PrimMST)
class LazyPrimMST:
    def __init__(self, g:EdgeWeightedGraph):
        self.weight = 0
        self.mst = Queue() # edges in the MST
        self.__pq = MinPQ() # edges with one endpoint in tree
        self.__marked = [False] * g.V #  marked[v] = true if v on tree
        for i, x in enumerate(self.__marked):
            if not x:
                self.__prim(g, i) # run Prim from all vertices to get a minimum spanning forest
    
    def edges(self): return self.mst.copy()

    # Prim's algorithm
    def __prim(self, g, s:int):
        self.__scan(g, s)
        while not self.__pq.is_empty(): #  better to stop when mst has V-1 edges
            e = self.__pq.del_min()
            v = e.either()
            w = e.other(v) # two endpoints
            if self.__marked[v] and self.__marked[w]: # lazy, both v and w already scanned
                continue
            self.mst.enqueue(e)
            self.weight += e.weight
            if not self.__marked[v]: 
                self.__scan(g, v) # v becomes part of tree
            if not self.__marked[w]:
                self.__scan(g, w) # w becomes part of tree

    # add all edges e incident to v onto pq if the other endpoint has not yet been scanned
    def __scan(self, g:EdgeWeightedGraph, v):
        self.__marked[v] = True
        for e in g.adjacency_list[v]:
            if not self.__marked[e.other(v)]:
                self.__pq.insert(e)
    
# computing a minimum spanning tree in an edge-weighted graph. Edge weights can be positive, zero, or negative and need not be distinct.
# If the graph is not connected, it computes a minimum spanning forest which is the union of minimum spanning trees in each connected component
class PrimMST:
    def __init__(self, g:EdgeWeightedGraph):
        self.v = g.V
        self.edge_to = [None] * g.V # edgeTo[v] = shortest edge from tree vertex to non-tree vertex
        self.dist_to = [inf] * g.V # weight of shortest such edge
        self.marked = [False] * g.V # marked[v] = true if v on tree, false otherwise
        self.pq = MinIndexPQ(g.V)
        for v in range(0,g.V): # run from each vertex to find
            if not self.marked[v]:
                self.__prim(g, v) # minimum spanning forest

    def weight(self): return reduce(lambda x,y: x+y, [e.weight for e in self.edge_to if e is not None] )

    def edges(self): return [e for e in self.edge_to if e is not None]

    # run Prim's algorithm in graph G, starting from vertex s
    def __prim(self, g, s):
        self.dist_to[s] = 0.0
        self.pq.insert(s, self.dist_to[s])
        while not self.pq.is_empty():
            v = self.pq.del_min()
            self.__scan(g, v)

    # scan vertex v
    def __scan(self, g:EdgeWeightedGraph, v):
        self.marked[v] = True
        for e in g.adjacency_list[v]:
            w = e.other(v)
            if self.marked[w]:
                continue # v-w is obsolete edge
            if e.weight < self.dist_to[w]:
                self.dist_to[w] = e.weight
                self.edge_to[w] = e
                if self.pq.contains(w):
                    self.pq.decrease_key(w, self.dist_to[w])
                else:
                    self.pq.insert(w, self.dist_to[w])

############# SHORTEST PATH ALGORITHMS ####################

# Eager Dijkstra Computes a shortest paths tree from s to every other vertex in the edge-weighted digraph. 
# Eager because of index PQ and updates instead of lazy inserting/validating in PQ
# Most efficient Dijkstra for large graphs uses Fibonacci Heap, not implemented here.
# No negative weights allowed
class DijkstraSP:
    def __init__(self, g:EdgeWeightedDigraph, source:int) -> None:
        for e in g.edges():
            if e.weight < 0:
                raise Exception(f"edge {e} has negative weight")
        self.__dist_to = [inf] * g.V
        self.__edge_to = [None] * g.V
        self.__dist_to[source] = 0.0

        # relax vertices in order of distance from s
        self.__pq = MinIndexPQ(g.V)
        self.__pq.insert(source, self.__dist_to[source])
        while not self.__pq.is_empty():
            v = self.__pq.del_min()
            for e in g.adjacency_list[v]:
                self.__relax(e)

    # relax edge e and update pq if changed
    def __relax(self, e:Edge):
        v = e.v
        w = e.w
        if self.__dist_to[w] > self.__dist_to[v] + e.weight:
            self.__dist_to[w] = self.__dist_to[v] + e.weight
            self.__edge_to[w] = e
            if self.__pq.contains(w):
                self.__pq.decrease_key(w, self.__dist_to[w])
            else:
                self.__pq.insert(w, self.__dist_to[w])
    
    def distance_to(self, v:int): return self.__dist_to[v]

    def has_path_to(self, v:int)->bool: return self.__dist_to[v] < inf

    def path_to(self, v:int):
        if not self.has_path_to(v):
            return None
        path = Stack()
        e = self.__edge_to[v]
        while e:
            path.push(e)
            e = self.__edge_to[e.v]
        return path

# shortest path, faster than Dijkstra, but requires DAG. Negative weights are allowed.
class AcyclicSP:
    def __init__(self, g:EdgeWeightedDigraph, source:int) -> None:
        self.__dist_to = [inf] * g.V
        self.__edge_to = [None] * g.V
        self.__dist_to[source] = 0.0

        # visit vertices in toplogical order
        topological = Topological(g)
        if not topological.has_order():
            raise Exception("Digraph is not acyclic")
        
        for v in topological.order:
            for e in g.adjacency_list[v]:
                self.__relax(e)

    def distance_to(self, v:int): return self.__dist_to[v]

    def has_path_to(self, v:int): return self.__dist_to[v] < inf

    def path_to(self, v:int)->Stack:
        if not self.has_path_to(v):
            return None
        path = Stack()
        e = self.__edge_to[v]
        while e:
            path.push(e)
            e = self.__edge_to[e.v]
        return path

    def __relax(self, e:Edge):
        v = e.v
        w = e.w
        if self.__dist_to[w] > self.__dist_to[v] + e.weight:
            self.__dist_to[w] = self.__dist_to[v] + e.weight
            self.__edge_to[w] = e

# longest path, requires DAG. Negative weights are allowed.
class AcyclicLP:
    def __init__(self, g:EdgeWeightedDigraph, source:int) -> None:
        self.__dist_to = [-inf] * g.V
        self.__edge_to = [None] * g.V
        self.__dist_to[source] = 0.0

        # visit vertices in toplogical order
        topological = Topological(g)
        if not topological.has_order():
            raise Exception("Digraph is not acyclic")
        
        for v in topological.order:
            for e in g.adjacency_list[v]:
                self.__relax(e)

    def distance_to(self, v:int): return self.__dist_to[v]

    def has_path_to(self, v:int): return self.__dist_to[v] > -inf

    def path_to(self, v:int)->Stack:
        if not self.has_path_to(v):
            return None
        path = Stack()
        e = self.__edge_to[v]
        while e:
            path.push(e)
            e = self.__edge_to[e.v]
        return path

    # relax edge e, but update if you find a *longer* path
    def __relax(self, e:Edge):
        v = e.v
        w = e.w
        if self.__dist_to[w] < self.__dist_to[v] + e.weight:
            self.__dist_to[w] = self.__dist_to[v] + e.weight
            self.__edge_to[w] = e

# Bellman-Ford shortest path algorithm. Computes the shortest path tree in edge-weighted digraph G from vertex s, 
# or finds a negative cost cycle reachable from s
class BellmanFordSP:
    def __init__(self, g:EdgeWeightedDigraph, source:int) -> None:
        self.__dist_to = [inf] * g.V # dist_to[v] = distance  of shortest s->v path
        self.__edge_to = [None] * g.V # edge_to[v] = last edge on shortest s->v path
        self.__on_queue = [False] * g.V # on_queue[v] = is v currently on the queue?
        self.__cost = 0 # number of calls to relax()
        self.__negative_cycle = None # negative cycle (or None if no such cycle)
        self.__q = Queue()
        self.__dist_to[source] = 0.0

        # Bellman-Ford algorithm
        self.__q.enqueue(source)
        self.__on_queue[source] = True
        while not self.__q.is_empty() and not self.has_negative_cycle():
            v = self.__q.dequeue()
            self.__on_queue[v] = False
            self.__relax(g, v)

    def has_negative_cycle(self): return self.__negative_cycle is not None

    def negative_cycle(self):
        if not self.has_negative_cycle():
            return None
        return self.__negative_cycle.copy()

    def has_path_to(self, v): return self.__dist_to[v] < inf

    def path_to(self, v):
        if self.has_negative_cycle():
            raise Exception("Negative cost cycle exists")
        if not self.has_path_to(v):
            return None
        path = Stack
        e = self.__edge_to[v]
        while e:
            path.push(e)
            e = self.__edge_to[e.v]
        return path

    def distance_to(self, v)->float:
        if self.has_negative_cycle():
            raise Exception("Negative cost cycle exists")
        return self.__dist_to[v]

    # relax vertex v and put other endpoints on queue if changed
    def __relax(self, g:EdgeWeightedDigraph, v):
        for e in g.adjacency_list[v]:
            w = e.w
            if self.__dist_to[w] > self.__dist_to[v] + e.weight:
                self.__dist_to[w] = self.__dist_to[v] + e.weight
                self.__edge_to[w] = e
                if not self.__on_queue[w]:
                    self.__q.enqueue(w)
                    self.__on_queue[w] = True
            self.__cost += 1
            if self.__cost % g.V == 0:
                self.__find_negative_cycle()
    
    #  by finding a cycle in predecessor graph
    def __find_negative_cycle(self):
        spt = EdgeWeightedDigraph(len(self.__edge_to))
        for v in range(0,spt.V):
            if self.__edge_to[v] is not None:
                spt.add_edge(self.__edge_to[v])
        
        finder = EdgeWeightedDirectedCycle(spt)
        self.__negative_cycle = finder.cycle()

# all-pairs shortest paths problem in edge-weighted digraphs with no negative cycles
# time proportional to V^3 and space proportional to V^2.
class FloydWarshall:
    def __init__(self, g:AdjMatrixEdgeWeightedDigraph) -> None:
        self.V = g.V
        self.has_negative_cycle = False
        self.__dist_to = [[inf for i in range(g.V)] for j in range(g.V)]
        self.__edge_to = [[None for i in range(g.V)] for j in range(g.V)]

        for v in range(0,g.V):
            for e in g.adj(v):
                self.__dist_to[e.v][e.w] = e.weight
                self.__edge_to[e.v][e.w] = e
            
            # in case of self-loops
            if self.__dist_to[v][v] >= 0.0:
                self.__dist_to[v][v]= 0.0
                self.__edge_to[v][v] = None

        # Floyd-Warshall updates
        for i in range(0,g.V):
            # compute shortest paths using only 0, 1, ..., i as intermediate vertices
            for v in range(0,g.V):
                if self.__edge_to[v][i] is None:
                    continue # optimization
                for w in range(0,g.V):
                    if self.__dist_to[v][w] > self.__dist_to[v][i] + self.__dist_to[i][w]:
                        self.__dist_to[v][w] = self.__dist_to[v][i] + self.__dist_to[i][w]
                        self.__edge_to[v][w] = self.__edge_to[i][w]
                
                # check for negative cycle
                if self.__dist_to[v][v] < 0.0:
                    self.has_negative_cycle = True

    def has_path(self, s, t)->bool: return self.__dist_to[s][t] < inf

    def distance(self, s, t): return self.__dist_to[s][t] if not self.has_negative_cycle else None

    def path(self, s, t):
        if self.has_negative_cycle:
            raise Exception("Negative cost cycle exists")
        if not self.has_path(s,t):
            return None
        path = Stack()
        e = self.__edge_to[s][t]
        while e:
            path.push(e)
            e = self.__edge_to[s][e.v]
        return path

    def negative_cycle(self):
        if not self.has_negative_cycle:
            return None
        
        for v in range(0, len(self.__dist_to)):
            # negative cycle in v's predecessor graph
            if self.__dist_to[v][v] < 0.0:
                V = len(self.__dist_to)
                spt = EdgeWeightedDigraph(V)
                for w in range(0,V):
                    if self.__edge_to[v][w] is not None:
                        spt.add_edge(self.__edge_to[v][w])
                finder = EdgeWeightedDirectedCycle(spt)
                return finder.cycle()

############# Max Flow / Min Cut ####################

class FlowEdge:
    def __init__(self, v, w, capacity:float, flow:float=0) -> None:
        if v < 0 or w < 0:
            raise Exception("Vertex name must be a nonnegative integer")
        if not capacity >= 0.0:
            raise Exception("Edge capacity must be nonnegaitve")
        if not flow <= capacity:
            raise Exception("Flow exceeds capacity")
        if not flow >= 0.0:
            raise Exception("Flow must be nonnnegative")

        self.v = v
        self.w = w
        self.capacity = capacity
        self.flow = flow

    def other(self, vertex):
        if vertex == self.v:
            return self.w
        elif vertex == self.w:
            return self.v
        else:
            raise Exception("Illegal endpoint")

    # Returns the residual capacity of the edge in the direction to the given vertex 
    # If v is the tail vertex, the residual capacity equals capacity() - flow()
    # If v is the head vertex, the residual capacity equals flow()
    def residual_capacity_to(self, vertex):
        if vertex == self.v:
            return self.flow # backward edge
        elif vertex == self.w:
            return self.capacity - self.flow # forward edge
        else:
            raise Exception("Illegal endpoint")

    def add_residual_flow_to(self, vertex, delta:float):
        if delta != delta: # check without using math.isnan()...
            raise Exception("Change in flow = NaN")

        if vertex == self.v:
            self.flow -= delta # backward edge
        elif vertex == self.w:
            self.flow += delta # forward edge
        else:
            raise Exception("Illegal endpoint")

        if not self.flow > 0.0:
            raise Exception("Flow is negative")

        if not self.flow <= self.capacity:
            raise Exception("Flow exceeds capacity")

# a capacitated network with vertices named 0 through V - 1
# each directed edge is of type FlowEdge and has a real-valued capacity and flow.
class FlowNetwork:
    def __init__(self, v) -> None:
        self.V = v
        self.E = 0
        self.adj_list = [[] for _ in range(v)] # edges incident on vertex v (adj_list[v] includes both edges pointing to and from v)

    def __str__(self) -> str:
        res = []
        res.append(str(self.V))
        res.append(str(self.E))
        for v in range(self.V):
            for e in self.adj_list[v]:
                res.append(str(e))
        return "\n".join(res)

    def add_edge(self, e:FlowEdge):
        if e.v >= self.V:
            raise Exception(f"vertex {e.v} is not between 0 and {self.V - 1}")
        if e.w >= self.V:
            raise Exception(f"vertex {e.w} is not between 0 and {self.V - 1}")
        self.adj_list[e.v].append(e)
        self.adj_list[e.w].append(e)
        self.E +=1
  
# Computing a maximum st-flow and minimum st-cut in a flow network using FF algorithm with shortest augmenting path heuristic
# If the capacities and initial flow values are all integers, then this implementation guarantees to compute an integer-valued maximum flow.
# If the capacities and floating-point numbers, then floating-point roundoff error can accumulate
class FordFulkerson:
    def __init__(self, g:FlowNetwork, s, t) -> None:

        if s<0 or s >= g.V:
            raise Exception("Source s is invalid")
        if t<0 or t >= g.V:
            raise Exception("Sink t is invalid")
        if s == t:
            raise Exception("Source equals sink")
        self.value = self.__excess(g, t)
        self.__marked = [False] * g.V #  marked[v] = true iff s->v path in residual graph
        self.__edge_to = [None] * g.V # edgeTo[v] = last edge on shortest residual s->v path
        if not self.__is_feasible(g, s, t):
            raise Exception("Initial flow is infeasible")
        
        # while there exists an augmenting path, use it
        while self.__has_augmenting_path(g, s, t):
            # compute bottleneck capacity
            bottle = inf
            v=t
            while v != s:
                tmp = self.__edge_to[v].residual_capacity_to(v)
                bottle = bottle if bottle <= tmp else tmp
                v = self.__edge_to[v].other(v)
            # augment flow
            v=t
            while v != s:
                self.__edge_to[v].add_residual_flow_to(v, bottle)
                v = self.__edge_to[v].other(v)
            self.value += bottle

    def edges(self):
        for e in self.__edge_to:
            yield e

    # is v in the s side of the min s-t cut?
    def in_cut(self, v)->bool:
        v = len(self.__marked)
        if v < 0 or v >= self.V:
            raise Exception(f"vertex {v} is not between 0 and {(self.V-1)}")
        return self.__marked[v]

    # is there an augmenting path? if so, upon termination edgeTo[] will contain a parent-link representation of such a path
    def __has_augmenting_path(self, g:FlowNetwork, s, t)->bool:
        self.__edge_to = [None] * g.V
        self.__marked = [False] * g.V

        #  breadth-first search
        q = Queue()
        q.enqueue(s)
        self.__marked[s] = True
        while not q.is_empty():
            v = q.dequeue()
            for e in g.adj_list[v]:
                w = e.other(v)
                if e.residual_capacity_to(w) > 0:
                    if not self.__marked[w]:
                        self.__edge_to[w] = e
                        self.__marked[w] = True
                        q.enqueue(w)
        return self.__marked[t] # is there an augmenting path?

    # return excess flow at vertex v
    def __excess(self, g:FlowNetwork, v):
        excess = 0.0
        for e in g.adj_list[v]:
            if v == e.v:
                excess -= e.flow
            else:
                excess += e.flow
        return excess


    def __is_feasible(self, g:FlowNetwork, s, t)->bool:
        EPS = 1e-11
        # check that capacity constraints are satisfied
        for v in range (g.V):
            for e in g.adj_list[v]:
                if e.flow < -EPS or e.flow > e.capacity + EPS:
                    return False # ArgumentException("Edge does not satisfy capacity constraints: " + e)

        # check that net flow into a vertex equals zero, except at source and sink
        if abs(self.value + self.__excess(g, s)) > EPS:
            return False # Exception("Excess at source = " + excess(G, s)), Exception("Max flow  = " + Value) 

        if abs(self.value - self.__excess(g, s)) > EPS:
            return False # Exception("Excess at sink = " + excess(G, s)), Exception("Max flow  = " + Value) 

        for v in range(g.V):
            if v == s or v == t:
                continue
            elif abs(self.__excess(g, v)) > EPS:
                return False # Exception("Net flow out of " + v + " doesn't equal zero")
        
        return True

    def check_optimality_conditions(self, g:FlowNetwork ,s, t)->bool:
        ok = True
        if not self.__is_feasible(g, s, t):
            ok = False
            # raise Exception("Flow is infeasible")
        
        elif not self.in_cut(s):
            ok = False
            # raise Exception("source {s} is not on source side of min cut")

        elif self.in_cut(t):
            ok = False
            # raise Exception("sink {t} is on source side of min cut")
        
        if not ok:
            return False

        mincut_val = 0.0
        for v in range(g.V):
            for e in g.adj_list[v]:
                if v == e.v and self.in_cut(e.v) and not self.in_cut(e.w):
                    mincut_val += e.capacity
        
        EPS = 1e-11

        if abs(mincut_val - self.value) > EPS:
            return False
            # raise Exception("Max flow value = {Value}, min cut value = {mincut_val}")

        return True




def main():
    seed(2)
    pass

if __name__ == "__main__":
    #sys.exit(main())
    main()

    
