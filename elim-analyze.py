import re
import sys

def load_words(file):
    # from https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/
    #file_to_open = 'common_3000.txt'
    if file:
        file_to_open = file
    else:
        # from https://www.wordfrequency.info/samples.asp, deduplicated
        file_to_open = 'lemmas-5000-sort.csv'

    with open(file_to_open) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


# Decide if this word matches known regular expression and list of letters
def word_match(word, \
      exact_positions, include_letters, mixed_letters, absent_letters):
    #print word + " : " + exact_re + " : " + str(include_letters)

    for pos in exact_positions:
        if word[pos] != exact_positions[pos]:
            return False

    for pos in range(5):
        if word[pos] in mixed_letters[pos]:
            return False

    for letter in absent_letters:
        if letter in word:
            return False

    for letter in include_letters:
        if not letter in word:
            return False
        
    #print "+++ " + word + " : " + exact_re + " : " + str(include_letters)
    return True


# Find regular expression and included letters given guess and answer
def eval_word(guess, answer):
    exact_re = ""
    exact_positions = {} # Dict of known letters: e.g. {2:r, 4:c}
    exact_letters = set() # Set of exactly known letters: e.g. {c, r}
    include_letters = set() # Letters that must be included at unknown position
    mixed_letters = [set(), set(), set(), set(), set()] # Wrong @ each position
    absent_letters = set() # Don't appear in the answer at all

    for position in range(5):
        if guess[position] == answer[position]:
            exact_positions[position] = guess[position]
            exact_letters.add(guess[position])
        elif guess[position] in answer:
            mixed_letters[position].add(guess[position])
            include_letters.add(guess[position])
        else:
            absent_letters.add(guess[position])

    for letter in exact_letters:
        include_letters.discard(letter)

    return [exact_positions, include_letters, mixed_letters, absent_letters]


def score_word(guess, eligible_answers):
    # Score word based on how much on average it reduces the space of available
    # answers.

    # Max value of this variable is len(eligible_answers)^2
    matches = 0

    # Loop over all eligible answers and "score" the guess
    for answer in eligible_answers:
        exact_positions, include_letters, mixed_letters, absent_letters = \
          eval_word(guess, answer)

        # Add num of eligible answers that ALSO match this guess
        matches += sum(1 for word in eligible_answers if \
          word_match(word, exact_positions, include_letters,
                         mixed_letters, absent_letters))

    return matches


def score_two_words(word1, word2, usage_freq, position_freq, params):
    # Score two words using the provided dictionary usage_freq. In the
    # second word, a letter is worth nothing if it matches the first
    # word, but follows the same rules as the single-word scoring
    # otherwise. Also, consider reducing the value of the second word
    # a bit, since you may not use it if the first is very useful.

    seen = {}
    words_score = 0

    # Start by scoring the first word as usual
    for position in range(5):
        letter = word1[position]
        letter_score = 0

        # If first time seen, add the letter frequency to the score
        if letter not in seen:
            letter_score = usage_freq[letter]
            seen[letter] = 1

        letter_score = (letter_score +
                          (position_freq[position][letter] *
                               params['position_mult']))

        words_score = words_score + letter_score

    # Next, score the second word in the context of the first
    for position in range(5):
        letter = word2[position]
        letter_score = 0

        # A letter in the same position as before contributes nothing
        if letter == word1[position]:
            continue
        
        # If first time seen, add the letter frequency to the score
        if letter not in seen:
            letter_score = usage_freq[letter]
            seen[letter] = 1

        letter_score = (letter_score +
                          (position_freq[position][letter] *
                               params['position_mult']))

        words_score = words_score + letter_score * params['second_word']
        
    return words_score


def score_three_words(word1, word2, word3, usage_freq, position_freq, params):
    # Score two words using the provided dictionary usage_freq. In the
    # second word, a letter is worth nothing if it matches the first
    # word, but follows the same rules as the single-word scoring
    # otherwise. Also, consider reducing the value of the second word
    # a bit, since you may not use it if the first is very useful.
    # (The third counts even less.)

    seen = {}
    words_score = 0

    # Start by scoring the first word as usual
    for position in range(5):
        letter = word1[position]
        letter_score = 0

        # If first time seen, add the letter frequency to the score
        if letter not in seen:
            letter_score = usage_freq[letter]
            seen[letter] = 1

        letter_score = (letter_score +
                          (position_freq[position][letter] *
                               params['position_mult']))

        words_score = words_score + letter_score

    # Next, score the second word in the context of the first
    for position in range(5):
        letter = word2[position]
        letter_score = 0

        # A letter in the same position as before contributes nothing
        if letter == word1[position]:
            continue
        
        # If first time seen, add the letter frequency to the score
        if letter not in seen:
            letter_score = usage_freq[letter]
            seen[letter] = 1

        letter_score = (letter_score +
                          (position_freq[position][letter] *
                               params['position_mult']))

        words_score = words_score + letter_score * params['second_word']
        
    # Next, score the third word
    for position in range(5):
        letter = word3[position]
        letter_score = 0

        # A letter in the same position as before contributes nothing
        if letter == word1[position] or letter==word2[position]:
            continue
        
       # If first time seen, add the letter frequency to the score
        if letter not in seen:
            letter_score = usage_freq[letter]
            seen[letter] = 1

        letter_score = (letter_score +
                          (position_freq[position][letter] *
                               params['position_mult']))

        words_score = words_score + letter_score * params['third_word']
        
    return words_score


def print_frequency_count(letter_count):
    print('Frequency count:\n')
    for letter in sorted(letter_count, key=letter_count.get, reverse=True):
        print(letter + ': ' + str(letter_count[letter]))


def get_five_letter_words(wordlist):
    eligible_words = set()
    for word in wordlist:
        include = True
        if len(word) != 5:
            continue

        if re.match('[^a-zA-Z]', word):
            # In case the provided wordlist contains any non-letter characters
            continue

        eligible_words.add(word.lower())
    print(str(len(eligible_words)) + ' five-letter words')
    return eligible_words


def get_usage_frequency(wordlist):
    frequency_count = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        frequency_count[letter] = 0

    for word in wordlist:
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            if letter in word:
                frequency_count[letter] = frequency_count[letter] + 1
                
    return frequency_count


def get_position_frequency(wordlist):
    # for each letter position, 0-4, determine how often the letter is
    # in that position
    position_count = {}
    for position in range(5):
        position_count[position] = {}
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            position_count[position][letter] = 0

    for word in wordlist:
        for position in range(5):
            letter = word[position]
            position_count[position][letter] = (
                position_count[position][letter] + 1)

    return position_count


if __name__ == '__main__':
    # Set parameters for relative weighting of different factors:
    # The multiplier for letter position frequency, the factor to
    # divide by for repeated letters, and the reduction in value
    # of later words.
    params = {'position_mult' : 1.5, 'second_word' : 0.5, 'third_word' : 0.2}

    # If we provided our first word
    my_word1 = ""
    if len(sys.argv) > 1 and len(sys.argv[1]) == 5:
        my_word1 = sys.argv[1].lower()

    # Load word lists and frequencies
    eligible_answers = get_five_letter_words(load_words(''))
    eligible_guesses = get_five_letter_words(load_words(''))
    score_scale = 1./(len(eligible_answers))**2
    usage_frequency = get_usage_frequency(eligible_answers)
    position_frequency = get_position_frequency(eligible_answers)

    # Score all the words, or if the first was given, score just it
    word_scores = {}
    if not my_word1:
        count = 0
        for word in eligible_guesses:
            count += 1
            word_scores[word] = \
              score_word(word, eligible_answers) * score_scale
            if count % 5 == 0:
                #print(str(count) + "/" + str(len(eligible_guesses)))
                sys.stdout.write("\r" + '{:>3}'.format(count) + "/" + \
                  str(len(eligible_guesses)) + " : " + word + \
                  ": " + '{:>6.2%}'.format(word_scores[word]))
                sys.stdout.flush()
    else:
        word_scores[my_word1] = \
          score_word(my_word1, eligible_answers) * score_scale

    print
    
    # Display the top ranking words
    scored_rank = sorted(word_scores, key=word_scores.get)
    max_to_display = min(30,len(word_scores))

    for idx in range(max_to_display):
        word = scored_rank[idx]
        print(word.upper() + ": " + '{:>6.2%}'.format(word_scores[word]))
        
