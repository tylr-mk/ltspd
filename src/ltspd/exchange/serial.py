"""Conceptualisations of Data, Again efficiencies

Once in memory / Python, we see the data as sets of iterables inside which
we expect to see the following types of fields:

Attributes

  > True ID >> ID --> Email | Pseudo ID
  > Pseudo ID >> First Name, Last Name
  > Generic >> Contact Details

Dimension
  > Categorical
    - Nominal > [Gender]
    - Ordinal > [Education Level] (Implied Ordering)
  > Numerical
    - Discrete > Age in Years
    - Continuous
    - Interval > [-5 ]
    - Ratio

>>> Calculated ???
>>> Rules


Read a little more here https://towardsdatascience.com/data-types-in-statistics-347e152e8bee
"""

from attrs import frozen


@frozen
class IdxSchemaPointer:
    true_id: list[int]
    attributes: list[int]
    dimensions: list[int]


@frozen
class NameSchemaPointer(IdxSchemaPointer):
    true_id: str
    attributes: list[str]
    dimensions: list[str]


@frozen
class Field:
    idx: int
    key: str
    name: str

    @classmethod
    def basic(cls, idx, name):
        return cls(idx=idx, key=name, name=name)


@frozen
class Value:
    field: Field
    val: str


@frozen
class OrdinalValue:
    order: int


@frozen
class NumericValue(Value):
    val: int | float


@frozen
class IntValue(NumericValue):
    val: int


@frozen
class FloatValue(NumericValue):
    val: float


@frozen
class Schema:
    true_id: Field
    attributes: list[Field]
    dimensions: list[Field]

    @classmethod
    def from_pointer(cls, schema_pointer, source):
        return cls(
            true_id=Field.basic(
                schema_pointer.true_id[0], source[schema_pointer.true_id[0]]
            ),
            attributes=[
                Field.basic(idx, source[idx]) for idx in schema_pointer.attributes
            ],
            dimensions=[
                Field.basic(idx, source[idx]) for idx in schema_pointer.dimensions
            ],
        )


def _assemble_row(row, indices):
    return [row[idx] for idx in indices]


@frozen
class Row:
    values: list[Value]

    @classmethod
    def from_pointer(cls, schema_pointer, row):
        return cls(
            sum(
                [
                    _assemble_row(row, indices)
                    for indices in [
                        schema_pointer.true_id,
                        schema_pointer.attributes,
                        schema_pointer.dimensions,
                    ]
                ],
                [],
            )
        )


@frozen
class DataSet:
    schema: Schema
    dataset: list[Row]
