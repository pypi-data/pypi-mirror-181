# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xerparser', 'xerparser.schemas', 'xerparser.scripts', 'xerparser.src']

package_data = \
{'': ['*']}

install_requires = \
['html-sanitizer>=1.9.3,<2.0.0', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'xerparser',
    'version': '0.3.0',
    'description': 'Parse a P6 .xer file to a Python dictionary object.',
    'long_description': '# xerparser\n\nA simple Python package that reads a P6 .xer file and converts it into a Python object.  \n<br>\n*Disclaimers:  \nThis package is only usefull if you are already familiar with the mapping and schemas used by P6 during the export process. \nRefer to the [Oracle Documentation]( https://docs.oracle.com/cd/F25600_01/English/Mapping_and_Schema/xer_import_export_data_map_project/index.htm) for more information regarding how data is mapped to the XER format.  \nTested on .xer files exported as versions 15.2 through 19.12.*  \n<br>\n## Install\n**Windows**:\n```bash\npip install xerparser\n```\n**Linux/Mac**: \n```bash\npip3 install xerparser\n```\n<br>  \n\n## Usage  \nImport the ***Xer*** class from **xerparser**  and pass a .xer file as an argument.  \n```python\nfrom xerparser import Xer\n\nfile = r"/path/to/file.xer"\nxer = Xer(file)\n```\nThe Xer class accepts .xer file passed as types **str**, **path**, or **bytes**.  \nThe file and table data will be parsed and returned as a Python object.  \n<br>\n## Attributes \nThe tables stored in the .xer file are attributes for the **Xer** class. Since a XER file can contain multiple projects/schedules, the tables are accessable as either Global , Project specific, or Task Specific:\n###  Global\n  ```python\n  xer.export    # export data\n  xer.errors    # list of potential errors in export process\n  xer.calendars # dict of CALENDAR objects\n  xer.projects  # dict of PROJECT objects\n  xer.resources # dict of RSRC objectrs\n  ```  \n### Project Specific\n```python\n# Get first project\nproject = xer.projects.values()[0]\n\nproject.calendars       # set of CALENDAR objects used by project\nproject.tasks           # dict of TASK objects\nproject.relationships   # dict of TASKPRED objects\nproject.wbs             # dict of PROJWBS objects\n```\n### Task Specific\n```python\n# Get first task\ntask = project.tasks.values()[0]\n\ntask.memos        # list of TASKMEMO objects\ntask.resources    # list of TASKRSRC objects\n```\n### Error Checking\nSometimes the xer file is corrupted during the export process. A list of potential errors is generated based on common issues encountered when analyzing .xer files:  \n- Minimum required tables - an error is recorded if one of the following tables is missing:\n  - CALENDAR\n  - PROJECT\n  - PROJWBS\n  - TASK\n  - TASKPRED  \n- Required table pairs - an error is recorded if Table 1 is included but not Table 2:  \n  \n  | P6 Table 1       | P6 Table 2       | Notes    |\n  | :----------- |:-------------|----------|\n  | TASKFIN | FINDATES | *Financial Period Data for Task* |\n  | TRSRCFIN | FINDATES | *Financial Period Data for Task Resource* |\n  | TASKRSRC | RSRC | *Resource Data* |\n  | TASKMEMO | MEMOTYPE | *Notebook Data* |\n  | ACTVCODE | ACTVTYPE | *Activity Code Data* |\n  | TASKACTV | ACTVCODE | *Activity Code Data* |\n\n- Non-existent calendars assigned to activities.\n\n<br>  \n\n## Example Code\n```python\nfrom xerparser import Xer, PROJECT\n\nfile = r"/path/to/file.xer"\nxer = Xer(file)  \nxer.export.version  # -> 15.2  \nxer.export.date  # -> datetime.datetime(2022, 11, 30, 0, 0)  \nxer.errors  # -> []  \n\n# get first project\nproject: PROJECT = xer.projects.values()[0]\n\n# get project name\nproject.name\n\n# get project data date\nproject.data_date\n\n# get project finish date\nproject.finish_date\n\n# get task and relationship count\nlen(project.tasks)\nlen(project.relationships)\n\n# loop through tasks\nfor task in project.tasks.values():\n    print(task)\n\n```',
    'author': 'Jesse',
    'author_email': 'code@seqmanagement.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jjCode01/xerparser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
