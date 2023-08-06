# mkapi-fix-coz
A fork of [mkapi-fix](https://github.com/pwwang/mkapi) to fit our needs and gives publishing control. Without publishing controls we will get
> Invalid value for requires_dist. Error: Can't have direct dependency: 

when trying to publish to PyPi with a dependency based on a Git commit hash. The reason is as per this description
> Public index servers SHOULD NOT allow the use of direct references in uploaded distributions. Direct references are intended as a tool for software integrators rather than publishers.

as described here https://peps.python.org/pep-0440/#direct-references

## Install
```bash
pip install mkapi-fix-coz
```
