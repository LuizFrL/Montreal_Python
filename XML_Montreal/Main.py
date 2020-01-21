from XML_Montreal.Arquivos.Arquivos import ArquivoDir
from XML_Montreal.Banco.ArquivosBanco import ArquivosBanco
from XML_Montreal.Arquivos.AnaliseArquivo import AnaliseArquivoOriResp
import os


arquivoDir = ArquivoDir()

banco = ArquivosBanco()
arquivos_banco = banco.arquivos()
aa = []
for arquivo in arquivoDir.arquivos_originais:
    if os.path.basename(arquivo) not in arquivos_banco:
        aa.append(arquivo)

total = len(aa)
for n, arquivo in enumerate(aa):
    if os.path.basename(arquivo) in ['lotenfce-18013487439502.xml', 'lotenfce-18030655451740.xml']:
        continue
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

