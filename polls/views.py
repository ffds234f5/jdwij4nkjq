from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import login
from .models import Question, Choice, Vote
from .forms import QuestionForm
from django.shortcuts import render, redirect
from accounts.models import UserProfile
import json

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

from django.shortcuts import redirect


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if Vote.objects.filter(user=request.user, choice__question=question).exists():
        return redirect('polls:results', question_id=question.id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Вы не выбрали вариант ответа.",
        })
    else:
        Vote.objects.create(user=request.user, choice=selected_choice)
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:results', question_id=question.id)

@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            if not question.pub_date:
                question.pub_date = timezone.now()
            question.save()


            for key, value in request.POST.items():
                if key.startswith('choice_') and value.strip():
                    Choice.objects.create(question=question, choice_text=value)

            return redirect('polls:index')
    else:
        form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': form})

from homepage.forms import CommentForm
from homepage.models import Comment

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    gender_stats = {}
    for choice in question.choice_set.all():
        gender_stats[choice.choice_text] = {
            'male': 0,
            'female': 0,
            'other': 0,
        }
        votes = Vote.objects.filter(choice=choice)
        for vote in votes:
            try:
                user_profile = UserProfile.objects.get(user=vote.user)
                gender = user_profile.gender
                if gender in gender_stats[choice.choice_text]:
                    gender_stats[choice.choice_text][gender] += 1
            except UserProfile.DoesNotExist:
                continue

    comments = question.comments.all().order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.question = question
            comment.save()
            return redirect('polls:results', question_id=question.id)

    return render(request, 'polls/results.html', {
        'question': question,
        'gender_stats': json.dumps(gender_stats),
        'comments': comments,
        'form': form,
    })

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['user_has_voted'] = Vote.objects.filter(user=self.request.user, choice__question=question).exists()
        return context


