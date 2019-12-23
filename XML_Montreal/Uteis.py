import json
import os
import xmltodict


def configuracoes():
    with open(r'{}\config.json'.format(os.path.dirname(os.path.realpath(__file__))), 'r', encoding='utf-8') as file:
        return json.load(file)

def json_arquivo(dir_aqrquivo):
    arquivo = open(dir_aqrquivo, 'r', encoding='utf-8')
    linhas = arquivo.readlines()
    arquivo.close()
    string = ''
    for linha in linhas:
        string += linha

    return json.loads(json.dumps(xmltodict.parse(string.replace('&', 'e'))))
