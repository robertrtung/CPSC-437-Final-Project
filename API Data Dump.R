library(RMySQL)
source("~/Documents/CPSC 437/Yelp Data Scrape.R")

output <- yelp_scrape("restaurant", "new haven")
for(i in 1:23) {
  temp <- yelp_scrape("restaurant", "new haven", offset=40*i)
  output <- rbind(output, temp)
}
con <- dbConnect(MySQL(), 
                 user="root",
                 host="localhost",
                 dbname="yelp")
dbWriteTable(con, "Restaurant", output, 
             append=TRUE, overwrite=FALSE, row.names=FALSE)
dbDisconnect(con)