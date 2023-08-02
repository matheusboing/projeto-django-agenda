# Toda view nova, realizar o import dela dessa forma descrita abaixo.
# Isso é uma forma de enganar o django, pois ele ainda assim lê o nome do package como 'views' e executa o __init__.py primeiro, sendo assim, a aplicação roda liso.

from .contact_views import *
from .contact_forms import *