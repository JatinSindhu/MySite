from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

# Create your views here.
def index(request):
	latest_question_list = Question.objects.order_by('pub_date')[:5]
#	template = loader.get_template('polls/index.html')
#	context = RequestContext( request , {
#		'latest_question_list': latest_question_list,
#		})
#	return HttpResponse(template.render(context))
	context = {'latest_question_list' : latest_question_list}
	return render(request,'polls/index.html', context)

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question':question})
#	return HttpResponse("You are looking at question %s." %question_id)

def results(request, question_id):
        question = get_object_or_404(Question , pk=question_id)
        return render(request, 'polls/results.html', {'question':question})
	#response = "You are looking at the results of question %s"
	#return HttpResponse(response % question_id)

def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError,Choice.DoesNotExist):
		#Redisplay the form
		return render(request , 'polls/detail.html', {'question':p, 'error_message': "You did not select a choice",})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('results', args=(p.id,)))
#	return HttpResponse("You are voting on question %s." %question_id)
