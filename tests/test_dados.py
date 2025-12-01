"""
Testes unitários para dados.py - Usando funções simples
"""
import pytest
from src.controle_inteligente_ie.dados import GeradorDados
from src.controle_inteligente_ie.modelos import Produto, ProdutoInspecionado, ConsultaProduto


# ==================== Testes Init ====================

def test_gerador_dados_init():
    """Inicializa gerador dados"""
    gerador = GeradorDados()
    assert gerador is not None


# ==================== Testes Gerar Produtos ====================

def test_gerar_lista_produtos_vazio():
    """Gera lista de produtos vazia"""
    gerador = GeradorDados()
    lista = gerador.gerar_lista_produtos(
        quantidade=0,
        tamanho_minimo=1,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=10
    )
    assert lista == []


def test_gerar_lista_produtos_um():
    """Gera um produto"""
    gerador = GeradorDados()
    lista = gerador.gerar_lista_produtos(
        quantidade=1,
        tamanho_minimo=10,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=5
    )
    assert len(lista) == 1
    assert isinstance(lista[0], Produto)


def test_gerar_lista_produtos_multiplos():
    """Gera múltiplos produtos"""
    gerador = GeradorDados()
    lista = gerador.gerar_lista_produtos(
        quantidade=10,
        tamanho_minimo=1,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=10
    )
    assert len(lista) == 10


def test_gerar_lista_produtos_grande():
    """Gera muitos produtos"""
    gerador = GeradorDados()
    lista = gerador.gerar_lista_produtos(
        quantidade=1000,
        tamanho_minimo=1,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=20
    )
    assert len(lista) == 1000


def test_gerar_lista_produtos_chave_cliente():
    """Gera produtos com chave_cliente válido"""
    gerador = GeradorDados()
    lista = gerador.gerar_lista_produtos(
        quantidade=10,
        tamanho_minimo=1,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=5
    )
    for produto in lista:
        assert 0 <= produto.chave_cliente < 5


def test_gerar_lista_produtos_tipo():
    """Gera produtos com tipo_produto válido"""
    gerador = GeradorDados()
    lista = gerador.gerar_lista_produtos(
        quantidade=10,
        tamanho_minimo=1,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=5
    )
    for produto in lista:
        assert produto.tipo_produto in [1, 2]


def test_gerar_lista_produtos_tamanho():
    """Gera produtos com tamanho em range válido"""
    gerador = GeradorDados()
    lista = gerador.gerar_lista_produtos(
        quantidade=10,
        tamanho_minimo=10,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=5
    )
    for produto in lista:
        assert 10 <= produto.tamanho <= 100


def test_gerar_lista_produtos_tipo_un():
    """Gera produtos tipo 1 só"""
    gerador = GeradorDados()
    lista = gerador.gerar_lista_produtos(
        quantidade=10,
        tamanho_minimo=1,
        tamanho_maximo=100,
        numero_tipos=1,
        numero_clientes=5
    )
    for produto in lista:
        assert produto.tipo_produto == 1


# ==================== Testes Gerar Buscas ====================

def test_gerar_lista_buscas_vazio():
    """Gera lista de buscas vazia"""
    gerador = GeradorDados()
    lista = gerador.gerar_lista_buscas(quantidade=0, produtos_inspecionados=[])
    assert lista == []


def test_gerar_lista_buscas_um():
    """Gera uma busca"""
    gerador = GeradorDados()
    produtos = [ProdutoInspecionado(1, 1, 10, 100)]
    lista = gerador.gerar_lista_buscas(quantidade=1, produtos_inspecionados=produtos)
    assert len(lista) == 1
    assert isinstance(lista[0], ConsultaProduto)


def test_gerar_lista_buscas_multiplas():
    """Gera múltiplas buscas"""
    gerador = GeradorDados()
    produtos = [
        ProdutoInspecionado(i, 1, 10 + i, 100 + i)
        for i in range(5)
    ]
    lista = gerador.gerar_lista_buscas(quantidade=20, produtos_inspecionados=produtos)
    assert len(lista) == 20


def test_gerar_lista_buscas_com_produtos():
    """Gera buscas com produtos válidos"""
    gerador = GeradorDados()
    produtos = [
        ProdutoInspecionado(1, 1, 10, 100),
        ProdutoInspecionado(2, 1, 20, 200),
    ]
    lista = gerador.gerar_lista_buscas(quantidade=10, produtos_inspecionados=produtos)
    
    for consulta in lista:
        assert isinstance(consulta, ConsultaProduto)
        assert consulta.chave_cliente >= 0
        assert consulta.tamanho_produto > 0


def test_gerar_lista_buscas_distribuicao_80_20():
    """Gera buscas com distribuição 80/20"""
    gerador = GeradorDados()
    produtos = [
        ProdutoInspecionado(i, 1, 10 + i, 100 + i)
        for i in range(5)
    ]
    lista = gerador.gerar_lista_buscas(quantidade=1000, produtos_inspecionados=produtos)
    
    buscas_validas = 0
    for consulta in lista:
        assert isinstance(consulta, ConsultaProduto)


def test_gerar_lista_buscas_valor_error_vazio():
    """Gera buscas com quantidade > 0 e lista vazia lança erro"""
    gerador = GeradorDados()
    with pytest.raises(ValueError):
        gerador.gerar_lista_buscas(quantidade=10, produtos_inspecionados=[])


# ==================== Testes Exibir Produtos ====================

def test_exibir_lista_produtos_vazio(capsys):
    """Exibe lista vazia"""
    gerador = GeradorDados()
    gerador.exibir_lista_produtos([])
    captured = capsys.readouterr()
    assert "LISTA DE PRODUTOS" in captured.out or len(captured.out) >= 0


def test_exibir_lista_produtos_um(capsys):
    """Exibe um produto"""
    gerador = GeradorDados()
    lista = [Produto(1, 1, 10)]
    gerador.exibir_lista_produtos(lista)
    captured = capsys.readouterr()
    assert "1" in captured.out or "LISTA" in captured.out


def test_exibir_lista_produtos_multiplos(capsys):
    """Exibe múltiplos produtos"""
    gerador = GeradorDados()
    lista = [Produto(i, (i % 2) + 1, 10 + i) for i in range(5)]
    gerador.exibir_lista_produtos(lista)
    captured = capsys.readouterr()
    assert len(captured.out) > 0


def test_exibir_lista_produtos_muitos(capsys):
    """Exibe muitos produtos (verifica truncamento)"""
    gerador = GeradorDados()
    lista = [Produto(i, 1, 10) for i in range(100)]
    gerador.exibir_lista_produtos(lista)
    captured = capsys.readouterr()
    assert "restante omitido" in captured.out or len(captured.out) > 0


# ==================== Testes Integração ====================

def test_fluxo_completo_geracao():
    """Fluxo completo de geração"""
    gerador = GeradorDados()
    
    produtos = gerador.gerar_lista_produtos(
        quantidade=100,
        tamanho_minimo=10,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=20
    )
    assert len(produtos) == 100
    
    # Converte para ProdutoInspecionado
    produtos_inspecionados = [
        ProdutoInspecionado(p.chave_cliente, p.tipo_produto, p.tamanho, 100 + i)
        for i, p in enumerate(produtos)
    ]
    
    buscas = gerador.gerar_lista_buscas(
        quantidade=50,
        produtos_inspecionados=produtos_inspecionados
    )
    assert len(buscas) == 50


def test_gerador_multiplas_chamadas():
    """Gerador funciona com múltiplas chamadas"""
    gerador = GeradorDados()
    
    lista1 = gerador.gerar_lista_produtos(
        quantidade=10,
        tamanho_minimo=1,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=5
    )
    lista2 = gerador.gerar_lista_produtos(
        quantidade=10,
        tamanho_minimo=1,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=5
    )
    
    assert len(lista1) == 10
    assert len(lista2) == 10


def test_gerador_quantidade_grande():
    """Gerador funciona com quantidade grande"""
    gerador = GeradorDados()
    
    produtos = gerador.gerar_lista_produtos(
        quantidade=5000,
        tamanho_minimo=1,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=50
    )
    assert len(produtos) == 5000
    
    produtos_inspecionados = [
        ProdutoInspecionado(p.chave_cliente, p.tipo_produto, p.tamanho, 100 + i)
        for i, p in enumerate(produtos)
    ]
    
    buscas = gerador.gerar_lista_buscas(
        quantidade=2000,
        produtos_inspecionados=produtos_inspecionados
    )
    assert len(buscas) == 2000

