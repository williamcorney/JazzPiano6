from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QAbstractItemView
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt, pyqtSignal
from theory import get_theory  # Import the get_theory function
from note_handler import NoteHandler  # Import the NoteHandler class
import pickle

class Tab1(QWidget):
    note_on_signal = pyqtSignal(int, str)  # Define the signal
    note_off_signal = pyqtSignal(int)  # Define the signal for note_off

    def __init__(self, parent_widget):
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        self.common_variables()
        self.init_ui()
        self.load_data()
        self.theory1.clicked.connect(self.theory1_clicked)
        self.theory2.clicked.connect(self.theory2_clicked)
        self.theory3.clicked.connect(self.theory3_clicked)
        self.go_button.clicked.connect(self.trigger_get_theory)

        self.note_on_signal.connect(self.insert_note)
        self.note_off_signal.connect(self.delete_note)  # Connect note_off_signal to delete_note

    def load_data(self):
        """Load the data from the theory.pkl file."""
        try:
            with open('theory.pkl', 'rb') as file:
                self.Theory = pickle.load(file)
                print(self.Theory['Theory'])  # Print the loaded data for debugging
        except FileNotFoundError:
            print("theory.pkl not found.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def common_variables(self):
        """Initialize all common variables."""
        self.label = QLabel("Waiting for MIDI input...")
        self.required_notes = []  # Initialize required_notes as an empty list
        self.note_handler = NoteHandler(self)  # Pass the Tab1 instance to NoteHandler
        self.theorymode = None  # Initialize theorymode as None (or False)
        self.labels, self.pixmap_item, self.Theory = {}, {}, {"Stats": {}}
        self.required_notes, self.pressed_notes = [], []
        self.score, self.number, self.lastnote, self.index = 0, 0, 0, 0
        self.previous_scale, self.correct_answer, self.correct_key = None, None, None
        self.theory1, self.theory2, self.theory3 = QListWidget(), QListWidget(), QListWidget()

    def init_ui(self):
        """Initialize the user interface."""
        self.setLayout(QVBoxLayout())
        self.horizontal = QHBoxLayout()
        self.layout().addLayout(self.horizontal)
        for theory in [self.theory1, self.theory2, self.theory3]: self.horizontal.addWidget(theory, stretch=1)
        self.theory1.addItems(["Notes", "Scales", "Triads", "Sevenths", "Modes", "Shells"])
        self.theory2.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.Scene = QGraphicsScene()
        self.BackgroundPixmap = QPixmap("./Images/Piano/keys.png")
        self.BackgroundItem = QGraphicsPixmapItem(self.BackgroundPixmap)
        self.Scene.addItem(self.BackgroundItem)
        self.View = QGraphicsView(self.Scene)
        self.View.setFixedSize(self.BackgroundPixmap.size())
        self.View.setSceneRect(0, 0, self.BackgroundPixmap.width(), self.BackgroundPixmap.height())
        self.View.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.View.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout().addWidget(self.View)
        self.horizontal_vertical = QVBoxLayout()
        self.horizontal.addLayout(self.horizontal_vertical, 2)
        self.init_labels()
        self.go_button = QPushButton("Go")
        self.horizontal_vertical.addWidget(self.go_button)

    def init_labels(self):
        """Initialize the labels."""
        for key in ['key_label', 'inversion_label', 'fingering_label', 'score_value']:
            label = QLabel("")
            if key == 'key_label':
                label.setFont(QFont("Arial", 32))
            self.labels[key] = label
            self.horizontal_vertical.addWidget(label)

    def insert_note(self, note, color):
        """Insert a note on the piano with the specified color."""
        print ('test3')
        self.xcord = self.Theory["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.pixmap_item[note] = QGraphicsPixmapItem(QPixmap(f"./Images/Piano/key_{color}{self.Theory['NoteFilenames'][note % 12]}"))
        self.pixmap_item[note].setPos(self.xcord, 0)
        current_scene = self.pixmap_item[note].scene()
        if current_scene:
            current_scene.removeItem(self.pixmap_item[note])
        self.Scene.addItem(self.pixmap_item[note])

    def delete_note(self, note):
        """Delete a note from the piano."""
        if note in self.pixmap_item:
            if self.pixmap_item[note].scene():
                self.pixmap_item[note].scene().removeItem(self.pixmap_item[note])
            del self.pixmap_item[note]

    def theory1_clicked(self):
        """Handle click on theory1 list."""
        self.labels['score_value'].setText("")
        self.labels['fingering_label'].clear()
        self.labels['key_label'].setText("")
        self.Theory['Stats'] = {}
        self.theory2.clear()
        self.theory3.clear()
        self.theorymode = self.theory1.selectedItems()[0].text()
        theory_items = {
            "Notes": ["Naturals", "Sharps", "Flats"],
            "Scales": ["Major", "Minor", "Harmonic Minor", "Melodic Minor"],
            "Triads": ["Major", "Minor"],
            "Sevenths": ["Maj7", "Min7", "7", "Dim7", "m7f5"],
            "Modes": ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"],
            "Shells": ["Major", "Minor", "Dominant"]
        }

        if self.theorymode in theory_items:
            self.theory2.addItems(theory_items[self.theorymode])

    def theory2_clicked(self):
        """Handle click on theory2 list."""
        self.Theory['Stats'] = {}
        self.theory3.clear()
        self.theory2list = [item.text() for item in self.theory2.selectedItems()]

        theory3_items = {
            "Notes": [],
            "Scales": ["Right", "Left"],
            "Triads": ["Root", "First", "Second"],
            "Sevenths": ["Root", "First", "Second", "Third"],
            "Modes": [],
            "Shells": ["3/7", "7/3"]
        }

        if self.theorymode in theory3_items:
            self.theory3.addItems(theory3_items[self.theorymode])

    def theory3_clicked(self):
        """Handle click on theory3 list."""
        modes_requiring_list = {"Notes", "Scales", "Triads", "Sevenths", "Shells"}
        if self.theorymode in modes_requiring_list:
            self.theory3list = [item.text() for item in self.theory3.selectedItems()]

    def trigger_get_theory(self):
        """Trigger the get_theory function when 'Go' button is clicked."""
        get_theory(self)

    def midi_handling(self, message):
        """Handle incoming MIDI messages."""
        self.note_handler.midi_handling(message)
