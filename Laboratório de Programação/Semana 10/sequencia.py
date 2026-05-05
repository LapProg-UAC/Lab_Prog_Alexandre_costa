def f(n):
    """
    Calcula uma sequência numérica baseada em uma relação de recorrência.
    
    :param n (int): O número de elementos a gerar na sequência.
    :return (list): Uma lista contendo os n elementos da sequência.
    """
    # Validação rigorosa do tipo de dado e valor de entrada
    # Booleans em Python são subclasses de int, por isso a verificação explícita
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n deve ser um número inteiro não negativo")
    
    if n < 0:
        raise ValueError("n deve ser um número inteiro não negativo")

    # Casos base para o tamanho da lista
    if n == 0:
        return []
    if n == 1:
        return [0]
    
    # Inicialização da sequência com f(0)=0 e f(1)=1
    sequencia = [0, 1]
    
    # Cálculo dos termos i >= 2 usando a fórmula f(i) = 3*f(i-2) + f(i-1)
    for i in range(2, n):
        termo_atual = 3 * sequencia[i - 2] + sequencia[i - 1]
        sequencia.append(termo_atual)
        
    return sequencia

def executar_interface():
    """
    Executa a interface de interação com o utilizador para testar a função f(n).
    """
    print("Gerador de Sequência (f(i) = 3*f(i-2) + f(i-1))")
    while True:
        entrada_utilizador = input("\nInsira n (ou 'sair'): ")
        
        if entrada_utilizador.lower() == 'sair':
            break
            
        try:
            # Tenta converter a entrada e calcular a sequência
            valor_n = int(entrada_utilizador)
            resultado = f(valor_n)
            print(f"Sequência gerada: {resultado}")
            
        except ValueError as erro:
            # Captura erros de validação e de conversão de tipo
            print(f"Erro de entrada: {erro}")

if __name__ == "__main__":
    executar_interface()