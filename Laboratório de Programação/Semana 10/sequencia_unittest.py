import unittest
from sequencia import f

"python3 -m unittest sequencia_unittest.py -v"

class TesteSequencia(unittest.TestCase):
    """
    Classe de testes unitários usando a ferramenta unittest.
    :param: unittest.TestCase
    :return: suite de testes
    """

    def test_valores_validos(self):
        """Verifica resultados esperados para n de 0 a 5."""
        self.assertEqual(f(0), [])
        self.assertEqual(f(1), [0])
        self.assertEqual(f(2), [0, 1])
        self.assertEqual(f(3), [0, 1, 1])
        self.assertEqual(f(4), [0, 1, 1, 4])
        self.assertEqual(f(5), [0, 1, 1, 4, 7])

    def test_recorrencia_longa(self):
        """Verifica um valor mais alto da sequência."""
        # f(7) deve ser 97
        esperado = [0, 1, 1, 4, 7, 19, 40, 97]
        self.assertEqual(f(8), esperado)

    def test_entradas_invalidas(self):
        """Verifica se a função levanta ValueError para entradas proibidas."""
        entradas_erradas = [-1, 1.5, "texto", None, True, False, [1]]
        for entrada in entradas_erradas:
            with self.subTest(entrada=entrada):
                with self.assertRaises(ValueError) as erro:
                    f(entrada)
                self.assertEqual(str(erro.exception), "n deve ser um número inteiro não negativo")

if __name__ == "__main__":
    # Executa os testes e detalha os resultados
    unittest.main(verbosity=2)