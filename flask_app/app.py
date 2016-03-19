from __future__ import print_function
import csv
import sys
from StringIO import StringIO
from flask import Flask
from flask import render_template, make_response, request, Markup
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
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
                           no_of_documents_with_stylo=data_warehouse.get_total_num_of_docs_with_stylo_values(),
                           author_and_docs=data_warehouse.get_author_and_written_docs_count()
                           )


@app.route('/details', methods=['GET', 'POST'])
def get_author_details():
    if request.method == 'GET':
        author_id = request.args.get('author_id')
        doc_num = request.args.get('doc_num')

        if author_id is None and doc_num is None:
            return render_template('data_visualize/select_author.html',
                                   title='Select an author',
                                   content=u'Select an author in the following list and the system will display the '
                                           u'details of that author you selected',
                                   authors_list=data_warehouse.get_author_id_and_name()
                                   )

    if request.method == 'POST':
        author_id = request.form['author_id']
        doc_num = data_warehouse.get_num_of_doc_written_by_an_author(author_id)

    try:
        author_id = int(author_id)
        doc_num = int(doc_num)
    except ValueError:
        abort(403)

    author_name = data_warehouse.get_author_name_by_id(author_id)
    return render_template('data_visualize/author_details.html',
                           title=author_name,
                           content=Markup(u'You are now looking at <strong>{}</strong>. There are <strong>{}</strong> '
                                          u'of documents written by {} stored in our database.'
                                          .format(author_name, doc_num, author_name)),
                           doc_list=data_warehouse.get_all_docs_by_author_id(author_id)
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


@app.route('/doccontent', methods=['POST'])
def get_doc_content():
    if request.method != 'POST':
        abort(403)

    try:
        doc_id = int(request.form['doc_id'])
    except ValueError:
        abort(403)

    output = make_response(data_warehouse.get_doc_content_by_id(doc_id))
    output.headers['Content-type'] = 'text/plaintext'
    return output




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


@app.errorhandler(403)
def return_403_forbidden(e):
    return render_template('errorhandler/403.html',
                           title='403 Forbidden',
                           contene='Bring it on!')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
    app.jinja_env.autoescape = False
