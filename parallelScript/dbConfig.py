#Do not commit login info to github !!
#There is security risk to leak the ip address of our mongodb server
from pymongo import MongoClient
HOSTNAME = "xxx.xxx.xxx.xxx"
USERNAME = "xxxx"
PASSWORD = "xxxxxx"
client = MongoClient(HOSTNAME, 27017)
client["admin"].authenticate(USERNAME, PASSWORD)
staticAnalysisDB = client['staticAnalysis']
androidAppDB = client['androidApp']
