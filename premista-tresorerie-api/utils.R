#revenu chargeTotal nb_personne_dans_le_foyer

#' Calcul le RAV de l'emprunteur
#'
#' @param currentdf
#'
#' @return ravProduitAUtiliser
#'
#' @examples
getRAVaUtiliser <- function(currentdf){
  currentdf <- currentdf%>%
    dplyr::rowwise()%>%
    dplyr::mutate(ravProduitAUtiliser = dplyr::case_when(as.numeric(nb_personne_dans_le_foyer)==1 ~ as.numeric(reste_a_vivre1),
                                                         as.numeric(nb_personne_dans_le_foyer)==2 ~  as.numeric(reste_a_vivre2),
                                                         as.numeric(nb_personne_dans_le_foyer)==3 ~  as.numeric(reste_a_vivre3),
                                                         as.numeric(nb_personne_dans_le_foyer)==4 ~  as.numeric(reste_a_vivre4),
                                                         as.numeric(nb_personne_dans_le_foyer)==5 ~  as.numeric(reste_a_vivre5),
                                                         as.numeric(nb_personne_dans_le_foyer)>5 ~  as.numeric(reste_a_vivre5) + ((as.numeric(nb_personne_dans_le_foyer)-5)*  as.numeric(reste_a_vivre_supp)),
                                                         TRUE~as.numeric(0)))
}

#' Calcul du MAF maximum et RAV Maximum
#'
#' @param currentdf
#'
#' @return
#' @export
#'
#' @examples
getMAFetRAVMaximum<- function(currentdf){
  currentdf <- currentdf %>%
    dplyr::rowwise()%>%
    dplyr::mutate(mensualiteMaximum = ((as.numeric(endettement_apres_ac)/100) * as.numeric(revenuTotal))-sum(as.numeric(charges),as.numeric(mensualiteCharge), na.rm = TRUE),
                  mafMaximum =(mensualiteMaximum)*
                    (((1+((as.numeric(taux_nominal)/12)/100))^as.numeric(duree_max)) -1)/
                    (
                      ((as.numeric(taux_nominal)/12)/100)*((1+((as.numeric(taux_nominal)/12)/100))^as.numeric(duree_max))
                    ),
                  ravMaximum = as.numeric(revenuTotal) - sum(as.numeric(charges),as.numeric(mensualiteCharge),mensualiteMaximum, na.rm = TRUE)

    )
}


#' Récupère la liste des dossiers
#'
#' @return
#' @export
#'
#' @examples
getListProduits <- function(){
  # return(excuteRequeteMaria(getRequeteProduit()))
  load('back-database/produitDB')
  return(listProduit)
}

#' Recupération des informations
#'
#' @param parametre_entrant
#'
#' @return dataframe
#'
#' @examples
getDataDF <-  function(parametre_entrant){
  currentdf <- dplyr::bind_cols(
    getListProduits(),
    t(parametre_entrant)
  )

  currentdf <-dplyr::filter(currentdf, grepl(pattern = parametre_entrant['typologie_dossier'],x = type_dossier, ignore.case = TRUE))
  return(currentdf)
}

#' Récupère la dernière mensualité de montant maximum
#'
#' @param currentdf
#'
#' @return
#' @export
#'
#' @examples
getCorrectMensualite <- function(currentdf){
  res <- lapply(1:dim(currentdf)[1], function(i){
    row <- currentdf[i,]
    if(row$ravProduitAUtiliser>row$ravMaximum){
      row["nouvelleMensualite"] <- sum(as.numeric(row$revenuTotal) ,-as.numeric(row$ravProduitAUtiliser) ,-as.numeric(row$charges), -as.numeric(row$mensualiteCharge), na.rm = TRUE)
    }else{
      row["nouvelleMensualite"] <- row$mensualiteMaximum
    }
    row["nouvelleMAF"] <-(row$nouvelleMensualite)*
      (((1+((as.numeric(row$taux_nominal)/12)/100))^as.numeric(row$duree_max)) -1)/
      (
        ((as.numeric(row$taux_nominal)/12)/100)*((1+((as.numeric(row$taux_nominal)/12)/100))^as.numeric(row$duree_max))
      )
    # row['tmpMAF'] <-  sum(as.numeric(row$montant_a_financer), -as.numeric(row$montant_treso),na.rm = TRUE)
    row['tresoreriePossible'] <- sum(row$nouvelleMAF, -as.numeric(row$montant_a_financer), na.rm = TRUE)
    row['tresoreriePossibleMaximum'] <- getMinNotInf(c(as.numeric(row$maxTresorerie), row$tresoreriePossible))
    return(row)

  })
  return(as.data.frame(do.call(rbind,res)))

}


#' Récuperer la trésorerie max par produits
#'
#' @param current
#'
#' @return
#' @export
#'
#' @examples
getTresoMaxCRD <- function(current){
  current <- current %>%
    dplyr::rowwise()%>%
    dplyr::mutate(
      maxCRD = dplyr::if_else(as.numeric(datascience_treso_crd)==-1,
                              true = 0,
                              false = (sum(as.numeric(crd_conso),as.numeric(crd_immo),na.rm = TRUE) *as.numeric(datascience_treso_crd))/100),
      maxMAF = dplyr::if_else(as.numeric(datascience_treso_maf)==-1,
                              true = 0,
                              false = (as.numeric(montant_a_financer) *as.numeric(datascience_treso_maf))/100),
      maxTresorerie = getMinNotInf(c(as.numeric(maxCRD), as.numeric(maxMAF), as.numeric(datascience_treso_max)))

    )
  return(current)
}

getMinNotInf <- function(myvector){
  myvector <- myvector[myvector > 0]
  myvecto <- c()
  if(length(myvector)>0){
    myvecto  <- myvector

  } else{
    myvecto = c(0)
  }

  return(min(myvecto))
}

checkIfNull <- function(champs){
  if(is.null(champs)|
     is.na(champs)){
    return(TRUE)
  }else{
    return(FALSE)
  }
}


getMessageError <- function(champs, msg = NULL, res = NULL){
  message(paste("Le champs " , champs , "est recquis", Sys.Date(), Sys.time()) )
  if(is.null(res)){
    return(paste("Le champs " , champs , "est recquis", Sys.Date(), Sys.time()) )
  }
  res$status = 400  # the response object that is always available in plumber functions
  res$body <- jsonlite::toJSON(auto_unbox = TRUE, list(
    status=400,
    message = paste("Le champs " , champs , " est recquis ", Sys.Date(), Sys.time(), msg ),
  ))
}
