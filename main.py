"""
Script principal - Executor da simulação.

Este módulo executa a simulação do sistema de controle inteligente de estoque
com configurações interativas fornecidas pelo usuário. Para usar com configurações
padrão, defina modo_interativo=False na função main().
"""

import sys
from pathlib import Path
from typing import List

# Adiciona src ao path para importações
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from controle_inteligente_ie import SimuladorSistema


def obter_entrada_inteira(mensagem: str, padrao: int) -> int:
    """
    Obtém uma entrada inteira do usuário com valor padrão.

    Entry:
        - mensagem: str (mensagem a exibir)
        - padrao: int (valor padrão)

    Exit:
        - int: Valor fornecido pelo usuário ou valor padrão

    Args:
        mensagem: Mensagem a exibir
        padrao: Valor padrão se usuário pressionar Enter

    Returns:
        Inteiro fornecido ou valor padrão
    """
    try:
        entrada = input(f"{mensagem} (padrão: {padrao}): ").strip()
        if entrada == "":
            return padrao
        return int(entrada)
    except ValueError:
        print(f"Entrada inválida. Usando valor padrão: {padrao}")
        return padrao


def obter_lista_inteiros(mensagem: str, padrao: str) -> List[int]:
    """
    Obtém uma lista de inteiros do usuário separados por vírgula.

    Entry:
        - mensagem: str (mensagem a exibir)
        - padrao: str (valores padrão separados por vírgula)

    Exit:
        - List[int]: Lista de inteiros fornecidos ou padrão

    Args:
        mensagem: Mensagem a exibir
        padrao: String com valores padrão separados por vírgula

    Returns:
        Lista de inteiros
    """
    try:
        entrada = input(f"{mensagem} (padrão: {padrao}): ").strip()
        if entrada == "":
            entrada = padrao

        # Converter string em lista de inteiros manualmente
        valores = []
        partes = entrada.split(",")
        for parte in partes:
            try:
                valor = int(parte.strip())
                valores.append(valor)
            except ValueError:
                continue

        if not valores:
            # Se nenhum valor válido, usar padrão
            partes_padrao = padrao.split(",")
            for parte in partes_padrao:
                try:
                    valor = int(parte.strip())
                    valores.append(valor)
                except ValueError:
                    continue

        return valores
    except Exception:
        # Se algo der errado, retornar valor padrão
        partes = padrao.split(",")
        valores = []
        for parte in partes:
            try:
                valor = int(parte.strip())
                valores.append(valor)
            except ValueError:
                continue
        return valores


def gerar_dados_interativo() -> None:
    """
    Executa a simulação em modo interativo.

    Entry:
        - None (obtém inputs do usuário via stdin)

    Exit:
        - None: Exibe resultados e gráficos opcionais
    """
    print("\n" + "=" * 60)
    print("SIMULADOR DE SISTEMA DE CONTROLE INTELIGENTE DE ESTOQUE")
    print("=" * 60 + "\n")

    print("Insira os parâmetros da simulação (pressione Enter para usar valor padrão):\n")

    # Obter quantidade de produtos
    quantidade = obter_entrada_inteira(
        "Quantidade de produtos", 100
    )

    # Obter tamanhos
    min_tamanho = obter_entrada_inteira("Tamanho mínimo de produto", 10)
    max_tamanho = obter_entrada_inteira("Tamanho máximo de produto", 1000)

    # Validar tamanhos
    if min_tamanho > max_tamanho:
        min_tamanho, max_tamanho = max_tamanho, min_tamanho
        print(f"Aviso: min e max foram invertidos. Novo intervalo: {min_tamanho} - {max_tamanho}")

    # Obter número de clientes
    num_clientes = obter_entrada_inteira("Número de clientes", 20)

    # Obter número de tipos de produto
    num_tipos = obter_entrada_inteira("Número de tipos de produto", 2)

    # Obter percentual de buscas
    percentual_buscas = obter_entrada_inteira("Percentual de buscas (0-100)", 50)

    print("\n" + "-" * 60)
    print("Configuração:")
    print(f"  Quantidade de produtos: {quantidade}")
    print(f"  Intervalo de tamanho: {min_tamanho} - {max_tamanho}")
    print(f"  Número de clientes: {num_clientes}")
    print(f"  Tipos de produto: {num_tipos}")
    print(f"  Percentual de buscas: {percentual_buscas}%")
    print("-" * 60 + "\n")

    # Executar simulação
    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=quantidade,
        tamanho_minimo=min_tamanho,
        tamanho_maximo=max_tamanho,
        numero_tipos=num_tipos,
        numero_clientes=num_clientes,
        percentual_buscas=percentual_buscas,
        usar_random=True,
    )

    print("Executando simulação...\n")
    simulador.executar_simulacoes()

    # Exibir resumo
    resumo = simulador.resumo_final()
    print("\n" + "=" * 60)
    print("RESUMO FINAL DA SIMULAÇÃO")
    print("=" * 60)

    configuracao = resumo.get("configuracao", {})
    resultados = resumo.get("resultados", {})

    print("\nConfigurações:")
    chaves_config = []
    for chave in configuracao:
        chaves_config.append(chave)

    for chave in chaves_config:
        print(f"  {chave}: {configuracao[chave]}")

    print("\nResultados:")

    # Inspeção tipo 1
    inspecao_tipo1 = resultados.get("inspecao_tipo1", {})
    print(f"\n  Inspeção Tipo 1:")
    print(f"    Tempo total: {inspecao_tipo1.get('tempo_total', 0)} ms")
    print(f"    Registros: {inspecao_tipo1.get('quantidade_registros', 0)}")

    # Inspeção tipo 2
    inspecao_tipo2 = resultados.get("inspecao_tipo2", {})
    print(f"\n  Inspeção Tipo 2:")
    print(f"    Tempo total: {inspecao_tipo2.get('tempo_total', 0)} ms")
    print(f"    Registros: {inspecao_tipo2.get('quantidade_registros', 0)}")

    # Inserções
    insercoes = resultados.get("insercoes", {})
    print(f"\n  Inserções:")
    print(f"    Quantidade: {insercoes.get('quantidade_total', 0)}")
    print(f"    Tempo total: {insercoes.get('tempo_total', 0):.4f} segundos")

    # Buscas
    buscas = resultados.get("buscas", {})
    print(f"\n  Buscas:")
    print(f"    Quantidade de buscas: {buscas.get('quantidade_buscas', 0)}")
    print(f"    Encontradas: {buscas.get('quantidade_encontrada', 0)}")
    print(f"    Tempo total: {buscas.get('tempo_total', 0):.4f} segundos")

    print("\n" + "=" * 60)
    print("Simulação concluída com sucesso!")
    print("=" * 60 + "\n")


def gerar_dados_padrao() -> None:
    """
    Executa a simulação com configurações padrão pré-definidas.

    Entry:
        - None

    Exit:
        - None: Exibe resultados da simulação padrão
    """
    print("Executando simulação com configurações padrão...\n")

    simulador = SimuladorSistema()
    simulador.configurar_simulacao(
        quantidade_produtos=100,
        tamanho_minimo=10,
        tamanho_maximo=1000,
        numero_clientes=20,
        numero_tipos=2,
        percentual_buscas=50,
        usar_random=True,
    )

    simulador.executar_simulacoes()

    resumo = simulador.resumo_final()
    print("\nResumo final da simulação:")

    configuracao = resumo.get("configuracao", {})
    resultados = resumo.get("resultados", {})

    print("\nConfigurações:")
    chaves_config = []
    for chave in configuracao:
        chaves_config.append(chave)

    for chave in chaves_config:
        print(f"  {chave}: {configuracao[chave]}")

    print("\nResultados:")
    chaves_resultado = []
    for chave in resultados:
        chaves_resultado.append(chave)

    for chave in chaves_resultado:
        valor = resultados[chave]
        print(f"  {chave}: {valor}")

    print("\nSimulação padrão concluída!\n")


def main() -> None:
    """
    Função principal que permite ao usuário escolher entre modo interativo
    ou usar configurações padrão.

    Entry:
        - None

    Exit:
        - None: Executa simulação (interativa ou padrão)
    """
    # Mudar para False se quiser modo não-interativo
    modo_interativo = True

    if modo_interativo:
        gerar_dados_interativo()
    else:
        gerar_dados_padrao()


if __name__ == "__main__":
    main()
