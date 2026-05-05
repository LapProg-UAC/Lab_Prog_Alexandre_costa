import pytest
from sequencia import f

"python3 -m pytest sequencia_pytest.py -v"

@pytest.mark.parametrize("n, esperado", [
    (0, []),
    (1, [0]),
    (2, [0, 1]),
    (3, [0, 1, 1]),
    (8, [0, 1, 1, 4, 7, 19, 40, 97])
])
def test_f_calculo_correto(n, esperado):
    """
    Testa se a função retorna a lista correta para n válidos.
    :param n(int): entrada
    :param esperado(list): lista esperada
    :return: None
    """
    assert f(n) == esperado

@pytest.mark.parametrize("entrada_invalida", [
    -10, 2.5, "3", None, True, []
])
def test_f_excecoes(entrada_invalida):
    """
    Testa se a função levanta ValueError com a mensagem correta.
    :param entrada_invalida: diversos tipos
    :return: None
    """
    with pytest.raises(ValueError, match="n deve ser um número inteiro não negativo"):
        f(entrada_invalida)

def test_consistencia_prefixo():
    """
    Verifica se f(n) é sempre o início de f(n+1).
    :param: None
    :return: None
    """
    assert f(5) == f(6)[:5]