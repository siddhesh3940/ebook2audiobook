import gradio as gr
import pyttsx3
import os
import tempfile

def text_to_speech(text, voice_speed=150):
    """Convert text to speech using pyttsx3"""
    if not text.strip():
        return None
    
    # Initialize TTS engine
    engine = pyttsx3.init()
    
    # Set properties
    engine.setProperty('rate', voice_speed)
    
    # Generate audio file
    output_path = os.path.join(tempfile.gettempdir(), "output.wav")
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    
    return output_path

def get_available_voices():
    """Get list of available voices"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_names = []
    for voice in voices:
        voice_names.append(voice.name)
    return voice_names

def text_to_speech_with_voice(text, voice_name, voice_speed):
    """Convert text to speech with specific voice"""
    if not text.strip():
        return None
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Set voice
    for voice in voices:
        if voice.name == voice_name:
            engine.setProperty('voice', voice.id)
            break
    
    # Set speed
    engine.setProperty('rate', voice_speed)
    
    # Generate audio
    output_path = os.path.join(tempfile.gettempdir(), "output.wav")
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    
    return output_path

# Create Gradio interface
with gr.Blocks(title="Simple Text to Speech") as app:
    gr.Markdown("# Simple Text to Speech")
    gr.Markdown("Convert any text to speech instantly!")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Enter Text",
                placeholder="Type your text here...",
                lines=6
            )
            
            with gr.Row():
                voice_dropdown = gr.Dropdown(
                    choices=get_available_voices(),
                    value=get_available_voices()[0] if get_available_voices() else "Default",
                    label="Select Voice"
                )
                speed_slider = gr.Slider(
                    minimum=50,
                    maximum=300,
                    value=150,
                    step=10,
                    label="Speech Speed"
                )
            
            convert_btn = gr.Button("🔊 Convert to Speech", variant="primary", size="lg")
        
        with gr.Column():
            audio_output = gr.Audio(label="Generated Audio", type="filepath")
    
    convert_btn.click(
        fn=text_to_speech_with_voice,
        inputs=[text_input, voice_dropdown, speed_slider],
        outputs=audio_output
    )

if __name__ == "__main__":
    print("Starting Simple Text-to-Speech Server...")
    print("Available voices:", len(get_available_voices()))
    app.launch(server_name="127.0.0.1", server_port=7860, show_error=True)