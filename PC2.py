produtos = [
    [1, "Coca-cola", 3.75, 2],
    [2, "Pepsi", 3.67, 5],
    [3, "Monster", 9.96, 1],
    [4, "Café", 1.25, 100],
    [5, "Redbull", 13.99, 2]
]
cedulas_moedas = [10000, 5000, 2000, 1000, 500, 200, 100, 50, 25, 10, 5, 1]
estoque_cedulas = {
    10000: 2, 5000: 2, 2000: 5, 1000: 10, 500: 10, 200: 20,
    100: 50, 50: 50, 25: 100, 10: 100, 5: 100, 1: 100
}

def is_int(valor):
    return valor.isdigit()

def is_float(valor):
    valor = valor.replace(",", ".")
    partes = valor.split(".")
    if len(partes) > 2:
        return False
    return all(p.isdigit() for p in partes if p)

def mostrar_produtos():
    print("\nProdutos disponíveis:")
    print("ID | Produto     | Preço   | Estoque")
    for p in produtos:
        print(f"{p[0]:<2} | {p[1]:<11} | R$ {p[2]:<6.2f} | {p[3]}")

def encontrar_produto(id_produto):
    for p in produtos:
        if p[0] == id_produto:
            return p
    return None

def calcular_troco_com_estoque(valor_troco):
    troco = {}
    valor_centavos = int(round(valor_troco * 100))
    temp_estoque = estoque_cedulas.copy()
    for valor in cedulas_moedas:
        qtd = min(valor_centavos // valor, temp_estoque[valor])
        if qtd > 0:
            troco[valor] = qtd
            temp_estoque[valor] -= qtd
            valor_centavos -= qtd * valor
    if valor_centavos == 0:
        return troco
    else:
        return None  # Não é possível dar o troco

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

def modo_admin():
    senha = input("Digite a senha de administrador: ")
    if senha != "admin":
        print("Senha incorreta.")
        return
    while True:
        print("\n--- Modo Administrador ---")
        print("1. Cadastrar produto")
        print("2. Editar produto")
        print("3. Remover produto")
        print("4. Listar produtos")
        print("0. Sair do modo admin")
        op = input("Escolha uma opção: ")
        if op == "1":
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
        elif op == "2":
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
        elif op == "3":
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
        elif op == "4":
            mostrar_produtos()
        elif op == "0":
            break
        else:
            print("Opção inválida.")

def vender():
    while True:
        print("\nDigite 'admin' para modo administrador.")
        mostrar_produtos()
        escolha = input("\nDigite o ID da bebida desejada (0 para sair): ")
        if escolha.lower() == "admin":
            modo_admin()
            continue
        if not is_int(escolha):
            print("Entrada inválida. Tente novamente.")
            continue
        escolha = int(escolha)
        if escolha == 0:
            print("Obrigado por utilizar a máquina!")
            break
        produto = encontrar_produto(escolha)
        if not produto:
            print("Produto não encontrado.")
            continue
        if produto[3] <= 0:
            print("Produto sem estoque.")
            continue
        print(f"Você escolheu {produto[1]} - R$ {produto[2]:.2f}")
        while True:
            valor_pago_str = input("Insira o valor pago (em reais): ").replace(",", ".")
            if not is_float(valor_pago_str):
                print("Valor inválido. Tente novamente.")
                continue
            valor_pago = float(valor_pago_str)
            if valor_pago < produto[2]:
                print("Valor insuficiente. Insira um valor igual ou maior ao preço do produto.")
            else:
                break
        troco = valor_pago - produto[2]
        if troco > 0:
            troco_dict = calcular_troco_com_estoque(troco)
            if troco_dict is None:
                print("Não é possível fornecer o troco com as notas/moedas disponíveis. Compra cancelada.")
                continue
            else:
                exibir_troco(troco_dict)
                for valor, qtd in troco_dict.items():
                    estoque_cedulas[valor] -= qtd
        else:
            print("Sem troco.")
        produto[3] -= 1
        print(f"Retire sua {produto[1]}. Obrigado pela compra!\n")

if __name__ == "__main__":
    vender()