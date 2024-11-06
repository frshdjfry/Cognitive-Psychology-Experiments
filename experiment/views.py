from datetime import datetime

from django.shortcuts import render

# Create your views here.
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Participant, Response
from django.utils import timezone

def landing_page(request):
    # Assign unique ID and group
    if 'participant_id' not in request.session:
        participant = Participant.objects.create()
        if participant.id % 2:
            group = 'A'
        else:
            group = 'B'
        participant.group = group
        participant.save()
        request.session['participant_id'] = participant.id

    return render(request, 'experiment/landing_page.html')


def wason_task(request):
    participant = Participant.objects.get(id=request.session['participant_id'])
    if request.method == 'POST':
        answer = request.POST.getlist('answer')

        # Calculate response time
        start_time = request.session.get('start_time')
        if start_time:
            response_time = timezone.now() - datetime.fromisoformat(start_time)
        else:
            response_time = None

        # Save response with response time
        Response.objects.create(
            participant=participant,
            subject="Wason",
            question_id="wason_q",
            answer=str(answer),
            response_time=response_time
        )
        return redirect('linda_problem')

    # Set the start time when page is loaded
    request.session['start_time'] = timezone.now().isoformat()

    return render(request, 'experiment/question_template.html', {
        'group': participant.group,
        'subject': 'Wason Selection Task',
        'question': "If a card has a vowel on one side, then it has an even number on the other side." if participant.group == 'A' else "If someone is drinking alcohol, then they must be over 21 years old.",
        'options': ['A', 'K', '4', '7'] if participant.group == 'A' else ['Drinking alcohol', 'Drinking a soft drink',
                                                                          'Over 21 years old', 'Under 21 years old'],
        'multiple_choice': True
    })


# Apply similar changes to other views

def linda_problem(request):
    participant = Participant.objects.get(id=request.session['participant_id'])
    if request.method == 'POST':
        if participant.group == 'A':
            answer = request.POST['answer']
        elif participant.group == 'B':
            bank_teller_number = int(request.POST.get('bank_teller_number', 0))
            feminist_number = int(request.POST.get('feminist_number', 0))
            answer = "Linda is a bank teller" if bank_teller_number > feminist_number else "Linda is a bank teller and active in the feminist movement"

        # Calculate response time
        start_time = request.session.get('start_time')
        if start_time:
            response_time = timezone.now() - datetime.fromisoformat(start_time)
        else:
            response_time = None

        # Save response with response time
        Response.objects.create(
            participant=participant,
            subject="Linda",
            question_id="linda_q",
            answer=answer,
            response_time=response_time
        )

        return redirect('framing_effect')

    request.session['start_time'] = timezone.now().isoformat()

    return render(request, 'experiment/question_template.html', {
        'group': participant.group,
        'subject': 'Linda Problem',
        'question': "Which is more probable?" if participant.group == 'A' else "Out of 100 people like Linda, how many would be:",
        'options': ['Linda is a bank teller',
                    'Linda is a bank teller and active in the feminist movement'] if participant.group == 'A' else None,
        'number_inputs': participant.group == 'B'
    })


def framing_effect(request):
    participant = Participant.objects.get(id=request.session['participant_id'])
    if request.method == 'POST':
        answer = request.POST['answer']

        # Calculate response time
        start_time = request.session.get('start_time')
        if start_time:
            response_time = timezone.now() - datetime.fromisoformat(start_time)
        else:
            response_time = None

        # Save response with response time
        Response.objects.create(
            participant=participant,
            subject="Framing",
            question_id="framing_q",
            answer=answer,
            response_time=response_time
        )

        return redirect('anchoring_bias')

    request.session['start_time'] = timezone.now().isoformat()

    return render(request, 'experiment/question_template.html', {
        'group': participant.group,
        'subject': 'Framing Effect',
        'question': "Which option would you choose?",
        'options': ["200 people will be saved",
                    "There’s a 33% chance that all 600 will be saved, and a 67% chance that no one will be saved."] if participant.group == 'A' else [
            "400 people will die",
            "There’s a 33% chance that no one will die, and a 67% chance that all 600 will die."],
        'multiple_choice': False
    })


def anchoring_bias(request):
    participant = Participant.objects.get(id=request.session['participant_id'])
    if request.method == 'POST':
        answer = request.POST['answer']
        number_answer = request.POST.get('number', None)

        # Calculate response time
        start_time = request.session.get('start_time')
        if start_time:
            response_time = timezone.now() - datetime.fromisoformat(start_time)
        else:
            response_time = None

        # Save response with response time
        Response.objects.create(
            participant=participant,
            subject="Anchoring",
            question_id="anchoring_q",
            answer=answer,
            response_time=response_time
        )

        if number_answer:
            Response.objects.create(participant=participant, subject="Anchoring", question_id="anchoring_number",
                                    answer=number_answer, response_time=response_time)

        return redirect('thanks_page')

    request.session['start_time'] = timezone.now().isoformat()

    return render(request, 'experiment/question_template.html', {
        'group': participant.group,
        'subject': 'Anchoring Bias',
        'question': "Is the population of Turkey more than 10 million?" if participant.group == 'A' else "Is the population of Turkey more than 80 million?",
        'options': ['Yes', 'No'],
        'multiple_choice': False,
        'number_input': True
    })


def thanks_page(request):
    return render(request, 'experiment/thanks.html')

