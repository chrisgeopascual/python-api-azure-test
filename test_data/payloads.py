from faker import Faker

fake = Faker()


def build_book_payload(book_id=None):

    return {
        "id": book_id if book_id is not None else fake.random_int(min=1, max=9999),
        "title": fake.sentence(nb_words=4),
        "description": fake.paragraph(nb_sentences=2),
        "pageCount": fake.random_int(min=50, max=900),
        "excerpt": fake.paragraph(nb_sentences=3),
        "publishDate": fake.iso8601() + "Z",
    }