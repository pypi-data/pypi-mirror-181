from os import access
from typing import List
from unittest import result
from .project import Projects
from .container import containers 
from .edgenode import EdgeNode
import getpass
from .result import mount, cloudImport, getFilePreview

class Devcloud:
    def connect(token: str = ""):
        if len(token) == 0:
            token = getpass.getpass("Token:")
            Projects.login(token, "PROD")
            print("LoggedIn")
            print("Overview - Project")
            Projects.getProject("wide")
            print("Overview - Dashboard")
            EdgeNode.getStatus("all", "wide")

    def transfer(region: str, bucketName: str, path: List, accessKey: str="", secretKey: str=""):
        if len(accessKey) == 0:
            accessKey = getpass.getpass("Access Key:")
        if len(secretKey) == 0:
            secretKey = getpass.getpass("Secret Key:")
        mount(accessKey, secretKey, region, bucketName)
        cloudImport(path, bucketName)

    def createContainer(projectName: str, containerName: str, url: str):
        Projects.createproject(projectName, "")
        containers.createcontainer(containerName, projectName, url)
        #containers.assigncontainer(containerName, projectName)

    
    def configureContainer(projectName: str, containerName: str, port: list, label: list, entryScript: str, output: str, mountPoint: list, environment: str):
        containers.createConfiguration(projectName, containerName, port, label, entryScript, output, mountPoint, environment)

    def availableHardware():
        EdgeNode.getNodeDetail()

    def launch(projectName: str, edgeNode: int):
        EdgeNode.deployProject(projectName, edgeNode)

    def getStatus():
        EdgeNode.getStatus("all", "wide")

    def getProject():
        Projects.getProject("wide")
    
    def previewOutput(path: str, type: str = "jpeg"):
        return getFilePreview(path=path, type=type)
