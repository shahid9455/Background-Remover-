from flask import Flask, request, send_file, render_template, redirect, url_for
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No image file provided", 400
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    try:
        img = Image.open(file.stream)

        img_no_bg = remove(img)

        resized_img = img_no_bg.resize((500, 500))

        img_io = io.BytesIO()
        resized_img.save(img_io, 'PNG')
        img_io.seek(0)

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_image.png')
        resized_img.save(output_path)

        return redirect(url_for('display_image'))
    
    except Exception as e:
        return str(e), 500

@app.route('/display')
def display_image():
    return render_template('display.html', image_url=url_for('uploaded_file', filename='processed_image.png'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
    app.run(debug=True)
