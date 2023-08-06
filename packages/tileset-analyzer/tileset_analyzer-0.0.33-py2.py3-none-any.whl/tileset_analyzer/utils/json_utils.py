
import json
import io


def write_json_file(content: str, file_path: str):
    with io.open(file_path, 'w', encoding='utf8') as outfile:
        outfile.write(content)

'''
Reference: 
https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
'''
