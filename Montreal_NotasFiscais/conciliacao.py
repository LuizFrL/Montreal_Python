import os, locale
from smtplib import SMTP
from datetime import datetime, date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import json, glob


def retorna_arquivo_recente(num, dir_resposta):

    arquivos_resposta = glob.glob(dir_resposta + '\\' + f'*{num}*')
    valores = [ ]

    diretorios = { }
    for arquivo_resposta in arquivos_resposta:
        time = int(os.stat(arquivo_resposta).st_ctime)
        valores.append(time)
        diretorios[time] = arquivo_resposta

    return diretorios[max(valores)] if len(valores) != 0 else False


def verifica_contingencia_erro(lista_strings):
    string = ''

    for item in lista_strings:
        string += item

    return string.find('<xMotivo>Autorizado o uso da NF-e</xMotivo>') == -1


def retornar_config():
    with open('config.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def ultimo_dia_mes():
    hoje = date.today()

    if hoje.month == 12:
        ultimo_dia = date(day=31, month=12, year=hoje.year)
    else:
        ultimo_dia = date(day=1, year=hoje.year, month=hoje.month + 1) - timedelta(days=1)
    return ultimo_dia


def enviar_email(informacoes_arquivo, pendencia):
    print("Enviando email.")
    email = 'gti@clubemontreal.com.br'
    senha = 'uM2&9D7K'
    servidor_email = SMTP('smtp.gmail.com:587')
    servidor_email.ehlo()
    servidor_email.starttls()
    servidor_email.login(email, senha)
    grupo = config['envio_email']['email']

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'[Monitoramento de envio de notas fiscais] Conciliação'
    msg['From'] = email
    msg['To'] = grupo

    layout = layout_envio(msg, informacoes_arquivo, pendencia)

    servidor_email.sendmail(email, grupo, layout.as_string().encode('utf-8'))

    msg_debug = MIMEMultipart('alternative')
    msg_debug['Subject'] = f'[Monitoramento de envio de notas fiscais] Conciliação DEBUG'
    msg_debug['From'] = email
    msg_debug['To'] = grupo

    servidor_email.sendmail(email, grupo, layout_debug(msg_debug, informacoes_arquivo).as_string().encode('utf-8'))

    print('Email enviado.')
    print(informacoes_arquivo)
    return informacoes_arquivo


def layout_debug(msg, arquivo):
    html = f"""<html>
                <head></head>
                <body>
                    <p>{arquivo}</p>
                </body>
                </html>
    """

    msg.attach(MIMEText(html, 'html'))

    return msg


def layout_envio(msg, informacoes_arquivo, pendencia):
    colunas = informacoes_arquivo.keys()

    string_tabela = ''
    locale.setlocale(locale.LC_ALL, locale='German')
    t_enviada = t_retornada = t_erro = t_contingencia = t_sem_retorno = 0
    q_enviada = q_retornada = q_erro = q_contingencia = q_sem_retorno = 0
    for coluna in colunas:

        q_enviada += informacoes_arquivo[coluna]['total_arquivos']
        q_retornada += informacoes_arquivo[coluna]['total_arquivos_resposta']
        q_erro += informacoes_arquivo[coluna]['erro']
        q_contingencia += informacoes_arquivo[coluna]['contingencia']
        q_sem_retorno += informacoes_arquivo[coluna]['total_arquivos_sem_retorno']

        t_enviada += informacoes_arquivo[coluna]['valor_total_enviadas']
        t_retornada += informacoes_arquivo[coluna]['valor_total_retornadas']
        t_erro += informacoes_arquivo[coluna]['valor_total_erro']
        t_contingencia += informacoes_arquivo[coluna]['valor_total_contingencia']
        t_sem_retorno += informacoes_arquivo[coluna]['valor_total_sem_retorno']



        string_tabela += f"""
                <tr>
                    <td> {coluna} </td>
                    <td style="color:green;">{informacoes_arquivo[coluna]['total_arquivos']}</td>
                    <td>R$ {locale.currency(informacoes_arquivo[coluna]['valor_total_enviadas'], grouping=True)}</td>

                    <td style="color:blue;">{informacoes_arquivo[coluna]['total_arquivos_resposta']}</td>
                    <td>R$ {locale.currency(informacoes_arquivo[coluna]['valor_total_retornadas'], grouping=True)}</td>

                    <td style="color:red;">{informacoes_arquivo[coluna]['erro']}</td>
                    <td>R$ {locale.currency(informacoes_arquivo[coluna]['valor_total_erro'], grouping=True)}</td>

                    <td style="color:purple;">{informacoes_arquivo[coluna]['contingencia']}</td>
                    <td>R$ {locale.currency(informacoes_arquivo[coluna]['valor_total_contingencia'], grouping=True)}</td>

                    <td style="color:DarkOrange;">{informacoes_arquivo[coluna]['total_arquivos_sem_retorno']}</td>
                    <td>R$ {locale.currency(informacoes_arquivo[coluna]['valor_total_sem_retorno'], grouping=True)}</td>
                </tr>
            """

    html = f"""<html>
       <head></head>
       <body>
          <FONT SIZE="4">
             <p>Sistema de monitoramento de envio de notas fiscais<br><br>
             <table border="2" style="text-align:center;width:1600px;">
                <tr>
                   <th></th>
                   <th> Enviada(s) </th>
                   <th> Total R$ (Enviadas) </th>
                   <th> Retornada(s) </th>
                   <th> Total R$ (Retornadas)</th>
                   <th> Erro(s) </th>
                   <th> Total R$ (Erros) </th>
                   <th> Contingência </th>
                   <th> Total R$ (Contingencia) </th>
                   <th> Aguardando retorno OOBJ </th>
                   <th> Total R$ (em análise na OBJ) </th>
                </tr>
                {string_tabela}
<tr>
    <td></td>
    <td> Enviada(s) </td>
    <td> Total R$ (Enviadas) </td>
    <td> Retornada(s) </td>
    <td> Total R$ (Retornadas)</td>
    <td> Erro(s) </td>
    <td> Total R$ (Erros) </td>
    <td> Contingência </td>
    <td> Total R$ (Contingencia) </td>
    <td> Aguardando retorno OOBJ </td>
    <td> Total R$ (em análise na OBJ) </td>
</tr>

<tr>
<td>Total</td>

<td style="color:green;"> {q_enviada} </td>
<td>R$ {locale.currency(t_enviada, grouping=True)} </td>

<td style="color:blue;"> {q_retornada} </td>
<td>R$ {locale.currency(t_retornada, grouping=True)} </td>

<td style="color:red;"> {q_erro} </td>
<td> R$ {locale.currency(t_erro, grouping=True)} </td>

<td style="color:purple;"> {q_contingencia} </td>
<td> R$ {locale.currency(t_contingencia, grouping=True)} </td>

<td style="color:DarkOrange;"> {q_sem_retorno} </td>
<td> R$ {locale.currency(t_sem_retorno, grouping=True)} </td>
</tr>

             </table>

             <br>
             Enviada(s): Notas geradas, tratadas e encaminhadas para a OOBJ que ainda se encontram pendentes.
             <br>
             Total R$ (Enviadas): Somatório dos valores das notas enviados para a OOBJ em pendência.
             <br>
             <br>
             Retornada(s): Notas que possuem uma resposta referente as notas enviadas para a SEFAZ.
             <br>
             Total R$ (Retornadas): Somatório dos valores das notas retornadas pela SEFAZ.
             <br>
             <br>
             Erro(s): Erro referente aos arquivos Retornados rejeitados pela SEFAZ.
             <br>
             Total R$ (Erros): Somatório dos valores das notas retornadas com erro pela SEFAZ.
             <br>
             <br>
             Contingência: Erro referente aos arquivos Retornados, onde a OOBJ não consegue se comunicar com a SEFAZ estadual para emitir o documento fiscal.
             <br>
             Total R$ (Contingencia): Somatório dos valores das notas retornadas em contingência pela SEFAZ.
             <br>
             <br>
             Aguardando retorno OOBJ: Notas que ainda estão em análise na OOBJ.
             <br>
             Total R$ (em análise na OBJ): Somatório dos valores das notas que ainda estão em análise na OOBJ.
             <br>
             <br>

             {f'<br>{str(pendencia)} Arquivo(s) pendente(s).<br><br>' if pendencia != 0 else ''}
             <b>GTI - MONITORAMENTO</b><br><br>
             </p>
          </FONT>
       </body>
    </html>"""
    msg.attach(MIMEText(html, 'html'))

    return msg


def retornar_arquivos():

    print("Iniciando Análise de arquivos...", end='')

    ultimo_arquivo_consolidacao = config['ultimo_arquivo_consolidacao']
    arquivos_ = {  }
    arquivos_originais = os.listdir(diretorio_originais)
    for index, arqu in enumerate(arquivos_originais):
        if arqu.find('.xml') != -1 and len(arqu) == len('lotenfce-18058647471708.xml'):
            timestamp_arquivo = int(os.stat(f'{diretorio_originais}\\{arqu}').st_ctime)
            data_arquivo = datetime.fromtimestamp(timestamp_arquivo)
            print('Faltam:', len(arquivos_originais) - index, 'Lidos:', index)

            if timestamp_arquivo >= ultimo_arquivo_consolidacao:
                numero = arqu.replace('lotenfce-', '').replace('.xml', '')
                arquivo_diretorio = retorna_arquivo_recente(numero, diretorio_resposta)
                if arquivo_diretorio:
                    ar_resposta = open(arquivo_diretorio, 'r', encoding='utf-8')
                    linhas = ar_resposta.readlines()
                    ar_resposta.close()
                    if not verifica_contingencia_erro(linhas):
                        continue

                format_data = data_arquivo.strftime('%d/%m/%Y')
                if format_data not in arquivos_.keys():
                    arquivos_[format_data] = {'arquivos': [], 'sem_retorno': []}
                arquivos_[format_data]['arquivos'].append(arqu)

    print("\nTerminando Análise.")
    return arquivos_


def retornar_string_arquivo(dir_):
    arquivo_res = open(dir_, 'r', encoding='utf-8')
    linhas = arquivo_res.readlines()
    arquivo_res.close()
    conteudo = ''

    for linha in linhas:
        conteudo += str(linha)
    return conteudo


def retornar_valor_tag(dire, tag):
    tag_end = tag.replace('<', '</')
    arquivo = open(dire, 'r', encoding='utf-8')
    linhas = arquivo.readlines()
    arquivo.close()
    string = ''
    for linha in linhas:
        string += str(linha)

    valores = [ ]
    while string.find(tag) != -1:

        valores.append(float(string[string.find(tag) + len(tag) : string.find(tag_end)]))
        string = string.replace(tag, '', 1).replace(tag_end, '', 1)

    return sum(valores)


def atualiza_json(informacoes_arquivo, config_):
    print('Iniciando atualização Arquivo Json')

    for item in informacoes_arquivo.keys():
        primeiro_dia_erro = item
        timestamp = datetime.strptime(primeiro_dia_erro, '%d/%m/%Y').timestamp()
        config_['ultimo_arquivo_consolidacao'] = timestamp

        with open('config.json', 'w', encoding='utf-8') as file:
            file.writelines(json.dumps(config_, indent=4, sort_keys=True))

        print('Json Atualizado', informacoes_arquivo.keys())
        break


print('Iniciando...')

if os.path.exists(r'C:\Users\m0864\Desktop\Notas Fiscais'):
    os.chdir(r'C:\Users\m0864\Desktop\Notas Fiscais')

config = retornar_config()

diretorio_originais = config["diretorios"]['diretorio_arquivos_originais']

diretorio_resposta = config["diretorios"]['diretorio_arquivos_resposta']

diretorio_pendentes = config["diretorios"]['diretorio_arquivos_geradas']

inicio = datetime.now()

analise_ = ''

arquivos_pendentes = len(os.listdir(diretorio_pendentes))

if date.today() == ultimo_dia_mes(): # Verificando se é o ultimo dia do mês
    analise_ = 'mensal'

arquivos_data = retornar_arquivos()
print("Iniciando verificação de erro...")

for data in arquivos_data.keys():
    quantidade_arquivos = quantidade_arquivos_resposta = arq_erro = em_contingencia = valor_total_erro = 0
    valor_total_contingencia = valor_total_enviadas = valor_total_retornadas = valor_total_sem_retorno = 0
    total_arquivos_sem_retorno = 0

    arquivos_com_erro = [ ]
    arquivos_em_contingencia = [ ]

    for arq in arquivos_data[data]['arquivos']:
        quantidade_arquivos += 1


        diretorio_arquivo_original = f'{diretorio_originais}\\{arq}'
        valor_total_enviadas += retornar_valor_tag(diretorio_arquivo_original, '<vProd>')
        arquivo_resposta = str(arq).replace('lotenfce-', '').replace('.xml', '')
        diretorio = retorna_arquivo_recente(arquivo_resposta, diretorio_resposta)

        if  diretorio:
            quantidade_arquivos_resposta += 1
            valor_total_retornadas += retornar_valor_tag(diretorio_arquivo_original, '<vProd>')
            arq_string = retornar_string_arquivo(diretorio)

            if arq_string.find('<xMotivo>Autorizado o uso da NF-e</xMotivo>') == -1 \
                    and arq_string.find('<xMotivo>Documento impresso em contingência.</xMotivo>') == -1\
                    and arq_string.find('<xMotivo>Substituição não permitida: Substituição não permitida</xMotivo>') == -1:
                arq_erro += 1
                valor_total_erro += retornar_valor_tag(diretorio_arquivo_original, '<vProd>')
                arquivos_com_erro.append(diretorio)

            if arq_string.find('<xMotivo>Documento impresso em contingência.</xMotivo>') != -1:
                em_contingencia += 1
                arquivos_em_contingencia.append(diretorio)
                if diretorio in arquivos_com_erro:
                    arquivos_com_erro.remove(diretorio)
                valor_total_contingencia += retornar_valor_tag(diretorio_arquivo_original, '<vProd>')
        else:
            arquivos_data[data]['sem_retorno'].append(diretorio)
            total_arquivos_sem_retorno += 1
            valor_total_sem_retorno += retornar_valor_tag(diretorio_arquivo_original, '<vProd>')

    arquivos_data[data]['erro'] = arq_erro
    arquivos_data[data]['contingencia'] = em_contingencia
    arquivos_data[data]['total_arquivos'] = quantidade_arquivos
    arquivos_data[data]['total_arquivos_resposta'] = quantidade_arquivos_resposta
    arquivos_data[data]['total_arquivos_sem_retorno'] = total_arquivos_sem_retorno

    arquivos_data[data]['arquivos_com_erro'] = arquivos_com_erro
    arquivos_data[data]['arquivos_em_contingencia'] = arquivos_em_contingencia

    arquivos_data[data]['valor_total_erro'] = valor_total_erro
    arquivos_data[data]['valor_total_contingencia'] = valor_total_contingencia
    arquivos_data[data]['valor_total_enviadas'] = valor_total_enviadas
    arquivos_data[data]['valor_total_retornadas'] = valor_total_retornadas
    arquivos_data[data]['valor_total_sem_retorno'] = valor_total_sem_retorno

print("Terminando verificação.")

atualiza_json(enviar_email(arquivos_data, arquivos_pendentes), config)

sleep(5)