# MistralSonification

This repository tracks my progress for my internship on Plasma Sonification at St. Jérôme's lab in marseille.

# OSC Table


| Header | Signification |
| ------ | ------------- |
| "/pression" | valeur de pression normalisée tel que la valeur de pression visée vaut 0.5  |
| "/lgmr_freq" | frequence mesurée de rotation du spoke |
| "/lgmr_noise" | estimation du rapport signal sur bruit normalisée : 0 le signal est pur, 1 ce n'est que du bruit |
| "/lgmr_phase" | déphasage entre le signal des deux sondes |
| "/jazGlobal" | intensité lumineuse moyenne de tout le spectre mesuré par le spectromètre |
| "/jazRel" | rapport de l'intensité entre deux fréquences spécifiques |
