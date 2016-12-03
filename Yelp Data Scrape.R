
#API keys not included in script
#import libraries
library(httr)
library(httpuv)
library(jsonlite)

#' 
#' @description Function to pull and clean data from Yelp v2 and v3 Fusion APIs
#' @param term - what you want to search for (e.g. Chinese)
#' @param location - where you are (e.g. New Haven)
#' @param limit - number of results to return
#' @param offset- offset to get around API rate limit
yelp_scrape <- function(term, location, limit=40, offset = 0) {
  #establish oauth for Yelp v2 API
  myapp <- oauth_app("YELP", key=consumerKey, secret=consumerSecret)
  sig <- sign_oauth1.0(myapp, token=token, token_secret=token_secret)
  
  #create query
  yelpurl <- "https://api.yelp.com/v2/search/"
  results <- GET(yelpurl, sig, query=list(term=term, location=location, limit=limit, offset=offset))

  #extract pulled data
  extractResults = content(results)
  resultsList=jsonlite::fromJSON(toJSON(extractResults))
  temp <- data.frame(resultsList)
  
  #initalize data frame
  output <- data.frame(ID=NA, Name=unlist(temp$businesses.name), Rating=unlist(temp$businesses.rating), 
                       Price=NA, Latitude=unlist(temp$businesses.location$coordinate$latitude), 
                       Longitude=unlist(temp$businesses.location$coordinate$longitude))
  ids <- unlist(temp$businesses.id)
  
  #extract price and ID for each restaurant pulled
  for(i in 1:nrow(output)){
    output$ID[i] <- i+offset
    res <- GET(paste("https://api.yelp.com/v3/businesses/", ids[i], sep=""), add_headers(Authorization=paste("Bearer", v3Token)))
    extractRes = content(res)
    Sys.sleep(.1)
    price <- length(extractRes$price)
    if(price > 0) {
      output$Price[i] <- price
    }
  }
  return(output)
}