﻿# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
#  FLEQ (Free LibreSoft Educational Quizbowl)                               #
#  A synchronous on-line competition software to improve and                #
#  motivate learning.                                                       #
#                                                                           #
#  Copyright (C) 2012  Arturo Moral, Gregorio Robles & Félix Redondo        #
#                                                                           #
#  This program is free software: you can redistribute it and/or modify     #
#  it under the terms of the GNU Affero General Public License as           #
#  published by the Free Software Foundation, either version 3 of the       #
#  License, or (at your option) any later version.                          #
#                                                                           #
#  This program is distributed in the hope that it will be useful,          #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #       
#  GNU Affero General Public License for more details.                      #
#                                                                           #
#  You should have received a copy of the GNU Affero General Public License #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                           #
#  Contact authors : Arturo Moral <amoral@gmail.com>                        #
#                    Gregorio Robles <grex@gsyc.urjc.es>                    #
#                    Félix Redondo <felix.redondo.sierra@gmail.com>			 #
#                                                                           #
#############################################################################

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from datetime import *
import datetime

from fleq.quizbowl.models import Date_time, Game, Preferred_start_time, Question_review, Round, Score, Tournament, Question, UserProfile
from fleq.quizbowl.views_notify import notify_user
from fleq.quizbowl.views_language import strLang, setBox
from fleq.quizbowl.views_tournaments_api import *



##################################
# QUESTION REVIEWS
##################################

class QuestionReviewForm(forms.Form):
	question = forms.IntegerField(label=(strLang()['label_question_id']), help_text=(strLang()['help_text_question_id']), required = True)
	arguments = forms.CharField(widget=forms.Textarea(),label=(strLang()['label_arguments']), required = True)

def newQuestionReview(request, gid):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# SIDEBAR INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	pendingQR = myAdminPendingQuestionReviews(request.user)

	# Info about user
	user_me = UserProfile.objects.get(user=request.user)

	# Load strings language to template newquestionreview.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.method == 'POST': # If the form has been submitted...
		form = QuestionReviewForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			try:
				question = Question.objects.get(pk = request.POST['question'])
				game = Game.objects.get(pk = gid)
			except:
				return HttpResponseRedirect('/games/' + str(gid) + '?status=error_question_no_exists')
			qr = Question_review(arguments = request.POST['arguments'],question = question, game = game, player = request.user)
			qr.save()
			notify_user(game.round.tournament.admin, 'new_review', qr)
			return HttpResponseRedirect('/games/' + str(gid) + '?status=success_added_question_review')
		else:
			return render_to_response('newquestionreview.html', {
				'user_me': user_me,
				'form': form,
				'lang': lang,
				'myTournaments': myTournaments,
				'myAdminTournaments': myAdmnTournaments,
				'todayGames': todayGames,
				'nextGames': nextGames,
				'admin_user': admin_user,
				'pendingQR': pendingQR,
			})
	else: # If get request, generate a new form
		# Only can do question reviews player1 and player2
		try:
			game = Game.objects.get(pk = gid)
		except:
			return HttpResponseRedirect('/games/' + str(gid) + '?status=error_question_no_exists')

		if user_me.user == game.player1 or user_me.user == game.player2:
	 		form = QuestionReviewForm()

			# Must we show a notification user?
			try:
		 		if request.GET['status']:
		 			box = setBox(request.GET['status'])
			except:
				box = ''
	 
			return render_to_response('newquestionreview.html', {
				'user_me': user_me,
				'form': form,
				'lang': lang,
				'box': box,
				'myTournaments': myTournaments,
				'myAdminTournaments': myAdmnTournaments,
				'todayGames': todayGames,
				'nextGames': nextGames,
				'game': game,
				'admin_user': admin_user,
				'pendingQR': pendingQR,
			})
		else:
			return HttpResponseRedirect('/my-tournaments')

def questionReview(request,qrid):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# Check if exists
	try:
		questionReview = Question_review.objects.get(pk = qrid)
	except:
		questionReview = ''

	# SIDEBAR INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	user_me = UserProfile.objects.get(user=request.user)
	pendingQR = myAdminPendingQuestionReviews(request.user)

	# Load strings language to template questionreviews.html
	try:
		lang = strLang()
	except:
		lang = ''
	
	# Only for admin reply
	if request.method == "POST" and request.POST['resolution']:
		questionReview.resolution = request.POST['resolution']
		questionReview.save()
		notify_user(questionReview.player, 'review_closed', questionReview)
		return HttpResponseRedirect('/question-review/' + qrid + '?status=success_resolution')	
	else:
		# Must we show a notification user?
		try:
	 		if request.GET['status']:
	 			box = setBox(request.GET['status'])
		except:
			box = ''
	
		return render_to_response('questionreview.html', {
			'user_me': user_me,
			'questionReview': questionReview,
			'lang': lang,
			'box': box,
			'myTournaments': myTournaments,
			'myAdminTournaments': myAdmnTournaments,
			'todayGames': todayGames,
			'nextGames': nextGames,
			'admin_user': admin_user,	
			'pendingQR': pendingQR,	
		})

##################################
# MY QUESTION REVIEWS
##################################

def myQuestionReviews(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')

	# Load strings language to template questionreviews.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# SIDEBAR AND MENU INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	user_me = UserProfile.objects.get(user=request.user)	
	pendingQR = myAdminPendingQuestionReviews(request.user)

	# My personal question reviews
	myQuestionReviews = Question_review.objects.filter(player = request.user).order_by('-pk')
	
	# Admin question reviews
	myAdminQuestionReviews = []
	allMyAdminTournaments = Tournament.objects.filter(admin=user_me.user)
	if allMyAdminTournaments:
		# All reviews in my Tournaments
		for tournament in allMyAdminTournaments:
			questionReviews = Question_review.objects.filter(game__round__tournament = tournament).order_by('-pk')
			for qr in questionReviews:
				myAdminQuestionReviews.append(qr)		

	# Must we show a notification user?
	try:
		if request.GET['status']:
			box = setBox(request.GET['status'])
	except:
		box = ''

	return render_to_response('myquestionreviews.html', {
		'user_me': user_me,
		'myQuestionReviews': myQuestionReviews,
		'myAdminQuestionReviews': myAdminQuestionReviews,		
		'lang': lang,
		'box': box,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'pendingQR': pendingQR,
		'admin_user': admin_user,	
	})
		

##################################
# GAME INFO
##################################

# Show information about a Tournament
def gameInfo(request, gid):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	try:
		print '0'
		game = Game.objects.get(id = gid)
		print '1'
		tournament = game.round.tournament
		print '2'
		r = game.round.round_number
		print '3'
		startDate = game.start_time
		print '4'
		player1 = game.player1
		print '5a'
		player2 = game.player2
		print '6'	
		if game.is_over():
			winner = game.winner
		else:
			winner = ""
		print '7'
		if request.user.is_superuser or request.user == tournament.admin:
			questionReviews = Question_review.objects.filter(game = game)
		else:
			questionReviews = Question_review.objects.filter(game = game, player = request.user)
		print '8'
	except:
		game = ''
		tournament = ''
		r = ''
		startDate = ''
		player1 = ''
		player2 = ''
		winner = ''
		questionReviews = ''

	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	# SIDEBAR INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	pendingQR = myAdminPendingQuestionReviews(request.user)

	# Info about user
	user_me = UserProfile.objects.get(user=request.user)

	# Must we show a notification user?
	try:
 		if request.GET['status']:
 			box = setBox(request.GET['status'])
	except:
		box = ''

	print "GAME: " + game.player1.username + " " + user_me.user.username

	return render_to_response('gameinfo.html', {
		'user_me': user_me,
		'game': game,
		'tournament': tournament,
		'round': r,
		'startDate': startDate,
		'player1': player1,
		'player2': player2,
		'winner': winner,
		'questionReviews': questionReviews,
		'lang': lang,
		'box': box,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,		
	})

##################################
# MY NEXT GAMES
##################################

def myNextGamesView(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')
           
	dateNow = datetime.datetime.now()

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# SIDEBAR INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	pendingQR = myAdminPendingQuestionReviews(request.user)

	# Info about user
	user_me = UserProfile.objects.get(user=request.user)

	# Games haven't been played and user has joined
	myFutureGames = Game.objects.filter(Q(log__isnull = False), Q(start_time__gte = dateNow), Q(player1 = request.user) | Q(player2 = request.user)).order_by('-start_time')

	# Save all dates of my uncommitted games to select date and time to play
	myUncommittedGamesDate = [] # Contains all options to select in my next games
	for g in myFutureGames:
		if not g.start_time_committed and dateNow <= g.start_time:
			startDate = g.round.start_date
			finishDate = g.round.finish_date
			while startDate <= finishDate:
				# Check to show only valid dates
				if startDate >= dateNow.date():
					d = {}
					d['gid'] = g.pk
					d['date'] = startDate
					myUncommittedGamesDate.append(d)
				startDate = startDate + timedelta(days = 1)

	# Extract all dates and times selected by user to show them
	mySelectedGamesDate = [] # Contains all options selected by user to each game
	opponentSelectedGamesDate = [] # Contains all options selected by opponent to each game
	for g in myFutureGames:
		if not g.start_time_committed and dateNow <= g.start_time:
			# Select game preferences by user
			mySelection = Preferred_start_time.objects.filter(Q(player = request.user), Q(game = g))
			for selection in mySelection:
				# Extract all datetimes selected by user to show them
				myDateTimesSelected = Date_time.objects.filter(Q(preferred_start_time = selection)).order_by('date_time')			
				for dateSelected in myDateTimesSelected:
					s = {}
					s['gid'] = g.pk
					s['date'] = dateSelected
					mySelectedGamesDate.append(s)
					
			# Select game preferences by opponent
			if g.player1 == request.user:
				opponent = g.player2
			else:
				opponent = g.player1
			opponentSelection = Preferred_start_time.objects.filter(Q(player = opponent), Q(game = g))
			for selection in opponentSelection:
				# Extract all datetimes selected by opponent to show them
				myDateTimesSelected = Date_time.objects.filter(Q(preferred_start_time = selection)).order_by('date_time')			
				for dateSelected in myDateTimesSelected:
					s = {}
					s['gid'] = g.pk
					s['date'] = dateSelected.date_time
					opponentSelectedGamesDate.append(s)

	# Load strings language to template mynextgames.html
	try:
		lang = strLang()
	except:
		lang = ''

	# Must we show a notification user?
	try:
		if request.GET['status']:
			box = setBox(request.GET['status'])
	except:
		box = ''

	return render_to_response('mynextgames.html', {
		'user_me': user_me,
		'myUncommittedGamesDate': myUncommittedGamesDate,
		'mySelectedGamesDate': mySelectedGamesDate,
		'opponentSelectedGamesDate': opponentSelectedGamesDate,
		'myNextGames': myFutureGames,
		'dateNow': dateNow,
		'box': box,
		'lang': lang,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})

##################################
# SELECT DATE AND TIME
##################################

@csrf_exempt
def selectStartTime(request, gid):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')

	game = Game.objects.get(id = gid)
	print "VIEWGAMES"
	pst = Preferred_start_time.objects.get(game = game, player = request.user)
  	print pst
	dateNow = datetime.datetime.now()

	if request.method == 'POST' and pst: # If the form has been submitted... save hour
		gameDate = pst.game.start_time.date()
		for time in request.POST.getlist('time'):
			hourSelected =  int(time)
			dateSelected = request.POST['date'].split('/')
			date = datetime.datetime(int(dateSelected[0]), int(dateSelected[1]), int(dateSelected[2]), hourSelected, 0, 0)

			# Check if dateTime exists in our database
			checkDate = Date_time.objects.filter(date_time = date, preferred_start_time = pst)
			if not checkDate and date > dateNow:
				print date.hour
				print dateNow.hour
				if date.date() == dateNow.date() and date.hour - dateNow.hour <= 1:
					return HttpResponseRedirect('/my-next-games/?status=error_datetime_selected_too_soon') # Redirect after POST
				else:
					dateTime = Date_time(date_time = date, preferred_start_time = pst)
					dateTime.save()
					pst.committed = True
					pst.save()
			else:
				if date <= dateNow or checkDate:
					return HttpResponseRedirect('/my-next-games/?status=error_datetime_selected_before') # Redirect after POST
      
      # Check if players saved the same hour to play
		pst = Preferred_start_time.objects.filter(game = pst.game)
		if pst[0].committed and pst[1].committed:
			d_t1 = Date_time.objects.filter(preferred_start_time = pst[0])
			d_t2 = Date_time.objects.filter(preferred_start_time = pst[1])
			for d_t_player1 in d_t1:
				for d_t_player2 in d_t2:
					if d_t_player1.date_time == d_t_player2.date_time and not game.start_time_committed:
						game.start_time = d_t_player1.date_time
						game.start_time_committed = True
						game.save()
						notify_user(game.player1, 'time_commited', game)
						notify_user(game.player2, 'time_commited', game)
						return HttpResponseRedirect('/my-next-games/?status=success_datetime_committed') # Redirect after POST
           
		return HttpResponseRedirect('/my-next-games/?status=success_datetime_selected') # Redirect after POST
	else:
		HttpResponseRedirect('/my-tournaments/')

##################################
# DELETE DATE AND TIME
##################################

@csrf_exempt
def deleteStartTime(request, gid):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')

	game = Game.objects.get(id = gid)  
	dateNow = datetime.datetime.now()

	if request.method == 'POST': # If the form has been submitted... delete dates
		for time in request.POST.getlist('time'):
			dateSelected =  Date_time.objects.get(pk = time)
			if dateSelected.preferred_start_time.player == request.user:
				dateSelected.delete()
			else:
				return HttpResponseRedirect('/my-next-games/?status=error_datetime_delete_other') # Redirect after POST

	return HttpResponseRedirect('/my-next-games')
		

##################################
# WON & LOST GAMES
##################################

def wonGames(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')
	
	# Select all won games
	wonGames = Game.objects.filter(winner = request.user).order_by('-start_time')

	# SIDEBAR INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	pendingQR = myAdminPendingQuestionReviews(request.user)

	# Info about user
	user_me = UserProfile.objects.get(user=request.user)

	# Load strings language to template mynextgames.html
	try:
		lang = strLang()
	except:
		lang = ''

	# Must we show a notification user?
	try:
		if request.GET['status']:
			box = setBox(request.GET['status'])
	except:
		box = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	return render_to_response('wongames.html', {
		'user_me': user_me,
		'box': box,
		'lang': lang,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'wonGames': wonGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})

def lostGames(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')
	
	# Select all won games
	lostGames = Game.objects.filter(Q(player1 = request.user) | Q(player2 = request.user), ~Q(winner = request.user)).order_by('-start_time')

	# SIDEBAR INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	pendingQR = myAdminPendingQuestionReviews(request.user)

	# Info about user
	user_me = UserProfile.objects.get(user=request.user)

	# Load strings language to template mynextgames.html
	try:
		lang = strLang()
	except:
		lang = ''

	# Must we show a notification user?
	try:
		if request.GET['status']:
			box = setBox(request.GET['status'])
	except:
		box = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	return render_to_response('lostgames.html', {
		'user_me': user_me,
		'box': box,
		'lang': lang,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'lostGames': lostGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})
