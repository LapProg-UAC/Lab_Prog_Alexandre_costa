import doctest
from sequencia import f

"python3 -m doctest sequencia_doctest.py -v"

def teste_f_vazio():
    """
    n = 0 deve retornar uma lista vazia.
    :param: nenhum
    :return: validacao doctest
    
    >>> from sequencia import f
    >>> f(0)
    []
    """

def teste_f_um():
    """
    n = 1 deve retornar [0].
    :param: nenhum
    :return: validacao doctest

    >>> from sequencia import f
    >>> f(1)
    [0]
    """

def teste_f_recorrencia():
    """
    Teste da fórmula f(i) = 3*f(i-2) + f(i-1).
    n = 4: f(2)=3*0+1=1; f(3)=3*1+1=4.
    :param: nenhum
    :return: validacao doctest

    >>> from sequencia import f
    >>> f(4)
    [0, 1, 1, 4]
    """

def teste_f_erros():
    """
    Verifica se erros de valor e tipo lançam a exceção correta.
    :param: nenhum
    :return: validacao doctest

    >>> from sequencia import f
    >>> f(-1)
    Traceback (most recent call last):
        ...
    ValueError: n deve ser um número inteiro não negativo
    >>> f("5")
    Traceback (most recent call last):
        ...
    ValueError: n deve ser um número inteiro não negativo
    >>> f(True)
    Traceback (most recent call last):
        ...
    ValueError: n deve ser um número inteiro não negativo
    """

if __name__ == "__main__":
    # Executa os testes unitários via doctest
    resultados = doctest.testmod(verbose=True)
    print(f"Doctest: {resultados.attempted} testes realizados, {resultados.failed} falhas.")