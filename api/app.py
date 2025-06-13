'''from flask import Flask, request, jsonify
import boto3
import os
import time
import botocore

app = Flask(__name__)

# Configurar boto3 para LocalStack
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localstack:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

sqs = boto3.client(
    'sqs',
    endpoint_url='http://localstack:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

# Nome da tabela e URL da fila
TABLE_NAME = 'Users'
#QUEUE_URL = sqs.get_queue_url(QueueName='user-queue')['QueueUrl']

# Rotas da API
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    table = dynamodb.Table(TABLE_NAME)

    table.put_item(Item={'email': data['email'], 'name': data['name']})

    # Enviar mensagem para SQS
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=str(data)
    )

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
def list_users():
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    users = response.get('Items', [])
    return jsonify(users), 200

def get_queue_url():
    while True:
        try:
            response = sqs.get_queue_url(QueueName='user-queue')
            print(f"Queue URL found: {response['QueueUrl']}")
            return response['QueueUrl']
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                print("Queue not ready yet. Waiting...")
                time.sleep(3)
            else:
                raise e

QUEUE_URL = get_queue_url()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''

from flask import Flask, request, jsonify
import boto3
import os
import time
import botocore

app = Flask(__name__)

print("🔄 [API] Configurando cliente DynamoDB...")
# Configuração do client DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localstack:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)
print("✅ [API] Cliente DynamoDB configurado.")

print("🔄 [API] Configurando cliente SQS...")
# Configuração do client SQS
sqs = boto3.client(
    'sqs',
    endpoint_url='http://localstack:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)
print("✅ [API] Cliente SQS configurado.")

# Função para esperar a fila estar pronta
def get_queue_url():
    tentativa = 1
    while True:
        try:
            print(f"🔎 [API] Tentativa {tentativa}: verificando se a fila 'user-queue' existe...")
            response = sqs.get_queue_url(QueueName='user-queue')
            print(f"✅ [API] Fila encontrada: {response['QueueUrl']}")
            return response['QueueUrl']
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                print(f"⏳ [API] Fila não disponível ainda (tentativa {tentativa}). Aguardando 3s...")
                time.sleep(3)
                tentativa += 1
            else:
                raise e

# Obter URL da fila
QUEUE_URL = get_queue_url()

# Rotas da API
@app.route('/users', methods=['POST'])
def create_user():
    print("➡️ [API] Recebido POST /users")
    data = request.json
    print(f"🗂️ [API] Dados recebidos: {data}")

    table = dynamodb.Table('Users')

    # Inserir no DynamoDB
    print("📝 [API] Inserindo usuário no DynamoDB...")
    table.put_item(Item={'email': data['email'], 'name': data['name']})
    print(f"✅ [API] Usuário inserido no DynamoDB: {data}")

    # Enviar mensagem para SQS
    print("📤 [API] Enviando mensagem para a fila SQS...")
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=str(data)
    )
    print(f"✅ [API] Mensagem enviada para a fila SQS: {data}")

    print("✅ [API] POST /users finalizado com sucesso.")
    return jsonify({'message': 'Usuario criado com sucesso'}), 201

@app.route('/users', methods=['GET'])
def list_users():
    print("➡️ [API] Recebido GET /users")
    table = dynamodb.Table('Users')
    print("🔍 [API] Consultando tabela Users no DynamoDB...")
    response = table.scan()
    users = response.get('Items', [])
    print(f"✅ [API] Consulta finalizada. Retornando {len(users)} usuário(s).")
    return jsonify(users), 200

if __name__ == '__main__':
    print("🚀 [API] Iniciando API Flask em 0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)
