# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['parquet_inspector']

package_data = \
{'': ['*']}

install_requires = \
['pyarrow>=6.0.0']

entry_points = \
{'console_scripts': ['pqi = parquet_inspector.main:main']}

setup_kwargs = {
    'name': 'parquet-inspector',
    'version': '0.1.0',
    'description': 'CLI tool for inspecting parquet files.',
    'long_description': '# Parquet-Inspector\n\nA command line tool for inspecting parquet files with PyArrow.\n\n## Installation\n\n```bash\npip install parquet-inspector\n```\n\n## Usage\n\n```txt\nparquet-inspector: cli tool for inspecting parquet files.\n\npositional arguments:\n  {metadata,schema,head,tail,count,validate,to-jsonl,to-parquet}\n    metadata            print file metadata\n    schema              print data schema\n    head                print first n rows (default is 10)\n    tail                print last n rows (default is 10)\n    count               print number of rows\n    validate            validate file\n    to-jsonl            convert parquet file to jsonl\n    to-parquet          convert jsonl file to parquet\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --version         show program\'s version number and exit\n  --threads, -t         use threads for reading\n  --mmap, -m            use memory mapping for reading\n\n```\n\n## Examples\n\n```bash\n# Print the metadata of a parquet file\n$ pqi metadata my_file.parquet\ncreated_by: parquet-cpp-arrow version 6.0.1\nnum_columns: 3\nnum_rows: 2\nnum_row_groups: 1\nformat_version: 1.0\nserialized_size: 818\n```\n\n```bash\n# Print the schema of a parquet file\n$ pqi schema my_file.parquet\na: list<item: int64>\n  child 0, item: int64\nb: struct<c: bool, d: timestamp[ms]>\n  child 0, c: bool\n  child 1, d: timestamp[ms]\n```\n\n```bash\n# Print the first 5 rows of a parquet file (default is 10)\n$ pqi head -n 5 my_file.parquet\n{"a": 1, "b": {"c": true, "d": "1991-02-03 00:00:00"}}\n{"a": 2, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 3, "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n{"a": 4, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 5, "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n```\n\n```bash\n# Print the last 5 rows of a parquet file\n$ pqi tail -n 5 my_file.parquet\n{"a": 3, "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n{"a": 4, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 5 "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n{"a": 6 "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 7 "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n```\n\n```bash\n# Print the first 5 rows of a parquet file, only reading the column a\n$ pqi head -n 5 -c a my_file.parquet\n{\'a\': 1}\n{\'a\': 2}\n{\'a\': 3}\n{\'a\': 4}\n{\'a\': 5}\n```\n\n```bash\n# Print the first 3 rows that satisfy the condition a > 3\n# (filters are defined in disjunctive normal form)\n$ pqi head -n 3 -f "[(\'a\', \'>\', 3)]" my_file.parquet\n{"a": 4, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 5 "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n{"a": 6 "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n```\n\n```bash\n# Print the number of rows in a parquet file\n$ pqi count my_file.parquet\n7\n```\n\n```bash\n# Validate a parquet file\n$ pqi validate my_file.parquet\nOK\n```\n\n```bash\n# Convert a parquet file to jsonl\n$ pqi to-jsonl my_file.parquet\n$ cat my_file.jsonl\n{"a": 1, "b": {"c": true, "d": "1991-02-03 00:00:00"}}\n{"a": 2, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 3, "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n{"a": 4, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 5, "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n{"a": 6, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 7, "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n```\n\n```bash\n# Convert a jsonl file to parquet\n$ pqi to-parquet my_file.jsonl\n$ pqi head my_file.parquet\n{"a": 1, "b": {"c": true, "d": "1991-02-03 00:00:00"}}\n{"a": 2, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 3, "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n{"a": 4, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 5, "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n{"a": 6, "b": {"c": false, "d": "2019-04-01 00:00:00"}}\n{"a": 7, "b": {"c": true, "d": "2019-04-01 00:00:00"}}\n```\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Dominic Thorn',
    'author_email': 'dominic.thorn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
