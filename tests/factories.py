from factory import Factory, Faker, LazyFunction, LazyAttribute
import random

fake = Faker._get_faker()

class ClientFactory(Factory):
    class Meta:
        model = dict

    name = Faker('first_name')
    surname = Faker('last_name')
    credit_card = LazyFunction(lambda: random.choice([None, fake.credit_card_number()]))
    car_number = Faker('license_plate')


class ParkingFactory(Factory):
    class Meta:
        model = dict

    address = Faker('address')
    opened = LazyAttribute(lambda x: random.choice([True, False]))
    count_places = Faker('random_int', min=1, max=100)
    count_available_places = LazyAttribute(lambda o: o.count_places)


