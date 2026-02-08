"""Tests for osm_objects._base helper functions."""

from __future__ import annotations

import pandas as pd

from openstudio_toolkit.osm_objects._base import build_dataframe


class TestBuildDataframe:
    def test_empty_list(self):
        df = build_dataframe([], "Space")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_sorts_by_name(self):
        dicts = [
            {"Handle": "c", "Name": "Zulu"},
            {"Handle": "a", "Name": "Alpha"},
            {"Handle": "b", "Name": "Mike"},
        ]
        df = build_dataframe(dicts, "Test")
        assert list(df["Name"]) == ["Alpha", "Mike", "Zulu"]
        assert list(df.index) == [0, 1, 2]

    def test_no_name_column(self):
        dicts = [{"Handle": "a", "Value": 1}, {"Handle": "b", "Value": 2}]
        df = build_dataframe(dicts, "NoName")
        assert len(df) == 2
        # No sorting applied, just returned as-is
        assert df.iloc[0]["Handle"] == "a"

    def test_custom_sort_column(self):
        dicts = [
            {"Handle": "a", "Name": "A", "Area": 300},
            {"Handle": "b", "Name": "B", "Area": 100},
        ]
        df = build_dataframe(dicts, "Test", sort_by="Area")
        assert df.iloc[0]["Area"] == 100
