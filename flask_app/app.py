import csv
from StringIO import StringIO
from flask import Flask
from flask import render_template, make_response, request
from werkzeug.utils import secure_filename
from data_analysis import data_warehouse
from data_analysis import data_to_csv

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('data_visualize/index.html',
                           title='Testing Page')


@app.route('/charts')
def get_chars():
    return render_template('data_visualize/charts.html')


@app.route('/getcsv')
def get_csv():
    author_list = []
    feature_list = []

    t1 = data_warehouse.get_features_from_database_by_doc_id(1)
    feature_list.extend(t1)
    author_list.extend([0 for x in range(len(t1))])

    t2 = data_warehouse.get_features_from_database_by_doc_id(408)
    feature_list.extend(t2)
    author_list.extend([1 for x in range(len(t2))])

    t3 = data_warehouse.get_features_from_database_by_doc_id(318)
    feature_list.extend(t3)
    author_list.extend([2 for x in range(len(t3))])

    string_io = StringIO()
    cw = csv.writer(string_io)
    cw.writerows(data_to_csv.get_output_lists_for_csv_after_3d_pca(author_list, feature_list))

    output = make_response(string_io.getvalue())
    #output.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    output.headers['Content-type'] = 'text/plaintext'
    return output


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploadhandler', methods = ['GET', 'POST'])
def upload_handler():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
