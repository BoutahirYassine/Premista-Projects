#' Récuperer la requete pour toutes les informations du produit
#'
#' @return requete:String
#'
#'
#' @examples
getRequeteProduit <- function() {
  return(
    "
  select fb.libelle as banque, fpb.taux_nominal , fpb.duree_max ,fpb.type_produit,
fpb.reste_a_vivre1 ,fpb.reste_a_vivre2 ,fpb.reste_a_vivre3  ,fpb.reste_a_vivre4  ,fpb.reste_a_vivre5  ,
fpb.reste_a_vivre_supp  ,fpb.endettement_apres_ac, fpb.libelle as libelleProduit,
fpb.pourcentage_revenus_fonciers, fpb.pourcentage_apl,fpb.revenu_without_pension_versee,
fpb.montant_max_pro, fpb.montant_max_loc,
fpb.datascience_treso_max , fpb.datascience_treso_crd , fpb.datascience_treso_maf, fpb.type_dossier
from financial_cf.financial_produit_banque fpb
left join financial_banque fb on fb.id_banque = fpb.id_banque
where fpb.actif =1 and fb.libelle not in ('RÉMÉRÉ','LOCAFI','COFIDIS','BROOKEO')
         "
  )
}

