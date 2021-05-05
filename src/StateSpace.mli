(************************************************************
 *
 *                       IMITATOR
 *
 * Laboratoire Spécification et Vérification (ENS Cachan & CNRS, France)
 * Université Paris 13, LIPN, CNRS, France
 *
 * Module description: Description of the symbolic states and of the state space
 *
 * File contributors : Étienne André, Dylan Marinho
 * Created           : 2009/12/08
 * Last modified     : 2021/05/05
 *
 ************************************************************)


(************************************************************)
(* Modules *)
(************************************************************)
open Automaton
open State
open AbstractAlgorithm


(************************************************************)
(** Type definitions *)
(************************************************************)

(** A combined transition is a list of transitions (one for each automaton involved) *)
type combined_transition = AbstractModel.transition_index list


(************************************************************)
(** Functions independent from state space *)
(************************************************************)

(** Get the (unique) action associated with a combined_transition *)
val get_action_from_combined_transition : combined_transition -> action_index


(************************************************************)
(** Nature of a state space (according to some property) *)
(************************************************************)
type statespace_nature =
	| Good
	| Bad
	| Unknown



(************************************************************)
(** Result of the function adding a new state *)
(************************************************************)
type addition_result =
	(* Completely new state *)
	| New_state of state_index
	(* State already present (possibly included depending on options), returns the old state index *)
	| State_already_present of state_index
	(* The new state replaced a former state (because the newer is larger), returns the old state index *)
	| State_replacing of state_index



(************************************************************)
(** Concrete run *)
(************************************************************)

type concrete_step = {
	(* First let time elapse *)
	time			: NumConst.t;
	(* Then take a discrete transition *)
	transition		: combined_transition;
	(* Then reach the target state *)
	target			: State.concrete_state;
}

(*** WARNING: the structure is here initial state followed by (transition, state) list, but in symbolic_run, it is (state, transition) followed by final state :( ***)

type concrete_run = {
	(* The parameter valuation for which this run exists *)
	p_valuation		: PVal.pval;
	(* The initial concrete state *)
	initial_state	: State.concrete_state;
	(* A possibly empty list of steps *)
	steps			: concrete_step list;
}


(************************************************************)
(** Impossible concrete run *)
(************************************************************)

(* An impossible concrete run is a run that starts with a concrete run prefix, and then follows by taking transitions NOT admissible in the state space. Transitions may be imaginary, but locations remain existing locations. *)

type impossible_concrete_step = {
	(* First let time elapse *)
	time			: NumConst.t;
	(* Then take a discrete transition *)
	action			: Automaton.action_index;
	(* Then reach the target state *)
	target			: State.concrete_state;
}

type impossible_concrete_run = {
	(* The parameter valuation for which this run exists *)
	p_valuation		: PVal.pval;
	(* The initial concrete state *)
	initial_state	: State.concrete_state;
	(* A possibly empty list of steps *)
	steps			: concrete_step list;
	(* A non-empty list of imaginary steps *)
	impossible_steps: impossible_concrete_step list;
}



(************************************************************)
(** Symbolic run in a state space *)
(************************************************************)

(*** WARNING: the structure is here (state, transition) followed by final state, but in concrete_run, it is initial state followed by (transition, state) list :( ***)

type symbolic_step = {
	source			: State.state_index;
	transition		: combined_transition;
}

type symbolic_run = {
	symbolic_steps	: symbolic_step list;
	final_state		: State.state_index;
}




(************************************************************)
(** Predecessors table *)
(************************************************************)
type predecessors_table = ((combined_transition * state_index) list) array


(************************************************************)
(** State space structure *)
(************************************************************)
type state_space

(** An SCC is just a list of states *)
type scc = state_index list


(************************************************************)
(** State space creation *)
(************************************************************)

(** Create a fresh state space *)
val make : int -> state_space


(************************************************************)
(** Interrogation on a state space *)
(************************************************************)

(*------------------------------------------------------------*)
(** Return the number of generated states (not necessarily present in the state space) *)
(*------------------------------------------------------------*)
val get_nb_gen_states : state_space -> int

(*------------------------------------------------------------*)
(** Return the number of states in a state space *)
(*------------------------------------------------------------*)
val nb_states : state_space -> int

(*------------------------------------------------------------*)
(** Return the number of transitions in a state space *)
(*------------------------------------------------------------*)
val nb_transitions : state_space -> int

(*------------------------------------------------------------*)
(** Return the global_location corresponding to a location_index *)
(*------------------------------------------------------------*)
val get_location : state_space -> Location.global_location_index -> Location.global_location

(*------------------------------------------------------------*)
(** Return the state of a state_index *)
(*------------------------------------------------------------*)
val get_state : state_space -> state_index -> state

(*------------------------------------------------------------*)
(** return the list of states with the same location (modulo hash collisions) *)
(*------------------------------------------------------------*)
val get_comparable_states : state_space -> state_index -> state_index list

(*------------------------------------------------------------*)
(** Return the global_location_index of a state_index *)
(*------------------------------------------------------------*)
val get_global_location_index : state_space -> state_index -> Location.global_location_index

(*------------------------------------------------------------*)
(** Return the index of the initial state, or raise Not_found if not defined *)
(*------------------------------------------------------------*)
val get_initial_state_index : state_space -> state_index

(*------------------------------------------------------------*)
(** Compte and return the list of index successors of a state *)
(*------------------------------------------------------------*)
val get_successors : state_space -> state_index -> state_index list

(*------------------------------------------------------------*)
(** Compte and return the list of pairs (index successor of a state, corresponding combined_transition) *)
(*------------------------------------------------------------*)
val get_successors_with_combined_transitions : state_space -> state_index -> (combined_transition * state_index) list


(*------------------------------------------------------------*)
(** Compte and return the list of pairs (index successor of a state, corresponding action) *)
(*------------------------------------------------------------*)
(* val get_successors_with_actions : state_space -> state_index -> (state_index * action_index) list *)

(*------------------------------------------------------------*)
(** Compute and return a predecessor array state_index -> (combined_transition , state_index) list *)
(*------------------------------------------------------------*)
val compute_predecessors_with_combined_transitions : state_space -> predecessors_table

(*------------------------------------------------------------*)
(** Return the table of transitions *)
(*------------------------------------------------------------*)
val get_transitions_table : state_space -> (state_index , ((combined_transition * state_index) list)) Hashtbl.t

(*------------------------------------------------------------*)
(** Return the list of all state indexes *)
(*------------------------------------------------------------*)
val all_state_indexes : state_space -> state_index list

(*------------------------------------------------------------*)
(** Test if state index is in the current statespace *)
(*------------------------------------------------------------*)
val test_state_index : state_space -> state_index -> bool

(*------------------------------------------------------------*)
(*** WARNING: big memory, here! Why not perform intersection on the fly? *)
(** Return the list of all constraints on the parameters associated to the states of a state space *)
(*------------------------------------------------------------*)
val all_p_constraints : state_space -> LinearConstraint.p_linear_constraint list

(** Returns the intersection of all parameter constraints, thereby destroying all constraints *)
(* val compute_k0_destructive : abstract_model -> state_space -> LinearConstraint.linear_constraint *)

(*------------------------------------------------------------*)
(** Check if two states are equal *)
(*------------------------------------------------------------*)
val states_equal: state -> state -> bool

(*------------------------------------------------------------*)
(** Check dynamically if two states are equal, i.e., if the first one + constraint equals second one + constraint *)
(*------------------------------------------------------------*)
val states_equal_dyn: state -> state -> LinearConstraint.px_linear_constraint -> bool

(*(** Test if a state exists satisfying predicate s *)
val exists_state: (state -> bool) -> state_space -> bool

(** test if all states satisfy predicate s *)
val forall_state: (state -> bool) -> state_space -> bool*)

(*------------------------------------------------------------*)
(** Find all "last" states on finite or infinite runs *)
(*------------------------------------------------------------*)
val last_states: AbstractModel.abstract_model -> state_space -> state_index list

(** Check if bad states are reached *)
(* val is_bad: abstract_model -> state_space -> bool *)



(*------------------------------------------------------------*)
(* Get the (full) guard associated with a transition *)
(*------------------------------------------------------------*)
val get_guard : state_space -> state_index -> combined_transition -> state_index -> LinearConstraint.pxd_linear_constraint

(*** NOTE: the function only works for regular resets (it raises NotImplemented for other updates) ***)
val get_resets : state_space -> state_index -> combined_transition -> state_index -> Automaton.clock_index list


(*------------------------------------------------------------*)
(* When a state is encountered for a second time, then a loop exists (or more generally an SCC): 'reconstruct_scc state_space state_index' reconstructs the SCC from state_index to state_index (using the actions) using a variant of Tarjan's strongly connected components algorithm; returns None if no SCC found *)
(*------------------------------------------------------------*)
val reconstruct_scc : state_space -> state_index -> scc option

(*------------------------------------------------------------*)
(** From a set of states, return all transitions within this set of states, in the form of a triple (state_index, combined_transition, state_index) *)
(*------------------------------------------------------------*)
val find_transitions_in : state_space -> scc -> (state_index * combined_transition * state_index) list


(*------------------------------------------------------------*)
(** Returns the symbolic run (list of pairs (state, combined transition)) from the source_state_index to the target_state_index. Can take a predecessors_table as an option, otherwise recomputes it from the state space. The list of transitions is ordered from the initial state to the target state; the target state is not included. Raise Not_found if run not found. *)
(*------------------------------------------------------------*)
val backward_symbolic_run : state_space -> state_index -> state_index -> predecessors_table option -> symbolic_run


(************************************************************)
(** Actions on a state space *)
(************************************************************)

(** Increment the number of generated states (even though not member of the state space) *)
val increment_nb_gen_states : state_space -> unit

(** Add a state to a state space: takes as input the state space, a comparison instruction, the state to add, and returns whether the state was indeed added or not *)
val add_state : state_space -> AbstractAlgorithm.state_comparison_operator -> state -> addition_result

(**Add a state to a state space dynamically**)
(* val add_state_dyn : AbstractModel.abstract_model -> state_space -> state -> LinearConstraint.linear_constraint -> (state_index * bool) *)

(** Add a transition to the state space *)
val add_transition : state_space -> (state_index * combined_transition * state_index) -> unit

(** Add a p_inequality to all the states of the state space *)
(*** NOTE: it is assumed that the p_constraint does not render some states inconsistent! ***)
val add_p_constraint_to_states : state_space -> LinearConstraint.p_linear_constraint -> unit


(** Replace the constraint of a state in a state space by another one (the constraint is copied to avoid side-effects later) *)
(* val replace_constraint : state_space -> LinearConstraint.linear_constraint -> state_index -> unit *)

(* Merges states in queue with states in state space. Removes unreachable states. Returns unmerged part of queue *)
val merge : state_space -> state_index list -> state_index list
(* Merge of v2.12 (ULRICH) *)
val merge212 : state_space -> state_index list -> state_index list

(** Empties the hash table giving the set of states for a given location; optimization for the jobshop example, where one is not interested in comparing  a state of iteration n with states of iterations < n *)
val empty_states_for_comparison : state_space -> unit

(** Iterate over the reachable states (with possible side effects) *)
val iterate_on_states : (state_index -> abstract_state -> unit) -> state_space -> unit




(************************************************************)
(** Misc: conversion to string *)
(************************************************************)
val string_of_state_index : state_index -> string

val string_of_statespace_nature : statespace_nature -> string


(************************************************************)
(** Debug and performances *)
(************************************************************)
(** Get statistics on states *)
val get_statistics_states : state_space -> string
