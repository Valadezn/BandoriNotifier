# BandoriNotifier

Windows notifier that sends toast notifications about how much time is left in a Ban

## Installation

This program obtains its data from [Bestdori](https://bestdori.com/). Therefore, the library [requests-html](http://requests-html.kennethreitz.org/) is used to obtain Javascript data from Bestdori.

Install requests-html using pip:
```
pip install requests-html
```

Then clone the repository and run Main.py from your terminal.
```
python Main.py
```

## Inspiration
BanGDream! Girls Band Party (or Bandori for short) is a rhythm gacha mobile game for Android and iOS. The game has Japan, WorldWide, China, Korea, and Taiwain servers, anc each server starts events at different times. 

This program was made so that someone who doesn't purposly check when an event ends can see how much time is left to gain event points before the event ends.