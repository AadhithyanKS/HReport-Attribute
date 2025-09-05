from SPM.spmclient import SPMClient
from SPM.utils import read_config, filter_childshapes, create_excel_report
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
spm = SPMClient('SPM/spmconfig.yaml')
config = read_config('config.yaml')

#Import Excel File
riskData = pd.read_excel('risks.xlsx',sheet_name = 'Testing Tab',skiprows=7) #replace with og file

print(riskData)

grouped = riskData.groupby("L3 ID")


riskJSON = []
controlJSON = []

'''
for l3id, group in grouped:
    riskJSON[l3id] = group.to_dict(orient="records")
    

print(json.dumps(riskJSON, indent=2))
'''

#print(json.dumps(result, indent=2))


#print(riskData)

#Risk json block
new_riskstest_block = {
                  "totalCount": 1,
                  "items": [
                    {
                      "meta-extentofdamagewithoutcontro": "Low",
                      "riskname": "Duplicate payments",
                      "meta-riskprobabilitywithoutcontr": "Normal",
                      "controls": {
                        "totalCount": 1,
                        "items": [
                          {
                            "meta-responsible": "",
                            "attachments": "",
                            "itemHref": "/glossary/af4e0909dff744b88237b53768693563",
                            "meta-documentation": "Hello",
                            "meta-typeofcontrol": "",
                            "name": "Control 2 (test)",
                            "description": "",
                            "meta-controlfrequency": "",
                            "meta-controlaim": "",
                            "meta-status": "1"
                          }
                        ]
                      },
                      "attachments": "",
                      "itemHref": "/glossary/bb39e8f6da6346e1a90f33e402c15fed",
                      "meta-extentofdamageresidualrisk": "High",
                      "meta-cause": "Cause3",
                      "meta-consequence": "Consequence3",
                      "description": "Test Description",
                      "meta-riskprobabilityresidualrisk": "Low",
                      "id": "oryx_332405ED-9D14-4CA6-885C-2310EEACC52D"
                    },
                   
                  ]
                }

#Function to update the key after behavior


def insert_after_key_globally(obj, target_sid,target_key_to_find, new_key_to_insert, new_value_to_insert):
    
    global currentL3, updateCompleted
    if isinstance(obj, dict):
        modified_dict = {}
        target_key_found_in_this_level = False
        
        if new_key_to_insert in obj.get("properties",{}) and obj.get("resourceId") == target_sid:
            print("Risk attrib already available, replacing it:")
            obj["properties"][new_key_to_insert] = new_value_to_insert
            return obj
            return

        # First pass: iterate to find target_key and build the new dict with insertion
        for key, value in obj.items():
            if obj.get("resourceId") == target_sid:
                #print("Instance of curr L3 found")
                currentL3 = True
            modified_dict[key] = value # Add current item
            if key == target_key_to_find and currentL3 and updateCompleted  == False:
                
                
                # Perform the insertion directly in this dictionary
                print("New Value inserted")
                modified_dict[new_key_to_insert] = new_value_to_insert
                target_key_found_in_this_level = True
                updateCompleted = True

            # Recursively process the value (which might be another dict or a list)
           
            if isinstance(value, (dict, list)):
                modified_dict[key] = insert_after_key_globally(value, target_sid,target_key_to_find, new_key_to_insert, new_value_to_insert)

   
       
        if new_key_to_insert in obj and not target_key_found_in_this_level:
     
            print("Passed")
            pass

        return modified_dict

    elif isinstance(obj, list):
        # Recursively process each item in the list
        return [insert_after_key_globally(item, target_sid, target_key_to_find, new_key_to_insert, new_value_to_insert) for item in obj]

    else:
        # Base case: not a dict or list, return as is
        return obj

#Variables
target_key_to_find = "behavior"
new_key_for_block = "meta-riskstest" # The key *for* your new block

start_time = time.time()
errors = {}

modelid = ''
#sid = 'sid-752D32E1-55F0-4273-836F-CC2D21E7898E'
sid = ''

riskList = []

for l3name, grp in grouped:
    currentL3 = False
    updateCompleted = False
    
    modelid = grp["Model ID"].iloc[0]
    sid= grp["L3 ID"].iloc[0]
    model_json = spm.get_model_json(modelid)
    
    riskCount = len(grp)
    
    riskGroup = grp.groupby("RiskName")
    for risk, riskGrp in riskGroup:
        print(riskGrp)
        firstRiskRow = riskGrp.iloc[0]
        controlCount = len(riskGrp)
        print(controlCount)
        #print(firstRiskRow)
        if firstRiskRow["Control Glossary ID"] == "":
            print("Control Count less than 1")
            controlJSON = ({
                "totalCount": 0,
                "items": [
                  ]
                })
            
        else:
            print("Controls present")
            controlJSON = ({
                "totalCount": controlCount,
                "items": [
                  {
                    "meta-responsible": row["Responsible"],
                    "attachments": "",
                    "itemHref": "/glossary/"+row["Control Glossary ID"],
                    "meta-documentation": row["Documentation"],
                    "meta-typeofcontrol": row["Type of control"],
                    "name": row["Controls"],
                    "description": row["Control Description"],
                    "meta-controlfrequency": row["Control Frequency"],
                    "meta-controlaim": row["Control Aim"],
                    "meta-status": row["Status"]
                  }for _, row in riskGrp.iterrows()]
                })
        
        print(controlJSON)
        print(f"Initial Risklist: {riskList}")
        riskList.append({
            "meta-extentofdamagewithoutcontro": firstRiskRow["Extent of damage (without controls)"],
            "riskname": "",
            "meta-riskprobabilitywithoutcontr": firstRiskRow["Risk Probability (without controls)"],
            "controls": controlJSON,
            "attachments": "",
            "itemHref": "/glossary/"+firstRiskRow["RiskName Glossary ID"],
            "meta-extentofdamageresidualrisk": firstRiskRow["Extent of damage (residual risk)"],
            "meta-cause": firstRiskRow["Cause"],
            "meta-consequence": firstRiskRow["Consequence"],
            "description": firstRiskRow["Risk Description"],
            "meta-riskprobabilityresidualrisk": firstRiskRow["Risk Probability (residual risk)"],
            "id": ""
            })
        
        print(f"risklist at 1: {riskList}")
        
    
        print("Appending results of group")
    riskJSON = ({
        "totalCount":riskCount,
        "items":riskList
            
        })
    
    print(json.dumps(riskJSON, indent=2))
    riskList = []

    modified_data = insert_after_key_globally(model_json,sid, target_key_to_find, new_key_for_block, riskJSON)

    if (spm.update_model(modelid, modified_data,comment='L3UID updated')):
      
       with open("jsonoutput.txt", "w") as file:
           file.write(json.dumps(modified_data,indent=2))
       print(f"Risks updated successfully for the model {modelid}: \n\n*********************************")

#Update the model - POST


logger.info('------ RESULTS -----')
logger.info('Total Runtime: ' + str(round((time.time() - start_time) / 60 , 2)) + ' minutes')
