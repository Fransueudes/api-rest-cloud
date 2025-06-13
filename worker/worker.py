'''import boto3
import time

sqs = boto3.client(
    'sqs',
    endpoint_url='http://localstack:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

QUEUE_URL = sqs.get_queue_url(QueueName='user-queue')['QueueUrl']

print("Worker started. Listening for messages...")

while True:
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5
    )

    messages = response.get('Messages', [])

    for message in messages:
        print(f"Processing message: {message['Body']}")

        # Deletar mensagem após processar
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=message['ReceiptHandle']
        )

    time.sleep(2)
################################################################


import boto3
import time
import botocore

# Configuração do client SQS
sqs = boto3.client(
    'sqs',
    endpoint_url='http://localstack:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

# Função para esperar a fila estar pronta
def get_queue_url():
    while True:
        try:
            response = sqs.get_queue_url(QueueName='user-queue')
            print(f"✅ Queue URL found: {response['QueueUrl']}")
            return response['QueueUrl']
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                print("⏳ Queue not ready yet. Waiting...")
                time.sleep(3)
            else:
                raise e

# Obter URL da fila
QUEUE_URL = get_queue_url()

print("🚀 Worker started. Listening for messages...")

# Loop de processamento da fila
while True:
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5
    )

    messages = response.get('Messages', [])

    for message in messages:
        print(f"📨 Processing message: {message['Body']}")

        # Deletar mensagem após processar
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=message['ReceiptHandle']
        )
        print("✅ Message deleted.")

    time.sleep(2)
'''
import boto3
import time
import botocore

print("🔄 [Worker] Configurando cliente SQS...")
# Configuração do client SQS
sqs = boto3.client(
    'sqs',
    endpoint_url='http://localstack:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)
print("✅ [Worker] Cliente SQS configurado.")

# Função para esperar a fila estar pronta
def get_queue_url():
    tentativa = 1
    while True:
        try:
            print(f"🔎 [Worker] Tentativa {tentativa}: verificando se a fila 'user-queue' existe...")
            response = sqs.get_queue_url(QueueName='user-queue')
            print(f"✅ [Worker] Fila encontrada: {response['QueueUrl']}")
            return response['QueueUrl']
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                print(f"⏳ [Worker] Fila não disponível ainda (tentativa {tentativa}). Aguardando 3s...")
                time.sleep(3)
                tentativa += 1
            else:
                raise e

# Obter URL da fila
QUEUE_URL = get_queue_url()

print("🚀 [Worker] Worker iniciado. Aguardando mensagens...")

# Loop de processamento da fila
while True:
    print("🔄 [Worker] Consultando fila por novas mensagens...")
    try:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )
    except Exception as e:
        print(f"❌ [Worker] Erro ao consultar fila: {str(e)}")
        time.sleep(2)
        continue

    messages = response.get('Messages', [])

    if messages:
        for message in messages:
            print(f"📨 [Worker] Iniciando processamento da mensagem: {message['Body']}")

            # Deletar mensagem após processar
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )
            print("✅ [Worker] Mensagem processada e removida da fila.")
    else:
        print("⚠️ [Worker] Nenhuma mensagem no momento.")

    time.sleep(2)
