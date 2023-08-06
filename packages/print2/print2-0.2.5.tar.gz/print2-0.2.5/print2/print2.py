from termcolor import colored


def print2(
    text: str, indent: str = "\t", prefix: str = "", level: int = 0, color: str = ""
):
    if is_multiline(text):
        for line in text.splitlines():
            print2(text=line, prefix=prefix, indent=indent, level=level, color=color)
        return
    if not color:
        print(f"{indent*level}{prefix}{text}")
        return
    print(colored(f"{indent*level}{prefix}{text}", color))
    return


def is_multiline(text):
    # https://docs.python.org/3/glossary.html#term-universal-newlines
    # A manner of interpreting text streams in which all of the following
    # are recognized as ending a line: the Unix end-of-line convention '\n',
    # the Windows convention '\r\n', and the old Macintosh convention '\r'.
    # See PEP 278 and PEP 3116, as well as bytes.splitlines() for an additional use.
    if "\n" in text:
        return True
    if "\r" in text:
        return True
    return False


class Print2:

    prefix = ""
    indent = "\t"
    level = 0

    def __init__(
        self, prefix: str = "", indent: str = "\t", level: int = 0, output: int = True
    ):
        self.prefix = prefix
        self.indent = indent
        self.level = level
        self.output = output
        self.level_tmp = 0

    def set_prefix(self, prefix: str) -> None:
        self.prefix = prefix

    def get_prefix(self) -> str:
        return self.prefix

    def set_indent(self, indent: str) -> None:
        self.indent = indent

    def get_indent(self) -> str:
        return self.indent

    def set_output(self, output: bool = True) -> None:
        self.output = output

    def get_output(self) -> bool:
        return self.output

    def set_level(self, level: int) -> None:
        self.level = level

    def set_tmp_level(self, level: int) -> None:
        self.level_tmp = level

    def inc_level(self) -> None:
        self.level = self.level + 1

    def get_level(self) -> int:
        return self.level

    def print(self, text, color: str = "", output: bool = None):
        if (self.output and output is not False) or output:
            if self.level_tmp:
                print2(
                    text=text,
                    prefix=self.prefix,
                    indent=self.indent,
                    level=self.level_tmp,
                    color=color,
                )
                self.level_tmp = 0
                return
            print2(
                text=text,
                prefix=self.prefix,
                indent=self.indent,
                level=self.level,
                color=color,
            )
        return
