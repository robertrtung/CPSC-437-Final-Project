#import library for interfacing with SQLite
library(sqldf)

#establish connection with DB and import files
db <- dbConnect(SQLite(), dbname="restaurantPredictions.db", flags=SQLITE_RWC)
rest <- read.csv("restaurants.csv", as.is=TRUE)
lab <- read.csv("labels.csv", as.is=TRUE)

#write data to DB and check to make sure write was successful
dbWriteTable(conn=db, name="Restaurants", value=rest, row.names=FALSE)
dbWriteTable(conn=db, name="Labels", value=lab, row.names=FALSE)
dbReadTable(db, "Restaurants")
dbReadTable(db, "Labels")
dbListTables(db)
dbDisconnect(db)