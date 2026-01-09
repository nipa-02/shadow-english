from flask import Flask, render_template, request, jsonify, send_from_directory
import whisper
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load Whisper model - use tiny for free hosting, can override with WHISPER_MODEL env var
# Options: tiny, base, small, medium, large
WHISPER_MODEL = os.environ.get('WHISPER_MODEL', 'tiny')
print(f"Loading Whisper model: {WHISPER_MODEL}...")
model = whisper.load_model(WHISPER_MODEL)
print("Model loaded!")

ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'mp4', 'm4a', 'ogg', 'flac', 'webm'}
ALLOWED_TEXT_EXTENSIONS = {'txt'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def merge_into_sentences(segments, end_buffer=0.2):
    """
    Split Whisper segments into proper individual sentences based on punctuation.
    Handles both merging incomplete sentences AND splitting segments with multiple sentences.
    """
    if not segments:
        return []
    
    # First, collect all words with their timestamps
    all_words = []
    for segment in segments:
        if 'words' in segment:
            # Use word-level timestamps if available
            for word in segment['words']:
                all_words.append({
                    'word': word.get('word', ''),
                    'start': word.get('start', segment['start']),
                    'end': word.get('end', segment['end'])
                })
        else:
            # Fall back to segment-level timestamps, estimate word times
            words = segment['text'].strip().split()
            if words:
                duration = segment['end'] - segment['start']
                word_duration = duration / len(words)
                for i, word in enumerate(words):
                    all_words.append({
                        'word': word,
                        'start': segment['start'] + i * word_duration,
                        'end': segment['start'] + (i + 1) * word_duration
                    })
    
    if not all_words:
        return []
    
    # Now group words into sentences based on punctuation
    sentences = []
    current_words = []
    
    for word_info in all_words:
        word = word_info['word']
        current_words.append(word_info)
        
        # Check if this word ends a sentence (ends with . ! ?)
        if re.search(r'[.!?]["\'\)]?\s*$', word):
            # Create a sentence from accumulated words
            if current_words:
                sentence_text = ' '.join(w['word'] for w in current_words).strip()
                # Clean up spacing around punctuation
                sentence_text = re.sub(r'\s+([.!?,;:])', r'\1', sentence_text)
                
                sentences.append({
                    'id': len(sentences),
                    'start': current_words[0]['start'],
                    'end': current_words[-1]['end'] + end_buffer,
                    'text': sentence_text
                })
                current_words = []
    
    # Don't forget remaining words that don't end with punctuation
    if current_words:
        sentence_text = ' '.join(w['word'] for w in current_words).strip()
        sentence_text = re.sub(r'\s+([.!?,;:])', r'\1', sentence_text)
        
        sentences.append({
            'id': len(sentences),
            'start': current_words[0]['start'],
            'end': current_words[-1]['end'] + end_buffer,
            'text': sentence_text
        })
    
    return sentences

    return sentences

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    script_file = request.files.get('script')
    
    if audio_file.filename == '':
        return jsonify({'error': 'No audio file selected'}), 400
    
    if not allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
        return jsonify({'error': 'Invalid audio file format'}), 400
    
    # Save audio file
    audio_filename = secure_filename(audio_file.filename)
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
    audio_file.save(audio_path)
    
    try:
        # Transcribe with Whisper
        print(f"Transcribing {audio_filename}...")
        result = model.transcribe(
            audio_path,
            word_timestamps=True,
            verbose=False
        )
        
        # Process segments and merge into proper sentences based on punctuation
        END_TIME_BUFFER = 0.2  # Extra time after each sentence
        raw_segments = result['segments']
        sentences = merge_into_sentences(raw_segments, END_TIME_BUFFER)
        
        # If a script file is provided, use it to match/override the text
        if script_file and script_file.filename != '' and allowed_file(script_file.filename, ALLOWED_TEXT_EXTENSIONS):
            script_content = script_file.read().decode('utf-8')
            script_sentences = [s.strip() for s in script_content.split('\n') if s.strip()]
            
            # If number of sentences match, use the script text with Whisper timestamps
            if len(script_sentences) == len(sentences):
                for i, script_text in enumerate(script_sentences):
                    sentences[i]['text'] = script_text
            else:
                # Return both for user to see
                return jsonify({
                    'success': True,
                    'audio_url': f'/uploads/{audio_filename}',
                    'sentences': sentences,
                    'script_sentences': script_sentences,
                    'warning': f'Script has {len(script_sentences)} lines but audio has {len(sentences)} segments. Using Whisper transcription.'
                })
        
        return jsonify({
            'success': True,
            'audio_url': f'/uploads/{audio_filename}',
            'sentences': sentences,
            'language': result.get('language', 'unknown')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/transcribe-only', methods=['POST'])
def transcribe_only():
    """Transcribe audio without script - just get timestamps"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        return jsonify({'error': 'No audio file selected'}), 400
    
    if not allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
        return jsonify({'error': 'Invalid audio file format'}), 400
    
    audio_filename = secure_filename(audio_file.filename)
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
    audio_file.save(audio_path)
    
    try:
        result = model.transcribe(
            audio_path,
            word_timestamps=True,
            verbose=False
        )
        
        # Merge segments into proper sentences
        END_TIME_BUFFER = 0.2
        sentences = merge_into_sentences(result['segments'], END_TIME_BUFFER)
        
        return jsonify({
            'success': True,
            'audio_url': f'/uploads/{audio_filename}',
            'sentences': sentences,
            'language': result.get('language', 'unknown')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
