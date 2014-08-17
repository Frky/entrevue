from django.contrib import admin

from rdv.models import RDV, Answer


class RDVAdmin(admin.ModelAdmin):
    pass


class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(RDV, RDVAdmin)
admin.site.register(Answer, AnswerAdmin)

