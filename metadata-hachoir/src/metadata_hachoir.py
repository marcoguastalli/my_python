from hachoir.parser import createParser


def extract_metadata_from_video(source_path):
    parser = createParser(source_path)
    if not parser:
        return None
    result = dict({'path': source_path, 'mime_type': str(parser.mime_type)})
    return result
