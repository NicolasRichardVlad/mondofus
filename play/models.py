from django.db import models
 
class Equipement(models.Model):
    id_equip = models.CharField(max_length=100, primary_key=True)
    taille_max = models.IntegerField(default=1)
    disponibilite = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='characters/', blank=True, null=True)
    def __str__(self):
        return self.id_equip

class Character(models.Model):
    id_character = models.CharField(max_length=100, primary_key=True)
    puissance = models.IntegerField(default=20)
    key=models.BooleanField(default=False)
    etat = models.CharField(max_length=20)
    sexe = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='characters/', blank=True, null=True)    
    lieu = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    def __str__(self):
        return self.id_character