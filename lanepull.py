import sys
sys.path.append(r"C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest")


from SPM.spmclient import SPMClient
from SPM.utils import read_config, filter_childshapes, create_excel_report, export_model
from SPM.logger import logger

import pandas as pd
import numpy as np

import traceback
import json
import time
import html

# =============================================================================
# Init
# =============================================================================
spm = SPMClient(r'C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest/SPM/spmconfig.yaml')
config = read_config(r'C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest/config.yaml')

start_time = time.time()
errors = {}
#modelID = "be618c3df62f49658e5a6c5a190d99cb"
#modelID = "e44e1a8063714e778912b0647e7e7d8a"
#modelID = "0739d7e1a3cb4029a58635cc63527507"
#modelID = "233ed51104c644bdb30386efc1764fba"
#modelID = "4bcc575382384620abeafcb71ebe5dfb"
sid = "sid-E4BC3858-C004-4A0D-8FF8-7F98B2E560E5"
directory_id = '29091c0b38ea43be9a3927a0adf5f1cd'
directory_id = 'c35b7e56eabe47f48384ed3f9e23140e'
#directory_id = 'fcc88674e6ca4095afb69497a9555b25'
#directory_id = '78f2128fc1c14a08a538813820180380'
#directory_id = '573eb91eb1484f1494658ec5f3c3583b'
#directory_id = 'f4f058d866b84c59a36edb8ea1443705'
#directory_id = '573eb91eb1484f1494658ec5f3c3583b' #S2P
#directory_id = 'b4b7df24d34847bf935a3c960bb04e72' #o2c
#directory_id = 'c2c0f38f0eb14650b12c35580fb681d1'

#model_json = spm.get_model_json(modelID)
elementDict = {}
taskDict = {}
connectorDataDictionary = []
df = pd.DataFrame({"e2eName":[],"L3":[],"Swimlane":[],"Addntl Participant":'',"Resource ID":'',"IT":'',"Fiori":'',"L3 UID":'',"IncorrectMappings":[]})

#df.loc[len(df)] = ["Hello","Analyst","Manager"]
#print(df)
#directory_content = spm.get_directory_content(directory_id)

#lanedata = filter_childshapes(model_json, filter_list=['Lane'])

def pullConnectorData(model_json):
    
    connectorDataDictionary = []
    
    tasks = filter_childshapes(model_json,filter_list=['Task','CollapsedSubprocess'])
    participants = filter_childshapes(model_json,filter_list='processparticipant')
    
    #--------Connector Data------------#
    connectors = filter_childshapes(model_json, filter_list="Association_Undirected")
    for connector in connectors:
        
        connectorOIDElementFound = False
        
        if connector.get('outgoing',{}):
            #print(f"Scanning connector: {connector['resourceId']}")
            
            for task in tasks:
                if task['resourceId'] == connector.get('outgoing',{})[0]['resourceId']:
                    connectorDataDictionary.append({"Connector ID": connector['resourceId'],"OID-Element":connector.get('outgoing',{})[0]['resourceId'],"Element Type":'Task'})
                    connectorOIDElementFound = True
                    
                    break
                
            if connectorOIDElementFound == False: #for future use
                for participant in participants:
                    if participant['resourceId'] == connector.get('outgoing',{})[0]['resourceId']:
                        connectorDataDictionary.append({"Connector ID": connector['resourceId'],"OID-Element":connector.get('outgoing',{})[0]['resourceId'],"Element Type":'Partiicipant'})
                        connectorOIDElementFound = True
                        break
                    
    #print(f"connector dict: {connectorDataDictionary}")
                    
     #----------------------------------------#

#If additional participants are available in the flow
def createTargetElementDict(model_json,element, elementJSONName):
    elementDict = {}
    filteredElementJSON = filter_childshapes(model_json, filter_list=elementJSONName)   
    tasks = filter_childshapes(model_json, filter_list=['Task','CollapsedSubprocess'])

    if len(filteredElementJSON)>0:
        incorrectMappingAddtnlParticipants = 0
        addtnlParticipantsAvailable = True
        connectors = filter_childshapes(model_json, filter_list="Association_Undirected")
        for elementDetail in filteredElementJSON:
            oidList = []
            
            rid = elementDetail.get('resourceId','')
            oids = elementDetail.get('outgoing',{})
            
            
            #check if the outgoing id is present (to ensure line is made from icon to L3)
            if oids:
                for oid in oids:
                    #oidList.append(oid)
                    connectorDict = {}
                    #get connector data
                    #print(oid['resourceId'])
                    
                    for connector in connectors:
                        #print(f"Connector OID:{connector.get('outgoing',{})[0]}")
                        #print(f"RID:{connector.get('resourceId','')}")
                        if connector.get('resourceId','') == oid['resourceId']:
                            if connector.get('outgoing',{}):
                                connectorDict = {"Connector ID": oid['resourceId'],"OID-Task":connector.get('outgoing',{})[0]['resourceId']}
                            
                    oidList.append(connectorDict)   
                
                elementDict[rid] = {
                    "Element Name": elementDetail.get('properties',{}).get('name',''),
                    "Outgoing ID": oidList
                        }
                
                
                
                #for multiple outgoing lines from a single addntl participant
                    
            else:
                connectorDict = {}
                
                for item in connectorDataDictionary:
                    if item['OID-Element'] == rid:
                        connectorDict = {"Connector ID": item['Connector ID'],"OID-Task":item['OID-Element']}
                        break
                oidList.append(connectorDict)
                elementDict[rid] = {
                    "Element Name": elementDetail.get('properties',{}).get('name',''),
                    "Outgoing ID": oidList
                        }
                       
                incorrectMappingAddtnlParticipants+=1    
        #print(json.dumps(elementDict,indent=2)) 
        print(f"Dict: {elementDict}")
    return elementDict




#Lane to task pull
def pullLaneData(model_json,e2eName,elementDict):
    
    
    lanedata = filter_childshapes(model_json, filter_list=['Lane'])
    
    for lane in lanedata:
        
        addtnlParticipantsAvailable = False #Check whether addtnl role is available (need to get it through the resource ID)
        connectorDict = ''
        
        print(f"Swimlane:{lane.get('properties',{}).get('name','')}")
        tasks = filter_childshapes(lane,filter_list=['Task','CollapsedSubprocess'])
        
        #print("\nL3s:")
        for task in tasks:
            #print(task.get('properties',{}).get('name',''))
            
            elementName = []
            
            #printing Addntl participants
            
            print(f"Element dict: {elementDict}")
            if elementDict is None:
                continue
                
            
            for elementDetail in elementDict:
                
                
                outgoingIDDict = elementDict[elementDetail]['Outgoing ID']
                
                for oidEntry in outgoingIDDict:
                    if oidEntry:
                        print(f"OID:{oidEntry['OID-Task']}, L3 RID: {task.get('resourceId','')}")
                        #check whether that connector oid matches with the L3 rid
                        if (oidEntry['OID-Task'] == task.get('resourceId','')):
                            elementName.append(elementDict[elementDetail]['Element Name'])
                            print(f"L3: {task.get('properties',{}).get('name','')},{elementName}")
            #for taskDetails in taskDict:
                
            
            #print(f"Associated Additional participant is:{addtnlPartyName}")
            #print(f"Df length:{len(df)}")
            '''
            #----------------Fetching Glossary values like Fiori, IT system etc--------------------#
            glossaryLink=task.get('glossaryLinks',{}).get('name','')
            glossaryDetails = spm.get_endpoint(glossaryLink[0][1:]+'/info') 
           
            print(glossaryDetails)
            #IT system pull
            if glossaryDetails:
                if(len(glossaryDetails.get('metaDataValues', {}).get('meta-itsystem', {}))>0):
                   itSystemObject = glossaryDetails.get('metaDataValues', {}).get('meta-itsystem', {})
                   itsystemArray = []
                   itsystemString = ''
                   for x in range(len(itSystemObject)):
                       itsystemArray.append(glossaryDetails.get('metaDataValues', {}).get('meta-itsystem', {})[x].get('title',''))
                   itsystemString = ','.join(itsystemArray)
                else:
                    itsystemString = ''
                    
                if(len(glossaryDetails.get('metaDataValues', {}).get('meta-fioriapptransaction', {}))>0):
                   fioriObject = glossaryDetails.get('metaDataValues', {}).get('meta-fioriapptransaction', {})
                   fioriArray = []
                   fioriString = ''
                   for x in range(len(fioriObject)):
                       fioriArray.append(glossaryDetails.get('metaDataValues', {}).get('meta-fioriapptransaction', {})[x].get('title',''))
                   fioriString = ','.join(fioriArray)
                else:
                    fioriString = ''  
            '''
            itsystemString = ''
            fioriString = ''
            df.loc[len(df)] = [e2eName,task.get('properties',{}).get('name',''),lane.get('properties',{}).get('name',''),elementName,task.get('resourceId',''),itsystemString,fioriString,task.get('properties',{}).get('meta-l3uid',''),'']
            
        #print("------------------\n")

#createTargetElementDict()
#pullLaneData()

def traverse_model_data(directory_id, level_id, hierarchy_id):
    model_count = 0
    
    try:
        
        level_id = level_id + 1
        tmp_id = ''
        print(f"Getting directory dtails of: {directory_id}")
        directory_content = spm.get_directory_content(directory_id)
        with open("directoryData.txt", "w") as file:
            file.write(json.dumps(directory_content,indent=2))
        #logger.debug(directory_content)
        
        for entry in directory_content:
            
            if(entry['rel'] == 'dir') or (entry['rel'] == 'mod'):
                
                  
                #DIRECTORY DATA
                if entry['rel'] == 'dir':
                    directoryName = entry['rep']['name']
                    
                    if directoryName == 'Master Data Management' or directoryName == 'Plan to Perform (P2P)': # or directoryName == 'L4 Process Flows'
                       logger.debug(directoryName)
                       continue
                   
                    if directoryName == 'L4 Process Flows':
                        l4ProcessFlowRunning = True
                        
                    directory_id = entry['href']
                    print(f"Traversing model data: {entry['rep']['name']}")
                    
                    traverse_model_data(directory_id, level_id, tmp_id)
                     
                #DIAGRAM DATA
                if entry['rel'] == 'mod':
                    model_count = model_count + 1
                    
                    e2eName = html.unescape(entry['rep']['name'])
                    e2eLink= html.unescape(entry['href'])
                    
                    if e2eName.startswith('PS-'):
                        print("HYC variants - skip")
                        continue
                    
                    model_json = spm.get_model_json(entry['href'])
                    print(e2eName)
                    #print(model_json)
                    
                    addtnlParticipantsAvailable = False
                    element = 'Addntl'
                    elementJSONName = 'processparticipant'
                    
                    #elementJSONName = 'DataObject'
                    
                    #elementJSONName = 'TextAnnotation'
                     
                    pullConnectorData(model_json)
                    elementDict = createTargetElementDict(model_json,element, elementJSONName)
                    pullLaneData(model_json,e2eName,elementDict)

    except Exception as err:
        pass
        logger.error(tmp_id + ' ' + type(err).__name__ + traceback.format_exc())
        errors[tmp_id] = traceback.format_exc()
          



traverse_model_data(directory_id, level_id=0, hierarchy_id=0)
df.to_excel("L3TaskAddtnlData - RnM.xlsx") 
end_time = time.time()
logger.info('Total Runtime: ' + str(round((time.time() - start_time) / 60 , 2)) + ' minutes')
logger.debug(df)
#print(incorrectMappingAddtnlParticipants)
#print(json.dumps(data[1],indent=2))
#print(update_json(model_json))

'''
#---------------PRINT-------------------
print(json.dumps(model_json,indent=2))

'''
'''
with open("test12thSep.txt", "w") as file:
    file.write(json.dumps(model_json,indent=2))            
'''