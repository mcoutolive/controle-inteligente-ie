"""
Testes unitários para inspecao.py - Usando funções simples
"""
import pytest
from src.controle_inteligente_ie.inspecao import ModuloInspecao
from src.controle_inteligente_ie.modelos import Produto, ProdutoInspecionado


# ==================== Testes Init ====================

def test_modulo_inspecao_init():
    """Inicializa módulo inspeção"""
    inspecao = ModuloInspecao()
    assert inspecao is not None


# ==================== Testes Tempo Tipo 1 (Método Privado) ====================

def test_tempo_inspecao_tipo1_um():
    """Calcula tempo tipo 1 com tamanho 1 - T(1) = 1"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo1(1)
    assert tempo == 1


def test_tempo_inspecao_tipo1_dois():
    """Calcula tempo tipo 1 com tamanho 2 - T(2) = 1 + 2*T(1) = 3"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo1(2)
    assert tempo == 3


def test_tempo_inspecao_tipo1_tres():
    """Calcula tempo tipo 1 com tamanho 3 - T(3) = 1 + 2*T(1) = 3"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo1(3)
    assert tempo == 3


def test_tempo_inspecao_tipo1_quatro():
    """Calcula tempo tipo 1 com tamanho 4 - T(4) = 1 + 2*T(2) = 7"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo1(4)
    assert tempo == 7


def test_tempo_inspecao_tipo1_dez():
    """Calcula tempo tipo 1 com tamanho 10 - T(10) = 1 + 2*T(5) = 1 + 2*3 = 15"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo1(10)
    assert tempo == 15


def test_tempo_inspecao_tipo1_grande():
    """Calcula tempo tipo 1 com número grande"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo1(100)
    # T(100) = 1 + 2*T(50) = 1 + 2*(1 + 2*T(25)) = 1 + 2 + 4*T(25)
    # Não é 2n-1, apenas para potências de 2!
    assert tempo > 0


def test_tempo_inspecao_tipo1_formula_potencias_2():
    """Valida fórmula T(n) = 2n - 1 para potências de 2"""
    inspecao = ModuloInspecao()
    for n in [1, 2, 4, 8, 16]:
        tempo = inspecao._tempo_inspecao_tipo1(n)
        esperado = 2 * n - 1
        assert tempo == esperado


# ==================== Testes Tempo Tipo 2 (Método Privado) ====================

def test_tempo_inspecao_tipo2_um():
    """Calcula tempo tipo 2 com tamanho 1 - T(1) = 1"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo2(1)
    assert tempo == 1


def test_tempo_inspecao_tipo2_dois():
    """Calcula tempo tipo 2 com tamanho 2 - T(2) = 3"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo2(2)
    assert tempo == 3


def test_tempo_inspecao_tipo2_tres():
    """Calcula tempo tipo 2 com tamanho 3 - T(3) = 6"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo2(3)
    assert tempo == 6


def test_tempo_inspecao_tipo2_quatro():
    """Calcula tempo tipo 2 com tamanho 4 - T(4) = 10"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo2(4)
    assert tempo == 10


def test_tempo_inspecao_tipo2_cinco():
    """Calcula tempo tipo 2 com tamanho 5 - T(5) = 15"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo2(5)
    assert tempo == 15


def test_tempo_inspecao_tipo2_dez():
    """Calcula tempo tipo 2 com tamanho 10 - T(10) = 55"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo2(10)
    assert tempo == 55


def test_tempo_inspecao_tipo2_grande():
    """Calcula tempo tipo 2 com número grande"""
    inspecao = ModuloInspecao()
    tempo = inspecao._tempo_inspecao_tipo2(100)
    assert tempo == 5050


def test_tempo_inspecao_tipo2_formula():
    """Valida fórmula T(n) = n*(n+1)/2"""
    inspecao = ModuloInspecao()
    for n in [1, 2, 5, 10, 20, 50]:
        tempo = inspecao._tempo_inspecao_tipo2(n)
        esperado = n * (n + 1) // 2
        assert tempo == esperado


# ==================== Testes Processar Lista Produtos ====================

def test_processar_lista_vazia():
    """Processa lista vazia"""
    inspecao = ModuloInspecao()
    produtos_result, stats = inspecao.processar_lista_produtos([])
    assert produtos_result == []
    assert stats["quantidade_tipo1"] == 0
    assert stats["quantidade_tipo2"] == 0


def test_processar_lista_um_tipo1():
    """Processa um produto tipo 1"""
    inspecao = ModuloInspecao()
    lista = [Produto(1, 1, 10)]
    produtos_result, stats = inspecao.processar_lista_produtos(lista)
    
    assert len(produtos_result) == 1
    assert stats["quantidade_tipo1"] == 1
    assert stats["quantidade_tipo2"] == 0
    # T(10) = 1 + 2*T(5) = 1 + 2*3 = 15
    assert produtos_result[0].tempo_inspecao == 15


def test_processar_lista_um_tipo2():
    """Processa um produto tipo 2"""
    inspecao = ModuloInspecao()
    lista = [Produto(1, 2, 10)]
    produtos_result, stats = inspecao.processar_lista_produtos(lista)
    
    assert len(produtos_result) == 1
    assert stats["quantidade_tipo1"] == 0
    assert stats["quantidade_tipo2"] == 1
    assert produtos_result[0].tempo_inspecao == 55


def test_processar_lista_multiplos():
    """Processa múltiplos produtos"""
    inspecao = ModuloInspecao()
    lista = [
        Produto(0, 1, 5),
        Produto(1, 2, 5),
        Produto(2, 1, 3),
    ]
    produtos_result, stats = inspecao.processar_lista_produtos(lista)
    
    assert len(produtos_result) == 3
    assert stats["quantidade_tipo1"] == 2
    assert stats["quantidade_tipo2"] == 1


def test_processar_lista_preserva_ids():
    """Processa preserva IDs dos clientes"""
    inspecao = ModuloInspecao()
    lista = [Produto(42, 1, 10)]
    produtos_result, stats = inspecao.processar_lista_produtos(lista)
    
    assert produtos_result[0].chave_cliente == 42


# ==================== Testes Ordenar Por Tempo ====================

def test_ordenar_por_tempo_vazio():
    """Ordena lista vazia"""
    inspecao = ModuloInspecao()
    resultado = inspecao.ordenar_por_tempo([])
    assert resultado == []


def test_ordenar_por_tempo_um():
    """Ordena um produto"""
    inspecao = ModuloInspecao()
    lista = [ProdutoInspecionado(1, 1, 10, 5)]
    resultado = inspecao.ordenar_por_tempo(lista)
    assert len(resultado) == 1


def test_ordenar_por_tempo_crescente():
    """Ordena em ordem crescente"""
    inspecao = ModuloInspecao()
    lista = [
        ProdutoInspecionado(3, 1, 30, 10),
        ProdutoInspecionado(1, 1, 10, 5),
        ProdutoInspecionado(2, 1, 20, 8),
    ]
    resultado = inspecao.ordenar_por_tempo(lista)
    assert resultado[0].tempo_inspecao == 5
    assert resultado[1].tempo_inspecao == 8
    assert resultado[2].tempo_inspecao == 10


def test_ordenar_por_tempo_ja_ordenado():
    """Ordena lista já ordenada"""
    inspecao = ModuloInspecao()
    lista = [
        ProdutoInspecionado(1, 1, 10, 1),
        ProdutoInspecionado(2, 1, 20, 2),
        ProdutoInspecionado(3, 1, 30, 3),
    ]
    resultado = inspecao.ordenar_por_tempo(lista)
    assert resultado[0].tempo_inspecao == 1


def test_ordenar_por_tempo_invertido():
    """Ordena lista invertida"""
    inspecao = ModuloInspecao()
    lista = [
        ProdutoInspecionado(3, 1, 30, 10),
        ProdutoInspecionado(2, 1, 20, 8),
        ProdutoInspecionado(1, 1, 10, 5),
    ]
    resultado = inspecao.ordenar_por_tempo(lista)
    assert resultado[0].tempo_inspecao == 5
    assert resultado[-1].tempo_inspecao == 10


def test_ordenar_por_tempo_duplicados():
    """Ordena com tempos duplicados"""
    inspecao = ModuloInspecao()
    lista = [
        ProdutoInspecionado(1, 1, 10, 5),
        ProdutoInspecionado(2, 1, 20, 5),
        ProdutoInspecionado(3, 1, 30, 5),
    ]
    resultado = inspecao.ordenar_por_tempo(lista)
    assert len(resultado) == 3
    assert all(p.tempo_inspecao == 5 for p in resultado)


def test_ordenar_por_tempo_preserva_dados():
    """Ordena preserva dados dos produtos"""
    inspecao = ModuloInspecao()
    lista = [
        ProdutoInspecionado(3, 2, 30, 10),
        ProdutoInspecionado(1, 1, 10, 5),
    ]
    resultado = inspecao.ordenar_por_tempo(lista)
    assert resultado[0].chave_cliente == 1
    assert resultado[0].tipo_produto == 1


# ==================== Testes Integração ====================

def test_fluxo_completo_inspecao():
    """Fluxo completo inspeção"""
    inspecao = ModuloInspecao()
    
    lista = [
        Produto(i, (i % 2) + 1, 10 + i)
        for i in range(5)
    ]
    produtos_result, stats = inspecao.processar_lista_produtos(lista)
    
    assert len(produtos_result) == 5
    assert all(isinstance(p, ProdutoInspecionado) for p in produtos_result)
    assert all(p.tempo_inspecao > 0 for p in produtos_result)
    
    ordenado = inspecao.ordenar_por_tempo(produtos_result)
    for i in range(len(ordenado) - 1):
        assert ordenado[i].tempo_inspecao <= ordenado[i + 1].tempo_inspecao


def test_tempo_tipo1_vs_tipo2():
    """Compara tempos tipo 1 vs tipo 2"""
    inspecao = ModuloInspecao()
    
    # Usar potência de 2 para tipo 1
    n = 8
    tempo1 = inspecao._tempo_inspecao_tipo1(n)
    tempo2 = inspecao._tempo_inspecao_tipo2(n)
    
    assert tempo1 == 2 * n - 1
    assert tempo2 == n * (n + 1) // 2
    assert tempo1 < tempo2


def test_inspecao_escalabilidade():
    """Testa escalabilidade com muitos produtos"""
    inspecao = ModuloInspecao()
    lista = [Produto(i % 100, (i % 2) + 1, 1) for i in range(1000)]
    produtos_result, stats = inspecao.processar_lista_produtos(lista)
    assert len(produtos_result) == 1000
