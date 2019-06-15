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

bot = ChatBot('Lenest',logic_adapters=[
               {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.SynsetDistance",
            "default_response": "I am sorry, but I do not understand.Please enter your question again or email us at - for further queries",
            "response_selection_method":get_first_response,
            "maximum_similarity_threshold": 0.65  }]
            ,response_selection_method=get_first_response
            )







#bot = ChatBot('Lenest',logic_adapters=[
#               {
#            "import_path": "chatterbot.logic.BestMatch",
#            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
#            "response_selection_method":get_most_frequent_response      }] )
#,"statement_comparison_function":chatterbot.comparisons.levenshtein_distance,"response_selection_method":chatterbot.response_selection.get_most_frequent_response
#
# "chatterbot.logic.BestMatch"
#response_selection_method=get_most_frequent_respons

conv = open('faq.txt', 'r').readlines()

trainer = ListTrainer(bot)
trainer.train(conv)
#trainer.train(conv)
#trainer1 = UbuntuCorpusTrainer(bot)
#trainer1.train()
trainer1 = ChatterBotCorpusTrainer(bot)
trainer1.train('chatterbot.corpus.english.greetings')
#bot.set_trainer(ListTrainer)
#bot.train(conv)
#get_stopwords("pregnancy")

#def get_stopwords(self):
#        """
#        Get the list of stopwords from the NLTK corpus.
#        """
#        if self.stopwords is None:
#            self.stopwords = stopwords.words(self.language.ENGLISH_NAME.lower())
#            stopwords.append('pregnancy')

#        return self.stopwords

while True:
	request = input('You: ')
	response = bot.get_response(request)
	print('Bot : ',response)
