from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

# Параметр декоратора takes_context=True сообщает Django, что для работы тега требуется передать контекст.
# context['request'].GET.copy() нам позволяет скопировать все параметры текущего запроса.
# Далее по указанным полям мы просто устанавливаем новые значения, которые нам передали при использовании тега.
# В конце мы кодируем параметры в формат, который может быть указан в строке браузера.
# Тег мы сделали, осталось применить его в шаблоне. Для этого мы добавляем тег в ссылки пагинации.
# Было: <a href="?page=1">1</a>
# Стало: <a href="?{% url_replace page=1 %}">1</a>
