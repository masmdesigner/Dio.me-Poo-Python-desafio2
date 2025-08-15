# 🏦 Sistema Bancário em Python — Desafio POO

Este projeto é um sistema bancário simples, desenvolvido como desafio de Programação Orientada a Objetos (POO) com Python. Ele permite simular operações bancárias como depósitos, saques, criação de contas e usuários, além de exibir extratos e listar contas.

---

## 📚 Conceitos Aplicados

- **Encapsulamento**: Protege os dados internos das classes.
- **Herança**: Permite que classes compartilhem atributos e comportamentos.
- **Polimorfismo**: Permite que diferentes classes implementem métodos com o mesmo nome.
- **Abstração**: Utiliza classes abstratas para definir contratos de operação.

---

## 🧩 Estrutura do Projeto

### 🔹 `Usuario`
Classe base que representa um cliente do sistema.

- Atributos:
  - `endereco`: endereço do cliente.
  - `contas_vinculadas`: lista de contas associadas.
- Métodos:
  - `executar_operacao(conta, operacao)`: executa uma operação (saque ou depósito).
  - `incluir_conta(conta)`: adiciona uma conta ao cliente.

---

### 🔹 `PessoaFisica` (herda de `Usuario`)
Representa um cliente pessoa física.

- Atributos adicionais:
  - `nome`
  - `nascimento`
  - `cpf`

---

### 🔹 `ContaBancaria`
Classe base para contas bancárias.

- Atributos:
  - `_saldo`: saldo atual.
  - `_numero`: número da conta.
  - `_agencia`: código da agência.
  - `_usuario`: cliente associado.
  - `_extrato`: histórico de operações.
- Métodos:
  - `retirar(valor)`: realiza saque.
  - `adicionar(valor)`: realiza depósito.
  - `criar_conta(usuario, numero)`: método de classe para instanciar nova conta.

---

### 🔹 `ContaCorrente` (herda de `ContaBancaria`)
Conta com limite de saque e número máximo de saques por dia.

- Atributos adicionais:
  - `_teto`: valor máximo por saque.
  - `_max_saques`: número máximo de saques permitidos.
- Sobrescreve:
  - `retirar(valor)`: com regras de limite e quantidade.

---

### 🔹 `Extrato`
Registra todas as operações realizadas em uma conta.

- Atributos:
  - `_movimentos`: lista de dicionários com tipo, valor e data.
- Métodos:
  - `registrar_movimento(operacao)`: adiciona uma operação ao extrato.

---

### 🔹 `Operacao` (classe abstrata)
Define a interface para operações bancárias.

- Propriedade abstrata:
  - `valor`
- Método abstrato:
  - `processar(conta)`

---

### 🔹 `Retirada` (herda de `Operacao`)
Implementa a operação de saque.

- Atributos:
  - `_valor`
- Método:
  - `processar(conta)`: realiza o saque e registra no extrato.

---

### 🔹 `Deposito` (herda de `Operacao`)
Implementa a operação de depósito.

- Atributos:
  - `_valor`
- Método:
  - `processar(conta)`: realiza o depósito e registra no extrato.

---

## 🧪 Funcionalidades do Menu

- `[d]` Depositar
- `[r]` Retirar
- `[x]` Extrato
- `[cc]` Criar conta
- `[lc]` Listar contas
- `[cu]` Cadastrar usuário
- `[s]` Sair

---

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio