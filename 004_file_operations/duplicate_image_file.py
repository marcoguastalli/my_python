def duplicate_image_file(source_file_name: str, target_file_name: str):
    with open(source_file_name, 'rb') as source_file:
        file_content = source_file.read()

    with open(target_file_name, 'wb') as target_file:
        target_file.write(file_content)

    pass
