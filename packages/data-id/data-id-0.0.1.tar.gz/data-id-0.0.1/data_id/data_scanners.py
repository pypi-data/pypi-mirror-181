import logging
from typing import Set, Iterable, Tuple

from runtype import dataclass

# TODO - use commonregex-improved instead (https://github.com/brootware/commonregex-improved)
import crim

from .abcs import DataScanner, DataScanResult, Database, TablePath, abstractmethod
from .utils import zips


logger = logging.getLogger(__name__)


@dataclass
class DataQueryScanner(DataScanner):
    pass


@dataclass
class DataSampleScanner(DataScanner):
    "Scan the data of a random sample of the table"

    sample_size: int

    def scan_table(self, db: Database, table_path: TablePath) -> DataScanResult:

        rows = db.query(table_path.sample(self.sample_size))

        for row in rows:
            for col_name, value in zips(table_path.schema.keys(), row):
                text = str(value)
                for cat, detected_values in self.scan_item(text):
                    yield DataScanResult(col_name, cat, detected_values, text)

    @abstractmethod
    def scan_item(self, item: str) -> Iterable[Tuple[str, Set[str]]]:
        ...


COMMON_REGEXES = {
    crim.phone: "Phone",
    crim.phones_with_exts: "Phone",
    crim.email: "Email",
    crim.ip_pattern: "IP",
    crim.credit_card: "Credit Card",
    crim.street_address: "Address",
    crim.btc_address: "BTC Address",
    crim.po_box: "Address",
    crim.ssn: "SSN",
    crim.iban_number: "IBAN",
    crim.mac_address: "MAC Address",
}


class DataSampleScanner_CommonRegex(DataSampleScanner):
    """A scanner that uses the commonregex package"""

    # A dict to map commonregex attribute to PII category

    def scan_item(self, item: str) -> Iterable[Tuple[str, Set[str]]]:
        """Scan the text and return all the types of info found, with their respective values"""

        for regex, cat in COMMON_REGEXES.items():
            detected_values = crim.match(item, regex)
            yield cat, set(detected_values)


class DataQueryScanner_CommonRegex(DataQueryScanner):
    regexes_by_type = {
        int: {k: v for k, v in COMMON_REGEXES.items() if v in ("Phone", "Credit Card")},
        str: COMMON_REGEXES,
    }

    def scan_table(self, db: Database, table_path: TablePath) -> Iterable[DataScanResult]:
        if not db.SUPPORTS_REGEX:
            logger.info("Skipping regex query scan, because database %s doesn't support regexes", db)
            return

        # For each column, by type, collect a list of appropriate regexes
        regexes_by_col = {col_name: self.regexes_by_type[col_type] for col_name, col_type in table_path.schema}

        # Query column values
        q = table_path.where(or_(col.like(regex(r)) for col, r in regexes_by_col.items()))
        rows = db.query(q)

        ds = DataSampleScanner_CommonRegex(0)
        for row in rows:
            for col_name, value in zips(table_path.schema.keys(), row):
                text = str(value)
                for cat, detected_values in ds.scan_item(text):
                    yield DataScanResult(col_name, cat, detected_values, text)
