"""
Controle Inteligente de Estoque - Projeto Final IE

Sistema para controle de estoque implementando:
- Módulo de Inspeção: Tipo 1 (O(n)) e Tipo 2 (O(n²))
- Módulo de Controle: Hash table com encadeamento
- Módulo de Monitoramento: Gráficos de performance
"""

from .dados import GeradorDados
from .inspecao import ModuloInspecao
from .controle import ModuloControle
from .monitoramento import ModuloMonitoramento
from .simulacao import SimuladorSistema
from .modelos import Produto, ProdutoInspecionado, ConsultaProduto

__all__ = [
    "GeradorDados",
    "ModuloInspecao",
    "ModuloControle",
    "ModuloMonitoramento",
    "SimuladorSistema",
    "Produto",
    "ProdutoInspecionado",
    "ConsultaProduto",
]

__version__ = "1.0.0"
__author__ = "Controle Inteligente"
