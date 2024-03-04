from flask import Flask, send_file, request, jsonify
import os
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # 启用 CORS

UPLOAD_FOLDER = './upload'  # 上传文件的目录
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFile' not in request.files:
        return 'No file part'
    file = request.files['pdfFile']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = str(uuid.uuid4())+'.pdf' # + os.path.splitext(file.filename)[1]
        print(filename)
        file.save('./upload/' + filename)
        return jsonify({'uuid': filename})


@app.route('/view/<filename>', methods=['GET'])
def view_pdf(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404
    
if __name__ == '__main__':
    app.run(debug=True)
