from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips

def combineVideos():
    # Load your video clips
    clip1 = VideoFileClip("./outputs/falVideos/video0.mp4")
    clip2 = VideoFileClip("./outputs/falVideos/video1.mp4")
    clip3 = VideoFileClip("./outputs/falVideos/video2.mp4")

    # Create a 1-second black screen (same size as clips)
    gap_duration = 1  # seconds
    gap = ColorClip(size=clip1.size, color=(0, 0, 0), duration=gap_duration)

    # Create the sequence with gaps
    final_clip = concatenate_videoclips([clip1, gap, clip2, gap, clip3])

    # Write the output
    final_clip.write_videofile("./outputs/falVideos/combined_with_gaps.mp4")

if __name__ == "__main__":
    combineVideos()