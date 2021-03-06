import sys
sys.path.append("../../")
from globals import *

def generatePostSplitMSF(MSFpreSplitBalancesCSV, numerator, denominator, postSplitFileName):
  MSF = open(MSFpreSplitBalancesCSV, "r")
  oldMSF = MSF.read()
  oldMSF = oldMSF.strip()
  oldMSF = oldMSF.split("\n")
  MSF.close()
  newMSF = open(postSplitFileName, "w")
  newMSF.write(oldMSF[0] + "\n")
  for shareholder in oldMSF[1:]:
    shareholder = shareholder.split(",")
    if(shareholder[1]):
      sharesAfterSplit = Decimal(shareholder[1]) * numerator / denominator
      shareholder[1] = ("{:." + MAX_NUM_DECIMALS + "f}").format(sharesAfterSplit)
      newMSF.write(",".join(shareholder) + "\n")
    else:
      newMSF.write(",".join(shareholder) + "\n")
  newMSF.close()
  return newMSF

def exportSplitNewShareTransactions(txnArr, queryAsset):
  for txns in txnArr:
    output = open(f"{str(datetime.now()).replace(":",".")} {queryAsset} StockSplitOutputXDR.txt", "w")
    output.write(txns.to_xdr())
    output.close()

