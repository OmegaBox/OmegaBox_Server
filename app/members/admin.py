from django.contrib import admin

from members.models import Member, Profile


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
