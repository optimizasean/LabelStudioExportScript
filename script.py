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

# DIRECTORIES FOR THINGS
VIDEOS = './videos'
IMAGES = './images'
LABELS = './labels'

# Still frame output type
FRAME_OUTPUT_TYPE = 'png'

# Make video folder
Path(VIDEOS).mkdir(parents = False, exist_ok = True)
# Move files (videos) from images to videos
[f.rename(Path(f"{VIDEOS}/{f.name}")) for f in Path(IMAGES).iterdir() if f.is_file()]
# Clear labels folder of all files
[f.unlink() for f in Path(LABELS).iterdir() if f.is_file()]

# Read JSON
data = None
with open(JSON_FILE) as f: data = json.load(f)

#    $                 X            X                       $
#data[0]['annotations'][0]['result'][0]['value']['sequence'][0].keys()
#dict_keys(['frame', 'enabled', 'rotation', 'x', 'y', 'width', 'height', 'time'])

# Process each video
for video_data in data:
    # Locate video and get video name
    video = Path(f"{VIDEOS}/{video_data['file_upload']}")

    # Get video name
    video_name = video.stem

    # MAYBE CHECK RESULT_COUNT - it might be more than 1?????
    # Process each frame
    for frame_data in video_data['annotations'][0]['result'][0]['value']['sequence']:
        # Get frame number we are processing
        frame_number = frame_data['frame']
        
        # FFMPEG do the thing
        process = subprocess.run(
                f"ffmpeg -i {str(video)} -vf \"select=eq(n\,{frame_number})\" -vsync 0 -frames:v 1 {IMAGES}/{video_name}_{frame_number:05d}.{FRAME_OUTPUT_TYPE}",
                shell = True
        )

        # Convert and save frame txt file in OBB format: [class_id x_center y_center width height angle]
        class_id = 'Drone'
        width = frame_data['width']
        height = frame_data['height']
        Path(f"{LABELS}/{video_name}_{frame_number:05d}.txt").write_text(
                f"{class_id} {frame_data['x'] + width / 2} {frame_data['y'] + height / 2} {width} {height} {frame_data['rotation']}"
        )