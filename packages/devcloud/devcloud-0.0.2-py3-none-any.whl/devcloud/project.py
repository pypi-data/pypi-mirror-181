from fileinput import close
import os
import textwrap
from .common import utils, json_data, cookies,data,validateToken,loadToken
from tabulate import tabulate
import pandas as pd
import typer
import json
import requests
import jwt
import typer
from typing import Optional
app=typer.Typer()
from pathlib import Path

class Projects:
    #with the help of login function, user can login to the devcloud container playground.
    @app.command()
    def login(token: str = typer.Option(...,"-t","--token",help="enter token"),environment:Optional[str]=typer.Option("PROD","-e","--environment",hidden=True,show_default=False)):
        
        """
        login to devcloud container playground.

        EXAMPLE: devcloud login --token "enter jwt token" 
        """
        if  os.path.exists('token.json'):
            try:
                with open("token.json", 'r') as json_file:
                    data = json.load(json_file)
                    data['TOKEN']['jwt'] = token
                    data['ENVIRONMENT']['env'] = environment
                    parse_data = jwt.decode(token,options={"verify_signature" : False})
                    data['USERID']['userId'] = parse_data['userId'] 
                    data['NAMESPACE'] = parse_data['serviceName'] 
                with open("token.json", 'w') as json_file:            
                    json.dump(data, json_file)
                loadToken()
            except:
                print("Invalid Token")
        else:
            try:
                parse_data = jwt.decode(token,options={"verify_signature" : False})
                data = {"TOKEN": {"jwt": token}, "USERID": {"userId": parse_data['userId']}, "ENVIRONMENT": {"env": environment}}
                with open("token.json", 'w+') as json_file:            
                    json.dump(data, json_file)
                loadToken()
            except:
                print("Unexpected error!")        
        
    #with the use of getproject. user will get the list of projects having on devcloud container playground.  
    @app.command()
    def getProject(output: Optional[str] = typer.Option(None,"-o", "--output")): 

        """
        give project list existing in devcloud container playground.

        EXAMPLE: devcloud getproject
        """
        validateToken()
        header = utils.getheader()
        env=data.get('ENVIRONMENT').get('env')
        projectDetailsUrl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projectDetails"))
        projectDetailsResponse = requests.get(projectDetailsUrl, headers=header)
        try:
            projectDetailsResponseData = projectDetailsResponse.json()
            mydata = []
            wide=[]
            head = ["Sr.No.","project_id", "Name", "Description"]
            headForWide=["Sr.No.","project_id", "Name", "Description","Create Time"]
            count=0
            statusCode = projectDetailsResponse.status_code
            if statusCode == 200:
                for data_items in projectDetailsResponseData.get('projectContainerDTOs'):
                    projectId = data_items.get('projectId')
                    name = data_items.get('name')
                    desc = data_items.get('description')
                    if desc == None:
                        desc = ""
                    Description = textwrap.fill(desc,50)
                    count=count+1
                    if output=="wide":
                        createTime = data_items.get('createTime')
                        wide.append([count,projectId, name, Description,createTime])
                    mydata.append([count,projectId, name, Description])
                if output=="wide":
                    utils.createTable(wide,headForWide)
                else:        
                    utils.createTable(mydata, head)
            else:
                print("Unexpected Error!\n",print(projectDetailsResponse.json)) 
        except:
            print("Unexpected Error!!\n",projectDetailsResponse.json)          

    #with the help of createproject, user will be able to create a new project on devcloud container playground     
    @app.command()
    def createproject(projectName:str = typer.Option(...,"-pn","--projectname",help="enter project name "),description:str = typer.Option(...,"-d","--description",help="enter description of your project")):
            """
            create new project.

            EXAMPLE:  devcloud createproject --name "your project name" --description "your project description"
            """
            validateToken()
            header = utils.getheader()
            env=data.get('ENVIRONMENT').get('env')
            
            projectUrl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projects"))
            payload = {"name": projectName, "description": description}
            projectResponse = requests.post(projectUrl, headers=header, json=payload, cookies=cookies)
            try:
                statusCode = projectResponse.status_code
                if statusCode==201:
                    print("Project {} created!.".format(projectName))
                else:
                    bytesValue = projectResponse.content
                    myJson = json.loads(bytesValue.decode())
                    print(myJson.get('message'))
            except:
                print("Unexpected Error!\n",projectResponse.json)        
                
    #with the help of deleteproject, user will be ableto delete existing project on devcloud container playground.
    @app.command()
    def deleteProject(projectName:str = typer.Option(...,"-pn","--projectname",help="enter project name that you want to delete")):
            """
            delete the existing project.

            EXAMPLE:  devcloud deleteproject --name "project name you want to delete" 
            """
            validateToken()
            header = utils.getheader()
            env=data.get('ENVIRONMENT').get('env')
            projectDetailsUrl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projectDetails"))    
            projectDetailsResponse = requests.get(projectDetailsUrl, headers=header, cookies=cookies)
            try:
                projectDetailsResponseData = projectDetailsResponse.json()
                projectId=utils.getprojectID(projectName)    
                projecturl=   utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projects"))
                projectUrl=projecturl+"/{}".format(projectId)
                projectDetailsResponse = requests.delete(projectUrl, headers=header, cookies=cookies)
                statusCode = projectDetailsResponse.status_code
                if statusCode==200:
                    print("project {} deleted!.".format(projectName))
                else: 
                    bytesValue = projectDetailsResponse.content
                    myJson = json.loads(bytesValue.decode())
                    print(myJson.get('message'))
            except:
                print("Unexpected error!\n",projectDetailsResponse.json)        
                    
                
                







    



    
        
        