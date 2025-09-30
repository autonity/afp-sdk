from afp.schemas import Model, PaginationFilter


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


def test_pagination_parameters__conversion():
    filter = PaginationFilter(batch=2, batch_size=20, newest_first=False)
    assert filter.model_dump() == {
        "page": 2,
        "page_size": 20,
        "sort": "ASC",
    }


def test_pagination_parameters__null_values():
    filter = PaginationFilter(batch=None, batch_size=None, newest_first=None)
    assert filter.model_dump(exclude_none=True) == {}
