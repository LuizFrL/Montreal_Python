# XML-Montreal
Analisa e adiciona ao Banco informações sobre as Notas Fiscais.

## Funcionamento.
    O arquivo de configuração serve para verificar em quais diretórios estão presentes os aquivos
    originais e os arquivos de resposta.
    
    Após identificar os diretorios, verifica quais arquivos já estão adicionados no banco.
    Idenfificando os arquivos fora da base de dados, lê o arquivo em XML e o formata como um 
    objeto Json, tanto o arquivo original como o de resposta, para coletar os dados necessários 
    para complementar o banco. 