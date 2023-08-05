## Page Object Elements

Dist: [pypi.org](https://pypi.org/project/page-object-elements/)

### Installation

`pip install page-object-elements`

### Aspect Logger

To customize behaviour of **poe** logger, `poe.ini` should be in the root of project (or in some child dirs). If not
present or some of the values aren't set in `poe.ini` (**e.g** `logs_absolute_path`) default values will be applied.

```
poe.ini

[LOGGER]
level = DEBUG
log_name = log
stdout = True
logs_absolute_path = C:\Users\<username>\workspace\<project>
```