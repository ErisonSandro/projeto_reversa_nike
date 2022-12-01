# -*- coding: utf-8 -*-

from unittest import TestCase
from correios_lib.webservices import LogisticaReversa
from correios_lib.entities import Remetente, Destinatario, Coleta, \
     Objeto, Produto, ColetaSimultanea
from correios_lib.requests import RequestSolicitarPostagemReversa, \
     RequestAcompanharPedido, RequestAcompanharPedidoPorData, \
     RequestCancelarPedido, RequestSolicitarRange, \
     RequestCalcularDigitoVerificador, RequestSolicitarPostagemSimultanea
import datetime
from os import listdir
from os.path import isfile, join
from datetime import datetime
from time import sleep
import pandas as pd 
import json
import requests

path = "/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/downloads/netshoes/protocolos_tratados/"
agora = datetime.now()
data = agora.strftime('%d%m%Y')



df_correio = pd.read_csv('/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/downloads/netshoes/protocolos_tratados/dados_teste.csv')
df_correio['cep'] = df_correio['cep'].apply(str)


cliente=LogisticaReversa(
    env='PROD',
    id_correios='grupo.sbf',
    password='centauro2021',
    cert=True)



df_correio.info()
for i, row in df_correio[0:1].iterrows():
    print(row['cep'])
    request = RequestSolicitarPostagemReversa(
                codAdministrativo='13415611',
                codigo_servico='04677',
                cartao='0075199017',

                destinatario=Destinatario(
                    nome='Nike - JP LOGISTICA',
                    logradouro='Rodovia Fernão Dias',
                    numero='S/N',
                    complemento='Km 947.5 G40 Modulo B-NIVEL1',
                    bairro='Bairro dos Pires',
                    cidade='́Extrema',
                    uf='MG',
                    cep='37640950'
                ),   
                coletas_solicitadas=[
                    Coleta(
                        tipo='A',
                        valor_declarado=row['Valor sku'],
                        remetente=Remetente(
                            nome=row['cliente'],
                            logradouro=row['logradouro'],
                            numero=row['numero'],
                            bairro=row['bairro'],
                            cidade=row['cidade'],
                            uf=row['uf'],
                            cep=row['cep'],
                            ddd=row['telefone_ddd'],
                            telefone=row['telefone_numero'],
                            email=row['email'],
                            identificacao=row['cpf'],
                            ddd_celular=row['celular_ddd'],
                            celular=row['celular_numero']
                        ),

                        obj_col=[
                            Objeto(
                                item=row['Qtd sku'],
                                id=row['SKU MktPlace']

                            )
                        ]
                    )
                ]
            )

# # response = cliente.SolicitarPostagemReversa(request)
    print(request)


