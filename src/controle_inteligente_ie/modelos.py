"""
Módulo modelos - Definição de modelos de dados para o sistema.

Define as classes de dados que representam produtos e consultas no sistema
de controle inteligente de estoque.

Classes:
    - Produto: Produto a ser inspecionado
    - ProdutoInspecionado: Produto após inspeção com tempo calculado
    - ConsultaProduto: Consulta ao estoque
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Produto:
    """
    Representa um produto a ser inspecionado.

    Attributes:
        chave_cliente (int): Identificador do cliente (inteiro positivo).
        tipo_produto (int): Tipo do produto (1 ou 2).
        tamanho (int): Tamanho do produto (inteiro positivo).

    Entry: 
        - chave_cliente: int >= 0
        - tipo_produto: int in {1, 2}
        - tamanho: int > 0

    Exit:
        - Instância de Produto com atributos validados
    """
    chave_cliente: int
    tipo_produto: int
    tamanho: int


@dataclass
class ProdutoInspecionado(Produto):
    """
    Produto após inspeção, com o tempo de inspeção calculado.

    Attributes:
        chave_cliente (int): Identificador do cliente.
        tipo_produto (int): Tipo do produto (1 ou 2).
        tamanho (int): Tamanho do produto.
        tempo_inspecao (int): Tempo total de inspeção calculado em millisegundos.

    Entry:
        - chave_cliente: int >= 0
        - tipo_produto: int in {1, 2}
        - tamanho: int > 0
        - tempo_inspecao: int >= 1

    Exit:
        - Instância de ProdutoInspecionado com tempo de inspeção definido
    """
    tempo_inspecao: int


@dataclass
class ConsultaProduto:
    """
    Consulta ao estoque para obter o tempo de inspeção.

    Attributes:
        chave_cliente (int): Identificador do cliente a consultar.
        tamanho_produto (int): Tamanho do produto a ser consultado.

    Entry:
        - chave_cliente: int >= 0
        - tamanho_produto: int > 0

    Exit:
        - Instância de ConsultaProduto pronta para busca no estoque
    """
    chave_cliente: int
    tamanho_produto: int
