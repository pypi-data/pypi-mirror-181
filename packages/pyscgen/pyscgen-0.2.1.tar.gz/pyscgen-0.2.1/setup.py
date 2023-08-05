# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyscgen',
 'pyscgen.__config',
 'pyscgen.avro',
 'pyscgen.avro._model',
 'pyscgen.avro.schema',
 'pyscgen.json',
 'pyscgen.json._model',
 'pyscgen.json.analyze',
 'pyscgen.json.merge',
 'pyscgen.pydantic',
 'pyscgen.pydantic.schema']

package_data = \
{'': ['*']}

install_requires = \
['glom>=22.1.0,<23.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pydantic-avro>=0.4.2,<0.5.0',
 'pydantic>=1.9.0,<2.0.0',
 'shortuuid>=1.0.8,<2.0.0']

setup_kwargs = {
    'name': 'pyscgen',
    'version': '0.2.1',
    'description': 'Python AVRO Schema generator which can use multiples example JSONs as input to infer the Schema.',
    'long_description': '# (pyscgen) python schema generator \nA Python Package to analyze JSON Documents, build a merged JSON-Document out of multiple provided JSON Documents and create an \nAVRO-Schemas based on multiple given JSON Documents.\n\n## Installation\n\n### pip\n``pip install pyscgen``\n\n### poetry\n``poetry add pyscgen``\n\n## JSON Analyzer\nreceives a list of json documents, analyzes the structure and outputs the following infos:\n\n-**Output**:\n- collection_data: \n  - dict which stores infos about the columns of each document with attributes like name, path, data type and if its null\n- column_infos: \n  - condensed/merged column infos of all given documents with attributes like name, path, nullability, density, unique values, data types found, parent column config etc.\n  - This is the "real" result of the analyzer and the building plan for the JSON Merger and AVRO Schema generator.\n- df_flattened\n  - A pandas DataFrame which stores the json documents flattened and contains every found column with data.\n  - One document is represented by one row, index starts at 0 and matches to the order in the given list of documents.\n- df_dtypes\n  - A pandas DataFrame which stores the python data type for each column of all given documents.\n  - One document is represented by one row, index starts at 0 and matches to the order in the given list of documents.\n- df_unique\n  - A pandas DataFrame which stores unique values found for each column of all given documents.\n  - This data frame is pivoted\n    - The column "0" stores all found column. One column is represented by one row.\n    - The columns 1 - n contain one distinct value each. If you analyze 10 documents and one field has a distinct value in each document, you´ll produce 10 value columns.\n\n## JSON Merger\nreceives a list of json documents, analyzes the structure with the JSON Analyzer and outputs one merged dictionary/json document with all found columns and dummy values according to the found data types:\n \n- **Output**: merged_doc: \n  - dictionary merged together from the all given JSON documents.\n\n## AVRO Schema generator\nreceives a list of json documents, analyzes the structure with the JSON Analyzer and outputs a "Schema"-object which can be converted to a dict and stored in an avsc-file\n \n- **Flow:**\n  - JSON Analyzer -> JSON Merger -> AVRO Schema generator\n- **Output**: avro_schema:\n  - AVRO Schema object can be converted to a dict and stored to an avsc file, see examples.\n- **Limitations/Currently not supported**:\n  - Resolution of duplicated names in the AVRO-Output\n    - You can resolve this manually by renaming duplicated elements by hand afterwards and use [aliases](https://avro.apache.org/docs/current/spec.html#Aliases) to still match with the input data.\n    - You can also use inheritance in AVRO-Schemas, here´s an example: https://www.nerd.vision/post/reusing-schema-definitions-in-avro, but that´s definitely more complicated\n  - empty dicts/maps:\n    - If one of your JSON input documents has an empty dictionary, e. g. ```{"field1": "value1", "field2": {}}``` an empty AVRO record will be generated, which is in valid in AVRO.\n    - You can resolve this by deleting the empty record or filling it with live if you know that it´s still needed in the future.\n  - Mixed types for one field in the the JSON Input documents currently results in the most generic AVRO type, which ist a String (Union types, as an option, is planned)\n    - This leads to the case that not all input documents automaticall validate positively against the AVRO schema, because you need to convert types beforehand. \n    - You can use the pydantic model generator to create a model, which automatically converts other data types to string, to solve this issue. Just let all your JSON flow through the model bevore validation.\n\n## Pydantic Model generator\nreceives a list of json documents analyzes the structure with the JSON Analyzer, creates an AVRO Schema which is then used to create a pydantic Model with [pydantic-avro](https://github.com/godatadriven/pydantic-avro)\n \n- **Flow**\n  - JSON Analyzer -> JSON Merger -> AVRO Schema generator -> Pydantic Model generator \n- **Output:** pydantic model:\n  - Pydantic Model as a string which can be written to a .py-File.\n- **Limitations/Currently not supported**:\n  - Python/AVRO bytes is currently not supported in pydantic model generation because there is no support in pydantic for this datatype right now.\n\n# Why should you use it?\nConsidering the fact that there are already other AVRO Schema generators, why should you use this one?\n\nThe simple answer is "null" or "nullability".\n\nAll other solutions I tried simply let you pass one JSON Document as a base for the AVRO-Schema generation.\nThis does obviously not allow to infer nullabilty, because only what\'s present in this one message can be observed \nand therefore used for schema generation.\n\nThis library lets you pass a list of JSON Documents and therefore can gather the infos which fields are always \npresent - aka. mandatory - and which fields are only found in a couple documents - and therefore nullable.\n\nHandling nullability in AVRO-Schemas for records and arrays is quite painful in my opinion, \nthis library gets rid of this chore for you.\n\nOf course, it works just fine with only one JSON document like any other AVRO generator, just without the nullability part then.\n\n# Principles\n- CI-CO (Crap in - Crap out): \n  - The JSON Documents are not validated, therefore, if you pass in garbage, crap in - crap out.\n  - The goal is to creata an AVRO-Schema no matter what. In my opinion, an half ready AVRO-Schema which needs to be edited by hand is better than no AVRO-Schema at all!\n\n# Examples:\n- [JSON Analyzer](./example/pyscgen_json_analyze.py)\n- [JSON Merger](./example/pyscgen_json_merge.py)\n- [AVRO Schema creator](./example/pyscgen_avro_create_schema.py)\n- [Pydantic model creator](./example/pyscgen_pydantic_create_schema.py)\n\n# Other useful resources regarding AVRO:\n- [Official Apache AVRO docs](https://avro.apache.org/docs/current/spec.html)\n- [Python AVRO Schema valdiator "fastavro"](https://github.com/fastavro/fastavro)\n\n# License:\n[BSD-3-Clause](LICENSE)',
    'author': 'Florian Salfenmoser',
    'author_email': 'florian.salfenmoser.dev@outlook.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Salfiii/pyscgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
