from XML_Montreal.Arquivos.Arquivos import ArquivoDir
from XML_Montreal.Banco.ArquivosBanco import ArquivosBanco
from XML_Montreal.Arquivos.AnaliseArquivo import AnaliseArquivoOriResp
import os


def modfi_string(string, num):
    pos_innicial = string.find('<nNF>') + len('<nNF>')

    pos_final = string.find('</nNF>')
    string__ = string[0:pos_innicial]
    __string = string[pos_final::]

    string = string__ + f'{num}' + __string
    return string


arquivoDir = ArquivoDir()
banco = ArquivosBanco()

banco.remover_arquivos_erro()

arquivos_banco = banco.arquivos()
arquivos_ori = arquivoDir.arquivos_originais

aa = arquivos_ori.difference(arquivos_banco)

print(aa.__len__())

diretorio = arquivoDir.diretorio_arquivo_original

total = len(aa)

for n, arquivo in enumerate(aa):
    arquivo = os.path.join(diretorio, arquivo)
    resultado = ''
    correcao = AnaliseArquivoOriResp(arquivo)
    if correcao.arquivo_resposta != '':
        a = correcao.analise_arquivo()
        resultado = banco.adicionar_banco(a)
    else:
        resultado = 'Sem Retorno'
    print(f'''Arquivos: {total}
Lidos: {n + 1}
Faltam: {total - (n + 1)}
Situação: {resultado}
''')
