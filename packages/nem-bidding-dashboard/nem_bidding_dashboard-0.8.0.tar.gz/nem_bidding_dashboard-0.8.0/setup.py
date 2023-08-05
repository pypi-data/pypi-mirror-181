# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nem_bidding_dashboard']

package_data = \
{'': ['*'], 'nem_bidding_dashboard': ['assets/*']}

install_requires = \
['dash-bootstrap-components>=1.2.1,<2.0.0',
 'dash-loading-spinners>=1.0.0,<2.0.0',
 'dash>=2.6.1,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'nemosis>=3.1.0,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.2,<2.0',
 'plotly>=5.10.0,<6.0.0',
 'psycopg[binary]>=3.1.4,<4.0.0',
 'supabase>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'nem-bidding-dashboard',
    'version': '0.8.0',
    'description': 'A dashboard for visualising bidding data for the National Energy Market',
    'long_description': '# Introduction\n\nnem-bidding-dashboard is a web app and python package for collating, processing and visualising data relevant to \nunderstanding participant behaviour in the Australian National Electricity Market wholesale spot market.\n\nThe web app is intended to make reviewing the bidding behaviour of market participants as easy as possible. Aggregate \nbehaviour can be visualised as at a whole of market, regional, or technology level. Alternatively, the non-aggregated \nbids of dispatch units, and stations can be visualised.\n\nWe have additionally published the code required to run the web app as a python package, so that it can used to help \nanalysis and visualise bidding behaviour in alternative or more sophisticated ways than allowed by the web app.\n\nThe development of nem-bidding-dashboard up to December 2022 was funded by the \n[Digital Grid Futures Institute](https://www.dgfi.unsw.edu.au/)\n\n## Status\n\nUnderdevelopment and not recommended for use yet, check back here in early 2023 to see if a production version has been\nlaunched.\n\n## Web app\n\nnem-bidding-dashboard is hosted as a web app here: [http://nembiddingdashboard.org](http://nembiddingdashboard.org)\n\n## Python package / API\n\nThe python api can be used to:\n- run the web app interface locally\n- download publicly available bidding and operational data from the Australian Energy Market Operator\n- process and aggregate bidding and operational data into the format used in the web app\n- build and populate a PostgresSQL database for efficiently querying and aggregating bidding and operational data\n\n### Installation\n\n`pip install nem_bidding_dashboard`\n\n### Quick examples\n\nBelow are some quick examples that provide at taste of the api capabilities, see the full set of examples and api\ndocumentation for a complete guide.\n\n#### Get raw data\nTo get the raw data used by nem-bidding-dashboard before preprocessing use functions in the `fetch_data` module, e.g.\n`get_volume_bids`.\n\n```python\nfrom nem_bidding_dashboard import fetch_data\n\nvolume_bids = fetch_data.get_volume_bids(\n    start_time=\'2020/01/01 00:00:00\',\n    end_time=\'2020/01/01 00:05:00\',\n    raw_data_cache=\'D:/nemosis_data_cache\')\n\nprint(volume_bids.head(5))\n#         SETTLEMENTDATE      DUID  ... PASAAVAILABILITY   INTERVAL_DATETIME\n# 9547382     2019-12-31    AGLHAL  ...            181.0 2020-01-01 00:05:00\n# 9547383     2019-12-31    AGLSOM  ...            140.0 2020-01-01 00:05:00\n# 9547384     2019-12-31   ANGAST1  ...             44.0 2020-01-01 00:05:00\n# 9547385     2019-12-31     APD01  ...              0.0 2020-01-01 00:05:00\n# 9547386     2019-12-31     APD01  ...              NaN 2020-01-01 00:05:00\n```\n\n#### Get processed data\nTo get data in the format stored by nem-bidding-dashboard in the PostgresSQL database use functions in the module\n`fetch_and_preprocess`, e.g. `bid_data`.\n\n```python\nfrom nem_bidding_dashboard import fetch_and_preprocess\n\nbids = fetch_and_preprocess.bid_data(\n    start_time=\'2020/01/01 00:00:00\',\n    end_time=\'2020/01/01 00:05:00\',\n    raw_data_cache=\'D:/nemosis_data_cache\')\n\nprint(bids.head(5))\n#        INTERVAL_DATETIME      DUID  ...  BIDVOLUMEADJUSTED  BIDPRICE\n# 0    2020-01-01 00:05:00    BALBL1  ...                0.0    -48.06\n# 1    2020-01-01 00:05:00    RT_SA4  ...                0.0  -1000.00\n# 2    2020-01-01 00:05:00    RT_SA5  ...                0.0  -1000.00\n# 3    2020-01-01 00:05:00    RT_SA6  ...                0.0  -1000.00\n# 4    2020-01-01 00:05:00   RT_TAS1  ...                0.0  -1000.00\n```\n\n#### Setup a PostgresSQL database\n\nCreate tables for storing processed data and functions, then populate the database with historical data.\n\n```python\nfrom nem_bidding_dashboard import postgres_helpers, build_postgres_db, populate_postgres_db\n\ncon_string = postgres_helpers.build_connection_string(\n    hostname=\'localhost\',\n    dbname=\'bidding_dashboard_db\',\n    username=\'bidding_dashboard_maintainer\',\n    password=\'1234abcd\',\n    port=5433)\n\nbuild_postgres_db.create_db_tables_and_functions(con_string)\n\nraw_data_cache = "D:/nemosis_cache"\nstart = "2020/01/01 00:00:00"\nend = "2020/02/01 00:00:00"\n\npopulate_postgres_db.duid_info(con_string, raw_data_cache)\npopulate_postgres_db.bid_data(con_string, start, end, raw_data_cache)\npopulate_postgres_db.region_data(con_string, start, end, raw_data_cache)\npopulate_postgres_db.unit_dispatch(con_string, start, end, raw_data_cache)\n```\n\n#### Query and aggregate bidding data from PostgresSQL database\n\nFilter bids by time and region, and then aggregate into price bands. Other functions in the module `query_postgres_db`\nprovide querying an aggregation and functionality for each table in the db.\n\n```python\n\nfrom nem_bidding_dashboard import postgres_helpers, query_postgres_db\n\ncon_string = postgres_helpers.build_connection_string(\n    hostname=\'localhost\',\n    dbname=\'bidding_dashboard_db\',\n    username=\'bidding_dashboard_maintainer\',\n    password=\'1234abcd\',\n    port=5433)\n\nagg_bids = query_postgres_db.aggregate_bids(\n    con_string,\n    [\'QLD\', \'NSW\', \'SA\'],\n    "2020/01/01 00:00:00",\n    "2020/01/01 01:00:00",\n    \'hourly\',\n    \'Generator\',\n    \'adjusted\',\n    [])\n\nprint(agg_bids)\n#      INTERVAL_DATETIME        BIN_NAME  BIDVOLUME\n# 0  2020-01-01 01:00:00    [1000, 5000)   1004.000\n# 1  2020-01-01 01:00:00      [100, 200)    300.000\n# 2  2020-01-01 01:00:00       [50, 100)   1788.000\n# 3  2020-01-01 01:00:00   [-1000, -100)   9672.090\n# 4  2020-01-01 01:00:00      [200, 300)   1960.000\n# 5  2020-01-01 01:00:00         [0, 50)   4810.708\n# 6  2020-01-01 01:00:00       [-100, 0)      7.442\n# 7  2020-01-01 01:00:00      [300, 500)    157.000\n# 8  2020-01-01 01:00:00     [500, 1000)    728.000\n# 9  2020-01-01 01:00:00  [10000, 15500)   4359.000\n# 10 2020-01-01 01:00:00   [5000, 10000)     20.000\n```\n\n## Contributing\n\nInterested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md).\n\nPlease note that this project is released with a [Code of Conduct](CONDUCT.md). By contributing to this project, you \nagree to abide by its terms.\n\n## License\n\n`nem-bidding-dashboard` was created by `Nicholas Gorman` and `Patrick Chambers`. It is licensed under the terms of the \n`BSD-3-Clause license`.\n\n',
    'author': 'Patrick Chambers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
