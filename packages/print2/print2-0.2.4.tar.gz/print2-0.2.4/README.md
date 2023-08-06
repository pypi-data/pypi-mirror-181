# PrettyPrint

## Simple Example

```python
from src.prettyprint.PrettyPrint import prett_print

pretty_print("Hello world !", prefix="### ", indent="\t", color="green", level=2)
```

### Result

<span style="color:green;padding:30pt;">
                ### Hello world !
</span>

## Advanced example

```python
from src.prettyprint.PrettyPrint import PrettyPrint

pp = PrettyPrint(prefix="* ", level=1)

pp.print(
    """LINE 1
LINE 2
"""
)

pp.set_level(2)
pp.set_prefix("# ")

pp.print(
    """AAAA
BBB
CCC
DDD
EEE
FFF
"""
)

pp.inc_level()

pp.print("Final")

```