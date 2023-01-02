# This is a sample Python script.
import io
import os

from PyPDF2 import PdfReader
from gtts import gTTS
from flask import Flask, render_template, request, app, abort, send_file, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
language = 'pt'


# Press the green button in the gutter to run the script.

def transform_file(filename) -> str:
    reader = PdfReader(filename)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    gTTS_tool = gTTS(text=text, lang=language, slow=False)

    #os.system("mpg321 test.mp3")

    output_filename = os.path.splitext(filename)[0] + ".mp3"

    gTTS_tool.save(output_filename)

    os.remove(filename)

    return output_filename


@app.route("/pdf", methods=["POST"])
def pdf_upload():
    if request.files.get("file") is None:
        abort(400, 'File was not found')
    f = request.files.get("file")
    f.save(secure_filename(f.filename))
    # Put here some other checks (security, file length etc...)
    output_filename = transform_file(f.filename)

    @after_this_request
    def remove_file(response):
        os.remove(output_filename)
        return response

    return send_file(output_filename, as_attachment=True, download_name=output_filename), 201

if __name__ == '__main__':
    app.run(port=8003, debug=True)