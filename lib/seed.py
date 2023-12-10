from faker import Faker
import random
import ipdb  # Import ipdb here
from models import session, Restaurant, Customer, Review

if __name__ == '__main__':
    ipdb.set_trace()
    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()

    fake = Faker()

    restaurants = []
    for j in range(50):
        restaurant = Restaurant(
            name=fake.unique.company(),
            price=random.randint(1000, 50000)
        )

        session.add(restaurant)
        restaurants.append(restaurant)
        session.commit()

    customers = []
    for i in range(50):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )

        session.add(customer)
        customers.append(customer)

        session.commit()

    reviews = []
    star_ratings = [0, 1, 2, 3, 4, 5]

    for restaurant in restaurants:
        for i in range(random.randint(1, 50)):
            customer = random.choice(customers)

            star_rating = random.choice(star_ratings)
            print(f"Star Rating: {star_rating}")

            review = Review(
                star_rating=star_rating,
                restaurant_id=restaurant.id,
                customer_id=customer.id
            )
            reviews.append(review)

    session.add_all(reviews)
    session.commit()
    session.close()
