from datetime import date, datetime
from Montreal_Robo_Zabbix.Zabbix.Relatorio import get_inf_zabbix
from Montreal_NotasFiscais.verificando_envio import ultimo_dia_mes
from Montreal_Robo_Zabbix.Scopi.Scopi import Scopi
import numpy as np


format = '%Y-%m-%d'
today = datetime(day=1, month=date.today().month, year=date.today().year)
inicio = today.strftime(format)
fim = ultimo_dia_mes().strftime(format)

df = get_inf_zabbix(inicio, fim)
dados = list(df.to_dict(orient='index').values())
scopi = Scopi()

portal_cliente = []

indicadores = scopi.get_indicadores()
dados_zabbix_id_scopi = [
    {'Name':'Atendimento 2.0 - Indisponível' , 'id': 519},
    {'Name':'Cadastro de Cliente - Indisponível' , 'id': 520},
    {'Name':'Callbox - Indisponível' , 'id': 521},
    {'Name':'CITSMART - Indisponível' , 'id': 522},
    {'Name':'Comercial - Indisponível' , 'id': 523},
    {'Name':'Confluence - Indisponível' , 'id': 524},
    {'Name':'Portal do Cliente - Indisponível' , 'id': 525},
    {'Name':'Portal Hoteleiro - Indisponível' , 'id': 528},
    {'Name':'SISREL - Indisponível' , 'id': 529},
    {'Name':'Sistemas Montreal - Indisponível' , 'id' :530},
    {'Name':'WBS' , 'id': 531},
    {'Name':'Atendimento 1.0 - indisponível' , 'id': 505},
    {'Name':'Portal do Cliente - WWW1 - Carrinho de compras' , 'id': 527},
    {'Name':'Portal do Cliente - WWW- Página Inicial' , 'id': 526}
                                        
]
nomes_servicos = [
        'Jira', '2Clix - Indisponível',
        'OCS - Indisponível', 'WBS HOMOL - Indisponível', 'SAC - ASCBRASIL - INDISPONÍVEL',
        'Encurtador de link - mtre.al - INDISPONÍVEL'
    ]


for item in dados_zabbix_id_scopi:
    for indicador in indicadores:
        if indicador['id'] == item['id']:
            ok = np.array(df[df.Name == item['Name']]['Ok'])[0]
            print(indicador['id'], item['Name'], ok.replace('.', ','))


