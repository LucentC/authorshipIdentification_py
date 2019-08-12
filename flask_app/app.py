import csv
import itertools
import os
from StringIO import StringIO

from flask import Flask
from flask import render_template, make_response, request, Markup, jsonify, session
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from csv_exportation import data_to_csv
from data_analysis import calculate_K_nearest_neighbors_classifier as cknn
from data_analysis import comparision_top10
from data_analysis import data_warehouse
from data_analysis import modified_hausdorff_distance as MHD
from data_etl import plaintext_data_etl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def index():
    return render_template('data_visualize/index.html',
                           title='Dashboard',
                           content=Markup(u'This is the index page of this application.<br> In the following 3 boxes, '
                                          u'<strong>Total number of authors</strong>, <strong>Total number of '
                                          u'documents</strong> and <strong>Total number of documents with Stylometric '
                                          u'features calculated</strong> will be shown.'),
                           no_of_authors='Retrieving',
                           no_of_documents='Retrieving',  # data_warehouse.get_total_num_of_docs(),
                           no_of_documents_with_stylo='Retrieving',
                           # data_warehouse.get_total_num_of_docs_with_stylo_values(),
                           author_and_docs=data_warehouse.get_author_and_written_docs_count()
                           )


@app.route('/get-dbstat')
def get_db_statistic():
    return jsonify({
        'no_of_authors': data_warehouse.get_total_num_of_authors(),
        'no_of_documents': data_warehouse.get_total_num_of_docs(),
        'no_of_documents_with_stylo': data_warehouse.get_total_num_of_docs_with_stylo_values(),
    })


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
                                   authors_list=data_warehouse.get_all_author_id_and_name()
                                   )

    if request.method == 'POST':
        try:
            author_id = int(request.form['author_id'])
            doc_num = data_warehouse.get_num_of_doc_written_by_an_author(author_id)
        except ValueError:
            abort(403)

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

@app.route('/getstylocsv')
def get_stylo_csv_file():
    try:
        doc_id = int(request.args.get('doc_id'))
    except ValueError:
        abort(403)

    header_row = ['author id', 'document id', 'paragraph id'] + ['feature ' + str(i) for i in range(1, 57)]
    data_list = data_warehouse.get_cross_tab_features_from_database_by_doc_id(doc_id)

    string_io = StringIO()
    cw = csv.writer(string_io)
    cw.writerow(header_row)

    for row in data_list:
        cw.writerow(row)

    output = make_response(string_io.getvalue())
    output.headers['Content-type'] = 'application/csv'
    output.headers['Content-Disposition'] = 'attachment;filename=doc_{}.csv'.format(doc_id)
    return output



@app.route('/doccontent', methods=['POST'])
def get_doc_content():
    if request.method != 'POST':
        abort(403)

    try:
        doc_id = int(request.form['doc_id'])
    except ValueError:
        abort(403)

    return jsonify(dict(data_warehouse.get_doc_content_by_id(doc_id)))


@app.route('/upload')
def upload_file():
    return render_template('data_visualize/upload.html',
                           title='KNN Authorship Determination',
                           content=Markup(u'In this page, you may upload a txt file to the server. The '
                                          u'application will search the entire database to find an author with the '
                                          u'closest writing style by using the Probabilistic K-Nearest Neighbor '
                                          u'Algorithm. Drag and Drop a txt file to the box in order to '
                                          u'upload the txt file to the server. The display of probabilistic values '
                                          u'is provided in the form of CSV file.'),
                           authors_list=data_warehouse.get_all_author_id_and_name()
                           )

@app.route('/saveauthors', methods=['POST'])
def save_authors():
    session['authors'] = request.form.getlist('authors')
    return 'ok'


@app.route('/knnstatics', methods=['POST'])
def get_knn_statics():
    if request.method != 'POST':
        abort(403)

    results = []
    prefix_path = '/var/tmp/stylometric_app/knn_upload/'

    f = request.files['file']
    path = os.path.join(prefix_path, secure_filename(f.filename))
    f.save(path)

    if not os.path.exists(path):
        abort(403)

    qp = plaintext_data_etl.read_file_and_get_doc_list(path)
    author_hash = dict([(row['author_id'], row['author_name']) for row in data_warehouse.get_all_author_id_and_name()])

    try:
        authors = session['authors']
        feature_list, author_list = data_warehouse.get_features_from_database_fact_by_list_of_author_id(authors)
    except KeyError:
        feature_list, author_list = data_warehouse.get_all_features_from_database_fact()

    knn_proba = cknn.get_query_set_probabilistic(feature_list, author_list, qp)

    authors = list(set(author_list))

    for idx in range(len(set(authors))):
        results.append((author_hash.get(authors[idx]), knn_proba[idx]))

    session.clear()
    return jsonify(dict(results))


@app.route('/charts')
def get_chars():
    return render_template('data_visualize/charts.html',
                           title='Stylometric Charts',
                           content=Markup(u'In this page, you can compare the writing styles of <strong>at most 3 '
                                          u'documents</strong> in terms of stylometric features. Firstly, you need to '
                                          u'select an author from the drop-down list. Afterwards, another drop-down '
                                          u'list is shown for you to select the document. Finally, click the button '
                                          u'<mark>Add to Table</mark> to add the document into the cache. You will '
                                          u'need to repeat the steps until there are at least 2 documents.'),
                           authors_list=data_warehouse.get_all_author_id_and_name()
                           )


@app.route('/gethausdis', methods=['POST'])
def get_haus_distance():

    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return itertools.izip(a, b)

    doc_id_list = request.form.getlist('doc_list')

    distance = {}
    for x, y in pairwise(doc_id_list + [doc_id_list[0]]):
        distance[data_warehouse.get_doc_title_by_id(x) + ", " + data_warehouse.get_doc_title_by_id(y)] = MHD.\
            get_min_of_avg_hausdorff_distance(
                data_warehouse.get_stylometric_features_by_doc_id(x),
                data_warehouse.get_stylometric_features_by_doc_id(y))

    return jsonify(distance)


@app.route('/getdoclist', methods=['POST'])
def return_doc_list():
    if request.method != 'POST':
        abort(403)

    try:
        author_id = int(request.form['author_id'])
    except ValueError:
        abort(403)

    # x, y, z refers to doc_id, doc_title and year_of_pub respectively
    doc_list = [(x, y) for x, y, z in data_warehouse.get_all_docs_by_author_id(author_id)]
    return jsonify(doc_list)


@app.route('/getcsv', methods=['POST'])
def get_csv():

    author_list = []
    feature_list = []

    doc_id_list = request.form.getlist('doc_list')

    

    for idx in range(0, len(doc_id_list)):
        features = data_warehouse.get_stylometric_features_by_doc_id(doc_id_list[idx])
        feature_list.extend(features)
        author_list.extend([doc_id_list[idx] for x in range(len(features))])

    string_io = StringIO()
    cw = csv.writer(string_io)
    cw.writerows(data_to_csv.get_output_lists_for_csv_after_3d_pca(author_list, feature_list))

    output = make_response(string_io.getvalue())
    output.headers['Content-type'] = 'text/plaintext'
    return output


@app.route('/getcsvall', methods=['POST'])
def get_csv_of_all_features():
    author_list = []
    feature_list = []

    doc_id_list = request.form.getlist('doc_list')

    for idx in range(0, len(doc_id_list)):
        features = data_warehouse.get_stylometric_features_by_doc_id(doc_id_list[idx])
        feature_list.extend(features)
        author_list.extend([idx for x in range(len(features))])

    string_io = StringIO()
    cw = csv.writer(string_io)
    cw.writerows(data_to_csv.get_output_lists_for_csv_after_3d_pca(author_list, feature_list))

    output = make_response(string_io.getvalue())
    output.headers['Content-type'] = 'text/plaintext'
    return output


@app.route('/selffunc')
def running_self_defined_distance():
    return render_template('data_visualize/selfdistance.html',
                           title='Self-defined Distance',
                           content='TBC',
                           authors_list=data_warehouse.get_all_author_id_and_name()
                           )


@app.route('/select-doc')
def select_document():
    if request.method == 'POST':
        abort(403)

    if request.method == 'GET':

        doc_list = []
        with open('/var/tmp/demo_queryset_all_docs.csv', 'rb') as csvfile:
            demo_query_set = csv.reader(csvfile, delimiter=',')
            for row in demo_query_set:
                doc_list.append(row[0])

        return render_template('data_visualize/select_doc.html',
                               title='Select an author',
                               content=u'Select an author in the following list and the system will display the '
                                       u'details of that author you selected',
                               doc_list=data_warehouse.get_docs_name_by_doc_ids(doc_list)
                               )


@app.route('/compare-top', methods=['POST'])
def compare_authors():
    if request.method == 'GET':
        abort(403)

    if request.method == 'POST':
        doc_id = request.form['doc_id']
        # try:
        author_id, stat = comparision_top10.queryExp(int(doc_id))
        print stat
        return render_template('data_visualize/show_stat.html',
                               title='Result',
                               content='',
                               author=data_warehouse.get_author_name_by_id(author_id),
                               stat=stat.iteritems()
                               )
        # except ValueError as e:
        #     print e.message
        #     abort(403)


@app.errorhandler(403)
def return_403_forbidden(e):
    return render_template('errorhandler/403.html',
                           title='403 Forbidden',
                           content='Bring it on!')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
    app.jinja_env.autoescape = False
