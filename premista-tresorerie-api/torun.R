library(plumber)
pr <- plumber::plumb("/usr/scripts/premista-tresorerie-api/plumber.R")
# pr <- plumber::plumb("plumber.R")
pr$run(host='0.0.0.0', port = 8000, swagger = TRUE)

