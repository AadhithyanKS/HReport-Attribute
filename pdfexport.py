import sys
sys.path.append(r"C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest")

print(sys.executable)

from SPM.spmclient import SPMClient
from SPM.utils import read_config, filter_childshapes, create_excel_report, export_model
from SPM.logger import logger
    
import traceback
import json
import time
import html
import os
import pikepdf

# =============================================================================
# Init
# =============================================================================
spm = SPMClient(r'C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest/SPM/spmconfig.yaml')
config = read_config(r'C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest/config.yaml')

#modelID = "8c5f2a39465b41d4898d7a49a9dcb351"
#modelID = "e44e1a8063714e778912b0647e7e7d8a"
#modelID = "233ed51104c644bdb30386efc1764fba"
#modelID = "e0c192d445f04fac8bdd0352c5f6609f"
#sid = "sid-AF04675B-DDF5-45F9-ACE7-001223265EB8"
#directory_id = "573eb91eb1484f1494658ec5f3c3583b" #orderingtest
#directory_id = "26a3575772694e1db96fef6d9981d16e"
#directory_id = "29091c0b38ea43be9a3927a0adf5f1cd" #Complete Practice
#directory_id = "2c011a10241844fcb54d591b278d5dc7" #HYC
#directory_id = "3b419a0e271b480e9abdeb7b6da46fac" #Practice
#directory_id = "aa54faa6b46840768311ac8b877c8d83" #Aadhifolder

#----------------HYC-----------------#
hycID = "2c011a10241844fcb54d591b278d5dc7"
#----------------NHYC-----------------#
nhycID = "2fffdc51904c4749bb148e8639b960e6"

#----------------Supporting Processes-----------------#
s2pID = 'c2c0f38f0eb14650b12c35580fb681d1' #S2P
o2cID = 'b4b7df24d34847bf935a3c960bb04e72' #o2c
p2pID = 'dbb2064d9f0547aa947f5b9447c5cec6' #p2p
r2rID = '3a47cac6b21e4fd193b3af281bcae868' #r2r
snmID = 'f4f058d866b84c59a36edb8ea1443705' #SnM
scID = '3fe14e53b2724f058542e073bd68a22f' #SC 
trsID = '2ba73b52e57a4993a1f40b4c82282596' #Trading
hcmdID = '3b419a0e271b480e9abdeb7b6da46fac' #HR
mpoID = '97eb35609b6545d48e5b972ca68002fc' #manufacturing Operations

directory_ids = [hcmdID,mpoID,r2rID,snmID,scID,trsID,s2pID,o2cID,hycID,nhycID]
#,r2rID,snmID,scID,trsID,hrID,mpoID

errors = []
modelArray = []
pdfList = []

#PDF CODE
def mergePDF(pdfList):
    pdfs = []
    for pdf in pdfList:
        pdfs.append(pdf)
        
    #pdfs = [r"C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest\export\PDF\New Folder\Reliability and Maintenance (R&M).pdf",
     #       r"C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest\export\PDF\New Folder\Order to Cash (OTC).pdf"]
    
    output = pikepdf.Pdf.new()
    
    for pdf in pdfs:
        src = pikepdf.Pdf.open(pdf)
        output.pages.extend(src.pages)
        
    output.save(r"C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest\export\PDF\New Folder\Combined.pdf")
    print("PDF merged")
def exportPDF(modelID,directoryName='New Folder'):
    
    postResponsePDF = spm.get_bpmn_pdf_post(modelID)
    print(postResponsePDF)
    #print(pdffile2)
    reqID = postResponsePDF['href'].split("/",2)[2]
    pdfName = postResponsePDF['rep']['filename']
    filePath = r"C:\Users\aasabu\Desktop\Sales and Marketing\Hierarchy Report\Spyder coding script latest\export\PDF" 
    fileExt = '.pdf'
    
    os.makedirs(filePath + '\\' + directoryName, exist_ok=True)
        
    fullPath = filePath + '\\' + directoryName + '\\' + pdfName + fileExt
    print(fullPath)
    
    pdffile = spm.get_bpmn_pdf_get(modelID,reqID)

    #print(f"file1:{pdffile}")
    #print(f"file2:{postResponsePDF['href']}")
    #print(f"file:{pdffile}")

    with open(fullPath, "wb") as f:
        f.write(pdffile)
        
    print(f"PDF generated for: {pdfName}")
    pdfList.append(fullPath)
    
    
def traverse_model_data(directory_id, level_id, hierarchy_id):
    model_count = 0
    try:
        level_id = level_id + 1
        tmp_id = ''
    
        directory_content = spm.get_directory_content(directory_id)
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
                    logger.debug(f"Current Dir:{directoryName}")
                    
                    if directoryName == 'Master Data Management' or directoryName == 'Plan to Perform (P2P)' or directoryName == 'L4 Process Flows':
                       logger.debug(f"Skipped Dir:{directoryName}")
                       continue
                   
                    directory_id = entry['href']
                    traverse_model_data(directory_id, level_id, tmp_id)
                
                #DIAGRAM DATA
                if entry['rel'] == 'mod':
                    if entry['rep']['type'] == 'Value Chain':
                        logger.debug("Value Chain skipped")
                        continue
                    model_count = model_count + 1
                    
                    e2eName = html.unescape(entry['rep']['name'])
                    e2eLink= html.unescape(entry['href'])
                    logger.debug(f"Model:{e2eName}")
                    
                    #Skip HYC Variants
                    if e2eName.startswith('PS-'):
                        print("HYC variants - skip")
                        continue
                    
                    #XML File extraction
                    #xmlFile = export_model(spm,entry['href'])
                    #print(xmlFile)
                    
                    #PDF Extraction
                    modelArray.append(entry['href'])
                    
                    #exportPDF(entry['href'])
                    
    except Exception as err:
        pass
        logger.error(tmp_id + ' ' + type(err).__name__ + traceback.format_exc())
        errors[tmp_id] = traceback.format_exc()
        

for directory_id in directory_ids:
    traverse_model_data(directory_id, level_id=0, hierarchy_id=0)
    print(f"total model ids: {len(modelArray)}")
    print("PDF Export function called...")
    exportPDF(modelArray)
    modelArray = []

mergePDF(pdfList)
 

'''
Rough work

model_json = spm.get_model_json(modelID)

pdffile = spm.get_bpmn_pdf(modelID)
print(f"file:{pdffile}")

with open("PDFExp", "wb") as f:
    f.write(pdffile)

print(type(pdffile))

#print(json.dumps(model_json,indent=2))
#with open("jsonoutput.txt", "w") as file:
 #   file.write(json.dumps(model_json,indent=2))
'''