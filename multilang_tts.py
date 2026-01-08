import gradio as gr
import edge_tts
import asyncio
import tempfile
import os

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

def update_voices(language):
    """Update voice dropdown based on selected language"""
    if language in VOICES:
        choices = list(VOICES[language].keys())
        return gr.Dropdown(choices=choices, value=choices[0])
    return gr.Dropdown(choices=[], value=None)

# Create Gradio interface
with gr.Blocks(title="Multi-Language Text to Speech", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🌍 Multi-Language Text to Speech")
    gr.Markdown("Convert text to speech in multiple languages with different voices and accents!")
    
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
            
            gr.Markdown("""
            ### 📋 Instructions:
            1. **Enter your text** in the text box
            2. **Select language/accent** from dropdown
            3. **Choose voice** (male/female options)
            4. **Adjust speed** (-50% to +50%)
            5. **Adjust pitch** (-200Hz to +200Hz)
            6. **Click Convert** to generate audio
            
            ### 🌟 Features:
            - **14+ Languages** with native accents
            - **Multiple voices** per language
            - **Speed control** for faster/slower speech
            - **Pitch adjustment** for tone variation
            - **High quality** neural voices
            """)
    
    # Update voice dropdown when language changes
    language_dropdown.change(
        fn=update_voices,
        inputs=language_dropdown,
        outputs=voice_dropdown
    )
    
    # Convert text to speech
    convert_btn.click(
        fn=text_to_speech,
        inputs=[text_input, language_dropdown, voice_dropdown, rate_slider, pitch_slider],
        outputs=audio_output
    )

if __name__ == "__main__":
    print("🚀 Starting Multi-Language TTS Server...")
    print(f"📊 Available languages: {len(VOICES)}")
    print(f"🎭 Total voices: {sum(len(voices) for voices in VOICES.values())}")
    app.launch(server_name="127.0.0.1", server_port=7860, show_error=True)