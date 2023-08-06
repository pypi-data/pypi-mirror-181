import os
from conf import settings


fonts = {
    'helvetica': {
        'regular': {
            'ttf': os.path.join(settings.BASE_DIR, 'fonts', 'helvetica-regular.ttf'),
            'name': 'helvetica'
        },
        'medium': {
            'ttf': os.path.join(settings.BASE_DIR, 'fonts', 'helvetica-medium.ttf'),
            'name': 'helveticaM'
        },
        'bold': {
            'ttf': os.path.join(settings.BASE_DIR, 'fonts', 'helvetica-bold.ttf'),
            'name': 'helveticaB'
        }
    }
}
