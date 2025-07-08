import csv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import cv2
import pytesseract
import os

app = Flask(__name__)
CORS(app)

#file to store extracted text
TEXT_FILE = "extracted_text.txt"

def save_text_to_file(text):
    """Save extracted text to a file."""
    with open(TEXT_FILE, "w") as f:
        f.write(text)

def load_text_from_file():
    """Load extracted text from a file."""
    try:
        with open(TEXT_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

# Store extracted text globally
extracted_text = "Hello World!"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/start_canvas", methods=["POST"])
def start_canvas():
    subprocess.Popen(["python", "virtual_painter/main.py"])  # Runs Air Canvas
    return "Air Canvas started! Draw your text and upload the image."

# Extract text using OpenCV & Tesseract
def extract_text(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(processed_image)
    return text.strip()    

@app.route('/save_text', methods=['POST'])
def save_text():
    data = request.get_json()
    if data and 'text' in data:
        extracted_text = data['text']
        save_text_to_file(extracted_text)  
        print("Received Extracted Text:", extracted_text)
        return jsonify({"message": "Text saved successfully!", "text": extracted_text})
    else:
        return jsonify({"error": "Invalid request"}), 400

@app.route('/get_text', methods=['GET'])
def get_text():
    extracted_text = load_text_from_file()  
    return jsonify({"text": extracted_text})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        extracted_text = extract_text(file_path)
        save_text_to_file(extracted_text)
        return jsonify({"message": "File uploaded and text extracted successfully!"}), 200

CSV_FILE = '/Users/apple/Desktop/virtual/genres.csv'

def read_songs_from_csv(file_path, genre):
    """Read songs from a CSV file and filter by genre."""
    songs = []
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['genre'].lower() == genre.lower():
                    songs.append({'title': row['title']})
    except FileNotFoundError:
        return None
    return songs

@app.route('/songs', methods=['GET'])
def get_songs_by_genre():
    genre = request.args.get('genre')
    if not genre:
        return jsonify({"error": "Genre parameter is required"}), 400

    songs = read_songs_from_csv(CSV_FILE, genre)
    if songs is None:
        return jsonify({"error": "CSV file not found"}), 500

    return jsonify(songs)

if __name__ == "__main__":
    app.run(debug=True)