from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

import datetime

from .models import Question

# Create your tests here.

def create_question(question_text, days):
    """
    :param question_text:
    :param days:
    :return:

    create a quesiton with the given question_text and
    publisehd the given number of days offset to now
    negative is past, positive for questions that have yet tobe published
    """
    time=timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionModelTests(TestCase):
    def test_was_recently_published_with_future_question(self):
        """
        was_recently_published method should return false for question whose pub_date
        is in the future

        :return:
        """
        time=timezone.now()+datetime.timedelta(days=30)
        future_question=Question(pub_date=time)
        self.assertIs(future_question.was_recently_published(),False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_recently_published(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_recently_published(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        create_question(question_text="future question", days=30)
        response=self.client.get(reverse("polls:index"))
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question_and_past_question(self):
        """
        even if past and future exist at same time ,only past question displayed
        :return:
        """

        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],
                                 ["<Question: Past question.>"]
                                 )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        should return a 404
        :return:
        """
        future_question=create_question("future question", 30)
        response=self.client.get(reverse("polls:detail", args=(future_question.id, )))
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        past_question=create_question("past question", -10)
        response=self.client.get(reverse("polls:detail", args=(past_question.id, )))
        self.assertContains(response,past_question.question_text)
