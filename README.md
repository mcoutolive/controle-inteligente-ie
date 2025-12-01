# Controle Inteligente de Estoque - Projeto Final IE

Sistema desenvolvido para controle inteligente de estoque, implementando estruturas de dados e algoritmos estudados em sala.

## Descrição

O projeto é organizado em três módulos principais:

- **Módulo de Inspeção**: Calcula tempo de inspeção para produtos (Tipo 1 e Tipo 2)
- **Módulo de Controle**: Gerencia inserção e busca de produtos usando tabela hash
- **Módulo de Monitoramento**: Acompanha performance com gráficos matplotlib

## Como Usar

### Menu Interativo

```bash
python main.py
```

Permite simular o sistema com parâmetros customizados e visualizar gráficos.

### Jupyter Notebook

```bash
jupyter notebook src/projeto_final_controle_estoque_ie.ipynb
```

Contém as 6 tarefas desenvolvidas:
1. Arquitetura geral do sistema
2. Gerador de dados e interface
3. Módulo de inspeção
4. Monitoramento da inspeção
5. Módulo de controle
6. Simulação completa

### Como Biblioteca

```python
from controle_inteligente_ie.simulacao import SimuladorSistema

sim = SimuladorSistema()
sim.configurar_simulacao(
    quantidade_produtos=100,
    tamanho_minimo=10,
    tamanho_maximo=500,
    numero_tipos=2,
    numero_clientes=5
)
sim.executar_simulacoes()
print(sim.resumo_final())
```

## Estrutura

```
src/
├── controle_inteligente_ie/
│   ├── modelos.py           # Classes de dados
│   ├── dados.py             # Gerador de produtos
│   ├── inspecao.py          # Algoritmos de inspeção
│   ├── controle.py          # Hash table para produtos
│   ├── monitoramento.py     # Gráficos de performance
│   └── simulacao.py         # Orquestração
└── projeto_final_controle_estoque_ie.ipynb  # 6 tarefas
```

## Requisitos

```
matplotlib>=3.5.0
```

Para instalar:

```bash
pip install -r requirements.txt
```

## Exemplos

### Exemplo 1: Tempo de Inspeção

```python
from controle_inteligente_ie.inspecao import ModuloInspecao

inspecao = ModuloInspecao()

# Tipo 1: T(n) = 2n - 1
t1 = inspecao._tempo_inspecao_tipo1(100)  # Retorna: 199 horas

# Tipo 2: T(n) = n(n+1)/2
t2 = inspecao._tempo_inspecao_tipo2(100)  # Retorna: 5050 horas
```

### Exemplo 2: Operações no Estoque

```python
from controle_inteligente_ie.controle import ModuloControle
from controle_inteligente_ie.dados import GeradorDados

gerador = GeradorDados()
produtos = gerador.gerar_lista_produtos(quantidade=100, tamanho_minimo=10, tamanho_maximo=500)

controle = ModuloControle()
tempo_insercao, qtd = controle.receber_dados_inspecao(produtos)

print(f"Tempo de inserção: {tempo_insercao:.4f}s")
```

### Exemplo 3: Visualizar Performance

```python
from controle_inteligente_ie.monitoramento import ModuloMonitoramento

mon = ModuloMonitoramento()

# Registrar alguns dados
mon.registrar_inspecao(numero_produtos=100, tipo=1, tempo_total=199, quantidade=50)
mon.registrar_inspecao(numero_produtos=100, tipo=2, tempo_total=5050, quantidade=50)

# Exibir gráficos
mon.plot_inspecao_tipo1()
mon.plot_inspecao_tipo2()
```

## Análise de Complexidade

| Operação | Complexidade |
|----------|-------------|
| Inspeção Tipo 1 | O(n) |
| Inspeção Tipo 2 | O(n²) |
| Inserção (hash) | O(1) médio |
| Busca (hash) | O(1) médio |
