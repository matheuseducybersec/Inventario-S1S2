"""
=============================================================
 INVENTÁRIO DE ATIVOS DE TI E VULNERABILIDADES
 Trabalho avaliativo - Cibersegurança - UFU 2026/2
=============================================================
"""

from enum import Enum
import json
import os

ARQUIVO = "inventario.json"


# =============================================================
# REQUISITO 2 — Enum com tipos de ativos (código + descrição)
# =============================================================
class TipoAtivo(Enum):
    NOTEBOOK   = (1, "Notebook")
    SERVIDOR   = (2, "Servidor")
    ROTEADOR   = (3, "Roteador")
    APLICACAO  = (4, "Aplicação Web")
    BANCO      = (5, "Banco de Dados")
    IMPRESSORA = (6, "Impressora de Rede")

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

    @classmethod
    def por_codigo(cls, codigo):
        """Devolve o TipoAtivo correspondente ao código, ou None."""
        for tipo in cls:
            if tipo.codigo == codigo:
                return tipo
        return None


# Listas fixas para validar entrada do usuário
SEVERIDADES = ["Baixa", "Média", "Alta", "Crítica"]
STATUS = ["Aberta", "Em tratamento", "Corrigida", "Aceita como risco"]


# =============================================================
# PERSISTÊNCIA — ler e salvar arquivo (REQUISITO 3)
# =============================================================
def carregar():
    """Lê o arquivo e devolve um dicionário {id_str: ativo}."""
    if not os.path.exists(ARQUIVO):
        return {}
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Aviso] Erro ao ler arquivo: {e}. Iniciando vazio.")
        return {}


def salvar(base):
    """Grava o dicionário no arquivo em JSON."""
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(base, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Erro] Não foi possível salvar: {e}")


# =============================================================
# FUNÇÕES AUXILIARES — entrada de dados
# =============================================================
def pedir_inteiro(mensagem):
    """Pede um número inteiro, repetindo até o usuário digitar algo válido."""
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print("[Erro] Digite um número inteiro válido.")


def pedir_texto(mensagem):
    """Pede um texto não vazio, repetindo até o usuário digitar algo."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("[Erro] Este campo não pode ficar vazio.")


def pedir_opcao(mensagem, opcoes):
    """Pede uma opção dentre uma lista fixa (aceita maiúsculas/minúsculas)."""
    while True:
        valor = input(mensagem).strip()
        for op in opcoes:
            if valor.lower() == op.lower():
                return op
        print(f"[Erro] Escolha uma das opções: {', '.join(opcoes)}")


# =============================================================
# REQUISITO 1 + 3 — Cadastrar ativo
# =============================================================
def cadastrar(base):
    print("\n--- CADASTRAR ATIVO ---")

    id_ativo = pedir_inteiro("ID único (número inteiro): ")
    chave = str(id_ativo)

    if chave in base:
        print(f"[Erro] Já existe ativo com ID {id_ativo}.")
        return

    hostname    = pedir_texto("Hostname: ")
    responsavel = pedir_texto("Responsável: ")
    setor       = pedir_texto("Setor/Localização: ")
    descricao   = input("Descrição (opcional): ").strip()

    print("\nTipos disponíveis:")
    for tipo in TipoAtivo:
        print(f"  [{tipo.codigo}] {tipo.descricao}")

    while True:
        codigo = pedir_inteiro("Código do tipo: ")
        tipo = TipoAtivo.por_codigo(codigo)
        if tipo:
            break
        print("[Erro] Código de tipo inválido.")

    base[chave] = {
        "id": id_ativo,
        "hostname": hostname,
        "responsavel": responsavel,
        "setor": setor,
        "descricao": descricao,
        "tipo_codigo": tipo.codigo,
        "tipo_descricao": tipo.descricao,
        "vulnerabilidades": []
    }
    salvar(base)
    print(f"[Sucesso] Ativo '{hostname}' cadastrado!")


# =============================================================
# REQUISITO 4 — Consultar ativo
# =============================================================
def consultar(base):
    print("\n--- CONSULTAR ATIVO ---")

    if not base:
        print("Nenhum ativo cadastrado.")
        return

    opcao = pedir_opcao("Buscar por (1) ID ou (2) Hostname? ", ["1", "2"])
    encontrados = []

    if opcao == "1":
        id_busca = pedir_inteiro("ID: ")
        chave = str(id_busca)
        if chave in base:
            encontrados.append(base[chave])
    else:
        texto = pedir_texto("Parte do hostname: ").lower()
        for ativo in base.values():
            if texto in ativo["hostname"].lower():
                encontrados.append(ativo)

    if not encontrados:
        print("Nenhum ativo encontrado.")
        return

    for a in encontrados:
        print("\n" + "-" * 45)
        print(f"ID..........: {a['id']}")
        print(f"Hostname....: {a['hostname']}")
        print(f"Tipo........: [{a['tipo_codigo']}] {a['tipo_descricao']}")
        print(f"Responsável.: {a['responsavel']}")
        print(f"Setor.......: {a['setor']}")
        if a['descricao']:
            print(f"Descrição...: {a['descricao']}")
        print(f"Vulnerabilidades: {len(a['vulnerabilidades'])}")
        print("-" * 45)


# =============================================================
# REQUISITO 5 — Atualizar ativo
# =============================================================
def atualizar(base):
    print("\n--- ATUALIZAR ATIVO ---")

    id_ativo = pedir_inteiro("ID do ativo: ")
    chave = str(id_ativo)

    if chave not in base:
        print("[Erro] Ativo não encontrado.")
        return

    ativo = base[chave]
    print("(Pressione ENTER para manter o valor atual)")

    # Cada campo é atualizado somente se o usuário digitar algo
    for campo in ["hostname", "responsavel", "setor", "descricao"]:
        novo = input(f"Novo {campo} [{ativo[campo]}]: ").strip()
        if novo:
            ativo[campo] = novo

    # Tipo (precisa de lógica especial por ser numérico)
    print(f"Tipo atual: [{ativo['tipo_codigo']}] {ativo['tipo_descricao']}")
    for tipo in TipoAtivo:
        print(f"  [{tipo.codigo}] {tipo.descricao}")
    novo = input("Novo código de tipo (ENTER para manter): ").strip()
    if novo:
        try:
            tipo_novo = TipoAtivo.por_codigo(int(novo))
            if tipo_novo:
                ativo["tipo_codigo"] = tipo_novo.codigo
                ativo["tipo_descricao"] = tipo_novo.descricao
            else:
                print("[Aviso] Tipo inválido. Mantido o anterior.")
        except ValueError:
            print("[Aviso] Valor inválido. Mantido o anterior.")

    salvar(base)
    print("[Sucesso] Ativo atualizado!")


# =============================================================
# REQUISITO 6 — Deletar ativo
# =============================================================
def deletar(base):
    print("\n--- DELETAR ATIVO ---")

    id_ativo = pedir_inteiro("ID do ativo: ")
    chave = str(id_ativo)

    if chave not in base:
        print("[Erro] Ativo não encontrado.")
        return

    removido = base.pop(chave)   # remove ativo + vulnerabilidades
    salvar(base)
    print(f"[Sucesso] Ativo '{removido['hostname']}' e suas "
          f"{len(removido['vulnerabilidades'])} vulnerabilidades foram removidos.")


# =============================================================
# REQUISITO 7 — Cadastrar vulnerabilidade em um ativo
# =============================================================
def cadastrar_vulnerabilidade(base):
    print("\n--- CADASTRAR VULNERABILIDADE ---")

    id_ativo = pedir_inteiro("ID do ativo: ")
    chave = str(id_ativo)

    if chave not in base:
        print("[Erro] Ativo não encontrado.")
        return

    descricao = pedir_texto("Descrição: ")
    categoria = pedir_texto("Categoria/Tipo: ")

    print(f"\nSeveridades válidas: {', '.join(SEVERIDADES)}")
    severidade = pedir_opcao("Severidade: ", SEVERIDADES)

    print(f"Status válidos: {', '.join(STATUS)}")
    status = pedir_opcao("Status: ", STATUS)

    base[chave]["vulnerabilidades"].append({
        "descricao": descricao,
        "categoria": categoria,
        "severidade": severidade,
        "status": status
    })
    salvar(base)
    print("[Sucesso] Vulnerabilidade registrada!")


# =============================================================
# REQUISITO 8 — Visualizar vulnerabilidades de um ativo
# =============================================================
def visualizar_vulnerabilidades(base):
    print("\n--- VULNERABILIDADES DO ATIVO ---")

    id_ativo = pedir_inteiro("ID do ativo: ")
    chave = str(id_ativo)

    if chave not in base:
        print("[Erro] Ativo não encontrado.")
        return

    ativo = base[chave]
    print(f"\nAtivo: {ativo['hostname']} (ID: {ativo['id']})")

    if not ativo["vulnerabilidades"]:
        print("[Status] Este ativo está SEM vulnerabilidades registradas.")
        return

    print(f"Total: {len(ativo['vulnerabilidades'])} vulnerabilidade(s).\n")
    for i, v in enumerate(ativo["vulnerabilidades"], start=1):
        print(f"[{i}] {v['descricao']}")
        print(f"    Categoria.: {v['categoria']}")
        print(f"    Severidade: {v['severidade']}")
        print(f"    Status....: {v['status']}")
        print("-" * 45)


# =============================================================
# REQUISITO 1 — Menu principal
# =============================================================
def menu():
    base = carregar()   # REQUISITO 3 e 9

    while True:
        print("\n==========================================")
        print("   INVENTÁRIO DE ATIVOS DE TI")
        print("==========================================")
        print("1 - Cadastrar ativo")
        print("2 - Consultar ativo")
        print("3 - Atualizar ativo")
        print("4 - Deletar ativo")
        print("5 - Cadastrar vulnerabilidade")
        print("6 - Visualizar vulnerabilidades")
        print("0 - Sair")
        print("==========================================")

        opcao = input("Escolha uma opção: ").strip()

        if   opcao == "1": cadastrar(base)
        elif opcao == "2": consultar(base)
        elif opcao == "3": atualizar(base)
        elif opcao == "4": deletar(base)
        elif opcao == "5": cadastrar_vulnerabilidade(base)
        elif opcao == "6": visualizar_vulnerabilidades(base)
        elif opcao == "0":
            print("\nEncerrando. Até logo!")
            break
        else:
            print("[Erro] Opção inválida. Escolha entre 0 e 6.")


if __name__ == "__main__":
    menu()