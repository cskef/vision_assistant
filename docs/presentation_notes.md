# Notes de presentation

## Probleme

Les personnes malvoyantes peuvent rencontrer des difficultes pour comprendre rapidement leur environnement, surtout dans les rues, les marches, les transports ou les lieux publics.

## Solution proposee

L'application agit comme un agent intelligent :

1. Elle percoit l'environnement avec la camera.
2. Elle detecte les vehicules avec un modele YOLO.
3. Elle suit les vehicules dans le temps.
4. Elle raisonne sur le danger potentiel.
5. Elle agit en produisant une alerte vocale.

## Partie agent intelligent

- Capteur : camera du smartphone.
- Perception : detection d'objets.
- Memoire courte : tracking des vehicules detectes.
- Raisonnement : position, proximite, approche.
- Action : message vocal contextualise.

## Exemple de scenario

Une voiture apparait au centre de l'image. Si sa boite de detection grossit rapidement, l'agent considere que la voiture s'approche et annonce :

```text
Attention, voiture en approche devant vous.
```

## Evolution possible

- Ajouter la detection des personnes et obstacles.
- Ajouter estimation de distance avec calibration camera.
- Entrainer sur BDD100K pour mieux reconnaitre taxis, bus et motos en contexte urbain.
- Integrer le modele ONNX dans React Native.

