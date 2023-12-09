from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy import desc
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}    

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


engine = create_engine('sqlite:///restaurants.db')

Session = sessionmaker(bind = engine)
session = Session()



class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price=Column(Integer)

    def __repr__(self):
        return f"name:: {self.name}: price::{self.price}"

    reviews = relationship('Review', back_populates='restaurant')
    customers = association_proxy('reviews', 'customer', 
        creator = lambda cu: Review(customer = cu))

    def reviews(self):
        return session.query(Review).filter_by(restaurant_id=self.id).all()

    def customers(self):
        reviews = self.reviews()
        return [review.customer() for review in reviews]

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(desc(cls.price)).first()

    def all_reviews(self):
        reviews = self.reviews
        review_strings = []
        for review in reviews:
            review_strings.append(review.full_review())
        return review_strings