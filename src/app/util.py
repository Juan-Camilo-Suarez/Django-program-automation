import tempfile
from django.template.loader import get_template
from htmldocx import HtmlToDocx


def render_to_word(template_src, context_dict={}):
    new_parser = HtmlToDocx()
    template = get_template(template_src)
    html = template.render(context_dict)
    # print(html)
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        docx = new_parser.parse_html_string(html)
        print(type(docx))
        docx.save(tmp)
        return tmp.name
