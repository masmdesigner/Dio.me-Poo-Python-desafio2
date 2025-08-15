import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# 🧍 Representa um usuário do sistema
class Usuario:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas_vinculadas = []

    def executar_operacao(self, conta, operacao):
        operacao.processar(conta)

    def incluir_conta(self, conta):
        self.contas_vinculadas.append(conta)

# 👤 Subclasse para pessoa física
class PessoaFisica(Usuario):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf

# 🏦 Conta bancária genérica
class ContaBancaria:
    def __init__(self, numero, usuario):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._usuario = usuario
        self._extrato = Extrato()

    @classmethod
    def criar_conta(cls, usuario, numero):
        return cls(numero, usuario)

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
    def usuario(self):
        return self._usuario

    @property
    def extrato(self):
        return self._extrato

    def retirar(self, valor):
        if valor <= 0:
            print("\n⚠️ Valor inválido.")
            return False

        if valor > self._saldo:
            print("\n⚠️ Saldo insuficiente.")
            return False

        self._saldo -= valor
        print("\n✅ Saque realizado com sucesso.")
        return True

    def adicionar(self, valor):
        if valor <= 0:
            print("\n⚠️ Valor inválido.")
            return False

        self._saldo += valor
        print("\n✅ Depósito realizado com sucesso.")
        return True

# 💳 Conta corrente com limites
class ContaCorrente(ContaBancaria):
    def __init__(self, numero, usuario, teto=500, max_saques=3):
        super().__init__(numero, usuario)
        self._teto = teto
        self._max_saques = max_saques

    def retirar(self, valor):
        saques_realizados = len([
            op for op in self.extrato.movimentos if op["tipo"] == Retirada.__name__
        ])

        if valor > self._teto:
            print("\n⚠️ Valor excede o limite permitido.")
            return False

        if saques_realizados >= self._max_saques:
            print("\n⚠️ Número máximo de saques atingido.")
            return False

        return super().retirar(valor)

    def __str__(self):
        return f"""
Agência:\t{self.agencia}
Conta:\t\t{self.numero}
Titular:\t{self.usuario.nome}
"""

# 📄 Histórico de operações
class Extrato:
    def __init__(self):
        self._movimentos = []

    @property
    def movimentos(self):
        return self._movimentos

    def registrar_movimento(self, operacao):
        self._movimentos.append({
            "tipo": operacao.__class__.__name__,
            "valor": operacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })

# 🔁 Classe abstrata para operações
class Operacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def processar(self, conta):
        pass

# 💸 Saque
class Retirada(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def processar(self, conta):
        if conta.retirar(self.valor):
            conta.extrato.registrar_movimento(self)

# 💰 Depósito
class Deposito(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def processar(self, conta):
        if conta.adicionar(self.valor):
            conta.extrato.registrar_movimento(self)

# 📋 Menu interativo
def exibir_menu():
    opcoes = """\n
    ================ MENU ================
    [d]\tDepositar
    [r]\tRetirar
    [x]\tExtrato
    [cc]\tCriar conta
    [lc]\tListar contas
    [cu]\tCadastrar usuário
    [s]\tSair
    => """
    return input(textwrap.dedent(opcoes))

# 🔍 Busca cliente por CPF
def localizar_usuario(cpf, usuarios):
    filtrados = [u for u in usuarios if u.cpf == cpf]
    return filtrados[0] if filtrados else None

# 🔁 Recupera conta associada
def obter_conta(usuario):
    if not usuario.contas_vinculadas:
        print("\n⚠️ Usuário não possui conta.")
        return
    return usuario.contas_vinculadas[0]  # FIXME: permitir escolha de conta

# 💰 Fluxo de depósito
def fluxo_deposito(usuarios):
    cpf = input("CPF do usuário: ")
    usuario = localizar_usuario(cpf, usuarios)

    if not usuario:
        print("\n⚠️ Usuário não encontrado.")
        return

    valor = float(input("Valor do depósito: "))
    operacao = Deposito(valor)

    conta = obter_conta(usuario)
    if conta:
        usuario.executar_operacao(conta, operacao)

# 💸 Fluxo de saque
def fluxo_retirada(usuarios):
    cpf = input("CPF do usuário: ")
    usuario = localizar_usuario(cpf, usuarios)

    if not usuario:
        print("\n⚠️ Usuário não encontrado.")
        return

    valor = float(input("Valor do saque: "))
    operacao = Retirada(valor)

    conta = obter_conta(usuario)
    if conta:
        usuario.executar_operacao(conta, operacao)

# 📄 Exibe extrato
def mostrar_extrato(usuarios):
    cpf = input("CPF do usuário: ")
    usuario = localizar_usuario(cpf, usuarios)

    if not usuario:
        print("\n⚠️ Usuário não encontrado.")
        return

    conta = obter_conta(usuario)
    if not conta:
        return

    print("\n=========== EXTRATO ===========")
    if not conta.extrato.movimentos:
        print("Sem movimentações registradas.")
    else:
        for mov in conta.extrato.movimentos:
            print(f"{mov['tipo']}:\n\tR$ {mov['valor']:.2f}")

    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("================================")

# 👤 Criação de usuário
def cadastrar_usuario(usuarios):
    cpf = input("CPF (somente números): ")
    if localizar_usuario(cpf, usuarios):
        print("\n⚠️ CPF já cadastrado.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (rua, número - bairro - cidade/UF): ")

    novo_usuario = PessoaFisica(nome, nascimento, cpf, endereco)
    usuarios.append(novo_usuario)
    print("\n✅ Usuário cadastrado com sucesso.")

# 🏦 Criação de conta
def cadastrar_conta(numero, usuarios, contas):
    cpf = input("CPF do usuário: ")
    usuario = localizar_usuario(cpf, usuarios)

    if not usuario:
        print("\n⚠️ Usuário não encontrado.")
        return

    nova_conta = ContaCorrente.criar_conta(usuario, numero)
    contas.append(nova_conta)
    usuario.incluir_conta(nova_conta)
    print("\n✅ Conta criada com sucesso.")

# 📋 Listagem de contas
def listar_todas_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

# 🚀 Execução principal
def main():
    usuarios = []
    contas = []

    while True:
        escolha = exibir_menu()

        if escolha == "d":
            fluxo_deposito(usuarios)
        elif escolha == "r":
            fluxo_retirada(usuarios)
        elif escolha == "x":
            mostrar_extrato(usuarios)
        elif escolha == "cu":
            cadastrar_usuario(usuarios)
        elif escolha == "cc":
            numero = len(contas) + 1
            cadastrar_conta(numero, usuarios, contas)
        elif escolha == "lc":
            listar_todas_contas(contas)
        elif escolha == "s":
            break
        else:
            print("\n⚠️ Opção inválida. Tente novamente.")

main()