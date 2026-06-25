import sys
import pathlib
project_root = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))
from src.data_normalizer import normalize_name, split_aliases
print(normalize_name("José Álvarez!"))
print(split_aliases("José Álvarez|J. Alvarez|Jose A."))
print(normalize_name("Müller & Söhne"))
print(split_aliases("Müller & Söhne|Mueller and Sons|Muller & Sons"))