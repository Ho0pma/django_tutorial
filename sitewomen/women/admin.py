from django.contrib import admin
from django.core.checks import messages
from django.db.models.functions import Length

from women.models import Women, Category, Husband


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        if self.value() == 'single':
            return queryset.filter(husband__isnull=True)


# Register your models here.
@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    # поля, которые будут видны при добавлении
    fields = ['title', 'slug', 'content', 'cat', 'husband', 'tags']

    # исключения полей из выборки при добавлении новой записи
    # exclude = ['tags', 'is_published']

    # поля только для чтения при просмотре записи
    # readonly_fields = ['slug']

    # горизонтальное отображение
    filter_horizontal = ['tags']

    # вертикальное отображение
    # filter_vertical = ['tags']

    # автоматическое формирование слага (не должен повторяться в readonly_fields)
    prepopulated_fields = {'slug': ['title']}

    # поля для вывода в админке
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat', 'brief_info')

    # кликабельные поля:
    list_display_links = ('id', 'title')

    # сначала сортировка по time_create, если одинаковые знач - по title
    ordering = ['time_create', 'title']

    # чтобы поле было редактируемым
    list_editable = ('is_published',)

    # ограничение вывода
    list_per_page = 5

    # для регистрации действий
    actions = ('set_published', 'set_draft')

    # поисковая строка (по чему будет поиск)
    search_fields = ('title__startswith', 'cat__name')

    # панель с фильтрами
    list_filter = (MarriedFilter, 'cat__name', 'is_published')

    # формирование своего поля, которого нет в бд
    @admin.display(description='Кол-во символов', ordering=Length('content'))
    def brief_info(self, women: Women):
        return f'Описание содержит {len(women.content)} символов'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Убрать из публикации статьи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{count} записей было убрано', messages.WARNING)


# admin.site.site_header = 'Панель администрирования'
# admin.site.index_title = 'Известные женщины мира'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


