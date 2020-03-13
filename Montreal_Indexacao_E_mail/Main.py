import glob
from Montreal_Indexacao_E_mail.Service.LerArquivoEmail import LerArquivoEmail
from Montreal_Indexacao_E_mail.DTO.IndexarArquivosBancoDTO import IndexarAqruivosBancoDTO


# a = glob.glob(r'C:\Users\m1015\Documents\E-mail\**\**', recursive=True)
# print(a)
# exit()
# for di in glob.glob(r'C:\Users\m1015\Documents\E-mail\**\**', recursive=True):

di = r'C:\Users\m1015\Documents\1575226077.Vca01I1c2404M473105.webmail%3A2,'
e_m = LerArquivoEmail(di)
dto = IndexarAqruivosBancoDTO(e_m)

print(e_m.id_email)
print(e_m.id_mensagem)

dto.inserir_dados_endereco_emails()
dto.inserir_dados_mensagens()
dto.inserir_dados_anexos()
dto.inserir_dados_mensagem_anexos()
dto.inserir_dados_mensagem_to()

print('Adicionado com sucesso.')