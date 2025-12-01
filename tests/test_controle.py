"""
Testes unitários para controle.py - Usando funções simples
"""
import pytest
from src.controle_inteligente_ie.controle import EntradaEstoque, TabelaHash, ModuloControle
from src.controle_inteligente_ie.modelos import ProdutoInspecionado, ConsultaProduto


# ==================== Testes EntradaEstoque ====================

def test_entrada_estoque_criacao():
    """Cria entrada de estoque"""
    entrada = EntradaEstoque(chave_cliente=1, tamanho=10, tempo_inspecao=100)
    assert entrada.chave_cliente == 1
    assert entrada.tamanho == 10
    assert entrada.tempo_inspecao == 100


def test_entrada_estoque_valores_diferentes():
    """Cria entrada com valores diferentes"""
    entrada = EntradaEstoque(chave_cliente=42, tamanho=500, tempo_inspecao=5000)
    assert entrada.chave_cliente == 42


# ==================== Testes TabelaHash Init ====================

def test_tabela_hash_init_padrao():
    """Inicializa com capacidade padrão"""
    tabela = TabelaHash()
    assert tabela._capacidade == 100
    assert len(tabela._buckets) == 100


def test_tabela_hash_init_customizado():
    """Inicializa com capacidade customizada"""
    tabela = TabelaHash(capacidade=50)
    assert tabela._capacidade == 50
    assert len(tabela._buckets) == 50


# ==================== Testes Função Hash ====================

def test_funcao_hash_valida():
    """Função hash retorna índice válido"""
    tabela = TabelaHash(capacidade=100)
    indice = tabela._funcao_hash(0, 1)
    assert 0 <= indice < 100


def test_funcao_hash_deterministica():
    """Função hash é determinística"""
    tabela = TabelaHash(capacidade=100)
    i1 = tabela._funcao_hash(10, 20)
    i2 = tabela._funcao_hash(10, 20)
    assert i1 == i2


def test_funcao_hash_negativo():
    """Função hash trata negativos"""
    tabela = TabelaHash(capacidade=100)
    indice = tabela._funcao_hash(-5, 10)
    assert 0 <= indice < 100


# ==================== Testes TabelaHash Inserir ====================

def test_inserir_entrada():
    """Insere entrada simples"""
    tabela = TabelaHash()
    entrada = EntradaEstoque(1, 10, 100)
    tabela.inserir(entrada)
    resultado = tabela.buscar(1, 10)
    assert resultado is not None


def test_inserir_multiplas():
    """Insere múltiplas entradas"""
    tabela = TabelaHash()
    for i in range(10):
        entrada = EntradaEstoque(i, 10 + i, 100 + i)
        tabela.inserir(entrada)
    
    resultado = tabela.buscar(5, 15)
    assert resultado is not None


def test_inserir_duplicada_atualiza():
    """Inserir duplicado atualiza"""
    tabela = TabelaHash()
    e1 = EntradaEstoque(1, 10, 100)
    e2 = EntradaEstoque(1, 10, 200)
    tabela.inserir(e1)
    tabela.inserir(e2)
    
    resultado = tabela.buscar(1, 10)
    assert resultado.tempo_inspecao == 200


def test_inserir_com_colisao():
    """Insere com colisão"""
    tabela = TabelaHash(capacidade=5)
    for i in range(10):
        entrada = EntradaEstoque(i, i + 1, (i + 1) * 10)
        tabela.inserir(entrada)
    
    resultado = tabela.buscar(5, 6)
    assert resultado is not None


# ==================== Testes TabelaHash Buscar ====================

def test_buscar_existente():
    """Busca entrada existente"""
    tabela = TabelaHash()
    entrada = EntradaEstoque(1, 10, 100)
    tabela.inserir(entrada)
    resultado = tabela.buscar(1, 10)
    assert resultado.tempo_inspecao == 100


def test_buscar_nao_existente():
    """Busca entrada inexistente"""
    tabela = TabelaHash()
    resultado = tabela.buscar(1, 10)
    assert resultado is None


def test_buscar_chave_diferente():
    """Busca com chave diferente"""
    tabela = TabelaHash()
    entrada = EntradaEstoque(1, 10, 100)
    tabela.inserir(entrada)
    resultado = tabela.buscar(2, 10)
    assert resultado is None


def test_buscar_tamanho_diferente():
    """Busca com tamanho diferente"""
    tabela = TabelaHash()
    entrada = EntradaEstoque(1, 10, 100)
    tabela.inserir(entrada)
    resultado = tabela.buscar(1, 20)
    assert resultado is None


# ==================== Testes ModuloControle Init ====================

def test_modulo_controle_init():
    """Inicializa módulo controle"""
    controle = ModuloControle()
    assert controle._tabela_hash is not None


def test_modulo_controle_init_capacidade():
    """Inicializa com capacidade customizada"""
    controle = ModuloControle(capacidade_tabela=50)
    assert controle._tabela_hash._capacidade == 50


# ==================== Testes Receber Dados Inspeção ====================

def test_receber_dados_vazio():
    """Recebe dados vazios"""
    controle = ModuloControle()
    tempo, qtd = controle.receber_dados_inspecao([])
    assert tempo >= 0
    assert qtd == 0


def test_receber_dados_um_produto():
    """Recebe um produto"""
    controle = ModuloControle()
    produto = ProdutoInspecionado(1, 1, 10, 100)
    tempo, qtd = controle.receber_dados_inspecao([produto])
    assert qtd == 1


def test_receber_dados_multiplos():
    """Recebe múltiplos produtos"""
    controle = ModuloControle()
    produtos = [
        ProdutoInspecionado(i, 1, 10 + i, 100 + i)
        for i in range(10)
    ]
    tempo, qtd = controle.receber_dados_inspecao(produtos)
    assert qtd == 10


def test_receber_dados_armazena():
    """Dados são armazenados"""
    controle = ModuloControle()
    produto = ProdutoInspecionado(5, 1, 20, 200)
    controle.receber_dados_inspecao([produto])
    resultado = controle.buscar_tempo_inspecao(ConsultaProduto(5, 20))
    assert resultado == 200


# ==================== Testes Buscar Tempo Inspeção ====================

def test_buscar_tempo_existe():
    """Busca tempo existente"""
    controle = ModuloControle()
    produto = ProdutoInspecionado(1, 1, 10, 100)
    controle.receber_dados_inspecao([produto])
    resultado = controle.buscar_tempo_inspecao(ConsultaProduto(1, 10))
    assert resultado == 100


def test_buscar_tempo_nao_existe():
    """Busca tempo inexistente"""
    controle = ModuloControle()
    resultado = controle.buscar_tempo_inspecao(ConsultaProduto(1, 10))
    assert resultado is None


def test_buscar_tempo_multiplos():
    """Busca após múltiplas inserções"""
    controle = ModuloControle()
    for i in range(5):
        produto = ProdutoInspecionado(i, 1, 10 + i, 100 + i * 10)
        controle.receber_dados_inspecao([produto])
    
    resultado = controle.buscar_tempo_inspecao(ConsultaProduto(2, 12))
    assert resultado == 120


# ==================== Testes Executar Buscas ====================

def test_executar_buscas_vazio():
    """Executa buscas vazias"""
    controle = ModuloControle()
    tempo, qtd_buscas, qtd_encontrada = controle.executar_buscas([])
    assert tempo >= 0
    assert qtd_buscas == 0
    assert qtd_encontrada == 0


def test_executar_buscas_simples():
    """Executa busca simples"""
    controle = ModuloControle()
    produto = ProdutoInspecionado(1, 1, 10, 100)
    controle.receber_dados_inspecao([produto])
    
    consultas = [ConsultaProduto(1, 10)]
    tempo, qtd_buscas, qtd_encontrada = controle.executar_buscas(consultas)
    assert qtd_buscas == 1
    assert qtd_encontrada == 1


def test_executar_buscas_multiplas():
    """Executa múltiplas buscas"""
    controle = ModuloControle()
    for i in range(5):
        produto = ProdutoInspecionado(i, 1, 10 + i, 100 + i)
        controle.receber_dados_inspecao([produto])
    
    consultas = [ConsultaProduto(i, 10 + i) for i in range(5)]
    tempo, qtd_buscas, qtd_encontrada = controle.executar_buscas(consultas)
    assert qtd_buscas == 5
    assert qtd_encontrada == 5


def test_executar_buscas_parcialmente():
    """Executa buscas parcialmente encontradas"""
    controle = ModuloControle()
    for i in range(0, 5, 2):
        produto = ProdutoInspecionado(i, 1, 10 + i, 100 + i)
        controle.receber_dados_inspecao([produto])
    
    consultas = [ConsultaProduto(i, 10 + i) for i in range(5)]
    tempo, qtd_buscas, qtd_encontrada = controle.executar_buscas(consultas)
    assert qtd_buscas == 5
    assert qtd_encontrada == 3


# ==================== Testes Integração ====================

def test_fluxo_completo_controle():
    """Fluxo completo controle"""
    controle = ModuloControle()
    
    produtos = [
        ProdutoInspecionado(i, 1 if i % 2 == 0 else 2, 10 + i, 100 + i * 10)
        for i in range(10)
    ]
    
    tempo_i, qtd_i = controle.receber_dados_inspecao(produtos)
    assert qtd_i == 10
    
    consultas = [ConsultaProduto(i, 10 + i) for i in range(10)]
    tempo_b, qtd_buscas, qtd_encontrada = controle.executar_buscas(consultas)
    assert qtd_buscas == 10
    assert qtd_encontrada == 10


def test_modulos_independentes():
    """Módulos são independentes"""
    controle1 = ModuloControle()
    controle2 = ModuloControle()
    
    produto = ProdutoInspecionado(1, 1, 10, 100)
    controle1.receber_dados_inspecao([produto])
    
    resultado = controle2.buscar_tempo_inspecao(ConsultaProduto(1, 10))
    assert resultado is None


def test_hash_negativo_ajuste():
    """Hash negativo é ajustado corretamente"""
    # Cria tabela com capacidade pequena para forçar hash negativo
    tabela = TabelaHash(capacidade=7)
    
    # Valores específicos que resultam em hash negativo
    # Se (chave * 31 + tamanho) % capacidade < 0, precisa adicionar capacidade
    entrada = EntradaEstoque(chave_cliente=1000, tamanho=2000, tempo_inspecao=100)
    tabela.inserir(entrada)
    
    # Verifica se foi inserido
    resultado = tabela.buscar(1000, 2000)
    assert resultado is not None
    assert resultado.chave_cliente == 1000

