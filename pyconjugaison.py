
"""
"""
from docopt import docopt
import sys
import random
import json
import time
from termcolor import colored

class ConjugaisonTeacher:
    def __init__(self):
        self.consecutives_corrects = 0;
        self.question_template = colored("Q: ", "blue") + "Answ: {} - {} - {}:"
        self.conjugaisons = self.load_conjugaisons()
        self.wrong_attemps = []

    def run(self, minutes):
        timeout = time.time() + 60*minutes
        while time.time() < timeout:
            exercise = self.get_random_exercise()
            attempt = self.get_and_check_answer(**exercise)
            if attempt:
                print(colored("SUPER!", "green"))

    def get_random_exercise(self):
        if self.wrong_attemps and self.consecutives_corrects > 1:
            return self.wrong_attemps.pop(0)
        verbs = [x for x in self.conjugaisons]
        random_verb = random.choice(verbs)
        pronoms = [x for x in self.conjugaisons[random_verb]['conjugaison']]
        pronom = random.choice(pronoms)
        return dict(
            temp=self.conjugaisons[random_verb]["temp"],
            verbe=random_verb,
            pronom=pronom,
            answer=self.conjugaisons[random_verb]['conjugaison'][pronom]
        )

    def load_conjugaisons(self):
        json_path = "./resources/conjugaison.json"
        try:
            data = json.load(open(json_path))
            return data
        except FileNotFoundError:
            print("Your conjugaison config file {} not found, "
                  "make sure its there, "
                  "check the git repo for an example".format(json_path))
        exit(2)

    def question_str(self, **kwargs):
        return self.question_template.format(
            kwargs.get("temp"), kwargs.get("verbe"), kwargs.get("pronom"))

    def get_and_check_answer(self, **kwargs):
        answer = input(self.question_str(**kwargs)+" ")
        right_answer = self.conjugaisons[kwargs.get("verbe")]["conjugaison"][kwargs.get("pronom")]
        correct = answer == right_answer
        if not correct:
            print(colored("Faux", "red") + "\nCorret: {}".format(right_answer))
            self.wrong_attemps.append(kwargs)
            self.consecutives_corrects = 0
        else:
            self.consecutives_corrects += 1
        return correct

    def test(self):
        question_args = dict(
            temp="presenté",
            verbe="avoir",
            pronom="elle"
        )

        # question
        assert self.get_and_check_answer(**question_args)
        self.run(5)


if __name__ == "__main__":
    ct = ConjugaisonTeacher()
    ct.run(5)


