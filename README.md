# Shadow English - Sentence by Sentence Practice Tool

A web-based application for practicing English speaking using the shadowing technique. The tool uses OpenAI's Whisper AI to transcribe audio files and display sentences with individual play buttons for focused practice.

## Features

- 🎵 **Audio Upload**: Support for MP3, WAV, MP4, M4A, OGG, FLAC, and WebM formats
- 🤖 **AI Transcription**: Automatic transcription using OpenAI's Whisper model
- 📝 **Optional Script**: Provide your own script file (TXT) or let Whisper generate one
- ▶️ **Sentence-by-Sentence Playback**: Individual play button for each sentence
- 🔁 **Loop Mode**: Loop a single sentence for repeated practice
- 🎚️ **Speed Control**: Adjust playback speed (0.5x to 1.5x)
- ✏️ **Editable**: Edit sentences and timestamps as needed
- 🎨 **Modern UI**: Clean, dark-themed interface optimized for learning

---

## 🚀 Quick Start Guide (Run Locally)

### Step 1: Install Prerequisites

#### Install Python 3.8 or higher

1. Download from https://www.python.org/downloads/
2. During installation, **check "Add Python to PATH"**
3. Verify installation:
   ```powershell
   python --version
   ```

#### Install FFmpeg (Required for audio processing)

**Option A - Using winget (Recommended for Windows 10/11):**

```powershell
winget install Gyan.FFmpeg
```

**Option B - Manual Installation:**

1. Download from https://www.gyan.dev/ffmpeg/builds/ (get "ffmpeg-release-full.7z")
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH:
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Go to **Advanced** → **Environment Variables**
   - Under "User variables", select **Path** → **Edit** → **New**
   - Add: `C:\ffmpeg\bin`
   - Click OK on all dialogs
4. **Restart your terminal** and verify:
   ```powershell
   ffmpeg -version
   ```

#### Install Git (if not already installed)

```powershell
winget install Git.Git
```

---

### Step 2: Clone the Repository

Open PowerShell and run:

```powershell
# Navigate to where you want to store the project
cd D:\Personal\Shadow

# Clone the repository (replace with your GitHub URL)
git clone https://github.com/YOUR_USERNAME/shadow-english.git

# Enter the project folder
cd shadow-english
```

---

### Step 3: Set Up Python Environment

```powershell
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# If you get an execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate

# You should see (venv) at the start of your prompt
```

---

### Step 4: Install Dependencies

```powershell
# Install all required packages (this may take 5-10 minutes)
pip install -r requirements.txt
```

---

### Step 5: Run the Application

```powershell
# Make sure FFmpeg is in PATH (if installed via winget, you may need to add it)
# Find FFmpeg location:
Get-ChildItem -Path "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter "ffmpeg.exe" -Recurse | Select-Object -First 1

# Add FFmpeg to PATH for this session (adjust path if different):
$env:PATH += ";$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"

# Set Whisper model (optional - use 'base' for better accuracy, 'tiny' for speed)
$env:WHISPER_MODEL = "base"

# Start the application
python app.py
```

---

### Step 6: Open in Browser

1. Open your web browser
2. Go to: **http://localhost:5000**
3. Upload an audio file and start practicing!

---

## 📋 Complete Command Summary (Copy-Paste Ready)

Run these commands in order in PowerShell:

```powershell
# ONE-TIME SETUP
# ==============

# 1. Install FFmpeg
winget install Gyan.FFmpeg

# 2. Clone repository
cd D:\Personal\Shadow
git clone https://github.com/YOUR_USERNAME/shadow-english.git
cd shadow-english

# 3. Create and activate virtual environment
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt


# EVERY TIME YOU WANT TO RUN
# ==========================

# 1. Open PowerShell and navigate to project
cd D:\Personal\Shadow\shadow-english

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Add FFmpeg to PATH (adjust path if your version is different)
$env:PATH += ";$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"

# 4. Run the app
python app.py

# 5. Open browser to http://localhost:5000
```

---

## 🔧 Troubleshooting

### "ffmpeg is not recognized"

FFmpeg is not in your PATH. Either:

- Restart your terminal after installing FFmpeg
- Manually add FFmpeg to PATH (see Step 1)
- Use the `$env:PATH +=` command shown above

### "execution policy" error when activating venv

Run this command first:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Transcription is slow

- The first transcription downloads the Whisper model (~74MB for base)
- Use `tiny` model for faster (but less accurate) results:
  ```powershell
  $env:WHISPER_MODEL = "tiny"
  python app.py
  ```

### Text not visible in edit boxes

Make sure you're using the latest version. Pull updates:

```powershell
git pull origin main
```

---

## Script File Format

If you have the transcript, create a TXT file with one sentence per line:

```
Hello, welcome to today's lesson.
We're going to learn about English pronunciation.
Let's start with the basics.
```

## Whisper Model Options

Set the model using environment variable before running:

```powershell
$env:WHISPER_MODEL = "base"  # or tiny, small, medium, large
python app.py
```

| Model  | Size    | Speed   | Accuracy |
| ------ | ------- | ------- | -------- |
| tiny   | 39 MB   | Fastest | Lower    |
| base   | 74 MB   | Fast    | Good     |
| small  | 244 MB  | Medium  | Better   |
| medium | 769 MB  | Slow    | High     |
| large  | 1550 MB | Slowest | Highest  |

## Tips for Shadowing Practice

1. **Listen First**: Play the sentence once without speaking
2. **Shadow**: Play again and speak along with the audio
3. **Loop**: Use the loop feature for difficult sentences
4. **Slow Down**: Use 0.75x or 0.5x speed for challenging phrases
5. **Repeat**: Practice each sentence until it feels natural

## Troubleshooting

### "FFmpeg not found" error

Make sure FFmpeg is installed and added to your system PATH.

### Model download is slow

The first run will download the Whisper model. This is normal and only happens once.

### Out of memory error

Try using a smaller Whisper model (tiny or base).

## License

MIT License - Feel free to use and modify for your learning needs!
