from XML_Montreal import Uteis
import os, glob


class ArquivoDir(object):

    def __init__(self):
        self.configuracoes = Uteis.configuracoes()
        self.diretorio_arquivo_original = self.configuracoes["diretorios"]["diretorio_arquivos_originais"]
        self.diretorio_arquivo_resposta = self.configuracoes["diretorios"]["diretorio_arquivos_resposta"]
        self.arquivos_originais = self.__arquivos_originais()

    def __arquivos_originais(self):
        arquivos_xml = []
        for file in os.listdir(self.diretorio_arquivo_original):
            if file[-3:] == 'xml' and len(file) == len('lotenfce-18064052475784.xml'):
                arquivos_xml.append(file)
        return set(arquivos_xml)

    def arquivo_resposta(self, arquivo_original):
        return self.__arquivo_resposta_recente(arquivo_original)

    def __arquivo_resposta_recente(self, arquivo):
        arquivo_glob = os.path.basename(arquivo).replace("lotenfce-", '*').replace(".xml", '*')
        arquivos = glob.glob(self.diretorio_arquivo_resposta + r'\{}'.format(arquivo_glob))
        if arquivos:
            valores = {}
            for diretorio in arquivos:
                valores[os.stat(diretorio).st_mtime] = diretorio
            lista_maior = []
            for key in valores.keys():
                lista_maior.append(key)
            item_mais_recente = sorted(lista_maior, reverse=True)[0]
            return valores[item_mais_recente]
        return ''
