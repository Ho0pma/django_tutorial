from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import slugify
from unidecode import unidecode
from .models import Category, Husband, Women


# свой валидатор
@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)

class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='не замужем', label='Замужем за')
    is_published = forms.BooleanField(initial=True, required=False)
    class Meta:
        model = Women
        # fields = '__all__'
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }

        labels = {
            'content': 'Контик'
        }

    # метод для сохранения слага
    # # TODO: вынести в модель
    # def save(self, commit=True):
    #     model = super().save(commit=False)
    #     model.slug = self.cleaned_data['slug']
    #     model.save()

    def save(self, commit=True):
        model = super().save(commit=False)
        # Получаем slug из cleaned_data, если он есть
        model.slug = self.cleaned_data.get('slug', model.slug)
        if commit:
            model.save()
        return model


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')