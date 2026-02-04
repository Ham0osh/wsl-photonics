# For simulating photonic components

> Author: Hamish J
> Date: Feb 03, 2026

This repository holds code from [byucamacholab Photonics Bootcamp](https://byucamacholab.github.io/Photonics-Bootcamp/index.html) to simulate various passive components as a lighter weight alternative to Lumerical.

## Install
1. Be using WSL or Linux
2. Install miniconda
3. Install the following:

`conda create --name photonics python=3.11`

`conda activate photonics`

`conda install -c conda-forge pymeep pymeep-extras`

`pip install -r requirements.txt`