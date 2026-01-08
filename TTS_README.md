# 🌍 Multi-Language Text to Speech

Convert text or documents (PDF, DOCX, TXT) to speech in 14+ languages with different voices, accents, and tones!

## 🚀 Quick Start

### Installation
```bash
pip install -r tts_requirements.txt
```

### Run the Application
```bash
python tts_app.py
```

Open your browser to: `http://127.0.0.1:7860`

## ✨ Features

- **14+ Languages**: English (US/UK), Spanish, French, German, Italian, Portuguese, Japanese, Korean, Chinese, Hindi, Arabic, Russian
- **Multiple Input Types**: Direct text input OR file upload (PDF, DOCX, TXT)
- **Multiple Voices**: Male/female options for each language
- **Speed Control**: Adjust speech rate (-50% to +50%)
- **Pitch Control**: Change voice tone (-200Hz to +200Hz)
- **Native Accents**: Authentic pronunciation for each region
- **High Quality**: Microsoft Edge neural voices
- **Tabbed Interface**: Separate tabs for text input and file upload

## 📋 Usage

### Text Input Tab:
1. **Enter your text** in the text box
2. **Select language/accent** from dropdown
3. **Choose voice** (male/female options)
4. **Adjust speed** (-50% to +50%)
5. **Adjust pitch** (-200Hz to +200Hz)
6. **Click Convert** to generate audio

### File Upload Tab:
1. **Upload PDF, DOCX, or TXT file**
2. **Select language/accent** from dropdown
3. **Choose voice** (male/female options)
4. **Adjust speed** (-50% to +50%)
5. **Adjust pitch** (-200Hz to +200Hz)
6. **Click Convert** to generate audio
7. **View extracted text** in the preview box

## 🌐 Supported Languages

| Language | Accents | Voices |
|----------|---------|--------|
| English | US, UK | 7 voices |
| Spanish | Spain, Mexico | 4 voices |
| French | France | 2 voices |
| German | Germany | 2 voices |
| Italian | Italy | 2 voices |
| Portuguese | Brazil | 2 voices |
| Japanese | Japan | 2 voices |
| Korean | Korea | 2 voices |
| Chinese | Mandarin | 2 voices |
| Hindi | India | 2 voices |
| Arabic | Saudi Arabia | 2 voices |
| Russian | Russia | 2 voices |

## 📄 Supported File Formats

- **PDF**: Extracts text from PDF documents
- **DOCX**: Extracts text from Word documents
- **TXT**: Reads plain text files

## 🛠️ Requirements

- Python 3.7+
- gradio
- edge-tts
- PyPDF2
- python-docx