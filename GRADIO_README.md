# 🎬 Tell Me Your Story - Gradio Interface

A beautiful web interface for exploring visual narratives with pre-generated screenplays, images, and videos!

## 🚀 Features

- **4-Frame Progressive Interface**: 
  1. **Story Input**: Enter your story prompt (max 5 sentences)
  2. **Screenplay Display**: View and review loaded screenplays
  3. **Image Gallery**: See 3 scene images from local files
  4. **Video Player**: Watch the corresponding video

- **Local File Integration**:
  - No API keys required
  - All content loaded from local files
  - Fast and offline operation

## 📋 Prerequisites

### Required Files
Make sure you have the following files in your project:

**Screenplay Files** (in `outputs/` directory):
- `screenplay.txt`
- `screenplay1.txt`
- `screenplay2.txt`
- `screenplay3.txt`
- `screenplay4.txt`
- `screenplay5.txt`

**Image Files** (in `outputs/openAIImages/` directory):
- `image0.png`
- `image1.png`
- `image2.png`

**Video Files** (in `outputs/falVideos/` directory):
- `video0.mp4`

### Python Dependencies
Install the required packages:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install gradio
```

## 🏃‍♂️ Running the Application

### Option 1: Using the Run Script
```bash
python run_gradio.py
```

### Option 2: Direct Execution
```bash
python gradio_app.py
```

The application will start on `http://localhost:7860`

## 📖 How to Use

### Step 1: Enter Your Story
1. Navigate to **Frame 1: Your Story**
2. Enter your story prompt in the text box (maximum 5 sentences)
3. Click "📖 Load Screenplay"
4. A screenplay will be randomly selected and loaded from available files

### Step 2: Load Images
1. Review the loaded screenplay in **Frame 2**
2. Click "🖼️ Load Images"
3. 3 scene images will be loaded and displayed in **Frame 3**

### Step 3: Load Video
1. View the loaded images in **Frame 3**
2. Click "🎥 Load Video"
3. The corresponding video will be loaded and displayed in **Frame 4**

## 📁 Local Files

Content is loaded from the following directories:

- **Screenplays**: `./outputs/screenplay*.txt` (multiple files available)
- **Images**: `./outputs/openAIImages/image0.png`, `image1.png`, `image2.png`
- **Videos**: `./outputs/falVideos/video0.mp4`

## 🛠️ Features & Validation

- **Input Validation**: Automatically checks that story prompts don't exceed 5 sentences
- **Local File Loading**: All content loaded from existing local files
- **Error Handling**: Clear error messages for missing files or common issues
- **Progress Tracking**: Status updates for each loading step
- **Random Selection**: Screenplays are randomly selected from available files

## 🎨 Interface Design

The interface uses Gradio's modern Soft theme and includes:

- **Intuitive 4-frame layout** following the natural workflow
- **Clear visual hierarchy** with emojis and section headers
- **Responsive design** that works on different screen sizes
- **Interactive elements** with appropriate button styling
- **Helpful instructions** and status messages

## 🔧 Troubleshooting

### Common Issues

1. **"No screenplay files found" error**
   - Make sure you have screenplay files in the `./outputs/` directory
   - Check that files are named `screenplay.txt`, `screenplay1.txt`, etc.

2. **"No image files found" error**
   - Verify that image files exist in `./outputs/openAIImages/`
   - Check that files are named `image0.png`, `image1.png`, `image2.png`

3. **"Video file not found" error**
   - Make sure `video0.mp4` exists in `./outputs/falVideos/`
   - Check file permissions and accessibility

4. **Empty content displayed**
   - Verify file contents are not corrupted
   - Check file encoding (should be UTF-8 for text files)

### Getting Help

If you encounter issues:

1. Check the status messages in each frame
2. Look at the console output for detailed error messages
3. Verify all required files exist in the correct directories
4. Ensure file permissions allow reading

## 🎯 Tips for Best Results

1. **Story Prompts**: 
   - Be specific but concise
   - Include character names and key plot points
   - Describe the setting and mood
   - The prompt helps select which screenplay to load

2. **File Organization**:
   - Keep files organized in the specified directory structure
   - Use consistent naming conventions

3. **Performance**:
   - Loading is instant since files are local
   - No internet connection required
   - Works offline once files are available

Enjoy creating your visual stories! 🎬✨ 