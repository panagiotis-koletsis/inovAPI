import pdfplumber
from langchain_ollama.llms import OllamaLLM
import json
import re





def read_pdf(path):
    #test path "filestest/t.pdf"
    all_text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"

    return all_text

def read_json_prot(path):
    #"filestest/Suspicious_Transaction_Report_Financial_Entities.json" tested path
    with open(path, "r") as f:
        jsonfile = json.load(f)
    return jsonfile

def llm(TEMPLATE):
    llm = OllamaLLM(model="gemma3:1b")
    answer = llm.invoke(TEMPLATE)
    return answer




def extract_to_json(path_pdf,path_json):

    all_text = read_pdf(path_pdf)
    jsonfile = read_json_prot(path_json)

    TEMPLATE = f"""
    I want you to fill the following json 
    {jsonfile} 
    ---
    based on this information 
    {all_text}
    ---
    Your final answer needs to be only the json completed based on the information above and only
    """

    answer = llm(TEMPLATE)

    match = re.search(r"\{.*\}", answer, re.DOTALL)

    if match:
        json_text = match.group(0)
        try:
            data = json.loads(json_text)   # Validate JSON
            clean_json = json.dumps(data, indent=2)
            return clean_json
        except json.JSONDecodeError:
            #return "Found a JSON-like block but it's not valid JSON."
            llm_structuring = OllamaLLM(model="gemma3:1b")
            answer = llm_structuring.invoke(f"please fix the following json in order to be valid without changing any information (provide only the fixed json)---{answer}")

            match = re.search(r"\{.*\}", answer, re.DOTALL)

            if match:
                json_text = match.group(0)
                try:
                    data = json.loads(json_text)   # Validate JSON
                    clean_json = json.dumps(data, indent=2)
                    return clean_json
                except json.JSONDecodeError:
                    return "Found a JSON-like block but it's not valid JSON."
            
    else:
        return "No JSON found in the text."

