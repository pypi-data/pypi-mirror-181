# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fourier_sine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fourier-sine',
    'version': '0.3.0',
    'description': 'Fourier Analysis with sine waves',
    'long_description': '# Fourier Analysis\n\nThis works nicely for sine waves. The series output was tested with plotly\'s line plot but can be used with any plotting library. It should output a new series (in list of floats format) with maximums corresponding to the frequency (highly accurate) and amplitude (usually 90%+ accurate) of the input series.\n\n## Usage\n\nExpected input: a path with a file of csv with one row only of floats.\nOutput: \n\n```python3\nimport fourier_sine\nseries = fourier_sine.create_random_series()\noutput = fourier_sine.fourier_analysis(series)\n```\n\nFor inspection you can also:\n\n```python3\nimport plotly\nplotly.plot(series, kind=\'line\', title=\'input\').show()\nplotly.plot(output, kind=\'line\', title=\'output\').show()\n```\n\nInput series composed of three sine waves:\nfrequency 95 amplitude 967, frequency 140 amplitude 731, frequency 170 amplitude 53\n\n![Input wave](wave_to_decompose.png "input wave series")\n\n![Output graph](fourier_output.png "output series")\n\nNotice that the amplitude of the first two waves listed, 967 and 731, respectively reflect the frequency of 95 an 140. Unfortunately, for this example, the amplitude of 53 is too small to detect visually from this graph at the 170 frequency.\n\nCredits: Andrew Matte and Bob Matte, implemented after watching the youtube video [The Algorithm That Transformed The World on the Veritasium channel](https://www.youtube.com/watch?v=nmgFG7PUHfo).',
    'author': 'Andrew Matte',
    'author_email': 'andrew.matte@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
