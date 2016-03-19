#install.packages('streamR','RCurl','RJSONIO')
library(ROAuth)
library(streamR)
library(RCurl)
library(RJSONIO)
library(stringr)

setwd('/Users/saguinag/Research/SocialSensing/NetAnalysis/')
load('my_oauth.Rdata')
filterStream(file.name = "tweets.json", # Save tweets in a json file
             track = c("C++ 17"), # Collect tweets mentioning either Affordable Care Act, ACA, or Obamacare
             language = "en",
             timeout = 60, # Keep connection alive for 60 seconds
             oauth = my_oauth) # Use my_oauth file as the OAuth credentials

tweets.df <- parseTweets("tweets.json", simplify = FALSE) # parse the json file and save to a data frame called tweets.df. Simplify = FALSE ensures that we include lat/lon information in that data frame.

