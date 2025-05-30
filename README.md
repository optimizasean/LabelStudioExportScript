# README

Label Studio JSON to OBB export

YOLOv8 OBB format: `[{class_id} {center_x} {center_y} {width} {height} {angle}]`

Python YOLO format: `[{class_id} {x} {y} {width} {height}]`

## What it does

This script converts label studio failed exports.
If you have a label studio project with videos and try to export to "YOLOv8 OBB with images", it will fail.
The "images" will just be the videos and the labels folder will have a single empty txt file per video.

### Exactly what happens

This script will:
1. Create a `[VIDEOS]` folder
2. Move "images" from `[IMAGES]` to `[VIDEOS]`
3. Clear `[LABELS]`
4. Load `[JSON_FILE]`
5. Process each video, frame by frame:
  - Outputs the frame as `./images/[video_name]_[frame_number:XXXXX].[FRAME_OUTPUT_TYPE]`
  - Outputs the label as `./labels/[video_name]_[frame_number:XXXXX].txt`

#### Side Note

I used to use single frame extraction, changed to multi-frame extraction (for like 10000% speedup boost).
Also removed the 5 digit extract requirement.

## How to use

You must export as YOLOv8 OBB with images, then export as JSON.
Copy the JSON into the export folder and name it `data.json` so this script can load it.

## Why

Label Studio is being a pickle.
Look at the repo - data output is an empty txt file per video from "YOLOv8 OBB with images" and a video.

IT DOES NOT EXPORT THE FRAMES AND FRAME LABELS AS IT SHOULD!

So I export JSON and put it in the folder, name it data, then put the script here and BLAM - exactly what I should start with.

Note: uses `ffmpeg` so make sure thats installed!

If you would rather have every single video frame do this: `ffmpeg -i <video.mp4> -vsync 0 <frame_%05d.png>`

The `%05d` ensures 5 digits exactly in the format `frame_00001.png` and is a counter.

You can extract from multiple input formats or save as multiple output formats as well.

## Where

Thanks to Ivan Alar Canada for a great video!

Check out the video source (couldn't upload too big) [here](https://youtu.be/LwAZZB0kj7M?si=AlFjumBdxBcEuAMo).
The video was cut to somewhere around `12:21` for about `3:14` long or so where I was processing it testing image detection and Label Studio.
