from flask import *
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
try:
    app.config["UPLOAD_FOLDER"] = r"C:\Users\62853\PycharmProjects\apriori_lab\implementation\through_web\temp"
except FileNotFoundError:
    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), r"\implementation\through_web\temp")


CSV_EXTENSIONS = {"csv"}


def allowed_filename(file_name: str):
    return "." in file_name and file_name.rsplit(".", 1)[1].lower() in CSV_EXTENSIONS


def slicing_dictionary(dct: dict, index: int):
    copy = dct.copy()
    copy.clear()

    for index, (key, value) in zip(range(index), dct.items()):
        copy[key] = value

    dct.clear()
    dct = copy

    return dct


def descending_dictionary_value(dct: dict):
    return dict(sorted(dct.items(), key=lambda item: item[1], reverse=True))


def ascending_dictionary_value(dct: dict):
    sorted_dict = {}
    for key in sorted(dct, key=dct.get):
        sorted_dict[key] = dct[key]

    return sorted_dict


@app.route('/')
def home():
    if len(os.listdir(app.config['UPLOAD_FOLDER'])) > 0:
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            try:
                os.remove(file)
            except FileNotFoundError:
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], file))
    return render_template("etl_tools.html")


@app.route('/transform_data', methods=['POST'])
def transform_files():
    if "file" in request.files:
        file = request.files["file"]
        if file and allowed_filename(file_name=file.filename):
            filename = secure_filename(file.filename)
            storage_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            retrieval_path = os.path.join(app.config['UPLOAD_FOLDER'], "binary_data.csv")
            try:
                file.save(storage_path)
            except Exception as e:
                return f'Error saving file: {str(e)}', 500
            else:
                from one_hot_encoding import OneHotEncoding
                from apriori import Apriori
                file_encoding = OneHotEncoding(source=storage_path, destination=retrieval_path)
                file_encoding.encode()

                min_sup = round(int(request.form["minimum_support"]) / 100, 4)
                min_confidence = round(int(request.form["minimum_confidence"]) / 100, 4)
                max_columns = int(request.form["maximum_columns"])
                sorting_option = request.form["option"]

                apriori = Apriori(filepath=retrieval_path, min_support=min_sup, min_confidence=min_confidence)
                apriori.start_now()

                supportive_items = apriori.items_which_above_support_value
                confidence_items = apriori.items_which_above_confidence_value
                validated_items = apriori.items_which_above_lift_ratio

                if sorting_option == "True":
                    supportive_items = descending_dictionary_value(supportive_items)
                    confidence_items = descending_dictionary_value(confidence_items)
                    validated_items = descending_dictionary_value(validated_items)
                elif sorting_option == "False":
                    supportive_items = ascending_dictionary_value(supportive_items)
                    confidence_items = ascending_dictionary_value(confidence_items)
                    validated_items = ascending_dictionary_value(validated_items)

                supportive_items = slicing_dictionary(supportive_items, max_columns)
                confidence_items = slicing_dictionary(confidence_items, max_columns)
                validated_items = slicing_dictionary(validated_items, max_columns)

                encapsulated_result = (supportive_items, confidence_items, validated_items)

                return render_template("result.html", results=encapsulated_result,
                                       minimum_support=min_sup, minimum_confidence=min_confidence)

        elif file and not allowed_filename(file_name=file.filename):
            return "Unggah Berkas :: Tidak Cocok"
        else:
            return "Unggah Berkas :: Tidak Ada Berkas"
    else:
        return 'Unggah Berkas :: Belum Ada Berkas', 400



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
                    max_columns = int(request.form["maximum_columns"])
                    sorting_option = request.form["option"]
                    apriori = Apriori(filepath=storage_path, min_support=min_sup, min_confidence=min_confidence)
                    apriori.start_now()

                    supportive_items = apriori.items_which_above_support_value
                    confidence_items = apriori.items_which_above_confidence_value
                    validated_items = apriori.items_which_above_lift_ratio

                    if sorting_option == "True":
                        supportive_items = descending_dictionary_value(supportive_items)
                        confidence_items = descending_dictionary_value(confidence_items)
                        validated_items = descending_dictionary_value(validated_items)
                    elif sorting_option == "False":
                        supportive_items = ascending_dictionary_value(supportive_items)
                        confidence_items = ascending_dictionary_value(confidence_items)
                        validated_items = ascending_dictionary_value(validated_items)

                    supportive_items = slicing_dictionary(supportive_items, max_columns)
                    confidence_items = slicing_dictionary(confidence_items, max_columns)
                    validated_items = slicing_dictionary(validated_items, max_columns)

                    encapsulated_result = (supportive_items, confidence_items, validated_items)

                    return render_template("result.html", results=encapsulated_result,
                                           minimum_support=min_sup, minimum_confidence=min_confidence)
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