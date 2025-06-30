# MistralSonification

MistralSound est le sujet de mon stage au laboratoire Piim du campus St-Jérôme de l'université Aix-Marseille dans le cadre de ma première année de Master Acoustique & Musicologie parcours Ingéniérie et Conception Sonore.

## OSC Table

Messages depuis les scripts python vers les patch puredata sur le port 57120 :
| Header | Contenu |
| ------ | ------------- |
| "/pression" | valeur de pression normalisée tel que la valeur de pression visée vaut 0.5  |
| "/lgmr_freq" | frequence mesurée de rotation du spoke |
| "/lgmr_noise" | estimation du rapport signal sur bruit normalisée : 0 le signal est pur, 1 ce n'est que du bruit |
| "/lgmr_phase" | déphasage entre le signal des deux sondes |
| "/jazGlobal" | intensité lumineuse moyenne de tout le spectre mesuré par le spectromètre |
| "/jazRel" | rapport de l'intensité entre deux fréquences spécifiques |
| "/indexToWl" | valeur en nm des longueurs d'ondes correspondants aux pixels il1 et il2 |
| "/iToSpc" | valeur de l'intensité des deux pixels il1 et il2 |
| "/poke" | 1 |

"/poke" permet d'obtenir une valeur pour il1 et il2 à chaque cycle d'actualisation de Jaz, sans attendre de changement de valeur. Le message déclenche un "bang" dans puredata qui programme l'envoi des messages "/pixel1" et "/pixel2". 

Messages depuis les patchs puredata vers les scripts python sur le port 57121 :

| Header | Contenu |
| ------ | ------- |
| "/pixel1" | index du pixel il1 |
| "/pixel2" | index du pixel il2 |
