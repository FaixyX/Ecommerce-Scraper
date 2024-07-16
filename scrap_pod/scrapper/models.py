from django.db import models


# Modal for store
class Store(models.Model):
    name = models.CharField( max_length=255 )
    # url = models.URLField( blank=True, null=True )

    def __str__(self):
        return self.name
    
# Modal for categories
class Categories(models.Model):
    name = models.CharField( max_length=255 )
    store = models.ForeignKey( Store, on_delete=models.CASCADE, null=True, blank=True )

    def __str__(self):
        return f"{self.name} in {self.store}"

# Modal for categories
class SubCategories(models.Model):
    name = models.CharField( max_length=255 )
    store = models.ForeignKey( Store, on_delete=models.CASCADE, null=True, blank=True )
    category = models.ForeignKey( Categories, on_delete=models.CASCADE, null=True, blank=True )
    url = models.URLField( blank=True, null=True )

    def __str__(self):
        return f"{self.name} of {self.category}"
    
# Modal for LiveGames
class Product(models.Model):
    name = models.CharField( max_length=255 )
    image = models.CharField( max_length=255, blank=True, null=True )
    price = models.CharField( max_length=255, blank=True, null=True )
    url = models.URLField( blank=True, null=True )
    store = models.ForeignKey( Store, on_delete=models.CASCADE, null=True, blank=True )
    category = models.ForeignKey( Categories, on_delete=models.CASCADE, null=True, blank=True )
    sub_category = models.ForeignKey( SubCategories, on_delete=models.CASCADE, null=True, blank=True )

    def __str__(self):
        return f"{self.name} of {self.sub_category} of {self.category} in {self.store}"
