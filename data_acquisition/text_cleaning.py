import os
import re
import json

def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)  # Remove emojis
    text = text.replace('&amp;', '&')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_jsonl_file(file_path):
    cleaned_lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)
                if 'content' in entry:
                    entry['content'] = clean_text(entry['content'])
                if 'title' in entry:
                    entry['title'] = clean_text(entry['title'])
                cleaned_lines.append(json.dumps(entry, ensure_ascii=False))
            except Exception as e:
                cleaned_lines.append(line.strip())  # fallback: keep original
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + '\n')

if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(folder):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(folder, filename)
            print(f"Cleaning {file_path}")
            clean_jsonl_file(file_path)
    print("All .jsonl files cleaned.")
