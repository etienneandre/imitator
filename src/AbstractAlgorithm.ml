(************************************************************
 *
 *                       IMITATOR
 *
 * Université de Lorraine, CNRS, Inria, LORIA, Nancy, France
 *
 * Module description: Mode and algorithms for IMITATOR
 *
 * File contributors : Étienne André, Dylan Marinho
 * Created           : 2019/12/18
 * Last modified     : 2021/07/08
 *
 ************************************************************)


(************************************************************)
(** Internal modules *)
(************************************************************)
open Exceptions


(************************************************************)
(** Available translations *)
(************************************************************)

type translation =
	| HyTech
	| IMI
	| DOT
	| JPG
	| PDF
	| PNG
	| TikZ
	| Uppaal
  | JaniSpec


(************************************************************)
(** Synthesis *)
(************************************************************)


(** Mode for IMITATOR *)
type imitator_mode =
	(** No analysis, syntactic check only *)
	| Syntax_check

	(** Translation to another language: no analysis *)
	| Translation of translation

	(** Full state space exploration, until fully explored or some preliminary termination *)
	| State_space_computation

	(** Synthesis algorithm *)
	| Algorithm (*of synthesis_algorithm*)



(************************************************************)
(** Options *)
(************************************************************)

type distribution_mode =
	(** Normal mode *)
	| Non_distributed

	(** Distributed mode: static distribution mode (each node has its own part with no communication) *)
	| Distributed_static

	(** Distributed mode: Master slave with sequential pi0 *)
	| Distributed_ms_sequential
	(** Distributed mode: Master slave with sequential pi0 shuffled *)
	| Distributed_ms_shuffle
	(** Distributed mode: Master slave with random pi0 and n retries before switching to sequential mode *)
	| Distributed_ms_random of int
	(** Distributed mode: Master slave with subpart distribution *)
	| Distributed_ms_subpart

	(**  Distributed mode: Workers live their own lives and communicate results to the coordinator  **)
	| Distributed_unsupervised
	(**  Distributed mode: multi-threaded version of Distributed_unsupervised  **)
	| Distributed_unsupervised_multi_threaded


type exploration_order =
	(** Layer-BFS: all states at depth i are computed, and then their successors at depth i+1 [original version] *)
	| Exploration_layer_BFS
	(** Queue-BFS: basic queue, independent of the depth [ANP17] *)
	| Exploration_queue_BFS
	(** Queue-BFS: queue-based, independent of the depth, with ranking system for the selection of the next state [ANP17] *)
	| Exploration_queue_BFS_RS
	(** Queue-BFS: queue-based, independent of the depth, with prior for the selection of the next state [ANP17] *)
	| Exploration_queue_BFS_PRIOR
(*	(** NDFS: standard Nested Depth-First Search **)
	| Exploration_NDFS
	(** NDFSsub: NDFS with subsumption [NPvdP18] **)
	| Exploration_NDFS_sub
	(** layerNDFS: NDFS with layers [NPvdP18] **)
	| Exploration_layer_NDFS
	(** layerNDFSsub: NDFS with subsumption  and layers [NPvdP18] **)
	| Exploration_layer_NDFS_sub*)

type pending_order =
	(** NDFS with layers: order in the pending list exploration **)
	(* no particular order *)
	| Pending_none
	(* biggest parametric projection of zone first *)
	| Pending_param
	(* accepting states first *)
	| Pending_accept
	(* biggest zone first *)
	| Pending_zone

(* Merging heuristic for EFsynthminpq *)
type merge_heuristic =
	(** Merge_always: merge after every processed state *)
	| Merge_always
	(** Merge_always: merge after every processed state for which the target state is a successor of the current state *)
	| Merge_targetseen
	(** Merge_always: merge after every processed state, for every 10th added state to PQ *)
	| Merge_pq10
	(** Merge_always: merge after every processed state, for every 100th added state to PQ *)
	| Merge_pq100
	(** Merge_always: merge after every 10th processed state *)
	| Merge_iter10
	(** Merge_always: merge after every 100th processed state *)
	| Merge_iter100

(* Undefined value for n1/n2 merge heuristics *)
let undefined_merge_n = -1

(* Merge heuristics for reachability analysis *)
type merge_algorithm =
	(** None *)
	| Merge_none
	(** TODO: description *)
	| Merge_static
	(** TODO: description *)
	| Merge_exponentialbackoff


(** Style of graphical state space to output *)
type graphical_state_space =
	(* No graphical state space *)
	| Graphical_state_space_none
	(* State space with state numbers only*)
	| Graphical_state_space_nodetails
	(* State space with state numbers and locations *)
	| Graphical_state_space_normal
	(* State space with state numbers, locations, constraints and parameter constraints *)
	| Graphical_state_space_verbose


type cycle_algorithm =
	(* Standard BFS algorithm using a variant of Tarjan's strongly connected components algorithm *)
	| BFS
	(* NDFS based algorithm [NPvdP18] *)
	| NDFS


(** Infinite-run (cycle) with non-Zeno assumption: method *)
type nz_method =
	(** Method by checking whether the PTA is already a CUB-PTA for some valuation *)
	| NZ_check

	(** Method by transforming the PTA into a CUB-PTA *)
	| NZ_transform

	(** Method assuming the PTA is already a CUB-PTA *)
	| NZ_already


(************************************************************)
(** Check when adding a new state *)
(************************************************************)
type state_comparison_operator =
	(* Does not check whether the state is present, add directly *)
	| No_check
	(* Does not add the new state if another state is exactly equal to it *)
	| Equality_check
	(* Does not add the new state if it is included in (i.e., is smaller than) another state *)
	| Inclusion_check
	(* Does not add the new state if it includes (i.e., is larger than) another state *)
	| Including_check
	(* Does not add the new state if it is included in another state, or if another state is included into the current state (in which case the new state replaces the old one in the state space) *)
	| Double_inclusion_check




(************************************************************)
(** Predicates on mode *)
(************************************************************)

(* Does the algorithm require a second (property) file in addition to the model? *)
type second_file_need =
	| Second_file_required
	| Second_file_optional
	| Second_file_useless

let property_needed = function
	| Syntax_check
	| State_space_computation
		-> Second_file_useless

	| Translation _
		-> Second_file_optional

	| Algorithm
		-> Second_file_required


let cartography_drawing_possible = function
	| Syntax_check
	| State_space_computation
	| Translation _
		-> false
	| Algorithm (*of synthesis_algorithm*)
		-> true


(************************************************************)
(** Conversions of modes to string *)
(************************************************************)

let string_of_translation = function
	| HyTech -> "HyTech"
	| IMI    -> "IMITATOR"
	| DOT    -> "DOT"
	| JPG    -> "JPG"
	| PDF    -> "PDF"
	| PNG    -> "PNG"
	| TikZ   -> "TikZ"
	| Uppaal -> "Uppaal"
  | JaniSpec -> "JaniSpec"


let string_of_mode (imitator_mode : imitator_mode) : string = match imitator_mode with
	(** No analysis, syntactic check only *)
	| Syntax_check -> "syntax check"

	(** Translation to another language: no analysis *)
	| Translation translation -> "translation to " ^ (string_of_translation translation)

	(** Translation to another language: no analysis *)
	| State_space_computation -> "full symbolic state space exploration "

	(** Synthesis algorithm *)
	| Algorithm (*synthesis_algorithm*) -> "algorithm" (*** TODO: not so precise! ***)



let string_of_exploration_order (exploration_order : exploration_order) : string = match exploration_order with
	(** Layer-BFS: all states at depth i are computed, and then their successors at depth i+1 [original version] *)
	| Exploration_layer_BFS -> "layer-based BFS"
	(** Queue-BFS: basic queue, independent of the depth [ANP17] *)
	| Exploration_queue_BFS -> "queue-based BFS [ACN17]"
	(** Queue-BFS: queue-based, independent of the depth, with ranking system for the selection of the next state [ANP17] *)
	| Exploration_queue_BFS_RS -> "queue-based BFS with ranking system [ACN17]"
	(** Queue-BFS: queue-based, independent of the depth, with prior for the selection of the next state [ANP17] *)
	| Exploration_queue_BFS_PRIOR -> "queue-based BFS with priority [ACN17]"
	(** NDFS: standard Nested Depth-First Search **)
(*	| Exploration_NDFS -> "standard NDFS [NPvdP18]"
	(** NDFSsub: NDFS with subsumption [NPvdP18] **)
	| Exploration_NDFS_sub -> "NDFS with subsumption [NPvdP18]"
	(** layerNDFS: NDFS with layers [NPvdP18] **)
	| Exploration_layer_NDFS -> "NDFS with layers [NPvdP18]"
	(** layerNDFSsub: NDFS with subsumption  and layers [NPvdP18] **)
	| Exploration_layer_NDFS_sub -> "NDFS with subsumption and layers [NPvdP18]"*)


let string_of_cycle_algorithm (cycle_algorithm : cycle_algorithm) : string = match cycle_algorithm with
	| BFS  -> "BFS"
	| NDFS -> "NDFS"


let string_of_state_comparison_operator (state_comparison_operator : state_comparison_operator) : string = match state_comparison_operator with
	(* Does not check whether the state is present, add directly *)
	| No_check -> "no check"
	(* Does not add the new state if another state is exactly equal to it *)
	| Equality_check -> "equality check"
	(* Does not add the new state if it is included in (i.e., is smaller than) another state *)
	| Inclusion_check -> "inclusion check"
	(* Does not add the new state if it includes (i.e., is larger than) another state *)
	| Including_check -> "including check"
	(* Does not add the new state if it is included in another state, or if another state is included into the current state (in which case the new state replaces the old one in the state space) *)
	| Double_inclusion_check -> "double inclusion check"


let string_of_merge_algorithm (merge_algorithm : merge_algorithm) : string = match merge_algorithm with
	| Merge_none				-> "no merge"
	| Merge_static				-> "static"
	| Merge_exponentialbackoff	-> "exponential backoff"
