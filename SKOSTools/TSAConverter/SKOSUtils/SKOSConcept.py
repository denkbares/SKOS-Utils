from string import punctuation
from rdflib import URIRef


class SKOSConcept:
    def __init__(self, name='Noname', note=None, uri_pre='', uri_post='', namespace=None):
        self.nc = namespace
        self.name = name
        uriname = self.urify(str(uri_pre) + name + str(uri_post))
        if self.nc:
            self.uri = URIRef(namespace + uriname)
        else:
            self.uri = uriname
        self.broader = []
        self.narrower = []
        self.notes = []
        self.hiddenName = None
        if note and isinstance(note, list):
            self.notes = note
        elif note:
            self.notes.append(note)

    def add_broader(self, concept=None):
        if concept and concept not in self.broader:
            self.broader.append(concept)

    def add_narrower(self, concept=None):
        if concept and concept not in self.narrower:
            self.narrower.append(concept)

    def add_note(self, note=''):
        if note:
            self.notes.append(note)

    @staticmethod
    def urify(string):
        """Method written by Benno"""
        # the valid charcaters
        validcharacters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                           "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                           "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5",
                           "6", "7", "8", "9", "0", " "]
        # delete the umlauts
        string = string.replace('ä', 'ae').replace('ß', 'ss').replace('Ö', 'Oe')\
            .replace('ö', 'oe').replace('Ü', 'Ue').replace('ü', 'ue').replace('Ä', 'Ae')
        # delete the characters that are not valid
        for i in range(len(string)):
            if string[i] in validcharacters:
                i += 1
            else:
                string = string.replace(string[i], " ")
                i += 1
        # CamlCase the string
        new_string = ""
        for x in string.split():
            new_string += x.capitalize()
        return new_string

