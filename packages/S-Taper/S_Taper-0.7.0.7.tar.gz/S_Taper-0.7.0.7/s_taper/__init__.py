import sqlite3
import s_taper.consts


class Taper:
    """
        Main class. Its instances correspond to a single table in the database.
        Use:
        table1 = Taper("table_name", "file.db")
    """

    def __init__(self, table_name: str, file_name: str):
        self._table_name: str = table_name
        self._file_name: str = file_name

    def write(self, table_name: str = None, values: list | tuple = None):
        if table_name is None:
            table_name = self._table_name
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        questions = "?"
        for x in range(len(values) - 1):
            questions += ", ?"

        cur.execute(f"INSERT or REPLACE into {self._table_name} VALUES({questions});", values)
        conn.commit()
        conn.close()
        return values

    def read(self, column_name: str, key: str | int):
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        cur.execute(f'SELECT * from {self._table_name} WHERE {column_name} = ? ', (key,))
        result = cur.fetchone()
        return result

    def read_all(self, table_name: str = None):
        if table_name is None:
            table_name = self._table_name
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        cur.execute(f"SELECT * from {table_name}")
        result = cur.fetchall()
        conn.close()
        return result

    def delete_row(self, column_name: str = None, key: str | int = None, all_rows: bool = None):
        """
        Func uses to deleting rows from the table.

        :param column_name: Column name to delete the row in which the key is found in the current column
        :param key: Key which looks in column
        :param all_rows: If True func delete all rows in the table
        """

        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        if all_rows:
            cur.execute(f'DELETE FROM {self._table_name}')
        else:
            cur.execute(f'DELETE FROM {self._table_name} WHERE {column_name} = ?', (key,))
        conn.commit()
        conn.close()

    def create_table(self, table: dict, table_name: str = None):
        """
        table - {
                    "table1": "type",
                    and so on
                }

        """
        if table_name is None:
            table_name = self._table_name
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        task = f"CREATE TABLE IF NOT EXISTS {table_name}("
        n = 0
        for key in table:
            n += 1
            task += f"{key} {table[key]}"
            if n != len(table):
                task += ", "
            else:
                task += ");"
        cur.execute(task)
        conn.commit()
        conn.close()
        return Taper(table_name, self._file_name)

    def pop_table(self, table_name: str = None):
        if not table_name:
            table_name = self._table_name
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        cur.execute(f"DROP TABLE {table_name}")
        conn.commit()
        conn.close()
