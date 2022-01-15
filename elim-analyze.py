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


# Decide if this word matches known conditions
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


# Find conditions on answers given list of guesses and answer
def eval_words(guesses, answer):
    exact_re = ""
    exact_positions = {} # Dict of known letters: e.g. {2:r, 4:c}
    exact_letters = set() # Set of exactly known letters: e.g. {c, r}
    include_letters = set() # Letters that must be included at unknown position
    mixed_letters = [set(), set(), set(), set(), set()] # Wrong @ each position
    absent_letters = set() # Don't appear in the answer at all

    for guess in guesses:
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


# Score list of words based on how much on average they reduce the space of
# available answers.
def score_words(guesses, eligible_answers):
    # Max value of this result is len(eligible_answers)^2
    matches = 0

    # Loop over all eligible answers and "score" the guess
    for answer in eligible_answers:
        exact_positions, include_letters, mixed_letters, absent_letters = \
          eval_words(guesses, answer)

        # Add num of eligible answers that ALSO match this guess
        matches += sum(1 for word in eligible_answers if \
          word_match(word, exact_positions, include_letters,
                         mixed_letters, absent_letters))

    return matches


def get_five_letter_words(wordlist):
    eligible_words = set()
    for word in wordlist:
        if len(word) != 5:
            continue

        if not word.isalpha():
            # In case the provided wordlist contains any non-letter characters
            continue

        eligible_words.add(word.lower())
    print(str(len(eligible_words)) + ' five-letter words')
    return eligible_words


if __name__ == '__main__':
    # If we provided our first word
    my_word1 = ""
    if len(sys.argv) > 1 and len(sys.argv[1]) == 5 and sys.argv[1].isalpha():
        my_word1 = sys.argv[1].lower()

    # If we provided our second word
    my_word2 = ""
    if len(sys.argv) > 2 and len(sys.argv[2]) == 5 and sys.argv[2].isalpha():
        my_word2 = sys.argv[2].lower()

    # Load word lists and frequencies
    eligible_answers = get_five_letter_words(load_words(''))
    eligible_guesses = get_five_letter_words(load_words(''))
    score_scale = 1./(len(eligible_answers))**2

    # Score all the words, or if the first was given, score just it
    word_scores = {}
    if not my_word1:
        count = 0
        best = ""
        best_score = 1
        for word in eligible_guesses:
            count += 1
            word_scores[word] = \
              score_words([word], eligible_answers) * score_scale
            if word_scores[word] < best_score:
                best = word
                best_score = word_scores[word]
            # Print an interesting progress message, since this is slow
            if count % 5 == 0:
                #print(str(count) + "/" + str(len(eligible_guesses)))
                sys.stdout.write("\r" + '{:>3}'.format(count) + "/" + \
                  str(len(eligible_guesses)) + " (" + \
                  '{:>3.0%}'.format(float(count)/len(eligible_guesses)) + \
                  "): " + word + \
                  ": " + '{:>6.2%}'.format(word_scores[word]) + \
                  " [Best: " + best + ": " + \
                  '{:>6.2%}'.format(best_score) + "]")
                sys.stdout.flush()
    else:
        word_scores[my_word1] = \
          score_words([my_word1], eligible_answers) * score_scale

    sys.stdout.write("\r" + " "*50)
    sys.stdout.flush()
    print
    
    # Display the top ranking words
    scored_rank = sorted(word_scores, key=word_scores.get)
    max_to_display = min(30,len(word_scores))
    for idx in range(max_to_display):
        word = scored_rank[idx]
        print(word.upper() + ": " + '{:>6.2%}'.format(word_scores[word]))

    # Show the worst words, too, out of curiosity
    if len(word_scores) > max_to_display+5:
        print "..."
        for idx in range(-5,0):
            word = scored_rank[idx]
            print(word.upper() + ": " + '{:>6.2%}'.format(word_scores[word]))

    print

    # Now consider second words
    two_word_scores = {}
    if my_word2:
        two_word_scores[my_word1 + " " + my_word2] = \
          score_words([my_word1, my_word2], eligible_answers) * score_scale

    # Display the top ranking words
    scored_rank_pairs = sorted(two_word_scores, key=two_word_scores.get)
    max_to_display = min(30,len(two_word_scores))
    for idx in range(max_to_display):
        words = scored_rank_pairs[idx]
        word_list = words.split()
        print(words.upper() + ": " + \
          '{:>7.3%}'.format(two_word_scores[words]) + " = " \
          '{:>6.2%}'.format(word_scores[word_list[0]]) + " * " \
          '{:>6.2%}'.format(two_word_scores[words]/word_scores[word_list[0]]))

    # Show the worst words, too, out of curiosity
    if len(two_word_scores) > max_to_display+5:
        for idx in range(-5,0):
            word = scored_rank[idx]
            print(word.upper() + ": " + '{:>6.2%}'.format(word_scores[word]))


