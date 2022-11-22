from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from datetime import datetime
from os import listdir
from os.path import isfile, join
import os
import json
import re
import requests


#Parametros
path_protocolos="/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/downloads/netshoes/protocolos/"
path_download_protocolos = path_protocolos
now = datetime.now()
date = now.strftime('%d%m%Y')



# chromeOptions = webdriver.ChromeOptions()
# prefs = {"download.default_directory" : path_download_protocolos, "profile.default_content_setting_values.automatic_downloads": 1}
# chromeOptions.add_experimental_option("prefs",prefs)
# browser = webdriver.Chrome(options=chromeOptions, executable_path="/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/chromedriver")
# sleep(3)
# browser.get("https://marketplace.netshoes.com.br/#/sac/atendimentos-novo")


# ####LOGIN
# sleep(3)
# browser.refresh()
# sleep(8)
# print('login')
# login = browser.find_element('xpath','/html/body/div/div/div/div/div[2]/div/form/div[1]/div/input')
# login.send_keys("fribeiro@limaconsulting.com")
# sleep(3)
# password = browser.find_element(By.NAME, 'senha')
# password.send_keys("Lima@2022")
# sleep(3)
# submit = browser.find_element('xpath',"/html/body/div/div/div/div/div[2]/div/form/button/span[2]").click()
# print('login ok')
# sleep(3)

# browser.refresh()
# sleep(5)
# #Pesquisa por NIKE          
# search = browser.find_element('xpath','/html/body/div[2]/div/ng-include/nav/div/div[3]/yield[2]/div/ns-select-seller/div/div/input')
# search.click()
# print('buscar nike')
# sleep(5)
# search.send_keys("Nike")
# webdriver.ActionChains(browser).send_keys(Keys.RETURN).perform()


# #Filtros avançados
# print('pesquisando data')
# sleep(8)
# filtros_avancados = browser.find_element(By.ID, 'botaoFiltrosAvancados').click()
# sleep(3)
# data_abertura = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section.sac-protocols.ng-scope > div:nth-child(3) > div > form > div.col-md-6.no-p-h.v-mid > div > ng-include > div > div.dropdown-menu.col-md-12 > div > div > div.tab-pane.active > div > div:nth-child(1) > div > div > div.ui-select-match.ng-scope').click()
# sleep(3)
# ontem = browser.find_element(By.CSS_SELECTOR, '#ui-select-choices-row-0-0 > span').click()
# sleep(5)

# print('filtrando por status pendentes')
# filtro_protocolo = browser.find_element(By.ID, 'abaProtocolo').click()
# sleep(3)
# status = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section.sac-protocols.ng-scope > div:nth-child(3) > div > form > div.col-md-6.no-p-h.v-mid > div > ng-include > div > div.dropdown-menu.col-md-12 > div > div > div.tab-pane.active > div > div:nth-child(2) > div > div > ul > li > input').click()
# sleep(3)
# pendente = browser.find_element(By.ID, 'ui-select-choices-row-3-0').click()
# sleep(5)
# filtrar = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section.sac-protocols.ng-scope > div:nth-child(3) > div > form > div.col-md-6.no-p-r > div > div.col-md-3.no-p.text-right > button:nth-child(1)').click()
# sleep(15)

# #fazendo download
# print('fazendo download')
# download = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/section[1]/div[1]/div/div[3]/button[2]')
# download.click()
# sleep(5)


# #Ler arquivos baixados
# print('ler arquivos baixados')
# onlyfiles = [f for f in listdir(path_download_protocolos)]

# for ix in onlyfiles:
#     if ix.startswith(f'Protocolos_{data}'):
#         df_protocolo = pd.read_excel(path_download_protocolos+ix, engine="openpyxl", usecols="A:K")
# #        os.remove(path_download_protocolos+'\\'+ix)
#         df1 = df_protocolo
#         df1 = df1[df1['Status'] == 'PENDENTE']
#         df1 = df1[(df1['Motivo do Protocolo'] == 'Troca ') | (df1['Motivo do Protocolo'] == 'Devolução')]
#         df_protocolo = df1
#         count = df_protocolo.shape[0]
#         print(f'total registros: [{count}]')

# sleep(10)   


        
# lista_cpf = []
# lista_chat = []
# lista_prio = []  
# index = 0

# for prot in df_protocolo['Protocolo']:
#         browser.get(f"https://marketplace.netshoes.com.br/#/sac/atendimentos-novo/{prot}")
#         sleep(5)
#         try:
#             erro = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'By.CSS_SELECTOR, #top > div.main > div > div.main-content.ng-scope > section > div.ns-card.ns-card--nohover.ns-top-background-doc.m-b-20 > div.ns-order-info.row.p-l-20.p-r-20.m-t-20 > div.col-xs-5.col-sm-3.col-md-2 > div > p')))

#             prioridade = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section > div.ns-card.ns-card--nohover.ns-top-background-doc.m-b-20 > div.ns-order-info.row.p-l-20.p-r-20.m-t-20 > div.col-xs-5.col-sm-3.col-md-2 > div > p')
#             priori = prioridade.text.replace("Prioridade:", "")
#             lista_prio.append(priori)

#             sleep(1)
#             chat = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section > div.ns-card.no-p.overflow-no.ns-card--nohover.m-b-20 > div > div.ns-chat__body.ns-chat-js')
#             lista_chat.append(chat.text)

#             sleep(1)
#             cpf_crawler = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/section/div[3]/div[2]/div[1]/p[2]')
#             cpf = cpf_crawler.text.replace('CPF/CNPJ: ', '').replace('.', '').replace('-', '')
#             lista_cpf.append(cpf)

#             index += 1
#             print(f'{index} - protocolo: {prot}')
            
#         except:
#             print('Erro encontrado')
#             browser.refresh()
#             print('recarregar pagina')
            
#             sleep(5)
#             prioridade = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section > div.ns-card.ns-card--nohover.ns-top-background-doc.m-b-20 > div.ns-order-info.row.p-l-20.p-r-20.m-t-20 > div.col-xs-5.col-sm-3.col-md-2 > div > p')
#             priori = prioridade.text.replace("Prioridade:", "")
#             lista_prio.append(priori)
            
#             sleep(1)
#             chat = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section > div.ns-card.no-p.overflow-no.ns-card--nohover.m-b-20 > div > div.ns-chat__body.ns-chat-js')
#             lista_chat.append(chat.text)
           
#             sleep(1)
#             cpf_crawler = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/section/div[3]/div[2]/div[1]/p[2]')
#             cpf = cpf_crawler.text.replace('CPF/CNPJ: ', '').replace('.', '').replace('-', '')
#             lista_cpf.append(cpf)

#             index += 1
#             print(f'{index} - protocolo: {prot}')

#             sleep(2)

# #browser.quit()



# ##Criando colunas com dados extraidos
# df_protocolo['prioridade'] = lista_prio
# df_protocolo['chat'] = lista_chat
# df_protocolo['cpf_crawler'] = lista_cpf



# ##Retirando codigos SKU do chat netshoes
# cod_sku = []
# for i in df_protocolo['chat']:
#     a = re.findall(r'\w*\d*-\d{4}-\d{3}-\d{2}', i)
#     aa = set(a)
#     cod_sku.append(list(aa))

# df_protocolo['cod_sku'] = cod_sku


# ##Renomeando colunas
# df_protocolo.rename(columns={"Responsável": "responsavel",
#                            "Pedido": "pedido",
#                            "Protocolo": "protocolo",
#                            "Status": "status",
#                            "Abertura": "abertura",
#                            "Tipo Protocolo": "tipo_protocolo",
#                            "Motivo do Protocolo": "motivo_do_protocolo",
#                            "Cliente": "cliente",
#                            "CPF/CNPJ": "cpf_cnpj",
#                            "Última Atualização do Trâmite": "ultima_atualizacao_tramite",
#                            "Tempo em Aberto": "tempo_em_aberto"},
#                   inplace=True)

#print('Protocolos extraidos')
# df_protocolo.to_csv(f'./downloads/netshoes/protocolos_tratados/Protocolos_{data}.csv', index=False)




print('ler arquivos protocolos baixados')

onlyfiles = [f for f in listdir(path_download_protocolos)]
for ix in onlyfiles:
    if ix.startswith(f'Protocolos_{date}'):
        df_protocolo = pd.read_csv(path_protocolos+ix)
       ###os.remove(path_download_protocolos+'\\'+ix)




print(df_protocolo)




####################### Crawler Pedidos  ########################################
# print('Iniciando crawler pedidos')
# path_pedidos="/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/downloads/netshoes/pedidos/"
# path_download_pedidos = path_pedidos
# now = datetime.now()
# date = now.strftime('%d%m%Y')

# chromeOptions = webdriver.ChromeOptions()
# prefs = {"download.default_directory" : path_download_pedidos, "profile.default_content_setting_values.automatic_downloads": 1}
# chromeOptions.add_experimental_option("prefs",prefs)
# #chromeOptions.add_argument("start-maximized")
# browser = webdriver.Chrome(options=chromeOptions, executable_path="/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/chromedriver")
# browser.get("https://marketplace.netshoes.com.br/#/pedido/consulta")
# sleep(3)

# ####LOGIN
# sleep(3)
# browser.refresh()
# sleep(8)
# print('login')
# login = browser.find_element('xpath','/html/body/div/div/div/div/div[2]/div/form/div[1]/div/input')
# login.send_keys("fribeiro@limaconsulting.com")
# sleep(3)
# password = browser.find_element(By.NAME, 'senha')
# password.send_keys("Lima@2022")
# sleep(3)
# submit = browser.find_element('xpath',"/html/body/div/div/div/div/div[2]/div/form/button/span[2]").click()
# print('login ok')
# sleep(10)


# search = browser.find_element('xpath','/html/body/div[2]/div/ng-include/nav/div/div[3]/yield[2]/div/ns-select-seller/div/div/input')
# search.click()
# print('buscar nike')
# sleep(2)
# search.send_keys("Nike")
# webdriver.ActionChains(browser).send_keys(Keys.RETURN).perform()
# sleep(10)

# #Encontrando botão de exportar
# try:
#     exportar =  browser.find_element('xpath',"/html/body/div[2]/div/div[1]/section/div[2]/div[5]/button")
#     print('exportando')
# except Exception as e:
#     print(e)

# #Clica no botão exportar
# actions = ActionChains(browser)
# actions.move_to_element(exportar).click().perform()


# print('aguardando carregamento dos pedidos')
# sleep(600)
# sleep(120)

# #EXPORTAR
# print('acessando pagina de exportacao')
# browser.get("https://marketplace.netshoes.com.br/#/pedido/exportar")
# sleep(3)

# #BUSCAR NIKE
# print('pesquisando nike')
# search = browser.find_element(By.CLASS_NAME,'search-input')
# search.click()
# sleep(5)
# #search.send_keys("Nike")
# #time.sleep(5)
# webdriver.ActionChains(browser).send_keys(Keys.RETURN).perform()
# sleep(3)

# months_number_download = 1
# lista_items_download = browser.find_elements(By.TAG_NAME, "tr")
# # print(lista_items_download)

# for x in range(1,months_number_download +1):
#     try:
#         row = lista_items_download[x]
#         print(row.get_attribute("innerText"))
#         sleep(2)
#         tds = row.find_elements(By.TAG_NAME, "td")
#         botao_download = tds[3].find_elements(By.TAG_NAME, "button")
#         botao_download[0].click()
#         sleep(30)
#         print('download ok')
#     except Exception as e:
#         print(e)

# sleep(5)

# #browser.quit()


# print('Lendo arquivo de pedidos')
# onlyfiles = [f for f in listdir(path_download_pedidos)]
# for ix in onlyfiles:
#     if ix.startswith(f'PedidosVenda_{date}'):
#         df_pedido = pd.read_excel(path_download_pedidos+ix, engine="openpyxl")
# #       os.remove(path_download_pedidos+'\\'+ix)
#         print('leu')



# #Alterar nome das colunas
# print('Alterando nome das colunas')
# df_ped = df_pedido
# df_ped = df_ped.rename(columns={"Número Pedido":"pedido",
#                                   'CPF/CNPJ do Comprador':'cpf_cnpj',
#                                   'Nome do Comprador':'cliente',
#                                   'Data da Compra':'data_compra',
#                                   'Valor Total Pedido Lojista':'valor_total_pedido',
#                                   'Nome do Produto':'nome_produto',
#                                   'Valor sku':'valor_sku',
#                                   'Qtd sku':'qtd_sku',
#                                   'SKU MktPlace':'cod_sku_mktp',
#                                   'Código identificação do item':'codigo_item'
#                                  })

# df_ped = df_ped.loc[:, ['pedido', 
#                          'data_compra',
#                          'valor_total_pedido', 
#                          'nome_produto',
#                          'valor_sku',
#                          'qtd_sku',
#                          'cod_sku_mktp',  
#                          'codigo_item',
#                          'cliente', 
#                          'cpf_cnpj'
#                         ]]


