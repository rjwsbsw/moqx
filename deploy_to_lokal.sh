#!/bin/bash

# ❗ Anpassen: Namen und Region
RESOURCE_GROUP="saengercontainer"
ACR_NAME="moqxregistry"
ACR_IMAGE_NAME="moqx"
WEBAPP_NAME="moqxapp"
REGION="germanywestcentral"
PLAN_NAME="appsvc_linux_${REGION}"
IMAGE_TAG="latest"
ACR_FULL_IMAGE="${ACR_NAME}.azurecr.io/${ACR_IMAGE_NAME}:${IMAGE_TAG}"
LOCAL_PORT="8001"

# ❗ SQL-Server Konfiguration
SQL_SERVER_NAME="saengersql"
SQL_DATABASE_NAME="quizdb01"
SQL_ADMIN_USER="saengeradmin"
SQL_ADMIN_PASSWORD="a9?w!5HA?UCTZxH"
DATABASE_URL="mssql+pymssql://${SQL_ADMIN_USER}:${SQL_ADMIN_PASSWORD}@${SQL_SERVER_NAME}.database.windows.net:1433/${SQL_DATABASE_NAME}?charset=utf8&timeout=30"


echo "🔧 [1/7] Azure Container Registry erstellen (falls nicht vorhanden)..."
az acr show --name $ACR_NAME &>/dev/null || \
az acr create --name $ACR_NAME --resource-group $RESOURCE_GROUP --sku Basic

echo "🔐 [2/7] Admin-Zugriff für ACR aktivieren..."
az acr update -n $ACR_NAME --admin-enabled true > /dev/null

echo "🔐 [3/7] ACR-Zugangsdaten abrufen..."
ACR_USERNAME=$(az acr credential show -n $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR_NAME --query "passwords[0].value" -o tsv)

echo "🐳 [4/7] Container-Image bauen und pushen..."
docker build -t $ACR_FULL_IMAGE .
az acr login --name $ACR_NAME
docker push $ACR_FULL_IMAGE

echo "🌍 [5/5] Azure-Image Lokal starten"
docker run --rm -p ${LOCAL_PORT}:80 \
    -e DATABASE_URL="${DATABASE_URL}" \
    $ACR_FULL_IMAGE

# docker run --rm -p ${LOCAL_PORT}:80 \
#     -e SQL_USER="${SQL_ADMIN_USER}" \
#     -e SQL_PASSWORD="${SQL_ADMIN_PASSWORD}" \
#     -e SQL_SERVER="${SQL_SERVER_NAME}.database.windows.net:1433" \
#     -e SQL_DATABASE="${SQL_DATABASE_NAME}" \
#     $ACR_FULL_IMAGE
