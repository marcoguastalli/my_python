def duplicate_txt_file(source_file_name: str, target_file_name: str):
    with open(source_file_name, 'r') as source_file:
        file_content = source_file.readlines()

    with open(target_file_name, 'w') as target_file:
        target_file.writelines(file_content)

    pass
