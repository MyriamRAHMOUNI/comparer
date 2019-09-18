# Comparaison de la dynamique de variants associés à des pathologies à l'aide d'un alphabet structural

Le logiciel PBxplore a été mis à disposition pour traiter des Dynamiques Moléculaires à l’aide d’un alphabet structural, les Blocs
Protéiques (Barnoud et al, bioarxiv preprint ; https://github.com/pierrepo/PBxplore). Il permet de coder chaque snapshots à l’aide des Blocs Protéiques et propose une analyse statistique des variations conformationnelles.

Ce programme permet donc de comparer les résultats de dynamique moléculaire issue de l'analyse complète offerte par PBxplore d’une protéine et de variants ponctuels (donc même longueur de séquence) associés à une pathologie. 

### Pré-requis

- python3
- sys, pandas et matplotlib

## Démarrage

Pour lancer le comparateur il faut avoir les résultats de PBxplore sur deux proteines (WT et variants NB: les variations doivent être ponctuelles donc même longueur de séquences)

python3 comparer.py help 

python3 comparer.py proteine-1.PB.Neq proteine-1.PB.count proteine-2.PB.Neq proteine-2.PB.count output



