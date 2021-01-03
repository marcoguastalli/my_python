from hachoir.metadata import extractMetadata
from hachoir.metadata.metadata import Metadata
from hachoir.parser import createParser


def extract_metadata(path_file_name):
    result = dict({'file: ': path_file_name})
    try:
        parser = createParser(path_file_name)
        if not parser:
            result['result'] = 'Parses is None'
            return result
        metadata: Metadata = extractMetadata(parser)
        if metadata:
            result['result'] = 'ok'
            for data in sorted(metadata, key=lambda data: data.priority):
                if not data.values:
                    continue
                text = []
                for item in data.values:
                    text.append(item.text)
                result[data.key] = text
        else:
            result['result'] = 'Metadata is None'
        return result
    except Exception as err:
        print("Metadata extraction error: %s" % err)
        return None
