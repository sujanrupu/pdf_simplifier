from flask import Flask, request, render_template, redirect, url_for
import fitz  # PyMuPDF
from utils import extract_text_from_pdf, extract_keywords, paraphrase_text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_bytes = file.read()
        text = extract_text_from_pdf(file_bytes)
        keywords = extract_keywords(text)
        
        return render_template('index.html', text=text, keywords=keywords)
    
    return redirect(url_for('index'))

@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    text_to_paraphrase = request.form['text']
    paraphrased_text = paraphrase_text(text_to_paraphrase)
    keywords = extract_keywords(text_to_paraphrase)  # Extract keywords again after paraphrasing
    return render_template('index.html', text=text_to_paraphrase, paraphrased_text=paraphrased_text, keywords=keywords)

