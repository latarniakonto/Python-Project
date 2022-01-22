import unittest
import context
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from io import TextIOWrapper, BytesIO
from list8 import list_friend, list_book, Base, Friend, Book
        
#https://coderedirect.com/questions/89611/python-unittest-testcase-execution-order 
#solution for executing tests in order of their declaration in the class
def make_orderer():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare

ordered, compare = make_orderer()
unittest.defaultTestLoader.sortTestMethodsUsing = compare
#solution for executing tests by default in order of their declaration in the class

#Tests should be executed by default in order of their declaration in the class
class TestList8(unittest.TestCase):

    def setUp(self):      
        #unittest.TestLoader.sortTestMethodsUsing = None  
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)          
        self.session = Session()        
        self._old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
        self._stdout = sys.stdout


    def _output(self):
        self._stdout.seek(0)
        return self._stdout.read()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)  
        sys.stdout = self._old_stdout
        self._stdout.close()

    @ordered
    def test_list_book_empty(self):                    
        list_book(self.session)
        self.assertEqual(self._output(), "")

    @ordered
    def test_list_book_not_empty(self):                    
        b = Book(author="George R. R. Martin", title="A Game of Thrones", year=1996)
        self.session.add(b)
        list_book(self.session)
        self.assertEqual(self._output(), "(1, 'George R. R. Martin', 'A Game of Thrones', 1996)\n")        

    @ordered
    def test_list_friend_empty(self):                    
        list_friend(self.session)
        self.assertEqual(self._output(), "")

    @ordered
    def test_list_friend_not_empty(self):                            
        b = Book(author="George R. R. Martin", title="A Game of Thrones", year=1996)
        self.session.add(b)
        f = Friend("Jon Snow", "night@watch.com", 1, self.session)
        self.session.add(f)
        list_friend(self.session)
        self.assertEqual(self._output(), "(1, 'Jon Snow', 'night@watch.com', 1)\n")


if __name__ == "__main__":            
    unittest.main()