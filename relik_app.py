import os
import glob
import json
from relik import Relik

def extract_to_json(text_content, relik_model):
    if not text_content.strip():
        return None

    response = relik_model(text_content)
    
    e_names = set()
    e_types = set()
    e_rels = set()

    for span in response.spans:
        e_names.add(text_content[span.start:span.end])
        e_types.add(span.label)

    for triplet in response.triplets:
        subj = text_content[triplet.subject.start:triplet.subject.end]
        obj = text_content[triplet.object.start:triplet.object.end]
        relation = triplet.label
        e_rels.add(f"{subj} --[{relation}]--> {obj}")

    return {
        "entityTypes": list(e_types),
        "entityNames": list(e_names),
        "entityRels": list(e_rels)
    }

def logic():
    input_folder = "uploads"
    output_folder = "outputs"

    os.makedirs(output_folder, exist_ok=True)

    files_to_process = glob.glob(os.path.join(input_folder, "*.txt"))
    print("Files to process:", files_to_process)

    if not files_to_process:
        print("❌ No .txt files found in the folder.")
        return

    # Load model once
    relik_model = Relik.from_pretrained("sapienzanlp/relik-relation-extraction-nyt-large")

    print(f"\nProcessing {len(files_to_process)} file(s)...")

    for file_path in files_to_process:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        result = extract_to_json(text, relik_model)
        print(result)
        if result:
            filename_without_ext = os.path.splitext(os.path.basename(file_path))[0]
            output_file = os.path.join(output_folder, f"{filename_without_ext}_extracted.json")

            # Save result for this specific file
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            print(f"✅ Extracted data saved for '{file_path}' -> '{output_file}'")

if __name__ == "__main__":
    logic()

