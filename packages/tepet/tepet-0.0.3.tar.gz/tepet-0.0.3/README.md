# tepet
**TE**mporal **PE**rformance **T**ool

~~25-cent term for a 5-cent concept!~~

[![PyPI](https://img.shields.io/pypi/v/tepet)](https://pypi.org/project/tepet/)
[![Test Python package](https://github.com/Toshakins/tepet/actions/workflows/python-package.yml/badge.svg)](https://github.com/Toshakins/tepet/actions/workflows/python-package.yml)

## What is this
tepet is a small utility to help you understand and track execution time of your code. You could write it anytime, but why do this every other day?

## Usage
Can be used as a context manager
```python
from tepet import Timer
with Timer():
  print('doing stuff...')

# Output:
#
# > 2020 May 31 20:11:49 +0000 ==== started
# > doing stuff...
# > 2020 May 31 20:11:49 +0000 ==== elapsed 0.00000 seconds
```
and a function decorator
```python
from tepet import Timer
@Timer()
def work():
  print("working...")

work()

# Output:
#
# > 2020 May 31 20:14:25 +0000 ==== started
# > working...
# > 2020 May 31 20:14:25 +0000 ==== elapsed 0.00001 seconds
