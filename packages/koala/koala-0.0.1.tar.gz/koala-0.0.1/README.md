## Description
[KLayout](https://www.klayout.de/) is an opensource and powerful mask design software. Thanks to its Ruby and Python APIs, programming extensions are available to the users. To simplify this programming aspect, Automated Mask Design Klayout (AMDK) has been created allowing a higher-level language and ease of use.

You will find the installation instructions as well as requirements below and a variety of examples to get you started! 

## What is gitlab and how does it work

## How does KLayout work

## Installation
- Download [Anaconda](https://www.anaconda.com/)
- Open Anaconda Prompt (Anaconda3)
- Type `conda create --name AMDK` and accept by typing `y`. This will create a new environment specific for AMDK
- Type `conda activate AMDK`. This will move you inside this new environment
- Type `conda install pip`and accept by typing `y`. Pip is a package installer for python and will be used to install necessary packages for making AMDK run
- Type `pip install klayout`and accept by typing `y`. KLayout package is now installed inside AMDK environment
- To make sure everything went well, type `conda list` and check if Klayout is listed. This command list every package that is installed in the environment that you are currently in
- Install a Integrated Development Environment (IDE) for python. We recommend you to install the community version of [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows).
- Open PyCharm, click at the bottom right to change your interpreter, and click on `Add interpreter`
- On the menu, click on `Conda Environment` and select the recently created AMDK environment. Your interpreter is now the one from the AMDK environment

## Roadmap
- [ ] How to pull this repository
- [ ] Working principle of KLayout
- [ ] Implementation of the functionHelper
- [ ] 3 basic examples
- [ ] 3 advanced examples

## Contributing
This repository has been created by Imke Krauhausen and Charles-Théophile Coen. We are responsible for the development and maintenance of AMDK. If you wish to contribute, please contact us by email!

## Project status
![25%](https://progress-bar.dev/25) Setting up gitlab
