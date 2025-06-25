jaz_acquis_DG007.exe
DG - 22/03/2019

Maj de l’appli d’acquisition des JAZ :
*	L’ergonomie est légèrement modifiée.
*	On peut définir un temps d’acquisition pour chaque JAZ. Le temps d’acquisition total sera donné par le plus long des temps d’intégration.
*	On peut définir un temps de répétition (dt). L’acquisition des 3 JAZ est démarrée tous les dt. Une led verte s’allume lorsque le temps acquisition est supérieur à dt.
*	Il y a 2 boutons pour la sauvegarde des données : 
*	Save in loop : enregistre les données des 3 JAZ à chaque acquisition.
*	Save one time : enregistre seulement le spectre affiché.
Dans les 2 cas, le nom du fichier est automatiquement incrémenté en fonction des fichiers déjà présents dans le répertoire (pas d’écrasement de fichier possible).


---
jaz_acquis_DG007.exe
DG - 08/03/2019

L'application jaz_acquis_DG007.exe réalise l'acquisition simultanée des spectres des 3 modules jaz.
avec post traitement des spectres par référence d'un corps noir. La communication avec les spectros jaz se fait par ip (par défaut 147.94.187.212).

Pour la calibration avec le corps noir, il faut déposer dans le répertoire de l'exécutable 2 fichiers en respectant les noms:
*	black_body_calibration.dat : mesure du corps noir avec le logiciel Labsphere. Le fichier est formaté sous 2 colonnes, longueur d'onde de 300 à 1100nm et radiance.
*	jaz_callibration.dat : mesure avec le jaz du corps noir et l'application jaz_acquis_DG007.exe. Faire l'acquisition d'un spectre avec l'option "activate the black body correction" désactivée. Le fichier se compose de 3 paires de colonnes définissant les longueurs d'onde et l'intensité de chaque spectro jaz. Le profil des spectres peut être amélioré soit avec les options d'acquisition ("integration time", "number of scans to be averaged", "number of points to smooth") ou en réalisant un traitement numérique des données (filtrage). Le données de sortie doivent reproduire le format initial (3 paires longueur d'onde - intensités).

*	Options d'acquisition : 
**	"integration time" : temps d'intégration pour l'acquisition du spectre d'un jaz. L'application gère le multitâche et réalise l'acquisition des 3 spectros en même temps.
**	"number of scans to be averaged" : nombre d'acquisition au temps d'intégration donnée avant de retourner les spectres.
**	"number of points to smooth" : option de lissage des courbes. Le paramètre définie le nombre de points de part et d'autre du point considéré.
**	"number of points to remove" : nombre de points à supprimer en début de spectre. Cette option permet de retirer les "dark pixels" (le callage des spectres autour du zéro).
** "show correction coefficients" : permet de visualiser les coefficients permettant de corriger les spectres avec la calibration du corps noir. Il faut activer la case avant le démarrage de l'application.


Tips : 
* Tous les fichier .dat peuvent commencer par un en-tête de commentaire. Les lignes doivent impérativement débuter par le caractère "#". Il est conseiller de documenter les fichiers de donnée (date d'acquisition, qui fait la mesure, protocole...).

