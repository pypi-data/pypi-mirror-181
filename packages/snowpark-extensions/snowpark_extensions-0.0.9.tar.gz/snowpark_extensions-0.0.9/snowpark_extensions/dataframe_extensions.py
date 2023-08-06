from snowflake.snowpark import DataFrame, Row, DataFrameNaFunctions
from snowflake.snowpark.functions import col, lit, udtf, regexp_replace
from snowflake.snowpark import functions as F
import pandas as pd
import numpy as np
from snowpark_extensions.utils import map_to_python_type, schema_str_to_schema
import shortuuid
from snowflake.snowpark.types import StructType,StructField
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
    overload,
)
from snowflake.snowpark._internal.type_utils import (
    ColumnOrName,
    ColumnOrSqlExpr,
    LiteralType,
)

if not hasattr(DataFrame,"___extended"):
    DataFrame.___extended = True
    def get_dtypes(schema):
        data = np.array([map_to_python_type(x.datatype) for x in schema.fields])
        # providing an index
        dtypes_series = pd.Series(data, index=schema.names)
        return dtypes_series

    DataFrame.dtypes = property(lambda self: get_dtypes(self.schema))


    def map(self,func,output_types,input_types=None,input_cols=None,to_row=False):
        clazz="map"+shortuuid.uuid()[:8]
        output_schema=[]
        if not input_types:
            input_types = [x.datatype for x in self.schema.fields]
        input_cols_len=len(input_types)
        if not input_cols:
            input_col_names=self.columns[:input_cols_len] 
            _input_cols = [self[x] for x in input_col_names]
        else:
            input_col_names=input_cols
            _input_cols = input_cols
        output_schema = [StructField(f"c_{i+1}",output_types[i]) for i in range(len(output_types))]
        output_cols = [col(x.name) for x in output_schema]
        if to_row:
            myRow = Row(*input_col_names)
            def process_func(self,*argv):
                yield func(myRow(*argv))
        else:
            def process_func(self,*argv):
                yield func(*argv)
        udtf_class = type(clazz, (object, ), {"process":process_func})
        udtf(udtf_class,output_schema=StructType(output_schema), input_types=input_types,name=clazz,replace=True,packages=["snowflake-snowpark-python"])
        return self.join_table_function(clazz,*_input_cols).select(*output_cols)

    DataFrame.map = map

    def simple_map(self,func):
        return self.select(*func(self))

    DataFrame.simple_map = simple_map

    DataFrameNaFunctions.__oldreplace = DataFrameNaFunctions.replace 
    
    def extended_replace(
        self,
        to_replace: Union[
            LiteralType,
            Iterable[LiteralType],
            Dict[LiteralType, LiteralType],
        ],
        value: Optional[Iterable[LiteralType]] = None,
        subset: Optional[Iterable[str]] = None,
        regex=False
    ) -> "snowflake.snowpark.dataframe.DataFrame":
        if regex:
            return self._df.select([regexp_replace(col(x.name), to_replace,value).alias(x.name) if isinstance(x.datatype,StringType) else col(x.name) for x in self._df.schema])
        else:
            return self.__oldreplace(to_replace,value,subset)
    
    DataFrameNaFunctions.replace = extended_replace    

    # EXPLODE HELPERS
    class Explode:
        def __init__(self,expr):
            self.expr = expr

    def explode(expr):
        return Explode(expr)

    F.explode = explode

    DataFrame.oldwithColumn = DataFrame.withColumn
    def withColumnExtended(self,colname,expr):
        if isinstance(expr, Explode):
            return self.join_table_function('flatten',date_range_udf(col("epoch_min"), col("epoch_max"))).drop(["SEQ","KEY","PATH","INDEX","THIS"]).rename("VALUE",colname)
        else:
            return self.oldwithColumn(colname,expr)
    DataFrame.withColumn = withColumnExtended


import shortuuid
from snowflake.snowpark import Window, Column
from snowflake.snowpark.types import *
from snowflake.snowpark.functions import udtf, col
from snowflake.snowpark.relational_grouped_dataframe import RelationalGroupedDataFrame

if not hasattr(RelationalGroupedDataFrame, "applyInPandas"):
  def applyInPandas(self,func,schema):
      output_schema = schema
      if isinstance(output_schema, str):
        output_schema = schema_str_to_schema(output_schema)
      from snowflake.snowpark.functions import col
      input_types = [x.datatype for x in self._df.schema.fields]
      input_cols  = [x.name for x in self._df.schema.fields]
      output_cols = [x.name for x in output_schema.fields]
      grouping_exprs = [Column(x) for x in self._grouping_exprs]
      clazz="applyInPandas"+shortuuid.uuid()[:8]
      def __init__(self):
          self.rows = []
          self.dfs  = []
      def process(self, *row):
          self.rows.append(row)
          # Merge rows into a dataframe
          if len(self.rows) >= 16000:
             df = pd.DataFrame(self.rows)
             self.dfs.append(df)
             self.rows = []
          # Merge dataframes into a single dataframe
          if len(self.dfs) >= 100:
             merged_df = pd.concat(self.dfs)
             self.dfs = [merged_df]
          yield None
      def end_partition(self):
        # Merge any remaining rows
        if len(self.rows) > 0:
          df = pd.DataFrame(self.rows,columns=input_cols)
          self.dfs.append(df)
          self.rows = []
        pandas_input = pd.concat(self.dfs)        
        pandas_output = func(pandas_input)
        for row in pandas_output.itertuples(index=False):
             yield tuple(row)
      non_ambigous_output_schema = StructType([StructField(f"pd_{i}",output_schema.fields[i].datatype) for i in range(len(output_schema.fields))])
      renamed_back = [col(f"pd_{i}").alias(output_schema.fields[i].name) for i in range(len(non_ambigous_output_schema.fields))]
      udtf_class = type(clazz, (object, ), {"__init__":__init__,"process":process,"end_partition":end_partition})
      tfunc = udtf(udtf_class,output_schema=non_ambigous_output_schema, input_types=input_types,name=clazz,replace=True,is_permanent=False,packages=["snowflake-snowpark-python", "pandas"])
      return self._df.join_table_function(tfunc(*input_cols).over(partition_by=grouping_exprs, order_by=grouping_exprs)).select(*renamed_back)

  RelationalGroupedDataFrame.applyInPandas = applyInPandas
  ###### HELPER END   
