# Integration mobile avec ONNX

## Objectif

L'application mobile React Native peut executer le modele directement sur le telephone avec ONNX Runtime Mobile. Cela reduit la dependance a un serveur distant et ameliore la confidentialite.

## Pipeline mobile

```text
Camera smartphone
  -> image redimensionnee en 640x640
  -> modele YOLO ONNX
  -> post-traitement des boites
  -> tracking
  -> generation d'un message court
  -> synthese vocale
```

## Export du modele

```bash
yolo export model=yolov8n.pt format=onnx imgsz=640
```

Le fichier obtenu ressemble a :

```text
yolov8n.onnx
```

## Bibliotheques React Native possibles

- `onnxruntime-react-native` pour executer le modele.
- `react-native-vision-camera` pour recuperer les images de la camera.
- `react-native-tts` pour la synthese vocale.

## Classes utiles

Pour reduire le calcul et rendre l'assistance plus claire, garder seulement :

- car
- bus
- truck
- motorcycle
- bicycle

## Logique d'alerte recommandee

Le mobile ne doit pas lire toutes les detections. Il doit prioriser :

1. Vehicule en approche.
2. Vehicule proche au centre.
3. Bus ou moto proche.
4. Resume contextuel si plusieurs vehicules sont presents.

Exemples :

```text
Attention, voiture en approche devant vous.
Bus proche a gauche.
Deux vehicules devant vous.
```

