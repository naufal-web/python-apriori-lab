from flask import *
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = r"C:\Users\62853\PycharmProjects\apriori_lab\implementation\through_web\temp"


CSV_EXTENSIONS = {"csv"}


def allowed_filename(file_name: str):
    return "." in file_name and file_name.rsplit(".", 1)[1].lower() in CSV_EXTENSIONS


@app.route('/')
def home():
    return render_template("file_upload.html")


@app.route('/upload', methods=['POST'])
def upload_files():
    if "file" in request.files:
        file = request.files["file"]
        if file and allowed_filename(file_name=file.filename):
            filename = secure_filename(file.filename)
            storage_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(storage_path)
            except Exception as e:
                return f'Error saving file: {str(e)}', 500
            else:
                try:
                    from apriori import Apriori

                    min_sup = round(int(request.form["minimum_support"]) / 100, 4)
                    min_confidence = round(int(request.form["minimum_confidence"]) / 100, 4)
                    apriori = Apriori(filepath=storage_path, min_support=min_sup, min_confidence=min_confidence)
                    apriori.start_now()

                    supportive_items = apriori.items_which_above_support_value
                    confidence_items = apriori.items_which_above_confidence_value
                    validated_items = apriori.items_which_above_lift_ratio

                    encapsulated_result = (supportive_items, confidence_items, validated_items)

                    return render_template("result.html", results=encapsulated_result)
                except ModuleNotFoundError:
                    return "Olah Data Belum Bisa"

        elif file and not allowed_filename(file_name=file.filename):
            return "Unggah Berkas :: Tidak Cocok"
        else:
            return "Unggah Berkas :: Tidak Ada Berkas"
    else:
        return 'Unggah Berkas :: Belum Ada Berkas', 400


@app.errorhandler(413)
def too_large(e):
    return make_response(jsonify(message="Berkas yang Anda unggah lebih dari 16 MB"), 413)


@app.errorhandler(RequestEntityTooLarge)
def file_too_large(e):
    return "Berkas yang Anda unggah jauh lebih besar daripada biasanya"


if __name__ == '__main__':
    app.run(debug=True)