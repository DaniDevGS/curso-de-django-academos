from rest_framework import serializers
from .models import Producto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class CategoriaPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('nombre','descripcion')     

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('nombre','descripcion','categoria','cantidad','precio')     