import random
import re
import uuid

from collections import namedtuple
from string import ascii_letters, ascii_uppercase
from typing import List, Optional

try:
    from typing import Literal  # Only available on 3.8+ directly
except ImportError:
    from typing_extensions import Literal

FQTN = namedtuple("FQTN", ["database", "schema", "table"], defaults=(None, None, None))


def is_fqtn(fqtn: str, raise_if_false: bool = False) -> bool:
    """
    Determine if a string is a fully qualified table name

    Allowed formats:
    DATABASE.SCHEMA.TABLE
    "DATABASE"."SCHEMA"."TABLE"
    `project:dataset.table`
    `project-001`.`dataset`.`table`

    Returns a boolean, or raises an exception if directed
    """
    if fqtn and re.match(r'["`\-\w]+[\.:]["`\w]+\.["`\w]+', fqtn):
        return True
    if raise_if_false:
        raise ValueError(f"{fqtn} is not a well-formed fqtn")
    return False


def make_fqtn(
    table: str, database: Optional[str] = None, schema: Optional[str] = None, org_defaults: dict = None
) -> str:
    if is_fqtn(table):
        return table
    if not org_defaults and (not database or not schema):
        raise ValueError("Need to pass database and schema to make a FQTN")
    database = database or org_defaults.get("database")
    schema = schema or org_defaults.get("schema")
    return f"{database}.{schema}.{table}"


def split_fqtn(fqtn: str, org_defaults: dict = None) -> FQTN:
    """
    Accepts a possible fully qualified table string and returns its component parts
    """
    database = org_defaults.get("database") if org_defaults else None
    schema = org_defaults.get("schema") if org_defaults else None
    table = fqtn
    if fqtn.count(".") == 2:
        database, schema, table = fqtn.split(".")
    if fqtn.count(".") == 1:
        schema, table = fqtn.split(".")
    return FQTN(database, schema, table)


def quote_fqtn(
    fqtn: str,
    dw_type: str = Literal['bigquery', 'snowflake'],
) -> str:
    """
    Handle quoting of fqtns
    """
    quote_char = '`' if dw_type == 'bigquery' else '"'
    if is_fqtn(fqtn, raise_if_false=True):
        database, schema, table = split_fqtn(fqtn)
        database = f"{quote_char}{database}{quote_char}" if needs_quoting(database) else database
        schema = f"{quote_char}{schema}{quote_char}" if needs_quoting(schema) else schema
        table = f"{quote_char}{table}{quote_char}" if needs_quoting(table) else table
        return f"{database}.{schema}.{table}"


def needs_quoting(token: str):
    """
    Does this token contain characters that need quoting in the DW

    Returns a boolean
    """
    # NOTE: we may want to use ascii_uppercase here when we can trust input data to be correctly casesd
    if any([char for char in token if char not in (ascii_letters + "_")]):
        return True
    if token in (SNOWFLAKE_RESTRICTED_KEYWORDS):
        return True
    return False


def gen_operation_table_name(
    op_num: int,
    transform_name: str,
) -> str:
    """
    Generate and return the table or view name to set as the
    output of an operation.

    We try to create as intelligent as a name possible with the information
    we have about the offline dataset at the time of transformation.

    GUID is added to ensure uniqueness of table/view names

    Args:
        op_num: Number of this operation in it's operation op set
        transform_name: Name of the transform applied

    Returns:
        Table or View name to set as output for a operation
    """
    short_guid = str(uuid.uuid4()).replace('-', '')[:10]
    return f"RASGO_SDK__OP{op_num}__{transform_name}_transform__{short_guid}".upper()


def random_alias() -> str:
    """
    Returns a random 16 char string
    """
    return ''.join(random.choice(ascii_uppercase) for x in range(16))


def cleanse_sql_data_type(dtype: str) -> str:
    """
    Converts a string to Snowflake compliant data type
    """
    if dtype.lower() in ["object", "text", "variant"]:
        return "string"
    else:
        return dtype.lower()


def cleanse_sql_list(list_in: List[str]) -> List[str]:
    """
    Converts a list of strings to Snowflake compliant names
    """
    return [cleanse_sql_name(n) for n in list_in]


def cleanse_sql_name(name: str) -> str:
    """
    Converts a string to a snowflake compliant value
    """
    name = name.replace(" ", "_").replace("-", "_").replace('"', '').replace(".", "_").upper()
    if name[0] not in (ascii_letters + "_"):
        return f"_{name}"
    return name


def cleanse_dbt_name(name: str) -> str:
    """
    Converts a string to a dbt compliant value
    """
    return name.replace(" ", "_").replace("-", "_").replace('"', '').replace(".", "_").lower()


def is_restricted_sql(sql: str) -> bool:
    """
    Checks a SQL string for presence of dangerous keywords
    """
    if any(word in sql.upper() for word in SNOWFLAKE_RESTRICTED_KEYWORDS):
        return True
    return False


def is_scary_sql(sql: str) -> bool:
    """
    Checks a SQL string for presence of injection keywords
    """
    if any(word in sql.upper() for word in SQL_INJECTION_KEYWORDS):
        return True
    return False


def is_valid_view_sql(sql: str) -> bool:
    """
    Checks a SQL string for presence of structural keywords
    """
    mandatory_words = ["SELECT", "FROM"]
    if not all(word in sql.upper() for word in mandatory_words):
        return False
    return True


SQL_RESTRICTED_CHARACTERS = [' ', '-', ';']

SQL_INJECTION_KEYWORDS = [
    'DELETE',
    'TRUNCATE',
    'DROP',
    'ALTER',
    'UPDATE',
    'INSERT',
    'MERGE',
]

# fmt: off
SNOWFLAKE_RESTRICTED_KEYWORDS = [
    'ACCOUNT','ALL','ALTER','AND','ANY','AS','BETWEEN','BY',
    'CASE','CAST','CHECK','COLUMN','CONNECT','CONNECTION','CONSTRAINT',
    'CREATE','CROSS','CURRENT','CURRENT_DATE','CURRENT_TIME','CURRENT_TIMESTAMP',
    'CURRENT_USER','DATABASE','DELETE','DISTINCT','DROP','ELSE','EXISTS','FALSE',
    'FOLLOWING','FOR','FROM','FULL','GRANT','GROUP','GSCLUSTER','HAVING','ILIKE',
    'IN','INCREMENT','INNER','INSERT','INTERSECT','INTO','IS','ISSUE','JOIN','LATERAL',
    'LEFT','LIKE','LOCALTIME','LOCALTIMESTAMP','MINUS','NATURAL','NOT','NULL','OF','ON',
    'OR','ORDER','ORGANIZATION','QUALIFY','REGEXP','REVOKE','RIGHT','RLIKE','ROW','ROWS',
    'SAMPLE','SCHEMA','SELECT','SET','SOME','START','TABLE','TABLESAMPLE','THEN','TO','TRIGGER',
    'TRUE','TRY_CAST','UNION','UNIQUE','UPDATE','USING','VALUES','VIEW','WHEN','WHENEVER','WHERE','WITH'
]
# fmt: on
