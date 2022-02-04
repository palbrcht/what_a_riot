
###
###  Loading required packages.
###

library(tidyverse)
library(ggplot2)
library(scales)

###
###  Clearing working environment.
###

rm(list = ls())

###
###  Loading data from CSV.
###
###  TODO: get into postgresql
###

training_data_import <- read.csv("INSERT_PATH_HERE")

###
###  Some operationalization of data.
###

analysis_data <- training_data_import %>%
  mutate(grade_S = as.factor(ifelse((manualGrade == 'S' | manualGrade == 'S+' | manualGrade == 'S-') , 'S', 'Not S'))) %>%
  mutate(deaths_per_minute = (deaths / (timePlayed/60))) %>%
  mutate(fewer_than_5_dpm = as.factor(ifelse(deaths_per_minute < 0.2, 1, 0)))

only_pyke <- analysis_data %>%
  filter(championName == 'Pyke')

###
###  Create a plot for highlighting pyke performance
###
###  VERY rudimentary
###

gg_pyke <- ggplot(only_pyke, aes(x=(timePlayed/60), y=goldEarned, color = grade_S, label = paste(deaths , ' deaths.'))) +
  geom_point(aes(size = deaths)) +
  theme_bw() +
  geom_line(linetype = 'dashed') +
  geom_smooth(method = 'loess') +
  geom_text(vjust = -1, size = 2) +
  labs(title="Getting S with Pyke Support.. Oversimplified",
       x ="Game Minutes", 
       y = "Gold Earned" , 
       subtitle= '51 Obs; February 4, 2022',
       caption = 'Donate your screenshots today!') +
  #theme(legend.title=element_blank()) +
  #annotate("text", x = 25, y = 20000, label = "(Data point labels indicate deaths; deaths per minute.)") +
  scale_x_continuous(limits=c(20, 44), breaks=seq(20,44,2)) +
  scale_y_continuous(limits=c(5000, 23000), breaks=seq(5000,23000,1000), label = comma)

gg_pyke 

ggsave('pyke_support_s.png' , gg_pyke, width = 10, height = 6)

