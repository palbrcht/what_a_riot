# what_a_riot

## Summary

Riot Games is a gigantic US-based video game company that produces world-known games like League of Legends, Legends of Runeterra, Valorant, among others.  The League of Legends game is one of the most popular online game in the world and has been relevant for over 10 years.  In a game of League of Legends, 10 players play against each other on two teams of 5 players.  

At the end of each game, individual player performance is 'graded' for each player depending on what character they use and what role they perform.  Players are graded similarly to how US schools grade students: A+, B-, C+, etc.  Just like school, an A+ is much better than a C.  However, in League of Legends, exceptional play will reward a S rank (S+, S, S-), which is the best rank a player can achieve.

While the creators of League of Legends have indicated roughly how these grades are achieved (percentile performance), Riot has never indicated specifically what variables or metrics are used to quantify performance.   Moreover, they have not indicated what thresholds are required for what metric either. This is by design to prevent characters from exploiting this information to 'game' the performance system.  Many players have speculated what metrics matter (and how much they matter), but no player has officially 'figured it out.' 

This project, called What a Riot, attempts to answer the question: What metrics matter in achieving the best performance grades in League of Legends?

## Process/Method

We used machine learning models to backwards engineer the match performance algorithm.  Like any machine learning model problem, the most important (and difficult) part was acquiring the data.  The in-game match data is not hard to acquire. Riot Games makes this readily available in their development API.  With some basic API querying, JSON parsing, and data wranling it's pretty easy to build a gigantic training data set.  

However, the actual letter grade (what we are trying to predict) is not available in the Riot Games API.  My assumption is that Riot does not include the actual game performance letter grade in the API because, ironically, they want to prevent players from doing exactly what we are doing. (Please read the Terms of Service section below to see why we think it's ok to do what we are doing and not agains the API TOS. Riot -- if you're reading this -- glad to explain!)  Using the Riot API we had the explanatory variables good to go (in-game performance data) but we did not have the outcome variable (letter grade).  

Because Riot keeps letter grades data private, there is no way to acquire large data sets in a scalable way for post-game performance letter grades.  So, to acquire the outcome variable (the letter grade), we went old school, 'went out into the field' figuratively speaking, and collected the data ourselves from our own post-game scoreboard screens.  At the post-game screen after every League of Legends match, the general scoreboard and game performance is shown to each player.  We took screenshots of our letter grades and compiled the meta data (player names) for this match into a spreadsheet.  We then used the Riot API to find what match a screenshot belonged to, then used the Riot API to compile the in-game match data for that particular screenshot. This would yield a record to be fed into a training set for a machine learning model. Since this is a very manual process, I recruited friends to help share their screen shots after every game. This would help scale up and speed up the creation of a training data set.


## What you'll need
-  You'll need an API key from Riot Games. Find them here:  https://developer.riotgames.com/
-  A .env file that has a list of player names and your Riot API key.

##  

##  Riot's API Terms of Service

need to update
