{
library(ggplot2) #load library
library(dplyr) #load library
setwd("/home/eebc177student/Developer/repos/eeb-c177-project/analyses")
final_data <- read.csv("final_data.csv")
names(final_data) <- tolower(names(final_data)) #lowercase column titles
final_data <- as.data.frame(final_data) #make dataframe
names(final_data) <- gsub(x = names(final_data), pattern = "a\\.1", replacement = "b") #rename badly named column titles
names(final_data) <- gsub(x = names(final_data), pattern = "\\.", replacement = " ")  #remove period in column titles
final_data$group <- tolower(final_data$group) #make values in 'group' column lowercase
rank <- tolower(readline(prompt = 'Do you want ranks for "disease" or "funding"?: ')) #ask user if they want a chart for disease rank or funding rank 
}

if (rank == 'disease') { #if user selected 'disease': 
  parliament <- filter(final_data, group == tolower('parliament')) #take data matching demographic 'parliament' 
  parliament <- select(parliament, ends_with('a')) #selecting columns 'states of being' that are disease rank responses since they end in 'a'
  names(parliament) <- gsub(x = names(parliament), pattern = "a$", replacement = "") #remove the 'a'
  doctor <- filter(final_data, group == tolower('doctor')) #take data matching demographic 'doctor'
  doctor <- select(doctor, ends_with('a'))
  names(doctor) <- gsub(x = names(doctor), pattern = "a$", replacement = "")
  nurse <- filter(final_data, group == tolower('nurse')) #take data matching demographic 'nurse'
  nurse <- select(nurse, ends_with('a'))
  names(nurse) <- gsub(x = names(nurse), pattern = "a$", replacement = "")
  layperson <- filter(final_data, group == tolower('layperson')) #take data matching demographic 'layperson'
  layperson <- select(layperson, ends_with('a'))
  names(layperson) <- gsub(x = names(layperson), pattern = "a$", replacement = "")
  
  
  par_mean <- colMeans(parliament) #take means for each 'state of being' ranked by this demographic
  doc_mean <- colMeans(doctor)
  nur_mean <- colMeans(nurse)
  lay_mean <- colMeans(layperson)
  
  lay_mean <- as.data.frame(lay_mean) #make layperson means and states of being into a datafram
  
  lay_mean$nurse <- nur_mean #add nurse means to dataframe
  lay_mean$doctor <- doc_mean #add doctor means to dataframe
  lay_mean$parliament <- par_mean #add parliament means to dataframe
  
  means <- as.data.frame(lay_mean) #rename dataframe as means
  
  df <- tibble::rownames_to_column(means, "VALUE") #'states of being' to column
  
  library(reshape2) #load lbrary
  df <- melt(df, id.vars="VALUE") #stack a set of columns into a single column of data
  
  p = ggplot(data=df, aes(x=VALUE,y=value,fill=variable)) + #states of being on x axis, ranks on x axis, group means as bars 
    geom_bar(position="dodge",stat="identity") + 
    coord_flip() + labs(y= "Mean Rank (1-5)", x = "States of Being") + scale_fill_discrete(name = "Demographic", labels = c("Layperson", "Nurse", "Doctor", "Parliament")) + #flip graph so bar plots run horizontal and add titles
    theme(plot.title = element_text(hjust = 0.5)) +
    ggtitle("Mean Demographic Ranks: Ranking 'States of Being' as Diseases")
  plot(p)
  
} else if (rank == 'funding') { #do this if user asked for funding
  parliament <- filter(final_data, group == tolower('parliament')) #take data matching demographic 'parliament'
  parliament <- select(parliament, ends_with('b')) #selecting columns 'states of being' that are funding rank responses since they end in 'b'
  names(parliament) <- gsub(x = names(parliament), pattern = "b$", replacement = "") #remove the 'b'
  doctor <- filter(final_data, group == tolower('doctor'))
  doctor <- select(doctor, ends_with('b'))
  names(doctor) <- gsub(x = names(doctor), pattern = "b$", replacement = "")
  nurse <- filter(final_data, group == tolower('nurse'))
  nurse <- select(nurse, ends_with('b'))
  names(nurse) <- gsub(x = names(nurse), pattern = "b$", replacement = "")
  layperson <- filter(final_data, group == tolower('layperson'))
  layperson <- select(layperson, ends_with('b'))
  names(layperson) <- gsub(x = names(layperson), pattern = "b$", replacement = "")
  
  
  par_mean <- colMeans(parliament)
  doc_mean <- colMeans(doctor)
  nur_mean <- colMeans(nurse)
  lay_mean <- colMeans(layperson)
  
  lay_mean <- as.data.frame(lay_mean)
  
  lay_mean$nurse <- nur_mean
  lay_mean$doctor <- doc_mean
  lay_mean$parliament <- par_mean
  
  means <- as.data.frame(lay_mean)
  
  df <- tibble::rownames_to_column(means, "VALUE")
  
  library(reshape2)
  df <- melt(df, id.vars="VALUE")
  
  p = ggplot(data=df, aes(x=VALUE,y=value,fill=variable)) +
    geom_bar(position="dodge",stat="identity") + 
    coord_flip() + labs(y= "Mean Rank (1-5)", x = "States of Being") + scale_fill_discrete(name = "Demographic", labels = c("Layperson", "Nurse", "Doctor", "Parliament")) +
    theme(plot.title = element_text(hjust = 0.5)) +
    ggtitle("Mean Demographic Ranks: Ranking 'States of Being' as Warranting Public Funding")
  plot(p)
} else { #if 'funding' or 'disease' not inputted
  print("please enter 'disease' or 'funding'") #print error message
}

