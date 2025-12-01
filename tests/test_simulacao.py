"""
Testes unitários para simulacao.py - Usando funções simples
"""
import pytest
from src.controle_inteligente_ie.simulacao import SimuladorSistema


# ==================== Testes Init ====================

def test_simulador_init():
    """Inicializa simulador"""
    simulador = SimuladorSistema()
    assert simulador is not None


def test_simulador_init_modulos():
    """Inicializa com módulos necessários"""
    simulador = SimuladorSistema()
    assert simulador._gerador_dados is not None
    assert simulador._modulo_inspecao is not None
    assert simulador._modulo_controle is not None
    assert simulador._modulo_monitoramento is not None


# ==================== Testes Configurar Simulação ====================

def test_configurar_simulacao_completa():
    """Configura simulação com todos os parâmetros"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=5,
        tamanho_maximo=50,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=50,
        usar_random=True
    )
    assert simulador._configuracao["quantidade_produtos"] == 10


def test_configurar_simulacao_parametros_salvos():
    """Configuração salva todos os parâmetros"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=20,
        tamanho_minimo=10,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=10,
        percentual_buscas=80,
        usar_random=False
    )
    assert simulador._configuracao["quantidade_produtos"] == 20
    assert simulador._configuracao["tamanho_minimo"] == 10
    assert simulador._configuracao["percentual_buscas"] == 80


# ==================== Testes Executar Simulações ====================

def test_executar_simulacao_simples():
    """Executa simulação simples"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=5,
        tamanho_minimo=1,
        tamanho_maximo=20,
        numero_tipos=2,
        numero_clientes=3,
        percentual_buscas=50,
        usar_random=True
    )
    resultado = simulador.executar_simulacoes()
    assert resultado is None


def test_executar_simulacao_sem_config():
    """Executa simulação sem configurar lança erro"""
    simulador = SimuladorSistema()
    with pytest.raises(ValueError):
        simulador.executar_simulacoes()


def test_executar_simulacao_tipo1_only():
    """Executa simulação apenas com tipo 1"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=1,
        tamanho_maximo=20,
        numero_tipos=1,
        numero_clientes=5,
        percentual_buscas=50,
        usar_random=True
    )
    simulador.executar_simulacoes()
    assert simulador._configuracao["numero_tipos"] == 1


def test_executar_simulacao_sem_buscas():
    """Executa simulação com 0% de buscas"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=1,
        tamanho_maximo=20,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=0,
        usar_random=True
    )
    simulador.executar_simulacoes()
    assert simulador._configuracao["percentual_buscas"] == 0


def test_executar_simulacao_muitas_buscas():
    """Executa simulação com 100% de buscas"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=5,
        tamanho_minimo=1,
        tamanho_maximo=20,
        numero_tipos=2,
        numero_clientes=3,
        percentual_buscas=100,
        usar_random=True
    )
    simulador.executar_simulacoes()
    assert simulador._configuracao["percentual_buscas"] == 100


# ==================== Testes Resumo Final ====================

def test_resumo_final_estrutura():
    """Resumo final retorna estrutura correta"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=5,
        tamanho_maximo=50,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=50,
        usar_random=True
    )
    simulador.executar_simulacoes()
    resumo = simulador.resumo_final()
    
    assert isinstance(resumo, dict)
    assert "configuracao" in resumo
    assert "resultados" in resumo


def test_resumo_final_resultados():
    """Resumo final contém resultados esperados"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=5,
        tamanho_maximo=50,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=50,
        usar_random=True
    )
    simulador.executar_simulacoes()
    resumo = simulador.resumo_final()
    
    resultados = resumo["resultados"]
    assert "inspecao_tipo1" in resultados
    assert "inspecao_tipo2" in resultados
    assert "insercoes" in resultados
    assert "buscas" in resultados


def test_resumo_final_sem_execucao():
    """Resumo final sem execução retorna estrutura vazia"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=5,
        tamanho_maximo=50,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=50,
        usar_random=True
    )
    resumo = simulador.resumo_final()
    assert isinstance(resumo, dict)


# ==================== Testes Fluxo Completo ====================

def test_fluxo_completo_simulacao():
    """Fluxo completo de simulação"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=20,
        tamanho_minimo=10,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=10,
        percentual_buscas=50,
        usar_random=True
    )
    simulador.executar_simulacoes()
    resumo = simulador.resumo_final()
    
    assert "configuracao" in resumo
    assert "resultados" in resumo


def test_fluxo_multiplas_reexecucoes():
    """Fluxo com múltiplas reexecuções"""
    simulador = SimuladorSistema()
    
    # Primeira simulação
    simulador.configurar_simulacao(
        quantidade_produtos=5,
        tamanho_minimo=1,
        tamanho_maximo=20,
        numero_tipos=2,
        numero_clientes=3,
        percentual_buscas=50,
        usar_random=True
    )
    simulador.executar_simulacoes()
    res1 = simulador.resumo_final()
    
    # Segunda simulação com configuração diferente
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=5,
        tamanho_maximo=50,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=80,
        usar_random=True
    )
    simulador.executar_simulacoes()
    res2 = simulador.resumo_final()
    
    assert res1 is not None
    assert res2 is not None


# ==================== Testes Módulos Integrados ====================

def test_modulos_sao_criados():
    """Todos os módulos são criados"""
    simulador = SimuladorSistema()
    assert simulador._gerador_dados is not None
    assert simulador._modulo_inspecao is not None
    assert simulador._modulo_controle is not None
    assert simulador._modulo_monitoramento is not None


def test_modulos_independentes():
    """Simuladores diferentes têm módulos independentes"""
    sim1 = SimuladorSistema()
    sim2 = SimuladorSistema()
    
    assert sim1._gerador_dados is not sim2._gerador_dados
    assert sim1._modulo_controle is not sim2._modulo_controle


# ==================== Testes Com Diferentes Tamanhos ====================

def test_simulacao_quantidade_minima():
    """Simulação com quantidade mínima"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=1,
        tamanho_minimo=1,
        tamanho_maximo=10,
        numero_tipos=1,
        numero_clientes=1,
        percentual_buscas=0,
        usar_random=True
    )
    simulador.executar_simulacoes()
    assert True


def test_simulacao_quantidade_media():
    """Simulação com quantidade média"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=100,
        tamanho_minimo=10,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=10,
        percentual_buscas=50,
        usar_random=True
    )
    simulador.executar_simulacoes()
    assert True


def test_simulacao_quantidade_grande():
    """Simulação com quantidade grande"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=500,
        tamanho_minimo=1,
        tamanho_maximo=200,
        numero_tipos=2,
        numero_clientes=50,
        percentual_buscas=30,
        usar_random=True
    )
    simulador.executar_simulacoes()
    assert True


# ==================== Testes Configuração ====================

def test_config_tamanhos_validos():
    """Configuração com tamanhos válidos"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=5,
        tamanho_maximo=100,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=50,
        usar_random=True
    )
    assert simulador._configuracao["tamanho_minimo"] == 5
    assert simulador._configuracao["tamanho_maximo"] == 100


def test_config_percentual_valido():
    """Configuração com percentual válido"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=1,
        tamanho_maximo=20,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=75,
        usar_random=True
    )
    assert 0 <= simulador._configuracao["percentual_buscas"] <= 100


def test_config_tipo1_apenas():
    """Configuração com apenas tipo 1"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=1,
        tamanho_maximo=20,
        numero_tipos=1,
        numero_clientes=5,
        percentual_buscas=50,
        usar_random=False
    )
    assert simulador._configuracao["numero_tipos"] == 1


# ==================== Testes Dados Monitorados ====================

def test_monitoramento_registro_inspecao():
    """Monitoramento registra inspeção"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=5,
        tamanho_maximo=50,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=50,
        usar_random=True
    )
    simulador.executar_simulacoes()
    resumo = simulador.resumo_final()
    
    assert "inspecao_tipo1" in resumo["resultados"]
    assert "inspecao_tipo2" in resumo["resultados"]


def test_monitoramento_registro_controle():
    """Monitoramento registra controle"""
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=10,
        tamanho_minimo=5,
        tamanho_maximo=50,
        numero_tipos=2,
        numero_clientes=5,
        percentual_buscas=50,
        usar_random=True
    )
    simulador.executar_simulacoes()
    resumo = simulador.resumo_final()
    
    assert "insercoes" in resumo["resultados"]
    assert "buscas" in resumo["resultados"]
