import itertools
from database import connect_to_database
from psycopg2.extensions import QuotedString

SQL_SELECT_QUERY = 'SELECT bigram_id, doc_id, para_id, bigram FROM bigram_feature WHERE bigram_id BETWEEN 1 AND 100 ' \
                   'ORDER BY bigram_id;'

# word_list = list(itertools.chain.from_iterable([[word for word in item['bigram'].split('-')]
#              for item in connect_to_database.execute_select_query(SQL_SELECT_QUERY)]))

# previous = ''
# for word in word_list:
#
#     if previous == word:
#         continue
#     previous = word
#
#     for idx in range(0, len(word) - 1):
#         print word[idx], ' - ', word[idx + 1]
#
#
# print '---------------------------------------------------------------------------------'

previous = ''
for item in connect_to_database.execute_select_query(SQL_SELECT_QUERY):

    for word in item['bigram'].split('-'):
        if previous == word:
            continue
        previous = word

        SQL_INSERT_QUERY = ''
        for idx in range(0, len(word) - 1):
            SQL_INSERT_QUERY += 'INSERT INTO char_bigram_feature(bigram_id, doc_id, para_id, char_bigram) ' \
                                'VALUES ({}, {}, {}, {})'.format(item['bigram_id'], item['doc_id'], item['para_id'],
                                                                 QuotedString(word[idx] + ' - ' + word[idx + 1])
                                                                 .getquoted())

        connect_to_database.execute_insert_query(SQL_INSERT_QUERY)
