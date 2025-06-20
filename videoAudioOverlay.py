import os
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, ColorClip

def overlay_audio_on_video(video_path, audio_paths, output_file_path, output_file_name, start_time=0):
    # Create output directory if it doesn't exist
    os.makedirs(output_file_path, exist_ok=True)

    # Load the base video
    video = VideoFileClip(video_path)
    
    audio_clips = []
    
    for audio_path in audio_paths:
        audio = AudioFileClip(audio_path)
        audio = audio.with_start(start_time)
        audio_clips.append(audio)
        start_time += audio.duration

    # Create a composite audio clip
    composite_audio = CompositeAudioClip(audio_clips)
    video = video.with_audio(composite_audio)

    # Export the video
    output_file = os.path.join(output_file_path, output_file_name)
    #print(f"Exporting: {output_file}")
    video.write_videofile(output_file, codec="libx264", audio_codec="aac")

def combineVideos(videos_paths, output_file_path, output_file_name):
    # Create output directory if it doesn't exist
    os.makedirs(output_file_path, exist_ok=True)
    
    video_clips = []
    
    # Load all video clips
    for video_path in videos_paths:
        if os.path.exists(video_path):
            video = VideoFileClip(video_path)
            video_clips.append(video)
        else:
            print(f"Warning: Video file not found: {video_path}")
    
    if not video_clips:
        print("No valid video clips found to combine.")
        return
    
    # Create a 0.25-second black screen (same size as first clip)
    gap_duration = 0.25  # seconds
    gap = ColorClip(size=video_clips[0].size, color=(0, 0, 0), duration=gap_duration)
    
    # Create the sequence with gaps between videos
    final_sequence = []
    for i, video in enumerate(video_clips):
        final_sequence.append(video)
        # Add gap after each video except the last one
        if i < len(video_clips) - 1:
            final_sequence.append(gap)
    
    # Concatenate all clips
    final_clip = concatenate_videoclips(final_sequence)
    
    # Write the output
    output_file = os.path.join(output_file_path, output_file_name)
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
    
    # Clean up
    for video in video_clips:
        video.close()
    final_clip.close()

def main():
    #overlay_audio_on_video(video_path0, audio_paths0, output_file_path0, output_file_name0, 0)
    #print("Video 0 done")
    #overlay_audio_on_video(video_path1, audio_paths1, output_file_path1, output_file_name1, 2)
    #print("Video 1 done")
    #overlay_audio_on_video(video_path2, audio_paths2, output_file_path2, output_file_name2, 2)
    #print("Video 2 done")
    #overlay_audio_on_video(video_path3, audio_paths3, output_file_path3, output_file_name3, 1)
    #print("Video 3 done")
    #overlay_audio_on_video(video_path4, audio_paths4, output_file_path4, output_file_name4, 1)
    #print("Video 4 done")

    combineVideos()



if __name__ == "__main__":
    main() 