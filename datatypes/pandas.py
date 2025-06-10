from vault.datatype import Wrapper
from enum import Enum
import pandas as pd
import io


class PandasFileFormat(Enum):
    # Better for long-term storage, compatibility with lots of langauges/ecosystems
    PARQUET = (1,)
    # Same as PARQUET, but using `snappy` compression
    PARQUET_COMPRESSED = (2,)
    # Faster binary format, less accurate (might have issues with complex nested structures)
    FEATHER = (3,)


class DataframeWrapper(Wrapper):
    def __init__(
        self,
        data: pd.DataFrame,
        pandas_format: PandasFileFormat = PandasFileFormat.PARQUET,
    ):
        self.data: pd.DataFrame = data
        self.pandas_format: PandasFileFormat = pandas_format

    def _dump(self) -> bytes:
        if self.pandas_format == PandasFileFormat.PARQUET:
            buffer = io.BytesIO()
            self.data.to_parquet(buffer)
            return buffer.getvalue()
        elif self.pandas_format == PandasFileFormat.PARQUET_COMPRESSED:
            buffer = io.BytesIO()
            self.data.to_parquet(buffer, compression="snappy")
            return buffer.getvalue()
        elif self.pandas_format == PandasFileFormat.FEATHER:
            buffer = io.BytesIO()
            self.data.to_feather(buffer)
            return buffer.getvalue()
        else:
            raise Exception(
                "Incompatible PandasFileFormat: {0}".format(self.pandas_format)
            )

    def _load(
        raw: bytes, pandas_format: PandasFileFormat = PandasFileFormat.PARQUET
    ) -> DataframeWrapper:
        if self.pandas_format == PandasFileFormat.PARQUET:
            data = pd.read_parquet(io.BytesIO(raw))
            return DataframeWrapper(data, pandas_format)
        elif self.pandas_format == PandasFileFormat.PARQUET_COMPRESSED:
            # The same as .PARQUET, Pandas should understand by the data's headers what compressions alghorithm is used
            data = pd.read_parquet(io.BytesIO(raw))
            return DataframeWrapper(data, pandas_format)
        elif self.pandas_format == PandasFileFormat.FEATHER:
            passdata = pd.read_feather(io.BytesIO(raw))
            return DataframeWrapper(data, pandas_format)
        else:
            raise Exception(
                "Incompatible PandasFileFormat: {0}".format(self.pandas_format)
            )
