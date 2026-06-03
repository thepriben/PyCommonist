# Dépôt HAL — PyCommonist v1.1

Archive source : **`pycommonist-v1.1.zip`** (même convention que `pycommonist-v1.0` pour la v1.0).

## Fichiers obligatoires (racine de l’archive)

- [README.md](../../README.md)
- [AUTHORS](../../AUTHORS)
- [LICENSE](../../LICENSE)

## Produire l’archive

```bash
./scripts/build_release_zip.sh 1.1
```

Fichier généré : `releases/pycommonist-v1.1.zip` (non versionné dans git).

## HAL — option 1 (archive zip)

1. Déposer sur [HAL](https://hal.science/) → type **Logiciel**.
2. Joindre **`pycommonist-v1.1.zip`** (un seul fichier compressé, &lt; 200 Mo).
3. Renseigner la **version** : `1.1` (ou `1.1.0` si aligné PyPI).
4. Métadonnées : titre *PyCommonist*, auteurs (voir AUTHORS), licence MIT, langage Python, description (batch upload Wikimedia Commons).
5. Lier éventuellement la publication HAL de la v1.0 (`pycommonist-v1.0`) comme version antérieure.

## HAL — option 2 (SWHID / dépôt Git)

Si le code est sur GitHub et archivé par [Software Heritage](https://www.softwareheritage.org/) :

1. Obtenir le SWHID du snapshot ou du dépôt (tag `pycommonist-v1.1` ou `v1.1.0`).
2. Déposer les métadonnées dans HAL avec ce SWHID (historique de développement conservé).

## Documents d’archive conservés

- [History.md](History.md) — historique des contributions
- [RELEASE_v1.1.0.md](RELEASE_v1.1.0.md) — notes PyPI / semver
- [README.md](README.md) — index de ce dossier

## codemeta.json

Un fichier [codemeta.json](../../codemeta.json) à la racine du dépôt facilite l’import des métadonnées HAL (recommandé, non obligatoire).
