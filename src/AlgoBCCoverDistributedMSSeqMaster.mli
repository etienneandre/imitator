(************************************************************
 *
 *                       IMITATOR
 * 
 * LIPN, Université Paris 13, Sorbonne Paris Cité (France)
 * 
 * Module description: Classical Behavioral Cartography with exhaustive coverage of integer points [AF10]. Distribution mode: master-slave with sequential distribution of points. [ACE14]
 * Master algorithm
 * 
 * File contributors : Étienne André
 * Created           : 2016/03/10
 * Last modified     : 2016/03/10
 *
 ************************************************************)


(************************************************************)
(* Modules *)
(************************************************************)


(************************************************************)
(* Class definition *)
(************************************************************)
class algoBCCoverDistributedMSSeqMaster :
	object
	inherit AlgoBCCoverDistributedMSPointBasedMaster.algoBCCoverDistributedMSPointBasedMaster
		(************************************************************)
		(* Class variables *)
		(************************************************************)


		(************************************************************)
		(* Class methods *)
		(************************************************************)
		method algorithm_name : string
		
		(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
		(** Return a new instance of the underlying cartography algorithm (typically BCrandom or BCcover) *)
		(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
		method bc_instance : AlgoCartoGeneric.algoCartoGeneric

end