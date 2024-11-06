import matplotlib
from django.shortcuts import render
from django.http import HttpResponse
from experiment.models import Response, TwoFourSixSequenceAttempt, TwoFourSixFinalGuess
from io import BytesIO
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from django.core.files.base import ContentFile
import base64


def wason_results(request):
    # Define correct answers for each group
    correct_answers_a = ["A", "4"]
    correct_answers_b = ["Drinking alcohol", "Under 21 years old"]

    # Get responses for each group
    responses_a = Response.objects.filter(subject="Wason", question_id="wason_q", participant__group="A")
    responses_b = Response.objects.filter(subject="Wason", question_id="wason_q", participant__group="B")

    # Count selections for each option in Group A
    options_a = ['A', 'K', '4', '7']
    counts_a = {option: 0 for option in options_a}
    for response in responses_a:
        selected_options = eval(response.answer)  # Assuming the answer is stored as a list of choices
        for option in selected_options:
            counts_a[option] += 1

    # Count selections for each option in Group B
    options_b = ['Drinking alcohol', 'Drinking a soft drink', 'Over 21 years old', 'Under 21 years old']
    counts_b = {option: 0 for option in options_b}
    for response in responses_b:
        selected_options = eval(response.answer)  # Assuming the answer is stored as a list of choices
        for option in selected_options:
            counts_b[option] += 1

    # Generate charts for both groups
    chart_a = generate_bar_chart(counts_a, correct_answers_a)
    chart_b = generate_bar_chart(counts_b, correct_answers_b)

    return render(request, 'experiment/wason_results.html', {
        'chart_a': chart_a,
        'chart_b': chart_b,
    })


def generate_bar_chart(counts, correct_answers):
    # Set up figure with transparent background
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.0)  # Make the background transparent

    # Colors: green for correct answers, red for incorrect answers
    colors = ['green' if option in correct_answers else 'red' for option in counts.keys()]

    # Bar chart
    ax.bar(counts.keys(), counts.values(), color=colors)
    ax.set_title("Selections")
    ax.set_xlabel("Options")
    ax.set_ylabel("Number of Selections")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

    # colors
    ax.tick_params(colors='#a6a6a6')  # Set color for tick labels on both axes
    ax.spines['bottom'].set_color('#a6a6a6')  # Set color for bottom spine
    ax.spines['left'].set_color('#a6a6a6')  # Set color for left spine
    ax.yaxis.label.set_color('#a6a6a6')  # Set y-axis label color
    ax.xaxis.label.set_color('#a6a6a6')  # Set x-axis label color
    ax.title.set_color('#a6a6a6')  # Set title color

    # Save chart to a PNG image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64 for embedding in HTML
    chart_base64 = base64.b64encode(image_png).decode("utf-8")
    plt.close(fig)  # Close the plot to free memory

    return chart_base64


def linda_results(request):
    # Define correct answers
    correct_answer_a = "Linda is a bank teller"  # Expected answer for Group A
    correct_answer_b = "Linda is a bank teller"  # Same for Group B

    # Get responses for each group
    responses_a = Response.objects.filter(subject="Linda", question_id="linda_q", participant__group="A")
    responses_b = Response.objects.filter(subject="Linda", question_id="linda_q", participant__group="B")

    # Count correct and incorrect answers for Group A
    correct_a = sum(1 for response in responses_a if response.answer == correct_answer_a)
    incorrect_a = len(responses_a) - correct_a

    # Count correct and incorrect answers for Group B
    correct_b = sum(1 for response in responses_b if response.answer == correct_answer_b)
    incorrect_b = len(responses_b) - correct_b

    # Generate pie charts for both groups
    chart_a = generate_pie_chart(correct_a, incorrect_a, "Group A")
    chart_b = generate_pie_chart(correct_b, incorrect_b, "Group B")

    return render(request, 'experiment/linda_results.html', {
        'chart_a': chart_a,
        'chart_b': chart_b,
    })


def generate_pie_chart(correct, incorrect, title):
    # Set up figure with transparent background
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.0)  # Transparent background

    # Data and labels for the pie chart
    data = [correct, incorrect]
    labels = ['Correct', 'Incorrect']
    colors = ['green', 'red']

    # Plot pie chart
    ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title(title, color='#a6a6a6')
    # colors
    ax.tick_params(colors='#a6a6a6')  # Set color for tick labels on both axes
    ax.spines['bottom'].set_color('#a6a6a6')  # Set color for bottom spine
    ax.spines['left'].set_color('#a6a6a6')  # Set color for left spine
    ax.yaxis.label.set_color('#a6a6a6')  # Set y-axis label color
    ax.xaxis.label.set_color('#a6a6a6')  # Set x-axis label color
    ax.title.set_color('#a6a6a6')  # Set title color
    ax.legend(frameon=False, labelcolor='#a6a6a6')  # Legend text color to gray

    ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
           textprops={'color': "#a6a6a6"})

    # Save chart to a PNG image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64 for embedding in HTML
    chart_base64 = base64.b64encode(image_png).decode("utf-8")
    plt.close(fig)  # Close the plot to free memory

    return chart_base64


def framing_results(request):
    # Define risk-averse and risk-seeking responses for each group
    risk_averse_a = "200 people will be saved"
    risk_seeking_a = "There’s a 33% chance that all 600 will be saved, and a 67% chance that no one will be saved."
    risk_averse_b = "400 people will die"
    risk_seeking_b = "There’s a 33% chance that no one will die, and a 67% chance that all 600 will die."

    # Get responses for each group
    responses_a = Response.objects.filter(subject="Framing", question_id="framing_q", participant__group="A")
    responses_b = Response.objects.filter(subject="Framing", question_id="framing_q", participant__group="B")

    # Count risk-averse and risk-seeking responses for Group A
    count_risk_averse_a = sum(1 for response in responses_a if response.answer == risk_averse_a)
    count_risk_seeking_a = len(responses_a) - count_risk_averse_a

    # Count risk-averse and risk-seeking responses for Group B
    count_risk_averse_b = sum(1 for response in responses_b if response.answer == risk_averse_b)
    count_risk_seeking_b = len(responses_b) - count_risk_averse_b

    # Generate the stacked bar chart
    chart = generate_stacked_bar_chart(count_risk_averse_a, count_risk_seeking_a, count_risk_averse_b,
                                       count_risk_seeking_b)

    return render(request, 'experiment/framing_results.html', {
        'chart': chart,
    })


def generate_stacked_bar_chart(risk_averse_a, risk_seeking_a, risk_averse_b, risk_seeking_b):
    # Set up figure with transparent background
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.0)  # Transparent background

    # Data for the chart
    labels = ['Group A', 'Group B']
    risk_averse_counts = [risk_averse_a, risk_averse_b]
    risk_seeking_counts = [risk_seeking_a, risk_seeking_b]

    # Plotting
    ax.bar(labels, risk_averse_counts, label='Risk Averse', color='#4f83cc')  # Light blue
    ax.bar(labels, risk_seeking_counts, bottom=risk_averse_counts, label='Risk Seeking', color='#1f4f99')  # Dark blue

    # Labels and style
    ax.set_title("Risk Preferences in Framing Effect Task", color='#a6a6a6')
    ax.set_ylabel("Number of Responses", color='#a6a6a6')
    ax.tick_params(colors='#a6a6a6')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#a6a6a6')
    ax.spines['bottom'].set_color('#a6a6a6')
    ax.legend(frameon=False, labelcolor='#a6a6a6')  # Legend text color to gray

    # Save chart to a PNG image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64 for embedding in HTML
    chart_base64 = base64.b64encode(image_png).decode("utf-8")
    plt.close(fig)  # Close the plot to free memory

    return chart_base64


def anchoring_results(request):
    # Get estimated population sizes for each group
    group_a_responses = Response.objects.filter(subject="Anchoring", question_id="anchoring_number",
                                                participant__group="A")
    group_b_responses = Response.objects.filter(subject="Anchoring", question_id="anchoring_number",
                                                participant__group="B")

    # Extract estimates as lists of integers
    estimates_a = [int(response.answer) for response in group_a_responses]
    estimates_b = [int(response.answer) for response in group_b_responses]

    # Generate the box plot
    chart = generate_box_plot(estimates_a, estimates_b)

    return render(request, 'experiment/anchoring_results.html', {
        'chart': chart,
    })


def generate_box_plot(estimates_a, estimates_b):
    # Set up figure with transparent background
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.0)  # Transparent background

    # Data for the chart
    data = [estimates_a, estimates_b]
    labels = ['Group A', 'Group B']

    # Plotting with chic colors
    box = ax.boxplot(data, patch_artist=True, labels=labels)
    colors = ['#87ceeb', '#4682b4']  # Light blue for Group A, dark blue for Group B

    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    # Styling
    ax.set_title("Distribution of Population Estimates (Anchoring Bias)", color='#a6a6a6')
    ax.set_ylabel("Estimated Population Size", color='#a6a6a6')
    ax.tick_params(colors='#a6a6a6')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#a6a6a6')
    ax.spines['bottom'].set_color('#a6a6a6')

    for element in ['medians', 'whiskers', 'caps', 'fliers']:
        plt.setp(box[element], color='#a6a6a6')
    plt.setp(box['medians'], color='red')
    plt.setp(box['fliers'], markeredgecolor='#a6a6a6')

    # Save chart to a PNG image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64 for embedding in HTML
    chart_base64 = base64.b64encode(image_png).decode("utf-8")
    plt.close(fig)  # Close the plot to free memory

    return chart_base64


def two_four_six_results(request):
    # Retrieve all sequence attempts
    correct_attempts = TwoFourSixSequenceAttempt.objects.filter(fits_rule=True).count()
    incorrect_attempts = TwoFourSixSequenceAttempt.objects.filter(fits_rule=False).count()

    # Generate pie chart
    chart = generate_pie_chart_246(correct_attempts, incorrect_attempts)

    # Prepare table data
    participants_data = []
    final_guesses = TwoFourSixFinalGuess.objects.all()
    for guess in final_guesses:
        attempts = TwoFourSixSequenceAttempt.objects.filter(final_guess=guess)
        sequence_list = [
            f"<span style='color: {'green' if attempt.fits_rule else 'red'};'>{attempt.sequence}</span>"
            for attempt in attempts
        ]
        participants_data.append({
            "final_guess": guess.final_guess,
            "sequences": ", ".join(sequence_list)
        })

    return render(request, 'experiment/two_four_six_results.html', {
        'chart': chart,
        'participants_data': participants_data
    })


def generate_pie_chart_246(correct, incorrect):
    # Set up figure with transparent background
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.0)  # Transparent background

    # Data and labels for the pie chart
    data = [correct, incorrect]
    labels = ['Correct Sequences', 'Incorrect Sequences']
    colors = ['green', 'red']

    # Plot pie chart
    ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title("Correct vs Incorrect Sequence Attempts", color='#a6a6a6')

    # Save chart to a PNG image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64 for embedding in HTML
    chart_base64 = base64.b64encode(image_png).decode("utf-8")
    plt.close(fig)  # Close the plot to free memory

    return chart_base64


