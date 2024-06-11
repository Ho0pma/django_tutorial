from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify, cut, first, last, join
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from unidecode import unidecode

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin


class WomenHome(DataMixin, ListView):
    template_name = 'women/index_actual.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related('cat')


class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    context_object_name = 'post' # чтобы использовать в html доке именно posts, а не object
    slug_url_kwarg = 'post_slug' # чтобы использовать в url именно post_slug

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # первым параметром передаем полученные данные (context), вторым - доп параметры
        # обязательно через именованный, чтобы сформировался именно такой ключ
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

@login_required(login_url='users:login')
def about(request: HttpRequest) -> HttpResponse:
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'title': 'О сайте',
        'page_obj': page_obj,
    }

    return render(request, 'women/about.html', context=data)


class AddPage(LoginRequiredMixin, DataMixin, FormView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    # login_url = '/admin/' # редирект неавторизованного пользователя

    # старый вар сохранения слага
    # def form_valid(self, form):
    #     form.cleaned_data['slug'] = slugify(unidecode(form.cleaned_data['title']))
    #     form.save()
    #     return super().form_valid(form)

    def form_valid(self, form):
        w = form.save(commit=False)  # Создаем экземпляр модели без сохранения в бд
        w.author = self.request.user  # Устанавливаем автора
        w.slug = slugify(unidecode(form.cleaned_data['title']))  # Генерируем slug на основе заголовка
        w.save()  # Сохраняем экземпляр модели в бд
        return super().form_valid(form)



class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
    success_url = reverse_lazy('home')
    template_name = 'women/addpage.html'
    slug_url_kwarg = 'edit_slug' # если хотим, отбирать по слагу
    title_page = 'Редактирование статьи'

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index_actual.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')

class ShowTagPostList(DataMixin, ListView):
    template_name = 'women/index_actual.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(
            context,
            title=f'Тег: {tag.tag}',
            posts=tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
        )

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

















