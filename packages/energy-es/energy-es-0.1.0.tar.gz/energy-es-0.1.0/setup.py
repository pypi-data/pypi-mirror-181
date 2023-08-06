"""Energy-ES - Setup."""

import setuptools as st


if __name__ == "__main__":
    with open("README.md") as f:
        long_desc = f.read()

    with open("requirements.txt") as f:
        requirements = [i.replace("\n", "") for i in f.readlines()]

    st.setup(
        name="energy-es",
        version="0.1.0",
        description=(
            "Desktop application that shows an interactive chart with the "
            "hourly values of the Spot Market and PVPC energy prices of the "
            "current day in Spain."
        ),
        author="Jose A. Jimenez",
        author_email="jajimenezcarm@gmail.com",
        license="MIT",
        long_description=long_desc,
        long_description_content_type="text/markdown",
        url="https://github.com/jajimenez/energy-es",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: MIT License"
        ],
        python_requires=">=3.9.0",
        install_requires=requirements,
        packages=[
            "energy_es",
            "energy_es.data",
            "energy_es.ui"
        ],
        package_dir={
            "energy_es": "src/energy_es",
            "energy_es.data": "src/energy_es/data",
            "energy_es.ui": "src/energy_es/ui"
        },
        package_data={
            "energy_es.ui": ["images/*.png"]
        },
        entry_points={
            "console_scripts": [
                "energy-es=energy_es:main"
            ]
        }
    )
