import sys
import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QLabel, QLineEdit, \
    QFileDialog, QHBoxLayout, QVBoxLayout, QTableWidget, QHeaderView, QProgressBar, QTableWidgetItem
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex

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

        # Load sections from file button
        self.load_sections_button = QPushButton('Load Sections From File')
        self.load_sections_button.clicked.connect(self.load_sections_from_file)
        layout.addWidget(self.load_sections_button)

        layout.addLayout(QHBoxLayout())

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

        # Process video button
        self.process_button = QPushButton('Process Video')
        self.process_button.clicked.connect(self.process_video)
        layout.addWidget(self.process_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        widget.setLayout(layout)

    def add_section(self):
        row = self.sections_table.rowCount()
        self.sections_table.insertRow(row)
        self.sections_table.setItem(row, 0, QTableWidgetItem(''))
        self.sections_table.setItem(row, 1, QTableWidgetItem(''))
        self.sections_table.setItem(row, 2, QTableWidgetItem(''))

    def load_sections_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Sections File', '', 'Text Files (*.txt);;All Files (*)')
        if file_name:
            sections = self.parse_sections_file(file_name)
            self.sections_table.setRowCount(0)
            for section in sections:
                row = self.sections_table.rowCount()
                self.sections_table.insertRow(row)
                self.sections_table.setItem(row, 0, QTableWidgetItem(section['title']))
                self.sections_table.setItem(row, 1, QTableWidgetItem(self.seconds_to_time_str(section['start_time'])))
                self.sections_table.setItem(row, 2, QTableWidgetItem(self.seconds_to_time_str(section['end_time'])))

    def browse_input_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Video File', '',
                                                   'Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)')
        if file_name:
            self.input_line_edit.setText(file_name)

    def browse_output_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        if folder_name:
            self.output_line_edit.setText(folder_name)

    def parse_sections_file(self, sections_file):
        with open(sections_file, 'r') as file:
            lines = file.readlines()

        sections = []
        for line in lines:
            match = re.match(r'(\d+:\d{2}:\d{2})\s*-\s*(.+)\s*-\s*(\d+:\d{2}:\d{2})$', line.strip())
            if match:
                start_time, title, end_time = match.groups()
                sections.append({
                    'title': title.strip(),
                    'start_time': self.time_str_to_seconds(start_time),
                    'end_time': self.time_str_to_seconds(end_time)
                })

        print(sections)
        return sections

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

        split_video(input_video, output_folder, sections)

        for index, section in enumerate(sections):
            self.progress_bar.setValue((index + 1) * 100 / total_sections)

    def time_str_to_seconds(self, time_str):
        time_parts = list(map(int, time_str.split(':')))
        seconds = 0
        for part in time_parts:
            seconds = seconds * 60 + part
        return seconds

    def seconds_to_time_str(self, seconds):
        return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"


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

