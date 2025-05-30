"""
Label Studio JSON to OBB export

This script converts label studio failed exports.
If you have a label studio project with videos and try to export to YOLOv8 OBB with images, it will fail.
The "images" will just be the videos and the labels folder will have a single empty txt file per video.

You must export as YOLOv8 OBB with images, then export as JSON.
Copy the JSON into the export folder and name it [data.json] so this script can load it.

This script will:
1. Create a [VIDEOS] folder
2. Move "images" from [IMAGES] to [VIDEOS]
3. Clear [LABELS]
4. Load [JSON_FILE]
5. Process each video, frame by frame:
  - Outputs the frame as "./images/[video_name]_[frame_number:XXXXX].[FRAME_OUTPUT_TYPE]"
  - Outputs the label as "./labels/[video_name]_[frame_number:XXXXX].txt"
"""

# Import libraries necessary
import subprocess
from pathlib import Path
import json

# FILE TO READ JSON EXPORT
JSON_FILE = 'data.json'
CLASSES_FILE = 'classes.json'

# DIRECTORIES FOR THINGS
VIDEOS = './videos'
IMAGES = './images'
LABELS = './labels'

# Still frame output type - jpg is best performance but png and others are supported
FRAME_OUTPUT_TYPE = 'jpg'

# Make video folder
Path(VIDEOS).mkdir(parents = False, exist_ok = True)
# Move files (videos) from images to videos
[f.rename(Path(f"{VIDEOS}/{f.name}")) for f in Path(IMAGES).iterdir() if f.is_file()]
# Clear labels folder of all files
[f.unlink() for f in Path(LABELS).iterdir() if f.is_file()]

# Read JSON
data = None
with open(JSON_FILE) as f: data = json.load(f)

# Function to export frames with ffmpeg
def export_frames(video, video_name, frame_numbers):
    # FFMPEG do the thing
    select_indexes = '+'.join([f"eq(n\\,{number})" for number in frame_numbers])
    process = subprocess.run(
        f"ffmpeg -i {str(video)} -vf \"select='{select_indexes}'\" -vsync 0 -frame_pts true {IMAGES}/{video_name}_%d.{FRAME_OUTPUT_TYPE}",
        shell = True
    )

# Process each video
labels = []
for video_data in data:
    # Locate video and get video name
    video = Path(f"{VIDEOS}/{video_data['file_upload']}")

    # Get video name
    video_name = video.stem

    # MAYBE CHECK RESULT_COUNT - it might be more than 1?????
    # Process each frame, maintain frame number list for video export
    frame_numbers = set()
    for result in video_data['annotations'][0]['result']:
        if len(result['value']['labels']) > 1: raise Exception("DANG: MULTILABEL")
        label = result['value']['labels'][0]
        if label not in labels: labels.append(label)
        label_number = labels.index(label)

        # Go through frame sequence for one result
        for sequence in result['value']['sequence']:
            # Get frame number we are processing
            frame_number = sequence['frame']
            frame_numbers.add(frame_number)

            # Convert and save frame txt file in OBB format: [class_id x_center y_center width height angle]
            width = sequence['width']
            height = sequence['height']
            
            # Write labels (append if file exists for that frame)
            file = Path(f"{LABELS}/{video_name}_{frame_number}.txt")
            with file.open('a') as f:
                f.write(
                    # Python YOLO package does not use rotation
                    #f"{label_number} {sequence['x'] + width / 2} {sequence['y'] + height / 2} {width} {height} {sequence['rotation']}"
                    f"{label_number} {x} {y} {width} {height}"
                )

    # Export video frames
    export_frames(video, video_name, frame_numbers)

# Create classes.json
with open(Path(CLASSES_FILE), 'w') as file: json.dump({label: labels.index(label) for label in labels}, file, indent=4)
