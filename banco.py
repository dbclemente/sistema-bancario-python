def menu():
    print("""
====== MENU DO SISTEMA BANCÁRIO ======
[1] Cadastrar usuário
[2] Depositar
[3] Sacar
[4] Extrato
[5] Sair
""")
    return input("Escolha uma opção: ")

usuarios = {}

def cadastrar_usuario():
    cpf = input("Informe o CPF (somente números): ")

    if cpf in usuarios:
        print("❌ Usuário já cadastrado.")
        return

    nome = input("Informe o nome completo: ")
    nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF): ")

    usuarios[cpf] = {
        "nome": nome,
        "nascimento": nascimento,
        "endereco": endereco,
        "saldo": 0.0,
        "extrato": [],
        "saques_diarios": 0
    }

    print("✅ Usuário cadastrado com sucesso!")

def depositar():
    cpf = input("Informe o CPF do usuário: ")

    if cpf not in usuarios:
        print("❌ Usuário não encontrado.")
        return

    valor = float(input("Informe o valor do depósito: "))

    if valor <= 0:
        print("❌ Valor inválido.")
        return

    usuarios[cpf]["saldo"] += valor
    usuarios[cpf]["extrato"].append(f"Depósito: R$ {valor:.2f}")
    print("✅ Depósito realizado com sucesso.")

def sacar():
    cpf = input("Informe o CPF do usuário: ")

    if cpf not in usuarios:
        print("❌ Usuário não encontrado.")
        return

    usuario = usuarios[cpf]

    if usuario["saques_diarios"] >= 3:
        print("❌ Limite de 3 saques diários atingido.")
        return

    valor = float(input("Informe o valor do saque: "))

    if valor <= 0:
        print("❌ Valor inválido.")
    elif valor > 500:
        print("❌ O limite por saque é R$500.")
    elif valor > usuario["saldo"]:
        print("❌ Saldo insuficiente.")
    else:
        usuario["saldo"] -= valor
        usuario["extrato"].append(f"Saque:    R$ {valor:.2f}")
        usuario["saques_diarios"] += 1
        print("✅ Saque realizado com sucesso.")

def extrato():
    cpf = input("Informe o CPF do usuário: ")

    if cpf not in usuarios:
        print("❌ Usuário não encontrado.")
        return

    usuario = usuarios[cpf]
    print("\n====== EXTRATO ======")

    if not usuario["extrato"]:
        print("Não foram realizadas movimentações.")
    else:
        for item in usuario["extrato"]:
            print(item)

    print(f"\nSaldo atual: R$ {usuario['saldo']:.2f}")

def main():
    while True:
        opcao = menu()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            depositar()
        elif opcao == "3":
            sacar()
        elif opcao == "4":
            extrato()
        elif opcao == "5":
            print("👋 Encerrando o sistema.")
            break
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    main()

