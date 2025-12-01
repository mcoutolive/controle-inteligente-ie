"""
Módulo controle - Gerenciamento de estoque com tabela hash.

Responsável por armazenar, recuperar e gerenciar informações de produtos
no estoque usando uma tabela hash com encadeamento para colisões.

Classes:
    - TabelaHash: Implementação de tabela hash com encadeamento
    - EntradaEstoque: Entrada individual no estoque
    - ModuloControle: Wrapper para gerenciar operações de estoque
"""

from __future__ import annotations
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from .modelos import ProdutoInspecionado, ConsultaProduto


@dataclass
class EntradaEstoque:
    """
    Entrada individual no estoque.

    Attributes:
        chave_cliente (int): Identificador do cliente.
        tamanho (int): Tamanho do produto.
        tempo_inspecao (int): Tempo de inspeção do produto.

    Entry:
        - chave_cliente: int >= 0
        - tamanho: int > 0
        - tempo_inspecao: int >= 1

    Exit:
        - Instância de EntradaEstoque com dados validados
    """
    chave_cliente: int
    tamanho: int
    tempo_inspecao: int


class TabelaHash:
    """
    Implementação de tabela hash com encadeamento para tratamento de colisões.

    Responsável por armazenar e recuperar EntradaEstoque de forma eficiente
    usando chave hash baseada em (chave_cliente, tamanho).

    Attributes:
        _capacidade (int): Tamanho da tabela hash
        _buckets (List[List[EntradaEstoque]]): Buckets para encadeamento

    Methods:
        inserir: Insere entrada no estoque
        buscar: Busca entrada por chave de cliente e tamanho
    """

    def __init__(self, capacidade: int = 100) -> None:
        """
        Inicializa tabela hash com capacidade especificada.

        Entry:
            - capacidade: int > 0 (tamanho desejado da tabela hash)

        Exit:
            - self: Tabela hash inicializada com buckets vazios

        Args:
            capacidade: Tamanho da tabela hash (padrão 100)
        """
        self._capacidade = capacidade
        self._buckets: List[List[EntradaEstoque]] = []

        # Inicializa buckets manualmente (sem list comprehension)
        contador = 0
        while contador < capacidade:
            self._buckets.append([])
            contador += 1

    def _funcao_hash(
        self,
        chave_cliente: int,
        tamanho: int,
    ) -> int:
        """
        Calcula hash baseado em chave_cliente e tamanho.

        Entry:
            - chave_cliente: int >= 0
            - tamanho: int > 0

        Exit:
            - int: Índice do bucket (0 <= idx < self._capacidade)

        Returns:
            int: Índice hash
        """
        valor_hash = (chave_cliente * 31 + tamanho) % self._capacidade
        if valor_hash < 0:
            valor_hash = valor_hash + self._capacidade
        return valor_hash

    def inserir(self, entrada: EntradaEstoque) -> None:
        """
        Insere entrada no estoque.

        Entry:
            - entrada: EntradaEstoque (contém chave_cliente, tamanho, tempo_inspecao)

        Exit:
            - None: Entrada inserida no bucket correspondente

        Args:
            entrada: Entrada a ser inserida
        """
        indice = self._funcao_hash(entrada.chave_cliente, entrada.tamanho)
        bucket = self._buckets[indice]

        # Verifica se já existe entrada com mesma chave
        indice_existente = -1
        contador = 0
        for item in bucket:
            if (item.chave_cliente == entrada.chave_cliente and
                item.tamanho == entrada.tamanho):
                indice_existente = contador
                break
            contador += 1

        if indice_existente >= 0:
            # Atualiza entrada existente
            bucket[indice_existente] = entrada
        else:
            # Adiciona nova entrada
            bucket.append(entrada)

    def buscar(
        self,
        chave_cliente: int,
        tamanho: int,
    ) -> Optional[EntradaEstoque]:
        """
        Busca entrada no estoque.

        Entry:
            - chave_cliente: int >= 0
            - tamanho: int > 0

        Exit:
            - Optional[EntradaEstoque]: Entrada encontrada ou None se não existe

        Args:
            chave_cliente: Chave do cliente a buscar
            tamanho: Tamanho do produto a buscar

        Returns:
            EntradaEstoque se encontrada, None caso contrário
        """
        indice = self._funcao_hash(chave_cliente, tamanho)
        bucket = self._buckets[indice]

        for item in bucket:
            if (item.chave_cliente == chave_cliente and
                item.tamanho == tamanho):
                return item

        return None


class ModuloControle:
    """
    Módulo de controle de estoque usando tabela hash.

    Wrapper que gerencia operações de inserção e busca de produtos no estoque,
    usando TabelaHash como estrutura de dados subjacente.

    Attributes:
        _tabela_hash (TabelaHash): Tabela hash para armazenar estoque

    Methods:
        receber_dados_inspecao: Insere múltiplos produtos do módulo de inspeção
        buscar_tempo_inspecao: Busca tempo de inspeção de um produto
        executar_buscas: Executa múltiplas buscas e retorna estatísticas
    """

    def __init__(self, capacidade_tabela: int = 100) -> None:
        """
        Inicializa módulo de controle com tabela hash.

        Entry:
            - capacidade_tabela: int > 0 (capacidade da tabela hash)

        Exit:
            - self: Módulo de controle inicializado

        Args:
            capacidade_tabela: Capacidade da tabela hash interna
        """
        self._tabela_hash = TabelaHash(capacidade_tabela)

    def receber_dados_inspecao(
        self,
        produtos_inspecionados: List[ProdutoInspecionado],
    ) -> Tuple[float, int]:
        """
        Insere múltiplos produtos inspecionados no estoque.

        Entry:
            - produtos_inspecionados: List[ProdutoInspecionado]
                * Cada produto contém: chave_cliente, tamanho, tempo_inspecao

        Exit:
            - Tuple[float, int]:
                * float: Tempo total gasto em inserções (em segundos)
                * int: Quantidade de produtos inseridos

        Args:
            produtos_inspecionados: Lista de produtos a inserir

        Returns:
            Tuple com tempo de execução e quantidade inserida
        """
        import time

        tempo_inicio = time.time()
        quantidade_inserida = 0

        for produto in produtos_inspecionados:
            entrada = EntradaEstoque(
                chave_cliente=produto.chave_cliente,
                tamanho=produto.tamanho,
                tempo_inspecao=produto.tempo_inspecao,
            )
            self._tabela_hash.inserir(entrada)
            quantidade_inserida += 1

        tempo_final = time.time()
        tempo_total = tempo_final - tempo_inicio

        return tempo_total, quantidade_inserida

    def buscar_tempo_inspecao(
        self,
        consulta: ConsultaProduto,
    ) -> Optional[int]:
        """
        Busca tempo de inspeção de um produto específico.

        Entry:
            - consulta: ConsultaProduto (contém chave_cliente, tamanho_produto)

        Exit:
            - Optional[int]: Tempo de inspeção se encontrado, None caso contrário

        Args:
            consulta: Consulta com chave_cliente e tamanho_produto

        Returns:
            Tempo de inspeção ou None se não encontrado
        """
        entrada = self._tabela_hash.buscar(
            consulta.chave_cliente,
            consulta.tamanho_produto,
        )

        if entrada is not None:
            return entrada.tempo_inspecao

        return None

    def executar_buscas(
        self,
        consultas: List[ConsultaProduto],
    ) -> Tuple[float, int, int]:
        """
        Executa múltiplas buscas e retorna estatísticas.

        Entry:
            - consultas: List[ConsultaProduto] (lista de consultas a executar)

        Exit:
            - Tuple[float, int, int]:
                * float: Tempo total gasto em buscas (em segundos)
                * int: Quantidade de buscas realizadas
                * int: Quantidade de produtos encontrados

        Args:
            consultas: Lista de consultas a executar

        Returns:
            Tuple com tempo total, quantidade de buscas e quantidade encontrada
        """
        import time

        tempo_inicio = time.time()
        quantidade_encontrada = 0

        for consulta in consultas:
            resultado = self.buscar_tempo_inspecao(consulta)
            if resultado is not None:
                quantidade_encontrada += 1

        tempo_final = time.time()
        tempo_total = tempo_final - tempo_inicio
        quantidade_buscas = len(consultas)

        return tempo_total, quantidade_buscas, quantidade_encontrada
