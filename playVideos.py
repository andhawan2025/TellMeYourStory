import cv2
import os

def play_videos(directory):
       video_files = [f for f in os.listdir(directory) if f.endswith(('.mp4', '.avi', '.mov'))] # Add video extensions as needed
       for video_file in video_files:
           video_path = os.path.join(directory, video_file)
           cap = cv2.VideoCapture(video_path)
           if not cap.isOpened():
               print(f"Error: Could not open video {video_file}")
               continue

           while True:
               ret, frame = cap.read()
               if not ret:
                   break # End of video
               cv2.imshow('Video Player', frame)
               if cv2.waitKey(25) & 0xFF == ord('q'):
                   break # Press 'q' to stop the current video
           cap.release()
           cv2.destroyAllWindows()

def main():
    play_videos("./outputs/leonardoVideos")

if __name__ == "__main__":
    main()
