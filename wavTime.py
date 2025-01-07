#shifts audio .wav file by specified offset time

import os
from pydub import AudioSegment

directory = "/Users/nelson/Documents/123F_audio/"

offset_minutes = 2.33
offset_ms = int(offset_minutes * 60 * 1000)

silence = AudioSegment.silent(duration=offset_ms)

def adjust(directory, append):
    day_folder = os.path.basename(directory)

    if append is None:
        append = silence
    
    if os.path.isdir(directory):
        original_files = [f for f in sorted(os.listdir(directory)) if f.endswith(".wav")]
        # Create an empty AudioSegment to store the entire day's audio
        full_day_audio = AudioSegment.empty()
        for hour_file in original_files:
            if hour_file.endswith(".wav"):
                print(hour_file)
                hour_path = os.path.join(directory, hour_file)
                hour_audio = AudioSegment.from_wav(hour_path)
                full_day_audio += hour_audio

        frame_rate = full_day_audio.frame_rate
        added = append + full_day_audio
        audio_length = len(added)
        start_point = audio_length - offset_ms
        extra_segment = added[start_point:]
        new_audio = added[:start_point]

        segment_duration_ms = 60 * 60 * 1000

        start_time = 0
        for hour_file in original_files:
            # Extract the original last 4 digits from the filename before the ".wav" extension
            #original_last_digits = hour_file.split(".wav")[0][-4:]

            # Format i to be two digits (e.g., 5 -> 05)
            #formatted_i = f"{i:02d}"
            end_time = start_time + segment_duration_ms

            segment = new_audio[start_time:end_time]
            segment = segment.set_frame_rate(frame_rate)


            # Construct the new filename
            segment_filename = hour_file

            # Export each segment back to the original folder
            segment.export(os.path.join(directory, segment_filename), format="wav", parameters=["-ar", str(frame_rate)])

            start_time = end_time

        return extra_segment

all_folders = sorted(os.listdir(directory))
first = os.path.join(directory,all_folders[1])
extra = adjust(first, None)

for day_folder in all_folders[2:]:
    day_dir = os.path.join(directory, day_folder)
    extra = adjust(day_dir, extra)