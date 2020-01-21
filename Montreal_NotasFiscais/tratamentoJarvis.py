import os
from unidecode import unidecode
import xml.etree.ElementTree as et
from datetime import date
from time import sleep
import requests
import json
import xml.etree.ElementTree


def solucoes_temporarias(string):
    #texto = "Documento emitido para fins de regularizacao da prestacao de servico de intermediacao relativa ao " \
    #        "periodo de apuracao 12/2019, nos termos da Instrucao Normativa SUREC n. 07, de 25 de setembro de 2009"
    #string = string.replace('<infAdic>', f'<infAdic><infCpl>{texto}</infCpl>', 1)
    #string = string.replace('</obsCont>', '</obsCont><obsCont xCampo="IN072009"><xTexto>12/2019</xTexto></obsCont>', 1)
    #print('--Alterações Feitas--')
    return string


def retornar_diretorios():
    if os.path.exists(r'C:\Users\m1015\Desktop\Notas'):
        os.chdir(r'C:\Users\m1015\Desktop\Notas')
    with open('config.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def erroNotwellformed(palavra):
    return palavra.replace("&", 'e')


def alterar_enderec_MONTREAL(string):

    MONTREAL_ENDERECO = """
<enderEmit>
<xLgr>SMAS AREA 6580 TORRE SUL, 1 E 3 ANDARES</xLgr>
<nro>sn</nro>
<xCpl>PARKSHOPPING CORPORATE</xCpl>
<xBairro>Zona Industrial (Guara)</xBairro>
<cMun>5300108</cMun>
<xMun>Brasilia</xMun>
<UF>DF</UF>
<CEP>70306901</CEP>
<cPais>1058</cPais>
<xPais>BRASIL</xPais>
<fone>6121054090</fone>
</enderEmit>
""".replace('\n', '')
    old_adres = """
<enderEmit>
<xLgr>SCS Qd 06, Bloco A</xLgr>
<nro>130</nro>
<xCpl>Edificio Ermes</xCpl>
<xBairro>Asa Sul</xBairro>
<cMun>5300108</cMun>
<xMun>Brasilia</xMun>
<UF>DF</UF>
<CEP>70306901</CEP>
<cPais>1058</cPais>
<xPais>BRASIL</xPais>
<fone>6121054090</fone>
</enderEmit>
""".replace('\n', '')
    if string.find(old_adres) == -1 and string.find(MONTREAL_ENDERECO) == -1: exit()

    print('Endereço Trocado.')
    return string.replace(old_adres, MONTREAL_ENDERECO)


def erroValidacao(string):
    tree = et.ElementTree(et.fromstring(string))
    root = tree.getroot()
    soma = somaIss = somaPis = somaCof = 0
    for book in root:
        if book.tag == '{http://www.oobj.com.br/nfe}NFe':
            for child in book:
                for att in child:
                    if att.tag == '{http://www.oobj.com.br/nfe}det':
                        for at in att:
                            if at.tag == '{http://www.oobj.com.br/nfe}prod':
                                for valordet in at:
                                    if valordet.tag == '{http://www.oobj.com.br/nfe}vProd':
                                        # print(valordet.tag, ':', valordet.text)
                                        soma += float(valordet.text)
                                    if valordet.tag == '{http://www.oobj.com.br/nfe}xProd':
                                        valordet.text = 'Servico de Intermediacao de Hospedagem'
                            if at.tag == "{http://www.oobj.com.br/nfe}imposto":
                                for impostosTag in at:
                                    if impostosTag.tag == '{http://www.oobj.com.br/nfe}ISSQN':
                                        for valoresIss in impostosTag:
                                            if valoresIss.tag == '{http://www.oobj.com.br/nfe}vISSQN':
                                                somaIss += round(float(valoresIss.text), 2)
                                    if impostosTag.tag == '{http://www.oobj.com.br/nfe}PIS':
                                        for valoresPis in impostosTag:
                                            if valoresPis.tag == '{http://www.oobj.com.br/nfe}PISAliq':
                                                for valorPis in valoresPis:
                                                    if valorPis.tag == '{http://www.oobj.com.br/nfe}vPIS':
                                                        somaPis += round(float(valorPis.text), 2)
                                    if impostosTag.tag == '{http://www.oobj.com.br/nfe}COFINS':
                                        for valoresCofins in impostosTag:
                                            for tagCofins in valoresCofins:
                                                if tagCofins.tag == '{http://www.oobj.com.br/nfe}vCOFINS':
                                                    somaCof += round(float(tagCofins.text), 2)
                    if att.tag == '{http://www.oobj.com.br/nfe}total':
                        # print(att.tag, 'TAG ---')
                        if att.tag == '{http://www.oobj.com.br/nfe}total':
                            for at in att:
                                if at.tag == '{http://www.oobj.com.br/nfe}ICMSTot':
                                    for vNF in at:
                                        if vNF.tag == '{http://www.oobj.com.br/nfe}vNF':
                                            vNF.text = str(soma)
                                if at.tag == '{http://www.oobj.com.br/nfe}ISSQNtot':
                                    # print(at.tag, 'TAG ----')
                                    for a in at:
                                        # print(a.tag, 'TAG DCOMPET')
                                        if a.tag == '{http://www.oobj.com.br/nfe}dCompet':
                                            # print(a.tag, ':' ,a.text)
                                            a.text = str(date.today())
                                            for a in at:
                                                # print(a.tag, 'TAG DCOMPET')
                                                if a.tag == '{http://www.oobj.com.br/nfe}vServ':
                                                    a.text = str(soma)
                                                if a.tag == '{http://www.oobj.com.br/nfe}vBC':
                                                    a.text = str(soma)
                                                if a.tag == '{http://www.oobj.com.br/nfe}vISS':
                                                    # print(a.tag, ':', a.text)
                                                    a.text = str(somaIss)
                                                if a.tag == '{http://www.oobj.com.br/nfe}vPIS':
                                                    # print(a.tag, ':', a.text)
                                                    a.text = str(somaPis)
                                                if a.tag == '{http://www.oobj.com.br/nfe}vCOFINS':
                                                    # print(a.tag, ':', a.text)
                                                    a.text = str(somaCof)
                                            for infE in book:
                                                for pag in infE:
                                                    if pag.tag == '{http://www.oobj.com.br/nfe}pag':
                                                        for detPag in pag:
                                                            for vpag in detPag:
                                                                if vpag.tag == '{http://www.oobj.com.br/nfe}vPag':
                                                                    vpag.text = str(soma)

    xmlstr = et.tostring(root, encoding='utf-8').decode('utf-8').replace('ns0:', '').replace(':ns0', '').replace('\n',
                                                                                                                 '')
    return xmlstr.replace('–', '-')


def erroConteudoInvalido(string):
    '''
    Erro: 5215 - Rejeição: arquivo com conteúdo inválido: Esperava {"http://www.portalfiscal.inf.br/nfe":impostoDevol,
    "http://www.portalfiscal.inf.br/nfe":infAdProd} mas foi encontrado 'prod'
    :param string:
    :return: Retorna a uma string com o erro tratado
    '''
    # Contador para definir a quantidade de itens na tag DET
    contador = 1
    while True:

        contador += 1

        # Substituindo valores
        auxiliar = string.replace('</imposto><prod>', f'</imposto></det><det nItem="{contador}"><prod>', 1)

        # Atribuindo a nova strig sem a tag para continuar gerando os itens
        string = auxiliar
        # Interromper loop caso não exista algo para substituir
        if auxiliar.find('</imposto><prod>') == -1:
            break

    return string


def erroxMun(string):
    import pyodbc

    driver_name = ''
    driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
    if driver_names:
        driver_name = driver_names[0]
    if driver_name:
        # Conexão com o banco de dados
        driver = driver_name
        server = '172.31.0.6'
        database = 'DNE'
        usuario = 'nfe'
        pasword = 'nfe2019'
        conexao = pyodbc.connect(f'DRIVER={driver};'
                                 f'SERVER={server};'
                                 f'DATABASE={database};'
                                 f'UID={usuario};'
                                 f'PWD={pasword}')
        # Cursor
        cursor = conexao.cursor()
    else:
        print('Sem Drivers SQL.')
        return string

    if string.find('</xBairro><xMun>') != -1:
        cepLocal = string.replace('</CEP>', '</.CEP>', 1).find('</CEP>')

        cep = string[cepLocal - 9: cepLocal - 1]

        linhas = cursor.execute(f"""
        select	*
        from	dbo.v_Cep
        where	cep = '{cep}'

        """).fetchall()

        codIBGE = None
        if len(linhas) != 0:
            for linha in linhas:
                codIBGE = linha[8]
        if codIBGE is None:
            linhas = cursor.execute(f"""
                    select	top 1 *
        from	[dbo].[v_Cep]
        where	cep < {cep} AND rtrim(ltrim(cep))<>'' and cep is not null
        order by	cep desc
            """).fetchall()
            for linha in linhas:
                codIBGE = linha[8]

        if codIBGE is None:
            import requests
            resultado = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
            try:
                codIBGE = resultado["ibge"]
            except:
                codIBGE = None
        if codIBGE is None:
            print("Arquivo Inalterado por falta de dados, erro ainda persiste")
            alerta_arquivo.append('Imposivel coletar codigo cMun')
        else:
            string = string.replace('</xBairro><xMun>', f'</xBairro><cMun>{codIBGE}</cMun><xMun>')

    return string


def xml_tag(root):
    for k in root:
        if type(k) == xml.etree.ElementTree.Element:
            if len(str(k.text)) > 60:
                k.text = str(k.text)[0:60]
            xml_tag(k)
    return root


def erroCvc_maxLength(string_):
    tree = et.ElementTree(et.fromstring(string_))
    root = tree.getroot()
    a = xml_tag(root)
    return et.tostring(a, encoding='utf-8').decode('utf-8').replace('ns0:', '').replace(':ns0', '').replace('\n', '')


def criarModulo_Jarvis() -> 'Retorna a chave de acesso para o encerramento':
    # URL de Abertura/Fechamento do proceeso
    link_start = 'https://montreal-jarvis.web.app/api/v1/session-start'

    # Json Abertura
    abrir_processo = {
        "keyModulo": "-LnTa3ruL8ou18mJPLKR"
    }

    # Abre o Módulo
    resultado_abrir = requests.post(link_start,
                                    data=abrir_processo)
    resultado_open = resultado_abrir.json()
    print(resultado_open)
    key_acesso = resultado_open['data']['keySessao']
    return key_acesso


def encerrarModulo_Jarvis(key: 'Chave gerada ao criar o Módulo') -> 'Retorna resultado do encerramento do Móduto':
    # URL de Fechamento
    link_end = 'https://montreal-jarvis.web.app/api/v1/session-end'

    # Encerrax o Módulo
    fechar_processo = {
        "keyModulo": "-LnTa3ruL8ou18mJPLKR",
        "keySessao": key
    }

    resultado_fechar = requests.post(link_end,
                                     data=fechar_processo)
    resultado_close = resultado_fechar.json()

    print(resultado_close)
    return resultado_close


def encaminharResultados_Jarvis(erros: 'Lista de erros durante a execução',
                                alertas: 'Lista de Alertas durante a execução') -> 'Retorna o resultado do encaminhamento de erros do Módulo':
    url_encaminhamento = 'https://montreal-jarvis.web.app/api/v1/log'

    encaminha = json.dumps({
        "keyModulo": "-LnTa3ruL8ou18mJPLKR",
        "erros": erros,
        "alertas": alertas
    })
    resultado_encaminhamento = requests.post(url_encaminhamento,
                                             headers={'Content-Type': 'application/json'},
                                             data=encaminha)

    print(encaminha)
    return resultado_encaminhamento


print('v-1.0')
exit()
try:
    os.chdir(r'C:\Users\m1015\Desktop\Notas')
except:
    pass

key_acesso = criarModulo_Jarvis()

erro_arquivo = []

alerta_arquivo = []

diretorios = retornar_diretorios()
geradas = str(diretorios['diretorios']['diretorio_arquivos_geradas'])
try:
    if len(os.listdir(geradas)) == 0:
        print('Nenhum arquivo no diretório')
        final = encerrarModulo_Jarvis(key_acesso)
        sleep(5)
        exit()
except Exception as erro_:
    erro_arquivo.append(f'293l Erro: {str(json.loads(erro_))}')
    encaminharResultados_Jarvis(erro_arquivo, alerta_arquivo)
    final = encerrarModulo_Jarvis(key_acesso)

# Pegando nome dos arquivos Gerados pelo Power Builder
arquivos = os.listdir(geradas)

# Diretorio dos arquivos originais a serem salvos
diretorio_arquivos_originais = diretorios['diretorios']['diretorio_arquivos_originais']

# Definindo diretorio a enviar os arquivos da OOBJ.
diretorio_envioOOBJ = diretorios['diretorios']['diretorio_arquivos_envioOOBJ']

# Dicionario para guardar os arquivos com erro
dicionario_Erro = {}

marcador = 0
total = len(arquivos)

for arquiv in arquivos:

    marcador += 1
    if len(arquiv) != len('lotenfce-18048008461809.xml'):
        alerta_arquivo.append(f'Número de caracteres inválidos {arquiv}')
        continue

    # Lendo arquivo em modo de leitura
    # Caso não consiga, ele guarda o nome do arquivo e o erro, e imprime no final

    arquivo = open(f'{geradas}\\{arquiv}', 'r', encoding='UTF-8')

    print('\n', arquiv)

    # Seleciona as linhas do arquivo e retorna uma lista com cada linha
    linhas = arquivo.readlines()
    arquivo.close()
    string = ''
    # Tira a quebra de linha e concatena todas as linhas em uma unica string
    for linha in linhas:
        string += linha.replace('\n', '').strip()

    # Trocando acentos do arquivo
    string = unidecode(string)

    # Primeira tratativa, retirar o &
    string = erroNotwellformed(string)

    # Colocar novo endereço da Montreal
    string = alterar_enderec_MONTREAL(string)

    # Tratamento necessário para correção, arquivos de 2018 NÃO devem ser corrigidos
    string = erroValidacao(string)

    # Declaração do tratamento de erro, xMun
    string = erroxMun(string=string)

    # Declaração do tratamento de erro por tag com valor a cima de 60 chars.
    string = erroCvc_maxLength(string)

    # Gerencia situações específicas temporarias
    string = solucoes_temporarias(string)

    # Declaração do tratamento de erro, voltado a arquivo com mais de um item
    auxiliar = erroConteudoInvalido(string=string)

    # Adicionando a extensão 7 para o arquivo
    arquivo_enviar_OOBJ = open(f'{diretorio_envioOOBJ}\\{arquiv}', 'w')
    arquivo_enviar_OOBJ.write(auxiliar)
    arquivo_enviar_OOBJ.close()

    arquivo_original = open(f'{diretorio_arquivos_originais}\\{arquiv}', 'w')
    arquivo_original.write(auxiliar)
    arquivo_original.close()

    print(auxiliar)
    print(f"""Total Arquivos : {total}
Lidos: {marcador}
Faltam: {total - marcador}""")

    os.unlink(geradas + '\\' + arquiv)

result = encaminharResultados_Jarvis(erro_arquivo, alerta_arquivo)
final = encerrarModulo_Jarvis(key_acesso)
sleep(5)
