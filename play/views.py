from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement
import random

# Create your views here.


def character_list(request):
    characters = Character.objects.all()
    return render(request, 'play/character_list.html', {'characters': characters})
 

def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    deplacement = False
    # print("ancien lieu : ", ancien_lieu)
    characters_dans_lieu = Character.objects.filter(lieu=ancien_lieu)
    message = ""
    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)
        if form.is_valid():
            form.save(commit="False")
            nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            if nouveau_lieu == ancien_lieu:
                message = f"{character.id_character} est déjà dans ce lieu"
                return render(request, 'play/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'message': message, 'characters_dans_lieu': characters_dans_lieu})
            print("nouveau_lieu : ", nouveau_lieu)
            print(f"Etat du perso: {character.id_character}+ {character.etat}")
            print(f"lieu demandé: {nouveau_lieu.id_equip}")
            if nouveau_lieu.disponibilite == "libre":
                deplacement = False
               
                nombre_lieu = Character.objects.filter(lieu=nouveau_lieu).count()
                
                # Si pas en état d'aller dans donjon puis si pas pour le harddonjon
                if nouveau_lieu.id_equip == "dunjeon" and character.etat != "repu":
                    print("n'est pas en état d'aller dans le donjon")
                    message = f"{character.id_character} n'est pas en état pour aller dans le donjon"
                    return render(request, 'play/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'message': message, 'characters_dans_lieu': characters_dans_lieu})
          #      if nouveau_lieu.id_equip == "harddunjeon" and character.etat != "repu" or character.key ==False:
          #          print("n'est pas en état d'aller dans le donjon")
          #          message = f"{character.id_character} n'est pas en état pour aller dans le donjon ou n'a pas la clef"
            #        return render(request, 'play/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'message': message, 'characters_dans_lieu': characters_dans_lieu})
                
  
                # si repu et vers donjon simple
                print("nouveau_lieu : " + nouveau_lieu.id_equip)
                if nouveau_lieu.id_equip == "dunjeon" and character.etat == "repu" and character.puissance<100:
                    if random.random()<=character.puissance/100: # Engros la puissance par defaut de chaque perso est de 20 donc la proba de gagner est de 0.20
                        print("gg")
                        character.etat = "affamé"
                        if character.puissance<100:
                            character.puissance += 10 # La puissance du perso monte de 10 donc le prochain donjon sera plus simple, etc.
                    else:
                        character.etat = "blessé"
                    character.save()
                    deplacement = True

                # harddunjeon plus de recompense en puissance mais il faut la clef et plus difficile
                if nouveau_lieu.id_equip == "harddunjeon" and character.etat == "repu" and character.key==True:
                    character.key=False # Le perso perd la clef
                    if random.random()<=character.puissance/200: # Engros la puissance par defaut de chaque perso est de 20 donc la proba de gagner est de 0.10
                        print("gg")
                        character.etat = "affamé"
                        if character.puissance<100:
                            character.puissance += 50 # La puissance du perso monte de 50 donc le prochain donjon sera plus simple, etc.
                    else:
                        character.etat = "blessé"
                        if character.puissance>10:
                            character.puissance-=10 
                    character.save()
                    deplacement = True

                # si affamé et vers bar
                elif nouveau_lieu.id_equip == "bar" and character.etat == "affamé":
                    character.etat = "repu"
                    character.save()
                    deplacement = True

                # si blessé et vers fontaine
                elif nouveau_lieu.id_equip == "fontaine" and character.etat == "blessé":
                    character.etat = "affamé"
                    character.save()
                    deplacement = True

                # si va vers la lotterie et a assez de puissance pour payer l'entrée    
                elif nouveau_lieu.id_equip == "lotterie" and character.puissance > 15:
                    character.puissance -= 5
                    if random.random()<0.33: # 33% chance d'avoir la clef du harddunjeon
                        character.key = True
                        message = f"{character.id_character} a obtenu la clef !"
                    else:
                        message = f"{character.id_character} n'a pas obtenu la clef !"
                    character.save()
                    deplacement = True
                    
                if ancien_lieu.disponibilite=="occupé": # SI ancien etait occ
                    print("on est dans le if2")
                    ancien_lieu.disponibilite = "libre"
                    print(ancien_lieu,character.lieu)
                    ancien_lieu.save()
                print("EEEEEEEEEEEEE")
                print(deplacement)
                if nombre_lieu > nouveau_lieu.taille_max - 1 and deplacement: #lieu rempli ou pas sachant que le perso s'est deplacé
                    print("on est dans le if1")
                    nouveau_lieu.disponibilite = "occupé"
                    nouveau_lieu.save()
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    
                if deplacement == False: #pas de deplacement
                    character.lieu=ancien_lieu
                    character.save()    

            else:
                print(f"on est ici+{ancien_lieu}")
                character.lieu = ancien_lieu
                character.save()
                occupants = Character.objects.filter(lieu=nouveau_lieu)
                occupants_names = ", ".join([o.id_character for o in occupants])
                print(occupants_names)
                message = f"Le lieu est déjà occupé par {occupants_names}"
                return render(request, 'play/character_detail.html', {'character': character, 'lieu': character.lieu, 'form': form, 'message': message, 'characters_dans_lieu': characters_dans_lieu})
                

                
            return redirect('character_detail', id_character=id_character)
    
    else:
        form = MoveForm()
        return render(request,
                    'play/character_detail.html',
                    {'character': character, 'lieu': character.lieu, 'form': form,'message': message, 'characters_dans_lieu': characters_dans_lieu})