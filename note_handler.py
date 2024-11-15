class NoteHandler:
    def __init__(self, tab1_instance):
        self.tab1 = tab1_instance  # Store the Tab1 instance in a shorthand variable

    def midi_handling(self, message):
        if message.type == "note_on":
            print('Received note_on')  # Debugging print
            # Check if the note is in required_notes
            if message.note in self.tab1.required_notes:
                # Emit the signal with the note and color (green)
                print('Note in required notes, emitting green')  # Debugging print
                self.tab1.note_on_signal.emit(message.note, "green")
            else:
                # Emit the signal with the note and color (red)
                print('Note not in required notes, emitting red')  # Debugging print
                self.tab1.note_on_signal.emit(message.note, "red")

        elif message.type == "note_off":
            print('Received note_off')  # Debugging print
            # Emit the signal to remove the note from the display
            self.tab1.note_off_signal.emit(message.note)  # Emit the note_off signal
