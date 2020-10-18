from django import template
from quesadiya.utils import split_text_into_paragraphs

register = template.Library()


@register.simple_tag
def textSplit(text):
    print(split_text_into_paragraphs("dafdssfd ewrtgwertg"))
    return split_text_into_paragraphs(text)
