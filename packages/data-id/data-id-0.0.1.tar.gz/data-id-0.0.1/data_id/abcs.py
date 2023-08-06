from abc import ABC, abstractmethod
from typing import Set, Iterable

from runtype import dataclass
from data_diff.sqeleton.databases import Database
from data_diff.sqeleton.queries.ast_classes import TablePath


@dataclass
class ScanResult:
    column_name: str
    category: str
    confidence: float


class Scanner(ABC):
    # TODO: TablePath_WithSchema
    @abstractmethod
    def scan_table(self, db: Database, table_path: TablePath) -> ScanResult:
        ...


@dataclass
class SchemaScanResult(ScanResult):
    ...


class SchemaScanner(Scanner):
    "Scan the schema of the table"

    @abstractmethod
    def scan_table(self, db: Database, table_path: TablePath) -> Iterable[SchemaScanResult]:
        ...


@dataclass
class DataScanResult(ScanResult):
    ...
    detected_values: Set[str]
    scanned_text: str


class DataScanner(Scanner):
    @abstractmethod
    def scan_table(self, db: Database, table_path: TablePath) -> Iterable[DataScanResult]:
        ...
