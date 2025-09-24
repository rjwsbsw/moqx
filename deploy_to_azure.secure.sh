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
SQL_DB_NAME="quizdb01"
SQL_DB_CONN_STR="mssql+pymssql://${SQL_ADMIN_USER}:${SQL_ADMIN_PASSWORD}@${SQL_SERVER_NAME}.database.windows.net/${SQL_DB_NAME}"

# # Passwort muss als Umgebungsvariable gesetzt sein!
# if [ -z "$SQL_ADMIN_PASSWORD" ]; then
#   echo "❌ Fehler: SQL_ADMIN_PASSWORD ist nicht gesetzt."
#   exit 1
# fi

read -sp "Bitte geben Sie das SQL Admin Passwort ein: " SQL_ADMIN_PASSWORD
echo "" # notwendiger Zeilenumbruch

# NEU: Key Vault
KEYVAULT_NAME="moqxkv"

###############################################################################
# Azure Key Valut konfigurieren
###############################################################################

echo "🔧 [-5/7] Azure Key Vault für User verfügbar machen ..."

az provider register --namespace Microsoft.KeyVault --wait
USER_OBJECT_ID=$(az ad signed-in-user show --query id -o tsv)
az role assignment create \
    --role "Key Vault Secrets Officer" \
    --assignee $USER_OBJECT_ID \
    --scope "/subscriptions/bb98ad61-3e61-4279-9ac1-327c69ee61e7/resourcegroups/saengercontainer/providers/microsoft.keyvault/vaults/moqxkv"

echo "🔧 [-4/7] Azure Key Vault konfigurieren..."
az keyvault show --name $KEYVAULT_NAME --resource-group $RESOURCE_GROUP &>/dev/null || \
az keyvault create --name $KEYVAULT_NAME --resource-group $RESOURCE_GROUP --location $REGION

ENCODED_PASSWORD=$(echo -n "$SQL_ADMIN_PASSWORD" | base64)
az keyvault secret set --vault-name $KEYVAULT_NAME --name "SqlAdminPassword" --value "$SQL_ADMIN_PASSWORD" &>/dev/null

###############################################################################
# Azure SQL Server konfigurieren
###############################################################################

echo "🔧 [-3/7] SQL Server testen und installieren..."
az sql server show --name $SQL_SERVER_NAME --resource-group $RESOURCE_GROUP &>/dev/null || \
az sql server create \
  --name $SQL_SERVER_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $REGION \
  --admin-user $SQL_ADMIN_USER \
  --admin-password $SQL_ADMIN_PASSWORD

echo "🔧 [-4/7] SQL DB testen und installieren..."
az sql db show --name $SQL_DB_NAME --server $SQL_SERVER_NAME --resource-group $RESOURCE_GROUP &>/dev/null || \
az sql db create \
  --resource-group $RESOURCE_GROUP \
  --server $SQL_SERVER_NAME \
  --name $SQL_DB_NAME \
  --service-objective S0  # oder Basic, je nach Bedarf

echo "🔧 [-2/7] SQL Firewall einrichten ..."
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
  --resource-group $RESOURCE_GROUP \
  --plan $PLAN_NAME \
  --name $WEBAPP_NAME \
  --deployment-container-image-name $ACR_FULL_IMAGE

echo "⚙️ [6/7] Container-Konfiguration an WebApp übergeben..."
az webapp config container set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --container-image-name $ACR_FULL_IMAGE \
  --container-registry-url https://${ACR_NAME}.azurecr.io \
  --container-registry-user $ACR_USERNAME \
  --container-registry-password $ACR_PASSWORD

# Key Vault Access konfigurieren
echo "🌍 [7/7] Key Vault Zugriff für die App konfigurieren."
az webapp identity assign \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP

# Managed Identity ID der WebApp abrufen
APP_IDENTITY=$(az webapp identity show \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query principalId \
  --output tsv)
# RBAC Rolle "Key Vault Secrets User" zuweisen
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee-object-id "$APP_IDENTITY" \
  --scope "/subscriptions/bb98ad61-3e61-4279-9ac1-327c69ee61e7/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.KeyVault/vaults/$KEYVAULT_NAME"

# App Settings mit Key Vault Referenz aktualisieren
az webapp config appsettings set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    SQL_USER="$SQL_ADMIN_USER" \
    SQL_PASSWORD="@Microsoft.KeyVault(SecretUri=https://${KEYVAULT_NAME}.vault.azure.net/secrets/SqlAdminPassword/)" \
    SQL_SERVER="${SQL_SERVER_NAME}.database.windows.net:1433" \
    SQL_DATABASE="$SQL_DB_NAME"

echo "🌍 [8/7] Bereit! Du findest die App unter:"
echo "https://${WEBAPP_NAME}.azurewebsites.net"

