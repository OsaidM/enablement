from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q
from . import team_maker

def index(request):
	
	# context = {
	# 	"leagues": League.objects.all(),
	# 	"teams": Team.objects.all(),
	# 	"players": Player.objects.all(),
	# }

	context = {
		"base_leagues": League.objects.filter(name__contains="Base"),
		"womens_leagues": League.objects.filter(name__contains="Womens'"),
		"hockey_league": League.objects.filter(sport__contains="hockey"),
		"but_football": League.objects.exclude(sport__contains="football"),
		"conferences": League.objects.filter(name__contains="conference"),
		"atlantic": League.objects.filter(name__contains="atlantic"),
		"dallas_team": Team.objects.filter(location="Dallas"),
		"raptors_team": Team.objects.filter(team_name="Raptors"),
		"location": Team.objects.filter(location__contains="City"),
		"city_t": Team.objects.filter(team_name__startswith="T"),
		"all_teams_ordered": Team.objects.order_by('team_name'),
		"all_teams_reveresd": Team.objects.order_by('-team_name'),
		"cooper_players": Player.objects.filter(last_name__startswith = 'Cooper'),
		"joshua_players": Player.objects.filter(first_name__startswith = 'Joshua'),
		"cooper_but_joshua_players": Player.objects.filter(last_name__startswith = 'Cooper').exclude(first_name='Joshua'),
		"joshua_or_alexander_players": Player.objects.filter(Q(first_name__startswith = 'Alexander') | Q(first_name__startswith = 'Wyatt')),
	}

	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")