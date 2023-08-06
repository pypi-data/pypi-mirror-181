# -*- coding: utf-8 -*-
from jdw.data.SurfaceAPI.yields import Yields


class StkYields(Yields):

    def __init__(self):
        super().__init__(table_name='stk_derived_yields')