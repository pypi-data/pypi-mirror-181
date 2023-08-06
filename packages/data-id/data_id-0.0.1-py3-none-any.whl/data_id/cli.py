import rich

from .api import scan_table
from .results_database import get_results_db


def review_results():
    results_db = get_results_db()
    for result in results_db.get_results():
        # Ask user to review the result
        answer = input(f"{result}. Is this correct? [y/n]")
        try:
            review = list("ny").index(answer.lower())
        except IndexError:
            rich.print("Answer must be 'y' or 'n'.")

        assert review in (0, 1)

        result.update_confidence(review)

        # TODO refresh results?


def scan(database, tables):
    for table in tables:
        scan_table(database, table)

    for r in get_results_db.get_new_results():
        rich.print(r)
