# MistralSonification

MistralSound est le sujet de mon stage au laboratoire Piim du campus St-Jérôme de l'université Aix-Marseille dans le cadre de ma première année de Master Acoustique & Musicologie parcours Ingéniérie et Conception Sonore.
## Presentation

Ce projet présente une sonification pour chacun des trois instruments de mesures suivant : une sonde de pression, une sonde de Langmuir et un spectromètre.

### Sonde de pression

La sonification de la sonde de pression est une alarme qui se déclenche lorsque la pression mesurée n'est plus dans l'intervalle `valeur cible +/- marge`. La valeur affichée est en 10⁻³ mbar.
### Sonde de Langmuir

La sonification de la sonde de Langmuir a pour objectif de faire entendre trois paramètres du plasma : la présence d'un spoke en rotation, sa fréquence d'oscillation, et la parité de son mode.

La sonification est composée de deux oscillateurs accordé à une quinte l'un de l'autre. Le son produit est tonal s'il y a une rotation et bruité sinon. La fréquence fondamentale de l'ensemble est proportionnelle à la fréquence de rotation du spoke. Ces deux oscillateurs ont chacun une enveloppe temporelle propre afin de faire percevoir la parité du mode de la rotation : si les enveloppes sont en phase alors le mode est pair, si les envellopes sont en opposition de phase alors le mode est impair.

### Spectromètre

La sonification du spectromètre Jaz est divisée en deux sous-modules : Jaz-Relatif et Jaz-Global.
#### Jaz Relatif

Le sous-module Jaz-Relatif permet d'entendre la différence d'intensité lumineuse entre deux raies choisies du spectre. Le choix de ces raies se fait à l'aide du patch puredata et de la fenêtre de visualisation du spectre.

Lorsque la première raie est plus lumineuse que la seconde alors l'utilisateur va entendre d'abord un son aigu et résonnant avec une attaque franche ressemblant à une cloche frappée, puis un son plus grave avec une attaque plus douce. Si la première raie est moins lumineuse que la seconde alors la séquence entendue se déroulera dans le sens contraire.
#### Jaz Global

Le sous-module Jaz-Global permet d'entendre l'intensité globale du spectre. La valeur de l'intensité globale est mesurée en moyennant toutes les raies dont l'intensité est supérieure à un certain seuil (pour ne pas compter tous les pixels concernant les raies non éclairées par le plasma).

Le son produit est un _pad_ accordé sur l'éventuelle fréquence de rotation du spoke. L'intensité globale est retranscrite par une modulation sinusoïdale sur la fréquence de coupure du filtre. Plus l'intensité globale est élevée, plus l'amplitude et la fréquence de la modulation est grande.
## Configuration
### Préparation de l'environnement python

Pour faire fonctionner la sonification il faut lancer deux programmes :
 - python/main.py
 - puredata/Main.pd

Pour créer l'environnement python il faut éxecuter la commande suivante (pensez à l'éxecuter dans `Anaconda Prompt` si `conda` n'est pas reconnu):
```
conda create -n sonif311 python=3.11
```
Ensuite, naviguez dans le dossier `/python` et éxecutez la commande suivante pour activer l'environnement :
```
conda activate sonif311
```
Une fois l'environnement activé, il faut installer les paquets requis :
```
pip install --requirement requirements.txt
```
Cette commande installe toutes les dépendances listées comme nécessaires au programme.
>L'environnement python est déjà préparé sur la machine EFILE et sur MISTRAL5 sous un nom similaire à "sonif311".

### Configuration du programme python

Vérifiez que le fichier les paramètres écrits dans `python/configuration.toml` sont corrects. En particulier :
 - les ports des sondes branchées à la carte d'acquisition
 - les coefficients de calibration du niveau de bruit (voir la section calibration).

Une fois que tous les réglages sont corrects, éxecutez le programme `python\main.py`. Surveillez la console pour vérifier qu'il n'y a pas d'erreurs.

A présent, vous pouvez lancer puredata.
### Initialisation du patch puredata

Ouvrez la patch `puredata/Main.pd`. Dans l'onglet console de puredata, activez le DSP. Cliquez sur le bouton `Connect` pour connecter le patch puredata au programme python. A présent, la configuration est terminée : vous pouvez régler le volume général, activer les différents modules de sonification, régler leurs niveaux... voir la section Utilisation.

### Calibration du niveau de bruit

Si la sonification de la sonde de Langmuir est très bruitée alors que le signal de la sonde ne l'est pas, c'est qu'il faut recalibrer le traitement de la sonde.

Etapes de calibrations :
 - Faire un plasma sans rotation de spoke.
 - Noter le taux de bruit indiqué dans la fenêtre puredata : c'est le `noise_only_level`.
 - Faire un plasma avec un spoke tournant à une fréquence stable.
 - Noter le taux de bruit indiqué dans la fenêtre puredata : c'est le `signal_only_level`.
 - Executer le programme `calibration/calibration.py`.
 - Entrer les valeurs demandées.
 - Changer les valeurs `noise_a` et `noise_b` dans le fichier `configuration.toml`.
 - Relancer le programme python.
## Utilisation

Une fois tout le système calibré et connecté, il ne reste plus qu'à activer les différents modules de sonification.

La sonification proposée présente trois modules : sonde de pression, sonde de Langmuir, et spectromètre.

Les trois modules ont les même réglages : un bouton on/off qui permet d'activer désactiver le son de la sonification et un curseur de volume.

### Sonde de pression

La valeur visée de pression ainsi que la marge tolérée sont réglable à l'aide des deux _boîtes à nombre_ "valeur visée" et "marge".

### Sonde de Langmuir

Le taux de bruit nécessaire à la calibration est inscrit dans la _boîte à nombre_ "Taux de bruit".

### Spectromètre Jaz

Le temps d'intégration du spectromètre est réglable à l'aide du curseur "Integration Time".
#### Jaz-Relatif

Les deux raies sont choisies à l'aide des curseurs horizontaux "pixel 1" (représentée en bleu sur le graphique) et "pixel 2" (représentée en vert sur le graphique). Les boutons "<" et ">" permettent de circuler au prochain pic détecté. Le curseur "Peak Threshold" permet de régler le seuil de détection des pics. La valeur en nm ainsi que la valeur d'intensité de la raie choisie est visible à droite du curseur horizontal.
## Bugs répertoriés

- La solution utilisée pour afficher le spectre n'est pas optimal : l'utilisation de `time.sleep()` dans la boucle d'affichage cause un manque de fluidité dans l'interaction avec la fenêtre.

- Le système de navigation entre les pics pour Jaz-Relatif n'est pas pratique. Les boutons ">" et "<" ne choisissent pas le premier pic avant ou après la longueur d'onde actuelle.

- La sonification de la parité du mode n'a pas pu être testée mais il semble que la méthode utilisée pour déterminer si les deux sondes sont en phase ne fonctionne pas systématiquement.
## Tableau des messages OSC

Messages depuis les scripts python vers les patch puredata sur le port 57120 :
| Header | Contenu |
| ------ | ------------- |
| "/pression" | valeur de pression normalisée telle que la valeur de pression visée vaut 0.5  |
| "/lgmr_freq" | fréquence mesurée de rotation du spoke |
| "/lgmr_noise" | estimation du rapport signal sur bruit normalisée : 0 le signal est pur, 1 ce n'est que du bruit |
| "/lgmr_phase" | déphasage entre le signal des deux sondes |
| "/jazGlobal" | intensité lumineuse moyenne de tout le spectre mesuré par le spectromètre |
| "/jazRel" | rapport de l'intensité entre deux fréquences spécifiques |
| "/indexToWl" | valeur en nm des longueurs d'ondes correspondantes aux pixels il1 et il2 |
| "/iToSpc" | valeur de l'intensité des deux pixels il1 et il2 |
| "/poke" | 1 |

"/poke" permet d'obtenir une valeur pour il1 et il2 à chaque cycle d'actualisation de Jaz, sans attendre de changement de valeur. Le message déclenche un "bang" dans puredata qui programme l'envoi des messages "/pixel1" et "/pixel2".

"/nexti1" et "/nexti2" permettent de circuler parmi les valeurs du spectre lumineux supérieures à une valeur de seuil.

Messages depuis les patchs puredata vers les scripts python sur le port 57121 :

| Header | Contenu |
| ------ | ------- |
| "/pixel1" | index du pixel il1 |
| "/pixel2" | index du pixel il2 |
| "/nexti1" | 0 ou 1 |
| "/nexti2" | 0 ou 1 |
| "/intTime" | temps d'intégration du spectromètre en ?? voir doc |
| "/peakThrshld" | valeur du seuil d'intensité pour la détection des pics |
