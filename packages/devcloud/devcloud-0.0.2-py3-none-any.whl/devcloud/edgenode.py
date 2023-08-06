import requests
from .common import utils,json_data,cookies,data,validateToken
from .project import *
import json
import typer
from typing import Optional

app=typer.Typer()
class EdgeNode:
    @app.command()
    #this function will give list of edge nodes
    def getNodeDetail():
        """
        give details about all edgenodes.

        EXAMPLE:devcloud getnodedetail
        """
        validateToken()
        env=data.get('ENVIRONMENT').get('env')
        header = utils.getheader()
        resourcesUrl = utils.geturl(json_data.get(env).get("EDGENODE_ENV"), json_data.get("endPoints").get("edgenode"))
        resoucesResponse = requests.get(resourcesUrl, headers=header)
        utils.updateId()
        try:
            statusCode=resoucesResponse.status_code
            if statusCode==204:
                print("No content Available")
            elif statusCode==200:
                resourceResponseData = resoucesResponse.json()     
                mydata=[]
                head = [ "Id","processorName","integratedGpuName","memory"]
                count=0
                for dataItems in resourceResponseData: 
                        integratedGpuName =  dataItems.get('integratedGpuName')
                        processorName =  dataItems.get('processorName')
                        memory=dataItems.get('memory')
                        count=count+1
                        mydata.append([count,processorName,integratedGpuName,memory])
                utils.createTable(mydata, head)
            else:
                bytesValue = resoucesResponse.content
                myJson = json.loads(bytesValue.decode())
                print(myJson.get('message'))
        except:
            print("Unexpected Error!\n",resoucesResponse.json)        

    @app.command()
    #this function will launch the project
    def deployProject(projectName:str=typer.Option(...,"-pn","--projectname",help="enter container name"),id:int=typer.Option(...,"-i","--id",help="enter id number ")):
        """
        deploy project in devcloud container playground.

        EXAMPLE: devcloud deployproject --id "enter id number" --projectname "enter projectname"
        """
        validateToken()
        env=data.get('ENVIRONMENT').get('env')          
        header = utils.getheader()
        edgeNode = utils.geturl(json_data.get(env).get("EDGENODE_ENV"), json_data.get("endPoints").get("edgenode"))
        edgeNodeResponse = requests.get(edgeNode, headers=header)
        try:
            edgeNodeResponseData=edgeNodeResponse.json() 
            id = int(id)
            mapIDList = [nodeID for i, nodeID in enumerate(json_data["MAPPING"]) if (i+1) == int(id)]
            if len(mapIDList) == 0:
                print("ID Not found. Please use devcloud get nodedetails for help")
                os._exit(0)
            mapID = mapIDList[0].get(str(id))
            for dataItems in edgeNodeResponseData: 
                edgeNodeId=dataItems.get('id')
                if edgeNodeId==mapID:
                    cpu=dataItems.get('processorType')
                    generation =  dataItems.get('generation')
                    variant=dataItems.get('variant')

            projectId= utils.getprojectID(projectName)      
            payload=json_data.get("payloads").get("deployMultipleHardeware") 
            payload[0].update({
                "cpu":cpu,
                "edgeNodeId": mapID,
                "generation":generation,
                "projectId":projectId,
                "variant":variant
                        })  
            deployMultipleHardewareURL =utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("deployMultipleHardware"))
            podUrl=utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("pod"))
            podUrlResponse = requests.get(podUrl, headers=header)
            podUrlResponseData=podUrlResponse.json()              
            deployMultipleHardewareResponse = requests.post(deployMultipleHardewareURL, headers=header, json=payload, cookies=cookies)
            statusCode = deployMultipleHardewareResponse.status_code
            if statusCode==202:
                print("successfully launched!!")
            else:
                bytesValue = deployMultipleHardewareResponse.content
                myJson = json.loads(bytesValue.decode())
                print(myJson.get('message'))
        except:
            print("Unexpected Error!\n",edgeNodeResponse.json)        
    
    @app.command()  
    #show the status of launched project
    def getStatus(projectName:Optional[str]=typer.Option(None,"-pn","--projectname"), output: Optional[str] = typer.Option(None,"-o", "--output")):
        """
        give the status of deployed project.

        EXAMPLE: devcloud getstatus or devcloud getstatus --projectname "enter projectname" 
        """
        validateToken()
        header = utils.getheader()
        env=data.get('ENVIRONMENT').get('env')
        podUrl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("pod"))
        podResponse = requests.get(podUrl, headers=header)
        try:
            podResponseData = podResponse.json()
            mydata = []
            wide=[]
            head = ["project", "target", "status"]
            headForWide=["project", "target", "status","execution time","fps","Throughput"]
            targetStatus = None
            for i, dItems in enumerate(podResponseData.get('listProjects')):  
                projectname=dItems.get('projectDTO').get('name')          
                if projectname == projectName or projectName == "all":
                    for target in dItems.get('targets'):
                        targetStatus = target.get('targetStatus')
                        targetName = target.get('targetName')
                        if output == "wide":
                            executionTime=target.get('executionTime')
                            fps=target.get('fps')
                            for data_items in target.get('deployments'):
                                throughput=data_items.get('throughput')
                                if throughput==None or fps==None:
                                    throughput="Unavailable"
                                    fps="None"
                                else:
                                    throughput=data_items.get('throughput')
                                wide.append([projectname, targetName,targetStatus,executionTime,fps,throughput])                                           
                        mydata.append([projectname, targetName,targetStatus])                                     
                else:  
                        
                        if projectName == None:
                            for target in dItems.get('targets'):
                                targetStatus = target.get('targetStatus')
                                targetName = target.get('targetName')
                                if output == "wide":
                                    executionTime=target.get('executionTime')
                                    fps=target.get('fps')
                                    for data_items in target.get('deployments'):
                                        throughput=data_items.get('throughput')
                                        if throughput==None or fps==None:
                                            throughput="Unavailable"
                                            fps="None"
                                        else:
                                            throughput=data_items.get('throughput')
                                        wide.append([projectname, targetName,targetStatus,executionTime,fps,throughput])
                                    break
                                mydata.append([projectname, targetName,targetStatus])
                                break
            if output == "wide":
                utils.createTable(wide, headForWide)
            else:
                utils.createTable(mydata,head)
        except:
            print("Unexpected Error!\n",podResponse.json)        
    
    @app.command() 
    #show the log               
    def getlog(podName:str=typer.Option(...,"-pdn","--podname",help="enter pod name")):
        """
        give the log of given pod name.

        EXAMPLE: EXAMPLE: devcloud getlog --podname "pod name"
        """
        validateToken()
        header = utils.getheader()
        env=data.get('ENVIRONMENT').get('env')
        podUrl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("pod"))
        podResponse = requests.get(podUrl, headers=header)
        try:
            podResponseData = podResponse.json()   
            targetName = None
            targetFound = False
            for i, pItems in enumerate(podResponseData.get('listProjects')):
                for tItems in pItems.get('targets'):
                    for dItems in tItems.get('deployments'):
                        targetName = dItems.get('podName')
                        if targetName==podName:
                            targetFound= True
                            podLogUrl=utils.geturl(json_data.get(env).get("EXECUTION_ENV"), json_data.get("endPoints").get("log"))
                            url=podLogUrl.format(podName)
                            payload=json_data.get("payloads").get("podLog")  
                            payload.update({'podName':podName})                        
                            podLogResponse = requests.get(url, headers=header, json=payload, cookies=cookies)                       
                            podLogResponseData = None
                            try:
                                podLogResponseData = podLogResponse.json()
                            except ValueError:
                                print("No Content available for this pod name")
                                break
                            logs=podLogResponseData.get('logs')
                            print(*logs, sep = "\n")
                            break
            if not targetFound:
                print("couldnt find podname ") 

        except:
            print("Unexpected Error!\n",podResponse.json)
                    
    