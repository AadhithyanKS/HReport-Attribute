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
#directory_id = '29091c0b38ea43be9a3927a0adf5f1cd'
#directory_id = '78f2128fc1c14a08a538813820180380'
#directory_id = '573eb91eb1484f1494658ec5f3c3583b'
#directory_id = 'f4f058d866b84c59a36edb8ea1443705'
directory_id = '573eb91eb1484f1494658ec5f3c3583b' #S2P

#model_json = spm.get_model_json(modelID)
addtnlParticipantDict = {}
taskDict = {}
connectorDataDictionary = []
df = pd.DataFrame({"e2eName":[],"L3":[],"Swimlane":[],"Addntl Participant":'',"Resource ID":'',"IncorrectMappings":[]})

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
            print(f"Scanning connector: {connector['resourceId']}")
            
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
                    
    print(f"connector dict: {connectorDataDictionary}")
                    
     #----------------------------------------#

#If additional participants are available in the flow
def createAddtnlParticipantDict(model_json):
    addtnlParticipants = filter_childshapes(model_json, filter_list="processparticipant")   
    tasks = filter_childshapes(model_json, filter_list=['Task','CollapsedSubprocess'])

    if len(addtnlParticipants)>0:
        incorrectMappingAddtnlParticipants = 0
        addtnlParticipantsAvailable = True
        connectors = filter_childshapes(model_json, filter_list="Association_Undirected")
        for addtnl in addtnlParticipants:
            oidList = []
            
            rid = addtnl.get('resourceId','')
            oids = addtnl.get('outgoing',{})
            
            
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
                
                addtnlParticipantDict[rid] = {
                    "Additional Participant Name": addtnl.get('properties',{}).get('name',''),
                    "Outgoing ID": oidList
                        }
                
                #for multiple outgoing lines from a single addntl participant
                    
            else:
                
                for item in connectorDataDictionary:
                    if item['OID-Element'] == rid:
                        connectorDict = {"Connector ID": item['Connector ID'],"OID-Task":item['OID-Element']}
                        break
                oidList.append(connectorDict)
                addtnlParticipantDict[rid] = {
                    "Additional Participant Name": addtnl.get('properties',{}).get('name',''),
                    "Outgoing ID": oidList
                        }
                       
                incorrectMappingAddtnlParticipants+=1    
        print(json.dumps(addtnlParticipantDict,indent=2))      
        return incorrectMappingAddtnlParticipants




#Lane to task pull
def pullLaneData(model_json,e2eName,incorrectMappings):
    
    
    lanedata = filter_childshapes(model_json, filter_list=['Lane'])
    

    
    for lane in lanedata:
        
        addtnlParticipantsAvailable = False #Check whether addtnl role is available (need to get it through the resource ID)
        connectorDict = ''
        
        print(f"Swimlane:{lane.get('properties',{}).get('name','')}")
        tasks = filter_childshapes(lane,filter_list=['Task','CollapsedSubprocess'])
        
        #print("\nL3s:")
        for task in tasks:
            #print(task.get('properties',{}).get('name',''))
            
            addtnlPartyName = []
            
            #printing Addntl participants
            
            for addtnlParty in addtnlParticipantDict:
                outgoingIDDict = addtnlParticipantDict[addtnlParty]['Outgoing ID']
                for oidEntry in outgoingIDDict:
                    if oidEntry:
                        #check whether that connector oid matches with the L3 rid
                        if (oidEntry['OID-Task'] == task.get('resourceId','')):
                            addtnlPartyName.append(addtnlParticipantDict[addtnlParty]['Additional Participant Name'])
            
            #for taskDetails in taskDict:
                
            
            #print(f"Associated Additional participant is:{addtnlPartyName}")
            #print(f"Df length:{len(df)}")
            l4ITSystem = task.get('properties',{}).get('meta-itsystem','')
            l4Fiori = task.get('properties',{}).get('meta-fioriapptransaction','')
            df.loc[len(df)] = [e2eName,task.get('properties',{}).get('name',''),lane.get('properties',{}).get('name',''),addtnlPartyName,task.get('resourceId',''),incorrectMappings]
            
        #print("------------------\n")

#createAddtnlParticipantDict()
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
        iterator = 0
        for entry in directory_content:
            
            if(entry['rel'] == 'dir') or (entry['rel'] == 'mod'):
                if hierarchy_id == 0:
                    iterator = iterator + 1
                    tmp_id = ''
                else:
                    iterator = iterator + 1
                    tmp_id = ''
                  
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
                     
                    pullConnectorData(model_json)
                    incorrectMappings = createAddtnlParticipantDict(model_json)
                    pullLaneData(model_json,e2eName,incorrectMappings)

    except Exception as err:
        pass
        logger.error(tmp_id + ' ' + type(err).__name__ + traceback.format_exc())
        errors[tmp_id] = traceback.format_exc()
          



traverse_model_data(directory_id, level_id=0, hierarchy_id=0)
df.to_excel("L3TaskAddtnlData - S2P.xlsx") 
end_time = time.time()
logger.debug(f"Time taken: {end_time-start_time}")
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