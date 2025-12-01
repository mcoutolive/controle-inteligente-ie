"""
Módulo dados - Geração de dados de teste e consultas para simulações.

Responsável por gerar dados de teste com propriedades controladas,
incluindo produtos e consultas ao sistema de controle inteligente.

Classes:
    - GeradorDados: Gerador de dados para simulações
"""

from __future__ import annotations
import random
from typing import List, Tuple
from .modelos import Produto, ConsultaProduto


class GeradorDados:
    """
    Gera dados de teste para simulações do sistema de controle inteligente.

    Responsável por criar listas de produtos e consultas com parâmetros
    controlados para fins de teste e validação do sistema.

    Attributes:
        None

    Methods:
        gerar_lista_produtos: Gera lista de produtos aleatórios
        gerar_lista_buscas: Gera lista de consultas ao estoque
        exibir_lista_produtos: Exibe informações sobre a lista de produtos
    """

    def gerar_lista_produtos(
        self,
        quantidade: int,
        tamanho_minimo: int,
        tamanho_maximo: int,
        numero_tipos: int,
        numero_clientes: int,
    ) -> List[Produto]:
        """
        Gera uma lista de produtos com parâmetros aleatórios.

        Entry:
            - quantidade: int > 0 (quantidade de produtos a gerar)
            - tamanho_minimo: int >= 1 (tamanho mínimo dos produtos)
            - tamanho_maximo: int >= tamanho_minimo (tamanho máximo dos produtos)
            - numero_tipos: int in {1, 2} (quantidade de tipos de produtos)
            - numero_clientes: int > 0 (quantidade de clientes distintos)

        Exit:
            - List[Produto]: Lista de produtos gerados com atributos aleatórios
                * chave_cliente: randint(0, numero_clientes-1)
                * tipo_produto: randint(1, numero_tipos)
                * tamanho: randint(tamanho_minimo, tamanho_maximo)

        Returns:
            List[Produto]: Lista contendo `quantidade` produtos aleatórios.
        """
        produtos = []
        contador = 0
        while contador < quantidade:
            chave_cliente = random.randint(0, numero_clientes - 1)
            tipo_produto = random.randint(1, numero_tipos)
            tamanho = random.randint(tamanho_minimo, tamanho_maximo)

            produto = Produto(
                chave_cliente=chave_cliente,
                tipo_produto=tipo_produto,
                tamanho=tamanho,
            )
            produtos.append(produto)
            contador += 1

        return produtos

    def gerar_lista_buscas(
        self,
        quantidade: int,
        produtos_inspecionados: List,
    ) -> List[ConsultaProduto]:
        """
        Gera lista de consultas com distribuição 80/20.

        80% das buscas referem-se a produtos existentes no estoque,
        20% referem-se a produtos não existentes (usando clientes aleatórios).

        Entry:
            - quantidade: int > 0 (quantidade de buscas a gerar)
            - produtos_inspecionados: List (lista de ProdutoInspecionado existentes)
                * Precisa ter len(produtos_inspecionados) > 0 se quantidade > 0

        Exit:
            - List[ConsultaProduto]: Lista com `quantidade` consultas
                * 80% referem-se a produtos em produtos_inspecionados
                * 20% referem-se a produtos não existentes

        Returns:
            List[ConsultaProduto]: Lista de consultas geradas.

        Raises:
            ValueError: Se quantidade > 0 e produtos_inspecionados está vazia.
        """
        if quantidade > 0 and len(produtos_inspecionados) == 0:
            raise ValueError(
                "Impossível gerar buscas: lista de produtos vazia"
            )

        buscas = []
        contador = 0
        while contador < quantidade:
            numero_aleatorio = random.random()

            if numero_aleatorio < 0.8:
                # 80% das buscas referem a produtos existentes
                indice = contador % len(produtos_inspecionados)
                produto = produtos_inspecionados[indice]
                consulta = ConsultaProduto(
                    chave_cliente=produto.chave_cliente,
                    tamanho_produto=produto.tamanho,
                )
            else:
                # 20% das buscas referem a produtos não existentes
                chave_cliente = random.randint(0, 999)
                tamanho_produto = random.randint(1, 1000)
                consulta = ConsultaProduto(
                    chave_cliente=chave_cliente,
                    tamanho_produto=tamanho_produto,
                )

            buscas.append(consulta)
            contador += 1

        return buscas

    def exibir_lista_produtos(
        self,
        produtos: List[Produto],
    ) -> None:
        """
        Exibe informações sobre a lista de produtos.

        Entry:
            - produtos: List[Produto] (lista de produtos a exibir)

        Exit:
            - None (função apenas imprime informações)
            - Saída: Exibe quantidade e primeiros 5 produtos (ou menos)

        Returns:
            None
        """
        quantidade_total = len(produtos)
        print(f"\n{'='*60}")
        print(f"{'LISTA DE PRODUTOS':^60}")
        print(f"{'='*60}")
        print(f"Total de produtos: {quantidade_total}")
        print(f"{'-'*60}")

        quantidade_mostrada = 0
        maximo_mostrar = 5

        for produto in produtos:
            if quantidade_mostrada >= maximo_mostrar:
                print("... (restante omitido)")
                break

            print(
                f"  Cliente: {produto.chave_cliente:<4} | "
                f"Tipo: {produto.tipo_produto:<4} | "
                f"Tamanho: {produto.tamanho:<4}"
            )
            quantidade_mostrada += 1

        print(f"{'='*60}\n")
