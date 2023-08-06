# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nmdc_schema']

package_data = \
{'': ['*']}

install_requires = \
['check-jsonschema>=0.19.2,<0.20.0',
 'docutils>=0.19,<0.20',
 'jupyter>=1.0.0,<2.0.0',
 'linkml>=1.3.15,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pymongo>=4.3.3,<5.0.0',
 'python-dotenv>=0.21.0,<0.22.0']

entry_points = \
{'console_scripts': ['fetch-nmdc-schema = '
                     'nmdc_schema.nmdc_data:get_nmdc_jsonschema',
                     'migrate_3_2_to_7 = nmdc_schema.migrate_3_2_to_7:cli',
                     'nmdc-data = nmdc_schema.nmdc_data:cli',
                     'nmdc-version = nmdc_schema.nmdc_version:cli',
                     'validate-nmdc-json = nmdc_schema.validate_nmdc_json:cli']}

setup_kwargs = {
    'name': 'nmdc-schema',
    'version': '7.1.0',
    'description': 'Schema resources for the National Microbiome Data Collaborative (NMDC)',
    'long_description': '<p align="center">\n    <img src="images/nmdc_logo_long.jpeg" width="100" height="40"/>\n</p>\n\n# National Microbiome Data Collaborative Schema\n\n[![PyPI - License](https://img.shields.io/pypi/l/nmdc-schema)](https://github.com/microbiomedata/nmdc-schema/blob/main/LICENSE)\n[![PyPI version](https://badge.fury.io/py/nmdc-schema.svg)](https://badge.fury.io/py/nmdc-schema)\n\nThe NMDC is a multi-organizational effort to integrate microbiome data across diverse areas in medicine, agriculture, bioenergy, and the environment. This integrated platform facilitates comprehensive discovery of and access to multidisciplinary microbiome data in order to unlock new possibilities with microbiome data science.\n\nThis repository mainly defines a [LinkML](https://github.com/linkml/linkml) schema for managing metadata from the [National Microbiome Data Collaborative (NMDC)](https://microbiomedata.org/).\n\n## Repository Contents Overview\nSome products that are maintained, and tasks orchestrated within this repository are:\n\n- Maintenance of LinkML YAML that specifies the NMDC Schema\n  - [src/schema/nmdc.yaml](src/schema/nmdc.yaml)\n  - and various other YAML schemas imported by it, like [prov.yaml](src/schema/prov.yaml), [annotation.yaml](src/schema/annotation.yaml), etc. all which you can find in the [src/schema](src/schema/) folder\n- Makefile targets for converting the schema from it\'s native LinkML YAML format to other artifact like [JSON Schema](jsonschema/nmdc.schema.json)\n- Build, deployment and distribution of the schema as a PyPI package\n- Automatic publishing of refreshed documentation upon change to the schema, accessible [here](https://microbiomedata.github.io/nmdc-schema/)\n## Background\n\nThe NMDC [Introduction to metadata and ontologies](https://microbiomedata.org/introduction-to-metadata-and-ontologies/) primer provides some the context for this project.\n\nSee also [these slides](https://microbiomedata.github.io/nmdc-schema/schema-slides.html) ![](images/16px-External.svg.png) describing the schema.\n\n## Maintaining the Schema\n\nSee [MAINTAINERS.md](MAINTAINERS.md) for instructions on maintaining and updating the schema.\n\n## NMDC metadata downloads\n\nSee https://github.com/microbiomedata/nmdc-runtime/#data-exports\n\n## Ecosystem Diagram\n\n```mermaid\nflowchart TD\n    subgraph nmdc-schema repo\n    ly([NMDC LinkML YAML files])\n    lg(generated artifacts)\n    ly-.make all.->lg\n    end\n    subgraph Data Validation\n    click ly href "https://github.com/microbiomedata/nmdc-schema/tree/main/src/schema" _top\n    d[(Some data)]\n    v[[Validation process]]\n    v--Has input-->d\n    v--Has input-->ly\n    end\n    subgraph MIxS\n    m([MIxS Schema])\n    end\n    subgraph SubmissionPortal\n    sppg[(Postgres)]\n    spa[Portal API]\n    sppg<-->spa\n    click spa href "https://data.dev.microbiomedata.org/docs" _top\n    ps[Pydantic schema]\n    end\n    subgraph MongoDB\n    mc[(Collections)]\n    ms[Implicit schema]\n    ma[Search API]\n    mc<-->ma\n    click ma href "https://api.dev.microbiomedata.org/docs" _top\n    end\n    mc --Ingest--> sppg\n    subgraph DH Template Prep\n    saf[sheets_and_friends repo]\n    sps([Submission Portal Schema])\n    dhjs[Data Harmoizer JS, etc.]\n    saf-->sps-->dhjs\n    end\n    dhjs-->SubmissionPortal\n    subgraph DataMapping\n    sa[sample-annotator repo]\n    end\n    spa-->sa-..->ma\n    ly-..->ps\n    sj[some json]\n    ly-..->sj-..->MongoDB-..->ps\n```\n',
    'author': 'Bill Duncan',
    'author_email': 'wdduncan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://microbiomedata.github.io/nmdc-schema/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
