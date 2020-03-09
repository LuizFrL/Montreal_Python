import json
import os
import xmltodict


def modfi_string(string, num):
    pos_innicial = string.find('<nNF>') + len('<nNF>')

    pos_final = string.find('</nNF>')
    string__ = string[0:pos_innicial]
    __string = string[pos_final::]

    string = string__ + f'{num}' + __string
    return string


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


def retornar_inf_tag(dire, tag):
    tag_end = tag.replace('<', '</')
    arquivo = open(dire, 'r', encoding='utf-8')
    linhas = arquivo.readlines()
    arquivo.close()
    string = ''
    for linha in linhas:
        string += str(linha)

    valores = [ ]
    while string.find(tag) != -1:
        valores.append(string[string.find(tag) + len(tag) : string.find(tag_end)])
        string = string.replace(tag, '', 1).replace(tag_end, '', 1)

    return valores


def retornar_valor_tag(dire, tag):
    valores = retornar_inf_tag(dire, tag)
    valores_por_tag = 0
    for num in valores:
        valores_por_tag += float(num)

    return valores_por_tag
