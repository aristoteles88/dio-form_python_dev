menu = '''

[d] = Depositar
[s] = Saque
[e] = Extrato
[x] = Sair

=> '''

saldo = 0
LIMITE = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def eh_float(valor: str):
    try:
        float(valor)
        return True
    except:
        return False

def verifica_valor(valor: str):
    valor = valor.replace(",", ".")
    if eh_float(valor):
        valor_float = float(valor)
        if valor_float != 0:
            return True, "", valor_float
        return False, "Valor digitado é 0. Por favor repita a operação com um valor válido.", -1
    return False, "Valor digitado não é um valor válido. Por favor repita a operação com um valor válido.", -1

while True:

    opcao = input(menu)

    if opcao == "d":
        print("Depósito")
        valor = input("Digite o valor que deseja depositar: ")
        valor_eh_valido, msg, valor_float = verifica_valor(valor)
        if valor_eh_valido:
            print(f"Valor R$ {valor_float:.2f} depositado com sucesso")
            saldo += valor_float
            extrato += f"Depósito: R$ {valor_float:>15.2f}\n"
        print(msg)

    elif opcao == "s":
        print("Saque")
        valor = input("Digite o valor que deseja sacar: ")
        valor_eh_valido, msg, valor_float = verifica_valor(valor)
        if valor_eh_valido:
            if valor_float > LIMITE:
                print(f"Não é possível sacar R$ {valor_float:.2f}, pois excede o limite de R$ {LIMITE} por saque. Por favor repita a operação com um valor válido.")
                continue
            if valor_float > saldo:
                print(f"Não é possível sacar R$ {valor_float:.2f}, saldo indisponível. Por favor repita a operação com um valor válido.")
                continue
            if numero_saques >= LIMITE_SAQUES:
                print(f"Não é possível sacar R$ {valor_float:.2f}, pois já foram realizados {LIMITE_SAQUES} hoje. Por favor tente novamente amanhã.")
                continue
            print(f"Valor R$ {valor_float:.2f} sacado com sucesso")
            numero_saques += 1
            saldo -= valor_float
            extrato += f"Saque   : R$ {valor_float:15.2f}\n"
        print(msg)

    elif opcao == "e":
        print("Extrato")
        print("="*40)
        print("Não foram realizadas movimentações até o momento." if not extrato else extrato)
        print("="*40)
        print(f"Saldo   : R$ {saldo:>15.2f}")


    elif opcao == "x":
        break

    else:
        print("Operação válida. Por favor selecione novamente a operação desejada.")