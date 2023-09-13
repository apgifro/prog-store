from django import forms


class CarrinhoAddProdutoForm(forms.Form):
    CHOICES = [(i, str(i)) for i in range(1,21)]
    quantidade = forms.TypedChoiceField(choices=CHOICES, coerce=int)
    atualizar = forms.BooleanField(required=False,
                                   initial=True, # EDITADO POR ALEXANDRE
                                   widget=forms.HiddenInput)
