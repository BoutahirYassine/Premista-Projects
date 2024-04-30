library(dplyr)
library(stringr)
library(rjson)

load('back-database/produitDB')
source(file = "utils.R")
# source(file = "back-database/database.R")
# source(file = "back-database/requete.R")
#load('back-database/produitDB')


#' @apiTitle Retourne les tresorerie
#' @apiDescription retourne un max et un min
#'
#' @param revenu:numeric revenu complet du ménage
#' @param crd_conso:numeric Montant restant des crédits à la consommation
#' @param crd_immo:numeric Montant restant des crédits immobiliers
#' @param mensualite_conso:numeric Montant des mensualites à la consommation
#' @param mensualite_immo:numeric Montant des mensualites immobiliers
#' @param charges:numeric Montant des autres charges
#' @param nb_personne_dans_le_foyer:int Nombre de personnes dans le foyer : Enfant + Emprunteur +Co emprunteur
#' @param typologie_dossier:string proprietaire ou locataire
#' @param montant_a_financer:numeric Montant à financer
#'
#' @serializer unboxedJSON
#' @get /tresoreriepremista
function(res, req, revenu,
         crd_conso ,mensualite_conso,
         crd_immo  ,mensualite_immo,
         charges , nb_personne_dans_le_foyer,
         typologie_dossier, montant_a_financer) {
  # print(res)
  # message("hi")
  # print(req$QUERY_STRING)
  CHAMPS_OBLIGATOIRE <- c("\\brevenu","crd_conso","crd_immo","charges",
                          "mensualite_conso","mensualite_immo",
                          "nb_personne_dans_le_foyer","typologie_dossier",
                          "montant_a_financer\\b")
  CHAMPS_OBLIGATOIRE <- paste(CHAMPS_OBLIGATOIRE, collapse = '\\b|\\b')
  # print(CHAMPS_OBLIGATOIRE)
  requete <- unlist(stringr::str_split(req$QUERY_STRING, "&"))
  if(length(requete)==0){
    return(getMessageError(CHAMPS_OBLIGATOIRE, msg = "Des champs sont non recus", res = res))
  }else{
    if(length(grep(CHAMPS_OBLIGATOIRE, requete)) != 9){
      return(getMessageError(CHAMPS_OBLIGATOIRE, msg = "Des champs sont non recus", res = res))
    }
  }

  if(checkIfNull(revenu)){
    return(getMessageError(revenu, msg = " ", res = res))
  }
  if(checkIfNull(crd_conso)){
    return(getMessageError(crd_conso, msg = " ", res = res))
  }
  if(checkIfNull(crd_immo)){
    return(getMessageError(crd_immo, msg = " ", res = res))
  }
  if(checkIfNull(mensualite_conso)){
    return(getMessageError(mensualite_conso, msg = " ", res = res))
  }
  if(checkIfNull(mensualite_immo)){
    return(getMessageError(mensualite_immo, msg = " ", res = res))
  }
  if(checkIfNull(charges)){
    return(getMessageError(charges, msg = " ", res = res))
  }
  if(checkIfNull(nb_personne_dans_le_foyer)){
    return(getMessageError(nb_personne_dans_le_foyer, msg = " ", res = res))
  }

  if(checkIfNull(typologie_dossier)){
    return(getMessageError(typologie_dossier, msg = " ", res = res))
  }
  if(checkIfNull(montant_a_financer)){
    return(getMessageError(montant_a_financer, msg = " ", res = res))
  }
  if(!(typologie_dossier %in% c('proprietaire', 'locataire'))){
    return(getMessageError(typologie_dossier, msg = " proprietaire ou locataire uniquement ", res = res))
  }
  tryCatch({

    parametreEntant <- c(
      revenuTotal = revenu,
      crd_conso = crd_conso,mensualite_conso=mensualite_conso,
      crd_immo  = crd_immo,mensualite_immo=mensualite_immo,
      charges = charges, nb_personne_dans_le_foyer=nb_personne_dans_le_foyer,
      typologie_dossier=typologie_dossier, montant_a_financer=montant_a_financer,
      montant_treso=0,mensualiteCharge=sum(as.numeric(mensualite_conso),as.numeric(mensualite_immo), na.rm = TRUE)

    )
    # parametreEntant <- c(
    #   revenuTotal = 5000,
    #   crd_conso = 15000 ,mensualite_conso=200,
    #   crd_immo  = 20000,mensualite_immo=460,
    #   charges = 10, nb_personne_dans_le_foyer=2,
    #   typologie_dossier="proprietaire", montant_a_financer="300000",
    #   montant_treso=0,mensualiteCharge=sum(as.numeric(200),as.numeric(450), na.rm = TRUE)
    #
    # )
    # parametreEntant <- data.frame(parametreEntant)
    current <- getDataDF(parametreEntant)

    res <- parallel::mclapply(1:25, FUN = function(duree_max){

      current$duree_max <- (duree_max*12)
      current <- getRAVaUtiliser(current)
      current <- getTresoMaxCRD(current)
      current <- getMAFetRAVMaximum(current)
      current <- getCorrectMensualite(current)

      return(lapply(unique(current$type_produit), function(typeGarantie){
        currentDF <- dplyr::filter(current, type_produit==typeGarantie)
        currentDF <- dplyr::filter(currentDF, nouvelleMensualite>0)
        currentDF <- dplyr::filter(currentDF, tresoreriePossible>0)
        getRowMax <- dplyr::arrange(currentDF, desc(tresoreriePossibleMaximum),nouvelleMensualite, taux_nominal, duree_max)%>%
          dplyr::slice(1)
        return(list(`taux` = getRowMax$taux_nominal, `annee`= duree_max, `mensualite`=getRowMax$nouvelleMensualite,
                    `tresorerie` = getRowMax$tresoreriePossibleMaximum, `banque`=getRowMax$banque,
                    `montantEmpruntable`=getRowMax$nouvelleMAF,
                    typologie_produit =typeGarantie
        ))
      }))
      # return(current)

    },mc.cores = 7)
    # print(res)
    return(resultat =res)
  }, error = function(e) {
    message(paste0(e, " ", Sys.Date()))
    res$status = 400  # the response object that is always available in plumber functions
    res$body <- jsonlite::toJSON(auto_unbox = TRUE, list(
      status=400,
      message = paste0("Erreur constate " , e),
      date_heure = paste(Sys.Date(), Sys.time())
    ))
    # list(error=jsonlite::unbox( "Erreur constate"))
  })

}
