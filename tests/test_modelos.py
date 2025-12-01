"""
Testes unitários para modelos.py - Usando funções simples
"""
import pytest
from src.controle_inteligente_ie.modelos import Produto, ProdutoInspecionado, ConsultaProduto


# ==================== Testes Produto ====================

def test_produto_criacao():
    """Cria produto simples"""
    produto = Produto(1, 1, 10)
    assert produto.chave_cliente == 1
    assert produto.tipo_produto == 1
    assert produto.tamanho == 10


def test_produto_valores_diferentes():
    """Cria produto com valores diferentes"""
    produto = Produto(42, 2, 500)
    assert produto.chave_cliente == 42
    assert produto.tipo_produto == 2
    assert produto.tamanho == 500


def test_produto_atributos():
    """Produto tem todos os atributos"""
    produto = Produto(1, 1, 10)
    assert hasattr(produto, "chave_cliente")
    assert hasattr(produto, "tipo_produto")
    assert hasattr(produto, "tamanho")


def test_produto_igualdade():
    """Produtos iguais são iguais"""
    p1 = Produto(1, 1, 10)
    p2 = Produto(1, 1, 10)
    assert p1 == p2


def test_produto_desigualdade_cliente():
    """Produtos com chave_cliente diferente não são iguais"""
    p1 = Produto(1, 1, 10)
    p2 = Produto(2, 1, 10)
    assert p1 != p2


def test_produto_desigualdade_tipo():
    """Produtos com tipo_produto diferente não são iguais"""
    p1 = Produto(1, 1, 10)
    p2 = Produto(1, 2, 10)
    assert p1 != p2


def test_produto_desigualdade_tamanho():
    """Produtos com tamanho diferente não são iguais"""
    p1 = Produto(1, 1, 10)
    p2 = Produto(1, 1, 20)
    assert p1 != p2


def test_produto_zero_cliente():
    """Cria produto com chave_cliente zero"""
    produto = Produto(0, 1, 10)
    assert produto.chave_cliente == 0


def test_produto_valores_grandes():
    """Cria produto com valores grandes"""
    produto = Produto(999999, 2, 999999)
    assert produto.chave_cliente == 999999
    assert produto.tamanho == 999999


# ==================== Testes ProdutoInspecionado ====================

def test_produto_inspecionado_criacao():
    """Cria produto inspecionado"""
    produto = ProdutoInspecionado(1, 2, 10, 100)
    assert produto.chave_cliente == 1
    assert produto.tipo_produto == 2
    assert produto.tamanho == 10
    assert produto.tempo_inspecao == 100


def test_produto_inspecionado_atributos():
    """Produto inspecionado tem todos os atributos"""
    produto = ProdutoInspecionado(1, 1, 10, 100)
    assert hasattr(produto, "chave_cliente")
    assert hasattr(produto, "tipo_produto")
    assert hasattr(produto, "tamanho")
    assert hasattr(produto, "tempo_inspecao")


def test_produto_inspecionado_heranca():
    """Produto inspecionado herda de Produto"""
    produto = ProdutoInspecionado(1, 1, 10, 100)
    assert isinstance(produto, Produto)


def test_produto_inspecionado_cliente_tamanho():
    """Produto inspecionado tem chave_cliente e tamanho de Produto"""
    produto = ProdutoInspecionado(5, 1, 20, 200)
    assert produto.chave_cliente == 5
    assert produto.tamanho == 20


def test_produto_inspecionado_tipo1():
    """Cria produto inspecionado tipo 1"""
    produto = ProdutoInspecionado(1, 1, 10, 100)
    assert produto.tipo_produto == 1


def test_produto_inspecionado_tipo2():
    """Cria produto inspecionado tipo 2"""
    produto = ProdutoInspecionado(1, 2, 10, 100)
    assert produto.tipo_produto == 2


def test_produto_inspecionado_igualdade():
    """Produtos inspecionados iguais são iguais"""
    p1 = ProdutoInspecionado(1, 1, 10, 100)
    p2 = ProdutoInspecionado(1, 1, 10, 100)
    assert p1 == p2


def test_produto_inspecionado_desigualdade_tipo():
    """Produtos inspecionados com tipo diferente não são iguais"""
    p1 = ProdutoInspecionado(1, 1, 10, 100)
    p2 = ProdutoInspecionado(1, 2, 10, 100)
    assert p1 != p2


def test_produto_inspecionado_desigualdade_tempo():
    """Produtos inspecionados com tempo diferente não são iguais"""
    p1 = ProdutoInspecionado(1, 1, 10, 100)
    p2 = ProdutoInspecionado(1, 1, 10, 200)
    assert p1 != p2


def test_produto_inspecionado_valores_diferentes():
    """Cria produto inspecionado com valores diferentes"""
    produto = ProdutoInspecionado(42, 2, 500, 5000)
    assert produto.chave_cliente == 42
    assert produto.tipo_produto == 2
    assert produto.tamanho == 500
    assert produto.tempo_inspecao == 5000


def test_produto_inspecionado_tempo_zero():
    """Cria produto inspecionado com tempo zero"""
    produto = ProdutoInspecionado(1, 1, 10, 0)
    assert produto.tempo_inspecao == 0


def test_produto_inspecionado_tempo_grande():
    """Cria produto inspecionado com tempo grande"""
    produto = ProdutoInspecionado(1, 1, 10, 999999)
    assert produto.tempo_inspecao == 999999


# ==================== Testes ConsultaProduto ====================

def test_consulta_produto_criacao():
    """Cria consulta produto"""
    consulta = ConsultaProduto(1, 10)
    assert consulta.chave_cliente == 1
    assert consulta.tamanho_produto == 10


def test_consulta_produto_atributos():
    """Consulta produto tem todos os atributos"""
    consulta = ConsultaProduto(1, 10)
    assert hasattr(consulta, "chave_cliente")
    assert hasattr(consulta, "tamanho_produto")


def test_consulta_produto_valores_diferentes():
    """Cria consulta com valores diferentes"""
    consulta = ConsultaProduto(42, 500)
    assert consulta.chave_cliente == 42
    assert consulta.tamanho_produto == 500


def test_consulta_produto_igualdade():
    """Consultas iguais são iguais"""
    c1 = ConsultaProduto(1, 10)
    c2 = ConsultaProduto(1, 10)
    assert c1 == c2


def test_consulta_produto_desigualdade_cliente():
    """Consultas com chave_cliente diferente não são iguais"""
    c1 = ConsultaProduto(1, 10)
    c2 = ConsultaProduto(2, 10)
    assert c1 != c2


def test_consulta_produto_desigualdade_tamanho():
    """Consultas com tamanho_produto diferente não são iguais"""
    c1 = ConsultaProduto(1, 10)
    c2 = ConsultaProduto(1, 20)
    assert c1 != c2


def test_consulta_produto_zero():
    """Cria consulta com valores zero"""
    consulta = ConsultaProduto(0, 0)
    assert consulta.chave_cliente == 0
    assert consulta.tamanho_produto == 0


# ==================== Testes Compatibilidade ====================

def test_produto_vs_consulta_compatibilidade():
    """Produto e Consulta são tipos diferentes"""
    p = Produto(1, 1, 10)
    c = ConsultaProduto(1, 10)
    assert type(p) != type(c)


def test_produto_inspecionado_compatibilidade():
    """Produto inspecionado compatível com Produto"""
    pi = ProdutoInspecionado(1, 1, 10, 100)
    p = Produto(1, 1, 10)
    assert pi.chave_cliente == p.chave_cliente
    assert pi.tamanho == p.tamanho


# ==================== Testes Serialização ====================

def test_produto_repr():
    """Produto tem representação"""
    produto = Produto(1, 1, 10)
    repr_str = repr(produto)
    assert isinstance(repr_str, str)
    assert "1" in repr_str or "Produto" in repr_str


def test_produto_inspecionado_repr():
    """Produto inspecionado tem representação"""
    produto = ProdutoInspecionado(1, 1, 10, 100)
    repr_str = repr(produto)
    assert isinstance(repr_str, str)


def test_consulta_repr():
    """Consulta tem representação"""
    consulta = ConsultaProduto(1, 10)
    repr_str = repr(consulta)
    assert isinstance(repr_str, str)


# ==================== Testes Múltiplos ====================

def test_criar_multiplos_produtos():
    """Cria múltiplos produtos"""
    produtos = [Produto(i, (i % 2) + 1, i * 10) for i in range(100)]
    assert len(produtos) == 100
    assert all(isinstance(p, Produto) for p in produtos)


def test_criar_multiplos_inspecionados():
    """Cria múltiplos produtos inspecionados"""
    produtos = [
        ProdutoInspecionado(i, (i % 2) + 1, i * 10, i * 100)
        for i in range(100)
    ]
    assert len(produtos) == 100
    assert all(isinstance(p, ProdutoInspecionado) for p in produtos)


def test_criar_multiplas_consultas():
    """Cria múltiplas consultas"""
    consultas = [ConsultaProduto(i, i * 10) for i in range(100)]
    assert len(consultas) == 100
    assert all(isinstance(c, ConsultaProduto) for c in consultas)


# ==================== Testes Edge Cases ====================

def test_lista_produtos_ordenacao():
    """Lista de produtos pode ser ordenada"""
    produtos = [
        Produto(3, 1, 30),
        Produto(1, 1, 10),
        Produto(2, 1, 20),
    ]
    produtos_ordenados = sorted(produtos, key=lambda p: p.chave_cliente)
    assert produtos_ordenados[0].chave_cliente == 1
    assert produtos_ordenados[1].chave_cliente == 2
    assert produtos_ordenados[2].chave_cliente == 3


def test_produto_inspecionado_com_zero():
    """Produto inspecionado com zero em valores"""
    produto = ProdutoInspecionado(0, 1, 0, 0)
    assert produto.chave_cliente == 0
    assert produto.tamanho == 0
    assert produto.tempo_inspecao == 0

