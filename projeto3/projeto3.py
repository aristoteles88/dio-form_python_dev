from datetime import datetime
import textwrap
from models.cliente import Deposito, Saque

from models.cliente import PessoaFisica, ContaCorrente

def remove_pontuacao_cpf(cpf: str):
    return "".join([i for i in cpf if i.isnumeric()])

def existe_cadastro_usuario(cpf) -> PessoaFisica:
    cliente = [cliente for cliente in clientes if cpf == cliente.cpf]
    return cliente[0] if len(cliente) > 0 else None

def recebe_data_nasc():
    while True:
        try:
            data = input("Data de nascimento (DD/MM/AAAA): ")
            return datetime.strptime(data, "%d/%m/%Y")
        except:
            print("Data informada em formato inválido. Tente novamente.")
    


def mostra_extrato(conta: ContaCorrente):
    transacoes = conta.historico.transacoes
    print("Extrato")
    print("="*36)
    if len(transacoes) == 0:
        print("Não foram realizadas movimentações até o momento." )
    else: 
        for transacao in transacoes:
            print(f"{transacao['tipo']: <10}{transacao['valor']:>26.2f}")   
        print("="*36)
        print(f"{'Saldo:': <10}{conta.saldo:>26.2f}")
    print("="*36)


def menu_principal():
    menu = '''
    [a]\tAcessar Conta
    [u]\tCriar Usuário
    [c]\tCriar Conta-corrente
    [x]\tSair
    => '''

    while True:

        opcao = input(textwrap.dedent(menu))

        if opcao == "a":
            cpf = input("Digite o CPF do usuário: ")
            cliente = existe_cadastro_usuario(remove_pontuacao_cpf(cpf))
            if not cliente:
                print("Não encontramos cliente com o CPF informado.")
            elif len(cliente.contas) == 0:
                print("Não encontramos conta para o cliente informado.")
            else:
                print("Contas do cliente:")
                for conta in cliente.contas:
                    print (f"Conta {conta.numero}")
                print("="*30)
                conta_valida = False
                while not conta_valida:
                    numero_conta = int(input("Digite o numero da conta que deseja acessar: "))
                    conta = [conta for conta in cliente.contas if numero_conta == conta.numero]
                    if len(conta) != 0:
                        conta_valida = True
                    else:
                        print("Conta invalida. Tente novamente]") 
                menu_conta(cliente=cliente, conta=conta[0])
                
        elif opcao == "u":
            print("Cadastro de usuário")
            cpf = input("CPF: ")
            cpf_numerico = remove_pontuacao_cpf(cpf)
            if not existe_cadastro_usuario(cpf_numerico):
                nome = input("Nome completo: ")
                data_nasc = recebe_data_nasc()
                endereco = input("Endereco: ")
                clientes.append(PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nasc, endereco=endereco))
                print(f"Cliente {nome} adicionado com sucesso")
            else:
                print("Já existe usuário cadastrado com o CPF informado.")

        elif opcao == 'c':
            numero_conta = len(contas) + 1
            print("Abertura de conta-corrente")
            cpf=input("Digite o CPF do titular da conta: ")
            cpf_numerico = remove_pontuacao_cpf(cpf)
            cliente = existe_cadastro_usuario(cpf)
            if cliente:
                conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
                cliente.contas.append(conta)
                contas.append(conta)
                print(f"Conta {conta.numero} criada com sucesso.")
            else:
                print("Não existe usuário cadastrado com o CPF informado.\nNão foi possível abrir a conta.")

        elif opcao == "x":
            break

        else:
            print("Operação válida. Por favor selecione novamente a operação desejada.")

def menu_conta(cliente: PessoaFisica, conta: ContaCorrente):
    menu = '''
    [d]\tDepositar
    [s]\tSaque
    [e]\tExtrato
    [x]\tSair
    '''

    while True:

        opcao = input(textwrap.dedent(menu))

        if opcao == "d":
            print("Depósito")
            valor = float(input("Digite o valor que deseja depositar: "))
            transacao = Deposito(valor)
            cliente.realizar_transacao(conta=conta, transacao=transacao)

        elif opcao == "s":
            print("Saque")
            valor = float(input("Digite o valor que deseja sacar: "))
            transacao = Saque(valor)
            cliente.realizar_transacao(conta=conta, transacao=transacao)

        elif opcao == "e":
            mostra_extrato(conta)

        elif opcao == "x":
            break

        else:
            print("Operação válida. Por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    clientes: list[PessoaFisica] = []
    contas = []
    menu_principal()