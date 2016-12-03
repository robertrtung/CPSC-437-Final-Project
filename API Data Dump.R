library(RMySQL)
source("~/Documents/CPSC 437/Yelp Data Scrape.R")

#pull cleaned restaurant data
output <- yelp_scrape("restaurant", "new haven")
for(i in 1:24) {
  temp <- yelp_scrape("restaurant", "new haven", offset=40*i)
  print(names(temp))
  output <- rbind(output, temp)
  Sys.sleep(1)
}

#insert into MySQL
con <- dbConnect(MySQL(), 
                 user="root",
                 host="localhost",
                 dbname="yelp")
dbWriteTable(con, "Restaurant", output, 
             append=TRUE, overwrite=FALSE, row.names=FALSE)
dbDisconnect(con)
