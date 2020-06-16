
# -*- coding: utf-8 -*-
import networkx as nx
import community
import matplotlib.pyplot as plt
from random import randint
import collections
import numpy as np
from operator import itemgetter

#aplicando louvain denovo nas P% maiores comunidades
def refazerLouvain(G,P,divisionOfLevel):
    #contando quantos itens tem cada comunidade
    quantComunidade = {}#quantos nodos tem uma comunidade
    for v in divisionOfLevel.keys():
        comAtual = divisionOfLevel[v]
        if(not(comAtual in quantComunidade)):
            quantComunidade[comAtual] = 0
        quantComunidade[comAtual] += 1
    
    #achando os P% maiores
    bigComunitys = sorted(quantComunidade.items(),key=lambda x: x[1],reverse=True )
    bigComunitys = bigComunitys[0:int(len(bigComunitys)* P)]
    bigComunitys = [ x[0] for x in bigComunitys]

    #construindo grafo só com essas comunidades maiores
    toPut = []
    for i in G.nodes :
        for j in bigComunitys:
            if(divisionOfLevel[i] == j):
                toPut.append(i)
    H = G.subgraph(toPut)


    partition = community.best_partition(H,weight='weight')
    return (H,partition)


def updateDict(divisionOfLevel,partition):
    #colocando as novas comunidades no grafo original
    comunidadeMax = max(divisionOfLevel.values())

    for i in partition:
        divisionOfLevel[i] = partition[i] + comunidadeMax
    return divisionOfLevel
    


grafo = nx.read_gml(f"grafo.gml")

#aplicando louvain
louvain = community.best_partition(grafo,weight='weight')

#reaplicando louvain
# (newGraph,newPartition) = refazerLouvain(grafo,1/4,louvain)
louvain = updateDict(louvain,louvain)

#colocando informacao no csv
infoNodos = []
for nodo in louvain.keys():
    #insumo, comunidade do insumo, grau de arestas
    infoNodos.append( (nodo,louvain[nodo],len(grafo.edges(nodo)) ) )
infoNodos = sorted(infoNodos,key=itemgetter( 1))
with open(f'infoComunidadeLevel.csv', 'w') as f:
    f.write("insumo,comunidade,grauEdges\n" )
    for nodo in infoNodos:
        f.write("%s,"  %( nodo[0] ))
        f.write("%s,"  %( nodo[1] ))
        f.write("%s\n" %( nodo[2] ))