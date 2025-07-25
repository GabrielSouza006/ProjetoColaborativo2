# Lista contendo os produtos disponíveis: [ID, Nome, Preço (R$), Estoque]
produtos = [
    [1, "Coca-cola", 3.75, 2],
    [2, "Pepsi", 3.67, 5],
    [3, "Monster", 9.96, 1],
    [4, "Café", 1.25, 100],
    [5, "Redbull", 13.99, 2]
]

# Lista de valores de cédulas e moedas em centavos (ordem decrescente)
cedulas_moedas = [10000, 5000, 2000, 1000, 500, 200, 100, 50, 25, 10, 5, 1]

# Dicionário representando o estoque de cada cédula/moeda disponível
estoque_cedulas = {
    10000: 2, 5000: 2, 2000: 5, 1000: 10, 500: 10, 200: 20,
    100: 50, 50: 50, 25: 100, 10: 100, 5: 100, 1: 100
}

# Função para verificar se uma string representa um número inteiro
def is_int(valor):
    return valor.isdigit()

# Função para verificar se uma string representa um número decimal (float)
def is_float(valor):
    valor = valor.replace(",", ".")          # Substitui vírgula por ponto decimal
    partes = valor.split(".")                # Divide a string em partes
    if len(partes) > 2:                      # Se houver mais de um ponto, é inválido
        return False
    return all(p.isdigit() for p in partes if p)  # Verifica se todas as partes são numéricas

# Função que imprime a lista de produtos no terminal
def mostrar_produtos():
    print("\nProdutos disponíveis:")
    print("ID | Produto     | Preço   | Estoque")
    for p in produtos:
        print(f"{p[0]:<2} | {p[1]:<11} | R$ {p[2]:<6.2f} | {p[3]}")

# Função para localizar um produto pelo seu ID
def encontrar_produto(id_produto):
    for p in produtos:
        if p[0] == id_produto:
            return p                            # Retorna o produto se encontrado
    return None                                 # Caso contrário, retorna None

# Função que calcula o troco possível com base no estoque de cédulas/moedas
def calcular_troco_com_estoque(valor_troco):
    troco = {}                                   # Dicionário para armazenar o troco calculado
    valor_centavos = int(round(valor_troco * 100))  # Converte valor para centavos
    temp_estoque = estoque_cedulas.copy()        # Faz uma cópia do estoque original
    for valor in cedulas_moedas:
        qtd = min(valor_centavos // valor, temp_estoque[valor])  # Calcula a quantidade possível
        if qtd > 0:
            troco[valor] = qtd                   # Registra a quantidade dessa cédula/moeda
            temp_estoque[valor] -= qtd           # Atualiza estoque temporário
            valor_centavos -= qtd * valor        # Subtrai o valor já coberto
    if valor_centavos == 0:
        return troco                             # Troco possível
    else:
        return None                              # Impossível fornecer troco exato

# Função que imprime o troco em formato legível (com nomes das cédulas/moedas)
def exibir_troco(troco):
    nomes = {
        10000: "nota de R$ 100,00",
        5000: "nota de R$ 50,00",
        2000: "nota de R$ 20,00",
        1000: "nota de R$ 10,00",
        500: "nota de R$ 5,00",
        200: "nota de R$ 2,00",
        100: "moeda de R$ 1,00",
        50: "moeda de 50 centavos",
        25: "moeda de 25 centavos",
        10: "moeda de 10 centavos",
        5: "moeda de 5 centavos",
        1: "moeda de 1 centavo"
    }
    print("Troco:")
    for valor, qtd in troco.items():
        print(f"{qtd} {nomes[valor]}")

# Modo de administração da máquina (com senha "admin")
def modo_admin():
    while True:
        print("\n--- Modo Administrador ---")
        print("1. Cadastrar produto")
        print("2. Editar produto")
        print("3. Remover produto")
        print("4. Listar produtos")
        print("0. Sair do modo admin")
        op = input("Escolha uma opção: ")

        if op == "1":  # Cadastro de novo produto
            novo_id = input("ID do novo produto: ")
            if not is_int(novo_id):
                print("ID inválido.")
                continue
            novo_id = int(novo_id)
            nome = input("Nome: ")
            preco = input("Preço: ").replace(",", ".")
            if not is_float(preco):
                print("Preço inválido.")
                continue
            preco = float(preco)
            estoque = input("Estoque: ")
            if not is_int(estoque):
                print("Estoque inválido.")
                continue
            estoque = int(estoque)
            produtos.append([novo_id, nome, preco, estoque])
            print("Produto cadastrado.")

        elif op == "2":  # Edição de produto
            id_edit = input("ID do produto para editar: ")
            if not is_int(id_edit):
                print("ID inválido.")
                continue
            id_edit = int(id_edit)
            prod = encontrar_produto(id_edit)
            if prod:
                nome = input(f"Novo nome ({prod[1]}): ")
                if nome:
                    prod[1] = nome
                preco = input(f"Novo preço ({prod[2]}): ").replace(",", ".")
                if preco and is_float(preco):
                    prod[2] = float(preco)
                estoque = input(f"Novo estoque ({prod[3]}): ")
                if estoque and is_int(estoque):
                    prod[3] = int(estoque)
                print("Produto editado.")
            else:
                print("Produto não encontrado.")

        elif op == "3":  # Remoção de produto
            id_remover = input("ID do produto para remover: ")
            if not is_int(id_remover):
                print("ID inválido.")
                continue
            id_remover = int(id_remover)
            prod = encontrar_produto(id_remover)
            if prod:
                produtos.remove(prod)
                print("Produto removido.")
            else:
                print("Produto não encontrado.")

        elif op == "4":  # Listagem de produtos
            mostrar_produtos()

        elif op == "0":  # Sair do modo administrador
            break

        else:
            print("Opção inválida.")

# Função principal de interação com o usuário para compra
def vender():
    while True:
        print("\nDigite 'admin' para modo administrador.")
        mostrar_produtos()
        escolha = input("\nDigite o ID da bebida desejada (0 para sair): ")

        if escolha.lower() == "admin":  # Acesso ao modo admin
            modo_admin()
            continue

        if not is_int(escolha):  # Validação de entrada
            print("Entrada inválida. Tente novamente.")
            continue
        escolha = int(escolha)

        if escolha == 0:  # Encerrar programa
            print("Obrigado por utilizar a máquina!")
            break

        produto = encontrar_produto(escolha)  # Busca produto pelo ID
        if not produto:
            print("Produto não encontrado.")
            continue

        if produto[3] <= 0:  # Verifica estoque do produto
            print("Produto sem estoque.")
            continue

        print(f"Você escolheu {produto[1]} - R$ {produto[2]:.2f}")

        while True:  # Loop até o valor pago ser válido e suficiente
            valor_pago_str = input("Insira o valor pago (em reais): ").replace(",", ".")
            if not is_float(valor_pago_str):
                print("Valor inválido. Tente novamente.")
                continue
            valor_pago = float(valor_pago_str)
            if valor_pago < produto[2]:
                print("Valor insuficiente. Insira um valor igual ou maior ao preço do produto.")
            else:
                break

        troco = valor_pago - produto[2]  # Calcula o troco necessário

        if troco > 0:
            troco_dict = calcular_troco_com_estoque(troco)  # Tenta calcular troco
            if troco_dict is None:
                print("Não é possível fornecer o troco com as notas/moedas disponíveis. Compra cancelada.")
                continue
            else:
                exibir_troco(troco_dict)  # Mostra troco ao usuário
                for valor, qtd in troco_dict.items():  # Atualiza estoque de cédulas
                    estoque_cedulas[valor] -= qtd
        else:
            print("Sem troco.")

        produto[3] -= 1  # Reduz uma unidade do estoque do produto
        print(f"Retire sua {produto[1]}. Obrigado pela compra!\n")

# Executa o programa principal se o script for executado diretamente
if __name__ == "__main__":
    vender()