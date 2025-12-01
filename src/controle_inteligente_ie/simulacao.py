"""
Módulo simulacao - Orquestração de simulações completas do sistema.

Responsável por coordenar todas as etapas de simulação: geração de dados,
inspeção de produtos, controle de estoque e monitoramento de métricas.

Classes:
    - SimuladorSistema: Orquestrador de simulações
"""

from __future__ import annotations
from typing import Dict, Any
from .dados import GeradorDados
from .inspecao import ModuloInspecao
from .controle import ModuloControle
from .monitoramento import ModuloMonitoramento


class SimuladorSistema:
    """
    Orquestrador de simulações do sistema de controle inteligente.

    Coordena todas as etapas da simulação: geração de dados, inspeção,
    controle e monitoramento, retornando relatório completo de execução.

    Attributes:
        _gerador_dados (GeradorDados): Gerador de dados de teste
        _modulo_inspecao (ModuloInspecao): Módulo de inspeção
        _modulo_controle (ModuloControle): Módulo de controle
        _modulo_monitoramento (ModuloMonitoramento): Módulo de monitoramento
        _configuracao (Dict): Configuração da simulação

    Methods:
        configurar_simulacao: Configura parâmetros da simulação
        executar_simulacoes: Executa simulação completa
        resumo_final: Retorna resumo com resultados
    """

    def __init__(self) -> None:
        """
        Inicializa simulador com módulos vazios.

        Entry:
            - None

        Exit:
            - self: Simulador inicializado

        Returns:
            None
        """
        self._gerador_dados = GeradorDados()
        self._modulo_inspecao = ModuloInspecao()
        self._modulo_controle = ModuloControle()
        self._modulo_monitoramento = ModuloMonitoramento()
        self._configuracao: Dict[str, Any] = {}

    def configurar_simulacao(
        self,
        quantidade_produtos: int,
        tamanho_minimo: int,
        tamanho_maximo: int,
        numero_tipos: int,
        numero_clientes: int,
        percentual_buscas: int,
        usar_random: bool,
    ) -> None:
        """
        Configura parâmetros da simulação.

        Entry:
            - quantidade_produtos: int > 0 (quantidade de produtos a gerar)
            - tamanho_minimo: int >= 1 (tamanho mínimo dos produtos)
            - tamanho_maximo: int >= tamanho_minimo (tamanho máximo)
            - numero_tipos: int in {1, 2} (quantidade de tipos)
            - numero_clientes: int > 0 (quantidade de clientes)
            - percentual_buscas: int in [0, 100] (percentual de buscas)
            - usar_random: bool (ativa randomização)

        Exit:
            - None: Configuração salva em self._configuracao

        Args:
            quantidade_produtos: Produtos a gerar
            tamanho_minimo: Tamanho mínimo
            tamanho_maximo: Tamanho máximo
            numero_tipos: Quantidade de tipos (1 ou 2)
            numero_clientes: Quantidade de clientes
            percentual_buscas: Percentual para buscas (0-100)
            usar_random: Habilita randomização
        """
        self._configuracao = {
            "quantidade_produtos": quantidade_produtos,
            "tamanho_minimo": tamanho_minimo,
            "tamanho_maximo": tamanho_maximo,
            "numero_tipos": numero_tipos,
            "numero_clientes": numero_clientes,
            "percentual_buscas": percentual_buscas,
            "usar_random": usar_random,
        }

    def executar_simulacoes(self) -> None:
        """
        Executa simulação completa do sistema.

        Entry:
            - None (usa configuração estabelecida em configurar_simulacao)

        Exit:
            - None: Executa todas as etapas:
                * 1. Geração de dados
                * 2. Inspeção de produtos
                * 3. Inserção no controle
                * 4. Execução de buscas

        Returns:
            None
        """
        if not self._configuracao:
            raise ValueError("Simulação não foi configurada")

        # 1. Geração de dados
        produtos = self._gerador_dados.gerar_lista_produtos(
            quantidade=self._configuracao["quantidade_produtos"],
            tamanho_minimo=self._configuracao["tamanho_minimo"],
            tamanho_maximo=self._configuracao["tamanho_maximo"],
            numero_tipos=self._configuracao["numero_tipos"],
            numero_clientes=self._configuracao["numero_clientes"],
        )

        # 2. Inspeção de produtos
        produtos_inspecionados, estatisticas_inspecao = (
            self._modulo_inspecao.processar_lista_produtos(produtos)
        )

        # Registra inspeção tipo 1
        if estatisticas_inspecao["quantidade_tipo1"] > 0:
            self._modulo_monitoramento.registrar_inspecao(
                numero_produtos=self._configuracao["quantidade_produtos"],
                tipo=1,
                tempo_total=estatisticas_inspecao["tempo_total_tipo1"],
                quantidade=estatisticas_inspecao["quantidade_tipo1"],
            )

        # Registra inspeção tipo 2
        if estatisticas_inspecao["quantidade_tipo2"] > 0:
            self._modulo_monitoramento.registrar_inspecao(
                numero_produtos=self._configuracao["quantidade_produtos"],
                tipo=2,
                tempo_total=estatisticas_inspecao["tempo_total_tipo2"],
                quantidade=estatisticas_inspecao["quantidade_tipo2"],
            )

        # 3. Inserção no controle
        tempo_insercao, quantidade_inserida = (
            self._modulo_controle.receber_dados_inspecao(
                produtos_inspecionados
            )
        )
        self._modulo_monitoramento.registrar_controle_insercao(
            quantidade_inserida=quantidade_inserida,
            tempo_execucao=tempo_insercao,
        )

        # 4. Execução de buscas
        quantidade_buscas = int(
            len(produtos_inspecionados)
            * self._configuracao["percentual_buscas"]
            / 100
        )

        if quantidade_buscas > 0:
            consultas = self._gerador_dados.gerar_lista_buscas(
                quantidade=quantidade_buscas,
                produtos_inspecionados=produtos_inspecionados,
            )

            tempo_busca, total_buscas, quantidade_encontrada = (
                self._modulo_controle.executar_buscas(consultas)
            )
            self._modulo_monitoramento.registrar_controle_busca(
                quantidade_buscas=total_buscas,
                quantidade_encontrada=quantidade_encontrada,
                tempo_execucao=tempo_busca,
            )

    def resumo_final(self) -> Dict[str, Any]:
        """
        Retorna resumo completo da simulação.

        Entry:
            - None (usa dados registrados em monitoramento)

        Exit:
            - Dict[str, Any]: Dicionário com resumo contendo:
                * "configuracao": Dict com parâmetros de simulação
                * "resultados": Dict com:
                    - "inspecao_tipo1": Tempo total tipo 1
                    - "inspecao_tipo2": Tempo total tipo 2
                    - "insercoes": Informações de inserção
                    - "buscas": Informações de buscas

        Returns:
            Dict com resumo completo de execução
        """
        historico = self._modulo_monitoramento.historico

        # Calcula estatísticas de inspeção tipo 1
        tempo_tipo1 = 0
        quantidade_tipo1 = 0
        for registro in historico["inspecao_tipo1"]:
            tempo_tipo1 += registro["tempo_total"]
            quantidade_tipo1 += 1

        # Calcula estatísticas de inspeção tipo 2
        tempo_tipo2 = 0
        quantidade_tipo2 = 0
        for registro in historico["inspecao_tipo2"]:
            tempo_tipo2 += registro["tempo_total"]
            quantidade_tipo2 += 1

        # Calcula estatísticas de inserção
        tempo_insercao_total = 0.0
        quantidade_insercao_total = 0
        for registro in historico["controle_insercao"]:
            tempo_insercao_total += registro["tempo_execucao"]
            quantidade_insercao_total += registro["quantidade"]

        # Calcula estatísticas de busca
        tempo_busca_total = 0.0
        quantidade_buscas_total = 0
        quantidade_encontrada_total = 0
        for registro in historico["controle_busca"]:
            tempo_busca_total += registro["tempo_execucao"]
            quantidade_buscas_total += registro["quantidade_buscas"]
            quantidade_encontrada_total += registro["quantidade_encontrada"]

        resumo = {
            "configuracao": self._configuracao,
            "resultados": {
                "inspecao_tipo1": {
                    "tempo_total": tempo_tipo1,
                    "quantidade_registros": quantidade_tipo1,
                },
                "inspecao_tipo2": {
                    "tempo_total": tempo_tipo2,
                    "quantidade_registros": quantidade_tipo2,
                },
                "insercoes": {
                    "quantidade_total": quantidade_insercao_total,
                    "tempo_total": tempo_insercao_total,
                },
                "buscas": {
                    "quantidade_buscas": quantidade_buscas_total,
                    "quantidade_encontrada": quantidade_encontrada_total,
                    "tempo_total": tempo_busca_total,
                },
            },
        }

        return resumo
