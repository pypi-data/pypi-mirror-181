import sys
import jaydebeapi
import pandas as pd
from getpass import getpass
import re
import itertools
import warnings
from base64 import b64encode
from base64 import b64decode
import hashlib
import os
import os.path
import yaml
import requests
import json
from sqlalchemy import create_engine
from datetime import datetime
from datetime import *
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from Cryptodome.Hash import SHA256
from getpass import getpass
import logging
from logging.handlers import RotatingFileHandler
from ndp_deployment.fetch_metastore import object_deployment

# Instantiating a Logger to log info+ data with a 1.5 GB max file size.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
maxByteSize = 1.5*1024*1024
file_handler = RotatingFileHandler('execute_versioncontrol.log', maxBytes=maxByteSize,backupCount=10)
file_format = logging.Formatter('%(asctime)s: %(message)s', datefmt='%d-%m-%Y || %I:%M:%S %p')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

warnings.filterwarnings("ignore")
dt = datetime.now()
ts = datetime.timestamp(dt)

def decrypt(folder_path,key_decrypt):
    file_path=str(folder_path).strip()+"cred.bin"
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        salt = f.read(32)
        data = f.read()
    key = str(key_decrypt)
    key = PBKDF2(key, salt, dkLen=32, count=1000000,hmac_hash_module=SHA256)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    data = unpad(cipher.decrypt(data), AES.block_size)
    data = bytes.decode(data)
    dec_data = data.split('|||')
    return(dec_data)

def get_encrypted_pass (folder_path,key_decrypt,api_url):
    dec_data = decrypt(folder_path,key_decrypt)
    obj = {
        'target':dec_data[1]
    }
    apiurl='https://'+str(api_url).lower().strip()+':8443/enc'
    response = requests.post(url=apiurl,params=obj)
    return response.text

def get_bearer_token (orgId,folder_path,key_decrypt,api_url):
    org_folder_path=str(folder_path).strip()+str(orgId)+"/"
    dec_data = decrypt(org_folder_path,key_decrypt)
    encrypted_password=get_encrypted_pass(org_folder_path,key_decrypt,api_url)
    username = dec_data[0]
    obj = {
        "password":encrypted_password,
        "username":username,
        "orgId": str(orgId).strip()
    }
    apiurl='https://'+str(api_url).lower().strip()+':8443/login'
    response = requests.post(url=apiurl,data=obj)
    response = json.loads(response.text)
    return response['bearer_token']

def runQuery(query:str,r,api_url,bearer_token):
    try:
        obj={
            "sql":query,
        }
        auth={
            "Authorization": "Bearer " + bearer_token
        }
        apiurl='https://'+str(api_url).lower().strip()+':8443/query'
        response = requests.post(url=apiurl, data=obj, headers=auth)
        response=json.loads(response.text)
        if response.get('data'):
            querytoken=response['data']['query_token']
            close_obj={
                "query_token":querytoken,
                "close_query": "true"
            }
            apiurl='https://'+str(api_url).lower().strip()+':8443/closequery'
            requests.post(url=apiurl, data=close_obj, headers=auth)

        if(r):
            data = response['data']['data']
            return data
    except Exception as e:
        logger.info("Run Query Function Error Logs")
        logger.info(e)

def run_fetch_metastore(orgId_alpha,orgId,folder_path,host,key_decrypt,jar_file_name,option_for_backup,container_name,object_name):
    object_deployment(orgId_alpha,orgId,folder_path,host,key_decrypt,jar_file_name,option_for_backup,container_name,object_name)

def get_individual_pipelines(orgId_alpha,orgId,host,key_decrypt,folder_path,api_url,bearer_token,jar_file_name):
    logger.info('Backup of Individual Pipelines')
    sql_ind_pipeline="select r.name as rname,c.name as cname from metastore.pipeline_relation r inner join metastore.pipeline_container c on c.id=r.fk_pipeline_container_id where c.fk_organisation_id="+str(orgId).strip()
    res = runQuery(sql_ind_pipeline,True,api_url,bearer_token)
    if isinstance(res[0],dict):
        for dic in res:
            con_name=list(dic.values())[0]
            pipe_name=list(dic.values())[1]
            if (len(str(pipe_name))>1):
                run_fetch_metastore(str(orgId_alpha).strip(),str(orgId).strip(),str(folder_path).strip(),str(host),str(key_decrypt),str(jar_file_name).strip(),"2",str(con_name),str(pipe_name))

def get_pipeline_containers(orgId_alpha,orgId,host,key_decrypt,folder_path,api_url,bearer_token,jar_file_name):
    logger.info('Backup of All Pipelines')
    sql_query_pipeline="select name from metastore.pipeline_container where fk_organisation_id="+str(orgId).strip()
    res = runQuery(sql_query_pipeline,True,api_url,bearer_token)
    if isinstance(res[0],dict):
        for i in res:
            name = str(i['name'])
            run_fetch_metastore(str(orgId_alpha).strip(),str(orgId).strip(),str(folder_path).strip(),str(host),str(key_decrypt),str(jar_file_name).strip(),"1",str(name),"")
        
def get_data_views(orgId_alpha,orgId,host,key_decrypt,folder_path,api_url,bearer_token,jar_file_name):
    logger.info('Backup of Permanent Views')
    sql_query_view="select name from metastore.schema_store_view where fk_organisation_id="+str(orgId).strip()
    res = runQuery(sql_query_view,True,api_url,bearer_token)
    if isinstance(res[0],dict):
        for i in res:
            name = str(i['name'])
            run_fetch_metastore(str(orgId_alpha).strip(),str(orgId).strip(),str(folder_path).strip(),str(host),str(key_decrypt),str(jar_file_name).strip(),"7",str(name),"")
        
def get_data_marts(orgId_alpha,orgId,host,key_decrypt,folder_path,api_url,bearer_token,jar_file_name):
    logger.info('Backup of Data Marts')
    sql_query_mart="select name from metastore.data_mart where fk_organisation_id="+str(orgId).strip()
    res = runQuery(sql_query_mart,True,api_url,bearer_token)
    if isinstance(res[0],dict):
        for i in res:
            name = str(i['name'])
            run_fetch_metastore(str(orgId_alpha).strip(),str(orgId).strip(),str(folder_path).strip(),str(host),str(key_decrypt),str(jar_file_name).strip(),"5",str(name),"")

def generate_file_name(arg1,arg2,object_type,type_of_restore,folder_path,api_url,bearer_token):
    logger.info('Inside Generate File Function...')
    if (type_of_restore=='full'):
        filename_restore=str(folder_path).strip()+'versioncontrol/backup/'+str(arg1)+''+str(arg2)+''+str(object_type)+'.sql'
        if(os.path.exists(filename_restore)):
            logger.info('File exists for restore, now executing the commands for restore\n')
            execute_sql_file(filename_restore,api_url,bearer_token)
        else:
            logger.info('Restore: File does not exist')
    elif (type_of_restore=='individual'):
        filename_restore=str(folder_path).strip()+'versioncontrol/restore/'+str(arg1)+''+str(arg2)+''+str(object_type)+'.sql'
        logger.info(filename_restore)
        if(os.path.exists(filename_restore)):
            logger.info('File exists for restore, now executing the commands for restore\n')
            execute_sql_file(filename_restore,api_url,bearer_token)
        else:
            logger.info('Restore: File does not exist')

def restore_views(orgId,arg1,folder_path,api_url,bearer_token):
    if len(str(arg1))>=1:
        sql_query_view="select name from metastore.schema_store_view where lower(name)='"+str(arg1)+"' and fk_organisation_id="+str(orgId).strip()
        res = runQuery(sql_query_view,True,api_url,bearer_token)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                sql_query_drop_view="Drop Permanent View "+name
                runQuery(sql_query_drop_view,False,api_url,bearer_token)
            generate_file_name(arg1,'','-permanent_view','individual',folder_path,api_url,bearer_token)
        else:
            generate_file_name(arg1,'','-permanent_view','individual',folder_path,api_url,bearer_token)
    else:
        sql_query_view="select name from metastore.schema_store_view where fk_organisation_id="+str(orgId).strip()
        res = runQuery(sql_query_view,True,api_url,bearer_token)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                sql_query_drop_view="Drop Permanent View "+name
                runQuery(sql_query_drop_view,False,api_url,bearer_token)
            generate_file_name('','','views','full',folder_path,api_url,bearer_token)
        else:
            generate_file_name('','','views','full',folder_path,api_url,bearer_token)

def restore_datamarts(orgId,arg1,folder_path,api_url,bearer_token):
    if len(str(arg1))>=1:
        sql_query_mart="select name from metastore.data_mart where lower(name)='"+str(arg1)+"' and fk_organisation_id="+str(orgId).strip()
        res = runQuery(sql_query_mart,True,api_url,bearer_token)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                sql_query_drop_datamart="Drop Datamart "+name
                runQuery(sql_query_drop_datamart,False,api_url,bearer_token)
            generate_file_name(arg1,'','-datamart','individual',folder_path,api_url,bearer_token)
        else:
            generate_file_name(arg1,'','-datamart','individual',folder_path,api_url,bearer_token)
    else:
        sql_query_mart="select name from metastore.data_mart where fk_organisation_id="+str(orgId).strip()
        res = runQuery(sql_query_mart,True,api_url,bearer_token)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                sql_query_drop_datamart="Drop Datamart "+name
                runQuery(sql_query_drop_datamart,False,api_url,bearer_token)
            generate_file_name('','','data_marts','full',folder_path,api_url,bearer_token)
        else:
            generate_file_name('','','data_marts','full',folder_path,api_url,bearer_token)

def restore_pipelines(orgId,arg1,arg2,folder_path,api_url,bearer_token):
    if len(str(arg1))>0 and len(str(arg2))>0:
        sql_query_pipeline="select r.name as rname,c.name as cname from metastore.pipeline_relation r inner join metastore.pipeline_container c on c.id=r.fk_pipeline_container_id where r.name='%s' and c.name='%s' and c.fk_organisation_id=%s"%(arg2,arg1,str(orgId).strip())
        logger.info(sql_query_pipeline)
        res = runQuery(sql_query_pipeline,True,api_url,bearer_token)
        if isinstance(res[0],dict):
            name = str(arg1.lower())+"."+str(arg2.lower())
            sql_query_drop_pipeline="Drop Pipeline Relation "+name
            runQuery(sql_query_drop_pipeline,False,api_url,bearer_token)
            generate_file_name(arg1,'-'+str(arg2),'-pipeline','individual',folder_path,api_url,bearer_token)
        else:
            generate_file_name(arg1,'-'+str(arg2),'-pipeline','individual',folder_path,api_url,bearer_token)
    elif len(str(arg1))>0 and len(str(arg2))==0:
        sql_query_pipeline="select name from metastore.pipeline_container where lower(name)='"+str(arg1)+"' and fk_organisation_id="+str(orgId).strip()
        res = runQuery(sql_query_pipeline,True,api_url,bearer_token)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                sql_query_drop_pipeline="Drop Pipeline Container "+name
                runQuery(sql_query_drop_pipeline,False,api_url,bearer_token)
            generate_file_name(arg1,'','-pipeline','individual',folder_path,api_url,bearer_token)
        else:
            generate_file_name(arg1,'','-pipeline','individual',folder_path,api_url,bearer_token)
    else:
        sql_query_pipeline="select name from metastore.pipeline_container where fk_organisation_id="+str(orgId).strip()
        res = runQuery(sql_query_pipeline,True,api_url,bearer_token)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                sql_query_drop_pipeline="Drop Pipeline Container "+name
                runQuery(sql_query_drop_pipeline,False,api_url,bearer_token)
            generate_file_name('','','pipelines','full',folder_path,api_url,bearer_token)
        else:
            generate_file_name('','','pipelines','full',folder_path,api_url,bearer_token)

def execute_sql_file(filename,api_url,bearer_token):
    logger.info(filename)
    logger.info("\n")
    fd = open(filename, 'r')
    sqlFile = fd.read()
    sqlCommands = sqlFile.split(';')[:-1]
    for query in sqlCommands:
        logger.info(query)
        runQuery(query,False,api_url,bearer_token)
    fd.close()
    restore_msg="\nRestore finished for the file "+str(filename)
    logger.info(restore_msg)


def object_versioncontrol(orgId_alpha,host,folder_path,key_decrypt,api_url,jar_file_name,vcarg1,vcarg2,vcarg3,vcarg4):
    get_org_id="select id from metastore.organisation where organisation_id='"+str(orgId_alpha).strip()+"'"
    api_url=str(api_url).lower().strip()
    bearer_token = get_bearer_token(orgId_alpha,folder_path,key_decrypt,api_url)
    org_list = runQuery(get_org_id,True,api_url,bearer_token)
    if isinstance(org_list[0],dict):
        for i in org_list:
            orgId = str(i['id'])
    if str(vcarg1).lower().strip()=='backup':
        get_individual_pipelines(orgId_alpha,orgId,host,key_decrypt,folder_path,api_url,bearer_token,jar_file_name)
        get_pipeline_containers(orgId_alpha,orgId,host,key_decrypt,folder_path,api_url,bearer_token,jar_file_name)
        get_data_views(orgId_alpha,orgId,host,key_decrypt,folder_path,api_url,bearer_token,jar_file_name)
        get_data_marts(orgId_alpha,orgId,host,key_decrypt,folder_path,api_url,bearer_token,jar_file_name)
    elif str(vcarg1).lower().strip()=='restore':
        if (len(str(vcarg2).lower().strip())>0 and len(str(vcarg3).lower().strip())==0 and len(str(vcarg4).lower().strip())==0):
            try:
                if str(vcarg2).lower().strip()=='pipelines':
                    logger.info("Restoring All Pipelines")
                    restore_pipelines(orgId,'','',folder_path,api_url,bearer_token)
                elif str(vcarg2).lower().strip()=='data_marts':
                    logger.info("Restoring All DataMarts")
                    restore_datamarts(orgId,'',folder_path,api_url,bearer_token)
                elif str(vcarg2).lower().strip()=='views':
                    logger.info("Restoring All Views")
                    restore_views(orgId,'',folder_path,api_url,bearer_token)
            except:
                exit()
        elif (len(str(vcarg2).lower().strip())>0 and len(str(vcarg3).lower().strip())>0 and len(str(vcarg4).lower().strip())==0):
            try:
                if str(vcarg2).lower().strip()=='pipelines':
                    logger.info("Restoring Pipeline Container")
                    restore_pipelines(orgId,str(vcarg3).lower().strip(),'',folder_path,api_url,bearer_token)
                elif str(vcarg2).lower().strip()=='data_marts':
                    logger.info("Restoring DataMart")
                    restore_datamarts(orgId,str(vcarg3).lower().strip(),folder_path,api_url,bearer_token)
                elif str(vcarg2).lower().strip()=='views':
                    logger.info("Restoring View")
                    restore_views(orgId,str(vcarg3).lower().strip(),folder_path,api_url,bearer_token)
            except:
                exit()
        elif (len(str(vcarg2).lower().strip())>0 and len(str(vcarg3).lower().strip())>0 and len(str(vcarg4).lower().strip())>0):
            try:
                if str(vcarg2).lower().strip()=='pipelines':
                    logger.info("Restoring Individual Pipelines")
                    restore_pipelines(orgId,str(vcarg3).lower().strip(),str(vcarg4).lower().strip(),folder_path,api_url,bearer_token)
            except:
                exit()
        else:
            logger.info("Restoring All")
            restore_pipelines(orgId,'','',folder_path,api_url,bearer_token)
            restore_datamarts(orgId,'',folder_path,api_url,bearer_token)
            restore_views(orgId,'',folder_path,api_url,bearer_token)
