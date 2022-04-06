# what_a_riot

##  Current Status

We temporarily stopped work on this project to collect larger training data sets. (2/15/2022)

We are in the process of making an easier system to contribute match information.

## Summary

Riot Games is a gigantic US-based video game company that produces world-known games like League of Legends, Legends of Runeterra, Valorant, among others.  The League of Legends game is one of the most popular online game in the world and has been relevant for over 10 years.  In a game of League of Legends, 10 players play against each other on two teams of 5 players.  

At the end of each game, individual player performance is 'graded' for each player depending on what character they use and what role they perform.  Players are graded similarly to how US schools grade students: A+, B-, C+, etc.  Just like school, an A+ is much better than a C.  However, in League of Legends, exceptional play will reward a S rank (S+, S, S-), which is the best rank a player can achieve.

While the creators of League of Legends have indicated roughly how these grades are achieved (percentile performance), Riot has never indicated specifically what variables or metrics are used to quantify performance.   Moreover, they have not indicated what thresholds are required for what metric either. This is by design to prevent characters from exploiting this information to 'game' the performance system.  Many players have speculated what metrics matter (and how much they matter), but no player has officially 'figured it out.' 

This project, called What a Riot, attempts to answer the question: What metrics matter in achieving the best performance grades in League of Legends?

## Process/Method

We used machine learning models to backwards engineer the match performance algorithm.  Like any machine learning model problem, the most important (and difficult) part was acquiring the data.  The in-game match data is not hard to acquire. Riot Games makes this readily available in their development API.  With some basic API querying, JSON parsing, and data wranling it's pretty easy to build a gigantic training data set.  

However, the actual letter grade (what we are trying to predict) is not available in the Riot Games API.  My assumption is that Riot does not include the actual game performance letter grade in the API because, ironically, they want to prevent players from doing exactly what we are doing. (Please read the Terms of Service section below to see why we think it's ok to do what we are doing and not agains the API TOS. Riot -- if you're reading this -- glad to explain!)  Using the Riot API we had the explanatory variables good to go (in-game performance data) but we did not have the outcome variable (letter grade).  

Because Riot keeps letter grades data private, there is no way to acquire large data sets in a scalable way for post-game performance letter grades.  So, to acquire the outcome variable (the letter grade), we went old school, 'went out into the field' figuratively speaking, and collected the data ourselves from our own post-game scoreboard screens.  At the post-game screen after every League of Legends match, the general scoreboard and game performance is shown to each player.  We took screenshots of our letter grades and compiled the meta data (player names) for this match into a spreadsheet.  

We then used the Riot API to find what match a screenshot belonged to, then used the Riot API to compile the in-game match data for that particular screenshot. This would yield a record to be fed into a training set for a machine learning model. I say 'We' in this paragraph because I recruited friends to help share their screen shots after every game because since this is a very manual process. This helped scale up and speed up the creation of a training data set.

##  First Pass Model

I wanted to make a very parsimonious and simple model just to see if we could find anything at a very basic level.  I wanted to predict the most using the fewest amount of variables. I prefer this kind of approach because they are the easiest to act on (it's easier disseminating results and getting buy-in from stakeholders when there are fewer things to explain).

First, I had to subset the data to only include 1 character and 1 role. This is because each end of game letter grade is based upon percentile performance of a specific character playing a certain role.  (If you don't play the game, it basically just means there are different expectations of in-game performance depending on the character you use and the role you perform.)

I have a friend who obsessively plays Pyke support. And since he reported a ton of his games, he helped create a 30 or so game dataset within a week.  So, as a first pass, I used that specific data subset as preliminary training data.

Next, I had to pick the variables to include. I did not want to do an overkill ML model for this first pass -- just something simple to start with and see if conceptually we were on the right track.  I wanted to keep it simple and rudimentary. I also had a hunch that time was a major component since matches can last anywhere from 15 minutes to an hour.  So time definitely had to be one of the predictors, or at least controlled for and incorporated.  Next, I figured that I would just use earned gold in a match. The ideas is that every 'good' gameplay action in the game produces gold.  So, gold is a proxy variable for high performance.

So, I just plotted gold earned over time stratified by two groups: one group comprising of matches where a S+, S, and S- were earned compared against a group where A's B's and C's were earned in matches.

The plot below shows this and it clearly indicates that with gold alone we are onto something.  There's a decent bit to unpack in this plot but it's pretty simple and explains a lot:

![](https://user-images.githubusercontent.com/7535790/151630391-f9188515-60ce-4209-b52e-6dce8d4528ed.png)

I performed some standard logistic regressions and they confirmed the associations with gold, time, and game performance (didn't include that output).  The overall take-away here is that these simple tests gave us evidence that we could actually reverse engineer data.  Now it is time to move on to more complicated models and establish thresholds.

##  First ML model

Underway!

## What you'll need
-  You'll need an API key from Riot Games. Find them here:  https://developer.riotgames.com/
-  A .env file that has a list of player names and your Riot API key. 

##  Riot's API Terms of Service

need to update
