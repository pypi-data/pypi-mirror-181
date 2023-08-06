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
from typing import List

from sqlalchemy.orm.exc import NoResultFound

from eva.catalog.catalog_type import TableType
from eva.catalog.models.df_metadata import DataFrameMetadata
from eva.catalog.services.base_service import BaseService
from eva.utils.errors import CatalogError
from eva.utils.logging_manager import logger


class DatasetService(BaseService):
    def __init__(self):
        super().__init__(DataFrameMetadata)

    def create_dataset(
        self, name: str, file_url: str, identifier_id, table_type: TableType
    ) -> DataFrameMetadata:
        """
        Create a new dataset entry for given name and file URL.
        Arguments:
            name (str): name of the dataset
            file_url (str): file path of the dataset.
            table_type (TableType): type of data in the table
        Returns:
            DataFrameMetadata object
        """
        try:
            metadata = self.model(
                name=name,
                file_url=file_url,
                identifier_id=identifier_id,
                table_type=int(table_type),
            )
            metadata = metadata.save()
        except Exception as e:
            logger.exception(
                f"Failed to create catalog dataset with exception {str(e)}"
            )
            raise CatalogError(e)
        else:
            return metadata

    def dataset_by_name(self, name: str) -> int:
        """
        Returns metadata id for the name queried

        Arguments:
            name (str)- Name for which id is required

        Returns:
            int (dataset id)
        """
        try:
            result = (
                self.model.query.with_entities(self.model._id)
                .filter(self.model._name == name)
                .one()
            )
            return result[0]
        except NoResultFound:
            logger.error("get_id_from_name failed with name {}".format(name))

    def dataset_by_id(self, dataset_id) -> DataFrameMetadata:
        """
        Returns the dataset by ID
        Arguments:
            dataset_id (int)
        Returns:
           DataFrameMetadata
        """
        return self.model.query.filter(self.model._id == dataset_id).one()

    def dataset_object_by_name(
        self, database_name, dataset_name, column_name: List[str] = None
    ):
        """
        Get the metadata for the given table.
        Arguments:
            database_name  (str): Database to which dataset belongs # TODO:
            use this field
            dataset_name (str): name of the dataset
            column_name (List[str]): list of columns for the  dataset which
            need be listed. If not specified, all columns will be retrieved
            # TODO:  perform column filtering when column_name not None
        Returns:
            DataFrameMetadata - metadata for given dataset_name
        """
        return self.model.query.filter(self.model._name == dataset_name).one_or_none()

    def drop_dataset(self, dataset: DataFrameMetadata):
        """Delete dataset from the db
        Arguments:
            dataset  (DataFrameMetadata): dataset to delete
        Returns:
            True if successfully removed else false
        """
        try:
            dataset.delete()
            return True
        except Exception as e:
            err_msg = f"Delete dataset failed for {dataset} with error {str(e)}."
            logger.exception(err_msg)
            raise CatalogError(err_msg)

    def rename_dataset(self, dataset: DataFrameMetadata, new_name: str):
        try:
            dataset.update(_name=new_name)
        except Exception as e:
            err_msg = "Update dataset name failed for {} with error {}".format(
                dataset.name, str(e)
            )
            logger.error(err_msg)
            raise RuntimeError(err_msg)
