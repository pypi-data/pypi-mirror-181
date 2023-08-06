from random import randint
import graphs
import pytest

@pytest.fixture
def graph1():
    g = graphs.Graph(9)
    g.add_edge(0,5)
    g.add_edge(0,8)
    g.add_edge(1,7)
    g.add_edge(2,5)
    g.add_edge(2,6)
    g.add_edge(3,7)
    g.add_edge(3,8)
    g.add_edge(4,8)
    return g

@pytest.fixture
def biconnected_graph():
    g = graphs.Graph(9)
    g.add_edge(1, 0)
    g.add_edge(0, 2)
    g.add_edge(2, 1)
    g.add_edge(0, 3)
    g.add_edge(3, 4)
    g.add_edge(2, 4)
    return g

@pytest.fixture
def not_biconnected_graph():
    g = graphs.Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    return g

@pytest.fixture
def digraph1():
    dg = graphs.Digraph(5)
    dg.add_edge(1,0)
    dg.add_edge(0,2)
    dg.add_edge(2,1)
    dg.add_edge(0,3)
    dg.add_edge(3,4)
    return dg

@pytest.fixture
def digraph_eulerian():
    dg = graphs.Digraph(6)
    dg.add_edge(0,1)
    dg.add_edge(1,5)
    dg.add_edge(5,4)
    dg.add_edge(5,3)
    dg.add_edge(3,2)
    dg.add_edge(2,4)
    dg.add_edge(4,5)
    dg.add_edge(4,0)
    return dg

@pytest.fixture
def edge_weighted_graph():
    ewg = graphs.EdgeWeightedGraph(7)
    ewg.add_edge(graphs.Edge(0,1,5))
    ewg.add_edge(graphs.Edge(0,2,1))
    ewg.add_edge(graphs.Edge(0,3,4))
    ewg.add_edge(graphs.Edge(1,3,8))
    ewg.add_edge(graphs.Edge(1,5,6))
    ewg.add_edge(graphs.Edge(2,3,3))
    ewg.add_edge(graphs.Edge(2,4,2))
    ewg.add_edge(graphs.Edge(3,5,8))
    ewg.add_edge(graphs.Edge(4,5,7))
    ewg.add_edge(graphs.Edge(4,6,9))
    return ewg

@pytest.fixture
def edge_weighted_digraph():
    g = graphs.EdgeWeightedDigraph(9)
    g.add_edge(graphs.Edge(0,1,4))
    g.add_edge(graphs.Edge(0,6,7))
    g.add_edge(graphs.Edge(1,2,9))
    g.add_edge(graphs.Edge(1,6,11))
    g.add_edge(graphs.Edge(1,7,20))

    g.add_edge(graphs.Edge(2,3,6))
    g.add_edge(graphs.Edge(2,4,2))

    g.add_edge(graphs.Edge(3,5,5))
    g.add_edge(graphs.Edge(3,4,10))

    g.add_edge(graphs.Edge(4,5,15))
    g.add_edge(graphs.Edge(4,7,1))
    g.add_edge(graphs.Edge(4,8,5))

    g.add_edge(graphs.Edge(5,8,12))

    g.add_edge(graphs.Edge(6,7,1))
    g.add_edge(graphs.Edge(7,8,3))

    return g

@pytest.fixture
def flow_network_1():
    g = graphs.FlowNetwork(4)
    g.add_edge(graphs.FlowEdge(0,1,1000,0))
    g.add_edge(graphs.FlowEdge(0,2,1000,0))
    g.add_edge(graphs.FlowEdge(1,2,1,0))
    g.add_edge(graphs.FlowEdge(1,3,1000,0))
    g.add_edge(graphs.FlowEdge(2,3,1000,0))
    return g


def test_symbol_graph():
    s = "MovieName1/Actor1/Actor2/Actor3\nMovieName2/Actor4/Actor5/Actor6\nMovieName3/Actor4/Actor2"
    sg = graphs.SymbolGraph(s, '/')
    assert sg.kevin_bacon_index("MovieName1","MovieName2") == 2


def test_DepthFirstOrder(digraph1):
    dfo = graphs.DepthFirstOrder(digraph1)
    assert dfo.check

def test_TarjanSCC(digraph1):
    cc = graphs.TarjanSCC(digraph1)
    assert not cc.are_strongly_connected(3,4)
    assert cc.are_strongly_connected(2,0)
    assert cc.are_strongly_connected(0,2)

def test_KosarajuSharirSCC(digraph1):
    cc = graphs.KosarajuSharirSCC(digraph1)
    assert not cc.are_strongly_connected(3,4)
    assert cc.are_strongly_connected(2,0)
    assert cc.are_strongly_connected(0,2)

def test_TransitiveClosure(digraph1):
    tc = graphs.TransitiveClosure(digraph1)
    assert tc.reachable(0,1)
    assert tc.reachable(2,4)
    assert not tc.reachable(3,0)

def test_kruskal_mst(edge_weighted_graph):
    mst = graphs.KruskalMST(edge_weighted_graph)
    assert mst.weight == 26
    es = mst.edges()
    count = 0
    while not es.is_empty():
        count +=1
        es.dequeue()
    assert count == 6

def test_lazy_prim(edge_weighted_graph):
    mst = graphs.LazyPrimMST(edge_weighted_graph)
    assert mst.weight == 26
    es = mst.edges()
    count = 0
    while not es.is_empty():
        count +=1
        es.dequeue()
    assert count == 6

def test_prim(edge_weighted_graph):
    mst = graphs.PrimMST(edge_weighted_graph)
    assert mst.weight() == 26
    es = mst.edges()
    assert len(es) == 6

def test_dijkstra_sp(edge_weighted_digraph):
    ewdg = edge_weighted_digraph
    sp = graphs.DijkstraSP(ewdg, 0)
    assert sp.has_path_to(5)
    assert sp.distance_to(5) == 24
    assert sp.distance_to(4) == 15

    ewg = graphs.EdgeWeightedGraph.from_edge_weighted_digraph(ewdg)
    sp = graphs.DijkstraSP(ewg, 0)
    assert sp.has_path_to(5)
    assert sp.distance_to(5) == 24
    assert sp.distance_to(4) == 15

def test_acyclic_sp(edge_weighted_digraph:graphs.EdgeWeightedDigraph):
    ewdg = edge_weighted_digraph
    sp = graphs.AcyclicSP(ewdg, 0)
    assert sp.has_path_to(5)
    assert sp.distance_to(5) == 24
    assert sp.distance_to(4) == 15
    assert sp.distance_to(8) == 11

    ewdg.adjacency_list[1][2].weight = -7
    sp = graphs.AcyclicSP(ewdg, 0)
    assert sp.has_path_to(5)
    assert sp.distance_to(5) == 24
    assert sp.distance_to(4) == 15
    assert sp.distance_to(8) == 0

def test_acyclic_lp(edge_weighted_digraph:graphs.EdgeWeightedDigraph):
    ewdg = edge_weighted_digraph
    sp = graphs.AcyclicLP(ewdg, 0)
    assert sp.has_path_to(5)
    assert sp.distance_to(5) == 44
    assert sp.distance_to(4) == 29
    assert sp.distance_to(8) == 44 + 12

    ewdg.adjacency_list[1][2].weight = -7
    sp = graphs.AcyclicLP(ewdg, 0)
    assert sp.has_path_to(5)
    assert sp.distance_to(5) == 44
    assert sp.distance_to(4) == 29
    assert sp.distance_to(8) == 44 + 12

def test_edge_weighted_directed_cycle():
    g = graphs.EdgeWeightedDigraph(5)
    g.add_edge(graphs.Edge(0,1,1))
    g.add_edge(graphs.Edge(1,2,2))
    g.add_edge(graphs.Edge(2,3,3))
    g.add_edge(graphs.Edge(3,4,4))
    
    cycle = graphs.EdgeWeightedDirectedCycle(g)
    assert not cycle.has_cycle()
    assert cycle.check()

    g.add_edge(graphs.Edge(4,0,5))
    cycle = graphs.EdgeWeightedDirectedCycle(g)
    assert cycle.has_cycle()
    assert cycle.check()

def test_directed_eulerian_cycle(digraph_eulerian):
    dg = digraph_eulerian
    ec = graphs.DirectedEulerianCycle(dg)
    assert ec.is_eulerian
    cycle = ec.eulerian_cycle()
    assert cycle is not None
    assert len(cycle) == dg.E + 1

def test_bipartate(graph1):
        g = graph1
        b = graphs.Bipartite(g)
        assert b.is_bipartate
        assert not b.odd_cycle()

def test_biconnected(biconnected_graph):
    g = biconnected_graph
    bc = graphs.Biconnected(g)
    assert bc.is_biconnected()
    assert not any(bc.articualtion)

def test_biconnected2(graph1):
    g = graph1
    bc = graphs.Biconnected(g)
    assert not bc.is_biconnected()
    assert any(bc.articualtion)

def test_biconnected3(not_biconnected_graph):
    g = not_biconnected_graph
    bc = graphs.Biconnected(g)
    assert not bc.is_biconnected()
    assert any(bc.articualtion)

def test_bridge(not_biconnected_graph):
    g = not_biconnected_graph
    b = graphs.Bridge(g)
    assert b.components() == 3
    assert "3-4" in b.bridges()
    assert "0-3" in b.bridges()

def test_bridge2(digraph1):
    g = digraph1
    b = graphs.Bridge(g)
    assert b.components() == 3
    assert "3-4" in b.bridges()
    assert "0-3" in b.bridges()

def test_bellman_ford_sp(edge_weighted_digraph):
    ewdg = edge_weighted_digraph
    sp = graphs.BellmanFordSP(ewdg, 0)
    assert sp.has_path_to(5)
    assert sp.distance_to(5) == 24
    assert sp.distance_to(4) == 15

def test_bellman_ford_sp_find_cycle(edge_weighted_digraph):
    ewdg = edge_weighted_digraph
    ewdg.add_edge(graphs.Edge(4,2,-20))
    sp = graphs.BellmanFordSP(ewdg, 0)
    assert sp.has_path_to(5)
    assert sp.has_negative_cycle()

def test_floyd_warshall(edge_weighted_digraph:graphs.EdgeWeightedDigraph):
    ewdg = edge_weighted_digraph
    g = graphs.AdjMatrixEdgeWeightedDigraph(ewdg.V)
    for e in ewdg.edges():
        g.add_edge(e)
    
    fw = graphs.FloydWarshall(g)

    assert fw.has_path(0,5)
    assert not fw.has_path(5,4)
    assert fw.distance(0,5) == 24
    assert fw.distance(0,4) == 15

def test_floyd_warshall_find_cycle(edge_weighted_digraph:graphs.EdgeWeightedDigraph):
    ewdg = edge_weighted_digraph
    ewdg.add_edge(graphs.Edge(4,2,-20))
    g = graphs.AdjMatrixEdgeWeightedDigraph(ewdg.V)
    for e in ewdg.edges():
        g.add_edge(e)
    
    fw = graphs.FloydWarshall(g)

    assert fw.has_path(0,5)
    assert fw.has_negative_cycle
    c = fw.negative_cycle()
    assert len(c) == 2
    assert c.pop().v == 2
    assert c.pop().w == 2

def test_ford_fulkerson(flow_network_1):
    g = flow_network_1
    ff = graphs.FordFulkerson(g, 0,3)
    assert ff.value == 2000
    

def main():
    
    pass
    

if __name__ == "__main__":
    #sys.exit(main())
    main()
    
