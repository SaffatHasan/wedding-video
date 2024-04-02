import yaml
import json
import subprocess

def split_video(video_path, timestamps_file, output_format="%02d - %s.mp4"):
  """
  Splits a video based on timestamps defined in a YAML file using ffmpeg.

  Args:
    video_path: Path to the video file.
    timestamps_file: Path to the YAML file containing a map of timestamp: description.
    output_format: Format string for output video names (e.g., "%02d - %s.mp4").
  """
  # Load timestamps from YAML
  with open(timestamps_file, 'r') as f:
    timestamps = yaml.safe_load(f)

  # The timestamps_file is a map of time: description
  timestamps_as_list = list(timestamps)

  # Split video based on timestamps
  for i, start_time in enumerate(timestamps_as_list):
    if i < len(timestamps) - 1:
      end_time = timestamps_as_list[i+1]
    else:
      # The last entry goes from {start_time} to the end of the video.
      end_time = get_video_duration(video_path)

    # Construct output filename
    description = timestamps[start_time]
    output_filename = output_format % ((i + 1), description)

    # Split video using ffmpeg
    command = [
        "ffmpeg",
        "-i", video_path,
        "-ss", start_time,
        "-to", end_time,
        output_filename
    ]
    subprocess.run(command)

    print(f"Created clip: {output_filename}")

def get_video_duration(video_path: str):
  command = ["ffprobe", "-loglevel", "quiet", "-show_format", "-print_format", "json", video_path]
  result = subprocess.run(command, capture_output=True)
  data = json.loads(result.stdout)
  return float(data['format']['duration'])


if __name__ == "__main__":
  video_path = "wedding.mp4"
  timestamps_file = "timeline.yml"
  split_video(video_path, timestamps_file)