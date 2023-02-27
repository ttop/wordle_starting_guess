This python program suggests good five-letter words and word sequences to use as starting guesses in [WORDLE](https://www.powerlanguage.co.uk/wordle/). The results are summarized below (ranked by percentage of possible answers excluded), after some commentary. (Naturally, you should only use a generic "best" second word if the first doesn't provide clear direction for your next guess.)

The [original version of this code](https://github.com/ttop/wordle_starting_guess) was written by Todd Wells, but this version has diverged more and more radically. The analyze.py script here is a fairly direct (but expanded) descendant of that original, but the new version elim-analyze.py and its partners wordle-analyze.py and answers-analyze.py take an entirely different approach (slower, but I think substantially better), and that's what I'll describe here.

The code reads a list of common words (not plurals or conjugated verbs!) and extracts those with five letters as "eligible answers". For each word guess (or set of words) considered, it loops through _all_ eligible answers. For each possible answer, it evaluates the given word for exact and inexact letter matches just as Wordle does, and then counts how well that information would reduce the answer list for the player. The score of that guess is then calculated in three ways: 1) the average percentage of eligible answers not eliminated, 2) the worst-case result outcome that eliminates the fewest answers, and 3) the average estimated turns until a solution (estimating the number of turns necessary as a logarithm of the remaining answers for that result).

For multi-word suggestions, you can either provide a first word (or two) as command line arguments to compute the best options for the second (or third) word, or (the default) the code will consider the top 20 first words (for all three scoring methods) and score all eligible second words to follow them.

The wordle-analyze.py and answers-analyze.py scripts here use the actual Wordle word lists: with this scoring strategy, I've concluded that the details do matter (more than in letter frequency approaches). (Earlier versions used word lists from ef.edu and wordfrequency.info.) It's important that there are only 2,315 allowed Wordle _answers_, much less than the 12,972 allowed Wordle _guesses_: the answers are limited to more familiar words, and do not include any "derived forms" like plurals or conjugated verbs. (So 'S' is rare as the final letter!)

If you use the answers-analyze.py script to compute the top starting guesses including only words that could be answers, the top suggestions for initial words (with their three scores) are:

	Ranked by average solution space reduction:
			 avg    worst    log        rankings
	RAISE:  2.64%   7.26%   1.595       1       1       1
	ARISE:  2.75%   7.26%   1.612       2       2       6
	IRATE:  2.76%   8.38%   1.609       3       7       4
	AROSE:  2.85%   7.90%   1.628       4       4       9
	ALTER:  3.02%   8.47%   1.645       5       8      15
	SANER:  3.03%   9.46%   1.639       6      22      14
	LATER:  3.03%   8.47%   1.647       7       9      16
	SNARE:  3.07%   9.46%   1.628       8      23       8
	STARE:  3.08%   9.81%   1.616       9      37       7
	SLATE:  3.09%   9.55%   1.602      10      27       2
	ALERT:  3.09%   8.47%   1.635      11      10      11
	CRATE:  3.15%  10.63%   1.608      12      58       3
	TRACE:  3.20%  10.63%   1.609      13      59       5
	STALE:  3.27%   9.55%   1.637      14      28      13
	AISLE:  3.29%   8.47%   1.668      15      11      23
	LEARN:  3.31%   9.16%   1.662      16      14      20
	ALONE:  3.33%   7.86%   1.675      17       3      29
	LEANT:  3.34%   8.98%   1.653      18      13      18
	LEAST:  3.38%   9.55%   1.633      19      29      10
	CRANE:  3.40%  11.36%   1.636      20     107      12
	ATONE:  3.41%   8.25%   1.692      21       5      39
	TRAIL:  3.43%   9.46%   1.681      22      24      34
	REACT:  3.45%  10.63%   1.650      23      60      17
	SCARE:  3.49%  10.24%   1.670      24      40      25
	CATER:  3.49%  10.63%   1.665      25      61      21
	TRADE:  3.50%  11.62%   1.654      26     120      19
	RENAL:  3.51%   9.16%   1.692      27      15      40
	STORE:  3.51%  10.63%   1.676      28      62      30
	SNORE:  3.57%  10.24%   1.685      29      41      36
	SOLAR:  3.58%  10.02%   1.698      30      39      49
	...
	PUPPY: 33.60%  55.59%   2.596    2311    2312    2307
	MAMMA: 34.18%  53.22%   2.682    2312    2310    2315
	VIVID: 35.27%  57.37%   2.614    2313    2314    2310
	MUMMY: 35.45%  57.24%   2.621    2314    2313    2312
	FUZZY: 36.96%  58.40%   2.670    2315    2315    2314

	Ranked by worst case remaining possibilities:
			 avg    worst    log        rankings
	RAISE:  2.64%   7.26%   1.595       1       1       1
	ARISE:  2.75%   7.26%   1.612       2       2       6
	ALONE:  3.33%   7.86%   1.675      17       3      29
	AROSE:  2.85%   7.90%   1.628       4       4       9
	ATONE:  3.41%   8.25%   1.692      21       5      39
	RATIO:  3.97%   8.29%   1.754      72       6     138
	IRATE:  2.76%   8.38%   1.609       3       7       4
	ALTER:  3.02%   8.47%   1.645       5       8      15
	LATER:  3.03%   8.47%   1.647       7       9      16
	ALERT:  3.09%   8.47%   1.635      11      10      11

	Ranked by average log-estimated guesses remaining:
			 avg    worst    log        rankings
	RAISE:  2.64%   7.26%   1.595       1       1       1
	SLATE:  3.09%   9.55%   1.602      10      27       2
	CRATE:  3.15%  10.63%   1.608      12      58       3
	IRATE:  2.76%   8.38%   1.609       3       7       4
	TRACE:  3.20%  10.63%   1.609      13      59       5
	ARISE:  2.75%   7.26%   1.612       2       2       6
	STARE:  3.08%   9.81%   1.616       9      37       7
	SNARE:  3.07%   9.46%   1.628       8      23       8
	AROSE:  2.85%   7.90%   1.628       4       4       9
	LEAST:  3.38%   9.55%   1.633      19      29      10

Somewhat longer results lists can be found in the results files in this repository.

These first word results aren't all that different than the ones produced by the original scoring algorithm (and even closer to my adjustments to it), and in any case the words at the top of the list are fairly similar in effectiveness.

The three scoring methods have somewhat different meanings, and which you prefer is probably a matter of taste. Optimizing for the worst case means you're less likely to be very unlucky and not narrow the possibilities by much. The difference between the average overall reduction in solutions and the average of the logarithms is more subtle. Roughly speaking, if the result of each guess reduces the number of possible solutions by (e.g.) a factor of 10, then two guesses reduce by 10², three by 10³, and so on: the number of guesses to find a unique solution among _N_ options is roughly log(_N_). So the log-based "guesses remaining" score slightly favors words that split the possible solutions into a mix of larger and (substantially )smaller categories over words where all results lead to categories of comparable size. (To some degree, this is _opposite_ the strategy of minimizing the worst case result, and this is visible in the data above: the words in the list of the top 10 words for minimizing the worst case tend to be much lower in the log rankings than in the straight solution space rankings. The basic "average reduction of solution space" is something of a compromise between the two.)

Meanwhile, we can also consider suggested two-word combinations for each scoring strategy:

	Ranked by average solution space reduction:
				  avg                worst                log
	TRICE SALON: 0.188%=3.72%* 5.1%  0.994%=11.97%* 8.3%  0.479=1.668-1.189
	TRAIL SCONE: 0.197%=3.43%* 5.7%  0.994%= 9.46%*10.5%  0.499=1.681-1.183
	CRATE SOLID: 0.206%=3.15%* 6.5%  0.950%=10.63%* 8.9%  0.515=1.608-1.093
	TRACE SOLID: 0.206%=3.20%* 6.5%  0.950%=10.63%* 8.9%  0.515=1.609-1.094
	TRIAL SCONE: 0.207%=3.58%* 5.8%  0.994%= 9.46%*10.5%  0.514=1.698-1.184
	SLATE MINOR: 0.213%=3.09%* 6.9%  0.907%= 9.55%* 9.5%  0.528=1.602-1.074
	TRAIL SHONE: 0.214%=3.43%* 6.2%  1.123%= 9.46%*11.9%  0.522=1.681-1.159
	SNARE PILOT: 0.216%=3.07%* 7.0%  1.123%= 9.46%*11.9%  0.523=1.628-1.105
	SLATE IRONY: 0.218%=3.09%* 7.0%  0.907%= 9.55%* 9.5%  0.554=1.602-1.048
	ROAST PLIED: 0.218%=3.60%* 6.1%  0.821%=11.49%* 7.1%  0.534=1.665-1.131
	CRANE PILOT: 0.218%=3.40%* 6.4%  1.166%=11.36%*10.3%  0.517=1.636-1.119
	ALTER SONIC: 0.219%=3.02%* 7.2%  1.037%= 8.47%*12.2%  0.537=1.645-1.107
	CATER SOLID: 0.219%=3.49%* 6.3%  0.994%=10.63%* 9.3%  0.541=1.665-1.123
	SLATE CRONY: 0.219%=3.09%* 7.1%  0.994%= 9.55%*10.4%  0.534=1.602-1.067
	LATER SONIC: 0.219%=3.03%* 7.2%  1.123%= 8.47%*13.3%  0.537=1.647-1.109
	REACT SOLID: 0.220%=3.45%* 6.4%  0.994%=10.63%* 9.3%  0.533=1.650-1.117
	SLATE GROIN: 0.220%=3.09%* 7.1%  1.253%= 9.55%*13.1%  0.535=1.602-1.067
	RAISE CLOUT: 0.221%=2.64%* 8.4%  0.950%= 7.26%*13.1%  0.538=1.595-1.057
	TRAIL NOSEY: 0.221%=3.43%* 6.4%  0.691%= 9.46%* 7.3%  0.563=1.681-1.118
	CRANE SPILT: 0.222%=3.40%* 6.5%  1.425%=11.36%*12.5%  0.499=1.636-1.137

	Ranked by worst case remaining possibilities:
				  avg                worst                log
	TRAIL NOSEY: 0.221%=3.43%* 6.4%  0.691%= 9.46%* 7.3%  0.563=1.681-1.118
	ROAST PLIED: 0.218%=3.60%* 6.1%  0.821%=11.49%* 7.1%  0.534=1.665-1.131
	ALTER DISCO: 0.244%=3.02%* 8.1%  0.821%= 8.47%* 9.7%  0.586=1.645-1.058
	TRAIL HONEY: 0.253%=3.43%* 7.4%  0.821%= 9.46%* 8.7%  0.595=1.681-1.087
	LATER DISCO: 0.250%=3.03%* 8.3%  0.864%= 8.47%*10.2%  0.591=1.647-1.056
	ALONE STAIR: 0.272%=3.33%* 8.2%  0.864%= 7.86%*11.0%  0.633=1.675-1.042
	SLATE MINOR: 0.213%=3.09%* 6.9%  0.907%= 9.55%* 9.5%  0.528=1.602-1.074
	SLATE IRONY: 0.218%=3.09%* 7.0%  0.907%= 9.55%* 9.5%  0.554=1.602-1.048
	LEAST MINOR: 0.222%=3.38%* 6.6%  0.907%= 9.55%* 9.5%  0.542=1.633-1.091
	STALE MINOR: 0.225%=3.27%* 6.9%  0.907%= 9.55%* 9.5%  0.551=1.637-1.086

	Ranked by average log-estimated guesses remaining:
				  avg                worst                log
	TRICE SALON: 0.188%=3.72%* 5.1%  0.994%=11.97%* 8.3%  0.479=1.668-1.189
	TRAIL SCONE: 0.197%=3.43%* 5.7%  0.994%= 9.46%*10.5%  0.499=1.681-1.183
	CRANE SPILT: 0.222%=3.40%* 6.5%  1.425%=11.36%*12.5%  0.499=1.636-1.137
	CRANE SPLIT: 0.223%=3.40%* 6.6%  1.425%=11.36%*12.5%  0.508=1.636-1.128
	TRIAL SCONE: 0.207%=3.58%* 5.8%  0.994%= 9.46%*10.5%  0.514=1.698-1.184
	TRACE SOLID: 0.206%=3.20%* 6.5%  0.950%=10.63%* 8.9%  0.515=1.609-1.094
	CRATE SOLID: 0.206%=3.15%* 6.5%  0.950%=10.63%* 8.9%  0.515=1.608-1.093
	CRANE PILOT: 0.218%=3.40%* 6.4%  1.166%=11.36%*10.3%  0.517=1.636-1.119
	TRAIL SHONE: 0.214%=3.43%* 6.2%  1.123%= 9.46%*11.9%  0.522=1.681-1.159
	SNARE PILOT: 0.216%=3.07%* 7.0%  1.123%= 9.46%*11.9%  0.523=1.628-1.105

Clearly the two-word suggestions depend much more sensitively on strategy (they're quite different than the ones from my earlier letter frequency scoring algorithm, too). The least-worst-case strategy suggestions seem quite different than the other two. In any case, I'm not sure I'd recommend just adopting the top pair from your favorite list: you really do want that first word to be as effective as possible, to make it more likely that you can make an _informed_ second choice rather than these generic ones. I can see solid arguments for "TRICE SALON", "CRATE SOLID", among others, or maybe even "RAISE CLOUT" to use that much better first word.

And of course, take _all_ of this with a grain of salt: these suggestions might be optimal for a computer trying to guess, but it's entirely possible that the best approach for human brains is different. Maybe we'd be wiser to prioritize vowels, or first/last letters, or something else. But maybe these lists can still be useful as a menu of options.

Looking at a few generic third word choices, it's hard to judge how successful they are by looking at their contribution to the total scores:

	Ranked by average solution space reduction:
						avg               worst             log
	TRICE SALON DUMPY: 0.068%=3.7%*5%*36% 0.35%=12%*8%*35% 0.14=1.7-1.2-0.3 
	TRICE SALON PUDGY: 0.070%=3.7%*5%*37% 0.43%=12%*8%*43% 0.14=1.7-1.2-0.3 
	TRICE SALON PLUMB: 0.077%=3.7%*5%*41% 0.43%=12%*8%*43% 0.17=1.7-1.2-0.3 
    
    CRATE SOLID NYMPH: 0.069%=3.1%*7%*34% 0.39%=11%*9%*41% 0.14=1.6-1.1-0.4
	CRATE SOLID HYMEN: 0.076%=3.1%*7%*37% 0.39%=11%*9%*41% 0.17=1.6-1.1-0.3
	CRATE SOLID PHONY: 0.077%=3.1%*7%*37% 0.52%=11%*9%*55% 0.17=1.6-1.1-0.3
	
	RAISE CLOUT NYMPH: 0.075%=2.6%*8%*34% 0.35%=7%*13%*36% 0.16=1.6-1.1-0.4
	RAISE CLOUT DOWNY: 0.080%=2.6%*8%*36% 0.35%=7%*13%*36% 0.19=1.6-1.1-0.3
	RAISE CLOUT DINGY: 0.080%=2.6%*8%*36% 0.43%=7%*13%*45% 0.18=1.6-1.1-0.4

At best, these generic third words reduce the range of possibilities by 2/3 or so: much less than an order of magnitude. But in fact, these numbers are getting close to the least they could be. The worst-case situation after "trice salmon dumpy" is a collection of just 8 possible words, and the _average_ number of words remaining is 1.5: that suggests that you've solved the whole puzzle more often than not. Still, a word chosen to fit the known data is probably even more likely to narrow things down to a unique answer.

A somewhat longer collection of all this data is in the answers-analyze-results.txt file.

---

All of those results were limited to suggesting words that could be answers, but if we use wordle-analyze.py to allow ourselves the full range of Wordle guesses (while still scoring based only on the possible answers), the data looks rather different: ("+" marks words in the answers list, and I've inserted in brackets a few notable words and pairs from the lists above that fell outside the top 30 first words here)

	Ranked by average solution space reduction:
			 avg    worst    log        rankings
	ROATE:  2.61%   8.42%   1.594       1      30       2
	+RAISE: 2.64%   7.26%   1.595       2       1       3
	RAILE:  2.65%   7.47%   1.599       3       8       4
	SOARE:  2.69%   7.90%   1.593       4      15       1
	+ARISE: 2.75%   7.26%   1.612       5       2      11
	+IRATE: 2.76%   8.38%   1.609       6      26       9
	ORATE:  2.76%   8.42%   1.613       7      31      12
	ARIEL:  2.82%   7.47%   1.626       8       9      17
	+AROSE: 2.85%   7.90%   1.628       9      16      23
	RAINE:  2.90%   8.42%   1.623      10      32      15
	ARTEL:  2.92%   8.47%   1.628      11      35      22
	TALER:  2.93%   8.47%   1.627      12      36      18
	RATEL:  3.02%   8.47%   1.639      13      37      36
	AESIR:  3.02%   7.26%   1.672      14       3      86
	ARLES:  3.02%   8.86%   1.669      15      55      75
	REALO:  3.02%   7.60%   1.670      16      11      81
	+ALTER: 3.02%   8.47%   1.645      17      38      40
	+SANER: 3.03%   9.46%   1.639      18     141      35
	+LATER: 3.03%   8.47%   1.647      19      39      41
	+SNARE: 3.07%   9.46%   1.628      20     142      21
	...
	GYPPY: 38.33%  59.61%   2.688   12968   12970   12960
	JUGUM: 38.92%  60.91%   2.649   12969   12971   12949
	JUJUS: 39.03%  58.44%   2.754   12970   12963   12970
	QAJAQ: 40.61%  59.14%   2.832   12971   12968   12972
	IMMIX: 41.90%  61.73%   2.768   12972   12972   12971

	Ranked by worst case remaining possibilities:
			 avg    worst    log        rankings
	+RAISE: 2.64%   7.26%   1.595       2       1       3
	+ARISE: 2.75%   7.26%   1.612       5       2      11
	AESIR:  3.02%   7.26%   1.672      14       3      86
	REAIS:  3.09%   7.26%   1.683      28       4     117
	SERAI:  3.15%   7.26%   1.682      37       5     113
	AYRIE:  3.41%   7.39%   1.740      93       6     410
	AIERY:  3.76%   7.39%   1.756     212       7     545
	RAILE:  2.65%   7.47%   1.599       3       8       4
	ARIEL:  2.82%   7.47%   1.626       8       9      17
	ALOES:  3.34%   7.52%   1.701      76      10     177

	Ranked by average log-estimated guesses remaining:
			 avg    worst    log        rankings
	SOARE:  2.69%   7.90%   1.593       4      15       1
	ROATE:  2.61%   8.42%   1.594       1      30       2
	+RAISE: 2.64%   7.26%   1.595       2       1       3
	RAILE:  2.65%   7.47%   1.599       3       8       4
	REAST:  3.10%   9.81%   1.599      30     203       5
	+SLATE: 3.09%   9.55%   1.602      26     158       6
	+CRATE: 3.15%  10.63%   1.608      36     324       7
	SALET:  3.08%   9.55%   1.608      22     157       8
	+IRATE: 2.76%   8.38%   1.609       6      26       9
	+TRACE: 3.20%  10.63%   1.609      44     326      10

	Ranked by average solution space reduction:
				  avg                worst                log
	SOARE CLINT: 0.189%=2.69%* 7.0%  1.080%= 7.90%*13.7%  0.465=1.593-1.128
	CARTE NOILS: 0.195%=3.18%* 6.1%  0.907%=10.63%* 8.5%  0.497=1.620-1.123
	CRATE NOILS: 0.195%=3.15%* 6.2%  0.994%=10.63%* 9.3%  0.494=1.608-1.114
	RAINE CLOTS: 0.197%=2.90%* 6.8%  1.080%= 8.42%*12.8%  0.498=1.623-1.124
	RAINE COLTS: 0.197%=2.90%* 6.8%  1.080%= 8.42%*12.8%  0.500=1.623-1.123
	TRACE NOILS: 0.197%=3.20%* 6.2%  0.994%=10.63%* 9.3%  0.500=1.609-1.110
	SLANE TORIC: 0.197%=3.20%* 6.2%  0.994%= 9.72%*10.2%  0.493=1.628-1.134
	CARTE SLOID: 0.198%=3.18%* 6.2%  0.734%=10.63%* 6.9%  0.511=1.620-1.109
	SLANE DROIT: 0.198%=3.20%* 6.2%  0.950%= 9.72%* 9.8%  0.500=1.628-1.128
	SNARE DOILT: 0.199%=3.07%* 6.5%  1.123%= 9.46%*11.9%  0.492=1.628-1.136
	CARTE LOINS: 0.199%=3.18%* 6.3%  0.907%=10.63%* 8.5%  0.498=1.620-1.123
	CRATE LOINS: 0.199%=3.15%* 6.3%  0.994%=10.63%* 9.3%  0.496=1.608-1.112 
	CARTE LIONS: 0.199%=3.18%* 6.3%  0.907%=10.63%* 8.5%  0.502=1.620-1.118 
	TRACE LOINS: 0.201%=3.20%* 6.3%  0.994%=10.63%* 9.3%  0.501=1.609-1.108 
	CARET SLOID: 0.201%=3.27%* 6.2%  0.864%=10.63%* 8.1%  0.510=1.626-1.116
	AROSE CLINT: 0.201%=2.85%* 7.1%  1.037%= 7.90%*13.1%  0.493=1.628-1.135
	CARLE DOITS: 0.202%=3.23%* 6.2%  0.734%=10.76%* 6.8%  0.517=1.627-1.111
	CARTE SOLID: 0.202%=3.18%* 6.3%  0.734%=10.63%* 6.9%  0.515=1.620-1.105
	CARLE STOND: 0.202%=3.23%* 6.3%  0.950%=10.76%* 8.8%  0.518=1.627-1.109
	CRATE LIONS: 0.202%=3.15%* 6.4%  0.994%=10.63%* 9.3%  0.504=1.608-1.104
    [CRATE SOLID:0.206%=3.15%* 6.5%  0.950%=10.63%* 8.9%  0.515=1.608-1.093]
    [IRATE CLONS:0.208%=2.76%* 7.5%  0.994%= 8.38%*11.9%  0.519=1.609-1.090]

	Ranked by worst case remaining possibilities:
				  avg                worst                log
	CARTE SLOID: 0.198%=3.18%* 6.2%  0.734%=10.63%* 6.9%  0.511=1.620-1.109
	CARLE DOITS: 0.202%=3.23%* 6.2%  0.734%=10.76%* 6.8%  0.517=1.627-1.111
	CARTE SOLID: 0.202%=3.18%* 6.3%  0.734%=10.63%* 6.9%  0.515=1.620-1.105
	CARTE DIOLS: 0.203%=3.18%* 6.4%  0.734%=10.63%* 6.9%  0.521=1.620-1.099
	CARLE ODIST: 0.209%=3.23%* 6.5%  0.734%=10.76%* 6.8%  0.529=1.627-1.099
	CARTE LOIDS: 0.212%=3.18%* 6.7%  0.734%=10.63%* 6.9%  0.538=1.620-1.082
	CARTE SOLDI: 0.213%=3.18%* 6.7%  0.734%=10.63%* 6.9%  0.541=1.620-1.079
	CARTE LIDOS: 0.219%=3.18%* 6.9%  0.734%=10.63%* 6.9%  0.548=1.620-1.072
	SLATE NIDOR: 0.203%=3.09%* 6.6%  0.778%= 9.55%* 8.1%  0.524=1.602-1.077
	CARTE IDOLS: 0.227%=3.18%* 7.2%  0.778%=10.63%* 7.3%  0.569=1.620-1.051

	Ranked by average log-estimated guesses remaining:
				  avg                worst                log
	SOARE CLINT: 0.189%=2.69%* 7.0%  1.080%= 7.90%*13.7%  0.465=1.593-1.128
	CARLE SUINT: 0.203%=3.23%* 6.3%  1.296%=10.76%*12.0%  0.488=1.627-1.140
	SNARE DOILT: 0.199%=3.07%* 6.5%  1.123%= 9.46%*11.9%  0.492=1.628-1.136
	AROSE CLINT: 0.201%=2.85%* 7.1%  1.037%= 7.90%*13.1%  0.493=1.628-1.135
	SLANE TORIC: 0.197%=3.20%* 6.2%  0.994%= 9.72%*10.2%  0.493=1.628-1.134
	CRATE NOILS: 0.195%=3.15%* 6.2%  0.994%=10.63%* 9.3%  0.494=1.608-1.114
	CRATE LOINS: 0.199%=3.15%* 6.3%  0.994%=10.63%* 9.3%  0.496=1.608-1.112
	REOIL CANST: 0.203%=3.33%* 6.1%  1.037%= 8.03%*12.9%  0.497=1.705-1.209
	CARTE NOILS: 0.195%=3.18%* 6.1%  0.907%=10.63%* 8.5%  0.497=1.620-1.123
	CARTE LOINS: 0.199%=3.18%* 6.3%  0.907%=10.63%* 8.5%  0.498=1.620-1.123

	SOARE CLINT DUMPY: 0.068%=2.7%*7%*36% 0.52%=8%*14%*48% 0.13=1.6-1.1-0.3
	SOARE CLINT BUMPH: 0.070%=2.7%*7%*37% 0.43%=8%*14%*40% 0.13=1.6-1.1-0.3
	SOARE CLINT PUDGY: 0.070%=2.7%*7%*37% 0.52%=8%*14%*48% 0.13=1.6-1.1-0.3

If you're curious, ROATE is an archaic variant spelling of "rote", RAILE means "to flow (steadily and smoothly), SOARE is an obsolete term for a young hawk, CLINT is a Scottish term for a hard, flinty rock, CLONS are genetically identical cells produced by asexual reproduction, and so on. Honestly, I feel kinda dirty using word recommendations that aren't remotely part of my active vocabulary, but these pairs do narrow down your options more than most of the first list. If you aren't willing to jump to the mysterious SOARE CLINT despite its great effectiveness and you want a better first word than TRAIL, maybe AROSE CLINT is close enough to familiar language to be okay? CRATE LOINS is at least made of familiar words, even if the second is plural and can't be an answer, and CRATE SOLID is still a solid choice even though it falls just off these lists. Or maybe IRATE CLONS is close enough to the related word "clones" to be worth using. Your call!
