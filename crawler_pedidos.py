
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from google.oauth2 import service_account
from google.cloud import storage 
from datetime import datetime, timedelta
from os import listdir
import os
import re
import pandas as pd 
import json
import http.client



################################################ protocolos #############################################
## Parametros protocolos
path_protocolos="/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/downloads/netshoes/protocolos/"
path_download_protocolos = path_protocolos
date = datetime.now().strftime('%d%m%Y')


#Crawler
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : path_download_protocolos, "profile.default_content_setting_values.automatic_downloads": 1}
chromeOptions.add_experimental_option("prefs",prefs)
#chromeOptions.add_argument("start-maximized")
browser = webdriver.Chrome(options=chromeOptions, executable_path="/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/chromedriver")
sleep(3)
browser.get("https://marketplace.netshoes.com.br/#/sac/atendimentos-novo")

####LOGIN
sleep(3)
print('CRAWLER PROTOCOLOS - login')
login = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div[2]/div/form/div[1]/div/input')))
sleep(1)
login.send_keys("fribeiro@limaconsulting.com")
sleep(1)
password = browser.find_element(By.NAME, 'senha')
sleep(1)
password.send_keys("Lima@2022")
sleep(2)
submit = browser.find_element('xpath',"/html/body/div/div/div/div/div[2]/div/form/button/span[2]")
sleep(1)
submit.click()
print('CRAWLER PROTOCOLOS - login ok')
sleep(5)

#Pesquisa por NIKE          
search = browser.find_element('xpath','/html/body/div[2]/div/ng-include/nav/div/div[3]/yield[2]/div/ns-select-seller/div/div/input')
search.click()
print('CRAWLER PROTOCOLOS - Pesquisar NIKE')
sleep(5)
search.send_keys("Nike")
webdriver.ActionChains(browser).send_keys(Keys.RETURN).perform()


#Filtros avançados
print('CRAWLER PROTOCOLOS - Filtrando data')
sleep(8)
filtros_avancados = browser.find_element(By.ID, 'botaoFiltrosAvancados').click()
sleep(3)
data_abertura = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section.sac-protocols.ng-scope > div:nth-child(3) > div > form > div.col-md-6.no-p-h.v-mid > div > ng-include > div > div.dropdown-menu.col-md-12 > div > div > div.tab-pane.active > div > div:nth-child(1) > div > div > div.ui-select-match.ng-scope').click()
sleep(3)
ontem = browser.find_element(By.CSS_SELECTOR, '#ui-select-choices-row-0-0 > span').click()
sleep(5)

print('CRAWLER PROTOCOLOS - Filtrando status')
filtro_protocolo = browser.find_element(By.ID, 'abaProtocolo').click()
sleep(3)
status = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section.sac-protocols.ng-scope > div:nth-child(3) > div > form > div.col-md-6.no-p-h.v-mid > div > ng-include > div > div.dropdown-menu.col-md-12 > div > div > div.tab-pane.active > div > div:nth-child(2) > div > div > ul > li > input').click()
sleep(3)
pendente = browser.find_element(By.ID, 'ui-select-choices-row-3-0').click()
sleep(5)
filtrar = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section.sac-protocols.ng-scope > div:nth-child(3) > div > form > div.col-md-6.no-p-r > div > div.col-md-3.no-p.text-right > button:nth-child(1)').click()
sleep(15)

#fazendo download
print('CRAWLER PROTOCOLOS - Fazendo download')
download = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/section[1]/div[1]/div/div[3]/button[2]')
sleep(1)
download.click()
sleep(10)


#Lendo arquivos baixados
print('CRAWLER PROTOCOLOS - Lendo arquivos baixados')
onlyfiles = [f for f in listdir(path_download_protocolos)]
for ix in onlyfiles:
    if ix.startswith(f'Protocolos_{date}'):
        df_protocolo = pd.read_excel(path_download_protocolos+ix, engine="openpyxl", usecols="A:K")
#       os.remove(path_download_protocolos+'\\'+ix)
        print('CRAWLER PROTOCOLOS - Filtrando df_protocolo')
        df1 = df_protocolo
        df1 = df1[df1['Status'] == 'PENDENTE']
        df1 = df1[(df1['Motivo do Protocolo'] == 'Troca ') | (df1['Motivo do Protocolo'] == 'Devolução')]
        df_protocolo = df1
        count = df_protocolo.shape[0]
        print(f'total registros: [{count}]')

sleep(5)   


print('CRAWLER PROTOCOLOS - Iniciando crawler chat')
lista_cpf = []
lista_chat = []
lista_prio = []  
index = 0
for prot in df_protocolo['Protocolo']:
        browser.get(f"https://marketplace.netshoes.com.br/#/sac/atendimentos-novo/{prot}")
        sleep(2)
        
        while True:
            try:
                prioridade=WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section > div.ns-card.ns-card--nohover.ns-top-background-doc.m-b-20 > div.ns-order-info.row.p-l-20.p-r-20.m-t-20 > div.col-xs-5.col-sm-3.col-md-2 > div > p')))
                if prioridade.text != '':  
                    priori = prioridade.text.replace("Prioridade:", "")
                    lista_prio.append(priori)
                    
                    chat = browser.find_element(By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section > div.ns-card.no-p.overflow-no.ns-card--nohover.m-b-20 > div > div.ns-chat__body.ns-chat-js')
                    lista_chat.append(chat.text)

                    cpf_crawler = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/section/div[3]/div[2]/div[1]/p[2]')
                    cpf = cpf_crawler.text.replace('CPF/CNPJ: ', '').replace('.', '').replace('-', '')
                    lista_cpf.append(cpf)
               
                    index += 1
                    print(f'{index} - protocolo: {prot} - {priori}')
                    sleep(1)
                    break                                 

                else:
                    print('Valores vazio - Recarregando pagina')
                    browser.refresh()
                    sleep(3)
                    
            except:
                print('Erro no try - Recarregando pagina')
                browser.refresh()
                sleep(5)

                ####LOGIN
                sleep(3)
                print('CRAWLER PROTOCOLOS - login')
                login = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div[2]/div/form/div[1]/div/input')))
                sleep(1)
                login.send_keys("fribeiro@limaconsulting.com")
                sleep(1)
                password = browser.find_element(By.NAME, 'senha')
                sleep(1)
                password.send_keys("Lima@2022")
                sleep(2)
                submit = browser.find_element('xpath',"/html/body/div/div/div/div/div[2]/div/form/button/span[2]")
                sleep(1)
                submit.click()
                print('CRAWLER PROTOCOLOS - login ok')
                sleep(5)

                browser.get(f"https://marketplace.netshoes.com.br/#/sac/atendimentos-novo/{prot}")
                sleep(5)
                prioridade=WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#top > div.main > div > div.main-content.ng-scope > section > div.ns-card.ns-card--nohover.ns-top-background-doc.m-b-20 > div.ns-order-info.row.p-l-20.p-r-20.m-t-20 > div.col-xs-5.col-sm-3.col-md-2 > div > p')))
                sleep(5)

                break


print('CRAWLER PROTOCOLOS - Finalizando crawler chat')
browser.quit()

##Criando colunas com dados extraidos
print('CRAWLER PROTOCOLOS - Criando coluna chat no DF')
df_protocolo['prioridade'] = lista_prio
df_protocolo['chat'] = lista_chat
df_protocolo['cpf_crawler'] = lista_cpf


##Retirando codigos SKU do chat netshoes
print('CRAWLER PROTOCOLOS - Criando coluna codigos SKU do chat')
cod_sku = []
for i in df_protocolo['chat']:
    a = re.findall(r'\w*\d*-\d{4}-\d{3}-\d{2}', i)
    aa = set(a)
    cod_sku.append(list(aa))

df_protocolo['cod_sku'] = cod_sku


##Renomeando colunas
df_protocolo.rename(columns={"Responsável": "responsavel",
                           "Pedido": "pedido",
                           "Protocolo": "protocolo",
                           "Status": "status",
                           "Abertura": "abertura",
                           "Tipo Protocolo": "tipo_protocolo",
                           "Motivo do Protocolo": "motivo_do_protocolo",
                           "Cliente": "cliente",
                           "CPF/CNPJ": "cpf_cnpj",
                           "Última Atualização do Trâmite": "ultima_atualizacao_tramite",
                           "Tempo em Aberto": "tempo_em_aberto"},
                  inplace=True)


print('CRAWLER PROTOCOLOS - FINALIZADO')


################################################ PEDIDOS ################################################

print('CRAWLER PEDIDOS - Iniciando crawler pedidos')
credentials = service_account.Credentials.from_service_account_file(
    'credential.json'
)

path_pedidos="/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/downloads/netshoes/pedidos/"
path_download_pedidos = path_pedidos
ontem = str(datetime.now() - timedelta(days=1))[0:10]
client = storage.Client(credentials=credentials)
bucket = client.get_bucket('bs_export_files_fisia')
blobs = bucket.list_blobs(prefix='netshoes/historico/', delimiter='/')

print('CRAWLER PEDIDOS - Lendo arquivo no bucket')
for blob in blobs:
    if blob.name.startswith(f'netshoes/historico/export-netshoes-{ontem}'):
        print(f'gs://{bucket.name}/{blob.name}')
        
        print('CRAWLER PEDIDOS - criando dataframe')
        df_pedido = pd.read_excel(f'gs://{bucket.name}/{blob.name}', engine="openpyxl", storage_options={"token": "credential.json"})


df_ped = df_pedido
print('CRAWLER PEDIDOS - Alterando nome das colunas')
df_ped = df_ped.rename(columns={"Número Pedido":"pedido",
                                  'CPF/CNPJ do Comprador':'cpf_cnpj',
                                  'Nome do Comprador':'nome_cliente',
                                  'Data da Compra':'data_compra',
                                  'Valor Total Pedido Lojista':'valor_total_pedido',
                                  'Nome do Produto':'nome_produto',
                                  'Valor sku':'valor_sku',
                                  'Qtd sku':'qtd_sku',
                                  'SKU MktPlace':'cod_sku_mktp',
                                 })


print('CRAWLER PEDIDOS - Selecionado somente colunas necessarias')
df_ped = df_ped.loc[:, ['pedido', 
                         'data_compra',
                         'valor_total_pedido', 
                         'nome_produto',
                         'valor_sku',
                         'qtd_sku',
                         'cod_sku_mktp',  
                         'nome_cliente', 
                         'cpf_cnpj'
                        ]]



### Unindo dataframes
print('CRAWLER PEDIDOS - Merge nos dataframes Pedido+Protocolo')
df = df_protocolo.merge(df_ped,  on=['pedido', 'cpf_cnpj'], how='inner')


#### Retirando itens que não esta em troca
dados_removidos = []
dados_filtrados = []
print('CRAWLER PEDIDOS - Filtrando SKUs')
df_fil = df.fillna('NULO')
for i, row in df_fil.iterrows():
    if row['cod_sku_mktp'] in row['cod_sku']:
        dados_filtrados.append(row)
        #print(i, row['cod_sku'], row['cod_sku_mktp'])
        
    elif row['cod_sku'] == []:
        row['cod_sku'] = row['cod_sku_mktp']
        dados_filtrados.append(row)
        #print(i, row['cod_sku'], row['cod_sku_mktp'])
        
    elif row['cod_sku_mktp'] == 'NULO':
        row['cod_sku_mktp'] = row['cod_sku']
        dados_filtrados.append(row)
        #print(i, row['cod_sku'], row['cod_sku_mktp'])
    
    else:
        row['cod_sku_mktp'] = row['cod_sku']
        dados_removidos.append(row)
       #print('Diferente  ', i, row['cod_sku'], row['cod_sku_mktp'])
    
print('CRAWLER PEDIDOS - Adicionando coluna cod_sku')    
df_completo = pd.DataFrame(dados_filtrados)



#### Adicionando zeros a esqueda nos cpf
print('CRAWLER PEDIDOS - Adicionando 0 a esquerda no cpf')
cpf = []
index = 0
total_df = df_completo['cpf_cnpj'].shape[0]
for c in df_completo['cpf_cnpj']:
    a = len(str(c))
    if a < 11:
        cpf.append(str(c).zfill(11))
    else:
        cpf.append(str(c))
    index += 1

print(f'total cpf: {total_df}')
df_completo['cpf_cnpj'] = cpf


## Remover duplicatas
print('CRAWLER PEDIDOS - Removendo duplicatas')
df_completo = df_completo.drop_duplicates(subset=['pedido', 'nome_produto', 'protocolo', 'cod_sku_mktp'])


### Remover dados de personalização de camisas
print('CRAWLER PEDIDOS - Removendo personalização de camisas')
df_remove = df_completo[(df_completo['nome_produto'] == 'Personalização de Número') | (df_completo['nome_produto'] == 'Personalização de Nome')]
df_final = df_completo.drop(df_remove.index)


print('CRAWLER PEDIDOS - Salvando dados crawlers')
df_completo.to_csv(f'./downloads/netshoes/protocolos_tratados/dados_crawlers_{date}.csv', index=False)



#################################################### API NIKE ##############################################


## Pegando Token para fazer a requisição na API NIKE
print('API NIKE - Iniciando API NIKE')
conn = http.client.HTTPSConnection("api.gruposbf.com.br")

payload = json.dumps({
  "username": "lima-prd",
  "password": "9v770zk5Vkuf"
})
print('API NIKE - Gerando token')
headers = {'Content-Type': 'application/json'}
conn.request("POST", f"/crm-fisia/api/token", payload, headers)
res = conn.getresponse()
tok = res.read()
print('API NIKE - Token Gerado')


#### Parametros
token = 'Bearer ' + f'{tok.decode("utf-8")[10:-2]}'
path = "/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/downloads/netshoes/protocolos_tratados/"
date = datetime.now().strftime('%d%m%Y')


#### Adicionando zeros a esqueda nos cpf
cpf_df = []
index = 0
total_df = df_final['cpf_cnpj'].shape[0]
for c in df_final['cpf_cnpj']:
    a = len(str(c))
    if a < 11:
        cpf_df.append(str(c).zfill(11))
    else:
        cpf_df.append(str(c))
    index += 1

print(f'API NIKE - total cpf: {total_df}')


##### Fazendo Requisição na API NIKE
print('API NIKE - Iniciando chamada na API')
dado_api = []
for i in cpf_df:
    conn = http.client.HTTPSConnection("api.gruposbf.com.br")
    payload = ''
    headers = {
      'Content-Type': 'application/json',
      'Authorization': token
    }
    
    conn.request("GET", f"/crm-fisia/api/clientes/cpf={i}", payload, headers)
    res = conn.getresponse()
    respon = res.read()
    
    t = json.loads(respon.decode("utf-8"))
    dado_api.append(t)
    
print('API NIKE - Fim das requisições')



#CRAINDO DATAFRAME COM OS DADOS DA API
print('API NIKE - Criando dataframes df_api')
dados = pd.Series(dado_api).to_frame(name='dados')
dados = dados.explode(column='dados', ignore_index=True)
df_api = pd.json_normalize(data=dados['dados'])


print('API NIKE - Filtrando colunas necessarias')
df_api = df_api.rename(columns={'endereco.local': 'local', 
                        'endereco.logradouro': 'logradouro',       
                        'endereco.numero': 'numero', 
                        'endereco.complemento': 'complemento', 
                        'endereco.bairro': 'bairro',
                        'endereco.referencia': 'referencia', 
                        'endereco.cep': 'cep',
                        'endereco.cidade': 'cidade',
                        'endereco.uf': 'uf',
                        'endereco.pais': 'pais', 
                        'endereco.telefone.ddd': 'telefone_ddd', 
                        'endereco.telefone.numero': 'telefone_numero',      
                        'endereco.celular.ddd': 'celular_ddd', 
                        'endereco.celular.numero': 'celular_numero',
                        'cpf':'cpf_cnpj'})


df_api = df_api.loc[:, ['id', 
                  'email',
                  'cpf_cnpj', 
                  'rg', 
                  'cnpj', 
                  'local', 
                  'logradouro',       
                  'numero', 
                  'complemento', 
                  'bairro',
                  'referencia', 
                  'cep',
                  'cidade',
                  'uf',
                  'pais', 
                  'telefone_ddd', 
                  'telefone_numero',      
                  'celular_ddd', 
                  'celular_numero']]

### Retirando valores nulos que vieram da API
print('API NIKE - removendo valores nulos')
df_api_fil = df_api[df_api['id'].notna()]

## Juntando informações PROTOCOLOS+PEDIDOS+API
print('API NIKE - Join Dataframe API NIKE + PEDIDO + PROTOCOLOS')
df_final = df_api_fil.merge(df_final,  on=['cpf_cnpj'], how='inner')

## Remover duplicatas
print('API NIKE - REMOVENDO VALORE NULOS DO DF FINAL')
df_final = df_final.drop_duplicates(subset=['pedido', 'nome_produto', 'protocolo', 'cod_sku_mktp'])


#Salvando dados não processados pela api 
cpf_api = []
cpf_comp = []
cpf_final = []

for i in df_api['cpf_cnpj']:
    cpf_api.append(i)
    
for a in cpf_df:
    cpf_comp.append(a)

index = 0
for i in cpf_comp:
    if not i in cpf_api:
        index += 1
        cpf_final.append(i)
     #   print(f'{index} - {i} not')


#Criando DF
df_nulos = df_completo[df_completo['cpf_cnpj'].isin(cpf_final)]

#Salvando dados não processados pela api para mandar por email
df_nulos.to_excel(f'/home/erison/Desktop/lima/nike/projeto_crawler_zendesk_correios/nao_processados/df_nao_processados_{date}.xlsx', index=False)





#Salvando DF FINAL
print('Salvando Dados DF_FINAL')
df_final.to_csv('../projeto_crawler_zendesk_correios/downloads/netshoes/protocolos_tratados/dados_tratados_{date}.csv', index=False, encoding='utf-8-sig') 




print('')
dados = df_api[df_api['id'].notna()].shape[0]
nulos = df_api[df_api['id'].isna()].shape[0]
print(f'Protocolos: {df_protocolo.shape[0]}')
print(f'Pedidos: {df_pedido.shape[0]}')
print(f'df: {df.shape[0]}')
print(f'df_completo: {df_completo.shape[0]}')
print(f'df_final: {df_final.shape[0]}')
print(f'Dados API: {dados} \nNulos: {nulos}')



