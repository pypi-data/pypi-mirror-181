# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['goats', 'goats.core', 'goats.eprem']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'netCDF4>=1.5.8,<2.0.0',
 'numpy>=1.21.4,<1.23',
 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'goats',
    'version': '0.1.0',
    'description': 'A set of tools for analyzing heliophysical datasets',
    'long_description': "# GOATS\n\nA set of tools for analyzing heliophysical datasets\n\nThe Generalized Observing Application Tool Suite (GOATS) is a collection of objects that support interactive and scripted analysis of simulated and observed data in heliophysics.\n\n## Installation\n\n```bash\n$ pip install goats\n```\n\n## Usage Example: EPREM\n\nThe [Energetic Particle Radiation Environment Module](https://github.com/myoung-space-science/eprem) (EPREM) simulates acceleration and transport of energetic particles throughout the heliosphere by modeling the focused transport equation on a Lagragian grid in the frame co-moving with the solar wind. It was the primary motivation for developing this package.\n\nThe first thing we'll do is import the packages we need.\n\n* `pathlib` is the built-in package for working with system paths  \n* `matplotlib` is a popular third-party package for creating figures  \n* `eprem` is the GOATS subpackage for working with EPREM output  \n\n\n```python\nimport pathlib\n\nimport matplotlib.pyplot as plt\n\nfrom goats import eprem\n```\n\nNext, we'll create a stream observer, which is the type of observer that corresponds to an EPREM output file with a name like `obs######.nc`. This invokation assumes that the data file, as well as an EPREM runtime parameter file called `eprem_input_file`, are in a local subdirectory called `data`.\n\nNote that if the data file is in the current directory, you can omit `source=<path/to/data>`.\n\n\n```python\nstream = eprem.Stream(350, source='data/example', config='eprem_input_file')\n```\n\nWe can request the value of simulation runtime parameters by aliased keyword. For example, let's check the assumed mean free path at 1 au.\n\n\n```python\nprint(stream['lambda0'])\n```\n\n    'lam0 | lambda0 | lamo': [1.] [au]\n\n\nThe text tells us that this simulation run used a value of 1.0 au (astronomical unit) for this parameter. It also suggests that we could have requested this value by the keywords 'lamo' or 'lam0'.\n\n\n```python\nprint(stream['lamo'])\nprint(stream['lam0'])\n```\n\n    'lam0 | lambda0 | lamo': [1.] [au]\n    'lam0 | lambda0 | lamo': [1.] [au]\n\n\nWe can also request observable quantities by aliased keyword. Here is the radial velocity.\n\n\n```python\nvr = stream['Vr']\nprint(vr)\n```\n\n    Observable('Vr', unit='m s^-1')\n\n\nThe text tells us that the radial velocity output array has a time axis and a shell axis. EPREM shells are logical surface of nodes in the Lagrangian grid. Each shell index along a given stream represents one node. We can observe radial velocity at a single time (e.g., 1 hour of real time since simulation start) on a single node as follows:\n\n\n```python\nt0 = 1.0, 'hour'\nvr.observe(time=t0, shell=1000)\n```\n\n\n\n\n    Observation(unit='m s^-1', dimensions=['time', 'shell'])\n\n\n\nIn the case of a constant isotropic solar wind, the stream nodes would extend radially outward from the Sun; with some trial-and-error, we could figure out which shell is closest to a particular radius (e.g., 1 au).\n\nInstead, we often want to interpolate an observation to the radius of interest.\n\n\n```python\nobserved = vr.observe(radius=[0.1, 'au'])\n```\n\nNow that we have an observation of the radial velocity at 0.1 au as a function of time, we can plot it. First, we'll define intermediate variables to hold the time in hours and the radial velocity in kilometers per second.\n\n\n```python\ntime = observed['time']\n```\n\nNext, we'll make sure there's a `figures` directory (to avoid cluttering the current directory) and load the plotting library.\n\n\n```python\nfigpath = pathlib.Path('figures').resolve()\nfigpath.mkdir(exist_ok=True)\n```\n\nFinally, we'll create and save the plot.\n\n\n```python\nplt.plot(time['hour'], observed['km / s'].array)\nplt.xlabel('Time [hours]')\nplt.ylabel('Vr [km/s]')\nplt.savefig(figpath / 'vr-hours.png')\n```\n\n\n    \n![png](readme_files/readme_25_0.png)\n    \n\n\nThere are many other observable quantities available to an observer, and they are not limited to those in the observer's source data.\n\n\n```python\nprint('flux' in stream.observables)\nprint('mean free path' in stream.observables)\n```\n\n    True\n    True\n\n\n\n```python\nstream['flux']\n```\n\n\n\n\n    Observable('flux', unit='J^-1 s^-1 sr^-1 m^-2')\n\n\n\n\n```python\nstream['mean free path']\n```\n\n\n\n\n    Observable('mean free path', unit='m')\n\n\n\nWe can even create observable quantities by symbolically composing existing observable quantities\n\n\n```python\nstream['mfp / Vr']\n```\n\n\n\n\n    Observable('mfp / Vr', unit='s')\n\n\n\n\n```python\nstream['rho * energy']\n```\n\n\n\n\n    Observable('rho * energy', unit='kg m^-1 s^-2')\n\n\n\nNote that the unit is consistent with the composed quantity and that the axes of the composed quantity represent the union of the axes of the component quantities.\n\nTo illustrate full use of a composed quantity, consider observing the ratio of the mean free path of protons with 1 and 5 MeV to the radial velocity of the solar wind.\n\n\n```python\nobserved = stream['mfp / Vr'].observe(radius=[0.1, 'au'], energy=[1, 5, 'MeV'])\nlines = plt.plot(observed['time']['hour'], observed.array)\nlines[0].set_label('1 MeV')\nlines[1].set_label('5 MeV')\nplt.xlabel('Time [hours]')\nplt.ylabel('mfp / Vr [s]')\nplt.legend()\nplt.savefig(figpath / 'mfp_vr-hours.png')\n```\n\n\n    \n![png](readme_files/readme_35_0.png)\n    \n\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`goats` was created by Matt Young. It is licensed under the terms of the GNU General Public License v3.0 license.\n\n## Credits\n\n`goats` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n\n",
    'author': 'Matt Young',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
