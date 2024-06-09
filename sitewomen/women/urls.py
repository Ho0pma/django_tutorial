from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.WomenHome.as_view(), name='home'),


    path('about/', views.about, name='about'),

    # path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),

    # path('addpage/', views.addpage, name='add_page'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),

    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),

    # path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),

    # path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('tag/<slug:tag_slug>/', views.ShowTagPostList.as_view(), name='tag'),

    path('edit/<slug:edit_slug>/', views.UpdatePage.as_view(), name='edit_page'),

    # path('new/', views.new, name='new'),
    # path('cats/<int:cat_id>/', views.categories, name='cat_id'),
    # path('cats/<slug:slug_id>/', views.categories_by_slug, name='cats'),
    # path('archive/<year4:year>/', views.archive, name='archive'),
    # path('posts/<int:year>', views.posts_list)
]

