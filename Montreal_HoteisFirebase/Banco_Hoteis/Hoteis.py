import pyodbc, json
import pandas as pd


class HoteisInfDAO(object):

    def __init__(self):
        self.driver = '{SQL Server Native Client 11.0}'
        self.server = 'cltsql01'
        self.database = 'montreal'
        self.conexao = pyodbc.connect(f'DRIVER={self.driver};'
                                      f'SERVER={self.server};'
                                      f'DATABASE={self.database};'
                                      f'Trusted_Connection=yes;')
        self.cursor = self.conexao.cursor()

    def return_json(self, dicionario):
        js_ = pd.DataFrame(dicionario).to_json()
        return json.dumps(js_)

    def parceiros(self):
        query = """
select  p.codParceiro,
        p.cnpj,
        p.nomeFantasia,
        p.razaoSocial,
        p.inscricaoEstadual,
        p.inscricaoMunicipal,
        p.isentoInscricaoEstadual,	
        p.isentoInscricaoMunicipal,
        -- p.codParcSankhya,
        p.dt_ultima_alteracao,
        h.codHotel,
        h.codRedeHotel,
        h.webSite,
        h.beneficiarioTerceiro,
        h.caracteristicas,
        h.contratado,
        h.ativo
       -- isnull(h.dt_ultima_alteracao, 0) as dt_alt
from    hotelaria.Parceiro as p
            inner join hotelaria.Hotel as h ON 
                h.codHotel = p.codParceiro
WHERE       codParceiro < 5
"""
        df = pd.read_sql(query, self.conexao)
        j = {}
        for k, v in df.to_dict(orient='index').items():
            j[v['codParceiro']] = v

        return j

    def enderecos_parceiros(self):
        query = """
select      codParceiro,
            logradouro,
            bairro,
            complemento,
            numero,
            codCidade, 
            cep,
            codigoIbge
FROM        hotelaria.ParceiroEnderecos      
WHERE       codParceiro < 5
        """
        df = pd.read_sql(query, self.conexao)

        parceiros_inf = self.parceiros()
        for values in df.to_dict('records'):
            parceiros_inf[values['codParceiro']]['Endereço'] = values
            print(parceiros_inf)

        return self.return_json(parceiros_inf)


if __name__ == '__main__':
    a = HoteisInfDAO()
    c = a.enderecos_parceiros()
    print(c)