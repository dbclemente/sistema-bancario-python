from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()

    def registrar(self, conta):
        if self.valor <= 0:
            print("❌ Valor de depósito inválido!")
            return False
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)
        print(f"✅ Depósito de R$ {self.valor:.2f} realizado com sucesso!")
        return True

    def __str__(self):
        return f"Depósito: R$ {self.valor:.2f} em {self.data.strftime('%d/%m/%Y %H:%M:%S')}"

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()

    def registrar(self, conta):
        if self.valor <= 0:
            print("❌ Valor de saque inválido!")
            return False
        if self.valor > conta.saldo:
            print("❌ Saldo insuficiente!")
            return False
        if self.valor > conta.limite:
            print("❌ Valor do saque excede o limite!")
            return False
        if conta.numero_saques >= conta.limite_saques:
            print("❌ Número máximo de saques excedido!")
            return False
        conta.saldo -= self.valor
        conta.numero_saques += 1
        conta.historico.adicionar_transacao(self)
        print(f"✅ Saque de R$ {self.valor:.2f} realizado com sucesso!")
        return True

    def __str__(self):
        return f"Saque: R$ {self.valor:.2f} em {self.data.strftime('%d/%m/%Y %H:%M:%S')}"

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def extrato(self):
        if not self.transacoes:
            return "Não foram realizadas movimentações."
        return '\n'.join(str(t) for t in self.transacoes)

class Conta:
    def __init__(self, cliente, numero, agencia="0001", limite=500, limite_saques=3):
        self.cliente = cliente
        self.numero = numero
        self.agencia = agencia
        self.saldo = 0
        self.historico = Historico()
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print(self.historico.extrato())
        print(f"\nSaldo atual: R$ {self.saldo:.2f}")
        print("==========================================")

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

# Exemplo rápido de uso

def main():
    clientes = []
    contas = []

    # Criar cliente
    cliente1 = Cliente("João Silva", "12345678900", "01-01-1980", "Rua A, 123")
    clientes.append(cliente1)

    # Criar conta para cliente
    conta1 = Conta(cliente1, numero=1)
    cliente1.adicionar_conta(conta1)
    contas.append(conta1)

    # Depositar
    conta1.depositar(1000)
    # Sacar
    conta1.sacar(200)
    # Mostrar extrato
    conta1.exibir_extrato()
def menu():
    return """
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[q] Sair
=> """

def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def criar_cliente(clientes):
    cpf = input("CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("❌ Já existe um cliente com esse CPF.")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nº - bairro - cidade/UF): ")

    cliente = Cliente(nome, cpf, data_nascimento, endereco)
    clientes.append(cliente)
    print("✅ Cliente criado com sucesso!")

def criar_conta(numero, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("❌ Cliente não encontrado. Crie o cliente primeiro.")
        return

    conta = Conta(cliente, numero)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("✅ Conta criada com sucesso!")

def listar_contas(contas):
    print("\n========== CONTAS ==========")
    for conta in contas:
        print(f"Agência: {conta.agencia}")
        print(f"Conta nº: {conta.numero}")
        print(f"Titular: {conta.cliente.nome}")
        print("----------------------------")

def selecionar_conta(cliente):
    if not cliente.contas:
        print("❌ Cliente não possui contas.")
        return None

    print("Contas disponíveis:")
    for i, conta in enumerate(cliente.contas):
        print(f"[{i}] Conta nº {conta.numero} - Saldo: R$ {conta.saldo:.2f}")

    indice = int(input("Escolha o número da conta: "))
    if 0 <= indice < len(cliente.contas):
        return cliente.contas[indice]
    else:
        print("❌ Índice inválido.")
        return None

def executar_menu():
    clientes = []
    contas = []
    numero_conta = 1

    while True:
        opcao = input(menu())

        if opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            criar_conta(numero_conta, clientes, contas)
            numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao in ["d", "s", "e"]:
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("❌ Cliente não encontrado.")
                continue

            conta = selecionar_conta(cliente)
            if not conta:
                continue

            if opcao == "d":
                valor = float(input("Valor do depósito: "))
                conta.depositar(valor)

            elif opcao == "s":
                valor = float(input("Valor do saque: "))
                conta.sacar(valor)

            elif opcao == "e":
                conta.exibir_extrato()

        elif opcao == "q":
            print("✅ Obrigado por usar o sistema bancário. Até logo!")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")

        

        
    ...

if __name__ == "__main__":
    executar_menu()
    



