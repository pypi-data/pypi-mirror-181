# -*- coding: utf-8 -*-
from jdw.data.SurfaceAPI.yields import Yields


class FutYields(Yields):

    def __init__(self):
        super().__init__(table_name='fut_derived_yields')