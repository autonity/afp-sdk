from afp.schemas import Model


class Person(Model):
    first_name: str
    last_name: str


def test_schema_aliasing__from_json():
    person = Person.model_validate_json('{"firstName":"Foo","lastName":"Bar"}')
    assert person.first_name == "Foo"
    assert person.last_name == "Bar"


def test_schema_aliasing__to_json():
    person = Person(first_name="Foo", last_name="Bar")
    assert person.model_dump_json() == '{"firstName":"Foo","lastName":"Bar"}'
