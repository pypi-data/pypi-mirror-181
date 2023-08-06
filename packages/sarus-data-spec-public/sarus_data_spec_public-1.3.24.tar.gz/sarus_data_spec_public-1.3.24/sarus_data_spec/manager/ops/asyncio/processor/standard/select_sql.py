import typing as t

import pyarrow as pa

from sarus_data_spec.arrow.type import type_from_arrow
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.asyncio.utils import async_iter
import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st


async def select_sql_to_arrow(
    dataset: st.Dataset, query: str, batch_size: int
) -> t.AsyncIterator[pa.RecordBatch]:
    """
    Pyarrow batches from results of an SQL query
    executed on the parent dataset
    """
    # TODO: Adapt when dataset.sql will return an arrow iterator with
    # the schema inferred from sqlalchemy results.
    parent_ds_id = dataset.protobuf().spec.transformed.arguments[0]
    parent_ds = t.cast(Dataset, dataset.storage().referrable(parent_ds_id))
    res = pa.Table.from_pylist(parent_ds.sql(query))
    if len(res) == 0:
        raise RuntimeError(
            f"SQL query: '{query}' without any result is not supported."
        )
    batches = res.to_batches(batch_size)
    return async_iter(batches)


def select_sql_schema(dataset: st.Dataset, query: str) -> sdt.Type:
    """
    Schema computed by inferring results of an SQL query
    executed on the parent dataset
    """
    # TODO: Adapt when dataset.sql will return an arrow iterator with
    # the schema inferred from sqlalchemy results.
    res_table = pa.Table.from_pylist(dataset.sql(query))
    if len(res_table) == 0:
        raise RuntimeError(
            f"SQL query: '{query}' without any result is not supported."
        )
    fields = {
        col: type_from_arrow(
            arrow_type=res_table.field(col).type,
            nullable=res_table.field(col).nullable,
        )
        for col in res_table.schema.names
    }

    return sdt.Struct(fields=fields)
