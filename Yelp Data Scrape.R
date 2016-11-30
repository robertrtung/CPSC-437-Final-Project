
library(httr)
library(httpuv)
library(jsonlite)

myapp = oauth_app("YELP", key=consumerKey, secret=consumerSecret)
sig=sign_oauth1.0(myapp, token=token,token_secret=token_secret)

########
yelp_scrape <- function(term, location, limit=40, offset = 0) {
  myapp <- oauth_app("YELP", key=consumerKey, secret=consumerSecret)
  sig <- sign_oauth1.0(myapp, token=token, token_secret=token_secret)
  
  yelpurl <- "https://api.yelp.com/v2/search/"
  results <- GET(yelpurl, sig, query=list(term=term, location=location, limit=limit, offset=offset))

  extractResults = content(results)
  resultsList=jsonlite::fromJSON(toJSON(extractResults))
  temp <- data.frame(resultsList)
  output <- data.frame(ID=NA, Name=unlist(temp[, 11]), Rating=unlist(temp[, 7]), 
                       Price=NA, Latitude=temp[, 23][[7]][1], Longitude=temp[, 23][[7]][2])
  ids <- unlist(temp[, 21])
  for(i in 1:nrow(output)){
    output$ID[i] <- i
    res <- GET(paste("https://api.yelp.com/v3/businesses/", ids[i], sep=""), add_headers(Authorization=paste("Bearer", v3Token)))
    extractRes = content(res)
    Sys.sleep(.1)
    output$Price[i] <- nchar(extractRes$price)
  }
  return(output)
}