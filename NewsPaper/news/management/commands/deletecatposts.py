from django.core.management.base import BaseCommand, CommandError
from ...models import PostCategory, Category, Post


def categories_list_command():
    return Category.objects.all().values_list('category_name', flat=True)


def posts_id_for_del_command(answer_1):
    return PostCategory.objects.filter(category_id=Category.objects.get(
        category_name=answer_1).id).values_list('post_id', flat=True)


class Command(BaseCommand):
    help = 'Удаляет ВСЕ посты выбранной категории'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(
            'Введите точное название категории, посты которой хотите удалить')
        answer_1 = input()
        if answer_1 in categories_list_command():
            self.stdout.write(
                'Точно хотите удалить ВСЕ посты данной категории? yes/no')
            answer_2 = input()
            if answer_2 == 'yes':
                for _id in posts_id_for_del_command(answer_1):
                    Post.objects.get(id=_id).delete()
                self.stdout.write(self.style.SUCCESS('Успешно удалено!'))
                return
            self.stdout.write(self.style.ERROR('Значит, в другой раз!'))

        else:
            self.stdout.write(self.style.ERROR('Такой категории нет!'))
            return
