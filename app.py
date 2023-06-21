import logging
from flask import Flask, request, send_file, jsonify
from gtts import gTTS
from moviepy.editor import TextClip, concatenate_videoclips, AudioFileClip
import tempfile

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/generate_video', methods=['POST'])
def generate_video():
    try:
        # Get data from request
        data = request.json
        qa_array = data.get('qa_array')
        language = data.get('language', 'en')  # Default to English

        # Generate video clips for each question and answer
        clips = []
        for qa in qa_array:
            text = "Question: {}\nAnswer: {}".format(qa['question'], qa['answer'])
            tts = gTTS(text=text, lang=language)
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(audio_file.name)
            audio_clip = AudioFileClip(audio_file.name)

            text_clip = TextClip(text, fontsize=24, size=(640, 480), color='black', bg_color='white', print_cmd=True)
            text_clip = text_clip.set_duration(audio_clip.duration).set_audio(audio_clip)

            clips.append(text_clip)

        # Concatenate clips and write to file
        final_clip = concatenate_videoclips(clips)
        video_file_path = 'qa_video.mp4'  # Save the file to the current directory with a fixed name
        final_clip.write_videofile(video_file_path, audio_codec='aac', fps=24)

        # Send video file as response
        return send_file(video_file_path, mimetype='video/mp4', as_attachment=True, download_name='qa_video.mp4')
    except Exception as e:
        logging.error("An error occurred: {}".format(str(e)))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
