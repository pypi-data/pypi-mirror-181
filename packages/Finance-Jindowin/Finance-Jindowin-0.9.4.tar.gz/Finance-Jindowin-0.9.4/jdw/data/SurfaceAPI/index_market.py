# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sqlalchemy import select, and_
from jdw.data.SurfaceAPI.engine import FetchKDEngine


class IndexMarket(object):

    def __init__(self):
        self._engine = FetchKDEngine()
        self._table_model = self._engine.table_model('index_market')

    def yields(self, start_date, end_date, index_code, offset=0):
        query = select([
            self._table_model.trade_date, self._table_model.indexCode,
            self._table_model.chgPct.label('returns')
        ]).where(
            and_(self._table_model.trade_date.between(start_date, end_date),
                 self._table_model.indexCode == index_code)).order_by(
                     self._table_model.trade_date, self._table_model.indexCode)

        market = pd.read_sql(query, self._engine.client())
        if offset > 0:
            market = market.sort_values(
                by=['trade_date']).set_index('trade_date').shift(offset)
            market = market.reset_index()
        return market
