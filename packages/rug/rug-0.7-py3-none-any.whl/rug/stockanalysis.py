import re

from .base import BaseAPI, HtmlTableParser
from .exceptions import DataException, SymbolNotFound


class StockAnalysis(BaseAPI):
    def get_etf_holdings(self):
        """
        Fetches ETF holdings table with following columns:

        - No.
        - Symbol
        - Name
        - % Weight
        - Shares
        """

        try:
            html = self._get(
                f"https://stockanalysis.com/etf/{self.symbol.lower()}/holdings/"
            )
        except Exception as e:
            raise SymbolNotFound from e

        finds = re.findall(r"<table.*?>.*?</table>", html.text, re.DOTALL)

        # Check if the HTML contains only one table.
        if 0 == len(finds):
            raise SymbolNotFound
        if 1 < len(finds):
            raise DataException(
                "More that one table found in HTML - don't know what to do now"
            )

        parser = HtmlTableParser(columns=5)
        # monkey patch - fixing the case where table header is
        # improperly parsed  - "%" has it's own column and the
        # last "shares" column is then not parsed.
        parser.feed(finds[0])
        parser.data[:6] = ("No.", "Symbol", "Name", "% Weight", "Shares")

        return parser.get_data()
