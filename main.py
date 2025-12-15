import json
from fastapi import FastAPI, UploadFile, File
import os
from relik_app import logic

from extractjsonform import extract_to_json

app = FastAPI()

UPLOAD_FOLDER = "uploads"

# Create folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     file_location = os.path.join(UPLOAD_FOLDER, file.filename)

#     with open(file_location, "wb") as buffer:
#         buffer.write(await file.read())

#     return {"filename": file.filename, "saved_to": file_location}

from typing import List
@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    saved_files = []

    for file in files:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        saved_files.append(file.filename)

    return {"uploaded_files": saved_files}

# @app.get("/getResults")
# def get_results():
#     # Example: return all file names currently in uploads folder
#     files = os.listdir(UPLOAD_FOLDER)
#     print("Files in upload folder:", files)
#     # relik_model = initialize()



#     # text_content = "test.txt"

    
#     # results = extract_to_json(text_content=text_content,relik_model=relik_model) 
#     logic()

#     outputs_folder = "outputs"
#     json_files = [f for f in os.listdir(outputs_folder) if f.endswith('.json')]
    
#     results = {}
#     for json_file in json_files:
#         file_path = os.path.join(outputs_folder, json_file)
#         with open(file_path, 'r') as f:
#             # Use filename (without .json) as key
#             key = json_file.replace('.json', '')
#             results[key] = json.load(f)
    
#     return results


# @app.get("/getResults")
# def get_results():
#     data = []
#     files = os.listdir(UPLOAD_FOLDER)
#     path_json = "json_structure/Suspicious_Transaction_Report_Financial_Entities.json"

    
    
#     for i in range(len(files)):
#         path_pdf = f"{UPLOAD_FOLDER}/{files[i]}" 

#         cleaned_json = extract_to_json(path_pdf=path_pdf,path_json=path_json)
#         data.append({"name": files[i], "cleaned": cleaned_json})

    
#     return data
@app.get("/getResults")
def get_results():
    try:
        data = []
        files = os.listdir(UPLOAD_FOLDER)
        
        # Filter only files (not directories)
        files = [f for f in files if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        
        if not files:
            return {"message": "No files found in upload folder", "data": []}
        
        path_json = "json_structure/Suspicious_Transaction_Report_Financial_Entities.json"
        
        for file in files:
            path_pdf = os.path.join(UPLOAD_FOLDER, file)
            
            try:
                cleaned_json = extract_to_json(path_pdf=path_pdf, path_json=path_json)
                data.append({"name": file, "cleaned": json.loads(cleaned_json)})
            except Exception as e:
                data.append({"name": file, "error": str(e)})
        
        return {"data": data}
    except Exception as e:
        return {"error": str(e), "message": "Failed to process files"}


@app.get("/getAllRelationTypes")
def get_all_relation_types():
    return {
        "relationTypes": ["rel1","rel2"]
    }

@app.get("/getAllEntityTypes")
def get_all_entity_types():
    return {
        "entityTypes": ["Reporting Entity","Individual Participants","Corporate Participant","Account / Insurance Policy Identification","Transaction Description"]
    }