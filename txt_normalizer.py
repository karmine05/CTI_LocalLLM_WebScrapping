import re
import hashlib
from tqdm import tqdm

# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

def upload_txtfile():
    # Normalize whitespace and clean up text
    with open("XYZ.txt", "r", encoding="utf-8") as vault_file:
        text = vault_file.read()
        text = re.sub(r'\s+', ' ', text).strip()

        # Split text into chunks by sentences, respecting a maximum chunk size
        sentences = re.split(r'(?<=[.!?]) +', text)  # split on spaces following sentence-ending punctuation
        chunks = []
        current_chunk = ""
        for sentence in tqdm(sentences, desc="Splitting text into chunks"):
            # Check if the current sentence plus the current chunk exceeds the limit
            if len(current_chunk) + len(sentence) + 1 < 1000:  # +1 for the space
                current_chunk += (sentence + " ").strip()
            else:
                # When the chunk exceeds 1000 characters, store it and start a new one
                chunks.append(current_chunk)
                current_chunk = sentence + " "
        if current_chunk:  # Don't forget the last chunk!
            chunks.append(current_chunk)

        # Write each chunk to its own line
        with open("vault.txt", "w", encoding="utf-8") as vault_file:
            for chunk in tqdm(chunks, desc="Writing chunks to file"):
                vault_file.write(chunk.strip() + "\n\n")  # Two newlines to separate chunks

    # Calculate the MD5 hash of the modified vault.txt file
    md5_hash = hashlib.md5()
    with open("vault.txt", "rb") as vault_file:
        for chunk in iter(lambda: vault_file.read(4096), b""):
            md5_hash.update(chunk)
    md5_hash = md5_hash.hexdigest()

    # Save the MD5 hash to a PID file
    with open("vault.pid", "w") as pid_file:
        pid_file.write(md5_hash)

    print(NEON_GREEN + "Text file content appended to vault.txt with each chunk on a separate line. MD5 hash:" + YELLOW + md5_hash + RESET_COLOR)
    print(NEON_GREEN + "MD5 hash saved to vault.pid" + RESET_COLOR)

# Call the upload_txtfile function
upload_txtfile()