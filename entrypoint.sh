#!/bin/bash

echo "✅ Iniciando criação de recursos AWS simulados..."

# Criar tabela DynamoDB
awslocal dynamodb create-table \
    --table-name Users \
    --attribute-definitions AttributeName=email,AttributeType=S \
    --key-schema AttributeName=email,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    && echo "✅ Tabela Users criada com sucesso." \
    || echo "⚠️ Tabela Users já existe."

# Criar fila SQS
awslocal sqs create-queue --queue-name user-queue \
    && echo "✅ Fila user-queue criada com sucesso." \
    || echo "⚠️ Fila user-queue já existe."

echo "✅ Finalizada criação de recursos AWS simulados."
