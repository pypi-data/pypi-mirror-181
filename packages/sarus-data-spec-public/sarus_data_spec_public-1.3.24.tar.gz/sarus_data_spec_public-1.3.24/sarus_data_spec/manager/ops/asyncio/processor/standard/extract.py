from typing import AsyncIterator, cast

import pyarrow as pa

import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


async def arrow_extract(
    dataset: st.Dataset, batch_size: int
) -> AsyncIterator[pa.RecordBatch]:
    """Implementation of the extract transform
    At the moment is takes the full dataset
    """
    args, kwargs = dataset.parents()
    parents = args + list(kwargs.values())
    assert len(parents) == 1
    (parent,) = parents
    assert parent.prototype() == sp.Dataset
    ds_parent = cast(st.Dataset, parent)
    return await ds_parent.async_to_arrow()
