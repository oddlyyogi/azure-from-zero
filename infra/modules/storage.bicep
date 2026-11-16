@description('Storage account name: 3-24 lower-case letters and numbers.')
@minLength(3)
@maxLength(24)
param name string

@description('Azure region.')
param location string

@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_ZRS'
])
param skuName string = 'Standard_LRS'

resource account 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: name
  location: location
  kind: 'StorageV2'
  sku: {
    name: skuName
  }
  tags: {
    project: 'photo-notes'
  }
  properties: {
    allowSharedKeyAccess: false
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01' = {
  parent: account
  name: 'default'
}

resource photos 'Microsoft.Storage/storageAccounts/blobServices/containers@2024-01-01' = {
  parent: blobService
  name: 'photos'
}

output id string = account.id
output name string = account.name
