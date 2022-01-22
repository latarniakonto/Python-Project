import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import sessionmaker
import argparse
from sqlalchemy.orm.mapper import validates
from sqlalchemy.engine import Engine
from sqlalchemy import event

documentation = """
Book storage-rental system

Friend table - It's a table of friends who are borrowing books from us. When we lent someone 
               our a book, we can add new entry friends to our database using "friend --add 
               --name NAME --email EMAIL --book BOOK". The same friend(in regard of NAME, EMAIL) 
               can borrow many different books from us. When adding to friend table NAME, 
               EMAIL and BOOK must be specified. When the borrowed book returns to us we can
               delete that entry from our database using "friend --delete --id ID --name NAME
               --email EMAIL --book BOOK". If any of --id, --name, --email, --book is omitted
               it's value will no longer take part in deletion process. Deletion will be done
               using only valid and specified arguments values. We can list contents of friend 
               table using "friend --list"

Book table - Its's a table of books that we own. We can add new book to our database
             using "book --add --author AUTHOR --title TITLE --year YEAR". We can have 
             many the same books(in ragard of AUTHOR, TITLE and YEAR), however their IDs
             will be different in the database. When adding to book table AUTHOR, TITLE 
             and YEAR must specified. We can delete book from our database using "book 
             --delete --id ID --author AUTHOR --title TITLE --year YEAR". If any of --id, 
             --author, --title, --year is omitted it's value will no longer take part in 
             deletion process. Deletion will be done using only valid and specified arguments
             values. We can list contents of book table using "book --list".                          
"""

#Event for handling cascade DELETE of foreign keys.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base = declarative_base()
current_session = None

class Friend(Base):
    __tablename__ = "Friend"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    book = Column(Integer, ForeignKey("Book.id", ondelete="CASCADE"))    

    def __init__(self, name, email, book, session=None):
        self.session = session
        self.name = name
        self.email = email
        self.book = book

    @validates("name")
    def validate_name(self, key, value):
        assert value is not None
        return value
    
    @validates("email")
    def validate_email(self, key, value):
        assert value is not None
        return value

    @validates("book")
    def validate_book(self, key, value):        
        if self.session is None:
            self.session = current_session

        for row in self.session.query(Friend):                                                            
            if int(row.book) == int(value):
                assert False

        for row in self.session.query(Book):            
            if int(row.id) == int(value):
                return value
        assert False

class Book(Base): 
    __tablename__ = "Book"

    id = Column(Integer, primary_key=True)
    author = Column(String)
    title = Column(String)
    year = Column(Integer)    

    @validates("author")
    def validate_author(self, key, value):
        assert value is not None
        return value

    @validates("title")
    def validate_title(self, key, value):
        assert value is not None
        return value

    @validates("year")
    def validate_year(self, key, value):
        assert value is not None
        return value

def init():
    global current_session
    engine = create_engine("sqlite:////tmp/temp.db")    
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)    
    current_session = Session()            

def parse_arguments(argv):        
    parser = argparse.ArgumentParser(description="Book storage-rental system")
        
    subparser = parser.add_subparsers(help="Supported tables", dest="table")
    parser_book = subparser.add_parser("book", help="Book table in database")
    group_book = parser_book.add_mutually_exclusive_group()
    group_book.add_argument("--add", action="store_true", help="Add row to book table")
    group_book.add_argument("--delete", action="store_true", help="Delete row from book table")
    group_book.add_argument("--list", action="store_true", help="List contents of book table")
    parser_book.add_argument("-i", "--id", type=int, help="Book's id in book table")
    parser_book.add_argument("-a", "--author", type=str, help="Book's author")
    parser_book.add_argument("-t", "--title", type=str, help="Book's title")
    parser_book.add_argument("-y", "--year", type=str, help="Year when book was published")
    
    parser_friend = subparser.add_parser("friend", help="Friend table in database")
    group_friend = parser_friend.add_mutually_exclusive_group()
    group_friend.add_argument("--add", action="store_true", help="Add row to friend table")
    group_friend.add_argument("--delete", action="store_true", help="Delete row from friend table")
    group_friend.add_argument("--list", action="store_true", help="List contents of friend table")
    parser_friend.add_argument("-i", "--id", type=int, help="Friend's id in friend table")
    parser_friend.add_argument("-n", "--name", type=str, help="Friend's name")
    parser_friend.add_argument("-e", "--email", type=str, help="Friend's email")
    parser_friend.add_argument("-b", "--book", type=str, help="Book that this friend borrowed from us")

    argv = parser.parse_args()
    return argv

def add_book(author, title, year):
    global current_session
    b = Book(author=author, title=title, year=year)        
    current_session.add(b)    

def add_friend(name, email, book):
    global current_session
    f = Friend(name=name, email=email, book=book)        
    current_session.add(f)    

def list_book(session=None):
    if session is None:
        session = current_session
        
    for row in session.query(Book):
        row_tuple = (row.id, row.author, row.title, row.year)
        print(row_tuple)    

def list_friend(session=None):
    if session is None:
        session = current_session

    for row in session.query(Friend):
        row_tuple = (row.id, row.name, row.email, row.book)
        print(row_tuple)    

def delete_book(del_id, del_author, del_title, del_year):    
    global current_session
    if del_id is None:
        del_id = Book.id    
    if del_author is None:
        del_author = Book.author
    if del_title is None:
        del_title = Book.title
    if del_year is None:
        del_year = Book.year
    
    current_session.query(Book).filter_by(id=del_id, author=del_author, title=del_title, year=del_year).delete()             

def delete_friend(del_id, del_name, del_email, del_book):    
    global current_session
    if del_id is None:
        del_id = Friend.id    
    if del_name is None:
        del_name = Friend.name
    if del_email is None:
        del_email = Friend.email
    if del_book is None:
        del_book = Friend.book
                    
    current_session.query(Friend).filter_by(id=del_id, name=del_name, email=del_email, book=del_book).delete()            

def read_arguments(argv):    
    if argv.table == "book":
        if argv.add:                        
            add_book(argv.author, argv.title, argv.year)
            pass        
        elif argv.delete:
            delete_book(argv.id, argv.author, argv.title, argv.year)
            
        elif argv.list:
            list_book()
        else:
            exit(1)
    elif argv.table == "friend":
        if argv.add:
            add_friend(argv.name, argv.email, argv.book)            
        elif argv.delete:
            delete_friend(argv.id, argv.name, argv.email, argv.book)
        elif argv.list:
            list_friend()                                    
        else:
            exit(1)
    else:
        exit(1)    

def main(argv):    
    global current_session
    init()
    if current_session is None: exit(1)
    argv = parse_arguments(argv)    
    read_arguments(argv)
                    
    current_session.commit()
    current_session.close()    
                     
if __name__ == "__main__":
    try:
        main(sys.argv)
    except ValueError:            
        exit(0)

# Test cases(commands lines that I ran)(commands line order matters)
# python3 list8.py book --add --author "George R. R. Martin" --title "A Game of Thrones" --year 1996
# python3 list8.py book --add --author "George R. R. Martin" --title "A Game of Thrones" --year 1996
# python3 list8.py book --add --author "George R. R. Martin" --title "A Game of Thrones" --year 1996
# python3 list8.py book --add --author "George R. R. Martin" --title "A Game of Thrones" --year 1996
# python3 list8.py book --add --author "George R. R. Martin" --title "A Game of Thrones" --year 1996
# python3 list8.py book --add --author "George R. R. Martin" --title "A Game of Thrones" --year 1996
# python3 list8.py book --list
# python3 list8.py friend --add --name "Jon Snow" --email "night@watch.com" --book 3
# python3 list8.py friend --list
# python3 list8.py friend --delete --name "Jon Snow" --email "night@watch.com" --book 3
# python3 list8.py friend --list
# python3 list8.py friend --add --name "Jon Snow" --email "night@watch.com" --book 3
# python3 list8.py friend --add --name "Jon Snow" --email "night@watch.com" --book 4
# python3 list8.py friend --list
# python3 list8.py friend --delete --name "Jon Snow" --email "night@watch.com"
# python3 list8.py friend --list
# python3 list8.py friend --add --name "Jon Snow" --email "night@watch.com" --book 3
# python3 list8.py friend --list
# python3 list8.py book --list
# python3 list8.py book --delete --author "George R. R. Martin"
# python3 list8.py book --list
# python3 list8.py friend --list