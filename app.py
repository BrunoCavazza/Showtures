import os
import uuid
from datetime import datetime

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Ruta para la carpeta de almacenamiento de imágenes
UPLOAD_FOLDER = 'imagenes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB por request

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

# URL de administración (borrado de fotos). No tiene autenticación: se confía
# en que el path no es adivinable y no se enlaza desde ninguna página de invitados.
ADMIN_PATH = 'admin-6f3k9p'

# Asegurarse de que la carpeta de imágenes existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def unique_filename(filename):
    safe_name = secure_filename(filename)
    prefix = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    return f"{prefix}-{safe_name}"


def is_inside_upload_folder(path):
    upload_folder_abs = os.path.abspath(app.config['UPLOAD_FOLDER'])
    return os.path.abspath(path).startswith(upload_folder_abs + os.sep)


@app.errorhandler(413)
def too_large(_e):
    return 'El archivo es demasiado grande (máximo 20MB por subida)', 413


# Ruta para subir imágenes
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        files = request.files.getlist('file')
        if not files or all(f.filename == '' for f in files):
            return 'No selected file', 400
        for file in files:
            if file.filename == '':
                return 'No selected file', 400
            if not allowed_file(file.filename):
                return f'Tipo de archivo no permitido: {file.filename}', 400
        for file in files:
            filename = unique_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('success.html')
    return render_template('upload.html')


# Ruta para servir imágenes estáticas
@app.route('/imagenes/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], secure_filename(filename))


# Ruta para obtener la lista de imágenes
@app.route('/imagenes-list')
def get_images_list():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    images = sorted(f for f in files if f.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS)
    if request.args.get('order') == 'desc':
        images.reverse()
    return jsonify({'images': images})


# Ruta de administración: ver y borrar fotos subidas
@app.route(f'/{ADMIN_PATH}')
def admin_gallery():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    images = sorted(
        (f for f in files if f.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS),
        reverse=True,
    )
    return render_template('admin.html', images=images, admin_path=ADMIN_PATH)


@app.route(f'/{ADMIN_PATH}/delete/<filename>', methods=['POST'])
def admin_delete(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if is_inside_upload_folder(filepath) and os.path.isfile(filepath):
        os.remove(filepath)
    return ('', 204)


@app.route(f'/{ADMIN_PATH}/clear', methods=['POST'])
def admin_clear():
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f)
        if is_inside_upload_folder(filepath) and os.path.isfile(filepath):
            os.remove(filepath)
    return ('', 204)


# Ruta para la presentación / slideshow (unifica todo en un solo servidor)
@app.route('/presentation')
def presentation():
    return render_template('presentation.html')


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
