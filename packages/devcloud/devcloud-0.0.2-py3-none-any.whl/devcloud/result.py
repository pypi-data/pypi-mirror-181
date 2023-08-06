from array import array
from doctest import UnexpectedException
from email import header
import re
import requests
from .common import utils,json_data,cookies,data, validateToken
from .project import *
import json, os
import typer
import urllib.request
import urllib.parse
import numpy as np


def mount(accessKey: str, secretKey: str, region: str, bucketName: str):
    #{"accessKey":"AKIAR6EU2ADQXHRDVV3F","secretAccessKey":"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","regionName":"us-west-2","bucketName":"train2infer"}
    #https://result-service-devcloud-prod-puneethr12087576-intel.apps.cfa.devcloud.intel.com/results/secure/cloud/mount
    #POST
    header = utils.getheader()
    payload = {"accessKey":accessKey,"secretAccessKey":secretKey,"regionName":region,"bucketName":bucketName}
    response = requests.post(getResultBaseURL()+"/results/secure/cloud/mount",  headers=header, json=payload, cookies=cookies)
    statusCode = response.status_code
    if statusCode==200:
        print("Successfully connected to S3")
    else:
        raise Exception("Unable to connect to S3")

def cloudImport(fromPath: list, bucket: str):
    #{"cloudPath":["/s3/train2infer/unet_kits19.mapping","/s3/train2infer/unet_kits19.bin"]}
    #https://result-service-devcloud-prod-puneethr12087576-intel.apps.cfa.devcloud.intel.com/results/secure/cloud/download
    #POST
    header = utils.getheader()
    payload = {"cloudPath":list(map(lambda path: "/s3/{bucket}/{path}".format(bucket=bucket, path=path), fromPath))}
    response = requests.post(getResultBaseURL()+"/results/secure/cloud/download",  headers=header, json=payload, cookies=cookies)
    statusCode = response.status_code
    if statusCode==200:
        print("Successfully import from S3")
    else:
        raise Exception("Unable to import from S3")

def getResultBaseURL() -> str:
    return "https://result-service-devcloud-{env}-{namespace}-intel.apps.cfa.devcloud.intel.com".format(env = "prod", namespace=utils.getUserNamespace())

def getFileOutput(path: str):
    pass

def getFilePreview(path: str, type:str = "jpeg"):
    header = utils.getheader()
    url = getResultBaseURL()+"/results/secure/text?fileType={type}&location={path}".format(type = type, path=urllib.parse.quote(path))
    if(type == "jpeg"):
        url = getResultBaseURL()+"/results/image?fileType={type}&location={path}&download=false".format(type = type, path=urllib.parse.quote(path))
    req = urllib.request.Request(url, headers=header)
    res = urllib.request.urlopen(req)
    return res