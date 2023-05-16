from datetime import datetime
import abc


class Cliente:

    def __init__(self, endereco) -> None:
        self.endereco: str = endereco
        self.contas: list[Conta] = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    
    def __init__(self, cpf: str, nome: str, data_nascimento: datetime, endereco: str) -> None:
        self.cpf: str = cpf
        self.nome: str = nome
        self.data_nascimento: datetime = data_nascimento
        super().__init__(endereco)

class Conta:

    def __init__(self, cliente: Cliente, numero: int) -> None:
        self._saldo: float = 0
        self._numero: int = numero
        self._agencia: str = "0001"
        self._cliente: Cliente = cliente
        self._historico: Historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    # @classmethod
    # def saldo(self) -> float:
    #     return self.saldo

    def sacar(self, valor: float) -> bool:
        saldo = self.saldo
        if valor > saldo:
            print(f"Não foi possível realizar saque, saldo insuficiente. Por favor repita a operação com um valor válido.")         
        # if valor > limite:
        #     print(f"Não foi possível realizar saque, pois o valor solicitado excede o limite de R$ {LIMITE} por saque. Por favor repita a operação com um valor válido.")    
        # if numero_saques >= limite_saques:
        #     print(f"Não foi possível realizar saque, pois já foram realizados {LIMITE_SAQUES} hoje. Por favor tente novamente amanhã.")
        elif valor <= 0:
            print(f"Não foi possível realizar saque, valor inválido. Por favor repita a operação com um valor válido.") 
        else:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            return True
        # numero_saques += 1
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print(f"Deposito de R$ {valor:.2f} realizado com sucesso")
            return True
        else: 
            print(f"Não foi possível realizar depósito, valor inválido. Por favor repita a operação com um valor válido.")
            return False

class ContaCorrente(Conta):
     
    def __init__(self, cliente: Cliente, numero: int, limite: float = 500, limite_saques: int = 3) -> None:
        self.limite: float = limite
        self.limite_saques: int = limite_saques
        super().__init__(cliente, numero)

    def sacar(self, valor: float) -> bool:
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])       
        if valor > self.limite:
            print(f"Não foi possível realizar saque, pois o valor solicitado excede o limite de R$ {self.limite} por saque. Por favor repita a operação com um valor válido.")    
        elif numero_saques >= self.limite_saques:
            print(f"Não foi possível realizar saque, pois já foram realizados {self.limite_saques} hoje. Por favor tente novamente amanhã.")
        else:
            return super().sacar(valor)
        return False

class Transacao(abc.ABC):
     @property
     @abc.abstractproperty
     def valor(self):
        pass
     
     @abc.abstractclassmethod
     def registrar(self, conta: Conta):
        pass
     
class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor: float = valor

    @property
    def valor(self):
        return self._valor  

    def registrar(self, conta: Conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
     
class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor: float = valor

    @property
    def valor(self):
        return self._valor  

    def registrar(self, conta: Conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Historico:
     
    def __init__(self) -> None:
        self._transacoes: list = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y - %H:%M:%s"),
        })