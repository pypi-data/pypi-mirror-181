import requests
from bs4 import BeautifulSoup as bs

from .base import FilingBase

class Filing(FilingBase):

    def get_13f_filing(self, qtr_year):
        return self.get_filing(qtr_year)

    @property
    def latest_13f_filing(self):
        return self.get_latest_filing()
    
    @property
    def latest_13f_filing_detailed(self):
        return self.get_latest_filing(simplified=False)

    @property
    def latest_13f_filing_cover_page(self):
        return self.get_latest_filing_cover_page()