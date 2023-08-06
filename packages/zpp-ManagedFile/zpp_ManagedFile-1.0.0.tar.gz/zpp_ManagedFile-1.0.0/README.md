# zpp_ManagedFile
## Informations
Système de fichier managé pour le contrôle des actions sur un fichier tels que la fermeture du fichier.
Permet de créer plusieurs types de fichier:
- file: Ouverture d'un fichier présent sur le système
- string: Simulation d'un fichier
- bytesio: Fichier bytes en mémoire
- stringio: Fichier en mémoire
- tempfile: Fichier temporaire

<br>

## Installation
```console
pip install zpp_ManagedFile
```
<br>

## Utilisation
```python
file = zpp_ManagedFile.ManagedFile()
```
filename=None, mode='r', typefile="stringio", encoding=None, closable=True
>En paramètre supplémentaire, nous pouvons mettre:<br/>
>- filename = Chemin du fichier si typefile=file
>- mode = Option sur le fichier (w/r/a)
>- typefile = type de fichier  (file,string,bytesio,stringio,tempfile)
>- encoding = type d'encodage du fichier
>- closable = activer le blocage de la fermeture (True pour activer)

Le fichier a les mêmes actions q'un fichier classique.

### Bloquer la fermeture du fichier

Il est possible de bloquer la fermeture du fichier en utlisant la méthode isClosable
```python
file.isClosable(True)
```
<br>

## Opération courantes sur les fichiers

### Fermeture du fichier
```python
file.close()
```

### Ecriture dans un fichier
```python
file.write(data)
```

### Ecriture d'une liste dans un fichier
```python
file.writelines(list)
```

### Flush des données du buffer
```python
file.flush()
```

### Tronquer le fichier
```python
file.truncate(size)
```
size détermine la taille du fichier tronqué

### Lecture d'un fichier
```python
file.read(size)
```
Si size est déterminé, lis seulement x bytes du fichier

### Lecture d'une ligne d'un fichier
```python
file.readline(size)
```
Si size est déterminé, lis seulement x bytes du fichier

### Récupération du contenu du fichier sous forme de liste
```python
file.readlines()
```

### Déplacer le curseur
```python
file.seek(offset, [mode])
```
offset correspond au déplacement
mode (optionnel) correspond à l'option de déplacement (0: déplacement depuis le début du fichier, 1: déplacement depuis la position actuelle, 2: déplacement depuis la fin du fichier)

### Connaitre la position du curseur
```python
file.tell()
```