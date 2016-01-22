import csv
from StringIO import StringIO
from flask import Flask
from flask import render_template, make_response
from pca import data_analysis

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

    t1 = data_analysis.get_features_from_database_by_doc_id(1)
    feature_list.extend(t1)
    author_list.extend([0 for x in range(len(t1))])

    t2 = data_analysis.get_features_from_database_by_doc_id(408)
    feature_list.extend(t2)
    author_list.extend([1 for x in range(len(t2))])

    t3 = data_analysis.get_features_from_database_by_doc_id(318)
    feature_list.extend(t3)
    author_list.extend([2 for x in range(len(t3))])

    string_io = StringIO()
    cw = csv.writer(string_io)
    cw.writerows(data_analysis.output_csv_lists(author_list, feature_list))

    output = make_response(string_io.getvalue())
    #output.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    output.headers['Content-type'] = 'text/plaintext'
    return output


@app.route('/upload')
def upload_file():
    """
        Peter, please place your code in this function
    """
    return "I love coding"


if __name__ == '__main__':
    app.run()
