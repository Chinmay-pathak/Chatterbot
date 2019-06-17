import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from django.conf import settings
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot.ext.django_chatterbot import settings

from chatterbot import ChatBot
from chatterbot.response_selection import get_most_frequent_response
#from .logic_adapter import logic_adapter
from chatterbot import utils
from chatterbot.response_selection import get_first_response
from chatterbot.comparisons import SynsetDistance

class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot('Lenest',logic_adapters=[
               {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.SynsetDistance",
            "default_response": "I am sorry, but I do not understand.Please enter your question again or email us at - for further queries",
            "response_selection_method":get_first_response,
            "maximum_similarity_threshold": 0.65  }]
            )
    conv = open('faq.txt', 'r').readlines()

    trainer = ListTrainer(chatterbot)
    trainer.train(conv)
    conv1 = open('general_questions.txt', 'r').readlines()

    trainer2 = ListTrainer(chatterbot)
    trainer2.train(conv1)
    trainer1 = ChatterBotCorpusTrainer(chatterbot)
    trainer1.train('chatterbot.corpus.english.greetings')



    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })
