from django import forms

from .models import Cliente

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'endereco', 'fone', 'email', 'foto']
        #fields = '__all__'

        error_messages = {
            'nome': {'required': 'O nome do fornecedor é um campo obrigatório'},
            'endereco': {'required': 'O endereco do fornecedor é um campo obrigatório'},
            'fone': {'required': 'O número do telefone é um campo obrigatório'},
            'email': {'required': 'O email do cliente é um campo obrigatório',
                      'invalid': 'Formato inválido para o e-mail. Exemplo de formato válido: fulano@dominio.com',
                      'unique': 'E-mail já cadastro'
            }
        }