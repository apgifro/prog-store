from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View, TemplateView
from app.models import Produto
from .carrinho import Carrinho
from .forms import CarrinhoAddProdutoForm


class CarrinhoAdd(FormView):
    form_class = CarrinhoAddProdutoForm
    success_url = reverse_lazy('carrinhodetalhe')

    def post(self, request, *args, **kwargs):
        self.produto = Produto.objects.get(id=kwargs['idprod'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        carrinho = Carrinho(self.request)
        carrinho.add_produto(produto=self.produto,
                            quantidade=cd['quantidade'],
                            alterarquantidade=cd[
                                'atualizar'])
        print(cd['atualizar'])
        return super().form_valid(form)


class CarrinhoRemove(View):
    def post(self, request, *args, **kwargs):
        self.produto = Produto.objects.get(id=kwargs['idprod'])
        carrinho = Carrinho(request)
        carrinho.remover_produto(self.produto)
        return redirect('carrinhodetalhe')


class CarrinhoDetalhe(TemplateView):
    template_name = 'carrinho/detalhe.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        carrinho = Carrinho(self.request)
        for item in carrinho:
            item['atualizarquantform'] = CarrinhoAddProdutoForm(initial={'quantidade': item['quantidade'],
                                                                         'alterarquantidade': True})
        contexto['carrinho'] = carrinho
        return contexto
