# P.S.I.
A data driven game.

## Sentiment Analysis
Difficulty and pace are functions of the niceness of a user's timeline.

## API
I make remote calls to my personal API, built with Flask into a Heroku app, for all of my functional needs. This keeps my projects lightweight and promotes a more streamlined use of multiprocessing/async. One of those needs is a call to the Twython for Python library to collect the tweets of anyone whom you might consider your peer (enemy) and/or friend (bantha-fodder).

## Data Collate
Thanks to the wonders of multithreading, as you play the game you are also scanning the sentiments of the users whom you attack for multiple data points. You can see why I am unable to freely distribute this game. Defamation is not a studying programmers concern. *gulp*

## Other Features
If you play against Donald Trump, all of the power ups become american flags and dollar bills.
If you play agains me (@YoshiYoshums), the theme is slightly Nintendo.

## Plans for future development (?)
- I would like to add an Elon Musk condition that turns the power ups into rocket boosters that land sit the bottom of the screen instead of disappearing.
- Fix the purple power up's line measure.

## Things I removed
- Ability to log-in. Again, this game is not for distrobution nor data mining (kinda) personal data.
- Stat tracking. For similar reasons.

## Things I would like changed
- Rethink the description of difficulty. Using the ratio of positive/negative words means 1 negative and 2 positive words makes the "playee" 50% unkind. This is surely not a fair representation. I would simply count total negative and total positive, and use each as game-state variables in their own terms.