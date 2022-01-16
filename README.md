This python program suggests good five-letter words and word sequences to use as starting guesses in [WORDLE](https://www.powerlanguage.co.uk/wordle/). The results are summarized below (ranked by percentage of possible answers excluded), after some commentary. (Naturally, you should only use a generic "best" second word if the first doesn't provide clear direction for your next guess.)

The [original version of this code](https://github.com/ttop/wordle_starting_guess) was written by Todd Wells, but this version has diverged more and more radically. The analyze.py script here is a fairly direct (but expanded) descendant of that original, but the new version elim-analyze.py and its partners wordle-analyze.py and answers-analyze.py take an entirely different approach (slower, but I think substantially better), and that's what I'll describe here.

The code reads a list of common words (not plurals or conjugated verbs!) and extracts those with five letters as "eligible answers". For each word guess (or set of words) considered, it loops through _all_ eligible answers. For each possible answer, it evaluates the given word for exact and inexact letter matches just as Wordle does, and then counts how well that information would reduce the answer list for the player. The score of that guess is then the average percentage of eligible answers not eliminated. _(I've also seen suggestions to score based on the least useful result you might get, or based on the average of a logarithmic estimate of the number of remaining guesses needed, but I haven't tried those yet.)_

For multi-word suggestions, you can either provide a first word (or two) as command line arguments to compute the best options for the second (or third) word, or (the default) the code will consider the top 20 first words and score all eligible second words to follow them.

The wordle-analyze.py and answers-analyze.py scripts here use the actual Wordle word lists: with this scoring strategy, I've concluded that the details do matter (more than in letter frequency approaches). (Earlier versions used word lists from ef.edu and wordfrequency.info.) It's important that there are only 2315 allowed Wordle _answers_, much less than the 12,972 allowed Wordle _guesses_: the answers are limited to more familiar words, and do not include any "derived forms" like plurals or conjugated verbs. (So 'S' is rare as the final letter!)

If you use the answers-analyze.py script to compute the top starting guesses including only words that could be answers, the top suggestions for initial words and initial word pairs (and the average percentage of eligible answers that are still allowed after each) are:

	RAISE:  2.64%
	ARISE:  2.75%
	IRATE:  2.76%
	AROSE:  2.85%
	ALTER:  3.02%
	SANER:  3.03%
	LATER:  3.03%
	SNARE:  3.07%
	STARE:  3.08%
	SLATE:  3.09%
	ALERT:  3.09%
	CRATE:  3.15%
	TRACE:  3.20%
	STALE:  3.27%
	AISLE:  3.29%
	LEARN:  3.31%
	ALONE:  3.33%
	LEANT:  3.34%
	LEAST:  3.38%
	CRANE:  3.40%
	ATONE:  3.41%
	TRAIL:  3.43%
	REACT:  3.45%
	SCARE:  3.49%
	CATER:  3.49%
	TRADE:  3.50%
	RENAL:  3.51%
	STORE:  3.51%
	SNORE:  3.57%
	SOLAR:  3.58%
	...
    PUPPY: 33.60%
	MAMMA: 34.18%
	VIVID: 35.27%
	MUMMY: 35.45%
	FUZZY: 36.96%

	TRAIL SCONE:  0.197% =  3.43% *  5.74%
	CRATE SOLID:  0.206% =  3.15% *  6.54%
	TRACE SOLID:  0.206% =  3.20% *  6.45%
	SLATE MINOR:  0.213% =  3.09% *  6.89%
	TRAIL SHONE:  0.214% =  3.43% *  6.23%
	SNORE PLAIT:  0.215% =  3.57% *  6.04%
	SNARE PILOT:  0.216% =  3.07% *  7.03%
	SNORE TIDAL:  0.218% =  3.57% *  6.10%
	SLATE IRONY:  0.218% =  3.09% *  7.04%
	CRANE PILOT:  0.218% =  3.40% *  6.42%
	ALTER SONIC:  0.219% =  3.02% *  7.23%
	CATER SOLID:  0.219% =  3.49% *  6.26%
	SLATE CRONY:  0.219% =  3.09% *  7.08%
	LATER SONIC:  0.219% =  3.03% *  7.23%
	REACT SOLID:  0.220% =  3.45% *  6.37%
	SLATE GROIN:  0.220% =  3.09% *  7.11%
	RAISE CLOUT:  0.221% =  2.64% *  8.37%
	TRAIL NOSEY:  0.221% =  3.43% *  6.45%
	CRANE SPILT:  0.222% =  3.40% *  6.51%
	LEAST MINOR:  0.222% =  3.38% *  6.59%
	TRAIL COPSE:  0.223% =  3.43% *  6.48%
	SANER CLOUT:  0.223% =  3.03% *  7.35%
	LATER SCION:  0.223% =  3.03% *  7.35%
	CRATE SPOIL:  0.223% =  3.15% *  7.08%
	CRANE SPLIT:  0.223% =  3.40% *  6.56%
	IRATE SCOLD:  0.224% =  2.76% *  8.12%
	ALONE CRUST:  0.224% =  3.33% *  6.72%
	TRACE SPOIL:  0.224% =  3.20% *  7.01%
	LEARN MOIST:  0.224% =  3.31% *  6.77%
	STALE CRONY:  0.224% =  3.27% *  6.87%

These first word results aren't all that different than the ones produced by the original scoring algorithm (and even closer to my adjustments to it), and in any case the words at the top of the list are fairly similar in effectiveness. But the two-word suggestions here are surprisingly different than the ones produced by my frequency-scoring algorithm: this must be somehow taking advantage of deeper patterns in letter arrangements. But I'm not sure I'd recommend just adopting the top two-word pair here: you really do want that first word to be as effective as possible, to make it more likely that you can make an _informed_ second choice rather than these generic ones. I can see solid arguments for "TRAIL SCONE", "CRATE SOLID", or maybe even "RAISE CLOUT" to get that much better first word.

And of course, these suggestions might be optimal for a computer trying to guess, but it's entirely possible that the best approach for human brains is different: maybe we'd be wiser to prioritize vowels, or first/last letters, or something else.

Looking at a few third word choices, it would appear that an uninformed, "generic" choice of third word really isn't very helpful. Here are a few examples:

	TRAIL SCONE DUMPY:  0.070% =  3.43% *  5.74% * 35.74%
	TRAIL SCONE PUDGY:  0.072% =  3.43% *  5.74% * 36.59%
	TRAIL SCONE PLUMB:  0.080% =  3.43% *  5.74% * 40.79%
	TRAIL SCONE GLYPH:  0.081% =  3.43% *  5.74% * 41.15%
	TRAIL SCONE PYGMY:  0.081% =  3.43% *  5.74% * 41.19%

	CRATE SOLID NYMPH:  0.069% =  3.15% *  6.54% * 33.66%
	CRATE SOLID HYMEN:  0.076% =  3.15% *  6.54% * 36.79%
	CRATE SOLID PHONY:  0.077% =  3.15% *  6.54% * 37.19%
	CRATE SOLID MANGY:  0.077% =  3.15% *  6.54% * 37.42%
	CRATE SOLID HUNKY:  0.078% =  3.15% *  6.54% * 37.95%

	RAISE CLOUT NYMPH:  0.075% =  2.64% *  8.37% * 34.22%
	RAISE CLOUT DOWNY:  0.080% =  2.64% *  8.37% * 36.19%
	RAISE CLOUT DINGY:  0.080% =  2.64% *  8.37% * 36.21%
	RAISE CLOUT DUMPY:  0.081% =  2.64% *  8.37% * 36.82%
	RAISE CLOUT HANDY:  0.081% =  2.64% *  8.37% * 36.82%

At best, these generic third words reduce the range of possibilities by 2/3. You're almost certainly better off making an informed third choice based on the knowledge gained from the first two guesses (though perhaps the program output could still be useful as a list of suggestions).

---

All of those results were limited to suggesting words that could be answers, but if we use wordle-analyze.py to allow ourselves the full range of Wordle guesses (while still scoring based only on the possible answers), the data looks rather different: ("+" marks words in the answers list, and I've inserted in brackets a few notable words and pairs from the lists above that fell outside the top 30 first words here)

	ROATE:  2.61%
	+RAISE:  2.64%
	RAILE:  2.65%
	SOARE:  2.69%
	+ARISE:  2.75%
	+IRATE:  2.76%
	ORATE:  2.76%
	ARIEL:  2.82%
	+AROSE:  2.85%
	RAINE:  2.90%
	ARTEL:  2.92%
	TALER:  2.93%
	RATEL:  3.02%
	AESIR:  3.02%
	ARLES:  3.02%
	REALO:  3.02%
	+ALTER:  3.02%
	+SANER:  3.03%
	+LATER:  3.03%
	+SNARE:  3.07%
	OATER:  3.08%
	SALET:  3.08%
	TASER:  3.08%
	+STARE:  3.08%
	TARES:  3.09%
	+SLATE:  3.09%
	+ALERT:  3.09%
	REAIS:  3.09%
	LARES:  3.10%
	REAST:  3.10%
	...
	[CRATE:  3.15%]
	[TRACE:  3.20%]
	[TRAIL: 3.43%]
	...
	GYPPY: 38.33%
	JUGUM: 38.92%
	JUJUS: 39.03%
	QAJAQ: 40.61%
	IMMIX: 41.90%

	SOARE CLINT:  0.189% =  2.69% *  7.01%
	RAINE CLOTS:  0.197% =  2.90% *  6.80%
	RAINE COLTS:  0.197% =  2.90% *  6.80%
	[+TRAIL SCONE:  0.197% =  3.43% *  5.74%]
	SNARE DOILT:  0.199% =  3.07% *  6.46%
	AROSE CLINT:  0.201% =  2.85% *  7.06%
	SLATE CORNI:  0.202% =  3.09% *  6.54%
	SLATE ORCIN:  0.202% =  3.09% *  6.54%
	SLATE NIDOR:  0.203% =  3.09% *  6.58%
	SANER DOILT:  0.204% =  3.03% *  6.74%
	STARE COLIN:  0.204% =  3.08% *  6.63%
	SLATE PRION:  0.206% =  3.09% *  6.66%
	RAINE SMOLT:  0.206% =  2.90% *  7.13%
	RAILE STOND:  0.206% =  2.65% *  7.79%
	[+CRATE SOLID:  0.206% =  3.15% *  6.54%]
	[+TRACE SOLID:  0.206% =  3.20% *  6.45%]
	REAST COLIN:  0.207% =  3.10% *  6.69%
	SALET ORCIN:  0.207% =  3.08% *  6.74%
	?IRATE CLONS:  0.208% =  2.76% *  7.54%
	SALET CORNI:  0.208% =  3.08% *  6.75%
	SLATE PROIN:  0.209% =  3.09% *  6.75%
	TALER COINS:  0.209% =  2.93% *  7.15%
	TALER CIONS:  0.209% =  2.93% *  7.16%
	TALER SONIC:  0.210% =  2.93% *  7.17%
	RATEL CIONS:  0.210% =  3.02% *  6.97%
	RAINE SLOTH:  0.211% =  2.90% *  7.27%
	RAILE SOUCT:  0.211% =  2.65% *  7.95%
	RAINE DOLTS:  0.211% =  2.90% *  7.28%
	RAILE PONTS:  0.211% =  2.65% *  7.97%
	SOARE CLIPT:  0.212% =  2.69% *  7.86%
	?SLATE DORIC:  0.212% =  3.09% *  6.86%
	SNARE LOTIC:  0.212% =  3.07% *  6.92%
	+SLATE MINOR:  0.213% =  3.09% *  6.89%

If you're curious, ROATE is an archaic variant spelling of "rote", RAILE means "to flow (steadily and smoothly), SOARE is an obsolete term for a young hawk, CLINT is a Scottish term for a hard, flinty rock,  CLONS are genetically identical cells produced by asexual reproduction, and so on. Honestly, I feel kinda dirty using word recommendations that aren't remotely part of my active vocabulary, but these pairs do narrow down your options more than most of the first list. If you aren't willing to jump to the mysterious SOARE CLINT despite its great effectiveness and you want a better first word than TRAIL, maybe AROSE CLINT is close enough to familiar language to be okay? CRATE SOLID is still a solid choice, or maybe IRATE CLONS is close enough to the related word "clones" to be worth using. Your call!
