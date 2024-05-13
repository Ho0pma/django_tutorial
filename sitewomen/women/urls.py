from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:post_id>/', views.show_post, name='post'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),

    # path('new/', views.new, name='new'),
    # path('cats/<int:cat_id>/', views.categories, name='cat_id'),
    # path('cats/<slug:slug_id>/', views.categories_by_slug, name='cats'),
    # path('archive/<year4:year>/', views.archive, name='archive'),
    # path('posts/<int:year>', views.posts_list)
]

