# README

Label Studio JSON to OBB export

## What it does

This script converts label studio failed exports.
If you have a label studio project with videos and try to export to "YOLOv8 OBB with images", it will fail.
The "images" will just be the videos and the labels folder will have a single empty txt file per video.

### Exactly what happens

This script will:
1. Create a [VIDEOS] folder
2. Move "images" from [IMAGES] to [VIDEOS]
3. Clear [LABELS]
4. Load [JSON_FILE]
5. Process each video, frame by frame:
  - Outputs the frame as "./images/[video_name]_[frame_number:XXXXX].[FRAME_OUTPUT_TYPE]"
  - Outputs the label as "./labels/[video_name]_[frame_number:XXXXX].txt"

## How to use

You must export as YOLOv8 OBB with images, then export as JSON.
Copy the JSON into the export folder and name it [data.json] so this script can load it.

## Why

Label Studio is being a pickle.
Look at the repo - data output is an empty txt file per video from "YOLOv8 OBB with images" and a video.

IT DOES NOT EXPORT THE FRAMES AND FRAME LABELS AS IT SHOULD!

So I export JSON and put it in the folder, name it data, then put the script here and BLAM - exactly what I should start with.

Note: uses `ffmpeg` so make sure thats installed!
