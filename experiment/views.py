from datetime import datetime
from .models import Participant, Response, TwoFourSixFinalGuess, TwoFourSixSequenceAttempt
from django.utils import timezone
from django.shortcuts import render, redirect


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
        'question': "Rule: If a card shows a triangle on one side, then it has a blue color on the other side. Select the options that could help check if the rule is violated or not." \
            if participant.group == 'A' else \
            "You are a health inspector at a social event, ensuring that pregnant attendees are not consuming alcohol. Select the options you would check to see if anyone is violating this rule.",
        'options': ['Triangle', 'Square', 'Blue color', 'Red color'] \
            if participant.group == 'A' else ['Pregnant', 'Not Pregnant', 'Drinking Water', 'Drinking Alcohol'],
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
            subject="Framing Problem",
            question_id="framing_q",
            answer=answer,
            response_time=response_time
        )

        return redirect('anchoring_bias')

    request.session['start_time'] = timezone.now().isoformat()

    return render(request, 'experiment/question_template.html', {
        'group': participant.group,
        'subject': 'Risk Problem',
        'question': "A deadly disease outbreak is expected to kill 600 people. Two treatment options are available. "
        "Which option would you choose?",
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
        'subject': 'Estimation Problem',
        'question': "Is the population of Turkey more than 10 million?" if participant.group == 'A' else "Is the population of Turkey more than 80 million?",
        'options': ['Yes', 'No'],
        'multiple_choice': False,
        'number_input': True
    })


def check_two_four_six_rule(sequence):
    """Check if the sequence fits the hidden rule (any three positive increasing numbers)."""
    return sequence[0] > 0 and sequence[1] > 0 and sequence[2] > 0 and sequence[0] < sequence[1] < sequence[2]


def two_four_six_experiment(request):
    # Get or create a final guess instance for the participant
    if 'final_guess_id' not in request.session:
        final_guess = TwoFourSixFinalGuess.objects.create()
        request.session['final_guess_id'] = final_guess.id
    else:
        final_guess = TwoFourSixFinalGuess.objects.get(id=request.session['final_guess_id'])

    message = None  # Message to show whether the sequence fits the rule

    if request.method == 'POST':
        # Handle sequence submission
        if 'submit_sequence' in request.POST:
            # Get the sequence values from the form
            sequence = [
                int(request.POST['num1']),
                int(request.POST['num2']),
                int(request.POST['num3'])
            ]
            fits_rule = check_two_four_six_rule(sequence)
            color = "green" if fits_rule else "red"
            message = f"<span style='color: {color};'>The sequence {sequence} {'follows' if fits_rule else 'does not follow'} the rule.</span>"

            # Save the sequence attempt
            TwoFourSixSequenceAttempt.objects.create(
                final_guess=final_guess,
                sequence=",".join(map(str, sequence)),
                fits_rule=fits_rule
            )

        # Handle final guess submission
        elif 'submit_guess' in request.POST:
            final_guess.final_guess = request.POST['final_guess']
            final_guess.save()
            return redirect('thanks_page')  # Redirect to the thanks page after final guess

    return render(request, 'experiment/two_four_six_experiment.html', {
        'message': message
    })


def thanks_page(request):
    return render(request, 'experiment/thanks.html')
