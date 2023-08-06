import copy
import re

from .base import BaseAPI, strip_html_tags
from .exceptions import DataException, SymbolNotFound


class EtfDb(BaseAPI):
    """
    EtfDb.com
    """

    def get_basic_info(self):
        """
        Returns basic info about the given ETF. The info is:

        - Issuer
        - Brand
        - Structure
        - Expense Ratio
        - Inception
        - Index Tracked
        - Category
        - Leveraged
        - Asset Class
        - Asset Class Size
        - Region (General)
        - Region (Specific)
        - Description

        :return: ETF basic info as a dict.
        :rtype: dict
        """

        # Get HTML.
        try:
            html = self._get(
                f"https://etfdb.com/etf/{self.symbol.upper()}/#etf-ticker-profile"
            )
        except Exception as e:
            raise SymbolNotFound from e

        finds = re.findall(
            r"class=\'ticker-assets\'.*?>(.*?)</div>[^<]*</div>", html.text, re.DOTALL
        )

        # Check if the HTML contains only two occurrences.
        if 0 == len(finds):
            raise SymbolNotFound
        if 2 < len(finds):
            raise DataException(
                "More that two occurrences found in HTML - don't know what to do now"
            )

        # Process 1st list.
        list_items = re.findall(r"<span.*?>(.*?)</span>", finds[0], re.DOTALL)
        list_items = [strip_html_tags(i) for i in list_items]
        data = dict(zip(list_items[::2], list_items[1::2]))

        # Process 2nd list.
        list_items = re.findall(r"<span.*?>(.*?)</span>", finds[1], re.DOTALL)
        list_items = [strip_html_tags(i) for i in list_items]
        data |= dict(zip(list_items[::2], list_items[1::2]))

        for key in copy.deepcopy(data).keys():
            if key not in [
                "Issuer",
                "Brand",
                "Structure",
                "Expense Ratio",
                "Inception",
                "Index Tracked",
                "Category",
                "Leveraged",
                "Asset Class",
                "Asset Class Size",
                "Region (General)",
                "Region (Specific)",
            ]:
                del data[key]

        # Fetch description.
        finds = re.findall(
            r"id='analyst-report'>.*?<p><p><p>(.+?)</p>", html.text, re.DOTALL
        )

        # Check if the HTML contains only ine occurrences.
        if 0 == len(finds):
            raise SymbolNotFound
        if 1 < len(finds):
            raise DataException(
                "More that two occurrences found in HTML - don't know what to do now"
            )

        data["Description"] = strip_html_tags(finds[0])

        return data
