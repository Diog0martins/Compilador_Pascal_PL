from symbol_table import generalSTable


class SemanticError(Exception):
    """Exceção personalizada para erros semânticos."""
    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem


def verificar_variavel_existe(nome):
    if not generalSTable.has_variable(nome):
        raise SemanticError(f"Erro: variável '{nome}' não foi declarada.")


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


def verificar_tipo_inteiro(tipo, contexto=""):
    if tipo != "integer":
        raise SemanticError(f"Esperava tipo inteiro no contexto de {contexto}, mas recebeu '{tipo}'.")

def verificar_variavel_e_array(nome):
    if not generalSTable.is_array(nome):
        raise SemanticError(f"'{nome}' não é um array.")

def verificar_tipo_suportado(tipo):
    if tipo.lower() not in ("integer", "real", "string", "boolean", "char"):
        raise SemanticError(f"Tipo não suportado: {tipo}")


def verificar_intervalo_valido(lower, upper):
    if int(upper) < int(lower):
        raise SemanticError(f"Intervalo inválido: [{lower}..{upper}]")
    
def verificar_funcao_nao_repetida(func_name):
    from symbol_table import generalSTable
    if generalSTable.has_function(func_name):
        raise SemanticError(f"Função '{func_name}' já declarada.")

def obter_tipo_variavel(nome):
    verificar_variavel_existe(nome)
    return generalSTable.get_type(nome)
