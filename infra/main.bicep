targetScope = 'resourceGroup'

@description('Azure region for every resource.')
param location string = resourceGroup().location

@description('Six characters that make global names unique.')
param suffix string

@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_ZRS'
])
param storageSku string = 'Standard_LRS'

var storageName = 'stphotonotes${suffix}'
var blobDataReader = '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'
var roleDefs = 'Microsoft.Authorization/roleDefinitions'

module storage 'modules/storage.bicep' = {
  name: 'storage'
  params: {
    name: storageName
    location: location
    skuName: storageSku
  }
}

resource appIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-photo-notes'
  location: location
  tags: {
    project: 'photo-notes'
  }
}

resource account 'Microsoft.Storage/storageAccounts@2024-01-01' existing = {
  name: storageName
}

resource readPhotos 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(account.id, appIdentity.id, blobDataReader)
  scope: account
  properties: {
    roleDefinitionId: subscriptionResourceId(roleDefs, blobDataReader)
    principalId: appIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
  dependsOn: [
    storage
  ]
}

output storageAccountName string = storage.outputs.name
output identityName string = appIdentity.name
