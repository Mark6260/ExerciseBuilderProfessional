from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QFormLayout,
    QGroupBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QScrollArea,
)


class InjectDetailsPanel(QGroupBox):
    """
    Displays the currently selected inject.
    """

    def __init__(self):
        super().__init__("Inject Details")

        content = QWidget()
        layout = QVBoxLayout(content)

        self.title = QLabel("No inject selected")

        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)

        self.title.setFont(title_font)
        self.title.setWordWrap(True)

        layout.addWidget(self.title)

        self.due = QLabel("Due: -")
        layout.addWidget(self.due)

        overview = QGroupBox("Overview")
        form = QFormLayout()

        self.phase = QLabel("-")
        self.category = QLabel("-")
        self.source = QLabel("-")
        self.method = QLabel("-")
        self.audience = QLabel("-")

        form.addRow("Phase:", self.phase)
        form.addRow("Category:", self.category)
        form.addRow("Source:", self.source)
        form.addRow("Method:", self.method)
        form.addRow("Audience:", self.audience)

        overview.setLayout(form)

        layout.addWidget(overview)

        self.content = self.make_section(layout, "Content", 180)
        self.expected = self.make_section(layout, "Expected Action", 120)
        self.notes = self.make_section(layout, "Facilitator Notes", 120)

        layout.addWidget(self.heading("Attachments"))

        self.attachments = QLabel("None")
        self.attachments.setWordWrap(True)
        self.attachments.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        layout.addWidget(self.attachments)
        layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)

        wrapper = QVBoxLayout()
        wrapper.addWidget(scroll)

        self.setLayout(wrapper)

    def heading(self, text):
        label = QLabel(text)

        font = QFont()
        font.setBold(True)
        font.setPointSize(11)

        label.setFont(font)

        return label

    def make_section(self, layout, heading, height):
        layout.addWidget(self.heading(heading))

        editor = QTextEdit()
        editor.setReadOnly(True)
        editor.setMinimumHeight(height)

        layout.addWidget(editor)

        return editor