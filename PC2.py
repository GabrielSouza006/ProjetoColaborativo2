produtos = [
    [1, "Coca-cola", 3.75, 2],
    [2, "Pepsi", 3.67, 5],
    [3, "Monster", 9.96, 1],
    [4, "Café", 1.25, 100],
    [5, "Redbull", 13.99, 2]
]
cedulas_moedas = [10000, 5000, 2000, 1000, 500, 200, 100, 50, 25, 10, 5, 1]

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

def calcular_troco(valor_troco):
    troco = {}
    valor_centavos = int(round(valor_troco * 100))
    for valor in cedulas_moedas:
        qtd, valor_centavos = divmod(valor_centavos, valor)
        if qtd > 0:
            troco[valor] = qtd
    return troco

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

def vender():
    while True:
        mostrar_produtos()
        try:
            escolha = int(input("\nDigite o ID da bebida desejada (0 para sair): "))
        except ValueError:
            print("Entrada inválida. Tente novamente.")
            continue
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
            try:
                valor_pago = float(input("Insira o valor pago (em reais): ").replace(",", "."))
            except ValueError:
                print("Valor inválido. Tente novamente.")
                continue
            if valor_pago < produto[2]:
                print("Valor insuficiente. Insira um valor igual ou maior ao preço do produto.")
            else:
                break
        troco = valor_pago - produto[2]
        if troco > 0:
            troco_dict = calcular_troco(troco)
            exibir_troco(troco_dict)
        else:
            print("Sem troco.")
        produto[3] -= 1
        print(f"Retire sua {produto[1]}. Obrigado pela compra!\n")

if __name__ == "__main__":
    vender()