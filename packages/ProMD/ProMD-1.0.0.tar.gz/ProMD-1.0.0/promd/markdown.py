from .nodes import *


class Markdown:

    def __init__(self, output: str = None):
        self.output = output
        self.markdown = ''

    def header(self, title: str, level: int = 1) -> Header:
        node = Header(title, level)
        self.markdown += node.__str__()

        return node

    def url(self, text: str, url: str) -> str:
        node = URL(text, url)

        return node.__str__()

    def embed(self, text: str, url: str) -> EmbedNode:
        node = EmbedNode(text, url)
        self.markdown += node.__str__()

        return node

    def text(self, text: str) -> Text:
        node = Text(text)
        self.markdown += node.__str__()

        return node

    def bold(self, text: str) -> str:
        node = Bold(text)

        return node.__str__()

    def ordered_list(self, items: list) -> str:
        node = OrderedList(items)
        self.markdown += node.__str__()

        return node.__str__()

    def unordered_list(self, items: list) -> str:
        node = UnorderedList(items)
        self.markdown += node.__str__()

        return node

    def table(self, table: dict[str]) -> Table:
        node = Table(table)
        self.markdown += node.__str__()

        return node

    def code(self, file: str = None, format: str = None) -> str:
        with open(file, 'r') as content:
            node = Code(content.read(), format)

        return node.__str__()

    def save(self) -> None:
        if self.output is None:
            return None

        with open(self.output, 'w') as output:
            output.write(self.markdown)
