from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Ruta para la carpeta de almacenamiento de imágenes
UPLOAD_FOLDER = 'imagenes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurarse de que la carpeta de imágenes existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ruta para subir imágenes
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        files = request.files.getlist('file')  # Permitir múltiples archivos
        for file in files:
            if file.filename == '':
                return 'No selected file', 400
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        # Mostrar el mensaje de éxito
        return render_template('success.html')
    return render_template('upload.html')

# Ruta para servir imágenes estáticas
@app.route('/imagenes/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta para obtener la lista de imágenes
@app.route('/imagenes-list')
def get_images_list():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [f for f in files if f.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    return jsonify({'images': images})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
