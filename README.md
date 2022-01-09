I wanted to figure out the best five-letter word to use as a starting word in [WORDLE](https://www.powerlanguage.co.uk/wordle/).

I grabbed a list of the supposed [3,000 most common words in English](https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/). I intentionally did not grab the actual word list which WORDLE uses, that felt a bit unfair, but regardless I have to imagine my top-rated guesses are probably in this list.

This code reads that list, filters it down to just the five-letter words (483 of them, from here on referred to as the "eligible words"), and then scores each word.

Each word gets a score based on the letters that appear in the word. Part of the score is based on the frequency of each letter in the eligible words. For example, 'A' is the most commonly used letter in the eligible words--it appears a total of 213 times--so an 'A' gets 213 points. 

The other part of the score is based on the frequency of the letter _in that position_ within the eligible words. For example, 'S' is the most frequent letter used in the first position (80 words), so it gets a bonus of 80 * 3 (I use 3 as an arbitrary multiplier here).

Additionally, a letter's score is reduced each additional time that it appears in a word, since knowing which letters appear in the answer is valuable information and without knowing ahead of time that a letter appears multiple times it is probably best to avoid duplicate letters in the initial guess. So each additional time that a letter appears I have arbitrarily divided that letter's score by 4 times the number of times it has previously appeared. 

Here are the top 15 starting guesses based on using this algorithm, along with their score:

    TRACE: 2085
    SHARE: 2068
    STARE: 2049
    ARISE: 1982
    TRADE: 1938
    SHORE: 1918
    STORE: 1899
    SCALE: 1879
    RAISE: 1874
    SHINE: 1868
    SLICE: 1868
    SHADE: 1864
    CHASE: 1864
    SAUCE: 1860
    SHAPE: 1838
    SPACE: 1836
    STONE: 1824
    STAGE: 1822
    SLAVE: 1809
    STATE: 1807
    PRICE: 1807
    SHAKE: 1804
    THOSE: 1796
    PHASE: 1793
    PLATE: 1785
    STAKE: 1785
    SCORE: 1775
    WRITE: 1770
    REACT: 1764
    TRIBE: 1763

Before I undertook this effort, I speculated that STARE was a very good starting guess. And according to this scoring methodology, that is true -- it ended up in third place.