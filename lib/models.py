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



class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', back_populates='customer')
    restaurants = association_proxy('reviews', 'restaurant',
        creator=lambda re: Review(restaurant = re))

    def __repr__ (self):
        return f"First-name:: {self.first_name}, Lastname: {self.last_name}"
    
    def reviews(self):
        return session.query(Review).filter_by(customer_id=self.id).all()

    def restaurants(self):
        reviews = self.reviews()
        return [review.restaurant() for review in reviews]

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def favorite_restaurant(self):
        # Assuming you have a relationship between Customer and Review through 'reviews'
        reviews = self.reviews
        if reviews:
            highest_rated_review = max(reviews, key=lambda review: review.star_rating)
            return highest_rated_review.restaurant
        return None

    def add_review(self, restaurant, rating):
        new_review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        # Assuming you have a relationship between Customer and Review through 'reviews'
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()


class Review(Base):
    __tablename__ = 'reviews'

    id=Column(Integer(), primary_key=True)
    star_rating=Column(Integer())
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')


    def __repr__(self):
        return f"id={self.id}, rating = {self.star_rating} customer={self.customer_id} for restaurant::{self.restaurant_id}"

    def customer(self):
        return session.query(Customer).filter_by(id=self.customer_id).first()

    def restaurant(self):
        return session.query(Restaurant).filter_by(id=self.restaurant_id).first()

    def full_review(self):
        return f'Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars.'


