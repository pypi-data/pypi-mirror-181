

# Nonholonomics

[![GitHub Issues](https://img.shields.io/badge/issue_tracking-github-blue.svg)](https://github.com/ardiste3/nonholonomics/issues)


See the [AUTHORS](AUTHORS) file for the list of authors.
Currently we only have one. It gets lonely so join the team!

License: New GNU License (see the [LICENSE](LICENSE) file for details) covers all
files in the nonholonomics repository unless stated otherwise.

See the [CONTRIBUTING](CONTRIBUTING) file for ways to contribute. 

Nonholonomics aims to become a central location for all things nonholonomic! We aim to centralize common methods for easy access and easy manipulation. Currently, the methods of solving nonholonomic systems in python are restricted to self built programs of by making use of Sympy's Lagrange multiplier method. 

Currently, nonholonomics is still in development. We have implemented a module to evaluate the nonholonomic Lagrange equations. This is a first step in producing modules to be tested. 

We also have a module for plotting purposes. In dynamics, we often plot the states of the system. The functions contained in this module aim to make this quick and easy. 

We have made a handful of examples for users to get familliar with. The examples are located in the examples directory and are simply numbered to keep naming short and easy. 

For a complte example using a holonomic linear system, take a look at example1.py for an indepth look at how to use most of the methods and classes.

Example2.py and example3.py compare the implementation of constraints. The current program will handle systems with and with out nonholonomoic constraints. 

Example4.py shows the program can evaluate a nonlinear system. In this case it is the pendulum. There are comments to make the system linear to compare the results. 

We are working on implementing support for Lagrange multipliers and the principal of virtual power. If you would like to help please check out the contributing documentation.

## Download

The recommended installation method is through pip,
we are not on pypi yet, we use test.pypi until our first launch. 

to in install from test.pypi, use:

    $ pip install -i https://test.pypi.org/simple/ nonholonomics

You can also get the latest version of nonholonomics from
<https://test.pypi.org/simple/ nonholonomics>

To get the git version do

    $ git clone https://github.com/ardiste3/nonholonomics

For other options (tarballs, debs, etc.), please wait patiently or email your request in.


## Contributing

We welcome contributions from anyone, even if you are new to open
source.

## Clean

To clean everything (thus getting the same tree as in the repository):

    $ git clean -Xdf

which will clear everything ignored by `.gitignore`, and:

    $ git clean -df

to clear all untracked files. You can revert the most recent changes in
git with:

    $ git reset --hard

WARNING: The above commands will all clear changes you may have made,
and you will lose them forever. Be sure to check things with `git
status`, `git diff`, `git clean -Xn`, and `git clean -n` before doing any
of those.

## Bugs

Our issue tracker is at <https://github.com/ardiste3/nonholonomics/issues>. Please
report any bugs that you find. Or, even better, fork the repository on
GitHub and create a pull request. We welcome all changes, big or small,
and we will help you make the pull request if you are new to git.

## Brief History
This started out as project in graduate school. 

