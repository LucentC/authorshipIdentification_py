from data_analysis import data_warehouse
import json

row = [(x, y) for x, y, z in data_warehouse.get_all_docs_by_author_id(2)]
print json.dumps(dict(row))
