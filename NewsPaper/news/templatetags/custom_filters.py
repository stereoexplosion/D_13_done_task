from django import template

register = template.Library()


@register.filter()
def censor(value):
    arg = ['путин', 'сука', 'черномазый', 'Путин', 'Сука', 'Черномазый']
    slova = value.split(' ')
    for censura in arg:
        for (index, slovo) in enumerate(slova):
            if slovo == censura:
                slova[index] = slovo[0] + ('*' * (len(slovo) - 1))
    return ' '.join(slova)
