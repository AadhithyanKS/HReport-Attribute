from SPM.spmclient import SPMClient
from SPM.utils import read_config, filter_childshapes, create_excel_report
from SPM.logger import logger

import traceback
import json
import time
import html

# =============================================================================
# Init
# =============================================================================
spm = SPMClient('SPM/spmconfig.yaml')
config = read_config('config.yaml')

#root_directory_id = 'ba71ddb7e5f14c5b895894701fd51337' # HYC test
#root_directory_id = 'e38a153129af4186a6e40337d8f4bda1' #Sandbox Test


#root_directory_id = '65fb63d5447b4cedbce4fbabddf995db' # SC
#root_directory_id = 'f81c4456c9d64291b50ce7f95694acf4' #PLM L4
#root_directory_id = '2e746e42f12c4a92bd7edb55ca31ab52' #S2P 4 flows
#root_directory_id = 'aa54faa6b46840768311ac8b877c8d83' 
#root_directory_id = '2c011a10241844fcb54d591b278d5dc7' #Pooja HYC test
#root_directory_id = 'ecbc52cf53be4dc4a5ec2855de594e29' #L4test2
#root_directory_id = '687b28ffc54c4ad1a2a40bd37e0be375' #TestEnv 
#root_directory_id = '29091c0b38ea43be9a3927a0adf5f1cd'
#root_directory_id = '977d1a3f0a674651aceadf96925bd803' # Modular folder
#root_directory_id = 'c7158422e9a64cee94a7b797a9953b5f' #testing
#root_directory_id = '97eb35609b6545d48e5b972ca68002fc' #manufacturing Operations 
#root_directory_id = '841916c8c87d4f1a8ab47723fa579b20' #mdm
#root_directory_id = 'b4b7df24d34847bf935a3c960bb04e72' #o2c
root_directory_id = 'da9b35bd49c44f23b3025f6260f05c97' #S2P L4s
#root_directory_id = '573eb91eb1484f1494658ec5f3c3583b' #sandbox
#root_directory_id = 'dbb2064d9f0547aa947f5b9447c5cec6' #p2p
#root_directory_id = '3a47cac6b21e4fd193b3af281bcae868' #r2r
#root_directory_id = 'f4f058d866b84c59a36edb8ea1443705' #SnM
#root_directory_id = 'c2c0f38f0eb14650b12c35580fb681d1' #S2P
#root_directory_id = '3fe14e53b2724f058542e073bd68a22f' #SC 
#root_directory_id = '2ba73b52e57a4993a1f40b4c82282596' #Trading2
#root_directory_id = 'd7d73caea37c4d18a0c986bd569f348e' # supp 
#root_directory_id = '29091c0b38ea43be9a3927a0adf5f1cd' #ETE full
#root_directory_id = '2c011a10241844fcb54d591b278d5dc7' # hydro carbon - 
#root_directory_id = '2fffdc51904c4749bb148e8639b960e6' # non hydro = 
#root_directory_id = '9bab68fdd2684008b4a5a93accbb032a' #PLM sandbox
#root_directory_id = '573eb91eb1484f1494658ec5f3c3583b' #test for security roles
#root_directory_id = 'aa54faa6b46840768311ac8b877c8d83' #Aadhi Sandbox
# =============================================================================
# Custom Code Logic
# =============================================================================
directoryName = ''

def add_directory_content(directory_id, level_id, hierarchy_id):
    model_count = 0
    try:
        level_id = level_id + 1
        logger.debug(directory_id) #activelogger
        tmp_id = ''
    
        directory_content = spm.get_directory_content(directory_id)
        #logger.debug(directory_content)
        iterator = 0
        for entry in directory_content:
            
            #logger.debug(entry['href'])
            #Skipping the l4 folder to avoid duplicates
            #dirName = ''
            #if entry['rel'] == 'dir':
               # dirName = entry['rep']['name']
            #logger.debug(dirName)
            #if dirName == 'L4 Processes':
                #logger.debug('L4 process folder skipped...')
               # tmp_id = ''
            
            if(entry['rel'] == 'dir') or (entry['rel'] == 'mod'):
                if hierarchy_id == 0:
                    iterator = iterator + 1
                    tmp_id = ''
                else:
                    iterator = iterator + 1
                    tmp_id = ''
                #logger.debug(str(tmp_id) + ': ' + entry['rep']['name'])
                  
                #DIRECTORY DATA
                if entry['rel'] == 'dir':
                    global directoryName
                    directoryName = entry['rep']['name']
                    if directoryName == 'Human Capital Management' or directoryName == 'Master Data Management' or directoryName == 'Plan to Perform (P2P)' or directoryName == 'L4 Process Flows':
                       logger.debug(directoryName) #activelogger
                       continue
                    report_data.append({'Process Area': directoryName,
                                        'ETE Group (Signavio Process Flow)':  html.unescape(entry['rep']['name']),
                                        'Source Industry L4': 'Directory',
                                        'Source Industry L3': '',
                                        'Industry Category L3': '',
                                        'Source Industry L2': '',
                                        'Industry Category L2': '',
                                        'Source Industry L1':'',
                                        'Industry Category L1': '',
                                        'Source Industry L0':'',
                                        'Industry Category L0': '',
                                        'L3 Description':'',
                                        'Source Industry L4 Taxonomy': '',
                                        'Source Industry L3 Taxonomy': '',
                                        'Source Industry L4 Practice': '',
                                        'Source Industry L3 Practice': '',
                                        'IT System': '',
                                        'L4 IT System': '',
                                        'Fiori App/Transaction':'',
                                        'L4 Fiori App/Transaction': '',
                                        'EM Capabilities': '',
                                        'E2E Scenario Owner': '', 
                                        'Value Chain Function': '',
                                        'Program L2': '',
                                        'Program Category L2': '',
                                        'Program L1': '',
                                        'Program Category L1': '',
                                        'Program L0': '',
                                        'Program Category L0': '',
                                        'Task Type':'',
                                        'L4 Task Type':'',
                                        'Security Composite Roles':'',
                                        'Signavio ID': entry['href'],
                                        'Signavio Link':'',
                                        'Model Description':''})
                    directory_id = entry['href']
                    add_directory_content(directory_id, level_id, tmp_id)
                     
                #DIAGRAM DATA
                if entry['rel'] == 'mod':
                    model_count = model_count + 1
                    #logger.debug(model_count)
                    #report_data.append({'Level': level_id,
                    #                    'Id': tmp_id,
                    #                   'E2E Scenario': '',
                    #                    'Name': html.unescape(entry['rep']['name']),          
                    #                    'Type': entry['rep'].get('type'),
                    #                    'L0':'',
                     #                   'L1':'',
                    #                    'L2':'',
                    #                    'Signavio ID': entry['href']}) 
                    e2eName = html.unescape(entry['rep']['name'])
                    e2eLink= html.unescape(entry['href'])
                    if e2eName.startswith('PS-'):
                        print("HYC variants - skip")
                        continue
                    
                    #TASK DATA
                    model_json = spm.get_model_json(entry['href'])
                    
                    #logger.debug(model_json) #activelogger
                    #logger.debug(model_json.get('properties', {}).get('meta-valuechainowner', {}))
                    modelDescription = model_json.get('properties',{}).get('documentation', {})
                    if model_json.get('properties', {}).get('meta-valuechainowner', {}):
                        e2eScenarioOwner = model_json.get('properties', {}).get('meta-valuechainowner', {})
                        e2eScenarioOwner = spm.get_glossary_entry(e2eScenarioOwner).get('title',{})
                        #logger.debug(e2eScenarioOwner)
                    else:
                        e2eScenarioOwner = '' 
                    
                    #if(model_json.get('properties', {}).get('meta-valuechainfunction', {})[0]):
                    #    valueChainFunction = model_json.get('properties', {}).get('meta-valuechainfunction', {})[0]
                    #    valueChainFunction = spm.get_glossary_entry(valueChainFunction).get('title',{})
                    #else:
                    valueChainFunction = ''
                   
                   
                
                    tasks = filter_childshapes(model_json, filter_list=['Task','CollapsedSubprocess'])
                    for index, task in enumerate(tasks):
                        name = task.get('properties',{}).get('name','')
                        tasktype = task.get('properties',{}).get('tasktype',{})
                        l4tasktype = task.get('properties',{}).get('meta-tasktype',{})
                        #logger.debug(tasktype) #activelogger
                        
                        taxonomy = ''
                        company =''
                        taskPractice = ''
                        itsystem =''
                        fiori =''
                        l3_category = ''
                        l2 =''
                        l2_category = ''
                        l1 =''
                        l1_category = ''
                        l0 = ''
                        l0_category = ''
                        workdayL0 = ''
                        description =''
                        capabilities = ''
                        emParentDecomp =''
                        programCategoryL2 = ''
                        emL1 =''
                        programCategoryL1 = ''
                        emL0 = ''
                        programCategoryL0 = ''
                        taskL3 = ''
                        l4_l3Check = ''
                        
                        
                        
                        
                        #testt
                        
                        
                        if task.get('stencil',{}).get('id','') == 'CollapsedSubprocess':
                            
                            processURL = task.get('properties',{}).get('entry','')
                            #logger.debug(processURL)
                            model_json2 = spm.get_model_json(processURL)
                            subProcessTitle = task.get('properties',{}).get('name','')
                            
                            subprocesstasktype = task.get('properties',{}).get('meta-tasktype',{})
                            if subprocesstasktype == "ci1736949300755917559122":
                                subprocesstasktype = "Service"
                            elif subprocesstasktype == "ci173694930075581598861":
                                subprocesstasktype = "Manual"
                            elif subprocesstasktype == "ci1736949300755257495320":
                                subprocesstasktype = "User"
                                
                            #composite role extraction
                            compositeroles = task.get('properties',{}).get('meta-compositerole',{})
                            #logger.debug("Printing compo") #activelogger
                            #logger.debug(compositeroles) #activelogger
                            
                            securitycompositeroles = ''
                            
                            if not compositeroles:
                                #print("No associated composite roles")
                                securitycompositeroles = ''.join(securitycompositeroles)
                            else:
                                for role in compositeroles:
                                    glossid = role.partition("glossary/")[2]
                                    
                                    if not securitycompositeroles:
                                        securitycompositeroles += spm.get_glossary_entry(glossid).get('title',{})
                                    else:
                                        securitycompositeroles += ', ' + spm.get_glossary_entry(glossid).get('title',{})
                                
                            
                            resource_id = task.get('resourceId','')
                            task_id = str(tmp_id) + str(index+1) + '.' 
                            glossary_link=task.get('glossaryLinks',{}).get('name','')
                            if(glossary_link):
                                logger.debug('Glossary Link: ' + glossary_link[0]) #activelogger
                            else:
                                logger.debug('No dictionary item') #activelogger
                            glossary_results=''
                            if(glossary_link):
                                glossary_link=glossary_link[0][1:]
                                glossary_info=glossary_link+'/info'
                                glossary_hireachy=get_all_sub_directories(spm,glossary_info)
                                
                                #logger.debug(glossary_hireachy) #activelogger
                                if len(glossary_hireachy) > 2:
                                    if(len(glossary_hireachy[2]) > 0):
                                        itsystem = glossary_hireachy[2].replace('&amp;', '&').strip()
                                    else:
                                        itsystem = ''
                                else:
                                    itsystem = '' 
                                                               
                                if len(glossary_hireachy) > 3:
                                    if(len(glossary_hireachy[3]) > 0):
                                        fiori = glossary_hireachy[3].replace('&amp;', '&').strip()
                                    else:
                                        fiori = ''   
                                else:
                                    fiori = ''
                                
                                if len(glossary_hireachy) > 4:
                                    if(len(glossary_hireachy[4]) > 0):
                                        l2 = glossary_hireachy[4].replace('&amp;', '&').strip()
                                    else:
                                        l2 = ''   
                                else:
                                    l2 = ''
                                    
                                
                                                                    
                                if len(glossary_hireachy) > 5:
                                     l1 = glossary_hireachy[5].replace('&amp;', '&').strip()
                                else:
                                     l1 = ''
                                
                                if len(glossary_hireachy) > 6:
                                      l0 = glossary_hireachy[6].replace('&amp;', '&').strip()
                                else:
                                      l0 = ''     
                                
                                if len(glossary_hireachy) > 7:
                                    workdayL0 = glossary_hireachy[7].replace('&amp;', '&').strip()
                                else:
                                    workdayL0 = ''
                                
                                if len(glossary_hireachy) > 8:
                                    if len(glossary_hireachy[8]) > 0:
                                        description = glossary_hireachy[8].replace('&amp;', '&').strip()
                                    else:
                                        description = ''
                                else:
                                    description = ''
                                    
                                if len(glossary_hireachy) > 9:    
                                    capabilities = glossary_hireachy[9].replace('&amp;', '&').strip()
                                else:
                                    capabilities = ''
                                
                                if len(glossary_hireachy) > 10:    
                                    emParentDecomp = glossary_hireachy[10].replace('&amp;', '&').strip()
                                else:
                                    emParentDecomp = ''
                                
                                if len(glossary_hireachy) > 11:    
                                    emL1 = glossary_hireachy[11].replace('&amp;', '&').strip()
                                else:
                                    emL1 = ''
                                
                                if len(glossary_hireachy) > 12:    
                                    emL0 = glossary_hireachy[12].replace('&amp;', '&').strip()
                                else:
                                    emL0 = ''
                                
                                if len(glossary_hireachy) > 13:    
                                    l2_category = glossary_hireachy[13].replace('&amp;', '&').strip()
                                else:
                                    l2_category = ''
                                
                                if len(glossary_hireachy) > 14:    
                                    l1_category = glossary_hireachy[14].replace('&amp;', '&').strip()
                                else:
                                    l1_category = ''
                                
                                if len(glossary_hireachy) > 15:    
                                    l0_category = glossary_hireachy[15].replace('&amp;', '&').strip()
                                else:
                                    l0_category = ''
                                
                                if len(glossary_hireachy) > 16:    
                                    l3_category = glossary_hireachy[16].replace('&amp;', '&').strip()
                                else:
                                    l3_category = ''
                                
                                if len(glossary_hireachy) > 17:    
                                    programCategoryL2 = glossary_hireachy[17].replace('&amp;', '&').strip()
                                else:
                                    programCategoryL2 = ''
                                
                                if len(glossary_hireachy) > 18:    
                                    programCategoryL1 = glossary_hireachy[18].replace('&amp;', '&').strip()
                                else:
                                    programCategoryL1 = ''
                                if len(glossary_hireachy) > 19:    
                                    programCategoryL0 = glossary_hireachy[19].replace('&amp;', '&').strip()
                                else:
                                    programCategoryL0 = ''
                                
                                #print(taxonomy, l2)
                                    
                                    
                            else:
                                l4 = ''
                                l3 = ''
                                l2 = ''
                                l2_category = 'Error'
                                l3_category = ''
                                l1 = ''
                                l1_category = ''
                                l0 = ''
                                l0_category
                                workdayL0 = ''
                                description = ''
                                taxonomy = ''
                                company = ''
                                itsystem = ''
                                fiori = ''
                                capabilities = ''
                                e2eScenarioOwner = ''
                                valueChainFunction = ''
                                emParentDecomp = ''
                                programCategoryL2 = ''
                                emL1 =''
                                programCategoryL1 = ''
                                emL0 = ''
                                programCategoryL0 = ''
                                
                                
                            #logger.debug(task_id + name)
                            
                            
                            #logger.debug(model_json2)
                            #report_data.append({'ETE Group (Signavio Process Flow)': e2eName,
                                                #'Source Industry L4':'',
                                                #'Source Industry L3':subProcessTitle,
                                                #'Industry Category L3': 'Sub-Process'})
                                
                            if model_json2:
                                l4Tasks = filter_childshapes(model_json2, filter_list =['Task'])
                            if l4Tasks:
                                for index, l4Task in enumerate(l4Tasks):
                                    name = l4Task.get('properties',{}).get('name','')
                                    tasktype = l4Task.get('properties',{}).get('tasktype',{})
                                    
                                    #--Needs to be converted to a function accordingly----
                                    
                                    resource_id = l4Task.get('resourceId','')
                                    task_id = str(tmp_id) + str(index+1) + '.' 
                                    glossary_link=l4Task.get('glossaryLinks',{}).get('name','')
                                    if(glossary_link):
                                        logger.debug('Glossary Link: ' + glossary_link[0]) #activelogger
                                    else:
                                        logger.debug('No dictionary item') #activelogger
                                    glossary_results=''
                                    if(glossary_link):
                                        glossary_link=glossary_link[0][1:]
                                        glossary_info=glossary_link+'/info'
                                        glossary_hireachy=get_all_sub_directories(spm,glossary_info)
                                        
                                        logger.debug(f"Gloss Hierarchy:{glossary_hireachy}") #activelogger
                                        
                                        if len(glossary_hireachy) > 0:
                                            if(len(glossary_hireachy[0]) > 0):
                                                taskTaxonomy = glossary_hireachy[0].replace('&amp;', '&').strip()
                                            else:
                                                taskTaxonomy = ''
                                        else:
                                            taskTaxonomy = ''
                                            
                                            
                                        if len(glossary_hireachy) > 1:
                                            if(len(glossary_hireachy[1]) > 0):
                                                taskPractice = glossary_hireachy[1].replace('&amp;', '&').strip()
                                            else:
                                                taskPractice = ''
                                        else:
                                            taskPractice = ''
                                            
                                        if len(glossary_hireachy) > 2:
                                            if(len(glossary_hireachy[2]) > 0):
                                                l4itsystem = glossary_hireachy[2].replace('&amp;', '&').strip()
                                            else:
                                                l4itsystem = ''
                                        else:
                                            l4itsystem = '' 
                                                                       
                                        if len(glossary_hireachy) > 3:
                                            if(len(glossary_hireachy[3]) > 0):
                                                l4fiori = glossary_hireachy[3].replace('&amp;', '&').strip()
                                            else:
                                                l4fiori = ''   
                                        else:
                                            l4fiori = ''
                                            
                                        if len(glossary_hireachy) > 4:
                                            if(len(glossary_hireachy[4]) > 0):
                                                taskL3 = glossary_hireachy[4].replace('&amp;', '&').strip()
                                                print(f"glosslev4: {taskL3}")
                                            else:
                                                taskL3 = ''   
                                        else:
                                            taskL3 = ''
                                            
                                        if len(glossary_hireachy) > 4:
                                            if(len(glossary_hireachy[4]) > 0):
                                                l2 = glossary_hireachy[4].replace('&amp;', '&').strip()
                                            else:
                                                l2 = ''   
                                        else:
                                            l2 = ''
                                            
                                                                            
                                        if len(glossary_hireachy) > 5:
                                             l1 = glossary_hireachy[5].replace('&amp;', '&').strip()
                                        else:
                                             l1 = ''
                                        
                                        if len(glossary_hireachy) > 6:
                                              l0 = glossary_hireachy[6].replace('&amp;', '&').strip()
                                        else:
                                              l0 = ''
                                        
                                    #L4-> L3 tagging check
                                        
                                        if taskL3 == subProcessTitle:
                                            l4_l3Check ='L3 dictionary Parent matching subprocess name'
                                        else:
                                            l4_l3Check = 'L3 dictionary Parent not matching subprocess name. L4 is currently linked to ' + l2 + ' as parent L3 instead of ' + subProcessTitle
                                         
                                    else:
                                        l4 = name
                                        l3 = subProcessTitle
                                        l2 = 'No Dictionary item linked'
                                        l2_category = ''
                                        l3_category = ''
                                        l1 = ''
                                        l1_category = ''
                                        l0 = ''
                                        l0_category
                                        workdayL0 = ''
                                        description = ''
                                        taskTaxonomy = ''
                                        taxonomy = ''
                                        taskPractice = ''
                                        company = ''
                                        itsystem = ''
                                        fiori = ''
                                        capabilities = ''
                                        e2eScenarioOwner = ''
                                        valueChainFunction = ''
                                        emParentDecomp = ''
                                        programCategoryL2 = ''
                                        emL1 =''
                                        programCategoryL1 = ''
                                        emL0 = ''
                                        programCategoryL0 = ''
                                        
                                    #logger.debug(task_id + name)
                                    if (len(workdayL0)) > 0:
                                        report_data.append({'ETE Group (Signavio Process Flow)': e2eName,
                                                            'Source Industry L4':name,
                                                            'Source Industry L3':l2,
                                                            'Industry Category L3': l2_category,
                                                            'Source Industry L2':l1,
                                                            'Industry Category L2': l1_category,
                                                            'Source Industry L1':l0,
                                                            'Industry Category L1': l1_category,
                                                            'Source Industry L0': workdayL0,
                                                            'Industry Category L0': l0_category,
                                                            'L3 Description': description,
                                                            'Source Industry L4 Taxonomy': taskTaxonomy,
                                                            'Source Industry L3 Taxonomy': taxonomy,
                                                            'Source Industry L4 Practice': taskPractice,
                                                            'Source Industry L3 Practice': company,
                                                            'L3 IT System': itsystem,
                                                            'L4 IT System': l4itsystem,
                                                            'Fiori App/Transaction': fiori,
                                                            'L4 Fiori App/Transaction': l4fiori,
                                                            'EM Capabilities': capabilities,
                                                            'E2E Scenario Owner': e2eScenarioOwner,
                                                            'Value Chain Function': valueChainFunction,
                                                            'Program L2': emParentDecomp,
                                                            'Program Category L2': programCategoryL2,
                                                            'Program L1': emL1,
                                                            'Program Category L1': programCategoryL1,
                                                            'Program L0': emL0,
                                                            'Program Category L0': programCategoryL0,
                                                            'Task Type':subprocesstasktype,
                                                            'L4 Task Type':tasktype,
                                                            'Composite Role':securitycompositeroles,
                                                            'Signavio ID': resource_id,
                                                            'Signavio Link': 'https://app-us.signavio.com/p/hub' + e2eLink,
                                                            'Model Description':modelDescription,
                                                            'L4->L3 Tagging Check':l4_l3Check}) 
                                    else:
                                        report_data.append({'Process Area': directoryName,
                                                            'ETE Group (Signavio Process Flow)': e2eName,
                                                            'Source Industry L4': name,
                                                            'Source Industry L3': subProcessTitle,
                                                            'Industry Category L3': l3_category,
                                                            'Source Industry L2':l2,
                                                            'Industry Category L2':l2_category,
                                                            'Source Industry L1':l1,
                                                            'Industry Category L1': l1_category,
                                                            'Source Industry L0':l0,
                                                            'Industry Category L0': '',
                                                            'L3 Description': description,
                                                            'Source Industry L4 Taxonomy': taskTaxonomy,
                                                            'Source Industry L3 Taxonomy': taxonomy,
                                                            'Source Industry L4 Practice': taskPractice,
                                                            'Source Industry L3 Practice': company,
                                                            'IT System': itsystem,
                                                            'L4 IT System': l4itsystem,
                                                            'Fiori App/Transaction':fiori,
                                                            'L4 Fiori App/Transaction': l4fiori,
                                                            'EM Capabilities': capabilities,
                                                            'E2E Scenario Owner': e2eScenarioOwner,
                                                            'Value Chain Function': valueChainFunction,
                                                            'Program L2': emParentDecomp,
                                                            'Program Category L2': programCategoryL2,
                                                            'Program L1': emL1,
                                                            'Program Category L1': programCategoryL1,
                                                            'Program L0': emL0,
                                                            'Program Category L0': programCategoryL0,
                                                            'Task Type':subprocesstasktype,
                                                            'L4 Task Type':tasktype,
                                                            'Composite Role':securitycompositeroles,
                                                            'Signavio ID': resource_id,
                                                            'Signavio Link': 'https://app-us.signavio.com/p/hub' + e2eLink,
                                                            'Model Description':modelDescription,
                                                            'L4->L3 Tagging Check':l4_l3Check})
                            
                                
                                    
                                
                        else:
                            
                            resource_id = task.get('resourceId','')
                            task_id = str(tmp_id) + str(index+1) + '.' 
                            
                            #composite role extraction
                            compositeroles = task.get('properties',{}).get('meta-compositerole',{})
                            #logger.debug("Printing compo") #activelogger
                            #logger.debug(compositeroles) #activelogger
                            
                            securitycompositeroles = ''
                            
                            if not compositeroles:
                                #print("No associated composite roles")
                                securitycompositeroles = ''.join(securitycompositeroles)
                            else:
                                for role in compositeroles:
                                    glossid = role.partition("glossary/")[2]
                                    
                                    if not securitycompositeroles:
                                        securitycompositeroles += spm.get_glossary_entry(glossid).get('title',{})
                                    else:
                                        securitycompositeroles += ', ' + spm.get_glossary_entry(glossid).get('title',{})
                                    
                            
                           
                            
                            glossary_link=task.get('glossaryLinks',{}).get('name','')
                            if(glossary_link):
                                logger.debug('Glossary Link: ' + glossary_link[0]) #activelogger
                            else:
                                logger.debug('No dictionary item')
                            glossary_results=''
                            if(glossary_link):
                                glossary_link=glossary_link[0][1:]
                                glossary_info=glossary_link+'/info'
                                glossary_hireachy=get_all_sub_directories(spm,glossary_info)
                                
                                if(glossary_hireachy):
                                    logger.debug(glossary_hireachy)
                                    if len(glossary_hireachy) > 0:
                                        if(len(glossary_hireachy[0]) > 0):
                                            taxonomy = glossary_hireachy[0].replace('&amp;', '&').strip()
                                        else:
                                            taxonomy = ''
                                    else:
                                         taxonomy = ''    
                                    
                                    if len(glossary_hireachy) > 1:
                                        if(len(glossary_hireachy[1]) > 0):
                                            company = glossary_hireachy[1].replace('&amp;', '&').strip()
                                        else:
                                            company = ''
                                    else:
                                        company = ''  
                                    
                                    if len(glossary_hireachy) > 2:
                                        if(len(glossary_hireachy[2]) > 0):
                                            itsystem = glossary_hireachy[2].replace('&amp;', '&').strip()
                                        else:
                                            itsystem = ''
                                    else:
                                        itsystem = '' 
                                                                   
                                    if len(glossary_hireachy) > 3:
                                        if(len(glossary_hireachy[3]) > 0):
                                            fiori = glossary_hireachy[3].replace('&amp;', '&').strip()
                                        else:
                                            fiori = ''   
                                    else:
                                        fiori = ''
                                    
                                    if len(glossary_hireachy) > 4:
                                        if(len(glossary_hireachy[4]) > 0):
                                            l2 = glossary_hireachy[4].replace('&amp;', '&').strip()
                                        else:
                                            l2 = ''   
                                    else:
                                        l2 = ''
                                        
                                    
                                                                        
                                    if len(glossary_hireachy) > 5:
                                         l1 = glossary_hireachy[5].replace('&amp;', '&').strip()
                                    else:
                                         l1 = ''
                                    
                                    if len(glossary_hireachy) > 6:
                                          l0 = glossary_hireachy[6].replace('&amp;', '&').strip()
                                    else:
                                          l0 = ''     
                                    
                                    if len(glossary_hireachy) > 7:
                                        workdayL0 = glossary_hireachy[7].replace('&amp;', '&').strip()
                                    else:
                                        workdayL0 = ''
                                    
                                    if len(glossary_hireachy) > 8:
                                        if len(glossary_hireachy[8]) > 0:
                                            description = glossary_hireachy[8].replace('&amp;', '&').strip()
                                        else:
                                            description = ''
                                    else:
                                        description = ''
                                        
                                    if len(glossary_hireachy) > 9:    
                                        capabilities = glossary_hireachy[9].replace('&amp;', '&').strip()
                                    else:
                                        capabilities = ''
                                    
                                    if len(glossary_hireachy) > 10:    
                                        emParentDecomp = glossary_hireachy[10].replace('&amp;', '&').strip()
                                    else:
                                        emParentDecomp = ''
                                    
                                    if len(glossary_hireachy) > 11:    
                                        emL1 = glossary_hireachy[11].replace('&amp;', '&').strip()
                                    else:
                                        emL1 = ''
                                    
                                    if len(glossary_hireachy) > 12:    
                                        emL0 = glossary_hireachy[12].replace('&amp;', '&').strip()
                                    else:
                                        emL0 = ''
                                    
                                    if len(glossary_hireachy) > 13:    
                                        l2_category = glossary_hireachy[13].replace('&amp;', '&').strip()
                                    else:
                                        l2_category = ''
                                    
                                    if len(glossary_hireachy) > 14:    
                                        l1_category = glossary_hireachy[14].replace('&amp;', '&').strip()
                                    else:
                                        l1_category = ''
                                    
                                    if len(glossary_hireachy) > 15:    
                                        l0_category = glossary_hireachy[15].replace('&amp;', '&').strip()
                                    else:
                                        l0_category = ''
                                    
                                    if len(glossary_hireachy) > 16:    
                                        l3_category = glossary_hireachy[16].replace('&amp;', '&').strip()
                                    else:
                                        l3_category = ''
                                    
                                    if len(glossary_hireachy) > 17:    
                                        programCategoryL2 = glossary_hireachy[17].replace('&amp;', '&').strip()
                                    else:
                                        programCategoryL2 = ''
                                    
                                    if len(glossary_hireachy) > 18:    
                                        programCategoryL1 = glossary_hireachy[18].replace('&amp;', '&').strip()
                                    else:
                                        programCategoryL1 = ''
                                    if len(glossary_hireachy) > 19:    
                                        programCategoryL0 = glossary_hireachy[19].replace('&amp;', '&').strip()
                                    else:
                                        programCategoryL0 = ''
                                    
                                    
                            else:
                                l2 = 'No dictionary item linked'
                                l2_category = ''
                                l3_category = ''
                                l1 = ''
                                l1_category = ''
                                l0 = ''
                                l0_category
                                workdayL0 = ''
                                description = ''
                                taxonomy = ''
                                company = ''
                                itsystem = ''
                                fiori = ''
                                capabilities = ''
                                e2eScenarioOwner = ''
                                valueChainFunction = ''
                                emParentDecomp = ''
                                programCategoryL2 = ''
                                emL1 =''
                                programCategoryL1 = ''
                                emL0 = ''
                                programCategoryL0 = ''
                                
                            #logger.debug(task_id + name)
                            if (len(workdayL0)) > 0:
                                report_data.append({'Process Area': directoryName,
                                                    'ETE Group (Signavio Process Flow)': e2eName,
                                                    'Source Industry L4':html.unescape(name),
                                                    'Source Industry L3':l2,
                                                    'Industry Category L3': l2_category,
                                                    'Source Industry L2':l1,
                                                    'Industry Category L2': l1_category,
                                                    'Source Industry L1':l0,
                                                    'Industry Category L1': 'Workday Level 1 - Process Group',
                                                    'Source Industry L0': workdayL0,
                                                    'Industry Category L0': 'Workday Level 0 - Enterprise Processes',
                                                    'Description': description,
                                                    'Source Industry L4 Taxonomy': '',
                                                    'Source Industry L3 Taxonomy': taxonomy,
                                                    'Source Industry L4 Practice': taskPractice,
                                                    'Source Industry L3 Practice': company,
                                                    'IT System': itsystem,
                                                    'L4 IT System':'',
                                                    'Fiori App/Transaction': fiori,
                                                    'L4 Fiori App/Transaction': '',
                                                    'EM Capabilities': capabilities,
                                                    'E2E Scenario Owner': e2eScenarioOwner,
                                                    'Value Chain Function': valueChainFunction,
                                                    'Program L2': emParentDecomp,
                                                    'Program Category L2': programCategoryL2,
                                                    'Program L1': emL1,
                                                    'Program Category L1': programCategoryL1,
                                                    'Program L0': emL0,
                                                    'Program Category L0': programCategoryL0,
                                                    'Task Type':html.unescape(tasktype),
                                                    'L4 Task Type':'',
                                                    'Composite Role':securitycompositeroles,
                                                    'Signavio ID': resource_id,
                                                    'Signavio Link': 'https://app-us.signavio.com/p/hub' + e2eLink,
                                                    'Model Description':modelDescription,
                                                    'L4->L3 Tagging Check':''}) 
                            else:
                                report_data.append({'Process Area': directoryName,
                                                    'ETE Group (Signavio Process Flow)': e2eName,
                                                    'Source Industry L4': '',
                                                    'Source Industry L3': html.unescape(name),
                                                    'Industry Category L3': l3_category,
                                                    'Source Industry L2':l2,
                                                    'Industry Category L2': l2_category,
                                                    'Source Industry L1':l1,
                                                    'Industry Category L1': l1_category,
                                                    'Source Industry L0':l0,
                                                    'Industry Category L0': l0_category,
                                                    'L3 Description': description,
                                                    'Source Industry L4 Taxonomy': '',
                                                    'Source Industry L3 Taxonomy': taxonomy,
                                                    'Source Industry L4 Practice': '',
                                                    'Source Industry L3 Practice': company,
                                                    'IT System': itsystem,
                                                    'L4 IT System':'',
                                                    'Fiori App/Transaction':fiori,
                                                    'L4 Fiori App/Transaction': '',
                                                    'EM Capabilities': capabilities,
                                                    'E2E Scenario Owner': e2eScenarioOwner,
                                                    'Value Chain Function': valueChainFunction,
                                                    'Program L2': emParentDecomp,
                                                    'Program Category L2': programCategoryL2,
                                                    'Program L1': emL1,
                                                    'Program Category L1': programCategoryL1,
                                                    'Program L0': emL0,
                                                    'Program Category L0': programCategoryL0,
                                                    'Task Type':html.unescape(tasktype),
                                                    'L4 Task Type':'',
                                                    'Composite Role':securitycompositeroles,
                                                    'Signavio ID': resource_id,
                                                    'Signavio Link': 'https://app-us.signavio.com/p/hub' + e2eLink,
                                                    'Model Description':modelDescription,
                                                    'L4->L3 Tagging Check':''})       
                                
                                
    except Exception as err:
        pass
        logger.error(tmp_id + ' ' + type(err).__name__ + traceback.format_exc())
        errors[tmp_id] = traceback.format_exc()

#L3 only extraction

def add_directory_contentL3Only(directory_id, level_id, hierarchy_id):
    model_count = 0
    try:
        level_id = level_id + 1
        logger.debug(directory_id)
        tmp_id = ''
    
        directory_content = spm.get_directory_content(directory_id)
        #logger.debug(directory_content)
        iterator = 0
        for entry in directory_content:
            
            logger.debug(entry['href'])
            #Skipping the l4 folder to avoid duplicates
            #dirName = ''
            #if entry['rel'] == 'dir':
               # dirName = entry['rep']['name']
            #logger.debug(dirName)
            #if dirName == 'L4 Processes':
                #logger.debug('L4 process folder skipped...')
               # tmp_id = ''
            
            if(entry['rel'] == 'dir') or (entry['rel'] == 'mod'):
                if hierarchy_id == 0:
                    iterator = iterator + 1
                    tmp_id = ''
                else:
                    iterator = iterator + 1
                    tmp_id = ''
                #logger.debug(str(tmp_id) + ': ' + entry['rep']['name'])
                  
                #DIRECTORY DATA
                if entry['rel'] == 'dir':
                    directoryName = entry['rep']['name']
                    e2eLink= html.unescape(entry['href'])
                    if directoryName == 'Human Capital Management' or directoryName == 'Master Data Management' or directoryName == 'Plan to Perform (P2P)' or directoryName == 'L4 Process Flows':
                       logger.debug(directoryName)
                       continue
                    report_data.append({'ETE Group (Signavio Process Flow)':  html.unescape(entry['rep']['name']),
                                        'Source Industry L4': 'Directory',
                                        'Source Industry L3': '',
                                        'Industry Category L3': '',
                                        'Source Industry L2': '',
                                        'Industry Category L2': '',
                                        'Source Industry L1':'',
                                        'Industry Category L1': '',
                                        'Source Industry L0':'',
                                        'Industry Category L0': '',
                                        'Description':'',
                                        'Source Industry Taxonomy': '',
                                        'Source Industry Practice': '',
                                        'IT System': '',
                                        'Fiori App/Transaction':'',
                                        'EM Capabilities': '',
                                        'E2E Scenario Owner': '', 
                                        'Value Chain Function': '',
                                        'Program L2': '',
                                        'Program Category L2': '',
                                        'Program L1': '',
                                        'Program Category L1': '',
                                        'Program L0': '',
                                        'Program Category L0': '',
                                        'Task Type':'',
                                        'Signavio ID': entry['href'],
                                        'Signavio Link':'https://app-us.signavio.com/p/hub' + e2eLink,
                                        'Model Description':modelDescription})
                    directory_id = entry['href']
                    add_directory_contentL3Only(directory_id, level_id, tmp_id)
                     
                #DIAGRAM DATA
                if entry['rel'] == 'mod':
                    model_count = model_count + 1
                    #logger.debug(model_count)
                    #report_data.append({'Level': level_id,
                    #                    'Id': tmp_id,
                    #                   'E2E Scenario': '',
                    #                    'Name': html.unescape(entry['rep']['name']),          
                    #                    'Type': entry['rep'].get('type'),
                    #                    'L0':'',
                     #                   'L1':'',
                    #                    'L2':'',
                    #                    'Signavio ID': entry['href']}) 
                    e2eName = html.unescape(entry['rep']['name'])
                    e2eLink= html.unescape(entry['href'])
                    
                    #TASK DATA
                    model_json = spm.get_model_json(entry['href'])
                    
                    #print("Model Json for the flow:")
                    #logger.debug(model_json)
                    #logger.debug(model_json.get('properties', {}).get('meta-valuechainowner', {}))
                    if model_json.get('properties', {}).get('meta-valuechainowner', {}):
                        e2eScenarioOwner = model_json.get('properties', {}).get('meta-valuechainowner', {})
                        e2eScenarioOwner = spm.get_glossary_entry(e2eScenarioOwner).get('title',{})
                        #logger.debug(e2eScenarioOwner)
                    else:
                        e2eScenarioOwner = '' 
                    
                    #if(model_json.get('properties', {}).get('meta-valuechainfunction', {})[0]):
                    #    valueChainFunction = model_json.get('properties', {}).get('meta-valuechainfunction', {})[0]
                    #    valueChainFunction = spm.get_glossary_entry(valueChainFunction).get('title',{})
                    #else:
                    valueChainFunction = ''
                   
                  
                    
                    tasks = filter_childshapes(model_json, filter_list=['Task','CollapsedSubprocess'])
                    for index, task in enumerate(tasks):
                        name = task.get('properties',{}).get('name','')
                        if task.get('properties',{}).get('meta-tasktype',{}) == 'ci1736949300755257495320':
                            tasktype = 'User'
                        elif task.get('properties',{}).get('meta-tasktype',{}) == 'ci1736949300755917559122':
                            tasktype = 'Service'
                        else: 
                            tasktype = task.get('properties',{}).get('tasktype',{})
                        #logger.debug(task)
                        
                        taxonomy = ''
                        company =''
                        itsystem =''
                        fiori =''
                        l3_category = ''
                        l2 =''
                        l2_category = ''
                        l1 =''
                        l1_category = ''
                        l0 = ''
                        l0_category = ''
                        workdayL0 = ''
                        description =''
                        capabilities = ''
                        emParentDecomp =''
                        programCategoryL2 = ''
                        emL1 =''
                        programCategoryL1 = ''
                        emL0 = ''
                        programCategoryL0 = ''
                        
                        #testt
                        
                        
                        if task.get('stencil',{}).get('id','') == 'CollapsedSubprocess':
                            processURL = task.get('properties',{}).get('entry','')
                            #logger.debug(processURL)
                            model_json2 = spm.get_model_json(processURL)
                            glossary_link=task.get('glossaryLinks',{}).get('name','')
                            if(glossary_link):
                                logger.debug('Glossary Link: ' + glossary_link[0])
                            else:
                                logger.debug('No dictionary item')
                            glossary_results=''
                            if(glossary_link):
                                glossary_link=glossary_link[0][1:]
                                glossary_info=glossary_link+'/info'
                                glossary_hireachy=get_all_sub_directories(spm,glossary_info)
                                
                                if(glossary_hireachy):
                                    logger.debug(glossary_hireachy)
                                    if len(glossary_hireachy) > 0:
                                        if(len(glossary_hireachy[0]) > 0):
                                            taxonomy = glossary_hireachy[0].replace('&amp;', '&').strip()
                                        else:
                                            taxonomy = ''
                                    else:
                                         taxonomy = ''    
                                    
                                    if len(glossary_hireachy) > 1:
                                        if(len(glossary_hireachy[1]) > 0):
                                            company = glossary_hireachy[1].replace('&amp;', '&').strip()
                                        else:
                                            company = ''
                                    else:
                                        company = ''  
                                    
                                    if len(glossary_hireachy) > 2:
                                        if(len(glossary_hireachy[2]) > 0):
                                            itsystem = glossary_hireachy[2].replace('&amp;', '&').strip()
                                        else:
                                            itsystem = ''
                                    else:
                                        itsystem = '' 
                                                                   
                                    if len(glossary_hireachy) > 3:
                                        if(len(glossary_hireachy[3]) > 0):
                                            fiori = glossary_hireachy[3].replace('&amp;', '&').strip()
                                        else:
                                            fiori = ''   
                                    else:
                                        fiori = ''
                                    
                                    if len(glossary_hireachy) > 4:
                                        if(len(glossary_hireachy[4]) > 0):
                                            l2 = glossary_hireachy[4].replace('&amp;', '&').strip()
                                        else:
                                            l2 = ''   
                                    else:
                                        l2 = ''
                                                                        
                                    if len(glossary_hireachy) > 5:
                                         l1 = glossary_hireachy[5].replace('&amp;', '&').strip()
                                    else:
                                         l1 = ''
                                    
                                    if len(glossary_hireachy) > 6:
                                          l0 = glossary_hireachy[6].replace('&amp;', '&').strip()
                                    else:
                                          l0 = ''     
                                    
                                    if len(glossary_hireachy) > 7:
                                        workdayL0 = glossary_hireachy[7].replace('&amp;', '&').strip()
                                    else:
                                        workdayL0 = ''
                                    
                                    if len(glossary_hireachy) > 8:
                                        if len(glossary_hireachy[8]) > 0:
                                            description = glossary_hireachy[8].replace('&amp;', '&').strip()
                                        else:
                                            description = ''
                                    else:
                                        description = ''
                                        
                                    if len(glossary_hireachy) > 9:    
                                        capabilities = glossary_hireachy[9].replace('&amp;', '&').strip()
                                    else:
                                        capabilities = ''
                                    
                                    if len(glossary_hireachy) > 10:    
                                        emParentDecomp = glossary_hireachy[10].replace('&amp;', '&').strip()
                                    else:
                                        emParentDecomp = ''
                                    
                                    if len(glossary_hireachy) > 11:    
                                        emL1 = glossary_hireachy[11].replace('&amp;', '&').strip()
                                    else:
                                        emL1 = ''
                                    
                                    if len(glossary_hireachy) > 12:    
                                        emL0 = glossary_hireachy[12].replace('&amp;', '&').strip()
                                    else:
                                        emL0 = ''
                                    
                                    if len(glossary_hireachy) > 13:    
                                        l2_category = glossary_hireachy[13].replace('&amp;', '&').strip()
                                    else:
                                        l2_category = ''
                                    
                                    if len(glossary_hireachy) > 14:    
                                        l1_category = glossary_hireachy[14].replace('&amp;', '&').strip()
                                    else:
                                        l1_category = ''
                                    
                                    if len(glossary_hireachy) > 15:    
                                        l0_category = glossary_hireachy[15].replace('&amp;', '&').strip()
                                    else:
                                        l0_category = ''
                                    
                                    if len(glossary_hireachy) > 16:    
                                        l3_category = glossary_hireachy[16].replace('&amp;', '&').strip()
                                    else:
                                        l3_category = ''
                                    
                                    if len(glossary_hireachy) > 17:    
                                        programCategoryL2 = glossary_hireachy[17].replace('&amp;', '&').strip()
                                    else:
                                        programCategoryL2 = ''
                                    
                                    if len(glossary_hireachy) > 18:    
                                        programCategoryL1 = glossary_hireachy[18].replace('&amp;', '&').strip()
                                    else:
                                        programCategoryL1 = ''
                                    if len(glossary_hireachy) > 19:    
                                        programCategoryL0 = glossary_hireachy[19].replace('&amp;', '&').strip()
                                    else:
                                        programCategoryL0 = ''
                                    
                            resource_id = task.get('resourceId','')
                            #print("Printing Model JSON")
                            #logger.debug(model_json2)
                            report_data.append({'ETE Group (Signavio Process Flow)': e2eName,
                                                'Source Industry L4':'Sub-Process',
                                                'Source Industry L3':task.get('properties',{}).get('name',''),
                                                'Industry Category L3': l3_category,
                                                'Source Industry L2': l2,
                                                'Industry Category L2': l2_category,
                                                'Source Industry L1': l1,
                                                'Industry Category L1': l1_category,
                                                'Source Industry L0':l0,
                                                'Industry Category L0': l0_category,
                                                'Description': description,
                                                'Source Industry Taxonomy': taxonomy,
                                                'Source Industry Practice': company,
                                                'IT System': itsystem,
                                                'Fiori App/Transaction':fiori,
                                                'EM Capabilities': capabilities,
                                                'E2E Scenario Owner': e2eScenarioOwner, 
                                                'Value Chain Function': '',
                                                'Program L2': emParentDecomp,
                                                'Program Category L2': programCategoryL2,
                                                'Program L1': emL1,
                                                'Program Category L1': programCategoryL1,
                                                'Program L0': emL0,
                                                'Program Category L0': programCategoryL0,
                                                'Task Type': tasktype,
                                                'Signavio ID': resource_id,
                                                'Signavio URL':'https://app-us.signavio.com/p/hub' + e2eLink,
                                                'Model Description':modelDescription})
                                
                        else:
                            
                            resource_id = task.get('resourceId','')
                            task_id = str(tmp_id) + str(index+1) + '.' 
                            glossary_link=task.get('glossaryLinks',{}).get('name','')
                            if(glossary_link):
                                logger.debug('Glossary Link: ' + glossary_link[0])
                            else:
                                logger.debug('No dictionary item')
                            glossary_results=''
                            if(glossary_link):
                                glossary_link=glossary_link[0][1:]
                                glossary_info=glossary_link+'/info'
                                glossary_hireachy=get_all_sub_directories(spm,glossary_info)
                                
                                if(glossary_hireachy):
                                    logger.debug(glossary_hireachy)
                                    if len(glossary_hireachy) > 0:
                                        if(len(glossary_hireachy[0]) > 0):
                                            taxonomy = glossary_hireachy[0].replace('&amp;', '&').strip()
                                        else:
                                            taxonomy = ''
                                    else:
                                         taxonomy = ''    
                                    
                                    if len(glossary_hireachy) > 1:
                                        if(len(glossary_hireachy[1]) > 0):
                                            company = glossary_hireachy[1].replace('&amp;', '&').strip()
                                        else:
                                            company = ''
                                    else:
                                        company = ''  
                                    
                                    if len(glossary_hireachy) > 2:
                                        if(len(glossary_hireachy[2]) > 0):
                                            itsystem = glossary_hireachy[2].replace('&amp;', '&').strip()
                                        else:
                                            itsystem = ''
                                    else:
                                        itsystem = '' 
                                                                   
                                    if len(glossary_hireachy) > 3:
                                        if(len(glossary_hireachy[3]) > 0):
                                            fiori = glossary_hireachy[3].replace('&amp;', '&').strip()
                                        else:
                                            fiori = ''   
                                    else:
                                        fiori = ''
                                    
                                    if len(glossary_hireachy) > 4:
                                        if(len(glossary_hireachy[4]) > 0):
                                            l2 = glossary_hireachy[4].replace('&amp;', '&').strip()
                                        else:
                                            l2 = ''   
                                    else:
                                        l2 = ''
                                                                        
                                    if len(glossary_hireachy) > 5:
                                         l1 = glossary_hireachy[5].replace('&amp;', '&').strip()
                                    else:
                                         l1 = ''
                                    
                                    if len(glossary_hireachy) > 6:
                                          l0 = glossary_hireachy[6].replace('&amp;', '&').strip()
                                    else:
                                          l0 = ''     
                                    
                                    if len(glossary_hireachy) > 7:
                                        workdayL0 = glossary_hireachy[7].replace('&amp;', '&').strip()
                                    else:
                                        workdayL0 = ''
                                    
                                    if len(glossary_hireachy) > 8:
                                        if len(glossary_hireachy[8]) > 0:
                                            description = glossary_hireachy[8].replace('&amp;', '&').strip()
                                        else:
                                            description = ''
                                    else:
                                        description = ''
                                        
                                    if len(glossary_hireachy) > 9:    
                                        capabilities = glossary_hireachy[9].replace('&amp;', '&').strip()
                                    else:
                                        capabilities = ''
                                    
                                    if len(glossary_hireachy) > 10:    
                                        emParentDecomp = glossary_hireachy[10].replace('&amp;', '&').strip()
                                    else:
                                        emParentDecomp = ''
                                    
                                    if len(glossary_hireachy) > 11:    
                                        emL1 = glossary_hireachy[11].replace('&amp;', '&').strip()
                                    else:
                                        emL1 = ''
                                    
                                    if len(glossary_hireachy) > 12:    
                                        emL0 = glossary_hireachy[12].replace('&amp;', '&').strip()
                                    else:
                                        emL0 = ''
                                    
                                    if len(glossary_hireachy) > 13:    
                                        l2_category = glossary_hireachy[13].replace('&amp;', '&').strip()
                                    else:
                                        l2_category = ''
                                    
                                    if len(glossary_hireachy) > 14:    
                                        l1_category = glossary_hireachy[14].replace('&amp;', '&').strip()
                                    else:
                                        l1_category = ''
                                    
                                    if len(glossary_hireachy) > 15:    
                                        l0_category = glossary_hireachy[15].replace('&amp;', '&').strip()
                                    else:
                                        l0_category = ''
                                    
                                    if len(glossary_hireachy) > 16:    
                                        l3_category = glossary_hireachy[16].replace('&amp;', '&').strip()
                                    else:
                                        l3_category = ''
                                    
                                    if len(glossary_hireachy) > 17:    
                                        programCategoryL2 = glossary_hireachy[17].replace('&amp;', '&').strip()
                                    else:
                                        programCategoryL2 = ''
                                    
                                    if len(glossary_hireachy) > 18:    
                                        programCategoryL1 = glossary_hireachy[18].replace('&amp;', '&').strip()
                                    else:
                                        programCategoryL1 = ''
                                    if len(glossary_hireachy) > 19:    
                                        programCategoryL0 = glossary_hireachy[19].replace('&amp;', '&').strip()
                                    else:
                                        programCategoryL0 = ''
                                    
                                    
                            else:
                                l2 = 'No dictionary item linked'
                                l2_category = ''
                                l3_category = ''
                                l1 = ''
                                l1_category = ''
                                l0 = ''
                                l0_category
                                workdayL0 = ''
                                description = ''
                                taxonomy = ''
                                company = ''
                                itsystem = ''
                                fiori = ''
                                capabilities = ''
                                e2eScenarioOwner = ''
                                valueChainFunction = ''
                                emParentDecomp = ''
                                programCategoryL2 = ''
                                emL1 =''
                                programCategoryL1 = ''
                                emL0 = ''
                                programCategoryL0 = ''
                                
                            #logger.debug(task_id + name)
                            if (len(workdayL0)) > 0:
                                report_data.append({'ETE Group (Signavio Process Flow)': e2eName,
                                                    'Source Industry L4':html.unescape(name),
                                                    'Source Industry L3':l2,
                                                    'Industry Category L3': l2_category,
                                                    'Source Industry L2':l1,
                                                    'Industry Category L2': l1_category,
                                                    'Source Industry L1':l0,
                                                    'Industry Category L1': 'Workday Level 1 - Process Group',
                                                    'Source Industry L0': workdayL0,
                                                    'Industry Category L0': 'Workday Level 0 - Enterprise Processes',
                                                    'Description': description,
                                                    'Source Industry Taxonomy': taxonomy,
                                                    'Source Industry Practice': company,
                                                    'IT System': itsystem,
                                                    'Fiori App/Transaction': fiori,
                                                    'EM Capabilities': capabilities,
                                                    'E2E Scenario Owner': e2eScenarioOwner,
                                                    'Value Chain Function': valueChainFunction,
                                                    'Program L2': emParentDecomp,
                                                    'Program Category L2': programCategoryL2,
                                                    'Program L1': emL1,
                                                    'Program Category L1': programCategoryL1,
                                                    'Program L0': emL0,
                                                    'Program Category L0': programCategoryL0,
                                                    'Task Type':html.unescape(tasktype),
                                                    'Signavio ID': resource_id,
                                                    'Signavio URL':'https://app-us.signavio.com/p/hub' + e2eLink,
                                                    'Model Description':modelDescription}) 
                            else:
                                report_data.append({'ETE Group (Signavio Process Flow)': e2eName,
                                                    'Source Industry L4': '',
                                                    'Source Industry L3': html.unescape(name),
                                                    'Industry Category L3': l3_category,
                                                    'Source Industry L2':l2,
                                                    'Industry Category L2': l2_category,
                                                    'Source Industry L1':l1,
                                                    'Industry Category L1': l1_category,
                                                    'Source Industry L0':l0,
                                                    'Industry Category L0': l0_category,
                                                    'Description': description,
                                                    'Source Industry Taxonomy': taxonomy,
                                                    'Source Industry Practice': company,
                                                    'IT System': itsystem,
                                                    'Fiori App/Transaction':fiori,
                                                    'EM Capabilities': capabilities,
                                                    'E2E Scenario Owner': e2eScenarioOwner,
                                                    'Value Chain Function': valueChainFunction,
                                                    'Program L2': emParentDecomp,
                                                    'Program Category L2': programCategoryL2,
                                                    'Program L1': emL1,
                                                    'Program Category L1': programCategoryL1,
                                                    'Program L0': emL0,
                                                    'Program Category L0': programCategoryL0,
                                                    'Task Type':html.unescape(tasktype),
                                                    'Signavio ID': resource_id,
                                                    'Signavio URL':'https://app-us.signavio.com/p/hub' + e2eLink,
                                                    'Model Description':modelDescription})       
                                
                                    

    except Exception as err:
        pass
        logger.error(tmp_id + ' ' + type(err).__name__ + traceback.format_exc())
        errors[tmp_id] = traceback.format_exc()

def get_all_sub_directories(spm, directoryID):
    try:
        directories = []
        print(f"Directory ID: {directoryID}")
        directory = spm.get_endpoint(directoryID)    
        #logger.debug(f"Directory Details:{directory}")
        description = directory.get('description', {})
        #description = description.replace('&amp;', '&')
        if(len(description)==0):
            description = ''
        description = description.replace('&amp;', '&')
        taxonomy = directory.get('metaDataValues', {}).get('meta-saptaxonomycode', {})
        company = directory.get('metaDataValues', {}).get('meta-sourceindustrypractice', {})
        l3_category_name = directory.get('categoryName')
        
        if(len(directory.get('metaDataValues', {}).get('meta-itsystem', {}))>0):
           itSystemObject = directory.get('metaDataValues', {}).get('meta-itsystem', {})
           itsystemArray = []
           itsystemString = ''
           for x in range(len(itSystemObject)):
               itsystemArray.append(directory.get('metaDataValues', {}).get('meta-itsystem', {})[x].get('title',''))
           itsystemString = ','.join(itsystemArray)
        else:
            itsystemString = ''
            
        if(len(directory.get('metaDataValues', {}).get('meta-fioriapptransaction', {}))>0):
           fioriObject = directory.get('metaDataValues', {}).get('meta-fioriapptransaction', {})
           fioriArray = []
           fioriString = ''
           for x in range(len(fioriObject)):
               fioriArray.append(directory.get('metaDataValues', {}).get('meta-fioriapptransaction', {})[x].get('title',''))
           fioriString = ','.join(fioriArray)
        else:
            fioriString = ''        
       
        if(len(directory.get('metaDataValues', {}).get('meta-emcapabilities', {}))>0):
          capabilitiesObject = directory.get('metaDataValues', {}).get('meta-emcapabilities', {})
          capabilitiesArray = []
          capabilitiesString = ''
          for x in range(len(capabilitiesObject)):
              capabilitiesArray.append(directory.get('metaDataValues', {}).get('meta-emcapabilities', {})[x].get('title',''))
          capabilitiesString = ','.join(capabilitiesArray)
        else:
           capabilitiesString = '' 
       
       
        emParentDecomp_id = ''
        if directory.get('metaDataValues', {}).get('meta-emdecompositionparent', {}):
            emParentDecomp = directory.get('metaDataValues', {}).get('meta-emdecompositionparent', {})
        else:
            emParentDecomp = ''
        em_l1 = ''
        em_l0 = ''
        em_categoryL2 = ''
        em_categoryL1 = ''
        em_categoryL0 = ''
        if len(emParentDecomp) > 0:
            emParentDecomp = directory.get('metaDataValues', {}).get('meta-emdecompositionparent', {}).get('title','')
            emParentDecomp_id = directory.get('metaDataValues', {}).get('meta-emdecompositionparent', {}).get('id', '')
            
        
        if len(emParentDecomp_id) > 0:
            em_id = 'glossary/' + emParentDecomp_id + '/info'
            em_parent = spm.get_endpoint(em_id)
            em_categoryL2 = em_parent.get('categoryName')
            em_l1 = em_parent.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('title','')
            em_l1_id = em_parent.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('id', '')
            if em_l1_id:
                em_id = 'glossary/' + em_l1_id + '/info'
                em_parent = spm.get_endpoint(em_id)
                em_categoryL1 = em_parent.get('categoryName')
                em_l0 = em_parent.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('title','')
                em_l0_id = em_parent.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('id', '')
                if em_l0_id:
                    em_id = 'glossary/' + em_l0_id + '/info'
                    em_parent = spm.get_endpoint(em_id)  
                    em_categoryL0 = em_parent.get('categoryName')
        
        industry_l2_name = ''
        industry_glossary_id_l2 = ''
        l2_category_name = ''
        l1_category_name = ''
        l0_category_name = ''
        industry_l2_name = directory.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('title', '')
        industry_glossary_id_l2 = directory.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('id', '')
        
        
     
        if len(industry_glossary_id_l2) > 0:
            industry_glossary_id_l2 = 'glossary/' + industry_glossary_id_l2 + '/info'
            industry_parent_item_l2 = spm.get_endpoint(industry_glossary_id_l2)
            #logger.debug(industry_parent_item_l2)
            l2_category_name = industry_parent_item_l2.get('categoryName')
            #logger.debug(l2_category_name)
            industry_l1_name = industry_parent_item_l2.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('title','')
            industry_glossary_id_l1 = industry_parent_item_l2.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('id', '')   
            
            if industry_glossary_id_l1:
                industry_glossary_id_l1 = 'glossary/' + industry_glossary_id_l1 + '/info'
                industry_parent_item_l1 = spm.get_endpoint(industry_glossary_id_l1)
                l1_category_name = industry_parent_item_l1.get('categoryName')
                industry_l0_name = industry_parent_item_l1.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('title','')
                industry_l0_id = industry_parent_item_l1.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('id','')                
                
                if industry_l0_id:
                    industry_glossary_id_HR = 'glossary/' + industry_l0_id + '/info'
                    industry_parent_item_HR = spm.get_endpoint(industry_glossary_id_HR)
                    #l0_category_name = industry_parent_item_HR.get('categoryName')
                    l0_category_name = ''
                    highRadiusL0 = industry_parent_item_HR.get('metaDataValues', {}).get('meta-sapprocessdecompositionpare', {}).get('title','')
                             
                
                
        logger.debug('Appending Values')
        directories.append(taxonomy)
        directories.append(company)
        directories.append(itsystemString)
        directories.append(fioriString)
        directories.append(industry_l2_name)
        directories.append(industry_l1_name)
        directories.append(industry_l0_name)
        directories.append(highRadiusL0)
        directories.append(description)
        directories.append(capabilitiesString)
        directories.append(emParentDecomp)
        directories.append(em_l1)
        directories.append(em_l0)
        directories.append(l2_category_name)
        directories.append(l1_category_name)
        directories.append(l0_category_name)
        directories.append(l3_category_name)
        directories.append(em_categoryL2)
        directories.append(em_categoryL1)
        directories.append(em_categoryL0)
        
        return directories
        
    except:
        return []

                

# =============================================================================
# Report Data Collection            
# =============================================================================
start_time = time.time()
errors = {}
report_data = []

userInput = ''
print("---------------------------------------")
print("HReport Code")
print(" ")
print("Select your option to extract HReport:")
print("*L3-L0 Hierarchy = Press 1")
print("*L4-L0 Hierarchy = Press 2")

userInput = input("Choose option:")

if userInput == '1':
    logger.debug("Running L3-L0 code..")
    add_directory_contentL3Only(directory_id=root_directory_id, level_id=0, hierarchy_id=0) 
    create_excel_report('L3 Report', report_data, save_directory='output', timezone='local')

elif userInput == '2':
    logger.debug("Running L4-L0 code..")
    add_directory_content(directory_id=root_directory_id, level_id=0, hierarchy_id=0) 
    create_excel_report('L4 Report', report_data, save_directory='output', timezone='local')
else:
    logger.debug("Wrong option")
      


# =============================================================================
# Runtime Information
# =============================================================================
logger.info('------ RESULTS -----')
logger.info('Total Runtime: ' + str(round((time.time() - start_time) / 60 , 2)) + ' minutes')
logger.info('Occured Errors: ' + str(len(errors)))
logger.info('Errors: ' + json.dumps(errors, indent=4))
