"""
Módulo monitoramento - Rastreamento e visualização de métricas de desempenho.

Responsável por registrar estatísticas de execução e criar visualizações
dos dados de inspeção e controle de estoque.

Classes:
    - ModuloMonitoramento: Módulo para rastreamento e visualização de métricas
"""

from __future__ import annotations
from typing import List, Dict, Any, Tuple
import time


class ModuloMonitoramento:
    """
    Módulo para rastreamento e visualização de métricas de desempenho.

    Responsável por registrar e exibir estatísticas de inspeção e operações
    de controle de estoque, incluindo visualizações gráficas.

    Attributes:
        _historico_inspecao_tipo1 (List): Registros de inspeção tipo 1
        _historico_inspecao_tipo2 (List): Registros de inspeção tipo 2
        _historico_controle_insercao (List): Registros de inserção
        _historico_controle_busca (List): Registros de busca

    Methods:
        registrar_inspecao: Registra estatísticas de inspeção
        registrar_controle_insercao: Registra operação de inserção
        registrar_controle_busca: Registra operação de busca
        historico: Property que retorna histórico completo
        plot_inspecao_tipo1: Visualiza dados de inspeção tipo 1
        plot_inspecao_tipo2: Visualiza dados de inspeção tipo 2
        plot_controle: Visualiza dados de controle combinados
    """

    def __init__(self) -> None:
        """
        Inicializa módulo de monitoramento com históricos vazios.

        Entry:
            - None

        Exit:
            - self: Módulo inicializado com 4 listas de histórico vazias

        Returns:
            None
        """
        self._historico_inspecao_tipo1: List[Dict[str, Any]] = []
        self._historico_inspecao_tipo2: List[Dict[str, Any]] = []
        self._historico_controle_insercao: List[Dict[str, Any]] = []
        self._historico_controle_busca: List[Dict[str, Any]] = []

    def registrar_inspecao(
        self,
        numero_produtos: int,
        tipo: int,
        tempo_total: int,
        quantidade: int,
    ) -> None:
        """
        Registra estatísticas de inspeção.

        Entry:
            - numero_produtos: int > 0 (número de produtos processados)
            - tipo: int in {1, 2} (tipo de inspeção)
            - tempo_total: int >= 0 (tempo total de inspeção)
            - quantidade: int > 0 (quantidade de produtos do tipo)

        Exit:
            - None: Registro adicionado ao histórico correspondente

        Args:
            numero_produtos: Quantidade de produtos inspecionados
            tipo: Tipo de inspeção (1 ou 2)
            tempo_total: Tempo total gasto em inspeção
            quantidade: Quantidade de produtos processados
        """
        registro = {
            "numero_produtos": numero_produtos,
            "tempo_total": tempo_total,
            "quantidade": quantidade,
            "timestamp": time.time(),
        }

        if tipo == 1:
            self._historico_inspecao_tipo1.append(registro)
        else:
            self._historico_inspecao_tipo2.append(registro)

    def registrar_controle_insercao(
        self,
        quantidade_inserida: int,
        tempo_execucao: float,
    ) -> None:
        """
        Registra operação de inserção no controle de estoque.

        Entry:
            - quantidade_inserida: int > 0 (quantidade de itens inseridos)
            - tempo_execucao: float >= 0.0 (tempo em segundos)

        Exit:
            - None: Registro adicionado ao histórico de inserção

        Args:
            quantidade_inserida: Quantidade de produtos inseridos
            tempo_execucao: Tempo de execução em segundos
        """
        registro = {
            "quantidade": quantidade_inserida,
            "tempo_execucao": tempo_execucao,
            "timestamp": time.time(),
        }
        self._historico_controle_insercao.append(registro)

    def registrar_controle_busca(
        self,
        quantidade_buscas: int,
        quantidade_encontrada: int,
        tempo_execucao: float,
    ) -> None:
        """
        Registra operação de busca no controle de estoque.

        Entry:
            - quantidade_buscas: int > 0 (quantidade total de buscas)
            - quantidade_encontrada: int (quantidade encontrada)
            - tempo_execucao: float >= 0.0 (tempo em segundos)

        Exit:
            - None: Registro adicionado ao histórico de busca

        Args:
            quantidade_buscas: Total de buscas realizadas
            quantidade_encontrada: Produtos encontrados
            tempo_execucao: Tempo de execução em segundos
        """
        registro = {
            "quantidade_buscas": quantidade_buscas,
            "quantidade_encontrada": quantidade_encontrada,
            "tempo_execucao": tempo_execucao,
            "timestamp": time.time(),
        }
        self._historico_controle_busca.append(registro)

    @property
    def historico(self) -> Dict[str, Any]:
        """
        Retorna histórico completo de todas as operações.

        Entry:
            - None (property)

        Exit:
            - Dict[str, Any]: Dicionário contendo todos os históricos
                * "inspecao_tipo1": List[Dict]
                * "inspecao_tipo2": List[Dict]
                * "controle_insercao": List[Dict]
                * "controle_busca": List[Dict]

        Returns:
            Dict com históricos de todas as operações (cópias manuais)
        """
        # Cria cópias manuais dos históricos (sem usar list())
        hist_tipo1 = []
        for item in self._historico_inspecao_tipo1:
            hist_tipo1.append(item)

        hist_tipo2 = []
        for item in self._historico_inspecao_tipo2:
            hist_tipo2.append(item)

        hist_insercao = []
        for item in self._historico_controle_insercao:
            hist_insercao.append(item)

        hist_busca = []
        for item in self._historico_controle_busca:
            hist_busca.append(item)

        return {
            "inspecao_tipo1": hist_tipo1,
            "inspecao_tipo2": hist_tipo2,
            "controle_insercao": hist_insercao,
            "controle_busca": hist_busca,
        }

    def plot_inspecao_tipo1(self) -> None:
        """
        Visualiza dados de inspeção tipo 1.

        Entry:
            - None (método sem parâmetros)

        Exit:
            - None: Exibe gráfico matplotlib de inspeção tipo 1
                * Eixo X: Número de produtos
                * Eixo Y: Tempo total de inspeção

        Returns:
            None
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Erro: matplotlib não está instalado")
            return

        if len(self._historico_inspecao_tipo1) == 0:
            print("Nenhum dado de inspeção tipo 1 para visualizar")
            return

        x = []
        y = []

        for registro in self._historico_inspecao_tipo1:
            x.append(registro["numero_produtos"])
            y.append(registro["tempo_total"])

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker='o', label='Inspeção Tipo 1')
        plt.xlabel('Número de Produtos')
        plt.ylabel('Tempo Total (ms)')
        plt.title('Inspeção Tipo 1: T(n) = 2n - 1')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_inspecao_tipo2(self) -> None:
        """
        Visualiza dados de inspeção tipo 2.

        Entry:
            - None (método sem parâmetros)

        Exit:
            - None: Exibe gráfico matplotlib de inspeção tipo 2
                * Eixo X: Número de produtos
                * Eixo Y: Tempo total de inspeção

        Returns:
            None
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Erro: matplotlib não está instalado")
            return

        if len(self._historico_inspecao_tipo2) == 0:
            print("Nenhum dado de inspeção tipo 2 para visualizar")
            return

        x = []
        y = []

        for registro in self._historico_inspecao_tipo2:
            x.append(registro["numero_produtos"])
            y.append(registro["tempo_total"])

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker='s', color='orange', label='Inspeção Tipo 2')
        plt.xlabel('Número de Produtos')
        plt.ylabel('Tempo Total (ms)')
        plt.title('Inspeção Tipo 2: T(n) = n(n+1)/2')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_controle(self) -> None:
        """
        Visualiza dados de controle combinados (inserção e busca).

        Entry:
            - None (método sem parâmetros)

        Exit:
            - None: Exibe gráfico matplotlib com operações de controle
                * Mostra tempo de inserção e busca em subplots

        Returns:
            None
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Erro: matplotlib não está instalado")
            return

        tem_insercao = len(self._historico_controle_insercao) > 0
        tem_busca = len(self._historico_controle_busca) > 0

        if not tem_insercao and not tem_busca:
            print("Nenhum dado de controle para visualizar")
            return

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Plot Inserção
        if tem_insercao:
            x_insercao = []
            y_insercao = []

            for registro in self._historico_controle_insercao:
                x_insercao.append(registro["quantidade"])
                y_insercao.append(registro["tempo_execucao"])

            axes[0].plot(x_insercao, y_insercao, marker='o', color='green',
                        label='Inserção')
            axes[0].set_xlabel('Quantidade Inserida')
            axes[0].set_ylabel('Tempo (segundos)')
            axes[0].set_title('Tempo de Inserção')
            axes[0].legend()
            axes[0].grid(True)
        else:
            axes[0].text(0.5, 0.5, 'Sem dados de inserção',
                        ha='center', va='center')

        # Plot Busca
        if tem_busca:
            x_busca = []
            y_busca = []

            for registro in self._historico_controle_busca:
                x_busca.append(registro["quantidade_buscas"])
                y_busca.append(registro["tempo_execucao"])

            axes[1].plot(x_busca, y_busca, marker='s', color='red',
                        label='Busca')
            axes[1].set_xlabel('Quantidade de Buscas')
            axes[1].set_ylabel('Tempo (segundos)')
            axes[1].set_title('Tempo de Busca')
            axes[1].legend()
            axes[1].grid(True)
        else:
            axes[1].text(0.5, 0.5, 'Sem dados de busca',
                        ha='center', va='center')

        plt.tight_layout()
        plt.show()
