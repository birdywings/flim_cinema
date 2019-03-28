import xadmin
from .models import *


class IndexLabelAdmin():
    list_display = ('name', )


xadmin.site.register(IndexLabel, IndexLabelAdmin)


class LabelAdmin():
    list_display = ('name', )


xadmin.site.register(Label, LabelAdmin)


class FilmAdmin():
    list_display = ('label', 'name', )


xadmin.site.register(Film, FilmAdmin)
