from django.shortcuts import render, redirect
from .models import Contestant, Voter, Category, Vote
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError


def index(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        try:
            voter = Voter.objects.get(phone=phone)
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
                voter=voter, category=category, contestant_id=choice
            )
            vote.save()

        voter.has_voted = True
        voter.save()
        return redirect("poll:index")

    context = {"categories": categories, "voter": voter}

    return render(request, "poll/vote.html", context)


def result(request):
    """Get results of the polling"""
    if not request.user.is_authenticated:
        return redirect("poll:index")
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, "poll/result.html", context)


def download_result(request):
    if not request.user.is_authenticated:
        return redirect("poll:index")

    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=result.txt"

    categories = Category.objects.all()
    data = []

    for category in categories:
        data.append(f"{category}\n\n")
        for contestant in category.contestants.all():
            v = Vote.objects.filter(category=category, contestant=contestant)
            data.append(f"{contestant} {v.count()}\n")
        data.append("\n\n")

    response.writelines(data)
    return response
