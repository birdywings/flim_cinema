# coding:utf-8
import xadmin
from xadmin.views import CommAdminView


class GlobalSetting(CommAdminView):
    site_title = 'cyh_film admin'
    site_footer = 'power by cyh'


xadmin.site.register(CommAdminView, GlobalSetting)

