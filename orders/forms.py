from django import forms
from .models import Pedido
from django.core.mail.message import EmailMessage


class PedidoModelForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ['nome', 'sobrenome', 'email', 'endereco', 'cep', 'cidade']

    def send_email(self, pedido):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']

        conteudo = f'Pedido nº {pedido.id}'
        mail = EmailMessage(
            subject=f'Pedido de {nome}',
            body=conteudo,
            from_email='alexgirardello@gmail.com',
            to=[email],
            headers={'Reply-To': email}
        )
        mail.send()
