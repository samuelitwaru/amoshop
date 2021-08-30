from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from app import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
# engine = create_engine('sqlite:///:memory:', echo=True)
# engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    description = Column(String, nullable=False)
    barcode = Column(String, unique=True)
    quantity = Column(Integer, nullable=False, default=0)
    units = Column(String, nullable=False)
    buying_price = Column(Integer, nullable=False)
    selling_price = Column(Integer, nullable=False)


# 	stock = relationship("Stock", backref="product")
# 	sales = relationship("Sale", backref="product")


# class Stock(Base):
# 	__tablename__ = 'stock'
# 	id = Column(Integer, primary_key=True)
# 	quantity = Column(Integer, nullable=False)
# 	product_id = Column(Integer, ForeignKey("products.id"))


# class Sale(Base):
# 	__tablename__ = 'sales'
# 	id = Column(Integer, primary_key=True)
# 	quantity = Column(Integer, nullable=False)
# 	buying_price = Column(Integer, nullable=False)
# 	selling_price = Column(Integer, nullable=False)
# 	product_id = Column(Integer, ForeignKey("products.id"))
# 	sale_group_id = Column(Integer, ForeignKey("sale_groups.id"))


# class SaleGroup(Base):
# 	__tablename__ = 'sale_groups'
# 	id = Column(Integer, primary_key=True)
# 	amount = Column(Integer, nullable=False)
# 	paid = Column(Integer, nullable=False)
# 	sales = relationship("Sale", backref="sale")

session = scoped_session(sessionmaker(bind=engine))


def create_db():
    Base.metadata.create_all(bind=engine)
