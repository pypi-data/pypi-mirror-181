# Print2

## Simple Example

```python
from print2 import pprint

pprint("Hello world !", prefix="### ", indent="\t", color="green", level=2)
```

### Result

<span style="color:green;padding:30pt;">
                ### Hello world !
</span>

## Advanced example

```python
from print2 import PPrint

pp = PPrint(prefix="* ", level=1)

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