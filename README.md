# Shadow English - Sentence by Sentence Practice Tool

A web-based application for practicing English speaking using the shadowing technique. The tool uses OpenAI's Whisper AI to transcribe audio files and display sentences with individual play buttons for focused practice.

## Features

- 🎵 **Audio Upload**: Support for MP3, WAV, MP4, M4A, OGG, FLAC, and WebM formats
- 🤖 **AI Transcription**: Automatic transcription using OpenAI's Whisper model
- 📝 **Optional Script**: Provide your own script file (TXT) or let Whisper generate one
- ▶️ **Sentence-by-Sentence Playback**: Individual play button for each sentence
- 🔁 **Loop Mode**: Loop a single sentence for repeated practice
- 🎚️ **Speed Control**: Adjust playback speed (0.5x to 1.5x)
- 🎨 **Modern UI**: Clean, dark-themed interface optimized for learning

## Prerequisites

1. **Python 3.8+**
2. **FFmpeg** - Required for audio processing
   - Windows: Download from https://ffmpeg.org/download.html and add to PATH
   - Or use: `winget install FFmpeg`

## Installation

1. **Navigate to the project folder**:

   ```bash
   cd d:\Personal\Shadow\Whisper
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Note: Installing PyTorch and Whisper may take a few minutes.

## Usage

1. **Start the server**:

   ```bash
   python app.py
   ```

2. **Open your browser** and go to:

   ```
   http://localhost:5000
   ```

3. **Upload an audio file** (required)

4. **Optionally upload a script file** (TXT with one sentence per line)

5. **Click "Process Audio with Whisper AI"**

6. **Practice**:
   - Click the **Play** button on any sentence to hear just that part
   - Click the **Loop** button to repeat a sentence continuously
   - Use the speed control to slow down or speed up playback

## Script File Format

If you have the transcript, create a TXT file with one sentence per line:

```
Hello, welcome to today's lesson.
We're going to learn about English pronunciation.
Let's start with the basics.
```

## Whisper Model Options

By default, the app uses the "base" model for a balance of speed and accuracy. You can change this in `app.py`:

| Model  | Size    | Speed   | Accuracy |
| ------ | ------- | ------- | -------- |
| tiny   | 39 MB   | Fastest | Lower    |
| base   | 74 MB   | Fast    | Good     |
| small  | 244 MB  | Medium  | Better   |
| medium | 769 MB  | Slow    | High     |
| large  | 1550 MB | Slowest | Highest  |

To change the model, edit line 17 in `app.py`:

```python
model = whisper.load_model("small")  # or "medium", "large", etc.
```

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
