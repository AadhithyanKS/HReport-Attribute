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



#PCR CODE

def exportPCR():
    
    postResponsePDF = spm.extract_pcr_post()
    print(f"POST Resp ID:{postResponsePDF['id']}")
    #print(pdffile2)
    
    reqID = postResponsePDF['id']
    
    
    for _ in range(5):
        pcrFiles = spm.extract_pcr_get(reqID)

        if "downloadURL" in pcrFiles:
            dwnldURL = pcrFiles['downloadURL']
            
            print(f"Download URL:{pcrFiles['downloadURL']}")
            break
        time.sleep(2)   
        
    file = spm.dwnld_pcr_get(dwnldURL)
        
    #print(f"file2:{postResponsePDF['href']}")
    print(f"file:{file}")

    with open('pcr1.xlsx', "wb") as f:
        f.write(file)
        
    #print(f"PDF generated for: {pdfName}")
    #pdfList.append(fullPath)
    

exportPCR()        
