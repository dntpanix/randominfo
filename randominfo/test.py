from faker import Faker

fake = Faker()

person = {
    "full_name": fake.name(),
    "gender": fake.random_element(["Male", "Female"]),
    "country": fake.country(),
    "address": fake.address(),
}

print(person["full_name"], person["gender"], person["country"], person["address"])
