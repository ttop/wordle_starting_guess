import sys
import math
from collections import Counter

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
    #Calculate three different scores
    
    # Max value of this result is len(eligible_answers)^2
    avg_remaining = 0 # Later /len(e_a)^2 to give weighted avg remaining answers
    max_category = 0 # Size of largest pattern category (worst case outcome)
    log_depth = 0 # Store a sum of logs of sizes, to estimate later steps
    patterns = Counter() # Number of times each result pattern is seen

    # Loop over all eligible answers and "score" the guess
    for answer in eligible_answers:
        # If we've already got it, ZERO solution space remains: add nothing
        if answer in guesses:
            continue

        # What information did we learn from this word?
        result = eval_words(guesses, answer)

        # Count the number of times this result pattern is seen
        patterns[result] = patterns[result] + 1

    for result in patterns:
        # The # of times the pattern was seen is also the # of matches!
        # So prob(result) equals frac_matching(result) is just the square.
        avg_remaining += patterns[result]**2
        max_category = max(max_category, patterns[result])
        log_depth += patterns[result] * math.log10(patterns[result])

    # Normalize once for prob of category and once for fract remaining
    avg_remaining = float(avg_remaining)/len(eligible_answers)**2
    # Just a max fract remaining, so normalize by dividing once
    max_category = float(max_category)/len(eligible_answers)
    # Normalize for probability of each category before averaging
    log_depth = log_depth/len(eligible_answers)


    return [avg_remaining, max_category, log_depth]


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

    # Score all the words, or if the first was given, score just it
    # Each score is a list: average remaining, worst case, and average log
    word_scores = {}
    ranking_labels = ["average solution space reduction",
                          "worst case remaining possibilities",
                          "average log-estimated guesses remaining"]
    score_progress = 0 # Which score to show during progress
    
    if not my_word1:
        count = 0
        best = ""
        best_score = 1
        for word in eligible_guesses:
            count += 1
            word_scores[word] = score_words([word], eligible_answers)
            if word_scores[word][score_progress] < best_score:
                best = word
                best_score = word_scores[word][score_progress]
            # Print an interesting progress message, since this is slow
            if count % 50 == 0:
                #print(str(count) + "/" + str(len(eligible_guesses)))
                sys.stdout.write("\r" + '{:>3}'.format(count) + "/" + \
                  str(len(eligible_guesses)) + " (" + \
                  '{:>3.0%}'.format(float(count)/len(eligible_guesses)) + \
                  "): " + word + \
                  ": " + '{:>6.2%}'.format(word_scores[word][score_progress]) + \
                  " [Best: " + best + ": " + \
                  '{:>6.2%}'.format(best_score) + "]  ")
                sys.stdout.flush()
    else:
        word_scores[my_word1] = score_words([my_word1], eligible_answers)

    sys.stdout.write("\r" + " "*77)
    sys.stdout.flush()
    print()


    # Rank the words, in three ways
    scored_rank = [[],[],[]]
    for rank_by in range(3):
        # Break ties in worst case using average
        scored_rank[rank_by] = sorted(word_scores, \
          key=lambda score: (word_scores[score][rank_by],word_scores[score][0]))

    # Keep track of individual word ranking order
    word_ranks =  {}
    for word in word_scores:
        word_ranks[word] = [0,0,0]

    for word_num in range(len(word_scores)):
        for rank_by in range(3):
            word_ranks[scored_rank[rank_by][word_num]][rank_by] = word_num+1

            
    # Display the top ranking words, in all three ways
    for rank_by in range(3):
        print("Ranked by " + ranking_labels[rank_by] + ":")
        # Break ties in worst case using average
        scored_rank[rank_by] = sorted(word_scores, \
          key=lambda score: (word_scores[score][rank_by],word_scores[score][0]))

        max_to_display = min(30,len(word_scores))
        print(" "*9 + "avg" + " "*4 + "worst" + " "*4 + "log" + " "*8 + "rankings")
        for i in range(max_to_display):
            word = scored_rank[rank_by][i]
            print(word.upper() + ": " + 
                         '{:>6.2%}'.format(word_scores[word][0]) +
                  "  " + '{:>6.2%}'.format(word_scores[word][1]) +
                  "   " + '{:>4.3f}'.format(word_scores[word][2]) +
                  "   " + '{:>5}'.format(word_ranks[word][0]) +
                  "   " + '{:>5}'.format(word_ranks[word][1]) +
                  "   " + '{:>5}'.format(word_ranks[word][2]))

        # Show the worst words, too, out of curiosity
        if len(word_scores) > max_to_display+5:
            print("...")
            for i in range(-5,0):
                word = scored_rank[rank_by][i]
                print(word.upper() + ": " + 
                            '{:>6.2%}'.format(word_scores[word][0]) +
                    "  " +  '{:>6.2%}'.format(word_scores[word][1]) +
                    "   " + '{:>4.3f}'.format(word_scores[word][2]) +
                    "   " + '{:>5}'.format(word_ranks[word][0]) +
                    "   " + '{:>5}'.format(word_ranks[word][1]) +
                    "   " + '{:>5}'.format(word_ranks[word][2]))
        print()


    # Now consider second words
    two_word_scores = {}
    if not my_word2:
        best = ""
        best_score = 1

        # Merge first words of all three rankings
        first_words_to_consider = min(20,len(scored_rank[0]))
        first_words = set(scored_rank[0][:first_words_to_consider]).union(
            scored_rank[1][:first_words_to_consider],
            scored_rank[2][:first_words_to_consider])

        count1 = 0
        for word1 in first_words:
            count1 += 1
            count2 = 0
            for word2 in eligible_guesses:
                count2 += 1
                pair = word1 + " " + word2
                two_word_scores[pair] = \
                  score_words([word1, word2], eligible_answers)
                if two_word_scores[pair][score_progress] < best_score:
                    best = pair
                    best_score = two_word_scores[pair][score_progress]
                # Print an interesting progress message, since this is slow
                if count2 % 50 == 0:
                    sys.stdout.write("\r[" + '{:>2}'.format(count1) + "/" + \
                      str(len(first_words)) + "] " + \
                      '{:>3}'.format(count2) + "/" + \
                      str(len(eligible_guesses)) + " (" + \
                      '{:>3.0%}'.format(float(count2)/len(eligible_guesses)) + \
                      "): " + pair + \
                      ": " + '{:>7.3%}'.format(two_word_scores[pair][score_progress]) + \
                      " [Best: " + best + ":" + \
                      '{:>7.3%}'.format(best_score) + "]  ")
                    sys.stdout.flush()
    else:
        two_word_scores[my_word1 + " " + my_word2] = \
          score_words([my_word1, my_word2], eligible_answers)

    sys.stdout.write("\r" + " "*77)
    sys.stdout.flush()
    print()

    # Display the top ranking pairs
    scored_rank_pairs = [[],[],[]]
    for rank_by in range(3):
        print("Ranked by " + ranking_labels[rank_by] + ":")
        # Break ties in worst case by average
        scored_rank_pairs[rank_by] = sorted(two_word_scores, \
          key=lambda score: \
            (two_word_scores[score][rank_by],two_word_scores[score][0]))

        max_to_display = min(30,len(two_word_scores))
        print(" "*14 + "avg" + " "*16 + "worst" + " "*16 + "log")

        for i in range(max_to_display):
            words = scored_rank_pairs[rank_by][i]
            word_list = words.split()
            print(words.upper() + ": " + \
              '{:>6.3%}'.format(two_word_scores[words][0]) + "=" \
              '{:>5.2%}'.format(word_scores[word_list[0]][0]) + "*" \
              '{:>5.1%}'.format(\
                  two_word_scores[words][0]/word_scores[word_list[0]][0]) + \
              "  " + \
              '{:>6.3%}'.format(two_word_scores[words][1]) + "=" \
              '{:>6.2%}'.format(word_scores[word_list[0]][1]) + "*" \
              '{:>5.1%}'.format(\
                    two_word_scores[words][1]/word_scores[word_list[0]][1]) + \
              "  " + \
              '{:>4.3f}'.format(two_word_scores[words][2]) + "=" \
              '{:>4.3f}'.format(word_scores[word_list[0]][2]) + "-" \
              '{:>4.3f}'.format(\
                    word_scores[word_list[0]][2]-two_word_scores[words][2]))

        # Show the worst words, too, out of curiosity
        if len(two_word_scores) > max_to_display+5:
            print("...")
            for i in range(-5,0):
                words = scored_rank_pairs[rank_by][i]
                word_list = words.split()
                print(words.upper() + ": " + \
                  '{:>6.3%}'.format(two_word_scores[words][0]) + "=" \
                  '{:>5.2%}'.format(word_scores[word_list[0]][0]) + "*" \
                  '{:>5.1%}'.format(two_word_scores[words][0] / \
                                        word_scores[word_list[0]][0]) + \
                  "  " + \
                  '{:>6.3%}'.format(two_word_scores[words][1]) + "=" \
                  '{:>6.2%}'.format(word_scores[word_list[0]][1]) + "*" \
                  '{:>5.1%}'.format(two_word_scores[words][1] / \
                                        word_scores[word_list[0]][1]) + \
                  "  " + \
                  '{:>4.3f}'.format(two_word_scores[words][2]) + "=" \
                  '{:>4.3f}'.format(word_scores[word_list[0]][2]) + "-" \
                  '{:>4.3f}'.format(word_scores[word_list[0]][2] - \
                                        two_word_scores[words][2]))
        print()


    # Consider limiting eligible_guesses to eligible_answers here
    eligible_guesses = eligible_answers
    
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
              score_words([my_word1, my_word2, word3], eligible_answers)
            if three_word_scores[triple][score_progress] < best_score:
                best = triple
                best_score = three_word_scores[triple][score_progress]
            # Print an interesting progress message, since this is slow
            if count3 % 50 == 0:
                sys.stdout.write("\r" + '{:>3}'.format(count3) + "/" + \
                  str(len(eligible_guesses)) + " (" + \
                  '{:>3.0%}'.format(float(count3)/len(eligible_guesses)) + \
                  "): " + triple + \
                  ":" + \
                  '{:>7.3%}'.format(\
                        three_word_scores[triple][score_progress]) + \
                  " [Best: " + best + ":" + \
                  '{:>7.3%}'.format(best_score) + "]  ")
                sys.stdout.flush()

        sys.stdout.write("\r" + " "*77)
        sys.stdout.flush()
        print()

        # Display the top ranking triples
        scored_rank_triples = [[],[],[]]
        for rank_by in range(3):
            print("Ranked by " + ranking_labels[rank_by] + ":")
            # Break ties in worst case by average
            scored_rank_triples[rank_by] = sorted(three_word_scores, \
                                                      key=lambda score: \
                (three_word_scores[score][rank_by],three_word_scores[score][0]))

            max_to_display = min(30,len(three_word_scores))
            print(" "*20 + "avg" + " "*17 + "worst" + " "*17 + "log")

            for i in range(max_to_display):
                words = scored_rank_triples[rank_by][i]
                word_list = words.split()
                first_pair = word_list[0] + " " + word_list[1]
                print(words.upper() + ": " + \
              '{:>6.3%}'.format(three_word_scores[words][0]) + "=" \
              '{:>4.1%}'.format(word_scores[word_list[0]][0]) + "*" \
              '{:>3.0%}'.format(\
                  two_word_scores[first_pair][0]/word_scores[word_list[0]][0]) \
                       + "*" \
              '{:>3.0%}'.format(three_word_scores[words][0] / \
                                    two_word_scores[first_pair][0]) + \
              "  " + \
              '{:>6.3%}'.format(three_word_scores[words][1]) + "=" \
              '{:>4.1%}'.format(word_scores[word_list[0]][1]) + "*" \
              '{:>3.0%}'.format(\
                  two_word_scores[first_pair][1]/word_scores[word_list[0]][1]) \
                       + "*" \
              '{:>3.0%}'.format(three_word_scores[words][1] / \
                                    two_word_scores[first_pair][1]) + \
              "  " + \
              '{:>4.3f}'.format(three_word_scores[words][2]) + "=" \
              '{:>3.1f}'.format(word_scores[word_list[0]][2]) + "-" \
              '{:>3.1f}'.format(word_scores[word_list[0]][2] - \
                                    two_word_scores[first_pair][2]) \
                + "-" \
              '{:>3.1f}'.format(two_word_scores[first_pair][2] - \
                                    three_word_scores[words][2]))
            print()
        
