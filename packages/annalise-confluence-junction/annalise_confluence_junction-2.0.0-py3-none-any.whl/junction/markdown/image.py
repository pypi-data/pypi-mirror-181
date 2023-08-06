import os
from typing import Any
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree

RE = r'<\s*img.*?src=(?:\'|\")(.*?)(?:\'|\").*?/?>'
RE_MD= r'^!\[.*?\]\((.*?)\)$'
class ImageExtension(Extension):
   def extendMarkdown(self, md):
        # Add our new MultiPattern
        md.inlinePatterns.register(ImagePattern(RE, md), 'image', 175)
        md.inlinePatterns.register(ImagePattern(RE_MD, md), 'image_confluence_md', 176)

class ImagePattern(InlineProcessor):
    def handleMatch(self, m, data):
        file_name = os.path.basename(m.group(1))
        el = etree.Element("ac:image")
        etree.SubElement(el,
            "ri:attachment",
            {
                "ri:filename":file_name
            }
        )

        return el, m.start(0), m.end(0)

def makeExtension(**kwargs: Any) -> ImageExtension:
    return ImageExtension(**kwargs)