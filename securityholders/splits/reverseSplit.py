import sys
sys.path.append("../../")
from globals import *

# testing: forwardSplit("StellarMart", 1, 10, "preSplitVeryRealStockIncMSF.csv")
def reverseSplit(queryAsset, numerator, denominator, MSFpreSplitBalancesCSV):
  try:
    secretKey = sys.argv[1]
  except:
    print("Running without key")
  postSplitFileName = "[BACKWARDS] {} Post-Split Master Securityholder File.csv".format(queryAsset)
  numerator = Decimal(numerator)
  denominator = Decimal(denominator)
  assert numerator < denominator 
  StellarBlockchainBalances = getStellarBlockchainBalances(queryAsset)
  outputPostSplitMSFwithUnclaimedShareholdersOnly = revokeMSFreverseSplitSharesUnclaimedOnStellarInclRestricted(MSFpreSplitBalancesCSV, numerator, denominator)
  newShareTxnArr = grantNewSplitSharesFromBalancesClaimedOnStellar(StellarBlockchainBalances, queryAsset, numerator, denominator)
  exportSplitNewShareTransactions(newShareTxnArr)
  generateFinalPostSplitMSF(outputPostSplitMSFwithUnclaimedShareholdersOnly, MSFpreSplitBalancesCSV)
  
  # Create burn ops per split ratio
  transactions[idx].append_clawback_op(
    asset = Asset(queryAsset, BT_ISSUER),
    from = address,
    amount = ("{:." + MAX_NUM_DECIMALS + "f}").format(sharesToClawback),
  )


  

def revokeMSFreverseSplitSharesUnclaimedOnStellarInclRestricted(MSFpreSplitBalancesCSV, numerator, denominator, queryAsset):
  MSF = open(MSFpreSplitBalancesCSV, "r")
  oldMSF = MSF.read()
  oldMSF = oldMSF.strip()
  oldMSF = oldMSF.split("\n")
  MSF.close()
  newMSF = open(postSplitFileName, "w")
  newMSF.write(oldMSF[0] + "\n")
  for shareholder in oldMSF[1:]: # Assume restricted entries are separate from unrestricted entries 
    shareholder = shareholder.split(",")
    if(shareholder[0] == ""):
      sharesAfterSplit = Decimal(shareholder[1]) * numerator / denominator
      shareholder[1] = str(sharesAfterSplit)
      newMSF.write(",".join(shareholder) + "\n")
  newMSF.close()
  return newMSF

def grantNewSplitSharesFromBalancesClaimedOnStellar(StellarBlockchainBalances, queryAsset, numerator, denominator):
  server = Server(horizon_url= "https://" + HORIZON_INST)
  distributor = server.load_account(account_id = BT_DISTRIBUTOR)
  try: 
    fee = server.fetch_base_fee()
  except: 
    fee = FALLBACK_MIN_FEE
  transactions = []
  transactions.append(
    TransactionBuilder(
      source_account = distributor,
      network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE,
      base_fee = fee,
    )
  )
  reason = "{}-for-{} forward stock split".format(numerator, denominator)
  numTxnOps = idx = 0
  for addresses, balances in StellarBlockchainBalances.items():
    sharesToPay = (balances * numerator / denominator) - balances
    if(sharesToPay):
      numTxnOps += 1
      transactions[idx].append_payment_op(
        destination = addresses,
        asset = Asset(queryAsset, BT_ISSUER),
        amount = ("{:." + MAX_NUM_DECIMALS + "f}").format(sharesToPay),
      )
    if(numTxnOps >= MAX_NUM_TXN_OPS):
      transactions[idx] = transactions[idx].add_text_memo(reason).set_timeout(7200).build()
      transactions[idx].sign(Keypair.from_secret(secretKey))
      numTxnOps = 0
      idx += 1
      transactions.append(
        TransactionBuilder(
          source_account = distributor,
          network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE,
          base_fee = fee,
        )
      )
  transactions[idx] = transactions[idx].add_text_memo(reason).set_timeout(7200).build()
  transactions[idx].sign(Keypair.from_secret(secretKey))
  return transactions

def exportSplitNewShareTransactions(txnArr):
  for txns in txnArr:
    output = open(str(datetime.now()) + " forwardSplitPaymentXDR.txt", "w")
    output.write(txns.to_xdr())
    output.close()

def generateFinalPostSplitMSF(outputMSF, MSFpreSplitBalancesCSV, queryAsset):
  finalMSF = open(postSplitFileName, "a")
  oldMSF = open(MSFpreSplitBalancesCSV, "r")
  readData = oldMSF.read()
  readData = readData.strip()
  readData = readData.split("\n")
  oldMSF.close()
  for shareholder in readData[1:]:
    shareholder = shareholder.split(",")
    if(shareholder[0]):
      finalMSF.write(",".join(shareholder) + "\n")
  finalMSF.close()

