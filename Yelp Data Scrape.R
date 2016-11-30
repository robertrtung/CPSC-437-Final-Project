consumerKey = "JmaomcAzFt7hKPNfS98NvQ"
consumerSecret = "4-ZNGbGD18oKjUSnL2n9Bth-QJo"
token = "hpbsaWY87YYNRYpr2gSH6eVyo9mhH_ZJ"
token_secret = "TZfgmUZq3gIx5vFmEwyaMrf_7yU"

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
  return(data.frame(resultsList))
}