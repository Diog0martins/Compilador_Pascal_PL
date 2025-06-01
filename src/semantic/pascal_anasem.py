from symbol_table import generalSTable


class SemanticError(Exception):
    """Exceção personalizada para erros semânticos."""
    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem


def verificar_variavel_existe(nome):
    if not generalSTable.has_variable(nome):
        raise SemanticError(f"Erro: variável '{nome}' não foi declarada.")


def verificar_tipos_iguais(tipo1, tipo2, contexto="operação"):
    if tipo1 != tipo2:
        raise SemanticError(f"Erro: tipos incompatíveis na {contexto} ('{tipo1}' vs '{tipo2}').")

def verificar_tipos_iguais(tipo1, tipo2, contexto=""):
    if tipo1 != tipo2:
        raise SemanticError(f"Tipos incompatíveis no contexto de {contexto}: '{tipo1}' ≠ '{tipo2}'")

def verificar_atribuicao_tipo(nome, tipo_valor):
    tipo_esperado = generalSTable.get_type(nome)
    if tipo_esperado != tipo_valor:
        raise SemanticError(
            f"Erro: atribuição incompatível para '{nome}'. "
            f"Esperado '{tipo_esperado}', obtido '{tipo_valor}'."
        )

def verificar_tipo_booleano(tipo):
    if tipo != "boolean":
        raise SemanticError(f"Esperava valor booleano, mas recebeu tipo '{tipo}'")

