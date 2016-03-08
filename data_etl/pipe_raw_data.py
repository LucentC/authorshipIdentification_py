import zipfile

dir_path = '/tmp/gutenberg/'
path_to_store_txt = '/tmp/gutenberg/txt'


def process_book_item(book):
    zip_path = dir_path + book['host_path'][0]
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(path_to_store_txt)
        print z.namelist()[0]
