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
        Extract basic inject information from the Master Events List table.
        """

        injects = []

        if not self.document.tables:
            return injects

        mel_table = self.document.tables[0]

        for row in mel_table.rows[1:]:
            cells = row.cells

            if len(cells) < 5:
                continue

            number_text = cells[0].text.strip()

            if not number_text.isdigit():
                continue

            inject = Inject(
                number=int(number_text),
                exercise_time=cells[1].text.strip(),
                phase=cells[2].text.strip(),
                title=cells[3].text.strip(),
                category=cells[4].text.strip(),
            )

            injects.append(inject)

        return injects