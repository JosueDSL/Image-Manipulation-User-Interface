from flask import Blueprint, current_app , render_template, request, redirect, url_for, jsonify, flash, send_file
from flask_login import login_required
from PIL import Image, ImageEnhance
from werkzeug.utils import secure_filename
import os

views = Blueprint("views", __name__)

@views.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html")

@views.route("/upload-image", methods=["GET","POST"])
@login_required
def upload_image():
    if request.method == 'POST':
        # Check if the post request has the 'image' key in it
        if 'image' not in request.files:
            flash('No file uploaded or received', category='danger')
            return redirect(url_for('views.upload_image'))
        
        # Get the file from the POST request
        file = request.files['image']

        # If the user does not select a file, return an error message
        if file.filename == '':
            flash('No selected file', category='danger')
            return redirect(url_for('views.upload_image'))

        # Make sure the file has an allowed extension
        if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
            flash('Invalid file type', category='danger')
            return redirect(url_for('views.upload_image'))
        
        # Ensure the file name is secure
        filename = secure_filename(file.filename)

        # Check if file is a valid image
        try:
            Image.open(file).verify()
        except Exception:
            return jsonify(message='Invalid image file'), 400
        file.seek(0) # Reset the file pointer

        # If the uploads folder does not exist, create one
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])
        
        # Ensure the file name does not already exist
        if os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
            flash('File already exists', category='danger')
            return redirect(url_for('views.upload_image'))
        
        # Save the file to the upload folder
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        flash(f'File {filename} successfully uploaded', category='success')
        return redirect(url_for('views.upload_image'))
    
    # GET
    else:
        return render_template("upload_image.html")

@views.route("/list-images-page", methods=["GET", "POST"])
@login_required
def list_images_page():
    if request.method == 'POST':

        return redirect(url_for('views.list_images_page'))

    images = list_images()
    return render_template("list_images.html", images=images)


@views.route("/list-images", methods=["GET"])
@login_required
def list_images():
    # Get the path to the upload folder
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # Get the list of files in the upload folder
    files = os.listdir(upload_folder)

    # if there are no files, return error message
    if len(files) == 0:
        return jsonify(message='No files found'), 404

    # Filter the list of files to only include images
    image_files = []
    for file_name in files:
        if file_name.endswith(('.png', '.jpg', '.jpeg')):
            image_files.append(file_name)

    # Return the list of files
    return image_files


@views.route("/delete-image/<filename>", methods=["POST"])
@login_required
def delete_image(filename):
    # Get the path to the upload folder
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # Make the full path to the image file
    file_path = os.path.join(upload_folder, filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        flash(f'Image {filename} deleted successfully', category='success')
        return redirect(url_for('views.list_images_page'))
    else:
        flash(f'The image "{filename}" was not found')
        return redirect(url_for('views.list_images_page'))

@views.route("/download-image/<filename>", methods=["GET"])
@login_required
def download_image(filename):
    # Get the path to the upload folder
    upload_folder = current_app.config['UPLOAD_FOLDER']

    # Get the full path to the image file
    file_path = os.path.join(upload_folder, filename)
    
    # Save absolute path to a new var
    absolute_file_path = os.path.abspath(file_path)

    # Check if the file exists
    if os.path.exists(file_path):
        return send_file(absolute_file_path, as_attachment=True)
    else:
        return jsonify(message=f'The image "{filename}" was not found'), 404


@views.route("/modify-image-page", methods=["GET"])
@login_required
def modify_image_page():
    # Get list of images
    images = list_images() 
    print(images)
    return render_template("modify_image.html", images=images)

@views.route("/modify-image/<filename>", methods=["POST"])
@login_required
def modify_image(filename):
    # Get path to the upload folder
    upload_folder = current_app.config['UPLOAD_FOLDER']

    # Get the full path to the image
    file_path = os.path.join(upload_folder, filename)

    # Function to check if a value is a float
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    # Check if the file exists
    if os.path.exists(file_path):
        # Open the image using pillow
        image = Image.open(file_path)

        # Get the request data
        width = request.form.get('width')
        height = request.form.get('height')
        rotate = request.form.get('rotate')
        contrast = request.form.get('contrast')

        # Ensure only numbers are passed in the request and convert them to int except for contrast
        variables = [('width', width), ('height', height), ('rotate', rotate), ('contrast', contrast)]

        print(type(width), type(height), type(rotate), type(contrast))
        print(width, height, rotate, contrast)
        for name, var in variables:
            if var is not None and var != '':
                if not is_float(var):
                    flash(f'{name.capitalize()} must be a number', category='danger')
                    return redirect(url_for('views.modify_image_page'))
                elif float(var) < 0:
                    flash(f'{name.capitalize()} must not be negative', category='danger')
                    return redirect(url_for('views.modify_image_page'))
                else:
                    if name == 'contrast':
                        contrast = float(var)
                    else:
                        var = int(var)
                        if name == 'width':
                            width = var
                        elif name == 'height':
                            height = var
                        elif name == 'rotate':
                            rotate = var   
        # Check for desired manipulations
        if width and height:
            MAX_SIZE = (1920, 1080)
            # If width or height is greater than the max size return error message
            if width > MAX_SIZE[0] or height > MAX_SIZE[1]:
                flash(f'Width and height must be less than {MAX_SIZE[0]} and {MAX_SIZE[1]} respectively', category='danger')
                return redirect(url_for('views.modify_image_page'))
            
            # Apply resize
            image = image.resize((width, height))
        
        # If only one field was passed return error message
        elif width or height:
            flash('Both width and height are required for resizing', category='danger')
            return redirect(url_for('views.modify_image_page'))

        if rotate:
            # if rotate greater than 360 or less than 0 return error message
            if rotate >= 360:
                flash('Rotation must be between 0 and 359', category='danger')
                return redirect(url_for('views.modify_image_page'))

            # Apply rotation
            image = image.rotate(rotate)

        if contrast:
            # Convert image to RGB mode if it's not
            if image.mode != 'RGB':
                image = image.convert('RGB')
            elif contrast > 10:
                flash('Contrast must be between 0 and 10', category='danger')
                return redirect(url_for('views.modify_image_page'))
            
            # Apply contrast
            image = ImageEnhance.Contrast(image).enhance(contrast)
        
        # Save the modified image
        image.save(file_path)

        # Return a success message
        flash(f'Image {filename} modified successfully', category='success')
        return redirect(url_for('views.modify_image_page'))
    else:
        flash(f'The image "{filename}" was not found', category='danger')
        return redirect(url_for('views.modify_image_page'))