from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, guess, hit=None, miss=None):
        self.hit = hit
        self.miss = miss
        self.guess = guess
        if self.hit and self.miss:
            raise InvalidGuessAttempt
        if self.hit == False and self.miss == False:
            raise InvalidGuessAttempt      
    def is_miss(self):
        if self.miss == True:
            return True
        else:
            return False
    def is_hit(self):
        if self.hit == True:
            return True
        else:
            return False
class GuessWord(object):
    def __init__(self, guessword):
        self.answer = guessword.lower()
        self.masked = self._mask_word(guessword)
        
    def perform_attempt(self, guess): 
        if len(guess) > 1:
            raise InvalidGuessedLetterException
        if guess.lower()  not in self.answer:
            return GuessAttempt(guess, miss=True)
        new_word = ''
        for answer_char, masked_char in zip(self.answer, self.masked):
            if guess.lower() == answer_char:
                new_word += answer_char
            else:
                new_word += masked_char
        self.masked = new_word
        return GuessAttempt(guess, hit=True)
            
 


    @classmethod
    def _mask_word(cls, word):
        if word == "":
            raise InvalidWordException
        return '*' * len(word)
    
class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self, list_of_words=None, number_of_guesses=5):
        if not list_of_words:
            list_of_words = self.WORD_LIST
            
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(list_of_words))
        
    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException()
        return random.choice(list_of_words)
    
    def is_won(self): # bool to check if game is won
        return self.word.masked == self.word.answer
    def is_lost(self): # bool to check if game is lost
        return self.remaining_misses == 0
    def is_finished(self): # bool to check if game is finished
        return self.is_won() or self.is_lost()
    
    def guess(self, guess_char): #returns an instance of GuessAttempt
        guess_char = guess_char.lower()
        if guess_char in self.previous_guesses:
            raise InvalidGuessedLetterException()
        if self.is_finished():
            raise GameFinishedException()
        self.previous_guesses.append(guess_char)
        
        attempt = self.word.perform_attempt(guess_char)
        if attempt.is_miss():
            self.remaining_misses -= 1
        
        if self.is_won():
            raise GameWonException()
        if self.is_lost():
            raise GameLostException()
        return attempt
        
        
    


