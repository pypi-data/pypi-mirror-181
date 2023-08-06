from typing import Union, Sequence, List

from runtype import dataclass
from data_diff.sqeleton.queries.ast_classes import TablePath
from data_diff.sqeleton.databases import Database

from .abcs import Scanner, ScanResult
from .schema_scanners import SchemaScanner_Regex
from .data_scanners import DataSampleScanner_CommonRegex, DataQueryScanner_CommonRegex
from .results_database import get_results_db

DEFAULT_SAMPLE_SIZE = 1024

DEFAULT_SCANNERS = [
    SchemaScanner_Regex(),
    DataQueryScanner_CommonRegex(),
    DataSampleScanner_CommonRegex(DEFAULT_SAMPLE_SIZE),
]


@dataclass
class ScanResults:
    results: List[ScanResult]


def scan_table(
    db: Database, table: Union[str, TablePath], *, scanners: Sequence[Scanner] = DEFAULT_SCANNERS
) -> Sequence[ScanResult]:
    tbl = TablePath.cast_from(table).with_schema()
    results = {s: ScanResults(list(s.scan_table(db, tbl))) for s in scanners}
    get_results_db().add_results(results)
    return results
