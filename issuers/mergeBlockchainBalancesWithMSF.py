import requests
from datetime import date

searchLimitMax200 = '200'
horizonInstance = 'horizon.stellar.org'
BTissuerAddress = 'GD3VPKNLTLBEKRY56AQCRJ5JN426BGQEPE6OIX3DDTSEEHQRYIHIUGUM'

# With "VeryRealStockIncMSF.csv", use "StellarMart" as queryAsset and any numRestrictedShares
def getMergedReportForAssetWithNumRestrictedSharesUsingMSF(queryAsset, numRestrictedShares, MSF):
  StellarBlockchainBalances = getStellarBlockchainBalances(queryAsset)
  totalOutstandingShares = getTotalOutstandingShares(queryAsset, numRestrictedShares)
  didSucceed = mergeBlockchainRecordsWithMSF(MSF, totalOutstandingShares, StellarBlockchainBalances)
  return didSucceed

def getStellarBlockchainBalances(queryAsset):
  StellarBlockchainBalances = {}
  requestAddress = 'https://' + horizonInstance + '/accounts?asset=' + queryAsset + ':' + BTissuerAddress + '&limit=' + searchLimitMax200
  r = requests.get(requestAddress)
  data = r.json()
  blockchainRecords = data['_embedded']['records']
  while(blockchainRecords != []):
    for accounts in blockchainRecords:
      accountAddress = accounts['id']
      for balances in accounts['balances']:
        if balances['asset_type'] != 'native' and balances['asset_code'] == queryAsset:
          accountBalance = float(balances['balance'])
          break
      StellarBlockchainBalances[accountAddress] = accountBalance
    # Go to next cursor
    requestAddress = data['_links']['next']['href'].replace('%3A', ':')
    r = requests.get(requestAddress)
    data = r.json()
    blockchainRecords = data['_embedded']['records']
  return StellarBlockchainBalances

def getTotalOutstandingShares(queryAsset, numRestrictedShares):
  requestAddress = 'https://' + horizonInstance + '/ledgers?asset=' + queryAsset + ':' + BTissuerAddress
  r = requests.get(requestAddress)
  data = r.json()
  numUnrestrictedShares = float(data['_embedded']['records'][len(data['_embedded']['records']) - 1]['total_coins'])
  totalOutstandingShares = numRestrictedShares + numUnrestrictedShares
  return totalOutstandingShares

def mergeBlockchainRecordsWithMSF(MSF, totalOutstandingShares, StellarBlockchainBalances):
  inFile = open(MSF)
  readFile = inFile.read()
  readFile = readFile.strip()
  readFile = readFile.split('\n')
  inFile.close()
  mergedMSF = open('mergedMSF.csv', 'w+')
  today = date.today()
  mergedMSF.write('Shares as of {},Percent of Total Shares,Registration,Email,Date of Birth / Organization,Address,Address Extra,City,State,Postal Code,Country,Onboarded Date,Issue Date of Security,Cancellation Date of Security,Restricted Shares Notes\n'.format(today))
  for lines in readFile[1:]:
    lines = lines.split(',')
    sharesNotYetClaimedOnStellar = 0 if lines[1] == '' else float(lines[1])
    try:
        blockchainBalance = 0 if lines[0] == '' else StellarBlockchainBalances[lines[0]]
    except KeyError:
        # This address is no longer a securityholder per removed trustline. Prune from merged MSF
        continue
    totalBalance = blockchainBalance + sharesNotYetClaimedOnStellar # perhaps string addition here, but float precision should suffice given this is for reading only, not reporting
    lines[0] = str(totalBalance)
    lines[1] = str(100 * totalBalance / totalOutstandingShares)
    mergedMSF.write(','.join(lines) + '\n')
  mergedMSF.close()
  return True




getMergedReportForAssetWithNumRestrictedSharesUsingMSF("StellarMart", 10000, "VeryRealStockIncMSF.csv")
