from django.shortcuts import render

# Create your views here.
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Participant, Response

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
        Response.objects.create(participant=participant, subject="Wason", question_id="wason_q", answer=str(answer))
        return redirect('linda_problem')
    
    return render(request, 'experiment/question_template.html', {
        'group': participant.group,
        'subject': 'Wason Selection Task',
        'question': "If a card has a vowel on one side, then it has an even number on the other side." if participant.group == 'A' else "If someone is drinking alcohol, then they must be over 21 years old.",
        'options': ['A', 'K', '4', '7'] if participant.group == 'A' else ['Drinking alcohol', 'Drinking a soft drink', 'Over 21 years old', 'Under 21 years old'],
        'multiple_choice': True
    })


def linda_problem(request):
    participant = Participant.objects.get(id=request.session['participant_id'])

    if request.method == 'POST':
        if participant.group == 'A':
            # Group A: Simple single-choice selection
            answer = request.POST['answer']
            Response.objects.create(participant=participant, subject="Linda", question_id="linda_q", answer=answer)

        elif participant.group == 'B':
            # Group B: Two number inputs for probability estimates
            bank_teller_number = int(request.POST.get('bank_teller_number', 0))
            feminist_number = int(request.POST.get('feminist_number', 0))

            # Determine answer based on comparison of the two numbers
            if bank_teller_number > feminist_number:
                answer = "Linda is a bank teller"
            else:
                answer = "Linda is a bank teller and active in the feminist movement"

            # Save the answer as if it was a selection
            Response.objects.create(participant=participant, subject="Linda", question_id="linda_q", answer=answer)
            # Optionally, save the raw numbers for additional analysis
            Response.objects.create(participant=participant, subject="Linda", question_id="linda_bank_teller_number",
                                    answer=str(bank_teller_number))
            Response.objects.create(participant=participant, subject="Linda", question_id="linda_feminist_number",
                                    answer=str(feminist_number))

        # Redirect to the next question (e.g., framing effect)
        return redirect('framing_effect')

    # Context for rendering the form based on the participant's group
    if participant.group == 'A':
        context = {
            'group': participant.group,
            'subject': 'Linda Problem',
            'question': "Which is more probable?",
            'options': ['Linda is a bank teller', 'Linda is a bank teller and active in the feminist movement'],
            'multiple_choice': False
        }
    else:  # Group B
        context = {
            'group': participant.group,
            'subject': 'Linda Problem',
            'question': "Out of 100 people like Linda, how many would be:",
            'number_inputs': True
        }

    return render(request, 'experiment/question_template.html', context)


def framing_effect(request):
    participant = Participant.objects.get(id=request.session['participant_id'])
    if request.method == 'POST':
        answer = request.POST['answer']
        Response.objects.create(participant=participant, subject="Framing", question_id="framing_q", answer=answer)
        return redirect('anchoring_bias')
    
    return render(request, 'experiment/question_template.html', {
        'group': participant.group,
        'subject': 'Framing Effect',
        'question': "Which option would you choose?",
        'options': ["200 people will be saved", "There’s a 33% chance that all 600 will be saved, and a 67% chance that no one will be saved."] if participant.group == 'A' else ["400 people will die", "There’s a 33% chance that no one will die, and a 67% chance that all 600 will die."],
        'multiple_choice': False
    })

def anchoring_bias(request):
    participant = Participant.objects.get(id=request.session['participant_id'])
    if request.method == 'POST':
        answer = request.POST['answer']
        number_answer = request.POST.get('number', None)
        Response.objects.create(participant=participant, subject="Anchoring", question_id="anchoring_q", answer=answer)
        if number_answer:
            Response.objects.create(participant=participant, subject="Anchoring", question_id="anchoring_number", answer=number_answer)
        return redirect('thanks_page')
    
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

