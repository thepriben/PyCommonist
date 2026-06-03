# PyCommonist

Application de bureau (Python / PyQt6) pour importer des images et médias sur [Wikimedia Commons](https://commons.wikimedia.org/), inspirée de [Commonist](https://commons.wikimedia.org/wiki/Commons:Commonist/fr).

Version **1.1** : fenêtre principale, sessions MDI, modèles `{{Information}}` et `{{Artwork}}`.

## Installation

```bash
git clone https://github.com/thepriben/PyCommonist.git
cd PyCommonist
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Lancement :

```bash
python main.py
# ou : ./run.sh
```

PyPI : pas encore publié ; l’installation via `pip install pycommonist` sera documentée ici le moment venu.

## Utilisation

1. Identifiants Commons en haut de la fenêtre.
2. Session **Information** par défaut : choisir un dossier à gauche.
3. Renseigner les champs globaux et par fichier, cocher **Import**, lancer l’import.
4. **Fichier → Nouvelle session** pour ouvrir une session **Artwork** ou une autre **Information**.

Configuration par défaut : [`src/pycommonist/resources/config/general.yaml`](src/pycommonist/resources/config/general.yaml).

## Releases

| Version | Archive | Tag |
|---------|---------|-----|
| 1.0 | `pycommonist-v1.0.zip` | `pycommonist-v1.0` |
| 1.1 | `pycommonist-v1.1.zip` | `pycommonist-v1.1` |

Archives HAL : [`docs/archives/HAL_v1.1.md`](docs/archives/HAL_v1.1.md). Historique des contributions : [`docs/archives/History.md`](docs/archives/History.md).

## Licence

MIT — voir [LICENSE](LICENSE).
