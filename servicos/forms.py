from django import forms

from servicos.models import Servico


class ServicoModelForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco']

        error_messages = {
            'nome': {'required': 'O nome do serviço é um campo obrigatório',
                     'unique': 'Serviço já cadastrado'},
            'descricao': {'required': 'A descrição do serviço é um campo obrigatório'},
            'preco': {'required': 'O preço do serviço é um campo obrigatório'},
        }