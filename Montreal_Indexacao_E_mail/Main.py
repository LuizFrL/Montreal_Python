from paramiko import SSHClient
import paramiko
import Inf
from Montreal_Indexacao_E_mail.DAO.MailAudit.MailAuditDAO import MailAuditDAO
from Montreal_Indexacao_E_mail.Service.LerArquivoEmail import LerArquivoEmail
from Montreal_Indexacao_E_mail.DTO.IndexarArquivosBancoDTO import IndexarAqruivosBancoDTO
import time


class SSH(object):
    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=Inf.Montreal_SSH_host(), username=Inf.Montreal_SSH_user(), password=Inf.Montreal_SSH_password())


if __name__ == '__main__':
    ssh = SSH()
    sftp_client = ssh.ssh.open_sftp()

    stdin, stdout, stderr = ssh.ssh.exec_command("cd /var/spool/eadm/montrealturismo.tur.br/auditoria\n find ./.201908* -name '*webmail*'")
    arquivos1 = set(stdout.readlines())

    sftp_client.chdir('/var/spool/eadm/montrealturismo.tur.br/auditoria')

    banco = MailAuditDAO().select_mail_files()
    dados_banco = set(list(banco['arquivo']))
    ct = 0

    arquivos = arquivos1.difference(dados_banco)
    total = len(arquivos)
    print(len(arquivos1) - len(arquivos))

    tempo_total = 0

    inicio_geral = time.time()
    for index, arqui in enumerate(arquivos):
        inicio = time.time()
        arqui = arqui.replace('\n', '')
        a = sftp_client.open(arqui)

        mensagem = ''
        for l in a:
            mensagem += l
        assert not mensagem.find('chown -R auditoria.auditoria') != -1
        try:
            arquivo = LerArquivoEmail(mensagem, arqui.replace('./', ''))
            dto = IndexarAqruivosBancoDTO(arquivo)
            dto.inserir_dados_endereco_emails()
            dto.inserir_dados_mensagens()
            dto.inserir_dados_anexos()
            dto.inserir_dados_mensagem_anexos()
            dto.inserir_dados_mensagem_to()
            dto.conexao.commit()
        except Exception as er:
            print(mensagem)
            ct += 1

        tempo_total += (time.time() - inicio)
        media_tempo = tempo_total / (index + 1)
        print(f"""Arquivo: {arqui}
Total: {total}
Lidos: {index + 1}
Faltam: {total - (index + 1)}
...Inserido com Sucesso
Erro: {ct}
Tempo: {time.time() - inicio}
Tempo Estimado: {(media_tempo * (total - (index + 1))) / 60 / 60}h
Média de Tempo: {media_tempo}""")
        print()
    print('Tempo total:', time.time() - inicio_geral, 'Erros:', ct)
    sftp_client.close()
    ssh.ssh.close()
