#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import cv2
import urllib.request
import os
from werkzeug.utils import secure_filename

def crop_by_position(img, position, size):
    size = int(size)
    height, width = img.shape[:2]
    if position == 'top_left':
        return img[0:size, 0:size]
    elif position == 'top_center':
        return img[0:size, width // 2 - size // 2:width // 2 + size // 2]
    elif position == 'top_right':
        return img[0:size, width - size:width]
    elif position == 'center_left':
        return img[height // 2 - size // 2:height // 2 + size // 2, 0:size]
    elif position == 'center':
        return img[height // 2 - size // 2:height // 2 + size // 2, width // 2 - size // 2:width // 2 + size // 2]
    elif position == 'center_right':
        return img[height // 2 - size // 2:height // 2 + size // 2, width - size:width]
    elif position == 'bottom_left':
        return img[height - size:height, 0:size]
    elif position == 'bottom_center':
        return img[height - size:height, width // 2 - size // 2:width // 2 + size // 2]
    elif position == 'bottom_right':
        return img[height - size:height, width - size:width]
    else:
        return None

app = Flask(__name__)

#filePath = ''
#filename = ''

UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        global filename
        filename = secure_filename(file.filename)
        global filePath
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
        file.save(filePath)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/crop/', methods=['GET', 'POST'])
def crop():
    # Handle the form submission
    size = request.form.get('size')
    position = request.form.get('position')
    print(f'the size is {size}')
    print(f'the position is {position}')
    
    # Process the size and position values as required
    # Perform any necessary operations based on the form data
    img = cv2.imread(filePath)
    cropedImage = crop_by_position(img, position, size)
    cv2.imwrite("static/crop/" + filename, cropedImage)
    # Return a response or redirect to another page
    # For example, you could render a template that displays the cropped image
    return render_template('result.html', filename=filename)


@app.route('/displayCrop/<filename>')
def display_CroppedImage(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='crop/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()