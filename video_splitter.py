import sys
import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QLabel, QLineEdit, \
    QFileDialog, QHBoxLayout, QVBoxLayout, QTableWidget, QHeaderView, QProgressBar, QTableWidgetItem
from moviepy.editor import VideoFileClip

class VideoSplitterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Splitter')
        self.setGeometry(100, 100, 800, 400)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout()

        # Input video file
        input_layout = QHBoxLayout()
        self.input_label = QLabel('Input Video:')
        self.input_line_edit = QLineEdit()
        self.input_button = QPushButton('Browse')
        self.input_button.clicked.connect(self.browse_input_video)
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_line_edit)
        input_layout.addWidget(self.input_button)

        layout.addLayout(input_layout)

        # Output folder
        output_layout = QHBoxLayout()
        self.output_label = QLabel('Output Folder:')
        self.output_line_edit = QLineEdit()
        self.output_button = QPushButton('Browse')
        self.output_button.clicked.connect(self.browse_output_folder)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_line_edit)
        output_layout.addWidget(self.output_button)

        layout.addLayout(output_layout)

        # Sections table
        self.sections_table = QTableWidget()
        self.sections_table.setColumnCount(3)
        self.sections_table.setHorizontalHeaderLabels(['Title', 'Start Time', 'End Time'])
        header = self.sections_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.sections_table)

        # Add section button
        self.add_section_button = QPushButton('Add Section')
        self.add_section_button.clicked.connect(self.add_section)
        layout.addWidget(self.add_section_button)

        # Process video button
        self.process_button = QPushButton('Process Video')
        self.process_button.clicked.connect(self.process_video)
        layout.addWidget(self.process_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        widget.setLayout(layout)

    # Add necessary functions for handling UI events

    def browse_input_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Video File', '', 'Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)')
        if file_name:
            self.input_line_edit.setText(file_name)

    def browse_output_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        if folder_name:
            self.output_line_edit.setText(folder_name)

    def add_section(self):
        row = self.sections_table.rowCount()
        self.sections_table.insertRow(row)
        self.sections_table.setItem(row, 0, QTableWidgetItem(''))
        self.sections_table.setItem(row, 1, QTableWidgetItem(''))
        self.sections_table.setItem(row, 2, QTableWidgetItem(''))

    def process_video(self):
        input_video = self.input_line_edit.text()
        output_folder = self.output_line_edit.text()

        if not input_video or not output_folder:
            return

        sections = []

        for row in range(self.sections_table.rowCount()):
            title = self.sections_table.item(row, 0).text()
            start_time = self.sections_table.item(row, 1).text()
            end_time = self.sections_table.item(row, 2).text()

            if title and start_time and end_time:
                sections.append({'title': title, 'start_time': self.time_str_to_seconds(start_time),
                                 'end_time': self.time_str_to_seconds(end_time)})
        self.progress_bar.setValue(0)
        total_sections = len(sections)
        for index, section in enumerate(sections):
            split_video(input_video, output_folder, [section])
            self.progress_bar.setValue((index + 1) * 100 / total_sections)


    def time_str_to_seconds(self, time_str):
        time_parts = list(map(int, time_str.split(':')))
        seconds = 0
        for part in time_parts:
            seconds = seconds * 60 + part
        return seconds




    


def split_video(input_video, output_folder, sections):
    video = VideoFileClip(input_video)

    for section in sections:
        start_time, end_time = section['start_time'], section['end_time']
        clip = video.subclip(start_time, end_time)
        output_path = f"{output_folder}/{section['title']}.mp4"
        clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    video.close()


def main():
    app = QApplication(sys.argv)
    window = VideoSplitterWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
