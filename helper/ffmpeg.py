import os, time, asyncio, subprocess, json
from helper.utils import metadata_text


async def get_duration(file_path: str) -> int:
    """Media duration in seconds via ffprobe, 0 on any failure. Blocking call, keep off hot paths."""
    try:
        out = await asyncio.to_thread(
            subprocess.check_output,
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            timeout=15,
        )
        return int(float(out.decode().strip()))
    except Exception as e:
        print(f"Error extracting duration: {e}")
        return 0

async def change_metadata(input_file, output_file, metadata):
    author, title, video_title, audio_title, subtitle_title = await metadata_text(metadata)
    output = subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-print_format', 'json', input_file])
    data = json.loads(output)
    streams = data['streams']
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-map', '0',  # Map all streams
        '-c:v', 'copy',  # Copy video stream
        '-c:a', 'copy',  # Copy audio stream
        '-c:s', 'copy',  # Copy subtitles stream
        '-metadata', f'title={title}',
        '-metadata', f'author={author}',
    ]

    # Add title to video stream
    for stream in streams:
        if stream['codec_type'] == 'video' and video_title:
            cmd.extend([f'-metadata:s:{stream["index"]}', f'title={video_title}'])
        elif stream['codec_type'] == 'audio' and audio_title:
            cmd.extend([f'-metadata:s:{stream["index"]}', f'title={audio_title}'])
        elif stream['codec_type'] == 'subtitle' and subtitle_title:
            cmd.extend([f'-metadata:s:{stream["index"]}', f'title={subtitle_title}'])

    cmd.extend(['-metadata', f'comment=Added by @TechifyBots'])
    cmd.extend(['-f', 'matroska']) # support all format 
    cmd.append(output_file)
    print(cmd)
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print("FFmpeg Error:", e.stderr)
        return False
