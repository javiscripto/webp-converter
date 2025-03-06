from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
from werkzeug.utils import secure_filename
import io
import os
import vercel_wsgi


app= Flask(__name__)

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
# carpeta de subida
UPLOAD_FOLDER="uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #usar jsonify para devolver el quality
        quality = int(request.form.get("quality"))
        if "file" not in request.files:
            return render_template("upload.html", mensaje="no has proporcionado una imagen")
        file = request.files["file"]
        if file.filename == "":
            return render_template("upload.html", mensaje="la imagen no contiene un nombre de archivo permitido")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            # convertir a webp
        try:
            image = Image.open(file)
            webp_image = io.BytesIO()
            image.save(webp_image, format="WEBP", quality=quality)
            webp_image.seek(0)
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return send_file(webp_image, mimetype='image/webp', as_attachment=True, download_name="converted.webp")
    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return render_template("upload.html", mensaje="carga una imagen para comenzar")


if __name__ == "__main__":
    app.run(debug=True)


def handler(event, context):
    return vercel_wsgi.handle_request(app, event, context)
