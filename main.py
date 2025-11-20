import json
from fastapi import FastAPI, UploadFile, File
import os
from relik_app import logic

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

@app.get("/getResults")
def get_results():
    # Example: return all file names currently in uploads folder
    files = os.listdir(UPLOAD_FOLDER)
    print("Files in upload folder:", files)
    # relik_model = initialize()



    # text_content = "test.txt"

    
    # results = extract_to_json(text_content=text_content,relik_model=relik_model) 
    logic()

    outputs_folder = "outputs"
    json_files = [f for f in os.listdir(outputs_folder) if f.endswith('.json')]
    
    results = {}
    for json_file in json_files:
        file_path = os.path.join(outputs_folder, json_file)
        with open(file_path, 'r') as f:
            # Use filename (without .json) as key
            key = json_file.replace('.json', '')
            results[key] = json.load(f)
    
    return results



@app.get("/getAllRelationTypes")
def get_all_relation_types():
    return {
        "relationTypes": ["rel1","rel2"]
    }

@app.get("/getAllEntityTypes")
def get_all_entity_types():
    return {
        "entityTypes": ["ent1","ent2"]
    }