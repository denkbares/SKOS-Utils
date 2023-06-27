import re
from string import punctuation
from rdflib import URIRef

from SKOSTools.TSAConverter.SKOSUtils.IDGenerator import IDGenerator
from SKOSTools.examples_tobe_removed.ProcessUtils import ProcessUtils


class SKOSConcept:
    def __init__(self, name='Noname', note=None, namespace=None, uuid=None, uuid_prefix='C_'):
        self.nc = namespace
        self.name = ProcessUtils.trim(name)

        if not uuid:
            generator = IDGenerator()
            uuid = uuid_prefix + generator.generate_uuid()

        uriname = uuid

        if self.nc:
            self.uri = URIRef(namespace + uriname)
        else:
            self.uri = uriname
        self.props = []
        self.broader = []
        self.narrower = []
        self.notes = []
        self.hiddenName = None
        self.add_notes(note)
        self.add_note('xmind_name', self.name)
        self.uuid = uuid

    def add_broader(self, concept=None):
        if concept and concept not in self.broader:
            self.broader.append(concept)

    def add_narrower(self, concept=None):
        if concept and concept not in self.narrower:
            self.narrower.append(concept)

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

    def add_note(self, note_attr='', note_value=None):
        if note_attr:
            if note_value:
                if note_value.startswith('"'):
                    note_value = note_value[1:]
                if note_value.endswith('"'):
                    note_value = note_value[:-1]
                if note_attr != 'order':
                    note_value = '"' + note_value + '"'
                self.notes.append('@' + note_attr + ': ' + note_value)
            else:
                self.notes.append(note_attr)

    def add_notes(self, note):
        if note and isinstance(note, list):
            for n in note:
                self.check_and_add_note(n)
        elif note:
            self.check_and_add_note(note)

    def check_and_add_note(self, n):
        if n.startswith('@done'):
            pass
        elif n.startswith('@phrase:'):
            regex = r"@phrase:\s*\"?([^\"]+)\"?\s*"
            value = '"' + re.sub(regex, "\\1", n, 0, re.MULTILINE) + '"'
            self.add_note('phrase', value)
        elif n.startswith('@'):
            i = n.find(' ')
            attr = n[1:i]
            value = n[i+1:]
            self.add_property(attr, value)
        else:
            self.add_note(n)

    def add_property(self, attr, value):
        if attr.endswith(':'):
            attr = attr[:-1]
        self.props.append((attr, value))



