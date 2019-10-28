import re
from requests          import Session
from typing            import Any, Text, Dict, List
from rasa_sdk          import Action, Tracker
from rasa_sdk.events   import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class ActionGetWikiData(Action):
	def name(self) -> Text:
		return "action_get_wiki_data"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		session = Session()

		try:
			search = tracker.get_slot("objeto_pesquisa")

			p = {
				"action": "query",
				"format": "json",
				"list": "search",
				"srsearch": search,
			}

			req  = session.get(url = 'https://pt.wikipedia.org/w/api.php', params = p)
			data = req.json()

			if data["query"]["search"][0]["title"] != "":
				raw = re.sub(re.compile("<.*?>"), "", data["query"]["search"][0]["snippet"]) 
				dispatcher.utter_message(raw)
			else:
				dispatcher.utter_message("Não deu")
		except Exception as err:
			print (err)
      
		return []