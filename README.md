# ZeBrands
sku, name, price and brand

(i) admins to create / update / delete products and to create / update / delete other admins; and 
(ii) anonymous users who can only retrieve products information but can't make changes.

As a special requirement, whenever an admin user makes a change in a product (for example, if a price is adjusted), we need to notify all other admins about the change, either via email or other mechanism.

We also need to keep track of the number of times every single product is queried by an anonymous user, so we can build some reports in the future.

# generar documentacion
pycco products/models.py -p
pycco products/schema.py -p

{
      "Authorization": "JWT <Token>"
}