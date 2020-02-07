from XML_Montreal.Arquivos.Arquivos import ArquivoDir
from XML_Montreal import Uteis
from datetime import datetime
from bs4 import BeautifulSoup as bs
import os, requests, func_timeout


class AnaliseArquivoOriResp(object):

    def __init__(self, arquivo):
        self.arquivo_original = arquivo
        self.arquivo_resposta = ArquivoDir().arquivo_resposta(arquivo)
        print(self.arquivoOriginal_analise(), end=' ')
        self.arquivo_original_json = Uteis.json_arquivo(self.arquivo_original)
        if self.arquivo_resposta != '':
            self.arquivo_resposta_json = Uteis.json_arquivo(self.arquivo_resposta)
        else:
            print('Arquivo sem retorno')
        self.valores_autorizacao_nf = self.__autorizacao_total()
        self.sefaz = self.__sefaz()

    def analise_arquivo(self):
        arquivo_inf_banco = {
                    'numero': self.numero_analise(),
                    'serie': self.serie_analise(),
                    'fatura': self.fatura_analise(),
                    'assCodigo': self.assCodigo_analise(),
                    'valorTotal': self.valorTotal_analise(),
                    'comErro': self.comErro_analise(self.arquivo_resposta_json['retConsReciNFe']['cStat']),
                    'status': self.status_analise(),
                    'motivo': self.motivo_analise(),
                    'dtInclusao': self.dtInclusao_analise(),
                    'arquivoOriginal': self.arquivoOriginal_analise(),
                    'arquivoRetorno': self.arquivoRetorno_analise(),
                    'dtRecebimento': self.dtRecebimento_analise(),
                    'dtCriacaoArquivo': self.dtCriacaoArquivo_analise(),
                    'autorizacao_total_dCompet': self.autorizacao_total_dCompet_analise(),
                    'autorizacao_cStat': self.autorizacao_cStat_analise(),
                    'autorizacao_motivo': self.autorizacao_motivo_analise(),
                    'autorizacao_total_vNF': self.valores_autorizacao_nf['vProd'],
                    'autorizacao_total_vISS': self.valores_autorizacao_nf['vISSQN'],
                    'autorizacao_total_vPIS': self.valores_autorizacao_nf['vPIS'],
                    'autorizacao_total_vCOFINS': self.valores_autorizacao_nf['vCOFINS'],
                    'obs': '',
                    'sefaz_qrcode': self.sefaz.get('link'),
                    'sefaz_vlTotal': 0 if self.sefaz.get('valor') is None else self.sefaz.get('valor'),
                    'sefaz_nome': self.sefaz.get('nome')
        }

        print(arquivo_inf_banco['dtCriacaoArquivo'])
        return arquivo_inf_banco

    def numero_analise(self):
        return self.arquivo_original_json['enviNFe']['NFe']['infNFe']['ide']['nNF']

    def serie_analise(self):
        return self.arquivo_original_json['enviNFe']['NFe']['infNFe']['ide']['serie']

    def fatura_analise(self):
        try:
            for item in self.arquivo_original_json['enviNFe']['NFe']['infNFe']['infAdic']['obsCont']:
                if 'CodigoFatura' in item.values():
                    return item['xTexto']
        except:
            print('Não encontrado Código Fatura')
            return 0

    def assCodigo_analise(self):
        try:
            for item in self.arquivo_original_json['enviNFe']['NFe']['infNFe']['infAdic']['obsCont']:
                if 'CodigoAssociado' in item.values():
                    return item['xTexto']
        except:
            print('Não possível encontrar o Código do Associado')
            return 0

    def valorTotal_analise(self):
        return self.arquivo_original_json['enviNFe']['NFe']['infNFe']['pag']['detPag']['vPag']

    def status_analise(self):
        return self.arquivo_resposta_json['retConsReciNFe']['cStat']

    def motivo_analise(self):
        return self.arquivo_resposta_json['retConsReciNFe']['xMotivo']

    def autorizacao_total_dCompet_analise(self):
        return self.arquivo_original_json['enviNFe']['NFe']['infNFe']['total']['ISSQNtot']['dCompet']

    def autorizacao_cStat_analise(self):
        try:
            autorizacao = self.arquivo_resposta_json['retConsReciNFe']['protNFe']['infProt']['cStat'] if \
            self.status_analise() != '5020' else self.status_analise()
        except KeyError:
            autorizacao = '0'

        return autorizacao

    def autorizacao_motivo_analise(self):
        try:

            motivo = self.arquivo_resposta_json['retConsReciNFe']['xMotivo'] if \
                self.arquivo_resposta_json['retConsReciNFe']['cStat'] == '5020' else \
                self.arquivo_resposta_json['retConsReciNFe']['protNFe']['infProt']['xMotivo']
        except KeyError:
            motivo = '0'
        return motivo

    def __autorizacao_total(self):
        det = self.arquivo_original_json['enviNFe']['NFe']['infNFe']['det']
        total_autorizacao = {
            'vProd': 0,
            'vPIS': 0,
            'vCOFINS': 0,
            'vISSQN': 0
        }

        if type(det) == list:
            for item in det:
                total_autorizacao['vProd'] += float(item['prod']['vProd'])
                total_autorizacao['vPIS'] += float(item['imposto']['PIS']['PISAliq']['vPIS'])
                total_autorizacao['vCOFINS'] += float(item['imposto']['COFINS']['COFINSAliq']['vCOFINS'])
                total_autorizacao['vISSQN'] += float(item['imposto']['ISSQN']['vISSQN'])
        elif type(det['prod']) == list:
            for index, item in enumerate(det['prod']):
                total_autorizacao['vProd'] += float(item['vProd'])
                total_autorizacao['vPIS'] += float(det['imposto'][index]['PIS']['PISAliq']['vPIS'])
                total_autorizacao['vCOFINS'] += float(det['imposto'][index]['COFINS']['COFINSAliq']['vCOFINS'])
                total_autorizacao['vISSQN'] += float(det['imposto'][index]['ISSQN']['vISSQN'])
        else:
            total_autorizacao['vProd'] = float(det['prod']['vProd'])
            total_autorizacao['vPIS'] = float(det['imposto']['PIS']['PISAliq']['vPIS'])
            total_autorizacao['vCOFINS'] = float(det['imposto']['COFINS']['COFINSAliq']['vCOFINS'])
            total_autorizacao['vISSQN'] = float(det['imposto']['ISSQN']['vISSQN'])

        return total_autorizacao

    def comErro_analise(self, status_motivo):
        lote_processado = ['104', '104']
        if status_motivo not in lote_processado:
            return 1
        return 0

    def dtInclusao_analise(self):
        return str(datetime.now().strftime('%Y/%m/%d %H:%M'))

    def arquivoOriginal_analise(self):
        return os.path.basename(self.arquivo_original)

    def arquivoRetorno_analise(self):
        return os.path.basename(self.arquivo_resposta)

    def dtRecebimento_analise(self):
        dados_arquivo_resp = os.stat(self.arquivo_resposta)
        return datetime.fromtimestamp(int(dados_arquivo_resp.st_ctime)).strftime('%Y/%m/%d %H:%M')

    def dtCriacaoArquivo_analise(self):
        dados_arquivo_ori = os.stat(self.arquivo_original)
        return datetime.fromtimestamp(int(dados_arquivo_ori.st_ctime)).strftime('%Y/%m/%d %H:%M')

    def __sefaz_qrcode_analise(self, link):
        if link.find('<![CDATA[') != -1:
            link = link.replace('<![CDATA[', '')[0:-2]
        return link

    def __valorCFAZ(self, url):
        retornarValores = {
                            'valor': 0,
                            'Nome': ''
                           }
        try:
            resultado = func_timeout.func_timeout(3, self.__request_url, (url, ))

            htmlPagina = resultado.content.decode('utf-8')

            pagina = bs(htmlPagina, 'html.parser')
            valor = pagina.find('span', {'style': 'font-weight: bold; font-size:10px;'}).text
            valor = int(str(valor).replace(',', '').replace('.', '')) / 100
            retornarValores['valor'] = valor
        except Exception as err:
            print('\nNão foi possível encontrar os valores pelo QRCode:', url)
        finally:
            return retornarValores

    def __request_url(self, url):
        return requests.get(url=url)

    def __sefaz(self):
        try:
            sefaz_valores = {'link': self.__sefaz_qrcode_analise(self.arquivo_resposta_json['retConsReciNFe']
                                                             ['protNFe']['infProt']['qrCode'])}

            sefaz = self.__valorCFAZ(sefaz_valores['link'])

            sefaz_valores['nome'] = sefaz['Nome']
            sefaz_valores['valor'] = sefaz['valor']
        except Exception:
            return {}

        return sefaz_valores
