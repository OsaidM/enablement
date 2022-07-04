from multiprocessing import context
from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q, Count
from . import team_maker
import leagues

def index(request):
	
	# context = {
	# 	"leagues": League.objects.all(),
	# 	"teams": Team.objects.all(),
	# 	"players": Player.objects.all(),
	# }

	# context = {
	# 	"base_leagues": League.objects.filter(name__contains="Base"),
	# 	"womens_leagues": League.objects.filter(name__contains="Womens'"),
	# 	"hockey_league": League.objects.filter(sport__contains="hockey"),
	# 	"but_football": League.objects.exclude(sport__contains="football"),
	# 	"conferences": League.objects.filter(name__contains="conference"),
	# 	"atlantic": League.objects.filter(name__contains="atlantic"),
	# 	"dallas_team": Team.objects.filter(location="Dallas"),
	# 	"raptors_team": Team.objects.filter(team_name="Raptors"),
	# 	"location": Team.objects.filter(location__contains="City"),
	# 	"city_t": Team.objects.filter(team_name__startswith="T"),
	# 	"all_teams_ordered": Team.objects.order_by('team_name'),
	# 	"all_teams_reveresd": Team.objects.order_by('-team_name'),
	# 	"cooper_players": Player.objects.filter(last_name__startswith = 'Cooper'),
	# 	"joshua_players": Player.objects.filter(first_name__startswith = 'Joshua'),
	# 	"cooper_but_joshua_players": Player.objects.filter(last_name__startswith = 'Cooper').exclude(first_name='Joshua'),
	# 	"joshua_or_alexander_players": Player.objects.filter(Q(first_name__startswith = 'Alexander') | Q(first_name__startswith = 'Wyatt')),
	# }
	
	context={
		"atlantic_league": Team.objects.filter(league__name__contains="Atlantic Soccer Conference"),
		"boston_league": Player.objects.filter(Q(curr_team__location__contains="Boston") & Q(curr_team__team_name__contains="Penguins")),
		"baseball_players": Player.objects.filter(curr_team__league__name__contains="International Collegiate Baseball Conference"),
		"american_football_players": Player.objects.filter(Q(curr_team__league__name__contains="American Conference of Amateur Football") & Q(last_name__contains="Lopez")),
		"all_football_players": Player.objects.filter(curr_team__league__sport__contains="Football"),
		"all_teams_sophia": Team.objects.filter(curr_players__first_name__contains="Sophia"),
		"flores_sophia": Player.objects.filter(last_name__contains="Flores").exclude(curr_team__team_name__contains="Washington Roughriders"),
		"all_teams_evans": Team.objects.filter(Q(all_players__first_name__contains="Samuel")&Q(all_players__last_name__contains="Evans")),
		"all_players_manitoba": Player.objects.filter(Q(all_teams__team_name__contains="Tiger-Cats")& Q(all_teams__location__contains="Manitoba")),
		"all_players_but_wichita_vikings": Player.objects.filter(Q(all_teams__team_name__contains="Vikings")& Q(all_teams__location__contains="Wichita")).exclude(Q(curr_team__team_name__contains="Vikings")& Q(curr_team__location__contains="Wichita")),
		"player_jacob_teams_but_colts": Team.objects.filter(Q(all_players__first_name = 'Jacob') & Q(all_players__last_name = 'Gray')).exclude(Q(team_name='Colts')&Q(location='Oregon')),
		"everyone_named_joshua": Player.objects.filter(Q(first_name="Joshua")&Q(all_teams__league__name="Atlantic Federation of Amateur Baseball Players")),
		"teams_12": Team.objects.annotate(total_num = Count('all_players')).filter(total_num__gte=12),
		"all_players_count_of_teams": Player.objects.annotate(teams_played_for = Count('all_teams')).order_by('teams_played_for'),
	}
	
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")