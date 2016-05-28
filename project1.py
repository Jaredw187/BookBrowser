from flask import Flask
from flask import render_template
from flask import abort
# To get the current year for our copyright information
from datetime import datetime
# Import JSON to use author.json and books.json
import json

# Telling flask what's included in my application.
app = Flask(__name__)

# Global Variables
site_title = "Digital Library Collection"
dict_books = {}
dict_authors = {}

# Load in all the json files into dictionaries.
with open('myFiles/books.json', 'r', encoding='utf-8') as myFile:
    dict_books = json.load(myFile)
with open('myFiles/authors.json', 'r', encoding='utf-8') as myFile:
    dict_authors = json.load(myFile)

# Get the # of authors and books in the current data set.
numAuthors = len(dict_authors)
numBooks = len(dict_books)


# Creating a list for all of the authors.
authorList = []
for authors in dict_authors:
    for author in authors:
        if author == 'name':
            authorList.append(authors['name'])


# Creating a list to total the number of editions
editions = []

# Appending all editions to a list if not in list
for ed in dict_books:
    for edi in ed["editions"]:
            editions.append(edi["id"])


# Getting the length of the editions (i.e. number of editions)
numEditions = len(editions)


# Leads to the homepage.
@app.route('/')
def index():
    return render_template('index.html', site_title=site_title, currentYear=datetime.now().year, numBooks=numBooks,
                           numAuthors=numAuthors, numEditions=numEditions)


# The page that shows a list of all the authors in the data set.
@app.route('/authors/')
def authors():
    return render_template('allAuthors.html', currentYear=datetime.now().year, site_title=site_title, dict_authors=dict_authors,
                           authorList=authorList, i=1)


# The page that shows a list of all the books in the data set.
@app.route('/books/')
def books():
    return render_template('allBooks.html', currentYear=datetime.now().year, site_title=site_title, dict_books=dict_books)


# The page that shows an individual author.
@app.route('/author/<aid>/')
def author(aid):
    match = None
    for author in dict_authors:
        if author["id"] == aid:
            match = True
            break
        else:
            match = False
    if match == False:
        return abort(404)
    else:
        return render_template('author.html', currentYear=datetime.now().year, author=aid, dict_authors=dict_authors, aid=aid, dict_books=dict_books)

# The page that shows an individual book.
@app.route('/book/<bid>/')
def book(bid):
    match = None;
    for book in dict_books:
        if book["id"] == bid:
            match = True
            break
        else:
            match = False
    if match == False:
        return abort(404)
    else:
        return render_template('book.html', currentYear=datetime.now().year, site_title=site_title, bid=bid, dict_books=dict_books, dict_authors = dict_authors)


# The page that show an individual book's editions.
@app.route('/books/<bid>/editions/<eid>/')
def editions(bid, eid):
    return render_template('edition.html', currentYear=datetime.now().year,  bookID=bid, editionID=eid, dict_books=dict_books, dict_authors=dict_authors)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', currentYear=datetime.now().year, site_title=site_title), 404


# Create our flask app for applification.
if __name__ == '__main__':
    app.run(debug=True)
