from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

# === Todos los modelos de la aplicacion ===

class Category(models.Model):
    """
        representacion de products_category en la bd
    """
    str_nombre = models.CharField(max_length=150)
    #extrasf
    created_at = models.DateTimeField(verbose_name="Fecha de creacion", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="Fecha de actualizacion", auto_now=True, null=True)

    def __str__(self):
        return '%s' % (self.str_nombre)

class Product(models.Model):
    """
        representacion de products_product en la bd
    """
    str_sku = models.CharField(verbose_name="Sku", max_length=150, unique=True)
    str_name = models.CharField(verbose_name="Name", max_length=150, unique=True)
    str_price = models.CharField(verbose_name="Price", max_length=150)
    obj_categoria = models.ForeignKey(Category, verbose_name="Categoria", on_delete=models.CASCADE)
    # extras
    #obj_user_login = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #obj_user_login = models.ForeignKey(get_user_model(),null=True, on_delete=models.CASCADE, verbose_name="Quien creo el rol")
    created_at = models.DateTimeField(verbose_name="Fecha de creacion", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="Fecha de actualizacion", auto_now=True, null=True)

    #def save(self, *args, **kwargs):
    #    if not self.id: # cuando es un insert
    #        try:
    #            last_id = Roles.objects.latest('id').id
    #        except:
    #            last_id = 1
    #        self.str_request_number = "RN-"+str(int(last_id)).zfill(10)
    #    super(Roles, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.str_name)

class View(models.Model):
    """
        * representacion de products_view en la bd
        * funciona para guardar las veces que un producto es requerido por un usuario anonimo
    """
    obj_products = models.ForeignKey(Product, verbose_name="Products", on_delete=models.CASCADE)
    str_times = models.CharField(verbose_name="times", max_length=150)
    # extras
    #obj_user_login = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #obj_user_login = models.ForeignKey(get_user_model(),null=True, on_delete=models.CASCADE, verbose_name="User")
    created_at = models.DateTimeField(verbose_name="Fecha de creacion", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="Fecha de actualizacion", auto_now=True, null=True)

    #def save(self, *args, **kwargs):
    #    if not self.id: # cuando es un insert
    #        try:
    #            last_id = Roles.objects.latest('id').id
    #        except:
    #            last_id = 1
    #        self.str_request_number = "RN-"+str(int(last_id)).zfill(10)
    #    super(Roles, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.str_times)

