import os
import re
from typing import List
import uuid
from pyppeteer import executablePath, launch
import cairosvg

HTML = ['<!DOCTYPE html>',
'<html lang="en">',
'<head>',
'<meta charset="utf-8">',
'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css">',
'</head>',
'<body>',
'<div class="mermaid">',
'MERMAID',
'</div>',
'<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>',
'<script>mermaid.initialize({startOnLoad:true});</script>',
'</body>',
'</html>']

async def render_mermaid_svg(file_name:str,diagram:List[str])->str:
    diagram_content = '\n'.join(diagram)
    html = re.sub(r'MERMAID', diagram_content, ''.join(HTML))
    browser = await launch(executablePath='/usr/bin/chromium',args=['--no-sandbox'])
    page = await browser.newPage()
    diagram_name = f'{uuid.uuid4()}.png'
    await page.setContent(html)
    await page.waitForSelector('svg')
    svg =  await page.evaluate("() => document.querySelector('svg').outerHTML")
    os.makedirs(f'mermaid/{file_name}', exist_ok=True)
    cairosvg.svg2png(bytes(svg,'utf-8'),write_to=f'mermaid/{file_name}/{diagram_name}')
    await browser.close()
    return diagram_name