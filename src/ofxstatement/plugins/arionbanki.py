from ofxstatement.plugin import Plugin
from ofxstatement.parser import StatementParser
from ofxstatement.statement import StatementLine, Statement
import xml.etree.ElementTree as ET
from datetime import datetime

class ArionBankiPlugin(Plugin):
    """Arionbanki plugin"""

    def get_parser(self, filename):
        return ArionBankiParser(filename)


class ArionBankiParser(StatementParser):
    """Arionbanki parser"""
    def __init__(self, filename):
        self.statement = Statement()
        self.filename = filename
        self.tree = None

    def parse(self):
        """Main entry point for parsers

        super() implementation will call to split_records and parse_record to
        process the file.
        """
        with open(self.filename, encoding="latin-1") as arionfile:
            self.tree = ET.parse(arionfile)
        return super(ArionBankiParser, self).parse()

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """
        root = self.tree.getroot()
        self.statement.account_id = root[0][0].text
        return root[1:-1]

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """
        tags = {element.tag: element.text for element in line}
        record_id = tags['Tilvisun']
        date = datetime.strptime(tags['Dagsetning'], "%d.%m.%Y %H:%M:%S")
        memo = tags['Skyring']
        amount = float(tags['Upphaed'].replace('.', '').replace(',', '.'))
        return StatementLine(record_id, date, memo, amount)
