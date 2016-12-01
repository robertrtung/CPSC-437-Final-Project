consumerKey = "JmaomcAzFt7hKPNfS98NvQ"
consumerSecret = "4-ZNGbGD18oKjUSnL2n9Bth-QJo"
token = "hpbsaWY87YYNRYpr2gSH6eVyo9mhH_ZJ"
token_secret = "TZfgmUZq3gIx5vFmEwyaMrf_7yU"

v3Token = "ZGCZLBa1pDe2UEMQ3JOJeGmLAetgCetLV0kb5DnlwXvXhupuWQgRqRKkfJ8VNh-R2ce1UeOT44vGm_IFBxxa4u6dA2JdLr3845yHSR4Pf5dZwtyIMWXk-Tg_5h0_WHYx"

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
  output <- data.frame(ID=NA, Name=unlist(temp$businesses.name), Rating=unlist(temp$businesses.rating), 
                       Price=NA, Latitude=temp$businesses.location$coordinate$latitude, Longitude=temp$businesses.location$coordinate$longitude)
  ids <- unlist(temp$businesses.id)
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