# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv
import re




base = pd.read_csv('base_gasto_de_sala v2.csv')  

print(f"a base de dados tem {len(base)} linhas ")

#cria lista de booleano, retirando linhas com CD_CIRURGIA_AVISO nulo
booleano = base.CD_CIRURGIA_AVISO.notnull()
base = base [booleano]
print(f"a base de dados tem {len(base)} linhas ")


#filtrando a base de dados para apena cesariana feto multiplo
base = base[base["DS_CIRURGIA"]=="CESARIANA - FETO UNICO" ]

print(f"a base de dados com qt == 0 {len(base)} linhas ")
#removendo linhas com QT_MOVIMENTACAO igual a 0
base = base[base.QT_MOVIMENTACAO != 0] 
print(f"a base de dados com qt != 0 {len(base)} linhas ")



#criando coluna que junta insumos com mesmo DS_PRODUTO_MESTRE
newColuna = []
for index, row in base.iterrows():


    if( pd.notnull(row.DS_PRODUTO_MESTRE) ):
        newColuna.append(row.DS_PRODUTO_MESTRE)
    else:
        newColuna.append(row.DS_PRODUTO)

#como o formato salvo é csv, trocado o "," por "."
newColuna = list( map( lambda  x : x.replace(",",".") , newColuna) )
base['LABEL'] = newColuna



#passando dos "nicks de procedimentos" para seus códigos reais
cadastroCirurgia = pd.read_csv('cirurgias.csv')

booleano = cadastroCirurgia['Codigo Tabela AMB'].notnull()
cadastroCirurgia = cadastroCirurgia[booleano]

#criando dicionario dos nicks para códigos reais
cadastroCirurgia = dict(zip(cadastroCirurgia.CD_CIRURGIA ,cadastroCirurgia['Codigo Tabela AMB']))


#caso exista para o CD_CIRURGIA um item correspontende na tabela AMD, será sinalizado com um "0-"
#caso não exista nela, terá o valor da pŕopria CD_CIRURGIA com "1-"
funcao = lambda x: f"0-{cadastroCirurgia[x]}" if x in cadastroCirurgia else f"1-{x}"
base['AMB'] = base['CD_CIRURGIA'].map( funcao )

base.to_csv('base_gasto_de_sala_v2.1.csv')



