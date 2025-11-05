import json
import argparse
from pathlib import Path
from fastmcp import FastMCP
from docxtpl import DocxTemplate
from pydantic import BaseModel, Field


parser = argparse.ArgumentParser(
    description="MCP server for populating docx templates with json"
)
parser.add_argument("--dir", required=True, help="Directory for templates and output")
parser.add_argument("--json-template", help="Name of json template file")
parser.add_argument("--docx-template", help="Name of docx template file")
args = parser.parse_args()
doc_dir = Path(args.dir)
json_template = (doc_dir / args.json_template).read_text()
docx_template_path = doc_dir / args.docx_template


class DocxGenerationRequest(BaseModel):
    name: str = Field(description='".docx"-suffixed output filename')
    json: str = Field(description=f"json formatted as this template: {json_template}")
    additional_instructions: str = Field(
        default="", description="Additional instructions for docx generation"
    )

mcp = FastMCP("json2docx MCP")

@mcp.tool()
def generate_docx(generation_request: DocxGenerationRequest) -> None:
    replacements = json.loads(generation_request.json)
    doc = DocxTemplate(str(docx_template_path))
    doc.render(replacements)
    doc.save(str(doc_dir / generation_request.name))


mcp.run()
