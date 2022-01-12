This python program suggests good five-letter words and word sequences to use as starting guesses in [WORDLE](https://www.powerlanguage.co.uk/wordle/).

The [original version of this code](https://github.com/ttop/wordle_starting_guess) was written by Todd Wells, and focused entirely on first words: that's very reasonable, because once you get feedback that often shapes your later choices. But sometimes it doesn't help much and you just want to cover as much ground as possible: that's what this revised version is for. In the process, I also revised the scoring algorithm to better separate the value of knowing whether a given letter appears at all from the value of knowing where in the word it appears.

The code reads a list of common words (not plurals!) and pulls out those with five letters. It builds statistics for how many times each letter appears and for how likely each letter is at a given position. Then it scores each word, followed by word pairs, followed by triples.

The score is computed letter by letter in each word. The first time a letter appears, it adds a score equal to how often words in the list include it. For example, 'E' appears in 348 of the five-letter words, 'A' in 291 of them, 'R' in 285, and so on. The letter also adds a score for how often it appears _in that position_ within words in the list. For example, 'S' appears first in 80 words, 'C' is first in 62, etc. This number is multiplied by a factor of 1.5 and added to the total score. (Higher multipliers prioritize exact matches, lower ones prioritize letter variety.)

Finally, letters appearing in the second word contribute 50% of their base score, and letters in the third contribute only 20%: that's because you're less likely to actually use those suggestions instead of your own guess. (Unlike the original, repeated letters don't get an overall penalty: they contribute only their position score but not their overall frequency.)

The original code used a list of  [3,000 most common words in English](https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/), which resulted in 483 five letter words. This code instead uses a list of the [5000 most common word 'lemmas'](https://www.wordfrequency.info/samples.asp) (word roots, basically) from www.wordfrequency.info, which yields a list of 693 five letter words: I appreciate the somewhat larger sample. (Like the original creator, I didn't feel quite right just taking the eligible word list directly from the Wordle code: a bit too much like cheating.)

The top starting guesses resulting from all this (and their scores) are:

    STARE: 2046
    TRACE: 2029
    SHARE: 2021
    ARISE: 2007
    TRADE: 1931
    SCARE: 1929
    RAISE: 1927
    SPARE: 1885
    STORE: 1873
    SHORE: 1848
    SCALE: 1844
    REACT: 1843
    GRACE: 1839
    ALTER: 1812
    CHASE: 1811
    SLICE: 1808
    HEART: 1805
    SHADE: 1798
    LEAST: 1797
    STAGE: 1787
    LATER: 1785
    SAUCE: 1779
    GREAT: 1779
    STAIR: 1778
    SLAVE: 1774
    PLATE: 1766
    TRAIL: 1765
    SUITE: 1763
    SPACE: 1760
    SHINE: 1760

    SHARE POINT: 2728
    TRACE SOLID: 2727
    SHARE COUNT: 2705
    ARISE COUNT: 2691
    TRACE SOUND: 2689
    STARE CHILD: 2689
    ARISE CLOTH: 2677
    SHARE GUILT: 2672
    SHARE JOINT: 2663
    ARISE TOUCH: 2662
    SHARE PILOT: 2662
    STARE COULD: 2661
    SHARE MOUNT: 2647
    SHARE PRINT: 2641
    STARE POINT: 2637
    STARE BLIND: 2637
    SCARE POINT: 2637
    TRACE SHOUT: 2637
    SHARE COULD: 2636
    ARISE MOUNT: 2633

    SHARE POINT CRUEL: 2928
    SHARE POINT CLOUD: 2923
    SHARE COUNT DAILY: 2912
    SHARE POINT COULD: 2909
    SHARE COUNT BUILD: 2906
    SHARE COUNT DRILL: 2904
    SHARE POINT FLUID: 2904
    SHARE POINT BLEED: 2903
    TRACE SOLID CHUNK: 2903
    SHARE POINT TRULY: 2902
    SHARE COUNT FIELD: 2902
    SHARE POINT BLOCK: 2902
    SHARE COUNT BLIND: 2896
    SHARE POINT CLEAR: 2894
    SHARE COUNT YIELD: 2893
    STARE CHILD MOUNT: 2893
    SHARE POINT CLOCK: 2893
    SHARE POINT BADLY: 2892
    SHARE COUNT TRIAL: 2890
    SHARE POINT LUCKY: 2888

I can't tell if this is trying to be a Microsoft ad, or to warn us away.

What I _can_ tell is that my intuitive starting guess of TEARS was a good collection of letters, but not at all an optimal order. (And I suspect that a longer list of candidate words might give even better second or especially third word guesses, since "cruel" doesn't appear in the 3,000 word list.)
