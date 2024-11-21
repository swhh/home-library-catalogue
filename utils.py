from collections import Counter


def count_books_by_author(books, author):
    return sum(1 for book in books if book[1] == author)

def find_top_n_authors(books, n):
    counter = Counter(book[1] for book in books)
    return counter.most_common(n)

def generate_books(texts, separator='-'):
    all_books = []
    for text in texts:
        books = text.split('\n')
        books = [book.split(separator) for book in books]
        books = [[item.strip() for item in book] for book in books] # strip whitespace
        all_books.extend(books)
    return all_books

def remove_duplicate_books(books):
    return list(map(list, dict.fromkeys(map(tuple, books))))



