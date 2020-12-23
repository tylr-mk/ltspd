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
from typing import Union, List


import attr


@attr.s(auto_attribs=True, frozen=True)
class IdxSchemaPointer:

    true_id: [int]
    attributes: List[int]
    dimensions: List[int]


@attr.s(auto_attribs=True, frozen=True)
class NameSchemaPointer(IdxSchemaPointer):

    true_id: str
    attributes: List[str]
    dimensions: List[str]


@attr.s(auto_attribs=True, frozen=True)
class Field:

    idx: int
    key: str
    name: str

    @classmethod
    def basic(cls, idx, name):
        return cls(idx=idx, key=name, name=name,)


@attr.s(auto_attribs=True, frozen=True)
class Value:

    field: Field
    val: str


@attr.s(auto_attribs=True, frozen=True)
class OrdinalValue:

    order: int


@attr.s(auto_attribs=True, frozen=True)
class NumericValue(Value):

    val: Union[int, float]


@attr.s(auto_attribs=True, frozen=True)
class IntValue(NumericValue):

    val: int


@attr.s(auto_attribs=True, frozen=True)
class FloatValue(NumericValue):

    val: float


@attr.s(auto_attribs=True, frozen=True)
class Schema:

    true_id: Field
    attributes: List[Field]
    dimensions: List[Field]

    @classmethod
    def from_pointer(cls, schema_pointer, source):
        return cls(
            true_id=Field.basic(schema_pointer.true_id, source[schema_pointer.true_id[0]]),
            attributes=[
                Field.basic(idx, source[idx]) for idx in schema_pointer.attributes
            ],
            dimensions=[
                Field.basic(idx, source[idx]) for idx in schema_pointer.dimensions
            ],
        )


def _assemble_row(row, indices):
    # import ipdb; ipdb.set_trace()
    return [row[idx] for idx in indices]


@attr.s(auto_attribs=True, frozen=True)
class Row:

    values: List[Value]

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


@attr.s(auto_attribs=True, frozen=True)
class DataSet:

    schema: Schema
    dataset: List[Row]



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
# from typing import Union, List


# import attr
# from pyarrow import Table


# @attr.s(auto_attribs=True, frozen=True)
# class NameSchemaPointer(IdxSchemaPointer):

#     true_id: str
#     dimensions: List[str]


# @attr.s(auto_attribs=True, frozen=True)
# class Field:

#     idx: int
#     key: str
#     name: str

#     @classmethod
#     def basic(cls, idx, name):
#         return cls(idx=idx, key=name, name=name,)


# @attr.s(auto_attribs=True, frozen=True)
# class Schema:

#     true_id: Field
#     dimensions: List[Field]

#     @classmethod
#     def from_pointer(cls, schema_pointer, source):
#         return cls(
#             true_id=Field.basic(schema_pointer.true_id, source[schema_pointer.true_id]),
#             dimensions=[
#                 Field.basic(idx, source[idx]) for idx in schema_pointer.dimensions
#             ],
#         )


# class DataSet:

#     schema: Schema
#     dataset: Table
