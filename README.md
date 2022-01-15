This python program suggests good five-letter words and word sequences to use as starting guesses in [WORDLE](https://www.powerlanguage.co.uk/wordle/). The results are summarized below (ranked by percentage of possible answers excluded), after some commentary. (Naturally, you should only use a generic "best" second word if the first doesn't provide clear direction for your next guess.)

The [original version of this code](https://github.com/ttop/wordle_starting_guess) was written by Todd Wells, but this version has diverged more and more radically. The analyze.py script here is a fairly direct (but expanded) descendant of that original, but the new version elim-analyze.py takes an entirely different approach (much slower, but I think substantially better), and that's what I'll describe here.

The code reads a list of common words (not plurals or conjugated verbs!) and extracts those with five letters as "eligible answers". For each word guess (or set of words) considered, it loops through _all_ eligible answers. For each possible answer, it evaluates the given word for exact and inexact letter matches just as Wordle does, and then counts how well that information would reduce the answer list for the player. The score of that guess is then the average percentage of eligible answers not eliminated.

For multi-word suggestions, you can either provide a first word (or two) as command line arguments to compute the best options for the second (or third) word, or (the default) the code will consider the top 20 first words and score all eligible second words to follow them. This is _slow_: on my computer, this code scores between 5-10 patterns per second, which adds up to over a minute for single words and 20 times that for the top pairs.

The original code used a list of  [3,000 most common words in English](https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/), which resulted in 483 five letter words. This code instead uses a list of the [5000 most common word 'lemmas'](https://www.wordfrequency.info/samples.asp) (dictionary entry words, basically) from www.wordfrequency.info, which yields a list of 693 five letter words: I appreciate the somewhat larger sample, though the results are fairly similar. (Like the original creator, I haven't felt quite right just taking the eligible word list directly from the Wordle code: a bit too much like cheating.) It's worth noting that, as far as I've seen, Wordle _solutions_ are never(?) plurals or verb conjugations: if you use a word list that includes those, almost all of the top suggestions end in "ES". (Plurals are still valid _guesses_.)

The top starting guesses resulting from all this (and the average percentage of eligible answers that are still allowed after each) are:

	ARISE:  2.17%
	TRACE:  2.33%
	RAISE:  2.34%
	STARE:  2.47%
	TRADE:  2.54%
	ALTER:  2.76%
	SHARE:  2.80%
	REACT:  2.81%
	TRAIL:  2.84%
	LEAST:  2.86%
	LATER:  2.89%
	STORE:  2.94%
	SCARE:  2.98%
	TRIAL:  2.98%
	LASER:  2.99%
	HEART:  3.01%
	STAIR:  3.02%
	AISLE:  3.15%
	TRAIN:  3.20%
	LEARN:  3.25%
	CLEAR:  3.26%
	GREAT:  3.35%
	SHORE:  3.39%
	ALONE:  3.41%
	SOLAR:  3.48%
	SCORE:  3.48%
	EARTH:  3.49%
	THEIR:  3.51%
	ROUTE:  3.54%
	HORSE:  3.55%
	...
	KNOWN: 26.45%
	FUNNY: 29.16%
	CIVIC: 30.21%
	BUDDY: 33.50%
	MOMMY: 36.45%

	TRAIN CLOSE:  0.278% =  3.20% *  8.68%
	TRACE SOLID:  0.281% =  2.33% * 12.07%
	ARISE CLOTH:  0.297% =  2.17% * 13.71%
	TRAIN SLOPE:  0.299% =  3.20% *  9.34%
	AISLE COURT:  0.301% =  3.15% *  9.55%
	TRACE SOUND:  0.306% =  2.33% * 13.16%
	SCARE PILOT:  0.309% =  2.98% * 10.38%
	ARISE COUNT:  0.310% =  2.17% * 14.29%
	RAISE COUNT:  0.313% =  2.34% * 13.33%
	TRAIL SCOPE:  0.313% =  2.84% * 11.02%
	RAISE CLOTH:  0.314% =  2.34% * 13.39%
	TRAIN SHELF:  0.317% =  3.20% *  9.92%
	TRAIN SLICE:  0.318% =  3.20% *  9.94%
	TRAIN FLESH:  0.318% =  3.20% *  9.96%
	REACT SOLID:  0.319% =  2.81% * 11.35%
	ARISE MONTH:  0.320% =  2.17% * 14.77%
	TRAIL PHONE:  0.320% =  2.84% * 11.28%
	SCARE POINT:  0.320% =  2.98% * 10.77%
	STAIR UNCLE:  0.321% =  3.02% * 10.62%
	TRAIL HOUSE:  0.322% =  2.84% * 11.33%
	AISLE NORTH:  0.322% =  3.15% * 10.21%
	TRAIN PULSE:  0.323% =  3.20% * 10.09%
	TRIAL SCOPE:  0.323% =  2.98% * 10.84%
	STARE CHILD:  0.325% =  2.47% * 13.17%
	LEAST MINOR:  0.328% =  2.86% * 11.47%
	TRAIN SCOPE:  0.328% =  3.20% * 10.27%
	TRAIL SCENE:  0.328% =  2.84% * 11.56%
	STORE PLAIN:  0.329% =  2.94% * 11.19%
	TRAIL SINCE:  0.330% =  2.84% * 11.61%
	STARE COULD:  0.331% =  2.47% * 13.42%
	...
	STAIR STAIR:  3.022% =  3.02% * 100.00%
	TRAIN IRAQI:  3.054% =  3.20% * 95.49%
	AISLE AISLE:  3.154% =  3.15% * 100.00%
	TRAIN TRAIN:  3.198% =  3.20% * 100.00%
	LEARN LEARN:  3.253% =  3.25% * 100.00%

These first word results aren't all that different than the ones produced by the original scoring algorithm (and even closer to my adjustments to it), and in any case the words at the top of the list are fairly similar in effectiveness. But the two-word suggestions here are surprisingly different than the ones produced by my frequency-scoring algorithm: this must be somehow taking advantage of deeper patterns in letter arrangements. (It's quite striking that TRAIN, just rank 19/20 among first guesses, leads to 25% of the top two-word combinations including the top spot. But you really do want that first word to be as effective as possible, to make it more likely that you can make an _informed_ second choice rather than these generic ones.)

And of course, these suggestions might be optimal for a computer trying to guess, but it's entirely possible that the best approach for human brains is different: maybe we'd be wiser to prioritize vowels, or first/last letters, or something else.

Looking at a few third word choices, it would appear that an uninformed, "generic" choice of third word really isn't very helpful. Here are a couple of examples:

	ARISE CLOTH POUND:  0.178% =  2.17% * 13.71% * 59.78%
	ARISE CLOTH FOUND:  0.178% =  2.17% * 13.71% * 59.92%
	ARISE CLOTH DEMON:  0.180% =  2.17% * 13.71% * 60.48%
	ARISE CLOTH WOUND:  0.180% =  2.17% * 13.71% * 60.62%
	ARISE CLOTH DYING:  0.183% =  2.17% * 13.71% * 61.60%
	ARISE CLOTH UNDER:  0.183% =  2.17% * 13.71% * 61.60%
	ARISE CLOTH ROUND:  0.184% =  2.17% * 13.71% * 61.88%
	ARISE CLOTH YOUNG:  0.184% =  2.17% * 13.71% * 62.02%
	ARISE CLOTH DRUNK:  0.184% =  2.17% * 13.71% * 62.02%
	ARISE CLOTH NAKED:  0.185% =  2.17% * 13.71% * 62.30%

	TRACE SOLID PUNCH:  0.175% =  2.33% * 12.07% * 62.34%
	TRACE SOLID HUMAN:  0.175% =  2.33% * 12.07% * 62.34%
	TRACE SOLID BUNCH:  0.176% =  2.33% * 12.07% * 62.64%
	TRACE SOLID BENCH:  0.182% =  2.33% * 12.07% * 64.71%
	TRACE SOLID PHONE:  0.182% =  2.33% * 12.07% * 64.86%
	TRACE SOLID MONTH:  0.183% =  2.33% * 12.07% * 65.01%
	TRACE SOLID THUMB:  0.183% =  2.33% * 12.07% * 65.01%
	TRACE SOLID CHUNK:  0.183% =  2.33% * 12.07% * 65.01%
	TRACE SOLID FUNNY:  0.185% =  2.33% * 12.07% * 65.90%
	TRACE SOLID LUNCH:  0.185% =  2.33% * 12.07% * 65.90%

At best, these third words reduce the range of possibilities by 40%. You're undoubtedly better off making an informed third choice based on the knowledge gained from the first two guesses (though perhaps the program output could still be useful as a list of suggestions).
