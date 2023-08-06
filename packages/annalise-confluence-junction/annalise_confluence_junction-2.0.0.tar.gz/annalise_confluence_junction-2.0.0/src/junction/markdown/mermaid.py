import re
from traceback import print_tb
from typing import List, Any
from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from junction.mermaid_renderer import render_mermaid_svg
import asyncio

class MermaidExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        md.preprocessors.register(MermaidPreprocessor(md), "code_block", 24)


class MermaidPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        m_start = None
        m_end = None
        in_mermaid_code = False
        mermaid_diagram = []
        filename = ""
        for line in lines:
            m_start = re.match(r'`{3}mermaid\s+filename\=(.*)$',line)
            m_end = re.match(r'`{3}$',line)

            if m_start:
                filename = m_start.expand(r'\1')
                in_mermaid_code = True
            elif m_end and in_mermaid_code:
                in_mermaid_code = False
                # render mermaid image
                image_name = asyncio.run(render_mermaid_svg(filename,mermaid_diagram))
                new_lines.append(f'<p><ac:image><ri:attachment ri:filename="{image_name}"></ri:attachment></ac:image></p>')
                mermaid_diagram = []
            elif in_mermaid_code:
                mermaid_diagram.append(line)
            else:
                new_lines.append(line)

        return new_lines



def makeExtension(**kwargs: Any) -> MermaidExtension:
    return MermaidExtension(**kwargs)