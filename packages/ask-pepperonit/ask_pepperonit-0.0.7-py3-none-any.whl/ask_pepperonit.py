# coding=utf-8

""" Pepper module utilizing Google and Wikipedia API
"""

import wikipedia
import search_google.api

class Ask:
    
    def __init__(self, g_api, g_cx):
         self.g_api = g_api
         self.g_cx = g_cx

    def ask_wikipedia_api(self, question):
        """
        End half of ask_wikipedia, it calls the helper function get_info_wikipedia
        question: the string input to wiki api
        wiki_lang: the language for wikipedia to search in, e.g. "sv"
        """
        summary, image = self.get_info_wikipedia(question)
        return summary, image
        
        
    def get_info_wikipedia(self, term):
        """
        term: A string as input into a wikipedia search
        """
        # wikipedia.set_lang("sv")
        summary = wikipedia.summary(term, sentences=2)
        try:
            page = wikipedia.page(term)
            image = page.images[0] 
            print("[INFO]: wiki image: " + image)# pylint: disable=superfluous-parens
            return summary, image

        except IndexError as error:
            print(error)# pylint: disable=superfluous-parens

        return (summary, 
        "https://upload.wikimedia.org/wikipedia/commons/6/61/Wikipedia-logo-transparent.png")
        
    def ask_google_api(self, question):
            """
            End half of ask_google, it calls the helper function get_info_google
            question: string input to google api
            """
            picture = self.get_info_google(question)
            return picture
        
    def get_info_google(self, term):
        """
        Helper function that calls Google's API with custom CE and settings
        term: A string as input into a google search engine
        """
        # Define buildargs for api api
        buildargs = {
            "serviceName": "customsearch",
            "version": "v1",
            "developerKey": self.g_api
        }
        # Define cseargs for search
        cseargs = {
            "q": term + ";jpg/png",
            "cx": self.g_cx,
            "num": 1,
            "searchType": "image"
        }
        results = search_google.api.results(buildargs, cseargs)
        links = results.get_values('items', 'link')
        links = results.links
        links = str(links[0])
        print("[INFO]: google_link: " + links)# pylint: disable=superfluous-parens
        return links# pylint: disable=inconsistent-return-statements

    def wikipedia_set_lang(self, lang):
        """
        Helper function to change Wikipedia language
        lang: Wikipedia language, e.g. "sv" for Swedish
        """
        wikipedia.set_lang(lang)
        return
