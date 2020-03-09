import json
import pandas as pd
from Banco.Conect import Conect


class HoteisBancoMontrealDAO(Conect):

    @staticmethod
    def return_json(dicionario):
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
        p.dt_ultima_alteracao,
        h.codHotel,
        h.codRedeHotel,
        h.webSite,
        h.beneficiarioTerceiro,
        h.caracteristicas,
        h.contratado,
        h.ativo
from    hotelaria.Parceiro as p
            inner join hotelaria.Hotel as h ON 
                h.codHotel = p.codParceiro
"""
        df = self._exec_query(query)
        return df


if __name__ == '__main__':
    a = HoteisBancoMontrealDAO()
    c = a.parceiros()
    print(c.to_json())
