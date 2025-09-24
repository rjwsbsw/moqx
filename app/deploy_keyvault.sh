KEYVAULT_NAME="moqxkv"

az keyvault show --name $KEYVAULT_NAME --resource-group $RESOURCE_GROUP &>/dev/null || \
az keyvault create --name $KEYVAULT_NAME --resource-group $RESOURCE_GROUP --location $REGION

az keyvault secret set --vault-name $KEYVAULT_NAME --name "SqlAdminPassword" --value "$SQL_ADMIN_PASSWORD"


az webapp identity assign --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

APP_ID=$(az webapp show --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --query identity.principalId -o tsv)

az keyvault set-policy --name $KEYVAULT_NAME --object-id $APP_ID --secret-permissions get list

az webapp config appsettings set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings SQL_ADMIN_PASSWORD="@Microsoft.KeyVault(SecretUri=https://${KEYVAULT_NAME}.vault.azure.net/secrets/SqlAdminPassword/)"