import graphene
import graphql_jwt
from graphene_django import DjangoObjectType

from pprint import pprint

from products.models import Product,View,Category
from users.models import CustomUser

#Django-GraphQL-Auth
from django.contrib.auth.middleware import get_user
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

from django.core import serializers

from django.contrib.auth import get_user_model


class CategoryType(DjangoObjectType):
    """
        objecto devuelto es Category junto con todos sus atributos
    """
    class Meta:
        model = Category
        fields = ("__all__")

class ProductType(DjangoObjectType):
    """
        objecto devuelto es Product junto con todos sus atributos
    """
    class Meta:
        model = Product
        fields = ("__all__")

class ViewType(DjangoObjectType):
    """
        objecto devuelto es Product junto con todos sus atributos
    """
    class Meta:
        model = View
        fields = ("__all__")

class UserType(DjangoObjectType):
    """
        objecto devuelto es User junto con todos sus atributos
    """
    class Meta:
        model = CustomUser
        fields = ("__all__")

class Query(UserQuery, MeQuery, graphene.ObjectType):
    # type definition
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    productsviews = graphene.List(ViewType, id=graphene.Int(required=False) )
    products = graphene.List(ProductType, id=graphene.Int(required=False) )
    categories = graphene.List(CategoryType, id=graphene.Int(required=False), name=graphene.String(required=False))

    @login_required # solo para usuario autenticados
    def resolve_users(self, info):
        return CustomUser.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure!')
        return user
        
    def resolve_products(root, info, **kwargs):
        """
            si se pasa el parametro id se hace un filter por id si no se devuelven todos los resultado
            guarda el historial de las consultas solo de usuarios anonimos
        """
        #pprint(dir(info.context.user))
        print("is_anonymous", info.context.user.is_anonymous)
        #print("is_authenticated", info.context.user.is_authenticated)
        id = kwargs.get("id")
        data = []
        if id is None:
            data = Product.objects.select_related("obj_categoria").all()
        else:
            data = Product.objects.select_related("obj_categoria").filter(id=id)
        #pprint(data)
        # tracked view
        if info.context.user.is_anonymous: 
            for item in data:
                obj_View = View.objects.get(id=item.id)
                #print(item.id)
                #print(obj_View)
                if obj_View:
                    #print("se encontro el valor")
                    obj_View.str_times =  int(obj_View.str_times) + 1
                    obj_View.save()
                else:
                    obj_Product = Product.objects.get(id=item.id)
                    view_ = View.objects.create(obj_products=obj_Product,str_times=1)
                #print(item.id)
        return data

    def resolve_productsviews(root, info, **kwargs):
        """
            si se pasa el parametro id se hace un filter por id si no se devuelven todos los resultado
        """
        id = kwargs.get("id")
        data = []
        if id is None:
            data = View.objects.select_related("obj_products").all()
        else:
            data = View.objects.select_related("obj_products").filter(id=id)
        return data

    def resolve_categories(root, info, **kwargs):
        str_id = kwargs.get('id','')
        str_nombre = kwargs.get('name','')
        data = []
        if str_id!="":
            data = Category.objects.filter(id=str_id)
        elif str_nombre!="":
            data = Category.objects.filter(str_nombre=str_nombre)
        else:
            data = Category.objects.all()
        return data

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    update_account = mutations.UpdateAccount.Field()
    delete_account = mutations.DeleteAccount.Field()

class Products_CreateMutation(graphene.Mutation):
    """
        crear productos 
        solo para usuario autenticados
    """
    class Arguments:
        str_sku = graphene.String(required=True)
        str_name = graphene.String(required=True)
        str_price = graphene.String(required=True)
        obj_categoria = graphene.Int(required=True)

    product = graphene.Field(ProductType)

    @login_required # solo para usuario autenticados
    def mutate(self, info, **kwargs):
        str_sku = kwargs.get('str_sku','')
        str_name = kwargs.get('str_name','')
        str_price = kwargs.get('str_price','')
        obj_categoria = kwargs.get('obj_categoria','')
        try:
            obj_Category = Category.objects.get(id=obj_categoria)
            product_ = Product.objects.create(str_sku=str_sku,str_name=str_name,str_price=str_price,obj_categoria=obj_Category)
        except:
            print("Error")
            product_ = False

        return Products_CreateMutation(product=product_)

class Products_UpdateMutation(graphene.Mutation):
    """
        actualizar productos
        solo para usuario autenticados
    """
    class Arguments:
        str_sku = graphene.String()
        str_name = graphene.String()
        str_price = graphene.String()
        obj_categoria = graphene.Int()
        id = graphene.ID(required=True)

    product = graphene.Field(ProductType)

    @login_required # solo para usuario autenticados
    def mutate(self, info, id, **kwargs):
        str_sku = kwargs.get('str_sku','')
        str_name = kwargs.get('str_name','')
        str_price = kwargs.get('str_price','')
        obj_categoria_id = kwargs.get('obj_categoria','')
        obj_Category = None
        if obj_categoria_id!="":
            try:
                obj_Category = Category.objects.get(id=obj_categoria_id)
            except:
                return Products_UpdateMutation(product=False)
        product = Product.objects.get(pk=id)
        if str_sku is not None:
            product.str_sku = str_sku
        if str_name is not None:
            product.str_name = str_name
        if str_price is not None:
            product.str_price = str_price
        if obj_Category is not None:
            product.obj_categoria = obj_Category
        product.save()

        return Products_UpdateMutation(product=product)

class Products_DeleteMutation(graphene.Mutation):
    """
        eliminar productos
        solo para usuario autenticados
    """
    class Arguments:
        id = graphene.ID(required=True)

    product = graphene.Field(ProductType)

    @login_required # solo para usuario autenticados
    def mutate(self, info, id):
        product = Product.objects.get(pk=id)
        product.delete()

        return Products_DeleteMutation(product=None)

# Mutation for sending the data to the server.
class Mutation(AuthMutation, graphene.ObjectType):
    """
        funciones para el CRUD
    """
    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
    # productos CRUD
    add_products = Products_CreateMutation.Field()
    update_products = Products_UpdateMutation.Field()
    delete_products = Products_DeleteMutation.Field()

# Create schema
schema = graphene.Schema(query=Query, mutation=Mutation)
