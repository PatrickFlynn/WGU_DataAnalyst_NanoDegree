setwd("C:/Users/p15144f/Desktop/WGU_DataAnalyst_NanoDegree/03 - Data Analysis with R")
wine <- read.csv(file="wineQualityReds.csv",header=TRUE, sep=",")

library(ggplot2)
library(dplyr)
library(reshape2)

melted_matrix <- melt(round(cor(select(wine, -c("X"))),2))
ggplot(data=melted_matrix, aes(x=Var1, y=Var2, fill=value)) + 
    geom_tile() + scale_fill_gradient(low="yellow", high="red") +
    