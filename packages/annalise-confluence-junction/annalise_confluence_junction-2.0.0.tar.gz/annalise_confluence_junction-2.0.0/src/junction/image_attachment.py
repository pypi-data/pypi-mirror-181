import os
from typing import Dict, List
import magic
from junction.confluence.api.content_api import ContentApi
from junction.confluence.models import Attachment

def walk_image_dir(dir:str) -> Dict[str,List[str]]:
    image_map = {}
    for (root,_,files)  in os.walk(dir, topdown=True):
        if root != dir:
            image_map[root] = files
    return image_map

def create_image_attachments(content_api:ContentApi,dir:str):
    image_dir = walk_image_dir(dir) 
    for (key,value) in image_dir.items():
        page_name = os.path.basename(key)
        results = content_api.get_page(page_name).results
        if  results:
            page_id =results[0].id
            for file in value:
                file_path = f'{key}/{file}'
                f = open(file_path, "rb")
                content = f.read()
                content_type = magic.from_file(file_path, mime=True)
                attachment = Attachment(type="attachment",fileName=file,contentType=content_type)
                content_api.create_attachment(attachment,page_id,file,content,content_type)