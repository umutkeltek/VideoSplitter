## Introduction

The Video Splitter application is a tool designed to help users easily split a video file into multiple smaller sections, based on the user's specified criteria. This application is built using the PyQt5 framework and utilizes the moviepy library to handle the actual video splitting process.

## Features
The Video Splitter application offers the following features:

* Input Video File Selection: Users can select a video file to be split from their local file system.
* Sections Table: Users can specify the different sections they want to split their video into using a table interface. Each section must have a title, start time, and end time specified.
* Load Sections From File: Users can load a pre-defined list of sections from a text file.
* Output Folder Selection: Users can specify the folder where the split video sections will be saved.
* Process Video: Users can initiate the video splitting process by clicking the "Process Video" button. The application will split the video based on the specified sections and save the split sections to the specified output folder.
* Progress Bar: The application features a progress bar that shows the progress of the video splitting process.

## Usage
To use the Video Splitter application, follow these steps:

1. Launch the application by running the provided Python script.
2. Select the input video file by clicking the "Browse" button next to the "Input Video" label and navigating to the desired video file.
3. Specify the sections you want to split the video into using the table interface. Click the "Add Section" button to add a new row to the table. Enter the section's title, start time, and end time in the appropriate cells.
4. (Optional) Load a pre-defined list of sections from a text file by clicking the "Load Sections From File" button and selecting the desired file.
5. Specify the folder where the split video sections should be saved by clicking the "Browse" button next to the "Output Folder" label and selecting the desired folder.
6. Click the "Process Video" button to initiate the video splitting process. The progress bar will update to show the progress of the process.

## Requirements
The Video Splitter application requires the following software and libraries to be installed:

Python 3.7 or higher
PyQt5
moviepy
To install these requirements, run the following command:

Copy code
```
pip install -r requirements.txt
```

## Limitations
* The application only supports video files in the following formats: MP4, AVI, MKV, MOV.
T* he application is not designed to handle large video files or a large number of sections. It may take some time to process and split the video depending on the size and complexity of the input file.


## License
This application is licensed under the MIT License. See the LICENSE file for more information.


