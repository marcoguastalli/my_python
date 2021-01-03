from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


def extract_metadata_from_video(source_path):
    try:
        parser = createParser(source_path)
        if not parser:
            return dict({'no parser for path: ': source_path})
        metadata = extractMetadata(parser)
        return metadata
    except Exception as err:
        print("Metadata extraction error: %s" % err)
        return None
