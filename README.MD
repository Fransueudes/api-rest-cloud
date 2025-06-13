# G2 - API REST com DynamoDB e SQS usando LocalStack

Este projeto foi desenvolvido como parte da Avaliação da disciplina de Computação em Nuvem.

Consiste em uma aplicação simples de coleta e persistência de dados em ambiente simulado de nuvem, utilizando serviços simulados da AWS (DynamoDB e SQS) com LocalStack, orquestrados por Docker Compose.

## 📋 Sumário

- [Introdução](#introdução)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração e Execução](#configuração-e-execução)
- [Uso da API](#uso-da-api)
- [Conceitos de Aplicação em Nuvem Aplicados](#conceitos-de-aplicação-em-nuvem-aplicados)

## 🚀 Introdução

Este projeto foi desenvolvido como parte da Avaliação da disciplina de Computação em Nuvem.

Consiste em uma aplicação simples de coleta e persistência de dados em ambiente simulado de nuvem, utilizando serviços simulados da AWS (DynamoDB e SQS) com LocalStack, orquestrados por Docker Compose.

## 🗂️ Estrutura do Projeto

```plaintext
📁 g2/
├── api/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
├── worker/
│   ├── worker.py
│   ├── requirements.txt
│   ├── Dockerfile
├── entrypoint.sh
├── docker-compose.yml
└── README.md
```

## ⚙️ Configuração e Execução

Siga os passos abaixo para configurar e executar o ambiente do projeto:

### 1. Iniciar o ambiente Docker Compose

No terminal, dentro da pasta raiz do projeto, execute:

```bash
docker-compose down -v   # Opcional: para limpar volumes anteriores
docker-compose up --build
```

### 2. Verificação da Inicialização dos Serviços

Aguarde a inicialização dos seguintes serviços:

-   **🗂️ LocalStack**: Simula os serviços AWS (DynamoDB + SQS).
-   **🚀 API**: Serviço da API REST (Flask).
-   **🚀 Worker**: Serviço que consome a fila SQS e processa mensagens.

### 3. Verificação no Terminal

Você verá no terminal mensagens indicando que os serviços foram inicializados corretamente, como por exemplo:

```
[API] Iniciando API Flask em 0.0.0.0:5000
[Worker] Worker iniciado. Aguardando mensagens...
[LocalStack] AWS sqs.ReceiveMessage => 200
```

Quando todos os serviços estiverem rodando, a aplicação estará pronta para testes.

## 💡 Uso da API

Utilize os exemplos de requisições `curl` abaixo para testar a API:

### Criar um Usuário (POST /users)

```bash
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name": "Fabio", "email": "fabio@example.com"}'
```

**Resposta esperada:**

```json
{"message": "Usuário criado com sucesso"}
```

### Listar Usuários (GET /users)

```bash
curl http://localhost:5000/users
```

**Resposta esperada (exemplo):**

```json
[
    {
        "email": "fabio@example.com",
        "name": "Fabio"
    }
]
```

## ☁️ Conceitos de Aplicação em Nuvem Aplicados

Este projeto demonstra a aplicação dos seguintes conceitos de computação em nuvem:

-   **Banco de Dados NoSQL (DynamoDB)**: Utilizado para persistência dos dados dos usuários. Simula um serviço de banco de dados gerenciado em nuvem.
-   **Fila de Mensagens (SQS)**: Utilizada para comunicação assíncrona entre a API e o Worker, demonstrando um padrão de arquitetura com desacoplamento de serviços.
-   **Serviços Desacoplados**: A API e o Worker foram desenvolvidos como serviços independentes, que se comunicam por meio de uma fila SQS. Isso permite escalabilidade e tolerância a falhas.
-   **Infraestrutura como Código (IaC)**: Todo o ambiente foi configurado com `docker-compose.yml`, permitindo rápida reprodução em qualquer máquina.
-   **Emulação de Ambiente de Nuvem**: O LocalStack foi utilizado para simular os serviços da AWS, permitindo testes e desenvolvimento local.

Fransueudes Alexandre Freitas
