from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify, cut, first, last, join
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from unidecode import unidecode

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

# пример данных из базы данных
# data_db = [
#
#     {'id': 1,
#      'title': 'Анджелина Джоли',
#      'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
#     Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
#      'is_published': True},
#
#     {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
#
#     {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
#
# ]

# # имитация дб для вывода категорий
# cats_db = [
#     {'id': 1, 'name': 'Актрисы'},
#     {'id': 2, 'name': 'Певицы'},
#     {'id': 3, 'name': 'Спортсменки'},
# ]

def index(request: HttpRequest):
    # posts = Women.objects.filter(is_published=False)
    posts = Women.objects.all().select_related('cat')

    # свой менеджер
    # posts = Women.published.all().select_related('cat')

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index_actual.html', context=data)

class WomenHome(ListView):
    model = Women
    template_name = 'women/index_actual.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related('cat')

# class WomenHome(TemplateView):
#     template_name = 'women/index_actual.html'
#     extra_context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': Women.objects.all().select_related('cat'),
#         'cat_selected': 0,
#     }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #
    #     return  context



def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1
    }

    return render(request, 'women/post.html', context=data)

# def handle_uploaded_file(f):
#     with open(f"upload/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

class ShowPost(DetailView):
    # model = Women # если есть get_object то не нужна эта строка
    template_name = 'women/post.html'
    context_object_name = 'post' # чтобы использовать в html доке именно posts, а не object
    slug_url_kwarg = 'post_slug' # чтобы использовать в url именно post_slug

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    # фильтр, чтобы запретить вывод неопубликованных статей
    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

def about(request: HttpRequest) -> HttpResponse:

    # if request.method == 'POST':
    #     handle_uploaded_file(request.FILES['file_upload'])

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    data = {
        'title': 'About',
        'menu': menu,
        'form': form
    }

    return render(request, 'women/about.html', context=data)

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)

        if form.is_valid():
            # автоматически делается слаг
            form.cleaned_data['slug'] = slugify(unidecode(form.cleaned_data['title']))
            form.save()
            return redirect('home')

    else:
        form = AddPostForm()

    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'women/addpage.html', context=data)

class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }

    def form_valid(self, form):
        form.cleaned_data['slug'] = slugify(unidecode(form.cleaned_data['title']))
        print(form.cleaned_data)
        form.save()
        return super().form_valid(form)

# тестовый пример с классом View
# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#
#         return render(request, 'women/addpage.html', context=data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             # автоматически делается слаг
#             form.cleaned_data['slug'] = slugify(unidecode(form.cleaned_data['title']))
#             form.save()
#             return redirect('home')
#
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', context=data)


def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def show_category(request, cat_slug):
    # выбирается запись из модели Category по слагу
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk
    }

    return render(request, 'women/index_actual.html', context=data)

class WomenCategory(ListView):
    template_name = 'women/index_actual.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')

def show_tag_postlist(request, tag_slug):
    # читаем пост из модели, где slug=tag_slug. Это будет точно одна запись, тк slug в бд uniq.
    # tag - это объект TagPost
    tag = get_object_or_404(TagPost, slug=tag_slug)

    # через параметр related_names (tags), который связывает две модели (вторичный ключ), можем
    # выбрать только те, что опубликованы.
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

    # формируем словарь, который будем передавать в шаблон
    data = {
        # второй tag - это один из атрибутов модели TagPost
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,

        # если None ничего не будет отображаться синим
        'cat_selected': None
    }

    return render(request, 'women/index_actual.html', context=data)

class ShowTagPostList(ListView):
    template_name = 'women/index_actual.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = f'Тег: {tag.tag}'
        context['menu'] = menu
        context['posts'] = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
        context['cat_selected'] = None

        return context

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')



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
























