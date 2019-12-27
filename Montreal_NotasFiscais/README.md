# Montreal-NotasFiscais
## TratamentoJarvis
    Módulo responsável pelo tratamento de Notas geradas pelo Power Builder.
    Corrige os seguintes tipos de erros:
* **[Acentuação](https://www.oobj.com.br/bc/article/erros-e-rejei%C3%A7%C3%B5es-na-emiss%C3%A3o-de-nfe-e-nfce-mapeados-no-oobj-dfe-453.html):**
Usa a biblioteca [Unidecode](https://pypi.org/project/Unidecode/) para retirar todos os acentos do XML.

* **[Valores de pagamento diferente da soma dos produtos presentes na nota](https://www.oobj.com.br/bc/article/rejei%C3%A7%C3%A3o-605-total-do-vserv-difere-do-somat%C3%B3rio-do-vprod-dos-itens-sujeitos-ao-issqn-como-resolver-317.html):**
Usa a biblioteca [xml ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) navegando pelas, verificando os valores de cada produto com objetivo de saber exatamente o valor a ser cobrado, presente na função
erroValidacao(). 

* **[Ajuste dos valores de Impostos](https://www.oobj.com.br/bc/article/rejei%C3%A7%C3%A3o-605-total-do-vserv-difere-do-somat%C3%B3rio-do-vprod-dos-itens-sujeitos-ao-issqn-como-resolver-317.html):** Usa os mesmos recursos do item anterior
só que calculando os valores dos impostos, presente na função
erroValidacao(). 
* **[Data de emissão diferente da data atual](https://www.oobj.com.br/bc/article/rejei%C3%A7%C3%A3o-704-nfc-e-com-data-hora-de-emiss%C3%A3o-atrasada-como-resolver-124.html):**
No mesmo módulo dos 2 itens anteriores, na tag dCompet do arquivo, coloca a data atual, presente na função
erroValidacao(). 
* **[Ausência do Código IBGE ná Nf](https://www.oobj.com.br/bc/article/erros-e-rejei%C3%A7%C3%B5es-na-emiss%C3%A3o-de-nfe-e-nfce-mapeados-no-oobj-dfe-453.html):**
As vezes o Power Builder não coloca o campo cMun no arquivo XML, como solução, a função erroxMun(), busca na base de dados
as informações necessárias para preencher esse campo, caso não exista o Código IBGE no banco,
ele utiliza a API [viacep](http://viacep.com.br/ws/70306901/json/) como última tentativa de correção.
* **[Excesso de informação em uma tag](https://www.oobj.com.br/bc/article/erros-e-rejei%C3%A7%C3%B5es-na-emiss%C3%A3o-de-nfe-e-nfce-mapeados-no-oobj-dfe-453.html):**
Usa a função erroCvc_maxLength(), usando a recursividade para verificar todas as tags do arquivo,
caso as informações da tag tenham mais de 60 caracteres, ele realiza um fatiamento para as informações
terem um tamanho aceitável (Entre 2 - 60 caracteres).
* **[Conteúdo inválido](https://www.oobj.com.br/bc/article/erros-e-rejei%C3%A7%C3%B5es-na-emiss%C3%A3o-de-nfe-e-nfce-mapeados-no-oobj-dfe-453.html):**
Ao gerar uma nota com mais de um produto, o Power Builder não separa os itens corretamente, gerando um erro de formatação. A
função erroConteudoInvalido() identifica os pontos em que o Power Builder não separa, e cria as devidas tags reconhecidas pela OOBJ.  

É importante lembrar que a maioria dos erros retornados pela sefaz são por 
má formatação do arquivo XML no qual as rotinas de Acentuação, Ausência do código IBGE
ná Nf, Exesso de informação em uma tag e Conteúdo invalido corrigem. Todas essas
rotinas estão relacionadas com o Status 5215.
### Jarvis
    Existem 3 funções responsáveis por gerenciar o envio de dados para o Jarvis, 
    criarModulo_Jarvis() -> Cria um módulo do jarvis e retorna a chave de acesso para
    esse mesmo módulo.
    encaminharResultados_Jarvis() -> Encaminha os dados de alerta e erros para o módulo.
    encerrarModulo_Jarvis() -> Encerra o módulo Jarvis.
    Essas funções tratam de encaminhar durante a execução do tratamentoJarvis informações
    sobre as notas ficais corrigidas.
    
