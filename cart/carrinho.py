from decimal import Decimal
from django.conf import settings

from app.models import Produto


class Carrinho:
    def __init__(self, request):
        self.session = request.session
        carrinho = self.session.get(settings.CARRINHO_SESSION_ID)
        if not carrinho:
            carrinho = self.session[settings.CARRINHO_SESSION_ID] = {}
        self.carrinho = carrinho

    def add_produto(self, produto, quantidade=1, alterarquantidade=False):
        id_prod = str(produto.id)
        if id_prod not in self.carrinho:
            self.carrinho[id_prod] = {'quantidade': 0, 'preco': str(produto.preco)}
        if alterarquantidade:
            self.carrinho[id_prod]['quantidade'] = quantidade
        else:
            self.carrinho[id_prod]['quantidade'] += quantidade
        self._salvar()

    def _salvar(self):
        self.session.modified = True

    def remover_produto(self, produto):
        id_prod = str(produto.id)
        if id_prod in self.carrinho:
            del self.carrinho[id_prod]
            self._salvar()

    def __iter__(self):
        idsprodutos = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=idsprodutos)
        carrinho = self.carrinho.copy()
        for p in produtos:
            carrinho[str(p.id)]['produto'] = p
        for item in carrinho.values():
            item['preco'] = Decimal(item['preco'])
            item['preco_total'] = item['preco'] * item['quantidade']
            yield item

    def __len__(self):
        return sum(item['quantidade'] for item in self.carrinho.values())

    def get_preco_total(self):
        return sum(Decimal(item['preco']) * item['quantidade'] for item in self.carrinho.values())

    def limpar(self):
        del self.session[settings.CARRINHO_SESSION_ID]
        self._salvar()
