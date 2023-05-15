menu = '''

[d] = Depositar
[s] = Saque
[e] = Extrato
[u] = Criar Usuário
[c] = Criar Conta-corrente
[x] = Sair

=> '''

AGENCIA = 1000
LIMITE = 500
LIMITE_SAQUES = 3

saldo = 0
extrato = ""
numero_saques = 0
usuarios = []
contas = []
numero_ultima_conta = 0

def remove_pontuacao_cpf(cpf: str):
    return "".join([i for i in cpf if i.isnumeric()])

def existe_cadastro_usuario(cpf):
    usuario_encontrado = None
    for usuario in usuarios:
        if cpf == usuario["cpf"]:
            usuario_encontrado = usuario['nome']
            return usuario_encontrado
    return usuario_encontrado

def saque(*, saldo: float, valor: float, extrato: str, limite: float, numero_saques: int, limite_saques: int):
    if valor > limite:
        print(f"Não foi possível realizar saque, pois o valor solicitado excede o limite de R$ {LIMITE} por saque. Por favor repita a operação com um valor válido.")
    if valor > saldo:
        print(f"Não foi possível realizar saque, saldo insuficiente. Por favor repita a operação com um valor válido.")
    if numero_saques >= limite_saques:
        print(f"Não foi possível realizar saque, pois já foram realizados {LIMITE_SAQUES} hoje. Por favor tente novamente amanhã.")
    else: 
        print(f"Valor R$ {valor:.2f} sacado com sucesso")
        numero_saques += 1
        saldo -= valor
        extrato += f"Saque   : R$ {valor:15.2f}\n"
    return saldo, extrato
    

def deposito(saldo: float, valor: float, extrato: str, /):
    print(f"Valor R$ {valor:.2f} depositado com sucesso")
    saldo += valor
    extrato += f"Depósito: R$ {valor:>15.2f}\n"
    return saldo, extrato

def mostra_extrato(saldo: float, /, *, extrato: str):
    print("Extrato")
    print("="*40)
    print("Não foram realizadas movimentações até o momento." if not extrato else extrato)
    print("="*40)
    print(f"Saldo   : R$ {saldo:>15.2f}")

def criar_usuario(nome: str, data_nasc: str, cpf: str, endereco: str):
    novo_usuario = {
        "nome": nome,
        "data_nasc": data_nasc,
        "cpf": remove_pontuacao_cpf(cpf),
        "endereco": endereco
    }
    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso")

def criar_conta_corrente(agencia: str, conta: int, usuario: str):
        conta += 1
        nova_conta = {
            "agencia": agencia,
            "conta": conta,
            "usuario": usuario,
        }
        contas.append(nova_conta)
        print(f"Conta {conta} criada com sucesso.")
        return conta

while True:

    opcao = input(menu)

    if opcao == "d":
        print("Depósito")
        valor = float(input("Digite o valor que deseja depositar: "))
        if valor > 0:
            saldo, extrato = deposito(saldo, valor, extrato)
        else:
            print("Valor inválido. Por favor repita a operação com um valor válido.")

    elif opcao == "s":
        print("Saque")
        valor = float(input("Digite o valor que deseja sacar: "))
        if valor > 0:
            saldo, extrato = saque(saldo=saldo, valor=valor, extrato=extrato, limite=LIMITE, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
        else:
            print("Valor inválido. Por favor repita a operação com um valor válido.")

    elif opcao == "e":
        mostra_extrato(saldo, extrato=extrato)

    elif opcao == "u":
        print("Cadastro de usuário")
        cpf = input("CPF: ")
        cpf_numerico = remove_pontuacao_cpf(cpf)
        if not existe_cadastro_usuario(cpf_numerico):
            nome = input("Nome completo: ")
            data_nasc = input("Data de nascimento: ")
            endereco = input("Endereco: ")
            criar_usuario(nome=nome, data_nasc=data_nasc, cpf=cpf_numerico, endereco=endereco)
        else:
            print("Já existe usuário cadastrado com o CPF informado.")

    elif opcao == 'c':
        print("Abertura de conta-corrente")
        cpf=input("Digite o CPF do titular da conta: ")
        cpf_numerico = remove_pontuacao_cpf(cpf)
        usuario = existe_cadastro_usuario(cpf)
        if usuario:
            numero_ultima_conta = criar_conta_corrente(agencia=AGENCIA, conta=numero_ultima_conta, usuario=usuario)
        else:
            print("Não existe usuário cadastrado com o CPF informado.\nNão foi possível abrir a conta.")

    elif opcao == "x":
        break

    else:
        print("Operação válida. Por favor selecione novamente a operação desejada.")