# Datasets libres recommandes

## 1. COCO Dataset

Lien : https://cocodataset.org/

Bon choix pour commencer rapidement. COCO contient deja les classes utiles au prototype :

- car
- bus
- truck
- motorcycle
- bicycle

Utilisation recommandee : prototype rapide avec un modele YOLO pre-entraine.

## 2. BDD100K

Lien : https://bdd-data.berkeley.edu/

Dataset tres adapte aux scenes routieres reelles : routes, villes, meteo variable, jour/nuit. Il est pertinent si l'objectif est d'ameliorer la detection des vehicules dans la rue.

Utilisation recommandee : fine-tuning du modele pour les routes, taxis, bus et trafic urbain.

## 3. KITTI Object Detection

Lien : https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d

Dataset classique pour la detection de voitures, pietons et cyclistes. Il est plus petit que BDD100K, mais tres connu dans les projets de vision par ordinateur.

Utilisation recommandee : evaluation et comparaison des performances.

## 4. Open Images

Lien : https://storage.googleapis.com/openimages/web/index.html

Tres grand dataset avec de nombreuses classes et des annotations par boites englobantes.

Utilisation recommandee : enrichissement du modele avec des objets varies.

## Choix conseille pour ce projet

Pour un rendu de projet :

1. Demarrer avec YOLO pre-entraine sur COCO.
2. Tester sur une video de rue ou de circulation.
3. Si le temps le permet, faire un fine-tuning sur BDD100K.
4. Exporter le modele final en ONNX pour mobile.

