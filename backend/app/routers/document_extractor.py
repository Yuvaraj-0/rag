from app.services.document_extractor import extract_text

# 4. Save file locally
with open(file_path, "wb") as buffer:
    shutil.copyfileobj(
        file.file,
        buffer
    )


# 5. Extract text
extracted_text = extract_text(
    file_path,
    file.filename     
)

print(extracted_text[:1000])


# 6. Get file size
file_size = os.path.getsize(file_path)