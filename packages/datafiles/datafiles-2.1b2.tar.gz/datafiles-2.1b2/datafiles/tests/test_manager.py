# pylint: disable=unused-variable

import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from unittest.mock import patch

import pytest

from datafiles.manager import Manager
from datafiles.model import create_model


@dataclass
class Nested:
    name: str


@dataclass
class MyClass:
    foo: int
    bar: int
    nested: Optional[Nested] = None


def describe_manager():
    @pytest.fixture
    def manager():
        shutil.rmtree(Path(__file__).parent / "files", ignore_errors=True)
        model = create_model(MyClass, pattern="files/{self.foo}.yml")
        return Manager(model)

    @pytest.fixture
    def manager_home():
        model = create_model(Nested, pattern="~/.{self.name}.json")
        return Manager(model)

    def describe_get_or_none():
        @patch("datafiles.mapper.Mapper.load")
        @patch("datafiles.mapper.Mapper.exists", True)
        @patch("datafiles.mapper.Mapper.modified", False)
        def when_file_exists(mock_load, expect, manager):
            expect(manager.get_or_none(foo=1, bar=2)) == MyClass(foo=1, bar=2)
            expect(mock_load.called).is_(True)

        @patch("datafiles.mapper.Mapper.exists", False)
        def when_file_missing(expect, manager):
            expect(manager.get_or_none(foo=3, bar=4)).is_(None)

        def when_file_corrupt(expect, manager):
            instance = manager.get_or_create(foo=2, bar=1)
            instance.datafile.path.write_text("{")
            instance2 = manager.get_or_none(foo=2, bar=2)
            expect(instance2).is_(None)
            expect(instance.datafile.path.is_file()).is_(False)

    def describe_get_or_create():
        @patch("datafiles.mapper.Mapper.save")
        @patch("datafiles.mapper.Mapper.load")
        @patch("datafiles.mapper.Mapper.exists", True)
        @patch("datafiles.mapper.Mapper.modified", False)
        def when_file_exists(mock_save, mock_load, expect, manager):
            expect(manager.get_or_create(foo=1, bar=2)) == MyClass(foo=1, bar=2)
            expect(mock_save.called).is_(True)
            expect(mock_load.called).is_(False)

        @patch("datafiles.mapper.Mapper.save")
        @patch("datafiles.mapper.Mapper.load")
        @patch("datafiles.mapper.Mapper.exists", False)
        def when_file_missing(mock_save, mock_load, expect, manager):
            expect(manager.get_or_create(foo=1, bar=2)) == MyClass(foo=1, bar=2)
            expect(mock_save.called).is_(True)
            expect(mock_load.called).is_(True)

        def when_file_corrupt(expect, manager):
            instance = manager.get_or_create(foo=2, bar=1)
            instance.datafile.path.write_text("{")
            instance2 = manager.get_or_create(foo=2, bar=2)
            expect(instance2.bar) == 2

    def describe_all():
        @patch("datafiles.mapper.Mapper.exists", False)
        def when_no_files_exist(expect, manager):
            items = list(manager.all())
            expect(items) == []

        def with_home_directory(expect, manager_home):
            items = list(manager_home.all())
            if "CI" not in os.environ:
                expect(len(items)) > 0

    def describe_filter():
        @patch("datafiles.mapper.Mapper.exists", False)
        def when_no_files_exist(expect, manager):
            items = list(manager.filter())
            expect(items) == []

        @patch("datafiles.mapper.Mapper.exists", False)
        def with_partial_positional_arguments(expect, manager):
            items = list(manager.filter(foo=1))
            expect(items) == []

        @patch("datafiles.mapper.Mapper.exists", False)
        def with_nested_key_query(expect, manager):
            items = list(manager.filter(nested__name="John Doe"))
            expect(items) == []
