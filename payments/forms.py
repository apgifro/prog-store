from django import forms


class CheckoutForm(forms.Form):
    payment_method_noncwe = forms.CharField(max_length=500, widget=forms.widgets.HiddenInput, required=False)
    
    def clean(self):
        self.cleaned_data = super().clean()
        if not self.cleaned_data.get('payment_method_nonce'):
            raise forms.ValidationError('Não foi possível processar o pagamento. Tente novamente.')
        return self.cleaned_data