"""
Testes unitários para monitoramento.py - Usando funções simples
"""
import pytest
import time
from unittest.mock import patch, MagicMock
from src.controle_inteligente_ie.monitoramento import ModuloMonitoramento


# ==================== Testes Inicialização ====================

def test_monitoramento_init():
    """Inicializa módulo com históricos vazios"""
    monitor = ModuloMonitoramento()
    assert monitor._historico_inspecao_tipo1 == []
    assert monitor._historico_inspecao_tipo2 == []
    assert monitor._historico_controle_insercao == []
    assert monitor._historico_controle_busca == []


# ==================== Testes Registrar Inspeção ====================

def test_registrar_inspecao_tipo1():
    """Registra inspeção tipo 1"""
    monitor = ModuloMonitoramento()
    monitor.registrar_inspecao(10, 1, 100, 5)
    assert len(monitor._historico_inspecao_tipo1) == 1
    assert monitor._historico_inspecao_tipo1[0]["numero_produtos"] == 10


def test_registrar_inspecao_tipo2():
    """Registra inspeção tipo 2"""
    monitor = ModuloMonitoramento()
    monitor.registrar_inspecao(20, 2, 200, 10)
    assert len(monitor._historico_inspecao_tipo2) == 1
    assert monitor._historico_inspecao_tipo2[0]["numero_produtos"] == 20


def test_registrar_inspecao_timestamp():
    """Registra timestamp válido"""
    monitor = ModuloMonitoramento()
    antes = time.time()
    monitor.registrar_inspecao(10, 1, 100, 5)
    depois = time.time()
    ts = monitor._historico_inspecao_tipo1[0]["timestamp"]
    assert antes <= ts <= depois


def test_registrar_multiplas_inspecoes():
    """Registra múltiplas inspeções"""
    monitor = ModuloMonitoramento()
    for i in range(5):
        monitor.registrar_inspecao(10, 1, 100, 5)
    assert len(monitor._historico_inspecao_tipo1) == 5


# ==================== Testes Registrar Controle Inserção ====================

def test_registrar_controle_insercao():
    """Registra inserção no controle"""
    monitor = ModuloMonitoramento()
    monitor.registrar_controle_insercao(50, 0.5)
    assert len(monitor._historico_controle_insercao) == 1
    assert monitor._historico_controle_insercao[0]["quantidade"] == 50


def test_registrar_insercao_tempo_zero():
    """Registra inserção com tempo zero"""
    monitor = ModuloMonitoramento()
    monitor.registrar_controle_insercao(10, 0.0)
    assert monitor._historico_controle_insercao[0]["tempo_execucao"] == 0.0


def test_registrar_multiplas_insercoes():
    """Registra múltiplas inserções"""
    monitor = ModuloMonitoramento()
    for i in range(3):
        monitor.registrar_controle_insercao(10 * i, 0.1 * i)
    assert len(monitor._historico_controle_insercao) == 3


# ==================== Testes Registrar Controle Busca ====================

def test_registrar_controle_busca():
    """Registra busca no controle"""
    monitor = ModuloMonitoramento()
    monitor.registrar_controle_busca(100, 80, 0.8)
    assert len(monitor._historico_controle_busca) == 1
    assert monitor._historico_controle_busca[0]["quantidade_buscas"] == 100


def test_registrar_busca_nenhum_encontrado():
    """Registra busca sem encontrados"""
    monitor = ModuloMonitoramento()
    monitor.registrar_controle_busca(50, 0, 0.1)
    assert monitor._historico_controle_busca[0]["quantidade_encontrada"] == 0


def test_registrar_multiplas_buscas():
    """Registra múltiplas buscas"""
    monitor = ModuloMonitoramento()
    for i in range(4):
        monitor.registrar_controle_busca(50, 40, 0.2)
    assert len(monitor._historico_controle_busca) == 4


# ==================== Testes Propriedade Histórico ====================

def test_historico_vazio():
    """Retorna histórico vazio"""
    monitor = ModuloMonitoramento()
    historico = monitor.historico
    assert historico["inspecao_tipo1"] == []
    assert historico["inspecao_tipo2"] == []


def test_historico_com_dados():
    """Retorna histórico com dados"""
    monitor = ModuloMonitoramento()
    monitor.registrar_inspecao(10, 1, 100, 5)
    monitor.registrar_inspecao(20, 2, 200, 10)
    monitor.registrar_controle_insercao(50, 0.5)
    monitor.registrar_controle_busca(100, 80, 0.8)
    
    historico = monitor.historico
    assert len(historico["inspecao_tipo1"]) == 1
    assert len(historico["inspecao_tipo2"]) == 1
    assert len(historico["controle_insercao"]) == 1
    assert len(historico["controle_busca"]) == 1


def test_historico_retorna_copia():
    """Histórico retorna cópias"""
    monitor = ModuloMonitoramento()
    monitor.registrar_inspecao(10, 1, 100, 5)
    h1 = monitor.historico
    h2 = monitor.historico
    assert h1 is not h2
    assert h1["inspecao_tipo1"] is not h2["inspecao_tipo1"]


# ==================== Testes Plot Inspeção Tipo 1 ====================

@patch('matplotlib.pyplot.figure')
@patch('matplotlib.pyplot.plot')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.grid')
@patch('matplotlib.pyplot.show')
def test_plot_inspecao_tipo1_com_dados(mock_show, mock_grid, mock_legend, mock_title,
                                       mock_ylabel, mock_xlabel, mock_plot, mock_figure):
    """Plot tipo 1 com dados"""
    monitor = ModuloMonitoramento()
    monitor.registrar_inspecao(10, 1, 100, 5)
    monitor.registrar_inspecao(20, 1, 200, 10)
    monitor.plot_inspecao_tipo1()
    
    mock_figure.assert_called_once_with(figsize=(10, 6))
    mock_plot.assert_called_once()
    mock_show.assert_called_once()


def test_plot_inspecao_tipo1_sem_dados(capsys):
    """Plot tipo 1 sem dados imprime mensagem"""
    monitor = ModuloMonitoramento()
    monitor.plot_inspecao_tipo1()
    captured = capsys.readouterr()
    assert "Nenhum dado de inspeção tipo 1 para visualizar" in captured.out


# ==================== Testes Plot Inspeção Tipo 2 ====================

@patch('matplotlib.pyplot.figure')
@patch('matplotlib.pyplot.plot')
@patch('matplotlib.pyplot.xlabel')
@patch('matplotlib.pyplot.ylabel')
@patch('matplotlib.pyplot.title')
@patch('matplotlib.pyplot.legend')
@patch('matplotlib.pyplot.grid')
@patch('matplotlib.pyplot.show')
def test_plot_inspecao_tipo2_com_dados(mock_show, mock_grid, mock_legend, mock_title,
                                       mock_ylabel, mock_xlabel, mock_plot, mock_figure):
    """Plot tipo 2 com dados"""
    monitor = ModuloMonitoramento()
    monitor.registrar_inspecao(10, 2, 100, 5)
    monitor.plot_inspecao_tipo2()
    
    mock_figure.assert_called_once()
    mock_plot.assert_called_once()
    mock_show.assert_called_once()


def test_plot_inspecao_tipo2_sem_dados(capsys):
    """Plot tipo 2 sem dados imprime mensagem"""
    monitor = ModuloMonitoramento()
    monitor.plot_inspecao_tipo2()
    captured = capsys.readouterr()
    assert "Nenhum dado de inspeção tipo 2 para visualizar" in captured.out


# ==================== Testes Plot Controle ====================

@patch('matplotlib.pyplot.subplots')
@patch('matplotlib.pyplot.tight_layout')
@patch('matplotlib.pyplot.show')
def test_plot_controle_com_dados(mock_show, mock_tight_layout, mock_subplots):
    """Plot controle com dados"""
    mock_ax1 = MagicMock()
    mock_ax2 = MagicMock()
    mock_fig = MagicMock()
    mock_subplots.return_value = (mock_fig, [mock_ax1, mock_ax2])
    
    monitor = ModuloMonitoramento()
    monitor.registrar_controle_insercao(50, 0.5)
    monitor.registrar_controle_busca(100, 80, 0.8)
    monitor.plot_controle()
    
    mock_subplots.assert_called_once()
    mock_show.assert_called_once()


def test_plot_controle_sem_dados(capsys):
    """Plot controle sem dados imprime mensagem"""
    monitor = ModuloMonitoramento()
    monitor.plot_controle()
    captured = capsys.readouterr()
    assert "Nenhum dado de controle para visualizar" in captured.out


# ==================== Testes Integração ====================

def test_fluxo_completo_monitoramento():
    """Fluxo completo de monitoramento"""
    monitor = ModuloMonitoramento()
    
    monitor.registrar_inspecao(10, 1, 100, 5)
    monitor.registrar_inspecao(20, 2, 200, 10)
    monitor.registrar_controle_insercao(50, 0.5)
    monitor.registrar_controle_busca(100, 80, 0.8)
    
    historico = monitor.historico
    assert len(historico["inspecao_tipo1"]) == 1
    assert len(historico["inspecao_tipo2"]) == 1
    assert len(historico["controle_insercao"]) == 1
    assert len(historico["controle_busca"]) == 1
