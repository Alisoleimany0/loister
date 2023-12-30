from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from shop.models import ProductImage, Product


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خود را وارد کنید'}),
    )

    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی خود را وارد کنید'}),
    )

    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل خود را وارد کنید'}),
    )

    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'name': 'password',
                'type': 'password',
                'placeholder': ' رمز بالای 8 کارکتر را وارد کنید و دارای حروف بزرگ و کوچک انگلیسی باشد'
            }
        )
    )

    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'name': 'password',
                'type': 'password',
                'placeholder': 'دوباره رمز خود را وارد کنید'
            }
        )
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class LogoForm(forms.Form):
    image = forms.ImageField()


class CustomChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        """
        Shows an image with the label
        """
        image = conditional_escape(obj.image.url)
        title = conditional_escape(obj.product)

        label = """<img src="%s" alt="%s" width="150" height="150" style="object-fit: cover;"/>""" % (image, title)

        return mark_safe(label)


# class HorizontalRadioSelect(forms.RadioSelect):
#     user renderer template. the IDE won't be able to locate it
#     def render(self, name, value, attrs=None, renderer=None):
#         super().render(name, value, attrs, renderer=renderer)


class ProductAdminForm(forms.ModelForm):
    default_image = CustomChoiceField(
        queryset=ProductImage.objects.none(),
        widget=forms.RadioSelect,
        required=False
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            queryset = ProductImage.objects.filter(product=self.instance)
            self.fields['default_image'].queryset = queryset
            self.fields['default_image'].initial = queryset.get(is_default=True)

    def save(self, commit=True):
        queryset = ProductImage.objects.filter(product=self.instance)
        queryset.update(is_default=False)
        image = self.cleaned_data['default_image']
        image.is_default = True
        image.save()
        return super().save(commit)
