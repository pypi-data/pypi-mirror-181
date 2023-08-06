from typing import Final
from volsite_postgres_common.db import CFn
from volsite_postgres_common.fn.insert import insert_function

ID_PREFIX: Final = 'i'

is_null_any: Final = (
    f" CREATE OR REPLACE FUNCTION "
    f" {CFn.is_null} (anyelement) "
    f" RETURNS BOOLEAN "
    f" AS"
    f" $$"
    f"   SELECT $1 IS NULL"
    f" $$ "
    f" LANGUAGE SQL "
    f" IMMUTABLE;")

bigint_2_id: Final = (
    f" CREATE OR REPLACE FUNCTION "
    f" {CFn.bigint_2_id} (_bid BIGINT) "
    f" RETURNS TEXT "
    f" AS"
    f" $$"
    f"   SELECT CONCAT ( '{ID_PREFIX}', _bid)"
    f" $$ "
    f" STRICT"
    f" LANGUAGE SQL "
    f" IMMUTABLE;")


def insert_util_fn__general(conn):
    insert_function(is_null_any, CFn.is_null, conn)
    insert_function(bigint_2_id, CFn.bigint_2_id, conn)
