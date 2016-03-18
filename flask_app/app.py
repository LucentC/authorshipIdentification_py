import csv
from StringIO import StringIO
from flask import Flask
from flask import render_template, make_response, request, Markup
from werkzeug.utils import secure_filename
from data_analysis import data_warehouse
from data_analysis import data_to_csv

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('data_visualize/index.html',
                           title='Dashboard',
                           content=Markup(u'This is the index page of this application.<br> In the following 3 boxes, '
                                          u'<strong>Total number of authors</strong>, <strong>Total number of '
                                          u'documents</strong> and <strong>Total number of documents with Stylometric '
                                          u'features calculated</strong> will be shown.'),
                           no_of_authors=data_warehouse.get_total_num_of_authors(),
                           no_of_documents=data_warehouse.get_total_num_of_docs(),
                           no_of_documents_with_stylo=data_warehouse.get_total_num_of_docs_with_stylo_values()
                           )


@app.route('/upload')
def upload_file():
    return render_template('data_visualize/upload.html',
                           title='Upload',
                           content=Markup(u'In this page, you may upload a txt file to the server. The '
                                          u'application will search the entire database to find an author with the '
                                          u'closest writing style. Drag and Drop a txt file to the box in order to '
                                          u'upload the txt file to the server. The display of probabilistic values '
                                          u'is provided in the form of CSV file.')
                           )


@app.route('/charts')
def get_chars():
    return render_template('data_visualize/charts.html',
                           title='Charts',
                           content='TBC'
                           )


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


@app.route('/uploadhandler', methods=['GET', 'POST'])
def upload_handler():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    app.jinja_env.autoescape = False
