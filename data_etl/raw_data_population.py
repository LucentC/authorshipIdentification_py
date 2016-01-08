import os
from gutenberg_crawler.BookItem import BookItem

base_dir = '/home/dickson/Documents/programming/Gutenberg/txt/'
min_size = 100 * 1000 #100 Kb

for root, sub_dir, files in os.walk(base_dir):
    for fi in files:
        if os.path.getsize(root + fi) >= min_size:
            book = BookItem()
            book['title'] = fi.split('___')[0]
            book['author_name'] = fi.split('___')[1][:-4]
            print book['title']
            print book['author_name']
            print
            # with open(root + fi, 'r') as doc_file:
            #     book['content'] = doc_file.read()

# print book['title']
# print book['author_name']
# print
#print book['content']

