import itertools
from database import connect_to_database

SQL_SELECT_QUERY = 'SELECT bigram_id, doc_id, para_id, bigram FROM bigram_feature ORDER BY bigram_id;'

word_list = list(itertools.chain.from_iterable([[word for word in item['bigram'].split('-')]
             for item in connect_to_database.execute_select_query(SQL_SELECT_QUERY)]))

previous = ''
for word in word_list:

    if previous == word:
        continue
    previous = word

    for idx in range(0, len(word) - 1):
        print word[idx], ' - ', word[idx + 1]