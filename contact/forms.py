
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from . import models


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
    )

    email = forms.EmailField()
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2'
        )

    # O método clean, serve ara validações e checar se existe tal informaçao no banco de dados. Sempre definir como 'clean_nome_do_campo'
    def clean_email(self):
        email = self.cleaned_data.get('email')

        
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe este e-mail', code='invalid')
            )

        return email

class ContactForm(forms.ModelForm):
    # Forma de modificar os campos no html através de Widgets.
    # https://docs.djangoproject.com/en/4.2/ref/forms/widgets/
    # def __init__(self,*args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields['first_name'].widget.attrs.update({
    #         'placeholder': 'Aqui veio do init'
    #     })

    # Outra forma de modificar através do widget.
    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Aqui veio do modelo'
            }
        ),
        label='Primeiro Nome',
        help_text='Texto de ajuda para o usuário'
    )

    picture = forms.ImageField(
        widget = forms.FileInput(
            attrs = {
                'accept': 'image/*'
            }
        )
    )

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture'
        )
    
    def clean(self):
        cleaned_data = self.cleaned_data 
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'O primeiro nome não pode ser igual ao sobrenome',
                code='invalid'
            )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        return super().clean()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if first_name == "ABC":
            self.add_error(
                'first_name',
                ValidationError(
                    'Mensagem de erro',
                    code='invalid'
                )
            )
        return first_name

class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=30,
        help_text='Required.',
        error_messages={
            'min_length': 'Por favor, adicione mais de duas letras.'
        }
    )

    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=30,
        help_text='Required'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete":"new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete":"new-password"}),
        help_text='Use a mesma senha anterior',
        required=False
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1