from faker import Faker
from faker.providers import (
    internet,
    date_time,
    address,
    file,
    lorem,
    user_agent,
    misc,
    BaseProvider,
)
from faker_web import WebProvider
from mdgen import MarkdownPostProvider

Faker.seed(0)
fake = Faker("en_US")
fake.add_provider(internet)
fake.add_provider(date_time)
fake.add_provider(address)
fake.add_provider(file)
fake.add_provider(lorem)
fake.add_provider(user_agent)
fake.add_provider(misc)
fake.add_provider(WebProvider)
fake.add_provider(MarkdownPostProvider)


class EmailAddress(BaseProvider):
    __provider__ = "email_set"

    def email_set(self):
        return f"{fake.name()} <{fake.company_email()}>"


fake.add_provider(EmailAddress)
