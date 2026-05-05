#!/usr/bin/python
"""
Deteção de erros com um bit de paridade
----------------------------------------
1. Gera k números inteiros pseudo-aleatórios (50 < k < 65), cada um < 128.
2. Calcula o bit de paridade par de cada número e guarda ambos em ficheiros.
3. Cria uma cópia dos inteiros e altera um único bit em vários deles.
4. Recalcula os bits de paridade e compara com os originais para detetar erros.
"""

import random
from datetime import datetime

random.seed(datetime.now().timestamp())


# ── Configuração ────────────────────────────────────────────────────────────

FICHEIRO_INTEIROS = "inteiros_gerados.txt"
FICHEIRO_PARIDADE = "paridade_original.txt"
FICHEIRO_ALTERADOS = "inteiros_alterados.txt"
FICHEIRO_PAR_ALTER = "paridade_alterada.txt"


# ── Funções auxiliares ───────────────────────────────────────────────────────


def gerar_bit_paridade(n: int) -> int:
    """
    Calcula o bit de paridade par de um inteiro não-negativo usando XOR.
    :param n(int): inteiro não-negativo
    :return int: paridade (0 se o número de bits 1 for par, 1 se for ímpar)
    """
    paridade = 0
    while n:
        paridade ^= n & 1
        n >>= 1
    return paridade


def alterar_bit_aleatorio(n: int, num_bits: int = 7) -> int:
    """
    Altera um único bit aleatório (posições 0..num_bits-1) do inteiro n.
    :param n: inteiro a alterar
    :param num_bits: número de bits a considerar (default 7 para 0..127)
    :return int: inteiro resultante com um bit alterado
    """
    posicao = random.randint(0, num_bits - 1)
    return n ^ (1 << posicao)


# ── Passo 1 – Geração dos números aleatórios ─────────────────────────────────


def gerar_k() -> int:
    """
    Gera um número aleatório k entre 51 e 64 (inclusive).
    :return int: número de inteiros a gerar
    """
    return random.randint(51, 64)


def gerar_int_aleatorio(known) -> int:
    """
    Gera um numero aleatorio, verificando se o mesmo ja tinha sido gerado
    :param known: set de numeros aleatorios ja gerados
    :return int: valor gerado
    """
    while True:
        val = random.randint(0, 127)
        if val in known:
            continue
        known.add(val)
        return val


def gerar_inteiros(k: int) -> list[int]:
    """
    Gera uma lista de k inteiros aleatórios entre 0 e 127 (inclusive)
    e guarda-os em ficheiro.
    :param k: número de inteiros a gerar
    :return list: lista de k inteiros aleatórios entre 0 e 127
    """
    vistos = set()
    inteiros = [gerar_int_aleatorio(vistos) for _ in range(k)]
    with open(FICHEIRO_INTEIROS, "w") as f:
        f.writelines(f"{n}\n" for n in inteiros)
    print(f"{k} inteiros gerados (0 a 127) e guardados em '{FICHEIRO_INTEIROS}'.")
    return inteiros


# ── Passo 2 – Calcular e guardar os bits de paridade originais ───────────────


def guardar_paridades_originais(inteiros: list[int]) -> list[int]:
    """
    Calcula os bits de paridade par dos inteiros e guarda-os em ficheiro.
    :param inteiros: lista de inteiros
    :return list: lista de bits de paridade correspondentes
    """
    paridades_originais = [gerar_bit_paridade(n) for n in inteiros]
    with open(FICHEIRO_PARIDADE, "w") as f:
        f.writelines(f"{p}\n" for p in paridades_originais)
    print(f"Bits de paridade originais guardados em '{FICHEIRO_PARIDADE}'.")
    return paridades_originais


# ── Passo 3 – Criar cópia com bits alterados em vários números ───────────────


def alterar_inteiros(inteiros: list[int]) -> tuple[list[int], list[int]]:
    """
    Cria uma cópia da lista de inteiros e altera um único bit em vários deles.
    :param inteiros: lista de inteiros original
    :param k: número total de inteiros
    :return tuple: (lista alterada, lista de índices alterados)
    """
    alterados = [v for v in inteiros]
    n_alterados = 0
    indices_alterados = []

    for idx, val in enumerate(alterados):
        # probabilidade de 20% de alterarmos o bit
        if random.random() <= 0.2:
            alterados[idx] = alterar_bit_aleatorio(val)
            indices_alterados.append(idx)
            n_alterados += 1

    with open(FICHEIRO_ALTERADOS, "w") as f:
        f.writelines(f"{n}\n" for n in alterados)

    print(
        f"\n{n_alterados} números tiveram um bit alterado "
        f"(índices: {indices_alterados})."
    )
    print(f"Inteiros alterados guardados em '{FICHEIRO_ALTERADOS}'.")
    return alterados, indices_alterados


# ── Passo 4 – Recalcular paridades dos inteiros alterados ────────────────────


def guardar_paridades_alteradas(inteiros_alterados: list[int]) -> list[int]:
    """
    Calcula os bits de paridade dos inteiros alterados e guarda-os em ficheiro.
    :param inteiros_alterados: lista de inteiros com bits alterados
    :return list: lista de bits de paridade correspondentes
    """
    paridades_alteradas = [gerar_bit_paridade(n) for n in inteiros_alterados]
    with open(FICHEIRO_PAR_ALTER, "w") as f:
        f.writelines(f"{p}\n" for p in paridades_alteradas)
    print(f"Bits de paridade alterados guardados em '{FICHEIRO_PAR_ALTER}'.")
    return paridades_alteradas


# ── Passo 5 – Deteção dos erros por comparação ───────────────────────────────


def detetar_erros(
    inteiros: list[int],
    inteiros_alterados: list[int],
    paridades_originais: list[int],
    paridades_alteradas: list[int],
    indices_alterados: list[int],
) -> list[int]:
    """
    Compara os bits de paridade originais e alterados para detetar erros.
    :param inteiros: lista de inteiros original
    :param inteiros_alterados: lista de inteiros com bits alterados
    :param paridades_originais: lista de bits de paridade originais
    :param paridades_alteradas: lista de bits de paridade recalculados
    :param indices_alterados: índices onde os bits foram efetivamente alterados
    :return list: lista de índices onde foram detetados erros
    """
    print("\n── Resultados da deteção de erros ─────────────────────────────────────")
    print(
        f"{'Índice':>7}  {'Original':>9}  {'Alterado':>9}  "
        f"{'Par.Orig':>9}  {'Par.Alt':>8}  {'Erro':>5}"
    )
    print("-" * 60)

    erros_detetados = []
    for idx, (orig, alt, p_orig, p_alt) in enumerate(
        zip(inteiros, inteiros_alterados, paridades_originais, paridades_alteradas)
    ):
        if p_orig != p_alt:
            erros_detetados.append(idx)
            marcador = "\x1b[1;31m  <--\x1b[0m"
        else:
            marcador = ""
        print(
            f"{idx:>7}  {orig:>9}  {alt:>9}  "
            f"{p_orig:>9}  {p_alt:>8}  {str(p_orig != p_alt):>5}{marcador}"
        )

    print("-" * 60)
    print(
        f"\nErros detetados em {len(erros_detetados)} número(s), "
        f"nos índices: {erros_detetados}"
    )
    print(f"(Números efetivamente alterados nos índices: {sorted(indices_alterados)})")

    nao_detetados = set(indices_alterados) - set(erros_detetados)
    if nao_detetados:
        print(
            f"\nATENÇÃO: {len(nao_detetados)} alteração(ões) NÃO detetada(s) "
            f"(bit de paridade coincidiu por acaso): índices {sorted(nao_detetados)}"
        )
    else:
        print("\nTodas as alterações foram corretamente detetadas.")

    return erros_detetados


# ── Programa principal ───────────────────────────────────────────────────────

_k = gerar_k()
_inteiros = gerar_inteiros(_k)
_paridades_originais = guardar_paridades_originais(_inteiros)
_inteiros_alterados, _indices_alterados = alterar_inteiros(_inteiros)
_paridades_alteradas = guardar_paridades_alteradas(_inteiros_alterados)
_erros_detetados = detetar_erros(
    _inteiros,
    _inteiros_alterados,
    _paridades_originais,
    _paridades_alteradas,
    _indices_alterados,
)
