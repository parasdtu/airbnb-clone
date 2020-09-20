from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Converstion Admin Definition """

    pass


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    pass
