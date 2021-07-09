import requests
import json
from pprint import pprint

BTissuerAddress = 'GD3VPKNLTLBEKRY56AQCRJ5JN426BGQEPE6OIX3DDTSEEHQRYIHIUGUM'

def getAllAccountApplicationsFromKYC(secretKeyBlockpass):
  r = requests.get('https://kyc.blockpass.org/kyc/1.0/connect/Block_Transfer/applicants', headers = {'Authorization': secretKeyBlockpass} )
  data = r.json()
  fullDataRecords = data['data']['records']
  allKYCidentities = []
  for identities in fullDataRecords:
    recordName = identities['identities']['given_name']['value'] + ' ' + identities['identities']['family_name']['value']
    recordStatus = identities['status']
    addressDictFromStrDict = json.loads(identities['identities']['address']['value'])
    recordPhysicalAddress = addressDictFromStrDict['address'] + ', ' + addressDictFromStrDict['extraInfo'] + ', ' + addressDictFromStrDict['city'] + ', ' + addressDictFromStrDict['state'] + ' ' + addressDictFromStrDict['postalCode'] + ', ' + addressDictFromStrDict['country']
    # recordStellarAddress = # coming soon, manual for now
    allKYCidentities.append((recordName, recordPhysicalAddress, recordStatus))
  return allKYCidentities

def allSuccessfulCandidatesOnly(allKYCidentities):
  successfulCandidates = []
  for identities in allKYCidentities:
    if identities[2] == 'approved':
        successfulCandidates.append((identities[0], identities[1]))
  return successfulCandidates

def mergeSuccessfulCandidateAccountsWithUserProvidedStellarAddress(successfulCandidates, MSF):

def getStellarAccountsAlreadySponsored(BTissuerAddress):
  #dlsps
  return accountsAlreadySponsored

def removeExistingAccountsFromSuccessfulCandidates(successfulCandidates, accountsAlreadySponsored):
  ##
  return remainingAccountsPassedKYCyetNotSponsored

def sponsorAccountCreation(remainingAccountsPassedKYCyetNotSponsored):
  # Generate bulk ops. in groups of 100 to be signed offline and broadcast
  # to create an account / sponsor trustline
  # send 2.01 XLM # enough for 3 trustlines and 1000 transfers or 1 trustline and 150,000 transfers
  return True

def goFromKYCrequestToSponsoringAccounts(secretKeyBlockpass, BTissuerAddress):
  allKYCidentities = getAllAccountApplicationsFromKYC(secretKeyBlockpass)
  successfulCandidates = allSuccessfulCandidatesOnly(allKYCidentities)
  accountsAlreadySponsored = getStellarAccountsAlreadySponsored(BTissuerAddress)
  remainingAccountsPassedKYCyetNotSponsored = removeExistingAccountsFromSuccessfulCandidates(successfulCandidates, accountsAlreadySponsored)
  sponsorAccountCreation(remainingAccountsPassedKYCyetNotSponsored)


#pprint(getAllAccountApplicationsFromKYC('c3820f100433fb7012639110fe4136d7'))
#print("\n\n Full Attributes \n\n")
allKYCidentities = getAllAccountApplicationsFromKYC('5c1fa7cd86481dea2145d6151be0014f')
pprint(allSuccessfulCandidatesOnly(allKYCidentities))