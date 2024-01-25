from django.db import models

class Clients(models.Model):
    document = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Bills(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    nit = models.CharField(max_length=20)
    code = models.CharField(max_length=50)

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
class Bills_Products(models.Model):
    client_id_FK = models.ForeignKey(Bills, on_delete=models.CASCADE)
    product_id_FK = models.ForeignKey(Products, on_delete=models.CASCADE)
