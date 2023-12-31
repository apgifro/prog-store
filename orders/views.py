from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from cart.carrinho import Carrinho
from orders.forms import PedidoModelForm
from .models import ItemPedido, Pedido


class PedidoCreateView(CreateView):
    form_class = PedidoModelForm
    success_url = reverse_lazy('resumopedido')
    template_name = 'formpedido.html'

    def form_valid(self, form):
        car = Carrinho(request=self.request)
        pedido = form.save()
        for item in car:
            ItemPedido.objects.create(pedido=pedido,
                                      produto=item['produto'],
                                      preco=item['preco'],
                                      quantidade=item['quantidade'])
        car.limpar()
        self.request.session['idpedido'] = pedido.id
        #form.send_email(pedido)
        return redirect('resumopedido', idpedido=pedido.id)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ResumoPedidoTemplateView(TemplateView):
    template_name = 'resumopedido.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pedido'] = Pedido.objects.get(id=self.kwargs['idpedido'])
        return ctx
