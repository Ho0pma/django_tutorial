from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify, cut, first, last, join

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

# пример данных из базы данных
data_db = [

    {'id': 1,
     'title': 'Анджелина Джоли',
     'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
    Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},

    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},

    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},

]

def index(request: HttpRequest):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db
    }

    return render(request, 'women/index_actual.html', context=data)


def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id: {post_id}')

def about(request: HttpRequest) -> HttpResponse:
    data = {
        'title': 'About',
        'menu': menu
    }

    return render(request, 'women/about.html', context=data)

def addpage(request):
    return HttpResponse('Добавление статьи')

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')

# -------------------------------------------------------------------------------------------------------------------- #

# def categories(request, cat_id):
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')
#
#
# def categories_by_slug(request, slug_id):
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>slug: {slug_id}</p>')
#
#
# def archive(request, year):
#     if year > 2024:
#         # raise Http404()
#         # return redirect('home', permanent=True)
#         # return redirect('cats', 'music')
#         # uri = reverse('cats', args=('music', ))
#         # uri = reverse('cats', args=['music'])
#
#         return redirect(reverse('new'))
#
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>year: {year}</p>')
#
#
# def page_not_found(request, exception):
#     return HttpResponseNotFound('<h1>Page not found</h1>')


# def new(request):
#     return HttpResponseNotFound('<h1>new</h1>')

# -------------------------------------------------------------------------------------------------------------------- #
# task: https://stepik.org/lesson/1089285/step/6?auth=login&unit=1099863
# def post_detail(request):
#     if request.GET:
#         return HttpResponse('|'.join(f'{k}={v}' for k, v in request.GET.items()))
#     else:
#         return HttpResponse("GET is empty")

# task: https://stepik.org/lesson/1089285/step/13?auth=login&unit=1099863
# def posts_list(request: HttpRequest, year):
#     if 1990 <= year <= 2023:
#         return HttpResponse(f'posts: {year}')
#
#     raise Http404()

# -------------------------------------------------------------------------------------------------------------------- #
# menu = ['About', 'Add', 'FAQ', 'Log in']
# class MyClass:
#     def __init__(self, a, b):
#         self.a = b
#         self.b = b


# def index(request: HttpRequest):
#     # t = render_to_string('women/index.html')
#     # return HttpResponse(t)
#
#     # task: https://stepik.org/lesson/1089289/step/9?auth=login&unit=1099867
#     # lst = ['main;', 'addpage;', 'contact;', 'about']
#     # f = first(lst)
#     # l = last(lst)
#     # print(cut(f, ';'), cut(l, ';'))
#
#
#     data = {
#         'title': 'главная страница?',
#         'menu': menu,
#         'float': 28.56,
#         'lst': [1, 2, 3, 'afdsa', True],
#         'set': {1, 2, 3, 4, 5},
#         'dict': {'key_1': 'value1', 'key_2': 'value2'},
#         'obj': MyClass(10, 20),
#         'url': slugify('The main page 2'),
#         'test': cut('test: :', ':'),
#         # 'test2': cut(first(['main;', 'addpage;']), ';')
#     }
#
#
#     return render(request, 'women/index.html', context=data)

# -------------------------------------------------------------------------------------------------------------------- #
























