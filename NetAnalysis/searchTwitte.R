api_key <-   "knDYepbodjYllFB52VkVXnvJh"
api_secret <-	"e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV"
access_token <-	"354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n"
access_token_secret <-	"8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK"

oauth_sig<- setup_twitter_oauth(api_key,api_secret,access_token,access_token_secret)
save(oauth_sig, file = "twitteR_oauth.Rdata")
