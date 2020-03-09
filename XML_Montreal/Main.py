from XML_Montreal.Arquivos.Arquivos import ArquivoDir
from XML_Montreal.Banco.ArquivosBanco import ArquivosBanco
from XML_Montreal.Arquivos.AnaliseArquivo import AnaliseArquivoOriResp
import os


arquivoDir = ArquivoDir()
banco = ArquivosBanco()

banco.remover_arquivos_erro()

arquivos_banco = banco.arquivos()
arquivos_ori = arquivoDir.arquivos_originais

aa = arquivos_ori.difference(arquivos_banco)

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


