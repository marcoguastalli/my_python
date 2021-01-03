from hachoir.metadata import extractMetadata
from hachoir.metadata.metadata import Metadata
from hachoir.parser import createParser


def extract_metadata_from_video(source_path):
    result = dict({'path: ': source_path})
    try:
        parser = createParser(source_path)
        if not parser:
            result['result'] = 'Parses is None'
            return result
        metadata: Metadata = extractMetadata(parser)
        if metadata:
            for data in sorted(metadata, key=lambda data: data.priority):
                if not data.values:
                    continue
                text = []
                for item in data.values:
                    text.append(item.text)
                result[data.key] = text
        return result
    except Exception as err:
        print("Metadata extraction error: %s" % err)
        return None
