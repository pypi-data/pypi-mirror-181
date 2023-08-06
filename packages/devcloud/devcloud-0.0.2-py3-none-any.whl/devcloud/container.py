from doctest import UnexpectedException
import re
import requests
from .common import utils,json_data,cookies,data, validateToken
from .project import *
import json, os
import typer

app = typer.Typer()
class containers:
    #with the help of createcontainer function, user can create container to the devcloud container playground.
    @app.command()
    def createcontainer(containerName:str= typer.Option(...,"-cn","--containername",help="enter container name"),projectName:str= typer.Option(...,"-pn","--projectname",help="enter project name you want to assign container"),url:str=typer.Option(...,"-u","--url",help="enter url")):
        """
        create a new container for project.

        EXAMPLE:devcloud createcontainer --containername "your container name" --projectname "project name you want to assign container" --url "enter URL"
        """
        validateToken()
        env=data.get('ENVIRONMENT').get('env')
        header = utils.getheader()
        Containersurl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("containers"))
        projectId= utils.getprojectID(projectName)     
        userId= userId=  utils.getuserID() 
        payload=json_data.get("payloads").get("createcontainer") 
        payload.update({'containerName': containerName,
                          'projectId' : projectId,
                          'projectName':projectName,
                          'url':url,
                          'userId': userId
                     })          
        validateURL=utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("validateimage"))
        validateURLResponse=requests.post(validateURL, headers=header, json=payload, cookies=cookies)
        try:
            statusCode=validateURLResponse.status_code
            if statusCode==502:
                print("Invalid url or the repository is private.Please check and import again.")
                os._exit(0)
            containerResponse = requests.post(Containersurl, headers=header, json=payload, cookies=cookies)
            status_code = containerResponse.status_code    
            if status_code==201:
                print("container {} created!.".format(containerName))
            else:
                bytesValue = containerResponse.content
                myJson = json.loads(bytesValue.decode())
                print(myJson.get('message'))
        except:
            pass 
    #with the help of getcontainer function, user can get the list of containers  that available on the devcloud container playground.
    @app.command()
    def  getcontainer(output: Optional[str] = typer.Option(None,"-o", "--output")):
        """
        give a list of containers exists in devcloud container playground.

        EXAMPLE: devcloud getcontainer
        """

        validateToken()
        env=data.get('ENVIRONMENT').get('env')
        header = utils.getheader()
        resourcesUrl = utils.geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("resources"))
        resoucesResponse = requests.get(resourcesUrl, headers=header)
        projectDetailsUrl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projectDetails"))
        projectDetailsResponse = requests.get(projectDetailsUrl, headers=header)
              
        try:
            projectDetailsResponseData = projectDetailsResponse.json()
            statusCode=resoucesResponse.status_code
            if statusCode==204:
                print("No content Available")
            elif statusCode==200:
                resourceResponseData = resoucesResponse.json()  
                mydata=[]
                wide=[]
                head = [ "Sr.No.","Container Id ", "Container Name"]
                headOfWide=["Sr.No.","Container Id ", "Container Name","Project Name"]
                count=0
                for dataItems in resourceResponseData.get('response'): 
                        ContainerId = dataItems.get('containerId')
                        ContainerName=dataItems.get('resourceName')    
                        count=count+1
                        if output=="wide":
                            projectID=dataItems.get('projectIds')
                            if projectID==None:
                                name="None"
                                wide.append([count,ContainerId,ContainerName,name])
                            else:
                                projectID=dataItems.get('projectIds')[0]    
                            for data_items in projectDetailsResponseData.get('projectContainerDTOs'):
                                projectId = data_items.get('projectId')
                                if projectId==projectID:
                                    name = data_items.get('name')
                                    wide.append([count,ContainerId,ContainerName,name])
                        mydata.append([count,ContainerId,ContainerName])
                if output=="wide":       
                    utils.createTable(wide, headOfWide)

                else:
                    utils.createTable(mydata, head)   
            else:
                print("Unexpected Error!",projectDetailsResponse.json)        
        except:
            print("Unexpected Error!\n",projectDetailsResponse.json)    
    #with the help of deletecontainer function, user can delete particular container from devcloud container playground.    
    @app.command()    
    def deletecontainer(containerName:str=typer.Option(...,"-cn","--containername",help="enter container name you want to delete")):
        """
        delete container of the project.

        EXAMPLE:  devcloud deletecontainer --containername "container name you want to delete"
        """
        validateToken()
        header = utils.getheader()
        env=data.get('ENVIRONMENT').get('env')
        resourcesUrl = utils.geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("resources"))
        resoucesResponse = requests.get(resourcesUrl, headers=header, cookies=cookies)
        try:
            resourceResponseData = resoucesResponse.json()
            project_id = None
            projectExists = False
            for dataItems in resourceResponseData.get('response'):
                    resouceName = dataItems.get('resourceName')   
                    name = re.split(":", resouceName)
                    if containerName == name[0]: 
                        projectExists = True
                        resoucename = dataItems.get('resourceName')
                        assignmentStatus=dataItems.get('projectAssignStatus')
                        if assignmentStatus == True:
                            project_id = dataItems.get('projectIds')
                            project_Id=project_id[0]  
                        else:
                            project_Id = None
            if not projectExists:
                print("The container name does not exists")
                os._exit(0) 

            projectDetailsUrl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projectDetails"))
            projectDetailsResponse = requests.get(projectDetailsUrl, headers=header, cookies=cookies)
            projectDetailsResponseData = projectDetailsResponse.json()        
            for data_items in projectDetailsResponseData['projectContainerDTOs']:
                    project_ID = data_items.get('projectId')    
                    if project_Id == project_ID:
                        project_name= data_items.get('name')                   
            if assignmentStatus==True:
                print("container " + containerName +" is assign to project " +project_name + ", please unassign that first")        
            else:
                    deleteUrl= utils.geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("deleteBuild"))
                    url=deleteUrl.format(resoucename)
                    deleteResponse = requests.delete(url, headers=header, cookies=cookies)
                    statusCode = deleteResponse.status_code
                    if statusCode==200:
                        print("Container {} deleted!.".format(containerName))
                    else:
                        bytesValue = deleteResponse.content
                        myJson = json.loads(bytesValue.decode())
                        print(myJson.get('message'))
        except:
            print("Unexpected Error!\n",resoucesResponse.json)                

                       

    #with the help of unassigncontainer function, user can unassign container on the devcloud container playground.  
    @app.command()           
    def unassigncontainer(containerName:str=typer.Option(...,"-cn","--containername",help="enter container name"),projectName:str=typer.Option(...,"-pn","--projectname",help="enter project name")):
            """
            unassign container of the project.

            EXAMPLE: devcloud unassigncontainer --containername "container name "
            """
            validateToken()
            header = utils.getheader()
            env=data.get('ENVIRONMENT').get('env')
            projectDetailsUrl = utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("projectDetails"))
            projectDetailsResponse = requests.get(projectDetailsUrl, headers=header, cookies=cookies)
             
            try:
                projectDetailsResponseResponseData = projectDetailsResponse.json() 
                project_Id= utils.getprojectID(projectName)
                count=0
                resourcesUrl = utils.geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("resources"))
                resoucesResponse = requests.get(resourcesUrl, headers=header, cookies=cookies)
                resourceResponseData = resoucesResponse.json()
                for dataItems in resourceResponseData.get('response'):
                    resouceName = dataItems.get('resourceName')   
                    name = re.split(":", resouceName)
                    if containerName == name[0]: 
                        assignmentStatus=dataItems.get('projectAssignStatus')
                        if assignmentStatus == False:
                            print("container is already unassigned")
                            os._exit(0)
                
                container_name=False
                for dataItems in projectDetailsResponseResponseData.get('projectContainerDTOs'):
                    name = dataItems.get('name')
                    count=count+1
                    for i in range (0,count):
                        if name == projectName:
                            for items in projectDetailsResponseResponseData['projectContainerDTOs'][count-1]['containers']:
                            #for items in projectDetailsResponseResponseData.get('projectContainerDTOs')[count-1].get('containers'):
                                resourceName =  items.get('containerName')
                                if resourceName==containerName:
                                    container_Id = items.get('containerId') 
                                    container_name = True
                                    break

                if container_name==False:
                    print("container name not exist")    
                    os._exit(0)   
                payload=json_data.get("payloads").get("unassignContainer")  
                payload.update({'containerId':container_Id,
                                'projectId':project_Id,
                                'resourceName':containerName
                                })              
                unassignUrl= utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("unassignContainer"))
                unassignResponse = requests.post(unassignUrl, headers=header, json=payload, cookies=cookies)          
                stausCode = unassignResponse.status_code
                if stausCode == 200:
                    print("Container {} Unassigned!.".format(containerName))
                else:
                    bytesValue = unassignResponse.content
                    myJson = json.loads(bytesValue.decode())
                    print(myJson.get('message'))
            except:  
                print("Unexpected Error!\n",projectDetailsResponse.json)      
                    
    #with the help of assigncontainer function, user can assign container to particular project on the devcloud container playground.
    @app.command()
    def assigncontainer(containerName:str=typer.Option(...,"-cn","--containername",help="enter container name"),projectName:str=typer.Option(...,"-pn","--projectname",help="enter project name")):     
            """
            assign container to the project.

            EXAMPLE: devcloud assigncontainer --containername "container name " --projectname "project to which you want to assign the container"
            """
            validateToken()
            header = utils.getheader()
            env=data.get('ENVIRONMENT').get('env')
            assignUrl= utils.geturl(json_data.get(env).get("BYOC_ENV"), json_data.get("endPoints").get("containers"))
            containersResponse = requests.get(assignUrl, headers=header, cookies=cookies)
            try:
                responseData = containersResponse.json()  
                container_name=False
                for data_items in responseData.get('resources'):
                    name = data_items.get('resourceName')
                    if containerName == name:
                        containerId = data_items.get('containerId')
                        container_name=True
                        break
                if container_name==False:
                    print("container name not exist")     
                    os._exit(0) 
                userId=  utils.getuserID()
                projectId= utils.getprojectID(projectName)
                payload=json_data.get("payloads").get("assignContainer")  
                payload.update({'containerId':containerId,'containerName':containerName,'projectId':projectId,'url':projectName,'userId':userId})
                assignResponse = requests.post(assignUrl, headers=header, json=payload, cookies=cookies)
                assignResponseData = assignResponse.json()
                staus_code = assignResponse.status_code       
                if staus_code == 201:
                    print("Container " + containerName +" assigned to project " +projectName)
                else:
                    bytesValue = assignResponse.content
                    myJson = json.loads(bytesValue.decode())
                    print(myJson.get('message'))
            except:
                print("Unexpected Error!\n",containersResponse.json)
    
    def createConfiguration(projectName: str, containerName: str, port: list=[], label: list=[], entryPoint: str="", outputPath: str="", mountPath: list=[()], environment: str=""):
        #{"additionalConfig":"","containerId":489303,"containerName":"container1","dependentOn":[],"entryPoint":"/s3/run.sh","mountPoint":"","port":"","projectId":489302,"newTags":[],"cancelledTags":[],"toStorage":"","routeEnabledPort":"","inputPaths":["/s3/train2infer"],"containerPaths":["/s3"]}
        #https://frontend.apps.cfa.devcloud.intel.com/config/api/v1/container/createConfiguration
        #POST
        validateToken()
        env=data.get('ENVIRONMENT').get('env')
        header = utils.getheader()
        containerID = containers.getContainerId(containerName)
        projectId= utils.getprojectID(projectName)    
        payload=json_data.get("payloads").get("createContainer")
        inputPaths, containerPaths = list(map(list, zip(*mountPath)))
        payload.update({'additionalConfig':environment,
                'containerId':containerID,
                'containerName':"",
                'dependentOn':[],
                'entryPoint':entryPoint,
                'mountPoint':outputPath,
                'port':','.join(port),
                'projectId':projectId,
                'newTags':label,
                'cancelledTags':[],
                'toStorage':"",
                'routeEnabledPort':"",
                'inputPaths':inputPaths,
                'containerPaths':containerPaths
            })          
        configurationURL = utils.geturl(json_data.get(env).get("CONFIG_ENV"), json_data.get("endPoints").get("configuration"))
        response = requests.post(configurationURL, headers=header, json=payload, cookies=cookies)
        status_code = response.status_code       
        if status_code == 200:
            print("Updated the configuration!!")
        else:
            print("Configuration update failed")

    def getContainerId(containerName: str) -> int:
        header = utils.getheader()
        env=data.get('ENVIRONMENT').get('env')
        resourcesUrl = utils.geturl(json_data.get(env).get("BYOS_ENV"), json_data.get("endPoints").get("resources"))
        resoucesResponse = requests.get(resourcesUrl, headers=header, cookies=cookies)
        project_id = None
        projectExists = False
        containerId = None
        try:
            resourceResponseData = resoucesResponse.json()
            for dataItems in resourceResponseData.get('response'):
                    resouceName = dataItems.get('resourceName')   
                    name = re.split(":", resouceName)
                    if containerName == name[0]: 
                        projectExists = True
                        containerId = dataItems.get('containerId')
                        assignmentStatus=dataItems.get('projectAssignStatus')
                        if assignmentStatus == True:
                            project_id = dataItems.get('projectIds')
                            project_Id=project_id[0]  
                        else:
                            project_Id = None
            if not projectExists: 
                raise Exception("No container");                
        except:  
            print("Unexpected Error!\n",projectDetailsResponse.json)  
            raise Exception("Failed to get container")
        return containerId