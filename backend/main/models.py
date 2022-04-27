from django.db import models


class Country(models.Model):
    """Модель Страны"""
    title = models.CharField(max_length=100, default="Россия")
    
    def __str__(self):
        return self.title
    

class City(models.Model):
    """Модель Города"""
    title = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name="citys", on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.title


class School(models.Model):
    """Модель школы"""
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City, related_name="schools", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.city} | {self.title}"

