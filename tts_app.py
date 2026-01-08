import gradio as gr
import edge_tts
import asyncio
import tempfile
import os
import PyPDF2
import docx
from pathlib import Path

# Language and voice mapping
VOICES = {
    "English (US)": {
        "Female - Aria": "en-US-AriaNeural",
        "Male - Guy": "en-US-GuyNeural", 
        "Female - Jenny": "en-US-JennyNeural",
        "Male - Davis": "en-US-DavisNeural"
    },
    "English (UK)": {
        "Female - Libby": "en-GB-LibbyNeural",
        "Male - Ryan": "en-GB-RyanNeural",
        "Female - Sonia": "en-GB-SoniaNeural"
    },
    "Spanish (Spain)": {
        "Female - Elvira": "es-ES-ElviraNeural",
        "Male - Alvaro": "es-ES-AlvaroNeural"
    },
    "Spanish (Mexico)": {
        "Female - Dalia": "es-MX-DaliaNeural",
        "Male - Jorge": "es-MX-JorgeNeural"
    },
    "French (France)": {
        "Female - Denise": "fr-FR-DeniseNeural",
        "Male - Henri": "fr-FR-HenriNeural"
    },
    "German": {
        "Female - Katja": "de-DE-KatjaNeural",
        "Male - Conrad": "de-DE-ConradNeural"
    },
    "Italian": {
        "Female - Elsa": "it-IT-ElsaNeural",
        "Male - Diego": "it-IT-DiegoNeural"
    },
    "Portuguese (Brazil)": {
        "Female - Francisca": "pt-BR-FranciscaNeural",
        "Male - Antonio": "pt-BR-AntonioNeural"
    },
    "Japanese": {
        "Female - Nanami": "ja-JP-NanamiNeural",
        "Male - Keita": "ja-JP-KeitaNeural"
    },
    "Korean": {
        "Female - Sun-Hi": "ko-KR-SunHiNeural",
        "Male - InJoon": "ko-KR-InJoonNeural"
    },
    "Chinese (Mandarin)": {
        "Female - Xiaoxiao": "zh-CN-XiaoxiaoNeural",
        "Male - Yunxi": "zh-CN-YunxiNeural"
    },
    "Hindi": {
        "Female - Swara": "hi-IN-SwaraNeural",
        "Male - Madhur": "hi-IN-MadhurNeural"
    },
    "Arabic": {
        "Female - Zariyah": "ar-SA-ZariyahNeural",
        "Male - Hamed": "ar-SA-HamedNeural"
    },
    "Russian": {
        "Female - Svetlana": "ru-RU-SvetlanaNeural",
        "Male - Dmitry": "ru-RU-DmitryNeural"
    }
}

def extract_text_from_file(file_path):
    """Extract text from various file formats"""
    if not file_path:
        return ""
    
    file_ext = Path(file_path).suffix.lower()
    
    try:
        if file_ext == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        
        elif file_ext == '.docx':
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        else:
            return "Unsupported file format. Please use PDF, DOCX, or TXT files."
    
    except Exception as e:
        return f"Error reading file: {str(e)}"

async def text_to_speech_async(text, voice, rate, pitch):
    """Convert text to speech using Edge TTS"""
    if not text.strip():
        return None
    
    # Create output file
    output_path = os.path.join(tempfile.gettempdir(), "tts_output.mp3")
    
    # Configure TTS
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=f"{rate:+d}%",
        pitch=f"{pitch:+d}Hz"
    )
    
    # Generate audio
    await communicate.save(output_path)
    return output_path

def text_to_speech(text, language, voice_name, rate, pitch):
    """Wrapper for async TTS function"""
    try:
        voice_id = VOICES[language][voice_name]
        return asyncio.run(text_to_speech_async(text, voice_id, rate, pitch))
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_file_and_convert(file, language, voice_name, rate, pitch):
    """Process uploaded file and convert to speech"""
    if file is None:
        return None, "Please upload a file first."
    
    # Extract text from file
    extracted_text = extract_text_from_file(file.name)
    
    if not extracted_text or "Error" in extracted_text:
        return None, extracted_text
    
    # Convert to speech
    audio_file = text_to_speech(extracted_text, language, voice_name, rate, pitch)
    
    return audio_file, extracted_text

def update_voices(language):
    """Update voice dropdown based on selected language"""
    if language in VOICES:
        choices = list(VOICES[language].keys())
        return gr.Dropdown(choices=choices, value=choices[0])
    return gr.Dropdown(choices=[], value=None)

# Create Gradio interface
with gr.Blocks(title="Multi-Language Text to Speech", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🌍 Multi-Language Text to Speech")
    gr.Markdown("Convert text or documents to speech in multiple languages with different voices and accents!")
    
    with gr.Tabs():
        # Text Input Tab
        with gr.TabItem("📝 Text Input"):
            with gr.Row():
                with gr.Column(scale=1):
                    text_input = gr.Textbox(
                        label="📝 Enter Text",
                        placeholder="Type your text here...",
                        lines=8,
                        max_lines=15
                    )
                    
                    with gr.Row():
                        language_dropdown = gr.Dropdown(
                            choices=list(VOICES.keys()),
                            value="English (US)",
                            label="🌐 Language/Accent"
                        )
                        
                        voice_dropdown = gr.Dropdown(
                            choices=list(VOICES["English (US)"].keys()),
                            value=list(VOICES["English (US)"].keys())[0],
                            label="🎭 Voice"
                        )
                    
                    with gr.Row():
                        rate_slider = gr.Slider(
                            minimum=-50,
                            maximum=50,
                            value=0,
                            step=5,
                            label="⚡ Speech Speed (%)"
                        )
                        
                        pitch_slider = gr.Slider(
                            minimum=-200,
                            maximum=200,
                            value=0,
                            step=10,
                            label="🎵 Pitch (Hz)"
                        )
                    
                    convert_btn = gr.Button(
                        "🔊 Convert to Speech", 
                        variant="primary", 
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    audio_output = gr.Audio(
                        label="🎧 Generated Audio",
                        type="filepath"
                    )
        
        # File Upload Tab
        with gr.TabItem("📄 File Upload"):
            with gr.Row():
                with gr.Column(scale=1):
                    file_input = gr.File(
                        label="📄 Upload Document",
                        file_types=[".pdf", ".docx", ".txt"],
                        type="filepath"
                    )
                    
                    with gr.Row():
                        file_language_dropdown = gr.Dropdown(
                            choices=list(VOICES.keys()),
                            value="English (US)",
                            label="🌐 Language/Accent"
                        )
                        
                        file_voice_dropdown = gr.Dropdown(
                            choices=list(VOICES["English (US)"].keys()),
                            value=list(VOICES["English (US)"].keys())[0],
                            label="🎭 Voice"
                        )
                    
                    with gr.Row():
                        file_rate_slider = gr.Slider(
                            minimum=-50,
                            maximum=50,
                            value=0,
                            step=5,
                            label="⚡ Speech Speed (%)"
                        )
                        
                        file_pitch_slider = gr.Slider(
                            minimum=-200,
                            maximum=200,
                            value=0,
                            step=10,
                            label="🎵 Pitch (Hz)"
                        )
                    
                    file_convert_btn = gr.Button(
                        "🔊 Convert File to Speech", 
                        variant="primary", 
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    file_audio_output = gr.Audio(
                        label="🎧 Generated Audio",
                        type="filepath"
                    )
                    
                    extracted_text_output = gr.Textbox(
                        label="📄 Extracted Text",
                        lines=10,
                        max_lines=15,
                        interactive=False
                    )
    
    gr.Markdown("""
    ### 📋 Instructions:
    **Text Input:**
    1. Enter your text in the text box
    2. Select language/accent and voice
    3. Adjust speed and pitch
    4. Click Convert to generate audio
    
    **File Upload:**
    1. Upload PDF, DOCX, or TXT file
    2. Select language/accent and voice
    3. Adjust speed and pitch
    4. Click Convert to generate audio
    
    ### 🌟 Features:
    - **14+ Languages** with native accents
    - **Multiple file formats** (PDF, DOCX, TXT)
    - **Multiple voices** per language
    - **Speed control** for faster/slower speech
    - **Pitch adjustment** for tone variation
    - **High quality** neural voices
    """)
    
    # Update voice dropdowns when language changes
    language_dropdown.change(
        fn=update_voices,
        inputs=language_dropdown,
        outputs=voice_dropdown
    )
    
    file_language_dropdown.change(
        fn=update_voices,
        inputs=file_language_dropdown,
        outputs=file_voice_dropdown
    )
    
    # Convert text to speech
    convert_btn.click(
        fn=text_to_speech,
        inputs=[text_input, language_dropdown, voice_dropdown, rate_slider, pitch_slider],
        outputs=audio_output
    )
    
    # Convert file to speech
    file_convert_btn.click(
        fn=process_file_and_convert,
        inputs=[file_input, file_language_dropdown, file_voice_dropdown, file_rate_slider, file_pitch_slider],
        outputs=[file_audio_output, extracted_text_output]
    )

if __name__ == "__main__":
    print("🚀 Starting Multi-Language TTS Server...")
    print(f"📊 Available languages: {len(VOICES)}")
    print(f"🎭 Total voices: {sum(len(voices) for voices in VOICES.values())}")
    app.launch(server_name="127.0.0.1", server_port=7860, show_error=True)