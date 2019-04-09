import os

from flask import Flask, jsonify, request, flash

from utils import extract_text_from_pdf, extract_name, extract_mobile_numbers, extract_emails, extract_skills, \
    get_skills

UPLOAD_FOLDER = 'upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/parse', methods=['POST'])
def parse_cv():
    if 'file' not in request.files:
        flash('No file part')

    file = request.files['file']

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'tmp.pdf'))

        file_path = 'upload/tmp.pdf'
        text = ''
        for page in extract_text_from_pdf(file_path):
            text += ' ' + page

        name = extract_name(text)
        phone = extract_mobile_numbers(text)
        email = extract_emails(text)
        skills = extract_skills(text)
        return jsonify(name=name, phones=phone, emails=email, skills=skills)


@app.route('/skills')
def skills():
    return jsonify(skills=get_skills())


if __name__ == '__main__':
    app.run()
