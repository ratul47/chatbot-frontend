# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from os import link
from typing import Any, Text, Dict, List
from urllib import response

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
import requests
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionSetTwoWay(Action):
    def name(self):
        return "action_set_twoway"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")

        if intent == "yes":
            return [SlotSet("two_way", True)]
        elif intent == "no":
            return [SlotSet("two_way", False)]
        return []

class ValidateInfoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_info_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        additional_slots = []
        if tracker.slots.get("is_two_way") is True:
            additional_slots.append("return_date")

        return additional_slots + domain_slots

class FlightSeachAction(Action):
    def name(self):
        return "action_get_flight"

    def run(self, dispatcher, tracker, domain):
        dep= tracker.get_slot('departure_place')
        des = tracker.get_slot('destination_place')
        arrdate = tracker.get_slot('arrival_date')
        retdate = tracker.get_slot('return_date')
        is_two_way= tracker.get_slot('is_two_way')
        no_of_ad=tracker.get_slot('no_of_adult')
        no_of_chd=tracker.get_slot('no_of_child')
        no_of_inf=tracker.get_slot('no_of_infant')
        print(str(dep)+" "+str(des)+" "+str(arrdate)+" "+str(retdate)+" "+str(is_two_way)+" "+str(no_of_ad)+" "+str(no_of_chd)+" "+str(no_of_inf))
        d={'dhaka':'dac','jessore':'jsr'}
        air_dict = {'dhaka': 'DAC',
                        'barishal': 'BZL',
                        'chattogram': 'CGP',
                        'coxsbazar': 'CXB',
                        'jashore': 'JSR',
                        'jessore':'JSR',
                        'rajshahi': 'RJH',
                        'saidpur': 'SPD',
                        'sylhet': 'ZYL',
                        'singapore': 'SIN',
                        'muscat': 'MCT',
                        'kolkata': 'CCU',
                        'chennai': 'MAA',
                        'kualalumpur': 'KUL',
                        'bangkok': 'BKK',
                        'doha': 'DOH',
                        'guangzhou': 'CAN',
                        'dubai': 'DXB',
                        'sharjah': 'SHJ',
                        'male': 'MLE'}
        # dispatcher.utter_message("Here is the link to your flight booking")
        print(str(dep)+" "+str(des)+" "+str(arrdate)+" "+str(retdate)+" "+str(is_two_way)+" "+str(no_of_ad)+" "+str(no_of_chd)+" "+str(no_of_inf))
        s=arrdate.split('/')
        arr_d= s[2]+'-'+s[1]+'-'+s[0]
        if retdate is not None:
            t= retdate.split('-')
            ret_d = t[2]+'-'+t[1]+'-'+t[0]
        else:
            ret_d=''
        print(air_dict[dep])
        print(air_dict[des])
        urls =("https://fo-asia.ttinteractive.com/Zenith/FrontOffice/usbangla/en-GB/BookingEngine/" +
        "SearchResult?OriginAirportCode="+ air_dict[dep]+
        "&DestinationAirportCode=" +air_dict[des]+
        "&OutboundDate=" +arr_d+
        "&InboundDate="+ret_d+
        "&TravelerTypes%5B0%5D."+
        "Key=AD&TravelerTypes%5B0%5D.Value="+ no_of_ad +"&TravelerTypes%5B1%5D."
        "Key=CHD&TravelerTypes%5B1%5D.Value="+no_of_chd+
        "&TravelerTypes%5B2%5D.Key=INF&TravelerTypes%5B2%5D.Value="+no_of_inf +
        "&Currency=BDT&DiscountCode=")
        hypLink = '<a href="%s">Details</a>' % (urls)
        dispatcher.utter_message(response="utter_link",link=urls)
        return []