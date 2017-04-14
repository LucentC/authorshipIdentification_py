import time
from database import connect_to_database
from data_analysis import data_warehouse
from DocumentRippleTagClass import DocumentRippleTag

language_dict = {
    'French': 'fr',
    'English': 'en',
    'Italian': 'it',
    'Finnish': 'fi',
    'Swedish': 'sv',
    'Spanish': 'es',
    'German': 'de',
    'Portuguese': 'pt',
    'Latin': 'la',
    'Dutch': 'nl',
}

start_time = time.time()
print 'Starting the extration process'
SQL_QUERY_GET_META = 'SELECT a.author_id, a.doc_id, a.lang, array_agg(b.para_id) as paragraph_list ' \
                     'FROM dickson_multiple_languages a INNER JOIN paragraph b ON a.doc_id = b.doc_id ' \
                     'WHERE a.doc_id > 3292 AND b.sw_id = 0 GROUP BY a.doc_id, a.author_id, a.lang;'
results = connect_to_database.execute_select_query(SQL_QUERY_GET_META)

for item in results:

    doc_id = item['doc_id']
    lang = language_dict[item['lang']]
    paragraph_list = item['paragraph_list']
    content = data_warehouse.get_doc_content_by_id(doc_id=doc_id)
    # Start to tag the document
    print 'Process document with doc_id: {}'.format(doc_id)
    doc = DocumentRippleTag(doc_id=doc_id, language=lang, paragraph_list=paragraph_list, doc_text=content)
    doc.to_csv('test')

print 'Total execution time: {} seconds'.format(time.time() - start_time)
