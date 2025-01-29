from django.test import TestCase
import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


from django.test import TestCase, Client
from polls.models import Question, Choice, Vote
from django.contrib.auth.models import User

class PollsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='superpuperpass123')
        self.question = Question.objects.create(question_text="Test Question", pub_date=timezone.now(), created_by=self.user)
        self.choice = Choice.objects.create(question=self.question, choice_text="Test Choice")

    def test_vote_functionality(self):
        self.client.login(username='testuser', password='superpuperpass123')
        response = self.client.post(f'/polls/{self.question.id}/vote/', {'choice': self.choice.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Vote.objects.filter(user=self.user, choice=self.choice).exists())

    def test_vote_limit(self):
        self.client.login(username='testuser', password='superpuperpass123')
        self.client.post(f'/polls/{self.question.id}/vote/', {'choice': self.choice.id})
        response = self.client.post(f'/polls/{self.question.id}/vote/', {'choice': self.choice.id})
        self.assertEqual(response.status_code, 302)
        votes_count = Vote.objects.filter(user=self.user, choice=self.choice).count()
        self.assertEqual(votes_count, 1)

    def test_poll_completion(self):
        self.question.is_active = False
        self.question.save()
        self.client.login(username='testuser', password='superpuperpass123')
        response = self.client.get(f'/polls/{self.question.id}/')
        self.assertEqual(response.status_code, 302)
