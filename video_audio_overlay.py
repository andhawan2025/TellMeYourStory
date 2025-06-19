import os
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, ColorClip

video_path0 = "./outputs/falVideos/video0.mp4"
audio_paths0 = ["./outputs/elevenlabsAudio/scene0_1.mp3", "./outputs/elevenlabsAudio/scene0_2.mp3"]
output_file_path0 = "./outputs/video_with_audio"
output_file_name0 = "combined_video0.mp4"

video_path1 = "./outputs/falVideos/video1.mp4"
audio_paths1 = ["./outputs/elevenlabsAudio/scene1_1.mp3"]
output_file_path1 = "./outputs/video_with_audio"
output_file_name1 = "combined_video1.mp4"

video_path2 = "./outputs/falVideos/video2.mp4"
audio_paths2 = ["./outputs/elevenlabsAudio/scene2_1.mp3"]
output_file_path2 = "./outputs/video_with_audio"
output_file_name2 = "combined_video2.mp4"

video_path3 = "./outputs/falVideos/video3.mp4"
audio_paths3 = ["./outputs/elevenlabsAudio/scene3_1.mp3", "./outputs/elevenlabsAudio/scene3_2.mp3"]
output_file_path3 = "./outputs/video_with_audio"
output_file_name3 = "combined_video3.mp4"

video_path4 = "./outputs/falVideos/video4.mp4"
audio_paths4 = ["./outputs/elevenlabsAudio/scene4_1.mp3", "./outputs/elevenlabsAudio/scene4_2.mp3"]
output_file_path4 = "./outputs/video_with_audio"
output_file_name4 = "combined_video4.mp4"

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

def combineVideos():
    video0 = VideoFileClip("./outputs/video_with_audio/combined_video0.mp4")
    video1 = VideoFileClip("./outputs/video_with_audio/combined_video1.mp4")
    video2 = VideoFileClip("./outputs/video_with_audio/combined_video2.mp4")
    video3 = VideoFileClip("./outputs/video_with_audio/combined_video3.mp4")
    video4 = VideoFileClip("./outputs/video_with_audio/combined_video4.mp4")

    # Create a 1-second black screen (same size as clips)
    gap_duration = 0.25  # seconds
    gap = ColorClip(size=video0.size, color=(0, 0, 0), duration=gap_duration)

    # Create the sequence with gaps
    final_clip = concatenate_videoclips([video0, gap, video1, gap, video2, gap, video3, gap, video4])

    # Write the output
    final_clip.write_videofile("./outputs/video_with_audio/combined_with_gaps.mp4")


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