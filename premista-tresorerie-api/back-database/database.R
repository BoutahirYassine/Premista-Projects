getConnectionMariaDatabase <- function() {
  return(
    RPresto::dbConnect(
      RMariaDB::MariaDB(),
      dbname = "financial_cf",
      host = "172.16.101.10",
      port = 3306,
      user = "datascience",
      password = "8fVrABXywCvmnuU3cPftu3qz",
    )
  )
}

excuteRequeteMaria <- function(requete) {
  connec <- getConnectionMariaDatabase()
  # print(connec)
  res <- RPresto::dbSendQuery(connec, requete)
  # data <- dbFetch(res, n = 200)
  data <-  data.frame()
  progress.bar <- NULL
  while(!RPresto::dbHasCompleted(res)){
    chunk <-RPresto::dbFetch(res, 10000)
    if (!nrow(data)) {
      data <- chunk
    } else if (nrow(chunk)) {
      data <- rbind(data, chunk)
    }
  }
  RPresto::dbClearResult(res)
  RPresto::dbDisconnect(connec)
  return(data)
}