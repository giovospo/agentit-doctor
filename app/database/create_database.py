from connection import get_connection

SCHEMA_FILE = "app/database/schema.sql"


def create_database():

    conn = get_connection()

    with open(
        SCHEMA_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        schema = f.read()

    conn.executescript(schema)

    conn.commit()

    conn.close()

    print(
        "Database created successfully"
    )


if __name__ == "__main__":
    create_database()