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


#root_directory_id = '29091c0b38ea43be9a3927a0adf5f1cd' #ETE full
#root_directory_id = "2c011a10241844fcb54d591b278d5dc7" #s2p,o2c,sc,mpo,S&M,r2r,hcm,trading,nhyc,hyc
root_directory_id = "97eb35609b6545d48e5b972ca68002fc" #mpo
#Import Excel File

df = pd.read_excel('uidtest.xlsx') #replace with og file
url_splitted = df['Signavio URL UID-Direct link to Signavio Flow'].str.split('/',expand=True)

df['model_id'] = url_splitted[6]
df['resource_id'] = url_splitted[8]

results = pd.DataFrame({'ETE':[],'L3':[],'UID':[],'Status':[]})

#Function to target an L3 using the SID and update the json
def update_json(obj, target_res_id, target_variable, new_value):
    if isinstance(obj, dict):
        if obj.get("resourceId") == target_res_id and target_variable in obj.get("properties", {}):
            
            obj["properties"]["meta-l3uid"] = new_value
            return True
        for key, value in obj.items():
            if update_json(value, target_res_id, target_variable, new_value):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if update_json(item, target_res_id, target_variable, new_value):
                return True
    return False

processFlowGroup = df.groupby('ETE Group (Signavio Process Flow)(Src: Same as L3)')



for flow, group in processFlowGroup: 
    
    verified = True
    
    modelID = group.iloc[0]['model_id']
    model_json = spm.get_model_json(modelID)
    
    for index, row in group.iterrows():
        
        modelID = row['model_id']
        l3 = row['Signavio L3 Instances(Src: Hierarchy Report L3-L0)']
        sid = row['resource_id']
        L3uid = row["L3 UID"]
        
        

        if update_json(model_json, sid, 'meta-l3uid', L3uid):
            
            results.loc[len(results)] = [flow,l3,L3uid,'Success']
        else:
            print(f"\nUpdate failed for L3: {l3}, sid: {sid}")
            results.loc[len(results)] = [flow,l3,L3uid,'Failed']
            verified = False

    if verified:
        if spm.update_model(modelID, model_json,comment='L3UID updated'):
            print(f"L3UID updated successfully for the model: {flow}\n------------------------------------")   
            spm.publish_model(modelID)
    else:
        logger.debug(f"Flow updation failed: {flow}")
start_time = time.time()
errors = {}



#Update the model - POST

results.to_excel('UIDResult.xlsx', index=False)


logger.info('------ RESULTS -----')
logger.info('Total Runtime: ' + str(round((time.time() - start_time) / 60 , 2)) + ' minutes')                  
