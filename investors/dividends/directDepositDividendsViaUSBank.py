# I, John Wooten of my own free will, hereby authorize U.S. Bank to freely use any materials
# disclosed herein for the distribution of secuirty dividends among its clients or affiliates.

# Import MSF -> Record Date via StellarNonNative in blocktransfer/record-date repo

import requests
import json
from datetime import datetime

USBankMoneyMovementSimAPI = "https://alpha-api.usbank.com/innovation/bank-node/money-movement/v1/"
USBankCoreBankingAPI = "https://alpha-api.usbank.com/innovation/bank-node/customer-accounts/v1/"
USBankAPIkey = "6HKCcpr2jijlT0H1QfluoNZ6NutndJNA"
USBankSecret = "pS5I39aTLkuPDsJk"
USBankAuthorization = "Basic NkhLQ2NwcjJqaWpsVDBIMVFmbHVvTlo2TnV0bmRKTkE6cFM1STM5YVRMa3VQRHNKaw=="
USBankCustomerID = "6700658872"
BlockTransferDividendsPayableAccountNum = "936606647590"
USBankAccountID = "947714798707"

def directDepositDividendsViaUSBank(recordDateShareholdersOptedForCashDividendsCSV, perShareDividend):
  USBankAPIheaders = {
    "Accept": "application/json",
    "Authorization": USBankAuthorization,
    "Content-Type": "application/json"
  }
  inFile = open(recordDateShareholdersOptedForCashDividendsCSV)
  readFile = inFile.read()
  readFile = readFile.strip()
  readFile = readFile.split("\n")
  inFile.close()
  print("*****\n\nDistributing dividend of $" + str(perShareDividend) + " per share\n\n*****\n")
  divSum = 0
  investorSum = 0
  mergedDirectDividendsMSF = open(f"Direct deposit dividends distributed on {datetime.now().date()}.csv", "a")
  mergedDirectDividendsMSF.write("Dividends Paid,Registration,Email,Routing # Direct Deposit,Account # Direct Deposit,Card # Card Deposit,Card CVV Card Deposit,Expiration Date Card Deposit,Billing Zip Card Deposit,For Internal Use: Card ID,Address,Address Extra,City,State,Postal Code,Country\n")
  mergedDirectDividendsMSF.close()
  for lines in readFile[1:]:
    lines = lines.split(",")
    if lines[5] != "": continue
    shareholderDividend = float(lines[0]) * perShareDividend
    USBankAPIbody = {
      "accountID": BlockTransferDividendsPayableAccountNum,
      "amount": float(f"{shareholderDividend if shareholderDividend <= 10000 else 10000:.2f}"),
      "party": lines[1].replace("&", "and").replace(",", "").replace(".", "").replace("-", " ")
    }
    if USBankAPIbody["amount"] <= 0.00: continue
    r = requests.post(USBankMoneyMovementSimAPI + "activity/withdrawal",  headers = USBankAPIheaders, data = json.dumps(USBankAPIbody))
    try: transactionID = r.json()["transactionID"]
    except: continue
    mergedDirectDividendsMSF = open("Direct deposit dividends distributed on {datetime.now().date()}.csv", "a")
    mergedDirectDividendsMSF.write(",".join([f"{shareholderDividend:.2f}", lines[1], lines[2], lines[3], lines[4], "", "", "", "", "", lines[10], lines[11], lines[12], lines[13], lines[14], lines[15]])+"\n")
    mergedDirectDividendsMSF.close()
    print("*** {lines[1]} compensated ${shareholderDividend:.2f} via dividend withdrawal #{transactionID} ***\n")
    divSum += shareholderDividend
    investorSum += 1
    #break # testing: prevent MAX_CARDS
  print("\n*****\n\nTotal of ${divSum:.2f} cash dividends direct deposited to {investorSum} securityholders\n\n*****\n")

directDepositDividendsViaUSBank("demoCashDividendsMSF.csv", .0023)
