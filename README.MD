# G2 - API REST com DynamoDB e SQS usando LocalStack

Este projeto foi desenvolvido como parte da Avaliação da disciplina de Computação em Nuvem.

Consiste em uma aplicação simples de coleta e persistência de dados em ambiente simulado de nuvem, utilizando serviços simulados da AWS (DynamoDB e SQS) com LocalStack, orquestrados por Docker Compose.

## 🗂️ Estrutura do projeto

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
---
## Passos para subir o ambiente

# 1. Subir o ambiente com Docker Compose

No terminal, dentro da pasta do projeto, execute:

```bash
docker-compose down -v   # Opcional, para limpar volumes anteriores
docker-compose up --build

```

# 2. Aguarde a inicialização dos serviços:
🗂️ localstack → simula os serviços AWS (DynamoDB + SQS)

🚀 api → serviço da API REST (Flask)
🚀 worker → serviço que consome a fila SQS e processa mensagens

# 3. Verificação no terminal
Você verá no terminal mensagens indicando que os serviços foram inicializados corretamente, como por exemplo:

[API] Iniciando API Flask em 0.0.0.0:5000
[Worker] Worker iniciado. Aguardando mensagens...
[LocalStack] AWS sqs.ReceiveMessage => 200

Quando todos os serviços estiverem rodando, a aplicação estará pronta para testes.
---
## Exemplos de requisições curl para testar a API
# Criar um usuário (POST /users)

```bash
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name": "Fabio", "email": "fabio@example.com"}'
```

Resposta esperada: 
```bash
{"message": "Usuário criado com sucesso"}
```
# Listar usuários (GET /users)

```bash
curl http://localhost:5000/users
```
Resposta esperada (exemplo):
```bash
[
    {
        "email": "fabio@example.com",
        "name": "Fabio"
    },
]
```
---
## Conceitos de aplicação em nuvem aplicados
- Banco de dados NoSQL (DynamoDB): utilizado para persistência dos dados dos usuários. Simula um serviço de banco de dados gerenciado em nuvem.
- Fila de mensagens (SQS): utilizada para comunicação assíncrona entre a API e o Worker, demonstrando um padrão de arquitetura com desacoplamento de serviços.
- Serviços desacoplados: a API e o Worker foram desenvolvidos como serviços independentes, que se comunicam por meio de uma fila SQS. Isso permite escalabilidade e tolerância a falhas.
- Infraestrutura como código: todo o ambiente foi configurado com docker-compose.yml, permitindo rápida reprodução em qualquer máquina.
- Emulação de ambiente de nuvem: o LocalStack foi utilizado para simular os serviços da AWS, permitindo testes e desenvolvimento local.
