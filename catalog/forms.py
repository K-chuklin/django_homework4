from django import forms

from catalog.models import Product, Version

error_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        for word in error_words:
            if word in cleaned_data:
                raise forms.ValidationError(f'Присутствует запрещенное слово {word}!')
        return cleaned_data

    def clean_desc(self):
        cleaned_data = self.cleaned_data['description']
        for word in error_words:
            if word in cleaned_data:
                raise forms.ValidationError(f'Присутствует запрещенное слово {word}!')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
