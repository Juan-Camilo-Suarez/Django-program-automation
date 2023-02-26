import docx
from django.test import TestCase
import filecmp
from docx import Document
from app.models import Program
from app.services import generate_doc_file


def get_text(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return "\n".join(fullText)


class DocumentTestCase(TestCase):
    fixtures = ["initial_data.json"]

    def test_generation_file(self):
        program = Program.objects.all().first()
        a = generate_doc_file(program)

        first = get_text(a)
        second = get_text("app/tests/files_test/program_test.docx")

        self.assertEqual(first, second)
