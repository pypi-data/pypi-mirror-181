import pykson


class BookAuthor(pykson.JsonObject):
    first_name = pykson.StringField(serialized_name="firstName", null=False)
    last_name = pykson.StringField(serialized_name="lastName", null=False)
    age = pykson.IntegerField(serialized_name="age", null=False)
    date_of_birth = pykson.StringField(serialized_name="dateOfBirth", null=False)


class BookReviews(pykson.JsonObject):
    publisher = pykson.StringField(serialized_name="publisher", null=False)
    reviewer_name = pykson.StringField(serialized_name="reviewerName", null=False)
    review_date = pykson.DateTimeField(datetime_format=None, serialized_name="reviewDate", null=False)
    rate = pykson.FloatField(serialized_name="rate", null=False)


class Book(pykson.JsonObject):
    name = pykson.StringField(serialized_name="name", null=False)
    pages = pykson.IntegerField(serialized_name="pages", null=False)
    publication_date = pykson.DateTimeField(datetime_format=None, serialized_name="publication_date", null=False)
    author = pykson.ObjectField(item_type=BookAuthor, serialized_name="author", null=False)
    reviews = pykson.ObjectListField(item_type=BookReviews, serialized_name="reviews", null=False)


if __name__ == "__main__":
    test_json = {
        "name": "Harry Potter and the Deathly Hallows",
        "pages": 607,
        "publication_date": "27 July 2007",
        "author": {
            "firstName": "J.K.",
            "lastName": "Rowling",
            "age": 57,
            "dateOfBirth": "1965-06-31 "
        },
        "reviews": [
            {
                "publisher": "The New York Times",
                "reviewerName": "Stephen King",
                "reviewDate": "July 23, 2000",
                "rate": 10.0
            },
            {
                "publisher": "Kirkus Reviews",
                "reviewerName": "Kirkus Reviews",
                "reviewDate": "JULY 8, 2000",
                "rate": 9.5
            }
        ]
    }    
    obj = pykson.Pykson().from_json(test_json, Book)
