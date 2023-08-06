# coding=utf-8
# Copyright 2018-2022 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from eva.catalog.catalog_type import IndexType
from eva.catalog.models.base_model import BaseModel


class IndexMetadata(BaseModel):
    __tablename__ = "index"

    _name = Column("name", String(100), unique=True)
    _save_file_path = Column("save_file_path", String(128))
    _type = Column("type", Enum(IndexType), default=Enum)

    # Secondary index reference.
    _secondary_index_id = Column(
        "secondary_index_id", Integer, ForeignKey("df_metadata._row_id")
    )
    _secondary_index = relationship("DataFrameMetadata")

    # Input feature column reference.
    _feat_df_column_id = Column(
        "df_column_id", Integer, ForeignKey("df_column._row_id")
    )
    _feat_df_column = relationship("DataFrameColumn")

    def __init__(
        self,
        name: str,
        save_file_path: str,
        type: IndexType,
        secondary_index_id: int = None,
        feat_df_column_id: int = None,
    ):
        self._name = name
        self._save_file_path = save_file_path
        self._type = type
        self._secondary_index_id = secondary_index_id
        self._feat_df_column_id = feat_df_column_id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def save_file_path(self):
        return self._save_file_path

    @property
    def type(self):
        return self._type

    @property
    def secondary_index(self):
        return self._secondary_index

    @property
    def feat_df_column(self):
        return self._feat_df_column

    @property
    def secondary_index_id(self):
        return self._secondary_index_id

    @secondary_index_id.setter
    def secondary_index_id(self, value):
        self._secondary_index_id = value

    @property
    def feat_df_column_id(self):
        return self._feat_df_column_id

    @feat_df_column_id.setter
    def feat_df_column_id(self, value):
        self._feat_df_column_id = value

    def __str__(self):
        index_str = "index: ({}, {}, {})\n".format(
            self.name, self.save_file_path, self.type
        )
        return index_str

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.save_file_path == other.save_file_path
            and self.name == other.name
            and self.type == other.type
            and self.secondary_index_id == other.secondary_index_id
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.id,
                self.name,
                self.save_file_path,
                self.type,
                self.secondary_index_id,
            )
        )
