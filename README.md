# ltspd

Rosters, schedules and leagues: pseudo-randomly group participants into
activities, with support for exclusions, mixed-size resources (rooms, tables,
taxis), proportional mixing across subgroups, and league/round-robin generation.

## Layout

```
src/ltspd/
  rosters/     # random, mixed-size and multi-group roster generators (+ retry/exclusion decorators)
  schedules/   # leagues and schedule expansion
  utils/       # grouping, mixing, refining and expansion primitives
  models.py    # attrs models for inventory, attendees and reservations
  exchange/    # schema/row/dataset models for tabular input
  io/          # CSV input
tests/
```

## Development

Tooling is managed by [mise](https://mise.jdx.dev) and [uv](https://docs.astral.sh/uv/).

```sh
mise install        # python 3.14 + uv
mise run sync       # uv sync → .venv
mise run test       # pytest with coverage
mise run format     # isort + black
mise run lint       # isort/black --check + ruff
mise run check      # lint + test
```

Enable the git hooks (black, isort, ruff, uv-lock) with `pre-commit install`.

## Example

```python
from ltspd.rosters.generators import generate_random_roster

people = list(range(12))
roster = generate_random_roster(people, group_size=3, exclusions={(1, 2), (3, 4)})
# -> iterator of 4 groups of 3, where 1 & 2 and 3 & 4 never share a group
```
