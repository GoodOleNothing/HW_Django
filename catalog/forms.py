from django import forms
from .models import Product
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def clean(self):
        cleaned_data = super().clean()
        forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно",
                           "обман", "полиция", "радар"]

        for field in ["name", "description"]:
            value = cleaned_data.get(field, "")
            for word in forbidden_words:
                if word.lower() in value.lower():
                    raise ValidationError(f"Слово '{word}' нельзя использовать.")
        return cleaned_data

    def clean_price(self):
        if self.cleaned_data['price'] < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return self.cleaned_data['price']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название товара'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание товара'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену товара'})

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError("Размер файла превышает 5 МБ.")

            extensions = ['jpeg', 'png']
            if image.content_type not in extensions:
                raise ValidationError("Только файлы JPEG и PNG.")

        return image

