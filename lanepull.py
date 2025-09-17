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

#modelID = "be618c3df62f49658e5a6c5a190d99cb"
modelID = "e44e1a8063714e778912b0647e7e7d8a"
#modelID = "0739d7e1a3cb4029a58635cc63527507"
#modelID = "233ed51104c644bdb30386efc1764fba"
#modelID = "4bcc575382384620abeafcb71ebe5dfb"
sid = "sid-E4BC3858-C004-4A0D-8FF8-7F98B2E560E5"
directory_id = 'b4b7df24d34847bf935a3c960bb04e72'

model_json = spm.get_model_json(modelID)
addtnlParticipantDict = {}
df = pd.DataFrame({"L3":[],"Swimlane":[],"Addntl Participant":[]})

#df.loc[len(df)] = ["Hello","Analyst","Manager"]


print(df)
#directory_content = spm.get_directory_content(directory_id)

lanedata = filter_childshapes(model_json, filter_list=['Lane'])
addtnlParticipants = filter_childshapes(model_json, filter_list="processparticipant")



#If additional participants are available in the flow

if len(addtnlParticipants)>0:
    incorrectMappingAddtnlParticipants = 0
    addtnlParticipantsAvailable = True
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
                connectors = filter_childshapes(model_json, filter_list="Association_Undirected")
                for connector in connectors:
                    #print(f"Connector OID:{connector.get('outgoing',{})[0]}")
                    #print(connector.get('resourceId',''))
                    if connector.get('resourceId','') == oid['resourceId']:
                        connectorDict = {"Connector ID": oid['resourceId'],"OID-Task":connector.get('outgoing',{})[0]['resourceId']}
                        
                oidList.append(connectorDict)   
            
            addtnlParticipantDict[rid] = {
                "Additional Participant Name": addtnl.get('properties',{}).get('name',''),
                "Outgoing ID": oidList
                    }
            
            #for multiple outgoing lines from a single addntl participant
            
                
        else:
            incorrectMappingAddtnlParticipants+=1
            
        
print(json.dumps(addtnlParticipantDict,indent=2))


#Lane to task
for lane in lanedata:
    
    addtnlParticipantsAvailable = False #Check whether addtnl role is available (need to get it through the resource ID)
    
    print(f"Swimlane:{lane.get('properties',{}).get('name','')}")
    tasks = filter_childshapes(lane,filter_list=['Task'])
    
    
    print("\nL3s:")
    for task in tasks:
        print(task.get('properties',{}).get('name',''))
        addtnlPartyName = []
        
        #printing Addntl participants
        
        for addtnlParty in addtnlParticipantDict:
            outgoingIDDict = addtnlParticipantDict[addtnlParty]['Outgoing ID']
            for oidEntry in outgoingIDDict:
                #check whether that connector oid matches with the L3 rid
                if oidEntry['OID-Task'] == task.get('resourceId',''):
                    addtnlPartyName.append(addtnlParticipantDict[addtnlParty]['Additional Participant Name'])
                
        print(f"Associated Additional participant is:{addtnlPartyName}")
        
        
                
            
        
        
        
    print("------------------\n")

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