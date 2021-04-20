(************************************************************
 *
 *                       IMITATOR
 *
 * Laboratoire Spécification et Vérification (ENS Cachan & CNRS, France)
 * Université Paris 13, LIPN, CNRS, France
 *
 * Module description: Description of the symbolic states and of the state space
 *
 * File contributors : Étienne André, Jaime Arias, Ulrich Kühne
 * Created           : 2009/12/08
 * Last modified     : 2021/04/20
 *
 ************************************************************)



(************************************************************)
(* Modules *)
(************************************************************)

open Exceptions
open OCamlUtilities
open ImitatorUtilities
open Statistics
open Automaton
open State
open AbstractModel
open AbstractAlgorithm



(************************************************************)
(** Nature of a state space according to some property *)
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
(** Transitions *)
(************************************************************)

(** A combined transition is a list of transitions (one for each automaton involved) *)
type combined_transition = AbstractModel.transition_index list


(************************************************************)
(** Predecessors table *)
(************************************************************)
type predecessors_table = ((combined_transition * state_index) list) array



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
(** Set of state index *)
(************************************************************)

(* state struct for constructing set type *)
module State = struct
	type t = state_index
	let compare = compare
end

(* set of states for efficient lookup *)
module StateIndexSet = Set.Make(State)



(************************************************************)
(** State space structure *)
(************************************************************)


type state_space = {
	(** The number of generated states (even not added to the state space) *)
	nb_generated_states : int ref;

	(** An Array 'state_index' -> 'State.abstract_state'; contains ALL states *)
	mutable all_states : (state_index, abstract_state) Hashtbl.t;

	(** The id of the initial state *)
	(*** NOTE: mutable due to the fact that the initial state can be merged with another state *)
	mutable initial : state_index option;

	(** A hashtable location -> location_index *)
	index_of_locations : (Location.global_location, location_index) Hashtbl.t;

	(** A DynArray location_index -> location *)
	locations : Location.global_location DynArray.t;

	(** A hashtable to quickly find states with identical locations (? ; made by Ulrich); only for states to be compared *)
        (* modified by Jaco van de Pol: use global_location_index as key, rather than hash code of global_location *)
	mutable states_for_comparison : (location_index, state_index) Hashtbl.t;

	(** A HashTable state_index -> list of (combined_transition * 'target_state_index') *)
	mutable transitions_table : (state_index , (combined_transition * state_index) list) Hashtbl.t;

	(** An integer that remembers the next index of state_index (may not be equal to the number of states, if states are removed *)
	next_state_index : state_index ref;
}


(** An SCC is just a list of states *)
type scc = state_index list


(************************************************************)
(** Statistics *)
(************************************************************)
(*let nb_state_comparisons = ref 0
let nb_constraint_comparisons = ref 0*)
let statespace_dcounter_nb_state_comparisons = create_discrete_counter_and_register "number of state comparisons" States_counter Verbose_standard
let statespace_dcounter_nb_constraint_comparisons = create_discrete_counter_and_register "number of constraints comparisons" States_counter Verbose_standard

(* Numbers of new states that were in fact included into an old state *)
let statespace_dcounter_nb_states_included = create_discrete_counter_and_register "number of new states <= old" States_counter Verbose_standard
(* Numbers of new states that were in fact larger than an old state *)
let statespace_dcounter_nb_states_including = create_discrete_counter_and_register "number of new states >= old" States_counter Verbose_standard

(* Numbers of merging attempts (for states that have the same discrete location) *)
let nb_merging_attempts = create_discrete_counter_and_register "StateSpace.merging attempts" States_counter Verbose_standard
(* Numbers of actual merges *)
let nb_merged = create_discrete_counter_and_register "StateSpace.merges" States_counter Verbose_standard

(* Complete time for merging *)
let tcounter_merge = create_time_counter_and_register "StateSpace.Merge time" States_counter Verbose_standard
(* Complete time for state space reconstruction while merging *)
let tcounter_merge_statespace = create_time_counter_and_register "StateSpace.Merge (reconstruct state space)" States_counter Verbose_standard

(* Functions *)
let counter_add_state = create_hybrid_counter_and_register "StateSpace.add_state" States_counter Verbose_experiments
let counter_compute_predecessors_with_combined_transitions = create_hybrid_counter_and_register "StateSpace.compute_predecessors" States_counter Verbose_experiments
let counter_get_location = create_hybrid_counter_and_register "StateSpace.counter_get_location" States_counter Verbose_experiments
let counter_get_state = create_hybrid_counter_and_register "get_state" States_counter Verbose_experiments

let counter_add_transition = create_hybrid_counter_and_register "StateSpace.add_transition" States_counter Verbose_experiments
let counter_get_successors = create_hybrid_counter_and_register "StateSpace.get_successors" States_counter Verbose_experiments
(* let counter_get_successors_with_actions = create_hybrid_counter_and_register "StateSpace.get_successors_with_actions" States_counter Verbose_experiments *)
let counter_get_transitions = create_hybrid_counter_and_register "StateSpace.get_transitions" States_counter Verbose_experiments
let counter_nb_states = create_hybrid_counter_and_register "StateSpace.nb_states" States_counter Verbose_experiments
let counter_nb_transitions = create_hybrid_counter_and_register "StateSpace.nb_transitions" States_counter Verbose_experiments
let counter_empty_states_for_comparison = create_hybrid_counter_and_register "StateSpace.empty_states_for_comparison" States_counter Verbose_experiments

(*
	(* Statistics *)
	counter_xx#increment;
	counter_xx#start;
	(* Statistics *)
	counter_xx#stop;
*)


(************************************************************)
(** Local exception *)
(************************************************************)
exception Found_cycle


(************************************************************)
(** Debug string function *)
(************************************************************)
let string_of_state_index state_index = "s_" ^ (string_of_int state_index)


(************************************************************)
(** State space creation *)
(************************************************************)

(** Create a fresh state space *)
let make guessed_nb_transitions =
	(* Create a Hashtbl : state_index -> (location_index, linear_constraint) for the reachable states *)
	let states = Hashtbl.create Constants.guessed_nb_states_for_hashtable in
	(* Create a hashtable : location -> location_index for the locations *)
	let index_of_locations = Hashtbl.create Constants.guessed_nb_states_for_hashtable in
	(* Create a DynArray : location_index -> location for the locations *)
	let locations = DynArray.make Constants.guessed_nb_states_for_hashtable in
	(* Create an empty lookup table : hash -> state_index *)
	let states_for_comparison = Hashtbl.create Constants.guessed_nb_states_for_hashtable in
	(* Create a hashtable for the state space *)
	let transitions_table = Hashtbl.create guessed_nb_transitions in

	print_message Verbose_high ("Creating empty state space with an initial guessed number of " ^ (string_of_int Constants.guessed_nb_states_for_hashtable) ^ " state" ^ (s_of_int Constants.guessed_nb_states_for_hashtable) ^ " and " ^ (string_of_int guessed_nb_transitions) ^ " transition" ^ (s_of_int guessed_nb_transitions) ^ ".");

	(* Create the state space *)
	{
		nb_generated_states   = ref 0;
		all_states            = states;
		initial               = None;
		index_of_locations    = index_of_locations;
		locations             = locations;
		states_for_comparison = states_for_comparison;
		transitions_table     = transitions_table;
		next_state_index      = ref 0;
	}


(************************************************************)
(** Interrogation on a state space *)
(************************************************************)

(** Return the number of generated states (not necessarily present in the state space) *)
let get_nb_gen_states state_space =
	!(state_space.nb_generated_states)

(** Return the number of states in a state space *)
let nb_states state_space =

	(* Statistics *)
	counter_nb_states#increment;
	counter_nb_states#start;

	let result =
		Hashtbl.length state_space.all_states
	in

	(* Statistics *)
	counter_nb_states#stop;

	result



(** Return the number of transitions in a state space *)
let nb_transitions state_space =
	(* Statistics *)
	counter_nb_transitions#increment;
	counter_nb_transitions#start;

	let result =
		Hashtbl.fold (fun _ current_transitions current_nb ->
			current_nb + (List.length current_transitions)
		) state_space.transitions_table 0
	in

	(* Statistics *)
	counter_nb_transitions#stop;

	result


(* Return the global_location corresponding to a location_index *)
let get_location state_space location_index =
	(* Statistics *)
	counter_get_location#increment;
	counter_get_location#start;

	let result =
		DynArray.get state_space.locations location_index
	in

	(* Statistics *)
	counter_get_location#stop;

	result


(** Return the state of a state_index *)
let get_state state_space state_index =
	(* Statistics *)
	counter_get_state#increment;
	counter_get_state#start;

	(* Find the state *)
	let state =
		(* Exception just in case *)
		try (
			Hashtbl.find state_space.all_states state_index
		) with Not_found -> raise (InternalError ("State of index `" ^ (string_of_int state_index) ^ "` was not found in state_space (in function: get_state)."))
	in

	(* Find the pair (location_index, constraint) *)
	let location_index, linear_constraint = state.global_location_index, state.px_constraint in

	(* Find the location *)
	let global_location = get_location state_space location_index in

	(* Statistics *)
	counter_get_state#stop;

	(* Return the state *)
	{ global_location = global_location; px_constraint = linear_constraint; }


(** Return the global_location_index of a state_index *)
let get_global_location_index state_space state_index =
	(* Statistics *)
	counter_get_state#increment;
	counter_get_state#start;

	(* Find the location_index *)
	let location_index =
		(* Exception just in case *)
		try (
			(Hashtbl.find state_space.all_states state_index).global_location_index
		) with Not_found -> raise (InternalError ("State of index `" ^ (string_of_int state_index) ^ "` was not found in state_space (in function: StateSpace.get_global_location_index)."))
	in

	(* Statistics *)
	counter_get_state#stop;

	(* Return the location_index *)
	location_index

(** return the list of states with the same location *)
let get_comparable_states state_space state_index =
        let location_index = get_global_location_index state_space state_index in
        Hashtbl.find_all state_space.states_for_comparison location_index


(** Return the index of the initial state, or raise Not_found if not defined *)
let get_initial_state_index state_space =
	match state_space.initial with
	| Some state_index -> state_index
	| None -> raise Not_found



(** Return the table of transitions *)
let get_transitions_table state_space =

	(* Statistics *)
	counter_get_transitions#increment;
	counter_get_transitions#start;

	let result =
		state_space.transitions_table
	in

	(* Statistics *)
	counter_get_transitions#stop;

	result


(** Compte and return the list of pairs (combined transition, index successor of a state) (if entry undefined in the hashtable, then []) *)
let get_successors_with_combined_transitions state_space state_index =
	(* Get all successors with their combined transition *)
	hashtbl_get_or_default state_space.transitions_table state_index []


(** Compte and return the list of index successors of a state (if entry undefined in the hashtable, then []) *)
let get_successors state_space state_index =
	(* Statistics *)
	counter_get_successors#increment;
	counter_get_successors#start;

	(*** NOTE: we get all pairs "transition , target", then we keep the second elements, i.e., the target state indexes ***)
	let _ , target_state_indices = List.split (get_successors_with_combined_transitions state_space state_index) in

	(* We eliminate duplicates *)
	let result = list_only_once target_state_indices in

	(* Statistics *)
	counter_get_successors#stop;

	result


(** Get all combined transitions from a state_index *)
let get_transitions_of_state state_space state_index =
	(* Print some information *)
	print_message Verbose_total ("Entering StateSpace.get_transitions_of_state");

	let transitions_and_targets = get_successors_with_combined_transitions state_space state_index in

	let result , _ = List.split transitions_and_targets in

	(* The end *)
	result


(** Get the (unique) action associated with a combined_transition (if entry undefined in the hashtable, then []) *)
let get_action_from_combined_transition combined_transition =
	(* Retrieve the model *)
	let model = Input.get_model() in
	(* The action is the same for any transition of a combined_transition, therefore pick up the first one *)
	let action_index =
	try (
		(* Get the first transition *)
		let first_transition_index = List.nth combined_transition 0 in
		(* Get the actual transition *)
		let transition = model.transitions_description first_transition_index in
		(* Get the action index *)
		transition.action
	) with Failure msg -> raise (InternalError ("Empty list of transitions in a combined_transition found in get_action_from_combined_transition, although this should not have been the case: `" ^ msg ^ "`."))
	in
	action_index


(*(** Compte and return the list of pairs (index successor of a state, corresponding action) (if entry undefined in the hashtable, then []) *)
let get_successors_with_actions state_space state_index =
	(* Statistics *)
	counter_get_successors_with_actions#increment;
	counter_get_successors_with_actions#start;

	(* Get all successors with their combined transition *)
	let transitions_and_successors = get_successors_with_combined_transitions state_space state_index in

	(* Transform to pair (target state index, action index) *)
	let result = List.map (fun (combined_transition , target_state_index) ->
		(* Get the action_index *)
		let action_index = get_action_from_combined_transition combined_transition in
		(* Create pair *)
		target_state_index , action_index
	) transitions_and_successors in

(*	(* We eliminate duplicates *)
	let result = list_only_once target_state_indices in*)
	(*** TODO: ??? ***)

	(* Statistics *)
	counter_get_successors_with_actions#stop;

	result*)



(*------------------------------------------------------------*)
(** Compute and return a predecessor array state_index -> (combined_transition , state_index) list *)
(*------------------------------------------------------------*)
let compute_predecessors_with_combined_transitions state_space : predecessors_table =

	(* Statistics *)
	counter_compute_predecessors_with_combined_transitions#increment;
	counter_compute_predecessors_with_combined_transitions#start;

	(* Print some information *)
	print_message Verbose_total "Computing predecessors…";

	(* Get the highest id of the state space *)
	(*** NOTE: we get the highest id and not the length of the Hashtbl due to the fact that states may be merged/removed by bidirectional inclusion ***)
	let highest_id = !(state_space.next_state_index) - 1 in

	(* Print some information *)
	print_message Verbose_total ("Creating an array of length " ^ (string_of_int (highest_id + 1)) ^ "");

	(* Create an array for predecessors: state_index -> (state_index, action_index) list *)
	let predecessors = Array.make (highest_id + 1) [] in

	(* Iterate on all states in the state space *)
	Hashtbl.iter(fun source_state_index _ ->
		(* Print some information *)
		print_message Verbose_total ("Retrieving successors of state #" ^ (string_of_int source_state_index));

		(* Get all successors of this state *)
		let successors = hashtbl_get_or_default state_space.transitions_table source_state_index [] in

		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total ("Successors of state #" ^ (string_of_int source_state_index) ^ ": " ^ (string_of_list_of_string_with_sep "," (List.map (fun (_, state_index) -> string_of_int state_index) successors)));
		);

		(* Iterate on pairs (combined_transition * 'target_state_index') *)
		List.iter (fun (combined_transition, target_state_index) ->

			(* Print some information *)
			if verbose_mode_greater Verbose_total then(
				print_message Verbose_total ("Adding #" ^ (string_of_int source_state_index) ^ " to the predecessors of #" ^ (string_of_int target_state_index) ^ "");
			);

			(* Add to the predecessor array *)
			Array.set predecessors target_state_index (
				(* Add the new element *)
				(combined_transition , source_state_index)
				(* to *)
				::
				(* the former list *)
				predecessors.(target_state_index)
				)
			;

			(* Print some information *)
			if verbose_mode_greater Verbose_total then(
				print_message Verbose_total ("Predecessors of #" ^ (string_of_int target_state_index) ^ " now: " ^ (string_of_list_of_string_with_sep "," (List.map (fun (_, state_index) -> string_of_int state_index) predecessors.(target_state_index))));
			);

		) successors;


	) state_space.all_states;

	(* Statistics *)
	counter_compute_predecessors_with_combined_transitions#stop;

	(* Return structure *)
	predecessors


(** Return the list of all state indexes *)
let all_state_indexes state_space = hashtbl_get_all_keys state_space.all_states
(*let all_state_indexes state_space =
	Hashtbl.fold
		(fun state_index _ current_list ->
			state_index :: current_list)
		state_space.all_states []*)

(** Test if state index is in the current statespace *)
let test_state_index state_space state_index = Hashtbl.mem state_space.all_states state_index


(*** WARNING: big memory, here! Why not perform intersection on the fly? *)

(** Return the list of all constraints on the parameters associated to the states of a state space *)
let all_p_constraints state_space =
	Hashtbl.fold
		(fun _ state current_list ->
			let p_constraint = LinearConstraint.px_hide_nonparameters_and_collapse state.px_constraint in
			p_constraint :: current_list)
		state_space.all_states []



(** Iterate over the reahable states *)
let iterate_on_states f state_space =
	Hashtbl.iter f state_space.all_states


(*(** Compute the intersection of all parameter constraints, DESTRUCTIVE!!! *)
(** HERE PROBLEM IF ONE WANTS TO COMPUTE THE states FILE AFTER **)
let compute_k0_destructive program state_space =
	let k0 = LinearConstraint.true_constraint () in
	iterate_on_states (fun _ (_, constr) ->
		LinearConstraint.hide_assign program.clocks_and_discrete constr;
		LinearConstraint.px_intersection_assign k0 [constr];

	) state_space;
	k0*)

(** find all "last" states on finite or infinite runs *)
(* Uses a depth first search on the reachability state_space. The *)
(* prefix of the current DFS path is kept during the search *)
(* in order to detect cycles. *)
let last_states model state_space =
	(* list to keep the resulting last states *)
	let last_states = ref [] in
	(* Table to keep all states already visited during DFS *)
	let dfs_table = ref StateIndexSet.empty in

	(* functional version for lookup *)
	let already_seen node = StateIndexSet.mem node !dfs_table in

	(* function to find all last states *)
	let rec cycle_detect node prefix =
		(* get all successors of current node *)
		let succs = get_successors state_space node in
		if succs = [] then
			(* no successors -> last node on finite path *)
			last_states := node :: !last_states
		else (
			(* insert node in DFS table *)
			dfs_table := StateIndexSet.add node !dfs_table;
			(* go on with successors *)
			List.iter (fun succ ->
				(* successor in current path prefix (or self-cycle)? *)
				if succ = node || StateIndexSet.mem succ prefix then
					(* found cycle *)
					last_states := succ :: !last_states
				else if not (already_seen succ) then
					(* go on recursively on newly found node *)
					cycle_detect succ (StateIndexSet.add node prefix)
			) succs;
		) in

	(* start cycle detection with initial state *)
	cycle_detect 0 StateIndexSet.empty;

	(* return collected last states *)
	!last_states


(*exception Satisfied

(** Checks if a state exists that satisfies a given predicate *)
let exists_state p state_space =
		try (
			iter (fun s ->
				if p s then raise Satisfied
			) state_space;
			false
		) with Satisfied -> true

(** Checks if all states satisfy a given predicate *)
let forall_state p state_space =
		try (
			iter (fun s ->
				if not (p s) then raise Satisfied
			) state_space;
			true
		) with Satisfied -> false	*)



(*(** Check if bad states are reachable *)
let is_bad program state_space =
	(* get bad state pairs from program *)
	let bad_states = program.bad in
	(* if no bad state specified, then must be good *)
	if bad_states = [] then false else (
		let is_bad_state = fun (location, _) ->
			List.for_all (fun (aut_index, loc_index) ->
				loc_index = Location.get_location location aut_index
			) bad_states in
		exists_state is_bad_state state_space
	) *)


(*------------------------------------------------------------*)
(** Access to guard and resets *)
(*------------------------------------------------------------*)

let get_guard state_space state_index combined_transition state_index' =
	(* Retrieve the model *)
	let model = Input.get_model () in

	(* Retrieve source and target locations *)
	let (location : Location.global_location) = (get_state state_space state_index).global_location in

	(* For all transitions involved in the combined transition *)
	let continuous_guards : LinearConstraint.pxd_linear_constraint list = List.fold_left (fun current_list_of_guards transition_index ->
		(* Get the actual transition *)
		let transition : AbstractModel.transition = model.transitions_description transition_index in

		(* Add the actual guard to the list *)
		match transition.guard with
			| True_guard -> current_list_of_guards
			(*** NOTE: we could optimize the case of False (because no need to go further); BUT the number of transitions is usually small and, most importantly, it is unlikely a guard is false in the model ***)
			| False_guard -> (LinearConstraint.pxd_false_constraint()) :: current_list_of_guards
			| Discrete_guard discrete_guard -> current_list_of_guards
			| Continuous_guard continuous_guard -> continuous_guard :: current_list_of_guards
			| Discrete_continuous_guard discrete_continuous_guard -> discrete_continuous_guard.continuous_guard :: current_list_of_guards

	) [] combined_transition
	in

	(* Replace with true if empty list *)
	let continuous_guards = if continuous_guards = [] then [LinearConstraint.pxd_true_constraint()] else continuous_guards in

	(*** NOTE (ÉA, 2019/05/30): Not sure what I did there??? ***)
	(* Compute constraint for assigning a (constant) value to discrete variables *)
	print_message Verbose_high ("Computing constraint for discrete variables");
	let discrete_values = List.map (fun discrete_index -> discrete_index, (Location.get_discrete_value location discrete_index)) model.discrete in

	(* Only use rational discrete values for preparing constraint, this behavior was checked with Etienne A. *)
	let only_discrete_rational_values = List.filter (fun (discrete_index, discrete_value) -> DiscreteValue.is_rational_value discrete_value) discrete_values in
	let discrete_rational_numconst_values = List.map (fun (discrete_index, discrete_value) -> discrete_index, DiscreteValue.numconst_value discrete_value) only_discrete_rational_values in

	(* Constraint of the form D_i = d_i *)
	let discrete_constraint = LinearConstraint.pxd_constraint_of_point discrete_rational_numconst_values in

	(* Create the constraint guard ^ D_i = d_i *)
	LinearConstraint.pxd_intersection (discrete_constraint :: continuous_guards)


(*** NOTE: the function only works for regular resets (it raises NotImplemented for other updates) ***)
(*** TODO: allow for all resets ***)
let get_resets state_space state_index combined_transition state_index' =
	(* Retrieve the model *)
	let model = Input.get_model () in

	(* For all transitions involved in the combined transition *)
	let resets = List.fold_left (fun current_resets transition_index ->
		(* Get the actual transition *)
		let transition = model.transitions_description transition_index in

		(*** WARNING: we only accept clock resets (no arbitrary updates) ***)
		match transition.updates.clock with
			(* No update at all *)
			| No_update -> current_resets
			(* Reset to 0 only *)
			| Resets clock_resets -> List.rev_append clock_resets current_resets
			(* Reset to arbitrary value (including discrete, parameters and clocks) *)
			| Updates _ -> raise (NotImplemented "Only clock resets are allowed for now in StateSpace.get_resets")
	) [] combined_transition
	in

	(* Keep each clock once *)
	list_only_once resets


(************************************************************)
(** SCC detection *)
(************************************************************)

(*** NOTE: this part is heavily based on the Tarjan's strongly connected components algorithm, as presented on Wikipedia, with some mild modification:
	- the top level algorithm is run once only (as we start from a state which we know belongs to the desired SCC)
	- the other SCCs are discarded
***)

(* Data structure: node with index / lowlink / onStack *)
type tarjan_node = {
	(* Additional field used to record the real state_index in the state space *)
	state_index	: state_index;
	mutable index		: state_index option;
	mutable lowlink		: state_index option;
	mutable onStack		: bool;
}

(* Exception raised when the SCC is found *)
exception Found_scc of scc


(* When a state is encountered for a second time, then a loop exists (or more generally an SCC): 'reconstruct_scc state_space source_state_index' reconstructs the SCC from source_state_index to source_state_index (using the actions) using a variant of Tarjan's strongly connected components algorithm; returns None if no SCC found *)
(*** NOTE: added the requirement that a single node is not an SCC in our setting ***)
let reconstruct_scc state_space source_state_index : scc option =
	(* Print some information *)
	print_message Verbose_high ("Entering reconstruct_scc " ^ (string_of_state_index source_state_index) ^ "…");

	(* Variables used for Tarjan *)
	let current_index = ref 0 in

	(* Hashtable state_index -> tarjan_node *)
	let tarjan_nodes = Hashtbl.create Constants.guessed_nb_states_for_hashtable in

	(* tarjan_node stack *)
	let stack = Stack.create () in

	(* Get the tarjan_node associated with a state_index; create it if not found in the Hashtable *)
	let tarjan_node_of_state_index state_index =
		(* If present in the hashtable already *)
		if Hashtbl.mem tarjan_nodes state_index then(
			Hashtbl.find tarjan_nodes state_index
		)else(
			(* Create an empty node *)
			let tarjan_node = {
				state_index = state_index;
				index		= None;
				lowlink		= None;
				onStack		= false;
			} in
			(* Add it *)
			Hashtbl.add tarjan_nodes state_index tarjan_node;
			(* Return it *)
			tarjan_node
		)
	in

	(* Get the index field from a tarjan_node; raise InternalError if index = None *)
	let get_index tarjan_node =
		match tarjan_node.index with
			| Some ll -> ll
			| _ -> raise (InternalError "v.index should not be undefined at that point")
	in

	(* Get the lowlink field from a tarjan_node; raise InternalError if lowlink = None *)
	let get_lowlink tarjan_node =
		match tarjan_node.lowlink with
			| Some ll -> ll
			| _ -> raise (InternalError "v.lowlink should not be undefined at that point")
	in


	(* Define a main local, recursive function *)
	let rec strongconnect state_index =
		(* Print some information *)
		print_message Verbose_high ("  Entering strongconnect " ^ (string_of_state_index state_index) ^ "…");

		(* Get the associated tarjan node *)
		let v = tarjan_node_of_state_index state_index in
		(* Set the depth index for v to the smallest unused index *)
		(*v.index := index*)
		v.index <- Some !current_index;

		(*v.lowlink := index*)
		v.lowlink <- Some !current_index;

		(*index := index + 1*)
		incr current_index;

		(* S.push(v) *)
		Stack.push v stack;

		(* Print some information *)
		print_message Verbose_high ("  Push " ^ (string_of_state_index state_index) ^ "");

		(* v.onStack := true *)
		v.onStack <- true;

		(* Print some information *)
		print_message Verbose_high ("  Considering successors of " ^ (string_of_state_index state_index) ^ "…");

		(* Consider successors of v *)
		(* for each (v, w) in E do *)
		let successors = get_successors state_space state_index in

		(* Print some information *)
		if verbose_mode_greater Verbose_high then(
			print_message Verbose_high (string_of_list_of_string_with_sep ", " (List.map string_of_state_index successors));
		);

		List.iter (fun successor_index ->
			(* Print some information *)
			print_message Verbose_high ("    Considering successor " ^ (string_of_state_index successor_index) ^ "");

			let w = tarjan_node_of_state_index successor_index in
			(* if (w.index is undefined) then *)
			if w.index = None then (
			(* // Successor w has not yet been visited; recurse on it
				strongconnect(w) *)
				strongconnect successor_index;

				(* v.lowlink  := min(v.lowlink, w.lowlink) *)

				let vlowlink = get_lowlink v in
				let wlowlink = get_lowlink w in

				(* Print some information *)
				print_message Verbose_high ("    " ^ (string_of_state_index v.state_index) ^ ".lowlink  := min(" ^ (string_of_state_index v.state_index) ^ ".lowlink, " ^ (string_of_state_index w.state_index) ^ ".lowlink) = min(" ^ (string_of_int vlowlink) ^ ", " ^ (string_of_int wlowlink) ^ ")");

				if wlowlink < vlowlink then(
					v.lowlink <- Some wlowlink;
				);
			(* else if (w.onStack) then *)
			) else if w.onStack then (
				(* // Successor w is in stack S and hence in the current SCC
				v.lowlink  := min(v.lowlink, w.index) *)
				let vlowlink = get_lowlink v in
				let windex = get_index w in
				if windex < vlowlink then v.lowlink <- Some windex;
			(* end if *)
			);
		(* end for *)
		) successors;

		(* // If v is a root node, pop the stack and generate an SCC *)
		(* if (v.lowlink = v.index) then *)
		let vlowlink = get_lowlink v in
		let vindex = get_index v in

		if vlowlink = vindex then (
			(* Print some information *)
			print_message Verbose_high ("  Root node! Start SCC");

			(* start a new strongly connected component *)
			let scc : scc ref = ref [] in

			(* repeat *)
			let found_v = ref false in
			while not !found_v do
				(* w := S.pop() *)
				let w = Stack.pop stack in

				(* Print some information *)
				print_message Verbose_high ("  Pop " ^ (string_of_state_index w.state_index) ^ "");

				(* w.onStack := false *)
				w.onStack <- false;

				(* add w to current strongly connected component *)
				scc := w.state_index :: !scc;

				if w = v then found_v := true
			(* while (w <> v) *)
			done;

			(* output the current strongly connected component *)
			(* In fact, we differ from the traditional Tarjan here: if the original source_state_index belongs to the scc, we are done; otherwise we keep working and this scc is discarded *)
			if List.mem source_state_index !scc then(

				(* In addition, the SCC must not be reduced to a singleton without a loop *)
				if List.length !scc > 1 then(
					print_message Verbose_high ("  Found SCC of size > 1 containing " ^ (string_of_state_index source_state_index) ^ "!");

					raise (Found_scc !scc)
				)else(
					(* If reduced to a state: must contain a self-loop, i.e., source_state_index must belong to its successors *)
					let successors = get_successors state_space source_state_index in

					(* Print some information *)
					if verbose_mode_greater Verbose_high then(
						print_message Verbose_high ("  Successors of " ^ (string_of_state_index source_state_index) ^ ": " ^ (string_of_list_of_string_with_sep ", " (List.map string_of_state_index successors)) );
					);

					let found_scc = List.mem source_state_index successors in

					if found_scc then(
						(* Print some information *)
						print_message Verbose_high ("  Found SCC containing exactly " ^ (string_of_state_index source_state_index) ^ "!");

						raise (Found_scc !scc)
					)else(
						(* Print some information *)
						print_message Verbose_high ("  Found SCC containing exactly " ^ (string_of_state_index source_state_index) ^ " but without a loop: discard.");
					);
				);
			)else(
				(* Print some information *)
				print_message Verbose_high ("  SCC NOT containing " ^ (string_of_state_index source_state_index) ^ ": discard.");
			);
		(* end if *)
		);

		(* Print some information *)
		print_message Verbose_high ("  Exiting strongconnect " ^ (string_of_state_index state_index) ^ ".");

		(* end local function strongconnect *)
		()


	in

	(* Call strongconnect from the desired starting node *)
	let scc =
	try
		strongconnect source_state_index;

		(* If an exception was not raised, we reach this point *)
		print_message Verbose_high ("SCC not found in strongconnect!");
		None
	with
		(* if an exception was raised while looking for the SCC: we found the SCC! *)
		Found_scc scc -> (
			(* Return the scc *)
			Some scc
		)
	in
	(* Return SCC *)
	scc


(*------------------------------------------------------------*)
(** From a set of states, return all transitions within this set of states, in the form of a triple (state_index, combined_transition, state_index) *)
(*------------------------------------------------------------*)
let find_transitions_in state_space (scc : scc) : (state_index * combined_transition * state_index) list =
	List.fold_left (fun current_list state_index ->
		(* Compute the successors of state_index *)
		let successors = get_successors_with_combined_transitions state_space state_index in

		(* Filter only those who belong to the scc *)
		let successors_in_scc = List.filter (fun (_, state_index) -> List.mem state_index scc) successors in

		(* Convert into triple (state_index, combined_transition, state_index) *)
		let triples = List.map (fun (combined_transition , target_state_index) -> (state_index, combined_transition, target_state_index) ) successors_in_scc in

		(* Add them to the current list *)
		List.rev_append triples current_list
	) [] scc


(************************************************************)
(** Backward run-computation *)
(************************************************************)

(*------------------------------------------------------------*)
(** Table to color/mark states *)
(*------------------------------------------------------------*)
let colortable_create init_nb : ('a, bool) Hashtbl.t = Hashtbl.create init_nb

let mark colortable element =
	Hashtbl.replace colortable element true

let unmark colortable element =
	Hashtbl.replace colortable element false

let is_marked colortable element : bool =
	(*** NOTE: split the test in case OCaml does not evaluate the way we think it does ***)
	if not (Hashtbl.mem colortable element) then false
	else Hashtbl.find colortable element


(*------------------------------------------------------------*)
(** Returns the symbolic run (list of pairs (state, combined transition)) from the source_state_index to the target_state_index. Can take a predecessors_table as an option, otherwise recomputes it from the state space. The list of transitions is ordered from the initial state to the target state; the target state is not included. Raise Not_found if run not found. *)
(*------------------------------------------------------------*)

let backward_symbolic_run state_space (target_state_index : state_index) (source_state_index : state_index) (predecessors_table_option : predecessors_table option) : symbolic_run =
	(* First manage the predecessors_table *)
	let predecessors_table = match predecessors_table_option with
		(* If given: keep it *)
		| Some predecessors_table -> predecessors_table
		(* Otherwise: recompute *)
		| None -> compute_predecessors_with_combined_transitions state_space
	in

	(* Create a table to remember whether a state is marked or not *)
	(*** NOTE: use the number of states in the state space as default init ***)
	let colortable = colortable_create (nb_states state_space) in

	(* Function to sort the predecessors made of a pair of a combined_transition and a state_index *)
	let sort_predecessors = List.sort (fun (_, a) (_, b) -> compare a b) in

	(*------------------------------------------------------------*)
	(* Use a recursive procedure returning a (list of (state, combined transition))'option ; None denotes the current run is useless. The states are returned in reversed order. *)
	let rec backward_symbolic_run_rec current_state_index =
		(* If target is reached: return *)
		if current_state_index = source_state_index then Some [] (*** NOTE: do not add index, it will be added during the recursion together with the transition ***)

		(* If the state is marked, give up *)
		else if is_marked colortable current_state_index then None

		(* Else process this state *)
		else(
			(* Mark it! *)
			mark colortable current_state_index;

			(* Get the predecessors *)
			let predecessors = predecessors_table.(current_state_index) in

			(* Heuristics: test the predecessors by increasing state_index (intuitively, a smaller state_index may be closer to the initial state, hence should be tried first) *)
			let sorted_predecessors = sort_predecessors predecessors in

			(* Iterate on the predecessors *)
			let symbolic_steps = List.fold_left (fun current_steps (combined_transition, predecessor_index) ->
				(* If predecessor is marked: skip and go to next predecessor *)
				if is_marked colortable predecessor_index then current_steps

				(* If unmarked: call recursively *)
				else
				let recursive_result = backward_symbolic_run_rec predecessor_index in
				match recursive_result with
					(* If no result in this direction: skip and go to next predecessor *)
					| None -> current_steps
					(* Otherwise: return the result and add the symbolic_step *)
					| Some symbolic_steps -> Some ({source = predecessor_index ; transition = combined_transition } :: symbolic_steps)

			) None sorted_predecessors in

			match symbolic_steps with
				(* If no steps found after iterating, we are in a deadlock *)
				| None -> None
				(* Otherwise return (do NOT add current state, as it was added above) *)
				| Some symbolic_steps -> Some symbolic_steps
		)

	in
	(*------------------------------------------------------------*)

	(* Call the recursive procedure and reverse the result *)
	match backward_symbolic_run_rec target_state_index with
	(* Oops! *)
	| None -> raise Not_found
	| Some symbolic_steps ->
		(* Construct the structure symbolic_run *)
		{
			(* Reverse because states were added in reversed order *)
			symbolic_steps = List.rev symbolic_steps;
			(* Add final state *)
			final_state = target_state_index;
		}




(************************************************************)
(** Actions on a state space *)
(************************************************************)
(* Old state found *)
exception Found_old of state_index
(* State found that is smaller that the new one (in which case the old state will be replaced with the new one) *)
exception Found_new of state_index

(** Increment the number of generated states (even though not member of the state space) *)
let increment_nb_gen_states state_space =
	state_space.nb_generated_states := !(state_space.nb_generated_states) + 1


(** Check if two states are equal *)
let states_equal (state1 : state) (state2 : state) : bool =
	let (loc1, constr1) = state1.global_location, state1.px_constraint in
	let (loc2, constr2) = state2.global_location, state2.px_constraint in
	if not (Location.location_equal loc1 loc2) then false else (
		(* Statistics *)
		print_message Verbose_high ("About to compare equality between two constraints.");

		(* Statistics *)
		statespace_dcounter_nb_constraint_comparisons#increment;

		if verbose_mode_greater Verbose_high then(
			let nb_comparisons = statespace_dcounter_nb_constraint_comparisons#discrete_value in
			print_message Verbose_high ("Already performed " ^ (string_of_int nb_comparisons) ^ " constraint comparison" ^ (s_of_int nb_comparisons) ^ ".");
		);

		LinearConstraint.px_is_equal constr1 constr2
	)

(* Check dynamically if two states are equal*)
let states_equal_dyn (state1 : state) (state2 : state) constr : bool =
	let (loc1, constr1) = state1.global_location, state1.px_constraint in
	let (loc2, constr2) = state2.global_location, state2.px_constraint in
	if not (Location.location_equal loc1 loc2) then false else (
		(* Statistics *)
		print_message Verbose_high ("About to compare (dynamic) equality between two constraints.");

		(* Statistics *)
		statespace_dcounter_nb_constraint_comparisons#increment;

		if verbose_mode_greater Verbose_high then(
			let nb_comparisons = statespace_dcounter_nb_constraint_comparisons#discrete_value in
			print_message Verbose_high ("Already performed " ^ (string_of_int nb_comparisons) ^ " constraint comparison" ^ (s_of_int nb_comparisons) ^ ".");
		);

		(*** WARNING!!! Really sure that one wants do MODIFY the constraints here?!!! ***)
		LinearConstraint.px_intersection_assign constr1  [constr];
		LinearConstraint.px_intersection_assign constr2 [constr];
		LinearConstraint.px_is_equal constr1 constr2
	)


(** Check if a state is included in another one *)
(* (Despite the test based on the hash table, this is still necessary in case of hash collisions) *)
let state_included (state1 : state) (state2 : state) : bool =
	let (loc1, constr1) = state1.global_location, state1.px_constraint in
	let (loc2, constr2) = state2.global_location, state2.px_constraint in
	if not (Location.location_equal loc1 loc2) then false else (

		(* Statistics *)
		statespace_dcounter_nb_constraint_comparisons#increment;

		if verbose_mode_greater Verbose_high then(
			let nb_comparisons = statespace_dcounter_nb_constraint_comparisons#discrete_value in
			print_message Verbose_high ("Already performed " ^ (string_of_int nb_comparisons) ^ " constraint comparison" ^ (s_of_int nb_comparisons) ^ ".");
		);

		LinearConstraint.px_is_leq constr1 constr2
	)

let new_location_index state_space location =
        let new_index = try (
	Hashtbl.find state_space.index_of_locations location
) with Not_found -> (
(* If not found: add it *)
	(* Find new index *)
	let new_index = Hashtbl.length state_space.index_of_locations in
	(* Add to hash table *)
	Hashtbl.add state_space.index_of_locations location new_index;
	(* Add to Dyn Array *)
	DynArray.add state_space.locations location;
	(* Check length (COULD BE REMOVED) *)
	(* if DynArray.length state_space.locations <> Hashtbl.length state_space.index_of_locations then(
		raise (InternalError "Locations and index_of_locations seem not to be consistent anymore."); *)
        new_index;
	) in
	(* Return new index *)
	new_index

(** Perform the insertion of a new state in a state space *)
let insert_state state_space location_index (new_state : state) =
	(* Compute the new state index *)
	let new_state_index = !(state_space.next_state_index) in
	(* Retrieve the location and the constraint *)
	let location, linear_constraint = new_state.global_location, new_state.px_constraint in
(*	print_warning "warning: consistency check";
	(* Consistency check: the state should NOT be present (otherwise this is a duplicate) *)
	Hashtbl.iter (fun state_index _ ->
(* 		print_string "."; *)
		let state = get_state state_space state_index in
		if states_equal state new_state then(
			raise (InternalError "Trying to add a state that is present");
		);
	) state_space.all_states;*)


	(* Set the initial state if not yet set *)
	if state_space.initial = None then(
		print_message Verbose_low ("Initial state set in the reachability state_space.");
		state_space.initial <- Some new_state_index;
	);


	(* Add the state to the tables *)
	Hashtbl.add state_space.all_states new_state_index {global_location_index = location_index; px_constraint = linear_constraint;};
	Hashtbl.add state_space.states_for_comparison location_index new_state_index;
	(* Update next state index *)
	state_space.next_state_index := !(state_space.next_state_index) + 1;
	(* Return state_index *)
	new_state_index


(*(**** TO DO: merge with add_state !!! *)
(** Add a state to a state space, if it is not present yet with the on-the-fly intersection *)
let add_state_dyn program state_space new_state constr =
	(* Retrieve the input options *)
	let options = Input.get_options () in
	(* compute hash value for the new state *)
	let hash = location_hash_code new_state in
	if verbose_mode_greater Verbose_total then (
		print_message Verbose_standard ("hash : " ^ (string_of_int hash));
	);
	(* In tree mode: does not test anything *)
	if options#tree then (
		(* Since the state does NOT belong to the state space: find the state index *)
		let new_state_index = insert_state state_space hash new_state in
		(* Return state_index, true *)
		new_state_index, true
	) else (
		(* The check used for equality *)
		let check_states = states_equal_dyn in
		try (
			(* use hash table to find states with same locations (modulo hash collisions) *)
			let old_states = Hashtbl.find_all state_space.states_for_comparison hash in
			if verbose_mode_greater Verbose_total then (
				let nb_old = List.length old_states in
				print_message Verbose_total ("hashed list of length " ^ (string_of_int nb_old));
			);

			(* Statistics *)
			print_message Verbose_medium ("About to compare new state with " ^ (string_of_int (List.length old_states)) ^ " state(s).");
			nb_state_comparisons := !nb_state_comparisons + (List.length old_states);
			print_message Verbose_medium ("Already performed " ^ (string_of_int (!nb_state_comparisons)) ^ " comparisons.");

			List.iter (fun index ->
				let state = get_state state_space index in
				if check_states new_state state constr then raise (Found index)
			) old_states;
			(* Not found -> insert state *)
			let new_state_index = insert_state state_space hash new_state in
			(* Return state_index, true *)
			new_state_index, true
		)	with Found state_index -> (
				state_index, false
		)
	)*)


(** Replace the constraint of a state in a state space by another one (the constraint is copied to avoid side-effects later) *)
let replace_constraint state_space state_index px_linear_constraint =
	(* Copy to avoid side-effects *)
	let linear_constraint_copy = LinearConstraint.px_copy px_linear_constraint in
	try (
		(* Get the location index *)
		let location_index = (Hashtbl.find state_space.all_states state_index).global_location_index in
		(* Replace with the new constraint *)
		Hashtbl.replace state_space.all_states state_index {global_location_index = location_index; px_constraint = linear_constraint_copy};
	) with Not_found -> raise (InternalError ("Error when replacing state `" ^ (string_of_int state_index) ^ "` in StateSpace.replace_constraint."))



(** Add a state to a state space: takes as input the state space, a comparison instruction, the state to add, and returns whether the state was indeed added or not *)
let add_state state_space state_comparison (new_state : state) =
	(* Statistics *)
	counter_add_state#increment;
	counter_add_state#start;

	let result =

        let location_index = new_location_index state_space new_state.global_location in
	(* If no check requested: does not test anything *)
	if state_comparison = No_check then (
		(* Since the state does NOT belong to the state space: insert directly and find the state index *)
		let new_state_index = insert_state state_space location_index new_state in
		(* Return state_index  *)
		New_state new_state_index
	) else (
		try (
			(* use hash table to find all states with same locations*)
			let old_states = Hashtbl.find_all state_space.states_for_comparison location_index in
			if verbose_mode_greater Verbose_total then (
				let nb_old = List.length old_states in
				print_message Verbose_total ("The list of states with the same location has length " ^ (string_of_int nb_old));
			);

			(* Statistics *)
			print_message Verbose_medium ("About to compare new state with " ^ (string_of_int (List.length old_states)) ^ " old state" ^ (s_of_int (List.length old_states)) ^ ".");

(* 			statespace_dcounter_nb_state_comparisons#increment_by (List.length old_states); *)

(* 			nb_state_comparisons := !nb_state_comparisons + (List.length old_states); *)
			if verbose_mode_greater Verbose_medium then(
				let nb_comparisons = statespace_dcounter_nb_state_comparisons#discrete_value in
				print_message Verbose_medium ("Already performed " ^ (string_of_int nb_comparisons) ^ " state comparison" ^ (s_of_int nb_comparisons) ^ ".");
			);

			(* Iterate on each state *)
			List.iter (fun state_index ->
				let state = get_state state_space state_index in

				print_message Verbose_total ("Retrieved state #" ^ (string_of_int state_index) ^ ".");

				(* Branch depending on the check function used for state comparison *)
				match state_comparison with

					(* No_check: case considered above already *)
					| No_check -> raise (InternalError("Case `No_check` should have been handled before, in function StateSpace.add_state"))

					(* Equality: check for equality *)
					| Equality_check ->
						statespace_dcounter_nb_state_comparisons#increment;
						if states_equal new_state state then raise (Found_old state_index)

					(* Inclusion: check for new <= old *)
					| Inclusion_check ->
						statespace_dcounter_nb_state_comparisons#increment;
						if state_included new_state state then(
							(* Statistics *)
							statespace_dcounter_nb_states_included#increment;
							raise (Found_old state_index)
						)

					(* Inclusion: check for new >= old *)
					| Including_check ->
						statespace_dcounter_nb_state_comparisons#increment;
						if state_included state new_state then(
							(* Statistics *)
							statespace_dcounter_nb_states_including#increment;
							
							(* Check if equality, i.e., reverse direction *)
							if state_included new_state state then(
								(* Print some information *)
								print_message Verbose_medium ("Found an old state = the new state");
								
								(* Statistics *)
								statespace_dcounter_nb_states_included#increment;
								
								raise (Found_old state_index)
							)else(
								(* Print some information *)
								print_message Verbose_medium ("Found an old state < the new state");
								
								(* Replace old with new *)
								replace_constraint state_space state_index new_state.px_constraint;

								(* Stop looking for states *)
								raise (Found_new state_index)
							)
						)

					(* Double inclusion: check for new <= old OR old <= new, in which case replace *)
					| Double_inclusion_check ->
						(* First check: new <= old *)
						statespace_dcounter_nb_state_comparisons#increment;
						if state_included new_state state then(
							(* Statistics *)
							statespace_dcounter_nb_states_included#increment;
							raise (Found_old state_index)
						)
						(* Second check: old <= new *)
						else(
						statespace_dcounter_nb_state_comparisons#increment;
						if state_included state new_state then (
							(* Print some information *)
							print_message Verbose_medium ("Found an old state < the new state");

							(* Replace old with new *)
							replace_constraint state_space state_index new_state.px_constraint;

							(* Statistics *)
							statespace_dcounter_nb_states_including#increment;

							(* Stop looking for states *)
							raise (Found_new state_index)
						))

			) old_states;

			(* Not found -> insert state *)
			let new_state_index = insert_state state_space location_index new_state in

			(* Print some information *)
			print_message Verbose_total ("Inserted new state #" ^ (string_of_int new_state_index) ^ ".");

			(* Return *)
			New_state new_state_index
		)	with
			| Found_old state_index -> State_already_present state_index
			| Found_new state_index -> State_replacing state_index
	)

	in
	(* Statistics *)
	counter_add_state#stop;
	result


(** Add a combined transition to the state space *)
let add_transition state_space (source_state_index, combined_transition, target_state_index) =
	(* Statistics *)
	counter_add_transition#increment;
	counter_add_transition#start;

	(* Print some information *)
	print_message Verbose_total ("Entering StateSpace.add_transition");

	(* check if it already exists *)
	let transitions = get_transitions_of_state state_space source_state_index in

	(* Print some information *)
	print_message Verbose_total ("Existence check done");

	(*** TODO: it seems that getting the list is doing twice here; optimization? ***)
	if not (List.mem combined_transition transitions) then
		(** Add to the data structure *)
		Hashtbl.replace state_space.transitions_table source_state_index
			(List.rev ((combined_transition , target_state_index) :: (get_successors_with_combined_transitions state_space source_state_index)))
	;
	(* Statistics *)
	counter_add_transition#stop;

	(* Print some information *)
	print_message Verbose_total ("Exiting StateSpace.add_transition");

	()


(** Add an inequality to all the states of the state space *)
(*** NOTE: it is assumed that the p_constraint does not render some states inconsistent! ***)
let add_p_constraint_to_states state_space p_constraint =
(* 	let constraint_to_add = LinearConstraint.make_p_constraint [inequality] in *)
	(* For all state: *)
	iterate_on_states (fun _ state ->
		 LinearConstraint.px_intersection_assign_p state.px_constraint [p_constraint]
	) state_space


(* ---------------------------- *)
(* Code for Merging starts here *)
(* ---------------------------- *)

(* Merges states in queue with states in state space. Removes unreachable states. Returns unmerged part of queue *)
let merge state_space queue =
	(* Statistics *)
	tcounter_merge#start;

(* Check if two states can be merged *)
(*** NOTE: with side-effects! ***)
let are_mergeable s s' =
	(* Statistics *)
	nb_merging_attempts#increment;

	(* Call dedicated function *)
	LinearConstraint.px_hull_assign_if_exact s s'
in

(* Get states sharing the same location and discrete values from hash_table, excluding s *)
let get_siblings state_space si new_states =
	let options = Input.get_options () in
	let s = get_state state_space si in
	let l = s.global_location in
        let li = new_location_index state_space l in
	let sibs = Hashtbl.find_all state_space.states_for_comparison li in
	(* lookup px_constraints and exclude si itself *)
        let result = List.fold_left (fun siblings sj ->
		if sj = si || (options#mergeq && not(List.mem sj new_states)) then siblings else begin
			let state = get_state state_space sj in
			let c' = state.px_constraint in
			(sj,c') :: siblings
		end
	) [] sibs in
        print_message Verbose_high ("Siblings (" ^ string_of_int si ^ ") : " ^ string_of_list_of_int (List.map fst result));
        result
in

(* function for merging one state with its siblings *)
let merge_state si =
	print_message Verbose_total ("[Merge] Try to merge state " ^ (string_of_int si));
	let state = get_state state_space si in
	let c = state.px_constraint in
	(* get merge candidates as pairs (index, state) *)
	let candidates = get_siblings state_space si queue in
	(* try to merge with siblings, restart if merge found, return eaten states *)
	let rec eat all_mc rest_mc = begin
		match rest_mc with
			| [] -> [] (* here, we are really done *)
			| m :: tail_mc -> begin
				let sj,c' = m in
				if are_mergeable c c' then begin
					(* Statistics *)
					nb_merged#increment;

					(* Print some information *)
					print_message Verbose_high ("[Merge] State " ^ (string_of_int si) ^ " merged with state " ^ (string_of_int sj));

					(* we ate sj, start over with new bigger state, removing sj *)
					let all_mc' = List.filter (fun (sk, _) -> sk <> sj) all_mc in
					sj :: eat all_mc' all_mc'
				end else begin
					(* try to eat the rest of them *)
					eat all_mc tail_mc
				end
			end
	end
	in
	eat candidates candidates
in

(* make a copy of the reachable part of the state space with the eaten states replaced by the merger_state *)
let copy_and_reduce state_space merger_state eaten =
	let new_states = Hashtbl.create 1024 in
	let new_trans = Hashtbl.create 1024 in
	let new_compare = Hashtbl.create 1024 in
	let add_state s = (* adds s to new_states *)
		let state = Hashtbl.find state_space.all_states s in
		let loc = state.global_location_index in
		Hashtbl.replace new_states s state;
		Hashtbl.add new_compare loc s in
	let add_trans s a t = (* adds s --a--> t to new_transitions *)
		let transitions = hashtbl_get_or_default new_trans s [] in
		if not (List.mem (a,t) transitions)
		then Hashtbl.replace new_trans s ((a,t)::transitions) in
	let rec crs s = (* depth-first copy of reachable part of the state space *)
		if not (Hashtbl.mem new_states s || List.mem s eaten) then begin
			(* s has not been visited and is not eaten, so continue with successors *)
			print_message Verbose_total ("[Merge] Visiting new state " ^ (string_of_int s));
			add_state s;
			List.iter (fun (trans,target) ->
				if (List.mem target eaten)
				then add_trans s trans merger_state
				else begin
					add_trans s trans target;
					crs target
				end
			) (get_successors_with_combined_transitions state_space s)
		end
		else if (Hashtbl.mem new_states s) then
			print_message Verbose_total ("[Merge] State " ^ (string_of_int s) ^ " was already visited")
		else if (List.mem s eaten) then
			print_message Verbose_total ("[Merge] State " ^ (string_of_int s) ^ " has been merged")
		in
	let init = get_initial_state_index state_space in
	print_message Verbose_medium ("[Merge] Merging " ^ (string_of_list_of_int eaten) ^ " into state " ^ (string_of_int merger_state));
	crs init;
	add_state merger_state;
	if List.mem init eaten then state_space.initial <- Some merger_state;
	state_space.all_states <- new_states;
	state_space.transitions_table <- new_trans;
	state_space.states_for_comparison <- new_compare
in
	(* Iterate list of states and try to merge them in the state space *)
	let rec main_merger states =
		match states with
			| [] -> ()
			| s :: ss -> begin
					main_merger ss;
					if Hashtbl.mem state_space.all_states s then (* treat s only if it is still reachable *)
					let eaten = merge_state s in
					if eaten <> [] then(
						(* Statistics *)
						tcounter_merge_statespace#start;
						
						(* Reconstruct state space *)
						copy_and_reduce state_space s eaten;
						
						(* Statistics *)
						tcounter_merge_statespace#stop;
					)
				     end
in
	(* Do it! main function of StateSpace.merge *)
	let orig_nb_states = nb_states state_space in
	let orig_nb_queue = List.length queue in
	main_merger queue;
	let new_queue = List.filter (test_state_index state_space) queue in
	let new_nb_states = nb_states state_space in
	let new_nb_queue = List.length new_queue in
	if (orig_nb_states <> new_nb_states || orig_nb_queue <> new_nb_queue)
	then print_message Verbose_standard (
		let diff_queue = (orig_nb_queue-new_nb_queue) in
		let diff_states = (orig_nb_states-new_nb_states) in
		let diff_explored =  diff_states - diff_queue in
		"[Merge] " ^ (string_of_int diff_states) ^ " states merged ("
		^ (string_of_int diff_explored) ^ " explored, " ^ (string_of_int diff_queue) ^ " queued), out of "
		^ (string_of_int orig_nb_states) ^ " states (" ^ (string_of_int orig_nb_queue) ^ " in queue)");
	
	(* Statistics *)
	tcounter_merge#stop;

	(* return *)
	new_queue

(** Empties the hash table giving the set of states for a given location; optimization for the jobshop example, where one is not interested in comparing  a state of iteration n with states of iterations < n *)
let empty_states_for_comparison state_space =
	(* Statistics *)
	counter_empty_states_for_comparison#increment;
	counter_empty_states_for_comparison#start;

	Hashtbl.clear state_space.states_for_comparison;

	(* Statistics *)
	counter_empty_states_for_comparison#stop;

	()






(************************************************************)
(** Misc: tile natures *)
(************************************************************)
(** Convert a statespace_nature into a string *)
let string_of_statespace_nature = function
	| Good -> "good"
	| Bad -> "bad"
	| Unknown -> "unknown"



(************************************************************)
(** Statistics *)
(************************************************************)

(** Get statistics on the structure of the states: number of different locations, number of different constraints *)
let get_statistics_states state_space =
	let nb_states = nb_states state_space in
	(* Compute the number of constraints per location *)
	let nb_constraints_per_location_id = Hashtbl.create (DynArray.length state_space.locations) in
	(* Compute the number of constraints equal to each other (list of pairs (constraint, nb) )*)
	let nb_per_constraint = DynArray.make 0 in
	(* Iterate on all states *)
	iterate_on_states (fun _ state ->
		(* Find former nb of constraints for this location *)
		let former_nb = try
			Hashtbl.find nb_constraints_per_location_id state.global_location_index
		with Not_found -> 0 in
		(* Add +1 *)
		Hashtbl.replace nb_constraints_per_location_id state.global_location_index (former_nb + 1);

		(*(* Find former nb of constraints *)
		let _ =
		try(
			(* Iterate on the array *)
			DynArray.iteri (fun array_index (current_constraint, current_nb) ->
				if LinearConstraint.is_equal the_constraint current_constraint then(
					DynArray.set nb_per_constraint array_index (the_constraint, current_nb + 1);
					(* Found index *)
					raise (Found 0 (*(don't care) *));
				);
			) nb_per_constraint;
			(* If here: not found, i.e., new index *)
			DynArray.add nb_per_constraint (the_constraint, 1);
		)
		with Found _ -> ();
		in ();*)
	) state_space;

	let nb_locations = Hashtbl.length nb_constraints_per_location_id in
	let nb_different_constraints = DynArray.length nb_per_constraint in
	let result_string = ref (
		(string_of_int nb_states) ^ " state" ^ (s_of_int nb_states) ^ ", " ^ (string_of_int nb_locations) ^ " location" ^ (s_of_int nb_locations) ^ ", " ^ (string_of_int nb_different_constraints) ^ " constraint" ^ (s_of_int nb_different_constraints) ^ ""
		^ "\nNumber of constraints per locations:"
	) in

	(* Add number of constraints per location *)
	Hashtbl.iter (fun location nb_constraints ->
		result_string := !result_string ^ " - " ^ (string_of_int nb_constraints);
	) nb_constraints_per_location_id;
	(* Add average *)
	result_string := !result_string ^ "\nAverage: " ^ (round3_float ((float_of_int nb_states) /. (float_of_int nb_locations)));
	(*
	(* Add number per constraint *)
	result_string := !result_string ^ "\nNumber of occurrence of constraints: ";
	DynArray.iter (fun (the_constraint , nb_constraints) ->
		result_string := !result_string ^ " - " ^ (string_of_int nb_constraints);
	) nb_per_constraint;
	(* Add average *)
	result_string := !result_string ^ "\nAverage: " ^ (string_of_float ((float_of_int nb_different_constraints) /. (float_of_int nb_states)));
	*)
	(* Return result *)
	!result_string



(*(** Get the number of comparisons between states (performance checking purpose) *)
let get_nb_state_comparisons () =
(*	print_message Verbose_standard ("About to return the number of comparisons (" ^ (string_of_int !nb_state_comparisons) ^ ").");*)
	!nb_state_comparisons

(** Get the number of comparisons between constraints (performance checking purpose) *)
let get_nb_constraint_comparisons () =
	!nb_constraint_comparisons*)
