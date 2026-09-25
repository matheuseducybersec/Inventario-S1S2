INVENTÁRIO DE ATIVOS DE TI E VULNERABILIDADES

Sistema em Python para gerenciamento de ativos de TI e das vulnerabilidades
associadas, simulando uma base de inventário de segurança utilizada por
equipes de Computação e Cibersegurança.

Trabalho avaliativo - 1ª Atividade Avaliativa (Sprints 1 e 2)
Disciplina: Cibersegurança
Instituição: Universidade Federal de Uberlândia (UFU)
Período: 2026/2


SOBRE O PROJETO

A aplicação permite realizar operações de CRUD (Create, Read, Update, Delete)
sobre ativos de TI, além de gerenciar as vulnerabilidades identificadas em
cada um deles. Toda a persistência é feita em um arquivo JSON, servindo como
base de dados simplificada.

O que é um ativo de TI?
Qualquer recurso computacional que precise ser acompanhado pela organização:
notebooks, servidores, roteadores, aplicações web, bancos de dados,
impressoras de rede, entre outros.

O que é uma vulnerabilidade?
Uma fragilidade ou problema que pode comprometer a segurança de um ativo:
falha de configuração, senha fraca, software desatualizado, exposição
indevida de serviço, etc.


COMO EXECUTAR

Pré-requisitos:
- Python 3.8 ou superior instalado
- Nenhuma biblioteca externa é necessária (usa apenas a biblioteca padrão)

Execução:
python trabalho.py

O programa abrirá um menu interativo no terminal com todas as operações
disponíveis.


FUNCIONALIDADES

O menu principal oferece as seguintes opções:

1 - Cadastrar ativo
    Cria um novo ativo com ID único, hostname, responsável, setor, tipo
    e descrição.

2 - Consultar ativo
    Busca ativos por ID ou por hostname (busca parcial).

3 - Atualizar ativo
    Altera os dados de um ativo existente (deixe em branco para manter).

4 - Deletar ativo
    Remove um ativo e todas as vulnerabilidades associadas a ele.

5 - Cadastrar vulnerabilidade
    Associa uma nova vulnerabilidade a um ativo existente.

6 - Visualizar vulnerabilidades
    Exibe todas as vulnerabilidades de um ativo.

0 - Sair
    Encerra o programa.


ESTRUTURA DO CÓDIGO

O arquivo trabalho.py está organizado em blocos bem definidos:

1. Enumeração de tipos de ativos
   A classe TipoAtivo é uma Enum com 6 categorias, cada uma contendo um
   código inteiro e uma descrição textual.

2. Persistência
   carregar() - lê o arquivo JSON e devolve um dicionário
   salvar() - grava o dicionário no arquivo JSON

3. Validação de entrada
   pedir_inteiro() - repete até o usuário digitar um número válido
   pedir_texto() - repete até o usuário digitar algo não vazio
   pedir_opcao() - repete até o usuário escolher uma opção válida da lista

4. Operações CRUD
   cadastrar(), consultar(), atualizar(), deletar()
   cadastrar_vulnerabilidade(), visualizar_vulnerabilidades()

5. Menu principal
   menu() - laço infinito com tratamento de exceções


DECISÕES TÉCNICAS

Por que usar dicionário (dict)?
A base de dados é um dicionário indexado por ID. Isso permite acesso direto
em tempo O(1) - busca por ID não precisa varrer a lista inteira.

Por que usar Enum para os tipos?
A Enum garante que só existam tipos válidos no sistema. Cada tipo carrega
dois dados acoplados: o código (para o usuário digitar) e a descrição (para
exibir). Isso evita strings soltas e erros de digitação.

Por que JSON para persistência?
JSON é um formato de texto que representa exatamente dicionários e listas do
Python. Salvar e carregar é natural, e o arquivo gerado é legível por humanos.

Por que as chaves do dicionário são strings?
Porque o formato JSON sempre devolve chaves como strings. Usar str(id) em
todos os acessos mantém a consistência entre memória e arquivo.

Por que funções pedir_* que repetem?
O requisito pede tratamento de erros. Em vez de encher cada função com
try/except, as três funções auxiliares centralizam a validação e garantem
que todo input é válido antes de prosseguir.


ESTRUTURA DE DADOS

Ativo (dicionário):
{
  "id": 1,
  "hostname": "PC-01",
  "responsavel": "João Silva",
  "setor": "Financeiro",
  "descricao": "Notebook do setor financeiro",
  "tipo_codigo": 1,
  "tipo_descricao": "Notebook",
  "vulnerabilidades": []
}

Vulnerabilidade (dicionário):
{
  "descricao": "Senha do usuário admin é fraca",
  "categoria": "Configuração",
  "severidade": "Alta",
  "status": "Aberta"
}


REQUISITOS ATENDIDOS

1  - Menu textual com tratamento de erros                  - OK
2  - Enumeração com 4 ou mais tipos de ativos              - OK
3  - Cadastro de ativos com persistência em arquivo        - OK
4  - Busca por ID ou hostname                              - OK
5  - Atualização de dados do ativo                         - OK
6  - Deleção de ativo e vulnerabilidades associadas        - OK
7  - Cadastro de vulnerabilidades                          - OK
8  - Visualização de vulnerabilidades                      - OK
9  - Uso de dicionário (hash map) para otimização          - OK
10 - Repositório com mais de 2 branches e merge            - OK


FLUXO DE TRABALHO COM GIT

O projeto foi desenvolvido usando três branches, com merges documentados
no histórico:

  main          (versão final, com os merges das features)
  feature-cadastro          (desenvolvimento do cadastro/consulta)
  feature-vulnerabilidades  (desenvolvimento das vulnerabilidades)

Para visualizar o histórico:
git log --oneline --graph --all

Ou acesse o gráfico visual em Insights -> Network no GitHub.


ARQUIVOS DO REPOSITÓRIO

trabalho.py  - Código-fonte principal da aplicação
.gitignore   - Arquivos ignorados pelo Git (banco de dados local)
README.md    - Este arquivo

Observação: o arquivo inventario.json (base de dados) é gerado
automaticamente em tempo de execução e não é versionado, conforme
definido no .gitignore.


AUTOR

Matheus Eduardo
Email: matheusedu@ufu.br
GitHub: github.com/matheuseducybersec


LICENÇA

Projeto acadêmico desenvolvido para fins educacionais na Universidade Federal de Uberlândia (UFU).
