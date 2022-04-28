import stellar ... 
import requests
import json

SecretKey = "ABCD..." # Admin temporary 1-weight signers... execute on offline airgapped sys... then remove from Issuer 

identityMappingCSV = "" # todo: make a style for a master identity ledger... store on offline airgapps sys with weekly? updates and sole physical backup monthly? with secure custodians (split btwn with partial images? - registered mail encrypted drives?) and then wipe Persona ea. week? on a 2-mo delayed basis? 
# that might be a bit much, and we could probably just use an authenticated sftp channel or put in Storj? 
HorizonInstance = "horizon.stellar.org"
minFeePerOp = .00001 # is there a get call for 100 stoops? in case minBaseFee changes one day 
maxNumOpsPerTxn = 100
BT_issuer = "GDRM3MK6KMHSYIT4E2AG2S2LWTDBJNYXE4H72C7YTTRWOWX5ZBECFWO7" # check for consistency for this field against other scripts

def getAllPendingTrustlinesWithAsset():
  r = "https://" + HorizonInstance + "..." + BT_issuer + "..."
  data = r.json()
  
  allPendingTrustlines = {}
  pendingTrustline = data[...]
  while(pendingTrustline):
    potentialAddress = pendingTrustline[...]
    potentialAsset = pendingTrustline[...]
    allPendingTrustlines[potentialAddress] = potentialAsset
    r = "https://" + HorizonInstance + "..." + BT_issuer + "..." -> next
    data = r.json()
    pendingTrustline = data[...]
  return allPendingTrustlines

def getKnownAddressesFromIdentityMappingCSV(inputCSV):
  allVerifiedAddresses[] = ""
  identityMapping = fopen(inputCSV)
  identityMapping.readline()
  i = -1
  while(identityMapping and i++):
    allVerifiedAddresses[i] = identityMapping.readline().split(',')[0]
  return allVerifiedAddresses

def verifyAddressesWithAssetDict(addressesWithAssetsDict):
  allKnownShareholderAddressesList = getKnownAddressesFromIdentityMappingCSV(identityMappingCSV)
  verifiedAddressesWithAssetDict = {}
  i = 0
  for potentialAddress, potentialAsset in addressesWithAssetsDict:
    if(potentialAddress in allKnownShareholderAddressesList):
      verifiedAddressesWithAssetDict[potentialAddress] = potentialAsset
  return verifiedAddressesWithAssetDict

def approveTrustlinesFromAddressAssetDict(addressesWithAssetsDict):
  bulkTxnXDR = ""
  i = 0
  for address, asset in addressesWithAssetsDict:
    if(i >= maxNumOpsPerTxn):
      break
    bulkTxnXDR.append(stellar.AuthorizeTrust(potentialAddress, ...)) # todo
    i++
  return bulkTxnXDR
  
def bulkApprovePendingTruslines():
  pendingAddressesWithAssetsDict = getAllPendingTrustlinesWithAsset()
  verifiedAddressesWithAssetsDict = verifyAddressesWithAssetDict(pendingAddressesWithAssetsDict)
  bulkTxnXDR = approveTrustlinesFromAddressAssetDict(verifiedAddressesWithAssetDict)
  #does bulkTxnXDR need to be a list or what? 
  
  
  
  # sign and export to [date, time in standard]-signedXDR-machineID-(error checking?).txt
  
  