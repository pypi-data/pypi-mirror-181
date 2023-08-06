import re
from typing import Iterable

from runtype import dataclass
from data_diff.sqeleton.queries.ast_classes import TablePath
from data_diff.sqeleton.databases import Database

from .abcs import SchemaScanner, SchemaScanResult


def compile_regex_dict(d):
    return {k: re.compile(v) for k, v in d.items()}


@dataclass
class ItemResult:
    column_name: str
    category: str


class SchemaScanner_Regex(SchemaScanner):
    # Adapted from PII Catcher
    regex = {
        "Person": "^.*(firstname|fname|lastname|lname|fullname|maidenname|_name|nickname|name_suffix|name).*$",
        "Email": "^.*(email|e-mail|mail).*$",
        "BirthDate": "^.*(date_of_birth|dateofbirth|dob|birthday|date_of_death|dateofdeath).*$",
        "Gender": "^.*(gender).*$)",
        "Nationality": "^.*(nationality).*$",
        "Address": "^.*(address|city|state|county|country|zipcode|postal|zone|borough).*$",
        "UserName": "^.*user(id|name|).*$",
        "Password": "^.*(pass|password).*$",
        "SSN": "^.*(ssn|social).*$",
    }

    def scan_column_names(self, col_names):
        for col_name in col_names:
            for cat, regex in self.regex.items():
                m = regex.match(col_name)
                if m is not None:
                    # TODO adjust confidence based on heuristics
                    yield SchemaScanResult(col_name, cat, 1.0)

    def scan_table(self, db: Database, table_path: TablePath) -> Iterable[SchemaScanResult]:
        column_names = table_path.with_schema(db).schema.keys()
        return self.scan_column_names(column_names)
