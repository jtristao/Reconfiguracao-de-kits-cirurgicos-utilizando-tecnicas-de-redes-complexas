
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv
import re
from collections import defaultdict
import networkx as nx



#retorna o grafo, 
def criarGrafo(base):

    DicionarioCodAviso = { }#label -> cod avisos cirurgia com label

    grafo = nx.Graph()
    labels = base['LABEL'].unique()

    #adicionar nó e identificar cirurgias com o insumo
    for l in labels:
        baseWithLabel = base[base['LABEL'] == l]

        booleano = baseWithLabel['CD_AVISO_CIRURGIA'].unique()     
        DicionarioCodAviso[l] = set(booleano)


        # adicionando vértices
        grafo.add_node(l)
    
    print(grafo.nodes())
    print(len(grafo.nodes()))
    print(labels)

    #adicionando as arestas 
    for i in labels:
        for j in labels:

            #AND entre os sets dos cd_cirurgia_aviso de i e j
            AND = len(DicionarioCodAviso[i] & DicionarioCodAviso[j] )
            OR = len(DicionarioCodAviso[i] | DicionarioCodAviso[j])
            codAvisosIguais = 10*AND/OR

            grafo.add_edge(i,j,weight=codAvisosIguais)


    toRemove = []
    #retirando arrestas com valor 0
    for (u, v, d) in grafo.edges(data=True):

        if d['weight'] == 0.0:
            toRemove.append([u,v])

    for k in toRemove:
        grafo.remove_edge(k[0],k[1])

    return grafo

base = pd.read_csv("base_gasto_de_sala_v2.1.csv")
grafo = criarGrafo(base)
nx.write_gml(grafo,f"grafo.gml")


