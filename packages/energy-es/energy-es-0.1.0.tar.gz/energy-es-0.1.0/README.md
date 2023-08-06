# Energy-ES
Energy-ES is a Python desktop application that shows an interactive chart with
the hourly values of the Spot Market and PVPC energy prices of the current day
in Spain. The data is provided by some APIs of *Red Eléctrica de España*.

- Version: 0.1.0
- Author: Jose A. Jimenez (jajimenezcarm@gmail.com)
- License: MIT License
- Repository: https://github.com/jajimenez/energy-es

![Screenshot](images/screenshot.png)

## How to install

We can install Energy-ES through the PyPI (Python Package Index) repository:

```bash
pip install --upgrade pip
pip install energy-es
```

## How to run

Once Energy-ES is installed, we can run it with this command:

```bash
energy-es
```

## How to run the unit tests

To run all the unit tests, run the following command from the project
directory:

```bash
python -m unittest discover test
```

## How to build the Wheel package

To generate the Wheel package of Energy-ES, run the following commands from the
project directory:

```bash
python setup.py bdist_wheel
```

Before running the above command for the first time, we need to install 
***wheel*** from PyPI (not to be confused with the wheel package of Energy-ES):

```bash
pip install wheel
```

## How to build the Source package

To generate the Source package of Energy-ES, run the following commands from
the project directory:

```bash
python setup.py sdist
```
