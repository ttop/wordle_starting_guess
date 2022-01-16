import sys

def load_words(file):
    if file:
        file_to_open = file
    else:
        # from https://www.wordfrequency.info/samples.asp, deduplicated
        file_to_open = 'lemmas-5000-sort.csv'

    with open(file_to_open) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


# Decide if this word matches known conditions
# This isn't actually used anymore, but I'm keeping it in case I find a use
def word_match(word, \
      exact_positions, include_letters, wrong_letters, absent_letters):

    for letter in include_letters:
        if not letter in word:
            return False

    for letter in absent_letters:
        if letter in word:
            return False

    for pos in exact_positions:
        if word[pos] != exact_positions[pos]:
            return False

    for pos in range(5):
        if word[pos] in wrong_letters[pos]:
            return False

    return True


# Find conditions on answers given list of guesses and answer
def eval_words(guesses, answer):
    exact_letters = set() # Set of exactly known letters: e.g. {c, r}
    exact_positions = {} # Dict of known letters: e.g. {2:r, 4:c}
    include_letters = set() # Letters included at any position
    wrong_letters = [set(), set(), set(), set(), set()] # Wrong @ each position
    absent_letters = set() # Don't appear in the answer at all
    result = "" # Unique code for these conditions
    
    for guess in guesses:
        for position in range(5):
            if guess[position] == answer[position]:
                exact_positions[position] = guess[position]
                include_letters.add(guess[position]) # Faster!
                exact_letters.add(guess[position])
            elif guess[position] in answer:
                wrong_letters[position].add(guess[position])
                include_letters.add(guess[position])
            else:
                absent_letters.add(guess[position])

    #for letter in exact_letters:
    #    include_letters'].discard(letter)

    for position in exact_positions:
        wrong_letters[position] = set()

    for position in range(5):
        for letter in absent_letters:
            wrong_letters[position].discard(letter)
        
        
    # Construct unique result code
    empty = ""
    for position in range(5):
        result += str(position)
        if position in exact_positions:
            result += exact_positions[position]
    include_str = empty.join(sorted(include_letters))
    result += "-" + include_str + "-"
    for position in range(5):
        result += str(position)
        mixed_str = empty.join(sorted(wrong_letters[position]))
        result += mixed_str
    absent_str = empty.join(sorted(absent_letters))
    result += "-" + absent_str

    return result


# Score list of words based on how much on average they reduce the space of
# available answers.
def score_words(guesses, eligible_answers):
    # Max value of this result is len(eligible_answers)^2
    score = 0
    patterns = {} # Number of times each result pattern is seen

    # Loop over all eligible answers and "score" the guess
    for answer in eligible_answers:
        # If we've already got it, ZERO solution space remains: add nothing
        if answer in guesses:
            continue

        # What information did we learn from this word?
        result = eval_words(guesses, answer)

        # Count the number of times this result pattern is seen
        if result in patterns:
            patterns[result] += 1
        else:
            patterns[result] = 1

    for result in patterns:
        # The # of times the pattern was seen is also the # of matches!
        # So prob(result) equals frac_matching(result) is just the square.
        score += patterns[result]**2

    return score


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

    # Load word lists and frequencies, from Wordle source answers only
    eligible_answers = get_five_letter_words(load_words('wordle-answers.txt'))
    eligible_guesses = eligible_answers
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
            if count % 50 == 0:
                #print(str(count) + "/" + str(len(eligible_guesses)))
                sys.stdout.write("\r" + '{:>3}'.format(count) + "/" + \
                  str(len(eligible_guesses)) + " (" + \
                  '{:>3.0%}'.format(float(count)/len(eligible_guesses)) + \
                  "): " + word + \
                  ": " + '{:>6.2%}'.format(word_scores[word]) + \
                  " [Best: " + best + ": " + \
                  '{:>6.2%}'.format(best_score) + "]  ")
                sys.stdout.flush()
    else:
        word_scores[my_word1] = \
          score_words([my_word1], eligible_answers) * score_scale

    sys.stdout.write("\r" + " "*75)
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



    # Now consider second words
    two_word_scores = {}
    if not my_word2:
        best = ""
        best_score = 1
        
        first_words_to_consider = min(30,len(scored_rank))
        for count1 in range(first_words_to_consider):
            word1 = scored_rank[count1]
            count2 = 0
            for word2 in eligible_guesses:
                count2 += 1
                pair = word1 + " " + word2
                two_word_scores[pair] = \
                  score_words([word1, word2], eligible_answers) * score_scale
                if two_word_scores[pair] < best_score:
                    best = pair
                    best_score = two_word_scores[pair]
                # Print an interesting progress message, since this is slow
                if count2 % 50 == 0:
                    sys.stdout.write("\r[" + '{:>2}'.format(count1) + "/" + \
                      str(first_words_to_consider) + "] " + \
                      '{:>3}'.format(count2) + "/" + \
                      str(len(eligible_guesses)) + " (" + \
                      '{:>3.0%}'.format(float(count2)/len(eligible_guesses)) + \
                      "): " + pair + \
                      ": " + '{:>7.3%}'.format(two_word_scores[pair]) + \
                      " [Best: " + best + ":" + \
                      '{:>7.3%}'.format(best_score) + "]  ")
                    sys.stdout.flush()
    else:
        two_word_scores[my_word1 + " " + my_word2] = \
          score_words([my_word1, my_word2], eligible_answers) * score_scale

    sys.stdout.write("\r" + " "*75)
    sys.stdout.flush()
    print

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
        print "..."
        for idx in range(-5,0):
            words = scored_rank_pairs[idx]
            word_list = words.split()
            print(words.upper() + ": " + \
              '{:>7.3%}'.format(two_word_scores[words]) + " = " \
              '{:>6.2%}'.format(word_scores[word_list[0]]) + " * " \
              '{:>6.2%}'.format(\
                  two_word_scores[words]/word_scores[word_list[0]]))



    # If (only if) we provided a second word, heck, let's go for three
    three_word_scores = {}
    if my_word1 and my_word2:
        count3 = 0
        best = ""
        best_score = 1
        
        for word3 in eligible_guesses:
            count3 += 1
            triple = my_word1 + " " + my_word2 + " " + word3
            three_word_scores[triple] = \
              score_words([my_word1, my_word2, word3], eligible_answers) \
                * score_scale
            if three_word_scores[triple] < best_score:
                best = triple
                best_score = three_word_scores[triple]
            # Print an interesting progress message, since this is slow
            if count3 % 50 == 0:
                sys.stdout.write("\r" + '{:>3}'.format(count3) + "/" + \
                  str(len(eligible_guesses)) + " (" + \
                  '{:>3.0%}'.format(float(count3)/len(eligible_guesses)) + \
                  "): " + triple + \
                  ": " + '{:>7.3%}'.format(three_word_scores[triple]) + \
                  " [Best: " + best + ":" + \
                  '{:>7.3%}'.format(best_score) + "]  ")
                sys.stdout.flush()

    sys.stdout.write("\r" + " "*75)
    sys.stdout.flush()
    print

    # Display the top ranking words
    scored_rank_triples = sorted(three_word_scores, key=three_word_scores.get)
    max_to_display = min(30,len(three_word_scores))
    for idx in range(max_to_display):
        words = scored_rank_triples[idx]
        word_list = words.split()
        first_pair = word_list[0] + " " + word_list[1]
        print(words.upper() + ": " + \
          '{:>7.3%}'.format(three_word_scores[words]) + " = " \
          '{:>6.2%}'.format(word_scores[word_list[0]]) + " * " \
          '{:>6.2%}'.format(\
              two_word_scores[first_pair]/word_scores[word_list[0]]) \
                   + " * " \
          '{:>6.2%}'.format(three_word_scores[words] / \
                                two_word_scores[first_pair]))
                        
    # Show the worst words, too, out of curiosity
    if len(three_word_scores) > max_to_display+5:
        print "..."
        for idx in range(-5,0):
            words = scored_rank_triples[idx]
            word_list = words.split()
        print(words.upper() + ": " + \
          '{:>7.3%}'.format(three_word_scores[words]) + " = " \
          '{:>6.2%}'.format(word_scores[word_list[0]]) + " * " \
          '{:>6.2%}'.format(\
              two_word_scores[first_pair]/word_scores[word_list[0]]) \
                   + " * " \
          '{:>6.2%}'.format(three_word_scores[words] / \
                                two_word_scores[first_pair]))
        