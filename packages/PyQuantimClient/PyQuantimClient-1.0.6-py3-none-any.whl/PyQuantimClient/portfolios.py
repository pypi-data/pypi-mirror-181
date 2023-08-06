# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
from .api import quantim

class portfolios(quantim):
    def __init__(self, username, password, secretpool, env="qa"):
        super().__init__(username, password, secretpool, env)

    def get_portfolios(self, ref_date=None, country=None, fields=None, port_names=None):
        '''
        Get portfolio
        '''
        if country is None and port_names is None:
            raise ValueError('Either country or port_names must be different to None.')
        data = {'date':ref_date, 'country':country, 'fields':fields, 'port_names':port_names}
        resp = self.api_call('query_portfolios', method="post", data=data, verify=False)
        ports_df = pd.DataFrame(resp)
        return ports_df

    def get_portfolios_views(self, ref_date=None, country=None, port_names=None, asset=None):
        '''
        Get portfolio views
        '''
        if country is None and port_names is None:
            raise ValueError('Either country or port_names must be different to None.')
        data = {'date':ref_date, 'country':country, 'port_names':port_names, 'asset':asset}
        resp = self.api_call('query_portfolios_views', method="post", data=data, verify=False)
        ports_df = pd.DataFrame(resp)
        return ports_df