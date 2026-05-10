import os
import xml.etree.ElementTree as ET

MEDQUAD_PATH = r"E:\projects\MedQuAD"
OUTPUT_PATH = r"E:\projects\healthcare-ai-assistant\data"

# Pick a few folders to keep data manageable
SELECTED_FOLDERS = [
    "1_CancerGov_QA",
    "2_GARD_QA",
    "3_GHR_QA",
    "4_MedlineplusGov_QA",
    "6_NIDDK_QA",
]

def parse_xml_file(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        pairs = []
        for qa in root.findall(".//QAPair"):
            question = qa.findtext("Question", "").strip()
            answer = qa.findtext("Answer", "").strip()
            if question and answer:
                pairs.append(f"Q: {question}\nA: {answer}")
        return pairs
    except Exception as e:
        print(f"Skipping {filepath}: {e}")
        return []

def main():
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    total_files = 0

    for folder in SELECTED_FOLDERS:
        folder_path = os.path.join(MEDQUAD_PATH, folder)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue

        all_pairs = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".xml"):
                filepath = os.path.join(folder_path, filename)
                pairs = parse_xml_file(filepath)
                all_pairs.extend(pairs)

        if all_pairs:
            out_filename = folder.replace(" ", "_") + ".txt"
            out_filepath = os.path.join(OUTPUT_PATH, out_filename)
            with open(out_filepath, "w", encoding="utf-8") as f:
                f.write("\n\n---\n\n".join(all_pairs))
            print(f"✅ Saved {len(all_pairs)} Q&A pairs → {out_filename}")
            total_files += 1

    print(f"\n🎉 Done! {total_files} files saved to /data folder.")

if __name__ == "__main__":
    main()