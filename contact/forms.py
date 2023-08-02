
from django import forms
from django.core.exceptions import ValidationError
from . import models

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
        help_text='Texto de ajuda para o usuário',
    )

    picture = forms.ImageField(
        widget = forms.FileInput(
            attrs = {
                'accept': 'image/*',
            }
        )
    )

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture',
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
                    code='invalid',
                )
            )
        return first_name