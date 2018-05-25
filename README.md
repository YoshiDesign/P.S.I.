# Personal Space Invaders
A socially data-driven game.

# Controls

WASD - Movement

Space - Fire

LeftClick - Lazer Cloud

There is no pause menu...

### Usage
python invade.py

(Install requirements.txt first ya dingus)

(vrt) user@User:~/P.S.I.$ pip install -r requirements.txt

## Disclaimer
This game was created as a personal learning exercise. I hope others will use it to a similar degree.

Due to formatting requirements and intellectual property rights this game is in violation of the Twitter(R) Developer ToS. This software must not be distributed and must not be sold as is presented in this repository (YoshiDesign). It is a proof of concept and an educational tool. I hope you will find the amalgamation of the ideas presented to be inspiring. I hope to also promote the use of realtime data in video game development.

# Features

## Sentiment Analyzer
All tweets are scored using the Natural Language ToolKit (nltk). A score is presented based upon the nice : mean words ratio. This score could be used to adjust difficulty, however, at this time all scenarios are the same difficulty (and non biased!). 

## API
Tweets(R) are collected over encrypted TLS1.2; the service making the Twython calls is not (directly) baked into this client. The game supports a currently disabled login fsystem and Twitter OAuth. All communications are encrypted. Passwords are transmitted as MD5 digests.

## Other Features
If you play against the current U.S. president, all of the power ups become american flags and dollar bills.
If you play agains me (@YoshiYoshums), the theme is slightly more retro.

## Plans for future development (?)
Probably not. I hope a fellow programmer will tweak this project to their liking. But seeing how many restrictions are placed on intellectual property rights, I think I will move on to my next project

## Bugs
None?

## Optimization
The bullets and bombs do not play well together. Needs some friendly optimizations from the maths and threads department.
