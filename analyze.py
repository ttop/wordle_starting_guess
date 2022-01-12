import re
import math


def load_words():
    # from https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/
    file_to_open = 'common_3000.txt'
    with open(file_to_open) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def score_word(word, usage_freq, position_freq):
    # Score word using the provided dictionary usage_freq where the letter is
    # worth the number of points corresponding to its frequency, plus a bonus
    # based on how common that letter is in that position in the word,
    # but each additional time that letter is used in the word, its points are
    # reduced.

    seen = {}
    word_score = 0

    for position in range(0, 5):
        letter = word[position]
        letter_score = (usage_freq[letter] +
                        (position_freq[position][letter] * 3))

        if letter in seen:
            reduction_factor = seen[letter] * 4
            letter_score = math.floor(letter_score / reduction_factor)
            seen[letter] = seen[letter] + 1
        else:
            seen[letter] = 1

        word_score = word_score + letter_score
    return word_score


def score_two_words(word1, word2, usage_freq, position_freq):
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
        letter_score = (usage_freq[letter] +
                        (position_freq[position][letter] * 3))

        if letter in seen:
            reduction_factor = seen[letter] * 4
            letter_score = math.floor(letter_score / reduction_factor)
            seen[letter] = seen[letter] + 1
        else:
            seen[letter] = 1

        words_score = words_score + letter_score

    # Next, score the second word in the context of the first
    second_word_reduce = 0.5
    for position in range(0, 5):
        letter = word2[position]

        # A letter in the same position as before contributes nothing
        if letter == word1[position]:
            continue
        
        letter_score = (usage_freq[letter] +
                        (position_freq[position][letter] * 3))

        if letter in seen:
            reduction_factor = seen[letter] * 4
            letter_score = math.floor(letter_score / reduction_factor)
            seen[letter] = seen[letter] + 1
        else:
            seen[letter] = 1

        words_score = (words_score +
                           math.floor(letter_score * second_word_reduce))
        
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
        for letter in word:
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

    # Score all the words
    word_scores = {}
    for word in eligible_words:
        word_scores[word] = score_word(
            word, usage_frequency, position_frequency)

    # Display the top ranking words
    scored_rank = sorted(word_scores, key=word_scores.get, reverse=True)
    max_to_display = 30

    for idx in range(max_to_display):
        word = scored_rank[idx]
        print(word.upper() + ": " + str(word_scores[word]))

    print

    # Consider followup words for the top first words
    two_word_scores = {}
    first_words_to_consider = 30
    for idx in range(first_words_to_consider):
        word1 = scored_rank[idx]
        for word2 in eligible_words:
            two_word_scores[word1 + " " + word2] = score_two_words(
                word1, word2, usage_frequency, position_frequency)

    scored_rank = sorted(two_word_scores, key=two_word_scores.get, reverse=True)
    max_to_display = 30
    count = 0
    for idx in range(max_to_display):
        words = scored_rank[idx]
        print(words.upper() + ": " + str(two_word_scores[words]))

