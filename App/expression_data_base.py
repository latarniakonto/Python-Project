from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.mapper import validates
from expression_formatter import decode_expression

Base = declarative_base()


class ArithmeticExpression(Base):
    __tablename__ = "ARITHMETIC_EXPRESSION"

    id = Column(Integer, primary_key=True)
    expression_encoding = Column(String)

    def __init__(self, expression_encoding, session=None):
        self.session = session
        self.expression_encoding = expression_encoding

    @validates("expression_encoding")
    def validate_expression_encoding(self, key, value):
        assert value is not None
        assert self.session is not None
        for row in self.session.query(ArithmeticExpression):
            if str(row.expression_encoding) == str(value):
                assert False

        return value


class ProgrammingExpression(Base):
    __tablename__ = "PROGRAMMING_EXPRESSION"

    id = Column(Integer, primary_key=True)
    expression_encoding = Column(String)

    def __init__(self, expression_encoding, session=None):
        self.session = session
        self.expression_encoding = expression_encoding

    @validates("expression_encoding")
    def validate_expression_encoding(self, key, value):
        assert value is not None
        assert self.session is not None
        for row in self.session.query(ProgrammingExpression):
            if(str(row.expression_encoding) == str(value)):
                assert False

        return value


def init():
    engine = create_engine("sqlite:////tmp/temp.db",
                           connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    current_session = Session()
    return current_session


def add_arithmetic_expression(expression_encoding, session):
    ae = ArithmeticExpression(expression_encoding=expression_encoding,
                              session=session)
    session.add(ae)
    return session


def add_programming_expression(expression_encoding, session):
    pe = ProgrammingExpression(expression_encoding=expression_encoding,
                               session=session)
    session.add(pe)
    return session


def list_programming_expression(session):
    for row in session.query(ProgrammingExpression):
        row_tuple = (row.id, row.expression_encoding)
        print(row_tuple)


def list_arithmetic_expression(session):
    for row in session.query(ArithmeticExpression):
        row_tuple = (row.id, row.expression_encoding)
        print(row_tuple)


def delete_arithmetic_expression(id, expression_encoding, session):
    if id is None:
        id = ArithmeticExpression.id
    if expression_encoding is None:
        expression_encoding = ArithmeticExpression.expression_encoding

    session.query(ArithmeticExpression). \
        filter_by(id=id,
                  expression_encoding=expression_encoding).delete()
    return session


def delete_arithmetic_expression(id, expression_encoding, session):
    if id is None:
        id = ProgrammingExpression.id
    if expression_encoding is None:
        expression_encoding = ProgrammingExpression.expression_encoding

    session.query(ProgrammingExpression). \
        filter_by(id=id,
                  expression_encoding=expression_encoding).delete()
    return session


def get_expressions_from_data_base(session, q):
    expressions = []

    for row in session.query(ArithmeticExpression):
        e = decode_expression(row.expression_encoding)
        expressions.append(e)
    for row in session.query(ProgrammingExpression):
        e = decode_expression(row.expression_encoding)
        expressions.append(e)
    q.put(expressions)
