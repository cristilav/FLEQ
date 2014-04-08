# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from views_connect import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.template.loader import get_template

from fleq.quizbowl.models import *
from fleq.quizbowl.views_language import *
from fleq.quizbowl.views_tournaments_api import *


# def Questions(request):
# 	
#     if request.mobile:
#         return HttpResponseRedirect('/')
# 	
#     preguntas = Preguntas_acertadas.objects.all().values('question', 'num_aciertos').distinct().order_by('-num_aciertos')[:10]
# 	
#     data = []
#     categories = []
# 	
#     for p in preguntas:
#         data.append(int(p['num_aciertos']))
#         categories.append('Pregunta '+ str(p['question']))
#     
#     template = get_template('custom/analytics/questions.html')
#     
#      
#     return HttpResponse(template.render(RequestContext(request, {'categories': categories, 'data': data})))


# def Categories(request):
# 	
#     if request.mobile:
#         return HttpResponseRedirect('/')
#     
#     categories = Category.objects.all()
#     
#     data = []
#     
#     for c in categories:
#         
#         preguntas = Preguntas_acertadas.objects.filter(question__categories=c).values('question', 'num_aciertos').distinct()
#         
#         aciertos = 0
#         for p in preguntas:
#             aciertos += p['num_aciertos']
#         
#         data_category = {'name': c.name.encode('utf-8'), 'number': aciertos}
#         data.append(data_category)
# 
#     print data
#     
#     template = get_template('custom/analytics/categories.html')
# 
#     return HttpResponse(template.render(RequestContext(request, {'data': data})))
#    
#    
   
def Questionsgid(request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)

	preguntas = Preguntas_acertadas.objects.filter(torneo=tournament.name).values('question', 'num_aciertos').distinct().order_by('-num_aciertos')[:10]
	
	data = []
	categories = []
	
	questions = []
	namequestions = []
	
	for p in preguntas:
		data.append(int(p['num_aciertos']))
		categories.append('Pregunta '+ str(p['question']))
		questions.append(int(p['question']))
	

	question = Question.objects.all().order_by('id')
	for q in question:
		if q.id in questions:
			pregunta= (q.question).encode('utf-8')
			namequestions.append('Pregunta '+ str(q.id) +': ' + pregunta)
			
	template = get_template('custom/analytics/questions.html')

    
	return HttpResponse(template.render(RequestContext(request, {'categories': categories, 'data': data, 'id': gid, 'namequestions': namequestions})))




def Categoriesgid(request, gid):
	
    if request.mobile:
        return HttpResponseRedirect('/')

    tournament = Tournament.objects.get(id=gid)

    data = []
    
    for c in tournament.categories.all():
        
        preguntas = Preguntas_acertadas.objects.filter(question__categories=c).values('question', 'num_aciertos').distinct()
        
        aciertos = 0
        for p in preguntas:
            aciertos += p['num_aciertos']
        
        data_category = {'name': c.name.encode('utf-8'), 'number': aciertos}
        data.append(data_category)


    
    template = get_template('custom/analytics/categories.html')

    return HttpResponse(template.render(RequestContext(request, {'data': data, 'id': gid})))
   
   
def Absences(request, gid):
	
 	tournament = Tournament.objects.get(id=gid)
 	
 	data = []
 	data2 = []
 	
 	absences = Juegos.objects.filter(torneo=tournament.name).order_by('partida')
 
 	ausencias = 0
 	partidas = 0
 	personas_por_ronda = 0
 	
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct().order_by('ronda')
 	

 	partidas = len(absences)/len(rondas)
 	personas_por_ronda = partidas*2
 	
 	for r in rondas:
 		data.append('Ronda ' + str(r['ronda']))
 	
 	for a in absences:
  		if a.ronda == 1:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
  	data2.append(ausencias)
  	ausencias = 0
  	
  	for a in absences:
  		if a.ronda == 2:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
  	data2.append(ausencias)
  	ausencias = 0
  	
  	for a in absences:
  		if a.ronda == 3:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
  	data2.append(ausencias)
  	ausencias = 0
  
  	for a in absences:
  		if a.ronda == 4:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
  	data2.append(ausencias)
  	ausencias = 0
  	
  	for a in absences:
  		if a.ronda == 2:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
 
  	data2.append(ausencias)
  	ausencias = 0

 	
	if request.mobile:
         return HttpResponseRedirect('/')
        

	template = get_template('custom/analytics/absences.html')        
	return HttpResponse(template.render(RequestContext(request, {'data': data, 'data2': data2, 'id': gid, 'personas': personas_por_ronda})))



def Absencesmedium(request, gid):
	
 	tournament = Tournament.objects.get(id=gid)
 	
 	data = []
 	data2 = []
 	
 	absences = Juegos.objects.filter(torneo=tournament.name).order_by('partida')
 
 	ausencias = 0
 	partidas = 0
 	personas_por_ronda = 0
 	
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct().order_by('ronda')
 	

 	partidas = len(absences)/len(rondas)
 	personas_por_ronda = partidas*2
 	
 	for r in rondas:
 		data.append('Ronda ' + str(r['ronda']))
 	
 	for a in absences:
  		if a.ronda == 1:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
 	fausencias = 0.0
 	fpersonas = 0.0
 	resultado = 0.0
 	fausencias= float(ausencias)
 	fpersonas = float(personas_por_ronda)
 	resultado = fausencias/fpersonas
 	resultado = resultado*100
 	resultado = round(resultado, 2)
 	data2.append(resultado)
  	ausencias = 0
  	
  	for a in absences:
  		if a.ronda == 2:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
 	fausencias = 0.0
 	fpersonas = 0.0
 	resultado = 0.0
 	fausencias= float(ausencias)
 	fpersonas = float(personas_por_ronda)
 	resultado = fausencias/fpersonas
 	resultado = resultado*100
 	resultado = round(resultado, 2)
 	data2.append(resultado)
  	ausencias = 0
  	
  	for a in absences:
  		if a.ronda == 3:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
 	fausencias = 0.0
 	fpersonas = 0.0
 	resultado = 0.0
 	fausencias= float(ausencias)
 	fpersonas = float(personas_por_ronda)
 	resultado = fausencias/fpersonas
 	resultado = resultado*100
 	resultado = round(resultado, 2)
 	data2.append(resultado)
  	ausencias = 0
  
  	for a in absences:
  		if a.ronda == 4:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
 	fausencias = 0.0
 	fpersonas = 0.0
 	resultado = 0.0
 	fausencias= float(ausencias)
 	fpersonas = float(personas_por_ronda)
 	resultado = fausencias/fpersonas
 	resultado = resultado*100
 	resultado = round(resultado, 2)
 	data2.append(resultado)
  	ausencias = 0
  	
  	for a in absences:
  		if a.ronda == 2:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
 
 	fausencias = 0.0
 	fpersonas = 0.0
 	resultado = 0.0
 	fausencias= float(ausencias)
 	fpersonas = float(personas_por_ronda)
 	resultado = fausencias/fpersonas
 	resultado = resultado*100
 	resultado = round(resultado, 2)
 	data2.append(resultado)
  	ausencias = 0

 	
	if request.mobile:
         return HttpResponseRedirect('/')
        

	template = get_template('custom/analytics/absences2.html')        
	return HttpResponse(template.render(RequestContext(request, {'data': data, 'data2': data2, 'id': gid, 'personas': personas_por_ronda})))





def Questionsless(request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)

	preguntas = Preguntas_acertadas.objects.filter(torneo=tournament.name).values('question', 'num_aciertos').distinct().order_by('num_aciertos')[:10]
	
	data = []
	categories = []
	questions = []
	namequestions = []
	
	for p in preguntas:
		data.append(int(p['num_aciertos']))
		categories.append('Pregunta '+ str(p['question']))
		questions.append(int(p['question']))
		
	question = Question.objects.all().order_by('id')
	for q in question:
		if q.id in questions:
			pregunta= (q.question).encode('utf-8')
			namequestions.append('Pregunta '+ str(q.id) +': ' + pregunta)
    
	template = get_template('custom/analytics/questionsless.html')
    
	return HttpResponse(template.render(RequestContext(request, {'namequestions': namequestions, 'categories': categories, 'data': data, 'id': gid})))

def Successtime (request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
 	tournament = Tournament.objects.get(id=gid)
 	mensajes = Mensajes.objects.filter(torneo=tournament.name)
 	
 	data = []
 	categories = []
 	count = 0
 	count2 = 0
 	count3 = 0
 	count4 = 0
 	count5 = 0
 	tiempo = 0
 	tiempo2 = 0
 	tiempo3 = 0
 	tiempo4 = 0
 	tiempo5 = 0
 	
 	
 	for m in mensajes:
 		if m.acierto == 1:
 		    if m.ronda == 1:
 		    	tiempo = tiempo + m.tiempo_respuesta
 		    	count = count + 1
  		    elif m.ronda == 2:
  		    	tiempo2 = tiempo2 + m.tiempo_respuesta
 		    	count2 = count2 + 1
  		    elif m.ronda == 3:
  		    	tiempo3 = tiempo3 + m.tiempo_respuesta
 		    	count3 = count3 + 1
  		    elif m.ronda == 4:
  		    	tiempo4 = tiempo4 + m.tiempo_respuesta
 		    	count4 = count4 + 1
 		    elif m.ronda ==5:
 		    	tiempo5 = tiempo5 + m.tiempo_respuesta
 		    	count5 = count5 + 1
 		    	
 	data.append(tiempo/count)
 	data.append(tiempo2/count2)
 	data.append(tiempo3/count3)
 	data.append(tiempo4/count4)
 	data.append(tiempo5/count5)
 	
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct()
	for r in rondas:
		categories.append('Ronda ' + str(r['ronda']))
   
	template = get_template('custom/analytics/successtime.html')
    
	return HttpResponse(template.render(RequestContext(request, {'data': data, 'categories':categories, 'id': gid})))


	
# 	if request.mobile:
# 		return HttpResponseRedirect('/')
# 	
#  	tournament = Tournament.objects.get(id=gid)
#  
#  	mensajes = Mensajes.objects.filter(torneo=tournament.name)
#  	
#  	data = []
#  	data2 = []
#  	data3 = []
#  	data4 = []
#  	data5 = []
#  	
#  	
#  	for m in mensajes:
#  		if m.acierto == 1:
#  		    if m.ronda == 1:
#  		    	tiempo = m.tiempo_respuesta
#  		    	count = count + 1
#   		    elif m.ronda == 2:
#   		    	data2.append(m.tiempo_respuesta)
#   		    elif m.ronda == 3:
#   		    	data3.append(m.tiempo_respuesta)
#   		    elif m.ronda == 4:
#   		    	data4.append(m.tiempo_respuesta)
#  		    elif m.ronda ==5:
#  		    	data5.append(m.tiempo_respuesta)
# 	
#    
# 	template = get_template('custom/analytics/successtime.html')
#     
# 	return HttpResponse(template.render(RequestContext(request, {'data': data,  'data2': data2, 'data3': data3, 'data4':data4, 'data5':data5, 'id': gid})))


def General(request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)
	
	mensajes = Mensajes.objects.filter(torneo=tournament.name).order_by('partida')
	
	categories = []
	
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct().order_by('ronda')
	for r in rondas:
		categories.append('Ronda ' + str(r['ronda']))
	
# 	acierto1 = 0
# 	fallo1 = 0
# 	preguntas1 = 0
# 	ronda1 = Mensajes.objects.filter(ronda=1)
# 	for r in ronda1:
#  		if r.acierto == 1:
#  			acierto1 = acierto1 + 1
#  			print "aciertos" + str(acierto1)
#  		if r.acierto == 0:
#  			fallo1 = fallo1 + 1
#  			print "fallos" + str(fallo1)
#  		if r.acierto == 2:
#  			if r.tipo == 0:
#  			    preguntas1 = preguntas1 + 1
#  			    print preguntas1
#  			
	
	
 	acierto1 = 0
 	acierto2 = 0
  	acierto3 = 0
  	acierto4 = 0
  	acierto5 = 0
  	fallo1 = 0
 	fallo2 = 0
 	fallo3 = 0
 	fallo4 = 0
 	fallo5 = 0
 	preguntas1 = 0
 	preguntas2 = 0
 	preguntas3 = 0
 	preguntas4 = 0
 	preguntas5 = 0
 	
 	
 	
 	for m in mensajes:
 		if m.acierto == 1:
 		    if m.ronda == 1:
 		    	acierto1 = acierto1 + 1
  		    if m.ronda == 2:
  		    	acierto2 = acierto2 + 1
  		    elif m.ronda == 3:
  		    	acierto3 = acierto3 + 1
  		    elif m.ronda == 4:
  		    	acierto4 = acierto4 + 1
 		    elif m.ronda ==5:
 		    	acierto5 = acierto5 + 1    	
 		elif m.acierto == 0:
 		    if m.ronda == 1:
 		    	fallo1 = fallo1 + 1
  		    elif m.ronda == 2:
  		    	fallo2 = fallo2 + 1
  		    elif m.ronda == 3:
  		    	fallo3 = fallo3 + 1
  		    elif m.ronda == 4:
  		    	fallo4 = fallo4 + 1
 		    elif m.ronda ==5:
 		    	fallo5 = fallo5 + 1
 		elif m.acierto == 2:
  		    if m.tipo == 0:
  		 	  	if m.ronda == 1:
  		 	  		preguntas1 = preguntas1 + 1
  		 	  	elif m.ronda == 2:
  		 	  		preguntas2 = preguntas2 + 1
  		 	  	elif m.ronda == 3:
  		 	  		preguntas3 = preguntas3 + 1
  		 	  	elif m.ronda == 4:
  		 	  		preguntas4 = preguntas4 + 1
  		 	  	elif m.ronda ==5:
  		 	  		preguntas5 = preguntas5 + 1	 		    	
 	template = get_template('custom/analytics/general.html')

 
	return HttpResponse(template.render(RequestContext(request, {'acierto1': acierto1, 'acierto2': acierto2, 'acierto3': acierto3, 'acierto4': acierto4, 'acierto5': acierto5, 'fallo1': fallo1, 'fallo2': fallo2, 'fallo3': fallo3, 'fallo4': fallo4, 'fallo5': fallo5, 'preguntas1': preguntas1, 'preguntas2': preguntas2, 'preguntas3': preguntas3, 'preguntas4': preguntas4, 'preguntas5': preguntas5, 'categories': categories, 'id': gid})))



def QuestionRoundssgid(request, gid):
 	
	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)
	
	mensajes = Mensajes.objects.filter(torneo=tournament.name).order_by('partida')
	
	data = []
	categories = []
	puno = 0
	pdos = 0
	ptres = 0
	pcuatro = 0
	pcinco = 0
	
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct().order_by('ronda')
	for r in rondas:
		categories.append('Ronda ' + str(r['ronda']))
		
 	for m in mensajes:
 		if m.acierto == 1:
 		    if m.ronda == 1:
 		    	puno= puno + 1
  		    if m.ronda == 2:
  		    	pdos = pdos + 1
  		    elif m.ronda == 3:
  		    	ptres = ptres + 1
  		    elif m.ronda == 4:
  		    	pcuatro = pcuatro + 1
 		    elif m.ronda ==5:
 		    	pcinco = pcinco + 1
 		    	
	
	data.append(puno)
 	data.append(pdos)
 	data.append(ptres)
 	data.append(pcuatro)
 	data.append(pcinco)
 	
	template = get_template('custom/analytics/gamesround.html')
     
	return HttpResponse(template.render(RequestContext(request, {'categories': categories, 'data': data, 'id': gid })))


def Questionmediumsgid(request, gid):

	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)
	
	mensajes = Mensajes.objects.filter(torneo=tournament.name).order_by('partida')
	
	data = []
	data2 = []
	categories = []
	puno = 0
	pdos = 0
	ptres = 0
	pcuatro = 0
	pcinco = 0
	
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct().order_by('ronda')
	for r in rondas:
		categories.append('Ronda ' + str(r['ronda']))
		
 	for m in mensajes:
 		if m.acierto == 1:
 		    if m.ronda == 1:
 		    	puno= puno + 1
  		    if m.ronda == 2:
  		    	pdos = pdos + 1
  		    elif m.ronda == 3:
  		    	ptres = ptres + 1
  		    elif m.ronda == 4:
  		    	pcuatro = pcuatro + 1
 		    elif m.ronda ==5:
 		    	pcinco = pcinco + 1
	
	
 	mensajes1 = Mensajes.objects.filter(torneo=tournament.name).filter(tipo=0).filter(ronda=1).order_by('partida')
 	mensajes2 = Mensajes.objects.filter(torneo=tournament.name).filter(tipo=0).filter(ronda=2).order_by('partida')
 	mensajes3 = Mensajes.objects.filter(torneo=tournament.name).filter(tipo=0).filter(ronda=3).order_by('partida')
 	mensajes4 = Mensajes.objects.filter(torneo=tournament.name).filter(tipo=0).filter(ronda=4).order_by('partida')
 	mensajes5 = Mensajes.objects.filter(torneo=tournament.name).filter(tipo=0).filter(ronda=5).order_by('partida')
 	
 	
 	fpuno = 0.0
 	fmensajes1 = 0.0
 	resultado1 = 0.0
 	fpuno= float(puno)
 	fmensajes1 = float(len(mensajes1))
 	resultado1 = fpuno/fmensajes1
 	resultado1 = resultado1*100
 	resultado1 = round(resultado1, 2)
 	

	fpdos = 0.0
 	fmensajes2 = 0.0
 	resultado2 = 0.0
 	fpdos= float(pdos)
 	fmensajes2 = float(len(mensajes2))
 	resultado2 = fpdos/fmensajes1
 	resultado2 = resultado2*100
 	resultado2 = round(resultado2, 2)

	fptres = 0.0
 	fmensajes3 = 0.0
 	resultado3 = 0.0
 	fptres= float(ptres)
 	fmensajes3 = float(len(mensajes3))
 	resultado3 = fptres/fmensajes3
 	resultado3 = resultado3*100
 	resultado3 = round(resultado3, 2)

	fpcuatro = 0.0
 	fmensajes4 = 0.0
 	resultado4 = 0.0
 	fpcuatro= float(pcuatro)
 	fmensajes4 = float(len(mensajes4))
 	resultado4 = fpcuatro/fmensajes4
 	resultado4 = resultado4*100
 	resultado4 = round(resultado4, 2)

	fpcinco = 0.0
 	fmensajes5 = 0.0
 	resultado5 = 0.0
 	fpcinco= float(pcinco)
 	fmensajes5 = float(len(mensajes5))
 	resultado5 = fpuno/fmensajes5
 	resultado5 = resultado5*100
 	resultado5 = round(resultado5, 2)


	data.append(resultado1)
 	data.append(resultado2)
 	data.append(resultado3)
 	data.append(resultado4)
 	data.append(resultado5)
 	

 	template = get_template('custom/analytics/gamesmedium.html')
     
	return HttpResponse(template.render(RequestContext(request, {'data': data, 'categories': categories, 'id': gid })))


def MaxSuccesstimegid (request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
 	tournament = Tournament.objects.get(id=gid)
 	mensajes = Mensajes.objects.filter(torneo=tournament.name).order_by('partida')
 	
 	data = []
 	categories = []
 
 	tiempo = 0
 	tiempo2 = 0
 	tiempo3 = 0
 	tiempo4 = 0
 	tiempo5 = 0
 	
 	
 	for m in mensajes:
 		if m.acierto == 1:
 		    if m.ronda == 1:
 		    	if m.tiempo_respuesta >= tiempo:
 		    		tiempo = m.tiempo_respuesta
  		    elif m.ronda == 2:
  		    	if m.tiempo_respuesta >= tiempo2:
 		    		tiempo2 = m.tiempo_respuesta
  		    elif m.ronda == 3:
  		    	if m.tiempo_respuesta >= tiempo3:
 		    		tiempo3 = m.tiempo_respuesta
  		    elif m.ronda == 4:
  		    	if m.tiempo_respuesta >= tiempo4:
 		    		tiempo4 = m.tiempo_respuesta
 		    elif m.ronda ==5:
 		    	if m.tiempo_respuesta >= tiempo5:
 		    		tiempo5 = m.tiempo_respuesta
 		    	
 	data.append(tiempo)
 	data.append(tiempo2)
 	data.append(tiempo3)
 	data.append(tiempo4)
 	data.append(tiempo5)
 	
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct().order_by('ronda')
	for r in rondas:
		categories.append('Ronda ' + str(r['ronda']))
   
	template = get_template('custom/analytics/maxsuccesstime.html')
    
	return HttpResponse(template.render(RequestContext(request, {'data': data, 'categories':categories, 'id': gid})))



def Summarygid (request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)
	
	numpreguntas = 0
	numcategories = 0
	categorias = []
	numrondas = 0
	contador = 0
	
	preguntaspartida = Mensajes.objects.filter(torneo=tournament.name).filter(tipo =0).order_by('partida')
	preguntas = Mensajes.objects.filter(torneo=tournament.name).filter(acierto=1).order_by('partida')
	
	numpregpartida = len(preguntaspartida)
	tournament = Tournament.objects.get(id=gid)
	categories = tournament.categories.all()
	numpreguntas= len(preguntas)
	numcategories = len(categories)

	
 	fnumpregpartida = 0.0
 	fnumpreguntas = 0.0
 	resultado1 = 0.0
 	fnumpregpartida= float(numpregpartida)
 	fnumpreguntas = float(numpreguntas)
 	resultado1 = fnumpreguntas/fnumpregpartida
 	resultado1 = resultado1*100
 	resultado1 = round(resultado1, 2)
	
	for c in categories:
		categorias.append(c.name.encode('utf-8'))
	
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct().order_by('ronda')
	numrondas = len(rondas)
	
	
 	absences = Juegos.objects.filter(torneo=tournament.name).order_by('partida')
 
 	ausencias = 0
 	partidas = 0
 	personas_por_ronda = 0
 	data = []
 	data2 = []
 	
 	partidas2 = len(absences)/len(rondas)
 	partidas = (len(absences)/len(rondas))*len(rondas)
 	personas_por_ronda = partidas2*2
 	partidas_por_ronda = personas_por_ronda/2
 	ausenciasposibles = partidas*2
	
	#+++++++++++++++++++++++++++++++++++ausencias+++++++++++++++++++
	acierto1 = 0
	for a in absences:
  		if a.ronda == 1:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
  	for a in absences:
  		if a.ronda == 2:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1

  	for a in absences:
  		if a.ronda == 3:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  
  	for a in absences:
  		if a.ronda == 4:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1

  	
  	for a in absences:
  		if a.ronda == 2:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
 
#++++++++++++++++++ausencias
	    	

 	fausencias = 0.0
 	fposibles= 0.0
 	resultado = 0.0
 	fausencias= float(ausencias)
 	fposibles = float(ausenciasposibles)
 	resultado = fausencias/fposibles
 	resultado = resultado*100
 	resultado = round(resultado, 2)



 	template = get_template('custom/analytics/summary.html')

 
	return HttpResponse(template.render(RequestContext(request, {'resultado1': resultado1, 'resultado': resultado, 'partidas_por_ronda': partidas_por_ronda, 'ausencias': ausencias, 'partidas': partidas, 'personas_por_ronda': personas_por_ronda, 'numpregpartida': numpregpartida, 'tournament': tournament, 'numpreguntas': numpreguntas, 'numcategories': numcategories, 'categorias': categorias,'numrondas': numrondas, 'id': gid})))




def Usersgid(request, gid):
  	
 	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	tournament = Tournament.objects.get(id=gid)
	rounds = Round.objects.filter(tournament = tournament).order_by('round_number')

	# Generate Score Table by this Tournament
	allscores = Score.objects.filter(tournament=tournament).order_by('-points', '-questions_won', 'questions_lost', 'player')
	scores = []
	pos = 0

	for userScore in allscores:
		userProfile = UserProfile.objects.get(user=userScore.player)
		user = {}
		user['profile'] = userProfile
		user['score'] = userScore.points
		
		# Create tournament positions
		if pos == 0:
			user['pos'] = pos+1
		else:
			if scores[pos-1]['score'] == userScore.points:
				user['pos'] = scores[pos-1]['pos']
			else:
				user['pos'] = pos+1
		
		# Initializing vars for question stats
		user['winner_questions'] = userScore.questions_won
		user['loser_questions'] = userScore.questions_lost
		user['winner_games'] = 0
		user['loser_games'] = 0
		
		# For each user, calculate how many games did he play
		gamesUser = []
		for r in rounds:
			game = Game.objects.filter(Q(round = r), Q(player1 = userProfile.user) | Q(player2 = userProfile.user), Q(log=True))
			try:
				#if game[0] and game[0].log:
				if game[0]:				
					gamesUser.append(game)
					# Total points won and lost
					try:
						if game[0].winner != userScore.player and game[0].winner.username != "jgonzalez":
							user['loser_games'] += 1
						elif game[0].winner.username == "FLEQBOT":
							user['loser_games'] += 1
						elif game[0].winner == userScore.player:
							user['winner_games'] += 1
					except:
						continue
			except:
				continue
		
		user['reflection_days'] = user['score'] - user['winner_games']
		user['total_games'] = user['loser_games'] + user['winner_games']
		
		# Save user stats and increment counter var
		scores.append(user)
		pos += 1

	rounds = Round.objects.filter(tournament=tournament)
	games = Game.objects.all()

	join = False
	disjoin = False

	if not (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		join = True
	elif (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		disjoin = True

	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


 	template = 'custom/analytics/user_statistics.html'
	
	userprofile = UserProfile.objects.get(user=request.user)
	timezone = int(userprofile.timezone)
 	
 	
 	data2 = []
 	cores = Score.objects.filter(tournament=tournament).order_by('-points')
 	for c in cores:
 		if (c.points) > 3:
 			data2.append(int(c.points))
 			
 	print data2

 	return render_to_response(template, {
			'id' : gid,
 			'user_me': request.user,
 			'timezone': timezone,
 			'tournament': tournament,
 			'join': join,
 			'disjoin': disjoin,
 			'scores': scores,
 			'rounds': rounds,
 			'games': games,
 			'lang': lang,
 			'data2': data2,
 		})



def Usersnoplaygid(request, gid):
  	
 	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	tournament = Tournament.objects.get(id=gid)
	rounds = Round.objects.filter(tournament = tournament).order_by('round_number')

	# Generate Score Table by this Tournament
	allscores = Score.objects.filter(tournament=tournament).order_by('-points', '-questions_won', 'questions_lost', 'player')
	scores = []
	pos = 0

	for userScore in allscores:
		userProfile = UserProfile.objects.get(user=userScore.player)
		user = {}
		user['profile'] = userProfile
		user['score'] = userScore.points
		
		# Create tournament positions
		if pos == 0:
			user['pos'] = pos+1
		else:
			if scores[pos-1]['score'] == userScore.points:
				user['pos'] = scores[pos-1]['pos']
			else:
				user['pos'] = pos+1
		
		# Initializing vars for question stats
		user['winner_questions'] = userScore.questions_won
		user['loser_questions'] = userScore.questions_lost
		user['winner_games'] = 0
		user['loser_games'] = 0
		
		# For each user, calculate how many games did he play
		gamesUser = []
		for r in rounds:
			game = Game.objects.filter(Q(round = r), Q(player1 = userProfile.user) | Q(player2 = userProfile.user), Q(log=True))
			try:
				#if game[0] and game[0].log:
				if game[0]:				
					gamesUser.append(game)
					# Total points won and lost
					try:
						if game[0].winner != userScore.player and game[0].winner.username != "jgonzalez":
							user['loser_games'] += 1
						elif game[0].winner.username == "FLEQBOT":
							user['loser_games'] += 1
						elif game[0].winner == userScore.player:
							user['winner_games'] += 1
					except:
						continue
			except:
				continue
		
		user['reflection_days'] = user['score'] - user['winner_games']
		user['total_games'] = user['loser_games'] + user['winner_games']
		
		# Save user stats and increment counter var
		scores.append(user)
		pos += 1

	rounds = Round.objects.filter(tournament=tournament)
	games = Game.objects.all()

	join = False
	disjoin = False

	if not (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		join = True
	elif (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		disjoin = True

	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


 	template = 'custom/analytics/usersnoplay.html'
 
	print
	
	userprofile = UserProfile.objects.get(user=request.user)
	timezone = int(userprofile.timezone)
 	
 	
 	data2 = []
 	cores = Score.objects.filter(tournament=tournament).order_by('questions_lost')[:10]
 	for c in cores:
  		data2.append(int(c.questions_lost))
 			
 	print data2

 	return render_to_response(template, {
			'id' : gid,
 			'user_me': request.user,
 			'timezone': timezone,
 			'tournament': tournament,
 			'join': join,
 			'disjoin': disjoin,
 			'scores': scores,
 			'rounds': rounds,
 			'games': games,
 			'lang': lang,
 			'data2': data2,
 		})


def Userswinnerquestions(request, gid):
  	
 	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	tournament = Tournament.objects.get(id=gid)
	rounds = Round.objects.filter(tournament = tournament).order_by('round_number')

	# Generate Score Table by this Tournament
	allscores = Score.objects.filter(tournament=tournament).order_by('-points', '-questions_won', 'questions_lost', 'player')
	scores = []
	pos = 0

	for userScore in allscores:
		userProfile = UserProfile.objects.get(user=userScore.player)
		user = {}
		user['profile'] = userProfile
		user['score'] = userScore.points
		
		# Create tournament positions
		if pos == 0:
			user['pos'] = pos+1
		else:
			if scores[pos-1]['score'] == userScore.points:
				user['pos'] = scores[pos-1]['pos']
			else:
				user['pos'] = pos+1
		
		# Initializing vars for question stats
		user['winner_questions'] = userScore.questions_won
		user['loser_questions'] = userScore.questions_lost
		user['winner_games'] = 0
		user['loser_games'] = 0
		
		# For each user, calculate how many games did he play
		gamesUser = []
		for r in rounds:
			game = Game.objects.filter(Q(round = r), Q(player1 = userProfile.user) | Q(player2 = userProfile.user), Q(log=True))
			try:
				#if game[0] and game[0].log:
				if game[0]:				
					gamesUser.append(game)
					# Total points won and lost
					try:
						if game[0].winner != userScore.player and game[0].winner.username != "jgonzalez":
							user['loser_games'] += 1
						elif game[0].winner.username == "FLEQBOT":
							user['loser_games'] += 1
						elif game[0].winner == userScore.player:
							user['winner_games'] += 1
					except:
						continue
			except:
				continue
		
		user['reflection_days'] = user['score'] - user['winner_games']
		user['total_games'] = user['loser_games'] + user['winner_games']
		
		# Save user stats and increment counter var
		scores.append(user)
		pos += 1

	rounds = Round.objects.filter(tournament=tournament)
	games = Game.objects.all()

	join = False
	disjoin = False

	if not (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		join = True
	elif (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		disjoin = True

	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


 	template = 'custom/analytics/usersnoplay.html'
 
	
	userprofile = UserProfile.objects.get(user=request.user)
	timezone = int(userprofile.timezone)
 	
 	
 	data2 = []
 	cores = Score.objects.filter(tournament=tournament).order_by('-questions_won')[:25]
 	for c in cores:
  		data2.append(int(c.questions_lost))
 			

 	return render_to_response(template, {
			'id' : gid,
 			'user_me': request.user,
 			'timezone': timezone,
 			'tournament': tournament,
 			'join': join,
 			'disjoin': disjoin,
 			'scores': scores,
 			'rounds': rounds,
 			'games': games,
 			'lang': lang,
 			'data2': data2,
 		})



 
def Questionsmoreappear(request, gid):
 	
 	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)

	preguntas = Preguntas_acertadas.objects.filter(torneo=tournament.name).values('question', 'num_aciertos').distinct().order_by('-num_aciertos')[:12]
	
	data = []
	categories = []
	dresult = []
	
	questions = []
	namequestions = []
	
	for p in preguntas:
		data.append(int(p['num_aciertos']))
		categories.append('Pregunta '+ str(p['question']))
		questions.append(int(p['question']))
 	
 	numpreguntas = Num_preguntas.objects.filter(torneo = tournament.name).order_by('-veces')
 	
 	aciertos = 0
 	faciertos = 1.0
 	resultado = 0.0
 	fveces = 1.0
 				
 	for p in preguntas:
 		aciertos = (int(p['num_aciertos']))
 		faciertos = float(aciertos)
	 	for n in numpreguntas:
	 		if (int(p['question'])) == n.numquestion:
	 			veces = n.veces
	 			fveces = float(veces)
	 			resultado = (faciertos/fveces)
	 			if resultado >= 1.0:
	 				resultado = 1.0
	 				resultado = resultado*100
	 				dresult.append(resultado)
	 			else:
	 				resultado = (faciertos/fveces)*100
	 				resultado = round(resultado, 2)
	 				dresult.append(resultado)

	 				
#  	dresult = sorted(dresult,  reverse = True)
#  	dresult = dresult[1:10]
 	
 	question = Question.objects.all().order_by('id')
 	for q in question:
 		if q.id in questions:
 			pregunta= (q.question).encode('utf-8')
 			namequestions.append('Pregunta '+ str(q.id) +': ' + pregunta)
 			
  	template = get_template('custom/analytics/qmoreappear.html')

 	return HttpResponse(template.render(RequestContext(request, {'categories': categories, 'dresult': dresult, 'id': gid, 'namequestions': namequestions})))

 
 #la primera vez para guardarlas
# 
#   	veces = 0
#    
#   	qtorneo = Mensajes.objects.filter(torneo=tournament.name).filter(tipo =0).order_by('num_question')
#    	
#   	questions = Question.objects.order_by('question')
#   	
#   	
#   	for q in questions:
#   		for qt in qtorneo:
#   			if (q.question).lower() == qt.texto:
#   				veces = veces + 1
#   		
#   		nuevo = Num_preguntas(numquestion= q.id, veces = veces, torneo = tournament.name)
#   		nuevo.save()
#   		veces = 0
