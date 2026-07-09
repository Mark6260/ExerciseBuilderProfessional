import re
from docx import Document
from core.inject import Inject


class WordParser:
    def __init__(self, filename):
        self.filename = filename
        self.document = None

    def open(self):
        self.document = Document(self.filename)

    def get_summary(self):
        if self.document is None:
            raise RuntimeError("Document has not been opened.")

        return {
            "paragraphs": len(self.document.paragraphs),
            "tables": len(self.document.tables),
            "injects": self.count_injects(),
        }

    def count_injects(self):
        count = 0

        # Search normal paragraphs
        for paragraph in self.document.paragraphs:
            text = paragraph.text.strip()
            if re.match(r"^No\.\s+\d+", text):
                count += 1

        # Search inside tables
        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        text = paragraph.text.strip()
                        if re.match(r"^No\.\s+\d+", text):
                            count += 1

        return count
    
    def get_injects(self):
        """
        Create a simple Inject object for every inject found.
        For now we only populate the inject number.
        """

        injects = []

        number = 1

        for table in self.document.tables:
            text = table.cell(0, 0).text.strip()

            if re.match(r"^No\.\s+\d+", text):
                inject = Inject(
                    number=number,
                    title=f"Inject {number}"
                )

                injects.append(inject)
                number += 1

        return injects
