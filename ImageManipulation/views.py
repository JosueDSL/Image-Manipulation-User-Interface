from flask import Blueprint, current_app , render_template, request, redirect, url_for, jsonify, flash, send_file
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from PIL import Image, ImageEnhance
from werkzeug.utils import secure_filename
import os

views = Blueprint("views", __name__)

@views.route("/upload-image", methods=["POST"])
@jwt_required()
def upload_image():
    # Check if the post request has the 'image' key in it
    if 'image' not in request.files:
        return jsonify(message='No file uploaded or received'), 400
    
    # Get the file from the POST request
    file = request.files['image']

    # If the user does not select a file, return an error message
    if file.filename == '':
        return jsonify(message='No selected file'), 400

    # Make sure the file has an allowed extension
    if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
        return jsonify(message='Invalid file type'), 400
    
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
        return jsonify(message='File already exists'), 400

    # Save the file to the upload folder
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    return jsonify(message=f'File {filename} successfully uploaded'), 200
    
@views.route("/list-images", methods=["GET"])
@jwt_required()
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
    return jsonify(images=image_files), 200


@views.route("/delete-image/<filename>", methods=["DELETE"])
@jwt_required()
def delete_image(filename):
    # Get the path to the upload folder
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # Make the full path to the image file
    file_path = os.path.join(upload_folder, filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        return jsonify(message=f'Image {filename} deleted successfully'), 200
    else:
        return jsonify(message=f'The image "{filename}" was not found'), 404

@views.route("/download-image/<filename>", methods=["GET"])
@jwt_required()
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

@views.route("/modify-image/<filename>", methods=["POST"])
@jwt_required()
def modify_image(filename):
    # Get path to the upload folder
    upload_folder = current_app.config['UPLOAD_FOLDER']

    # Get the full path to the image
    file_path = os.path.join(upload_folder, filename)

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the image using pillow
        image = Image.open(file_path)

        # Get the request data
        data = request.get_json()

        # Check for desired manipulations
        if 'resize' in data:
            # Apply resize
            width = data['resize']['width']
            height = data['resize']['height']
            image = image.resize((width, height))
        
        if 'rotate' in data:
            # Apply rotation
            angle = data['rotate']['angle']
            image = image.rotate(angle)

        if 'contrast' in data:
            # Convert image to RGB mode if it's not
            if image.mode != 'RGB':
                image = image.convert('RGB')
            # Apply contrast
            factor = data['contrast']['factor']
            image = ImageEnhance.Contrast(image).enhance(factor)
        
        # Save the modified image
        image.save(file_path)

        # Return a success message
        return jsonify(message=f'Image {filename} modified successfully'), 200
    else:
        return jsonify(message=f'The image "{filename}" was not found'), 404



        
