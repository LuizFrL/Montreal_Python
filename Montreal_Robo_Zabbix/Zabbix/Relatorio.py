import Inf
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


ano_mes_dia_de = '2020-02-01'
ano_mes_dia_ate = '2020-02-29'
url = f'http://172.31.68.39/zabbix/index.php?request=report2.php%3Fmode%3D0%26from%3D{ano_mes_dia_de}%2B00%253A00%253A00%26to%3D{ano_mes_dia_ate}%2B23%253A59%253A59%26filter_groupid%3D4%26filter_hostid%3D10084%26filter_set%3D1'

driver = webdriver.Chrome()

driver.get(url)
driver.find_element_by_xpath('//input[@id="name"]').send_keys(Inf.Montreal_Robo_Zabbix_user())
driver.find_element_by_xpath('//input[@id="password"]').send_keys(Inf.Montreal_Robo_Zabbix_password())
driver.find_element_by_xpath('//button[@id="enter"]').click()

driver.find_element_by_xpath('//a[@href="report2.php?page=1"]').click()
tabela = driver.find_element_by_xpath('//table[@class="list-table"]')
table1 = BeautifulSoup(tabela.get_attribute('outerHTML'), 'html.parser').find(name='table')

driver.find_element_by_xpath('//a[@href="report2.php?page=2"]').click()
tabela = driver.find_element_by_xpath('//table[@class="list-table"]')
table2 = BeautifulSoup(tabela.get_attribute('outerHTML'), 'html.parser').find(name='table')

driver.quit()

df_full = pd.concat([pd.read_html(str(table1))[0], pd.read_html(str(table2))[0]], ignore_index=True)
df_full['Ok'] = df_full['Ok'].str.replace('%', '')
df_full['Problems'] = df_full['Problems'].str.replace('%', '')
df_full.drop('Graph', inplace=True, axis=1)
df_full.drop('Host', inplace=True, axis=1)

nomes_servicos = [
    'Atendimento 1.0 - indisponível', 'Atendimento 2.0 - Indisponível', 'Cadastro de Cliente - Indisponível',
    'Callbox - Indisponível', 'CITSMART - Indisponível', 'Comercial - Indisponível', 'Jira', '2Clix - Indisponível',
    'OCS - Indisponível', 'Portal do Cliente - Indisponível', 'Portal do Cliente - WWW- Página Inicial',
    'Portal do Cliente - WWW1 - Carrinho de compras', 'Portal Hoteleiro - Indisponível', 'SISREL - Indisponível',
    'Sistemas Montreal - Indisponível', 'WBS', 'WBS HOMOL - Indisponível', 'SAC - ASCBRASIL - INDISPONÍVEL',
    'Encurtador de link - mtre.al - INDISPONÍVEL', 'Confluence - Indisponível'
]

df_util = df_full[df_full.Name.isin(nomes_servicos)]
