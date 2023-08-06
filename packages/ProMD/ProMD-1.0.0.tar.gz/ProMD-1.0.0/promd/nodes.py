class Header:

    def __init__(self, text: str = None, level: int = 1):
        self.level = level
        self.text = text

    def __str__(self):
        header = '#' * self.level

        return f'{header} {self.text}\n'


class Text:

    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text + '\n'


class Code:

    def __init__(self, code: str, highlight: str = None):
        self.code = code
        self.format = highlight

    def __str__(self):
        string = '```'
        string += self.format + '\n' if self.format is not None else ''
        string += self.code + ('\n```' if self.format is not None else '```')

        return string


class URL:

    def __init__(self, text: str, url: str):
        self.text = text
        self.url = url

    def __str__(self):
        return f'[{self.text}]({self.url})'


class OrderedList:

    def __init__(self, item_list: list):
        self.item_list = item_list

    def __str__(self):
        return ('\n'.join(
            f'{index + 1}. {item}'
            for index, item in enumerate(self.item_list)
        )) + '\n\n'


class EmbedNode(URL):

    def __str__(self):
        return f'![]({self.url})'


class Bold(Text):

    def __str__(self):
        return f'**{self.text}**'


class Cursive(Text):

    def __str__(self):
        return f'*{self.text}*'


class UnorderedList(OrderedList):

    def __str__(self):
        return ('\n'.join(
            '- ' + str(item)
            for item in self.item_list
        )) + '\n\n'


class Table:

    def __init__(self, elements: list):
        self.arrays = elements

    def __str__(self):
        result = ' | '.join(header.name for header in self.arrays) + '\n'
        result += ' | '.join(
            '-' * len(header.name)
            for header in self.arrays
        ) + '\n'

        for index, _ in enumerate(self.arrays[0].array):
            result += ' | '.join(array.array[index] for array in self.arrays)
            result += '\n'

        return result


class Array:

    def __init__(self, name: str, array: list):
        self.array = array
        self.name = name
