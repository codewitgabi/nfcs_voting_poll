from django.contrib import admin
from .models import Contestant, Voter, Category, Vote


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
	list_display = ("name",)
	search_fields = ("name",)
	
	
@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
	list_display = ("name", "phone", "has_voted")
	search_fields = ("name", "phone")
	
	
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name",)
	search_fields = ("name",)
	

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
	list_display = ("voter", "category", "contestant")
	
	