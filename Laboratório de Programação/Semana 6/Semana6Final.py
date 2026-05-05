import random

"""
Sistema de Hashing por Folding e Autenticacao.
Este script permite cifrar mensagens ou ficheiros utilizando 
o metodo de folding e uma chave secreta.
"""

def folding_hash(phrase, block_size=4):
    """
    Calcula o hash base de uma string utilizando o metodo de folding.
    Divide o texto em colunas e soma os valores ASCII.
    """
    ascii_chars = []
    
    for c in phrase:
        ascii_chars.append(ord(c))
    
    while len(ascii_chars) % block_size != 0:
        ascii_chars.append(ord(str(block_size)))
    
    column_sums = [0] * block_size

    for i, value in enumerate(ascii_chars):
        target_column = i % block_size
        column_sums[target_column] += value
            
    hex_list = []
    for s in column_sums:
        remainder = s % 256
        hex_list.append(remainder)

    return hex_list

def key_encryption(hex_list, key):
    """
    Adiciona a chave secreta aos valores e converte para hexadecimal.
    """
    encrypted_hex_list = []
    
    for i in range(len(hex_list)):
        encrypted_value = (hex_list[i] + key[i]) % 256
        hex_val = format(encrypted_value, '02X')
        encrypted_hex_list.append(hex_val)
    return encrypted_hex_list

def processar_ficheiro(input_file, output_file, key):
    """
    Le um ficheiro e guarda a assinatura num novo documento.
    """
    try:
        with open(input_file, 'r') as f:
            conteudo = f.read()
        
        hash_decimal = folding_hash(conteudo, 4)
        hex_list_doc = key_encryption(hash_decimal, key)

        
        with open(output_file, 'w') as f:
            f.write("Chave utilizada: " + str(key))
            f.write("\nLista Hexadecimal final: " + str(hex_list_doc))
            
        print("\nSucesso! Resultado guardado em: ", output_file)
        
    except FileNotFoundError:
        print("\nErro: Ficheiro nao encontrado.")

choice = input("Deseja encriptar uma string ou ficheiro (s/f): ").lower().strip()

if choice == "s":
    try:
        foldingtext = input("\nEscreva uma mensagem para encriptar: ")
        key_hex_list = folding_hash(foldingtext, 4)

        key = []
        print("\n")
        for i in range(len(key_hex_list)):
            keyinput = int(input(f"Digite o valor da chave {i+1} (0-255): "))
            key.append(keyinput)

        final_result = key_encryption(key_hex_list, key)
        print("\nLista Hexadecimal final: ", final_result)

    except Exception as e:
        print("\nOcorreu um erro: " + str(e))
        
elif choice == "f":
    try:
        filename = input("\nEscreva o nome do ficheiro (ex: doc.txt): ")
        
        key = []
        for i in range(4):
            key.append(random.randint(0, 255))
            
        processar_ficheiro(filename, "output.txt", key)
        
    except Exception as e:
        print("\nOcorreu um erro:", e)