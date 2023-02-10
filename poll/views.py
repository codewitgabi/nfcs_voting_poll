from django.shortcuts import render, redirect
from .models import Contestant, Voter, Category, Vote
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import csv
from django.conf import settings
import os

def add_voters_from_csv():
	"""
	Add those who filled the biodata form to the list of voters.
	"""
	BASE_DIR = settings.BASE_DIR
	csv_file = os.path.join(BASE_DIR, "data.csv")
	print(csv_file)
	with open(csv_file, "r") as file:
		content = csv.reader(file)
		for data in content:
			name, email = data
			try:
				voter = Voter.objects.create(
					name=name.strip(), email=email.strip())
				voter.save()
			except:
				pass
			
add_voters_from_csv()

def index(request):
	if request.method == "POST":
		email = request.POST.get("email")
		try:
			voter = Voter.objects.get(email= email)
			print(voter.id)
			if voter:
				return redirect("poll:vote", id=voter.id)
			messages.info("Seems you have already registered")
			return redirect("poll:index")
			
		except Voter.DoesNotExist:
			messages.error(request, "It seems you didn't complete the bio data form")
			
	return render(request, "poll/index.html")
	
	
def vote(request, id):
	try:
		voter = Voter.objects.get(id=id)
	except ValidationError:
		messages.error(request, "User with the given uuid does not exist")
		return redirect("poll:index")
	except Voter.DoesNotExist:
		messages.error(request, "User matching query does not exist")
		return redirect("poll:index")
		
	categories = Category.objects.all()
	
	# check for already voted voters
	if voter.has_voted:
		messages.info(request, "It seems you have already voted.")
		return redirect("poll:index")
	
	if request.method == "POST":
		data = request.POST
		
		for cat, choice in data.items():
			if cat == "csrfmiddlewaretoken":
				continue
			
			# create vote
			category = Category.objects.get(name=cat)
			vote = Vote.objects.create(
				voter=voter,
				category=category,
				contestant_id=choice
			)
			vote.save()

		voter.has_voted = True
		voter.save()
		return redirect("poll:index")
		
	context = {
		"categories": categories,
		"voter": voter
	}
		
	return render(request, "poll/vote.html", context)


def result(request):
	if not request.user.is_authenticated:
		return redirect("poll:index")
	categories = Category.objects.all()
	context = {
		"categories": categories,
	}
	return render(request, "poll/result.html", context)
	
	