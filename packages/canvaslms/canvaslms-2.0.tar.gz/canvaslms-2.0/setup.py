# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['canvaslms', 'canvaslms.cli', 'canvaslms.grades', 'canvaslms.hacks']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'argcomplete>=2.0.0,<3.0.0',
 'arrow>=1.2.3,<2.0.0',
 'cachetools>=5.2.0,<6.0.0',
 'canvasapi>=3.0.0,<4.0.0',
 'keyring>=23.11.0,<24.0.0',
 'pypandoc>=1.10,<2.0']

entry_points = \
{'console_scripts': ['canvaslms = canvaslms.cli:main']}

setup_kwargs = {
    'name': 'canvaslms',
    'version': '2.0',
    'description': 'Command-line interface to Canvas LMS',
    'long_description': '# canvaslms: A CLI to Canvas LMS.\n\nThis program provides a command-line interface for Canvas. The command\nis `canvaslms` and it has several subcommands in the same style as Git.\n`canvaslms` provides output in a format useful for POSIX tools, this\nmakes automating tasks much easier.\n\nLet\'s consider how to grade students logging into the student-shell SSH\nserver. We store the list of students\' Canvas and KTH IDs in a file.\n\n``` {.text}\ncanvaslms users -c DD1301 -s | cut -f 1,2 > students.csv\n```\n\nThen we check who has logged into student-shell.\n\n``` {.text startFrom="2"}\nssh student-shell.sys.kth.se last | cut -f 1 -d " " | sort | uniq \\\n  > logged-in.csv\n```\n\nFinally, we check who of our students logged in.\n\n``` {.text startFrom="4"}\nfor s in $(cut -f 2 students.csv); do\n  grep $s logged-in.csv && \\\n```\n\nFinally, we can set their grade to P and add the comment "Well done!" in\nCanvas. We set the grades for the two assignments whose titles match the\nregular expression `(Preparing the terminal|The terminal)`.\n\n``` {.text startFrom="6"}\n    canvaslms grade -c DD1301 -a "(Preparing the terminal|The terminal)" \\\n      -u $(grep $s students.csv | cut -f 1) \\\n      -g P -m "Well done!"\ndone\n```\n\n## Installation\n\nJust install the PyPI package:\n```\npython3 -m pip install canvaslms\n```\nSome subcommands use `pandoc`, so you will likely have to [install \npandoc][pandoc] on your system manually.\n\n[pandoc]: https://pandoc.org/installing.html\n',
    'author': 'Daniel Bosk',
    'author_email': 'dbosk@kth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbosk/canvaslms',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
