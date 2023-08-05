from typing import Union, List, Dict


class ColumnSet(object):
    """
    Class to provide quick access to column names.
    """
    def __init__(self, columns: Union[List[str], Dict[str, str]]):
        """
        Create a new ColumnSet.

        :param columns: List of property and column names if identical, or
        mapping from column names to property names.
        """
        if isinstance(columns, list):
            for column in columns:
                setattr(self, ColumnSet._get_python_name(column), column)
            self._columns = {column: column for column in columns}
        elif isinstance(columns, dict):
            for column_name, attr_name in columns.items():
                setattr(self, attr_name, column_name)
            self._columns = columns

    @staticmethod
    def _get_python_name(name: str) -> str:
        """
        Convert the given name to a valid Python variable name.

        :param name: The name to convert.
        """
        new_name = ''
        for c, char in enumerate(name):
            char_ord = ord(char)
            if not (
                    (48 <= char_ord <= 57) or  # 0 to 9
                    (65 <= char_ord <= 90) or  # A-Z
                    (char_ord == 95) or  # _
                    (97 <= char_ord <= 122)
            ):
                new_name += '_'
            else:
                if c == 0 and 48 <= char_ord <= 57:
                    new_name += '_'
                else:
                    new_name += char
        return new_name

    def _to_list(self) -> List[str]:
        """
        Return a list of the column accessor names in the set.
        """
        return list(self._columns.values())

    @property
    def _source_names(self) -> List[str]:
        """
        Return the names of the columns in the original data source.
        """
        return list(self._columns.keys())

    def _print_protocol(self, protocol_name: str):
        """
        Print the protocol definition for non-interactive development.
        """
        print(f'class {protocol_name}(Protocol):\n')
        for attr_name in self._columns.values():
            print(f'    {attr_name}: str')

    def __len__(self):

        return len(self._columns)
