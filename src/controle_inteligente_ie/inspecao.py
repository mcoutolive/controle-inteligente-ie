"""
Módulo inspecao - Processamento e inspeção de produtos.

Responsável por calcular tempos de inspeção para diferentes tipos de produtos
e realizar ordenação dos produtos baseada nesses tempos.

Classes:
    - ModuloInspecao: Módulo responsável pela inspeção de produtos
"""

from __future__ import annotations
from typing import List, Dict, Tuple, Any
from .modelos import Produto, ProdutoInspecionado


class ModuloInspecao:
    """
    Módulo para processamento e inspeção de produtos.

    Responsável por calcular o tempo de inspeção de cada produto baseado
    em seu tipo e tamanho, e por ordenar os produtos por tempo de inspeção.

    Attributes:
        None

    Methods:
        processar_lista_produtos: Processa lista de produtos e calcula tempos
        ordenar_por_tempo: Ordena produtos por tempo de inspeção
    """

    def processar_lista_produtos(
        self,
        produtos: List[Produto],
    ) -> Tuple[List[ProdutoInspecionado], Dict[str, Any]]:
        """
        Processa lista de produtos e calcula tempo de inspeção para cada um.

        Entry:
            - produtos: List[Produto] (lista de produtos a processar)
                * Cada produto contém: chave_cliente, tipo_produto, tamanho

        Exit:
            - Tuple contendo:
                * List[ProdutoInspecionado]: Produtos com tempo_inspecao calculado
                * Dict[str, Any]: Estatísticas de inspeção:
                    - "tempo_total_tipo1": int (soma de tempos para tipo 1)
                    - "tempo_total_tipo2": int (soma de tempos para tipo 2)
                    - "quantidade_tipo1": int (quantidade de produtos tipo 1)
                    - "quantidade_tipo2": int (quantidade de produtos tipo 2)

        Returns:
            Tuple com produtos inspecionados e estatísticas
        """
        produtos_inspecionados = []
        tempo_total_tipo1 = 0
        tempo_total_tipo2 = 0
        quantidade_tipo1 = 0
        quantidade_tipo2 = 0

        for produto in produtos:
            if produto.tipo_produto == 1:
                tempo_inspecao = self._tempo_inspecao_tipo1(produto.tamanho)
                tempo_total_tipo1 += tempo_inspecao
                quantidade_tipo1 += 1
            else:  # tipo_produto == 2
                tempo_inspecao = self._tempo_inspecao_tipo2(produto.tamanho)
                tempo_total_tipo2 += tempo_inspecao
                quantidade_tipo2 += 1

            produto_inspecionado = ProdutoInspecionado(
                chave_cliente=produto.chave_cliente,
                tipo_produto=produto.tipo_produto,
                tamanho=produto.tamanho,
                tempo_inspecao=tempo_inspecao,
            )
            produtos_inspecionados.append(produto_inspecionado)

        estatisticas = {
            "tempo_total_tipo1": tempo_total_tipo1,
            "tempo_total_tipo2": tempo_total_tipo2,
            "quantidade_tipo1": quantidade_tipo1,
            "quantidade_tipo2": quantidade_tipo2,
        }

        return produtos_inspecionados, estatisticas

    def _tempo_inspecao_tipo1(self, tamanho: int) -> int:
        """
        Calcula tempo de inspeção tipo 1 usando recorrência: T(n) = 1 + 2*T(n//2).

        Padrão exponencial: T(n) = 2n - 1

        Entry:
            - tamanho: int > 0 (tamanho do produto)

        Exit:
            - int: Tempo de inspeção calculado (resultado de T(n))

        Returns:
            int: Tempo de inspeção tipo 1
        """
        if tamanho == 1:
            return 1

        return 1 + 2 * self._tempo_inspecao_tipo1(tamanho // 2)

    def _tempo_inspecao_tipo2(self, tamanho: int) -> int:
        """
        Calcula tempo de inspeção tipo 2 usando soma triangular: T(n) = 1+2+...+n.

        Padrão polinomial: T(n) = n*(n+1)/2

        Entry:
            - tamanho: int > 0 (tamanho do produto)

        Exit:
            - int: Tempo de inspeção calculado (soma triangular)

        Returns:
            int: Tempo de inspeção tipo 2
        """
        tempo_total = 0
        contador = 1
        while contador <= tamanho:
            tempo_total += contador
            contador += 1

        return tempo_total

    def ordenar_por_tempo(
        self,
        produtos: List[ProdutoInspecionado],
    ) -> List[ProdutoInspecionado]:
        """
        Ordena produtos por tempo de inspeção usando Insertion Sort.

        Implementação manual de Insertion Sort sem usar sorted() ou sort().

        Entry:
            - produtos: List[ProdutoInspecionado] (lista de produtos a ordenar)

        Exit:
            - List[ProdutoInspecionado]: Lista ordenada por tempo_inspecao
                * Ordem crescente (menor tempo primeiro)
                * Usa Insertion Sort manual

        Returns:
            List[ProdutoInspecionado]: Lista ordenada por tempo
        """
        # Cria cópia para não modificar lista original
        resultado = []
        for produto in produtos:
            resultado.append(produto)

        # Insertion Sort
        indice_inicio = 1
        while indice_inicio < len(resultado):
            item_atual = resultado[indice_inicio]
            posicao = indice_inicio - 1

            # Encontra posição correta para inserir
            while posicao >= 0 and resultado[posicao].tempo_inspecao > item_atual.tempo_inspecao:
                resultado[posicao + 1] = resultado[posicao]
                posicao -= 1

            resultado[posicao + 1] = item_atual
            indice_inicio += 1

        return resultado
