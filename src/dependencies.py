from fastapi import Request
from stores.llm.templates.template_parser import TemplateParser

def get_template_parser(request: Request) -> TemplateParser:
    return request.app.state.template_parser
