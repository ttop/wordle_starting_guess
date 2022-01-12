import re
import math


def load_words():
    # from https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/
    file_to_open = 'common_3000.txt'
    with open(file_to_open) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def score_word(word, usage_freq, position_freq, params):
    # Score word using the provided dictionary usage_freq. The first
    # time a letter appears, it is worth the number of points equal to
    # its frequency. There is an additional score based on how common
    # that letter is in that position in the word.

    seen = {}
    word_score = 0

    for position in range(0, 5):
        letter = word[position]
        letter_score = 0

        # If first time seen, add the letter frequency to the score
        if letter not in seen:
            letter_score = usage_freq[letter]
            seen[letter] = 1

        letter_score = (letter_score +
                          (position_freq[position][letter] *
                               params['position_mult']))

        word_score = word_score + letter_score

    return word_score


def score_two_words(word1, word2, usage_freq, position_freq, params):
    # Score two words using the provided dictionary usage_freq. In the
    # second word, a letter is worth nothing if it matches the first
    # word, but follows the same rules as the single-word scoring
    # otherwise. Also, consider reducing the value of the second word
    # a bit, since you may not use it if the first is very useful.

    seen = {}
    words_score = 0

    # Start by scoring the first word as usual
    for position in range(0, 5):
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
    for position in range(0, 5):
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
    for position in range(0, 5):
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
    for position in range(0, 5):
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
    for position in range(0, 5):
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
    eligible_words = []
    for word in wordlist:
        include = True
        if len(word) != 5:
            continue

        if re.match('[^a-zA-Z]', word):
            # In case the provided wordlist contains any non-letter characters
            continue

        eligible_words.append(word.lower())
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
    for position in range(0, 5):
        position_count[position] = {}
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            position_count[position][letter] = 0

    for word in wordlist:
        for position in range(0, 5):
            letter = word[position]
            position_count[position][letter] = (
                position_count[position][letter] + 1)

    return position_count


if __name__ == '__main__':
    eligible_words = get_five_letter_words(load_words())
    usage_frequency = get_usage_frequency(eligible_words)
    position_frequency = get_position_frequency(eligible_words)

    # Set parameters for relative weighting of different factors:
    # The multiplier for letter position frequency, the factor to
    # divide by for repeated letters, and the reduction in value
    # of later words.
    params = {'position_mult' : 1.5, 'second_word' : 0.5, 'third_word' : 0.2}
    
    # Score all the words
    word_scores = {}
    for word in eligible_words:
        word_scores[word] = score_word(
            word, usage_frequency, position_frequency, params)

    # Display the top ranking words
    scored_rank = sorted(word_scores, key=word_scores.get, reverse=True)
    max_to_display = 30

    for idx in range(max_to_display):
        word = scored_rank[idx]
        print(word.upper() + ": " + str(int(word_scores[word])))
        
    print

    # Consider followup words for the top first words
    two_word_scores = {}
    first_words_to_consider = 50
    for idx in range(first_words_to_consider):
        word1 = scored_rank[idx]
        for word2 in eligible_words:
            two_word_scores[word1 + " " + word2] = score_two_words(
                word1, word2,
                usage_frequency, position_frequency, params)

    scored_rank_pairs = sorted(
        two_word_scores, key=two_word_scores.get, reverse=True)
    max_to_display = 20
    for idx in range(max_to_display):
        words = scored_rank_pairs[idx]
        print(words.upper() + ": " + str(int(two_word_scores[words])))

    print
    
    # Consider followup words for the top first pairs
    three_word_scores = {}
    first_pairs_to_consider = 80
    for idx in range(first_pairs_to_consider):
        pair = scored_rank_pairs[idx]
        [word1, word2] = pair.split()
        for word3 in eligible_words:
            three_word_scores[pair + " " + word3] = score_three_words(
                word1, word2, word3,
                usage_frequency, position_frequency, params)

    scored_rank_threes = sorted(
        three_word_scores, key=three_word_scores.get, reverse=True)
    max_to_display = 20
    for idx in range(max_to_display):
        words = scored_rank_threes[idx]
        print(words.upper() + ": " + str(int(three_word_scores[words])))
    
