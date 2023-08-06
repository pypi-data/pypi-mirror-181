from psycopg2._json import Json
from volsite_postgres_common.api.CA import CA


def json_fn(fn: str, input_j: dict, conn, print_json,
            do_commit: bool = False,
            print_input_output: bool = True,
            print_long_att: bool = True):  # -> dict:
    cursor = conn.cursor()
    if print_input_output:
        print(f'==== [FN] {fn} ====')
        print('=== Input ===')
        print('<code>')
        print_json(input_j, print_long_att)
        print('</code>')
    cursor.execute(f'SELECT {fn}( %s::JSONB ) AS {CA.Result}', (
        Json(input_j),
    ))
    rows = cursor.fetchall()
    assert 1 == len(rows)
    # print('[json_fn] rows[0] = %r' % rows[0])
    if do_commit:
        conn.commit()
    output = rows[0][CA.Result]
    if print_input_output:
        print('=== Output ===')
        print('<code>')
        print_json(output, print_long_att)
        print('</code>')
    return output
