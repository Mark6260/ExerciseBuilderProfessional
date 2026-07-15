from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QListWidget,
    QVBoxLayout,
)


class MasterEventsListPanel(QGroupBox):
    """
    Displays the Master Events List (MEL).

    This panel is responsible only for:
    • displaying injects
    • notifying when the selected inject changes
    """

    inject_selected = Signal(int)

    def __init__(self):
        super().__init__("Master Events List")

        self.list_widget = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        self.list_widget.currentRowChanged.connect(
            self.inject_selected.emit
        )

    def set_injects(self, injects):
        """Populate the MEL."""

        self.list_widget.clear()

        for inject in injects:
            self.list_widget.addItem(str(inject))

    def clear(self):
        self.list_widget.clear()

    def current_row(self):
        return self.list_widget.currentRow()