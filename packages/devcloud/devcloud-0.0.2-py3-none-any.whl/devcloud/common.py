from fileinput import close
import importlib.resources
import json
import os
import requests
import textwrap
import jwt
import typer
import pandas as pd
from tabulate import tabulate

app = typer.Typer()
cookies = {
    'XSRF-TOKEN': 'devcloud'
} 
with importlib.resources.open_text("devcloud","environment.json") as json_file:
    json_data = json.load(json_file)
data = {}       

def loadToken():
    if os.path.exists("token.json"):
        with open("token.json", 'r') as json_file:
            data.update(json.load(json_file))

loadToken()

def validateToken():
    if not os.path.exists('token.json'): 
        with open("token.json", 'w+') as json_file:
            data = {"TOKEN": {"jwt": ""}, "USERID": {"userId":0}, "ENVIRONMENT": {"env": ""}, "NAMESPACE": ""}
            json.dump(data,json_file)   
    with open("token.json", 'r') as json_file:
        data = json.load(json_file) 
        if data.get("TOKEN").get('jwt') == "":
            print("Error: JWT Token missing")
            os._exit(0) 
         
class utils():
    def geturl(host: str, endPoint: str):
        try:
            url = host + endPoint
            return url
        except:
            print("Unexpected Error!\n")  
            os._exit(0)  

    def getheader():
        with open("token.json", 'r') as json_file:
            data = json.load(json_file)
            jwt = data.get('TOKEN').get('jwt')
        header = {
            'Authorization': 'Bearer {}'.format(jwt),
            "X-XSRF-TOKEN": 'devcloud',
            "Cookie": 'token={};XSRF-TOKEN={}'.format(jwt,'devcloud')}
        return header

    def getjwt():
        return data.get("TOKEN").get('jwt')

    def getuserID():        
        return data.get('USERID').get('userId')

    def getUserNamespace():
        return data.get("NAMESPACE")

    def getRequest(host: str, endPoint: str, header: dict = {}):
        header = utils.getheader()
        response = requests.get(utils.geturl(host, endPoint), headers=header)
        return response
       
    def createTable(mydata:list,head:list):        
        dataframe = pd.DataFrame(mydata, columns=head)
        pd.set_option('display.colheader_justify', 'center')
        print(tabulate(dataframe, headers=head,stralign="center", tablefmt="grid",showindex="never"))
        
    def getprojectID(project_name:str):
            header = utils.getheader()
            env=data.get('ENVIRONMENT').get('env')
            projectDetailsUrl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projectDetails"))
            projectDetailsResponse = requests.get(projectDetailsUrl, headers=header, cookies=cookies)
            try:
                response_data = projectDetailsResponse.json()
                projectExists = False     
                for data_items in response_data.get('projectContainerDTOs'):
                    Name = data_items.get('name')
                    if project_name == Name:
                        projectExists = True
                        project_Id = data_items.get('projectId')
                if not projectExists:
                    print("The project name does not exists")
                    os._exit(0)         
                return project_Id    
            except:
                print("Unexpected Error!\n",projectDetailsResponse.json)  
                os._exit(0)    
    def getcontainerID(containerName:str):
        header = utils.getheader()
        env=data.get('ENVIRONMENT').get('env')
        assignUrl= utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("containers"))
        containersResponse = requests.get(assignUrl, headers=header, cookies=cookies)
        try:
            responseData = containersResponse.json()  
            for data_items in responseData.get('resources'):
                name = data_items.get('resourceName')
                if containerName == name:
                    containerId = data_items.get('containerId')
            return containerId  
        except:
            print("Unexpected Error!\n",containersResponse.json)   
            os._exit(0)

    def updateId():
        validateToken()
        env=data.get('ENVIRONMENT').get('env')          
        header = utils.getheader()
        edgeNode = utils.geturl(json_data.get(env).get("EDGENODE_ENV"), json_data.get("endPoints").get("edgenode"))
        edgeNodeResponse = requests.get(edgeNode, headers=header)
        try:
            resourceResponseData=edgeNodeResponse.json()
            with importlib.resources.open_text("devcloud","environment.json") as json_file:
                    dataJson = json.load(json_file)
                    j=0
                    mapId = []
                    for dataItems in resourceResponseData: 
                        id=dataItems.get('id')
                        j=j+1
                        mapId.append({j:id})
                    dataJson['MAPPING'] = mapId 
                    with open(importlib.resources.path("devcloud","environment.json"), 'w+') as json_file:  
                        json.dump(dataJson, json_file)  
        except:
            print("Unexpected Error\n",edgeNodeResponse.json)