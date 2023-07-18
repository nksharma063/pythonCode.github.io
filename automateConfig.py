import os
from pathlib import Path
import time
import json
from pymongo import MongoClient
from flask import Flask,jsonify

# def userDirFile():
#     path = input("Please enter the path to files: ")
# #     file = input("Please enter the file names with appropriate extension with comma ")
# #     fileNew = list(file)
# #     # Check the operating system
#     if os.name == 'nt':  # Windows
#         path = path.replace('/', '\\').replace('\\', '\\\\')
#         path.replace(' ', '')

#     else:
#         path = path.replace(' ', '')
    
#     return path


def readDirFileLocation(file):
    # path = userDirFile()
    path = os.getcwd()
    # dir = os.path.isdir(path)
    if not os.path.isdir(path):  # if path is not  valid
        print("Please enter the valid directory")
    else:
        result = []        
        # for each in os.scandir(path):
        for each in Path(path).iterdir():  #two operation found in os module scadr and iterddir fro Path module, tried both, iter module seems to be givig the path with file name to process further.
            if each.is_file() and each.name in file:   #Checking whether the file name and it is file matches
                result.append(str(each))
            # if each.name == file and each.is_file():
        return result
# print(readDirFileLocation(['server.yml','database.yml']))





def extractdata(file):
    database,server =  readDirFileLocation(file)  #Reading content based from previous list result
    #  print(database, server)
    finalDatabaseDict = {}
    finalServerDict = {}
    with open(database, 'r') as f:     
        for each in f:  # Readinge ach in line from result
            # print(each)
            if '=' in each:    #if = is there , we could have replace with any fucntion
                key, value = each.strip().split('=')  # We are stripping and rmeoving any content and splitting based on special variable
                finalDatabaseDict[key] = value # appendig the value to dictionary
                continue
            else:
                pass 
    with open(server, 'r') as f:
        for each in f:
            # print(each)
            if '=' in each:
                key, value = each.strip().split('=')
                finalServerDict[key] = value
                continue
            else:
                pass
    return [finalDatabaseDict, finalServerDict]
print(extractdata(['server.yml','database.yml']))

def storeDatabase(file):
    finalDatabaseDict, finalServerDict = extractdata(file)

    client = MongoClient('mongodb+srv://nksharma063:Her0V1red%4012345@cluster0.gdlcigy.mongodb.net/')
    db = client['PythonAssignment']
    database = db['databaseCred']  #creating collection database
    server = db['severCred']   # creating collection server

    databaseJSON = json.loads(finalDatabaseDict)  #Loading data in to json format
    serverJSON = json.loads(finalServerDict)

    database.insert_one(databaseJSON)  #Inserting the data as json format
    server.insert_one(serverJSON)

    return database     # extracting teh data from dict and storing in json format using pymomgo, json and creating object these classes



app = Flask(__name__)
app.route('/')
def get_data(file):
    return storeDatabase(file)

    







# print(userDirFile())
# path, file = userDirFile()
# print(f"Path: {path}")
# print(f"File: {file}")