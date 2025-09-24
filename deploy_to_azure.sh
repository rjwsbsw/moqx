#!/bin/bash

###############################################################################
# Script-Variable konfigurieren
###############################################################################
WEBAPP_NAME="moqxapp"

# Namen und Region
RESOURCE_GROUP="saengercontainer"
REGION="germanywestcentral"
PLAN_NAME="appsvc_linux_${REGION}"

# Azure Container Registry
ACR_NAME="moqxregistry"
ACR_IMAGE_NAME="moqx"
ACR_IMAGE_TAG="latest"
ACR_FULL_IMAGE="${ACR_NAME}.azurecr.io/${ACR_IMAGE_NAME}:${ACR_IMAGE_TAG}"

# SQL Server
SQL_SERVER_NAME="saengersql"
SQL_ADMIN_USER="saengeradmin"
SQL_ADMIN_PASSWORD="a9?w!5HA?UCTZxH"  # Am besten als Umgebungsvariable!
SQL_DB_NAME="quizdb01"
SQL_DB_CONN_STR="mssql+pymssql://${SQL_ADMIN_USER}:${SQL_ADMIN_PASSWORD}@${SQL_SERVER_NAME}.database.windows.net:1433/${SQL_DB_NAME}"


###############################################################################
# Azure SQL Server konfigurieren
###############################################################################

az sql server show --name $SQL_SERVER_NAME --resource-group $RESOURCE_GROUP &>/dev/null || \
az sql server create \
  --name $SQL_SERVER_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $REGION \
  --admin-user $SQL_ADMIN_USER \
  --admin-password $SQL_ADMIN_PASSWORD

az sql db show --name $SQL_DB_NAME --server $SQL_SERVER_NAME --resource-group $RESOURCE_GROUP &>/dev/null || \
az sql db create \
  --name $SQL_DB_NAME \
  --resource-group $RESOURCE_GROUP \
  --server $SQL_SERVER_NAME \  \
  --service-objective S0  # oder Basic, je nach Bedarf

az sql server firewall-rule show --name AllowAzureServices --resource-group $RESOURCE_GROUP --server $SQL_SERVER_NAME &>/dev/null || \
az sql server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --server $SQL_SERVER_NAME \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
az sql server firewall-rule show --name AllowLocalRoman --resource-group $RESOURCE_GROUP --server $SQL_SERVER_NAME &>/dev/null || \
az sql server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --server $SQL_SERVER_NAME \
  --name AllowLocalRoman \
  --start-ip-address 88.78.62.222 \
  --end-ip-address 88.78.62.222

###############################################################################
# Azure Container Registry konfigurieren
###############################################################################

echo "🔧 [1/7] Azure Container Registry erstellen (falls nicht vorhanden)..."
az acr show --name $ACR_NAME &>/dev/null || \
az acr create --name $ACR_NAME --resource-group $RESOURCE_GROUP --sku Basic

echo "🔐 [2/7] Admin-Zugriff für ACR aktivieren..."
az acr update -n $ACR_NAME --admin-enabled true

echo "🔐 [3/7] ACR-Zugangsdaten abrufen..."
ACR_USERNAME=$(az acr credential show -n $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR_NAME --query "passwords[0].value" -o tsv)

echo "🐳 [4/7] Container-Image bauen und pushen..."
docker build -t $ACR_FULL_IMAGE .
az acr login --name $ACR_NAME
docker push $ACR_FULL_IMAGE

###############################################################################
# Azure WebApp / ContainerApp konfigurieren
###############################################################################

echo "🌐 [5/7] Azure WebApp erstellen (falls noch nicht vorhanden)..."
az webapp show --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP &>/dev/null || \
az webapp create \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $PLAN_NAME \
  --deployment-container-image-name $ACR_FULL_IMAGE

echo "⚙️ [6/7] Container-Konfiguration an WebApp übergeben..."
az webapp config container set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name $ACR_FULL_IMAGE \
  --docker-registry-server-url https://${ACR_NAME}.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD
# --- Connection String als App Setting (optional, empfohlen) ---
az webapp config appsettings set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
      DATABASE_URL="$SQL_DB_CONN_STR"


echo "🌍 [7/7] Bereit! Du findest die App unter:"
echo "https://${WEBAPP_NAME}.azurewebsites.net"

