(************************************************************
 *
 *                       IMITATOR
 *
 * Université Paris 13, LIPN, CNRS, France
 * Université de Lorraine, CNRS, Inria, LORIA, Nancy, France
 *
 * Module description: main virtual class to explore the state space: only
 * defines post-related function, i.e., to compute the successor states of ONE
 * state. That (still) represents a large list of functions.
 *
 * File contributors : Étienne André, Jaime Arias, Nguyễn Hoàng Gia
 * Created           : 2015/12/02
 * Last modified     : 2021/03/26
 *
 ************************************************************)


(************************************************************)
(* Modules *)
(************************************************************)
open OCamlUtilities
open Exceptions
open ImitatorUtilities
open Statistics
open AbstractAlgorithm
open AbstractModel
open AbstractProperty
open DiscreteExpressions
open AlgoGeneric
open State
open Result
open StateSpace


(************************************************************)
(************************************************************)
(* Object-independent functions *)
(************************************************************)
(************************************************************)

(************************************************************)
(* Exception *)
(************************************************************)

exception Unsat_exception

(* Local exception to denote a division by 0 *)
(* exception Division_by_0_while_evaluating_discrete *)


(************************************************************)
(* Local type *)
(************************************************************)

type time_direction = Forward | Backward

let string_of_time_direction = function
	| Forward	-> "elapsing"
	| Backward	-> "past"


(************************************************************)
(* Costs *)
(************************************************************)

(*** TODO: move to a future proper class for costs ***)

(* Instantiated costs (no need to compute them for each location) *)
let instantiated_costs = ref (Array.make 0 (Array.make 0 NumConst.zero)) (*Array.make (Hashtbl.length index_of_automata) (Array.make 0 (NumConst.zero))*)

let instantiate_costs pi0 =
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* Create an empty array *)
	let costs = Array.make model.nb_automata (Array.make 0 NumConst.zero) in

	(* For each automaton *)
	for automaton_index = 0 to model.nb_automata - 1 do
		(* Retrieve the number of locations for this automaton *)
		let nb_locations = List.length (model.locations_per_automaton automaton_index) in
		(* Create the array of costs for this automaton *)
		costs.(automaton_index) <- Array.make nb_locations NumConst.zero;
		(* For each location *)
		for location_index = 0 to nb_locations - 1 do
			(* Retrieve the cost *)
			let cost = model.costs automaton_index location_index in
			(* Instantiate it *)
			let instantiated_cost = match cost with
				| None -> NumConst.zero
				| Some cost -> LinearConstraint.evaluate_p_linear_term pi0#get_value cost in
			(* Save it *)
			costs.(automaton_index).(location_index) <- instantiated_cost;
		done;
	done;
	(* Set the global array *)
	instantiated_costs := costs;
	()






(************************************************************)
(* Functions related to locations *)
(************************************************************)

(*------------------------------------------------------------*)
(* Check whether at least one local location is urgent *)
(*------------------------------------------------------------*)

(*** TODO: move to Location.mli (but creates a dependency problem, as the model is needed…) ***)

let is_location_urgent location =
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* Subfunction checking that one location is urgent in a given automaton *)
	let is_local_location_urgent automaton_index =
		(* Retrieve location *)
		let location_index = Location.get_location location automaton_index in
		(* Check if urgent *)
		model.is_urgent automaton_index location_index
	in
	List.exists is_local_location_urgent model.automata



(************************************************************)
(* Cache *)
(************************************************************)

(* hash function for locations *)
let loc_hash locations =
	Array.fold_left (fun h l ->
		7919 * h + l
	) 0 locations


(*(* hash function for clock updates *)
let upd_hash clock_update =
	List.fold_left (fun h v ->
		7919 * h + v
	) 0 clock_update*)



(*** TODO: move to the class! (otherwise, if several algorithms in the row, cache will not be reinitialized… ***)


(* Cache for computed invariants *)
let inv_cache = Cache.make loc_hash 200

(*(* Cache for clock updates *)
let upd_cache = Cache.make upd_hash 100*)


(************************************************************)
(** Statistics *)
(************************************************************)


(*** NOTE: defined OUTSIDE the class, as many instances of this class can be created (for BC), and we want a single counter *)



(*(* Print statistics for cache usage *)
let print_stats _ =
	print_message Verbose_standard "invariant cache:";
	Cache.print_stats inv_cache(*;
 	print_message Verbose_standard "clock update cache:"; *)
(* 	Cache.print_stats upd_cache *)*)


(* Number of constraints checked unsatisfiable while looking for the actions (discrete guard unsatisfiable) *)
let counter_nb_early_unsatisfiable_discrete = create_discrete_counter_and_register "early unsat states (local discrete guard)" States_counter Verbose_experiments

(* Number of constraints checked unsatisfiable while looking for the actions *)
let counter_nb_early_unsatisfiable = create_discrete_counter_and_register "early unsat states (local continuous guard)" States_counter Verbose_experiments

(* Number of actions discarded *)
let counter_nb_early_skip = create_discrete_counter_and_register "skipped actions" States_counter Verbose_experiments

(* Number of constraints computed but unsatisfiable *)
let counter_nb_unsatisfiable = create_discrete_counter_and_register "unsatisfiable constraints" States_counter Verbose_experiments

(* Number of discrete constraints unsatisfiable *)
let counter_nb_unsatisfiable_discrete = create_discrete_counter_and_register "unsatisfiable global discrete constraints" States_counter Verbose_experiments

(* Number of discrete invariants unsatisfiable *)
let counter_nb_unsatisfiable_discrete_invariants = create_discrete_counter_and_register "unsatisfiable global discrete invariants" States_counter Verbose_experiments

(* Number of different combinations considered when computing post *)
let counter_nb_combinations = create_discrete_counter_and_register "different combinations" States_counter Verbose_experiments

(* Early unsatisfiability when computing new states, after performing intersection of Di = di and C(X) and g(X) *)
let counter_nb_unsat1 = create_discrete_counter_and_register "early unsat (D^g)" States_counter Verbose_experiments

(* Counter measuring the time spent on the computation of successor (discrete) transitions *)
(*** NOTE: if this is correct, this counter should not measure any PPL-based computation! ***)
let tcounter_next_transitions = create_time_counter_and_register "next transitions" States_counter Verbose_experiments

(* Counter measuring the time spent on exhibiting which transitions can effectively be taken (this DOES include some PPL time) *)
let tcounter_legal_transitions_exist = create_time_counter_and_register "legal transitions exist" States_counter Verbose_experiments

(* Counter measuring the time spent in function compute_new_location_guards_updates_combinedtransition *)
let tcounter_compute_location_guards_discrete = create_time_counter_and_register "compute locations,guards,updates" States_counter Verbose_experiments

(* let nb_unsat2 = ref 0 *)

(* Functions counters *)
let counter_add_transition_to_state_space = create_hybrid_counter_and_register "StateBased.add_transition_to_state_space" States_counter Verbose_experiments
let counter_explore_using_strategy = create_hybrid_counter_and_register "StateBased.explore_using_strategy" States_counter Verbose_experiments
let counter_post_from_one_state = create_hybrid_counter_and_register "StateBased.post_from_one_state" States_counter Verbose_experiments
let counter_process_post_n = create_hybrid_counter_and_register "StateBased.process_post_n" States_counter Verbose_experiments

(* Misc counters *)
let counter_nplus1 = create_hybrid_counter_and_register "StateBased.computation of post_n+1" States_counter Verbose_medium

let counter_gcmajor = create_hybrid_counter_and_register "StateBased.gcmajor" States_counter Verbose_experiments



(************************************************************)
(* Syntactic functions (i.e. on the automaton structure) *)
(************************************************************)

(** Compute the predecessors of a location in an automaton via SOME given action or via any (NONE) *)
let predecessors_of_location_gen (automaton_index : Automaton.automaton_index) (location_index : Automaton.location_index) (action_index_option : Automaton.action_index option) : (Automaton.location_index list) =
	(* Retrieve the model *)
	let model = Input.get_model() in
	
	(* Iterate on locations *)
	let predecessors =
	List.fold_left (fun current_predecessors_for_all_locations source_location_index ->
		(* source_location_index is a predecessor of location_index iff there exists an action for which there exists with location_index as target *)
		if (
			let actions_to_iterate = match action_index_option with
			(* Only iterate on the specified action *)
			| Some action_index -> [action_index]
			(* Iterate on all actions for this automaton *)
			| None -> (model.actions_per_automaton automaton_index)
			in
			(* Iterate on the specified set of actions *)
			List.exists (fun action_index ->
				(* Iterate on the transitions for this automaton, location and action *)
				List.exists (fun transition_index ->
					(* Get the transition *)
					let transition = model.transitions_description transition_index in
					(* Get the target *)
					let target_location = transition.target in
					(* If target = our location, then keep the source *)
					target_location = location_index
				) (model.transitions automaton_index source_location_index action_index)
			) actions_to_iterate
		)
		then source_location_index :: current_predecessors_for_all_locations
		else current_predecessors_for_all_locations
	) [] (model.locations_per_automaton automaton_index)
	in
	(* Remove duplicates *)
	list_only_once predecessors


(** Compute the predecessors of a location in an automaton *)
let predecessors_of_location (automaton_index : Automaton.automaton_index) (location_index : Automaton.location_index) : (Automaton.location_index list) =
	predecessors_of_location_gen automaton_index location_index None


(** Compute the predecessors of a location in an automaton via a given action *)
let predecessors_of_location_via_action (automaton_index : Automaton.automaton_index) (location_index : Automaton.location_index) (action_index : Automaton.action_index) : (Automaton.location_index list) =
	predecessors_of_location_gen automaton_index location_index (Some action_index)


(************************************************************)
(* Main semantic functions *)
(************************************************************)

(** Check whether a d_linear_constraint is satisfied by the discrete values in a location *)
let evaluate_d_linear_constraint_in_location location =
	(* Directly call the build-in function *)
	LinearConstraint.d_is_pi0_compatible (Location.get_discrete_rational_value location)

(** Check whether a discrete non-linear constraint is satisfied by the discrete values in a location **)
let evaluate_d_nonlinear_constraint_in_location location =
    NonlinearConstraint.check_nonlinear_constraint (Location.get_discrete_value location)

(** Check whether the discrete part of a guard is satisfied by the discrete values in a location *)
let is_discrete_guard_satisfied location (guard : AbstractModel.guard) : bool =
	match guard with
	| True_guard -> true
	| False_guard -> false
	| Discrete_guard discrete_guard -> evaluate_d_nonlinear_constraint_in_location location discrete_guard
	| Continuous_guard _ -> true
	| Discrete_continuous_guard discrete_continuous_guard -> evaluate_d_nonlinear_constraint_in_location location discrete_continuous_guard.discrete_guard

(** Check whether the discrete part of a guards are satisfied by the discrete values in a location *)
let is_discrete_guards_satisfied location =
    List.for_all (is_discrete_guard_satisfied location)

(** Check whether the intersection between a pxd_constraint with an AbstractModel.guard if satisfiable (both inputs remain unchanged) *)
let is_constraint_and_continuous_guard_satisfiable pxd_linear_constraint = function
	(* True: trivially satisfiable because we assume the original constraint was satisfiable *)
	| True_guard -> true

	(* False: trivially unsatisfiable *)
	| False_guard -> false

	(* Discrete guard: trivially satisfiable because no continuous part, and we assume the original constraint was satisfiable *)
	| Discrete_guard _ -> true

	(* Continuous guard: we have to intersect and check satisfiability *)
	| Continuous_guard continuous_guard ->
		LinearConstraint.pxd_is_satisfiable (LinearConstraint.pxd_intersection [pxd_linear_constraint; continuous_guard])

	(* Discrete + continuous guard: we have to intersect and check satisfiability *)
	| Discrete_continuous_guard discrete_continuous_guard ->
		LinearConstraint.pxd_is_satisfiable (LinearConstraint.pxd_intersection [pxd_linear_constraint; discrete_continuous_guard.continuous_guard])

(*(*------------------------------------------------------------*)*)
(*(* Compute the intersection of guards *)*)
(*(*------------------------------------------------------------*)*)
(*let intersection_of_guards location guards =*)
(*    (* Partition of discrete guards and continuous guards *)*)
(*    let discrete_guards, continuous_guards = List.partition (fun guard -> match guard with | Discrete_guard _ -> true | _ -> false) guards in*)
(*    match discrete_guards, continuous_guards with*)
(*        (* is_discrete_guard_satisfied ? and then (thanks to short-circuit evaluation *)*)
(*        (* is_constraint_and_continuous_guard_satisfiable ? *)*)
(*        | dg, cg when*)
(*            (List.for_all (fun guard -> is_discrete_guard_satisfied location guard) dg) ->*)

(*                let pxd_linear_constraints = List.map(fun guard -> Continuous_guard guard) continuous_guards in*)
(*                (* if yes, compute intersection of continuous part *)*)
(*                (* Perform the intersection *)*)
(*                LinearConstraint.pxd_intersection pxd_linear_constraints*)

(*        (* no -> False ! *)*)
(*        | _ -> False_guard*)

(** Split guards into two list, one of discrete guards and other of continuous guards *)
let split_guards_into_discrete_and_continuous =
    List.fold_left (fun (current_discrete_guards, current_continuous_guards) guard ->
		match guard with
		(* True guard: unchanged *)
		| True_guard -> current_discrete_guards, current_continuous_guards
		(* False guard: should have been tested before! *)
		| False_guard -> raise (InternalError "Met a false guard while computing new location, although this should have been tested in a local automaton")
		| Discrete_guard discrete_guard -> discrete_guard :: current_discrete_guards, current_continuous_guards
		| Continuous_guard continuous_guard -> current_discrete_guards, continuous_guard :: current_continuous_guards
		| Discrete_continuous_guard discrete_continuous_guard ->
			discrete_continuous_guard.discrete_guard :: current_discrete_guards, discrete_continuous_guard.continuous_guard :: current_continuous_guards
	) ([], [])

(*
(* Evaluate a discrete_arithmetic_expression using a discrete variable valuation *)
(*** NOTE: define a top-level function to avoid recursive passing of all common variables ***)
let evaluate_discrete_arithmetic_expression v =
	let rec evaluate_discrete_arithmetic_expression_rec = function
		| DAE_plus (discrete_arithmetic_expression, discrete_term) -> NumConst.add (evaluate_discrete_arithmetic_expression_rec discrete_arithmetic_expression) (evaluate_discrete_term discrete_term)
		| DAE_minus (discrete_arithmetic_expression, discrete_term) -> NumConst.sub (evaluate_discrete_arithmetic_expression_rec discrete_arithmetic_expression) (evaluate_discrete_term discrete_term)
		| DAE_term discrete_term -> evaluate_discrete_term discrete_term

	and evaluate_discrete_term = function
		| DT_mul (discrete_term, discrete_factor) -> NumConst.mul (evaluate_discrete_term discrete_term) (evaluate_discrete_factor discrete_factor)
		| DT_div (discrete_term, discrete_factor) ->
			(*** NOTE: here comes the infamous division by 0 ***)
			(* Compute the denominator *)
			let denominator = evaluate_discrete_factor discrete_factor in
			(* Check if 0 *)
			if NumConst.equal denominator NumConst.zero then(
				raise Division_by_0_while_evaluating_discrete
			)
			(* Else go on with division *)
			else
			NumConst.div (evaluate_discrete_term discrete_term) denominator
		| DT_factor discrete_factor -> evaluate_discrete_factor discrete_factor

	and evaluate_discrete_factor = function
		| DF_variable discrete_index -> v discrete_index
		| DF_constant discrete_value -> discrete_value
		| DF_unary_min discrete_factor -> NumConst.neg (evaluate_discrete_factor discrete_factor)
		| DF_expression discrete_arithmetic_expression -> evaluate_discrete_arithmetic_expression_rec discrete_arithmetic_expression
	in
	evaluate_discrete_arithmetic_expression_rec*)

(*------------------------------------------------------------*)
(* Create a PXD constraint of the form D_i = d_i for the discrete variables *)
(*------------------------------------------------------------*)
let discrete_constraint_of_global_location (global_location : Location.global_location) : LinearConstraint.pxd_linear_constraint =
	(* Retrieve the model *)
	let model = Input.get_model() in

	let discrete_values = List.map (fun discrete_index -> discrete_index, (Location.get_discrete_value global_location discrete_index)) model.discrete in

    (* TODO check with étienne, maybe can use all numeric as constraint ??? *)
    (* Get only rational discrete for constraint encoding *)
    let only_discrete_rational_values = List.filter (fun (discrete_index, discrete_value) -> DiscreteValue.is_rational_value discrete_value) discrete_values in
    (* map to num const *)
    let discrete_rational_numconst_values = List.map (fun (discrete_index, discrete_value) -> discrete_index, DiscreteValue.numconst_value discrete_value) only_discrete_rational_values in

	(* Constraint of the form D_i = d_i *)
	LinearConstraint.pxd_constraint_of_point discrete_rational_numconst_values

(*------------------------------------------------------------*)
(* Get all invariants of model's automatas *)
(* Note : use of Input.get_model *)
(*------------------------------------------------------------*)
let get_model_invariants (location : Location.global_location) =
    (* Retrieve the model *)
	let model = Input.get_model() in

	List.map (fun automaton_index ->
		(* Get the current location *)
		let location_index = Location.get_location location automaton_index in
		(* Compute the invariant *)
		model.invariants automaton_index location_index
	) model.automata

(*------------------------------------------------------------*)
(* Compute the invariant associated to a location   *)
(*------------------------------------------------------------*)
let compute_plain_continuous_invariant (location : Location.global_location) : LinearConstraint.pxd_linear_constraint =
    (* construct invariant *)
	let invariants = get_model_invariants location in
	let _ (* discrete_invariants *), continuous_invariants = split_guards_into_discrete_and_continuous invariants in
	(* Perform the intersection *)
	LinearConstraint.pxd_intersection continuous_invariants

(*------------------------------------------------------------*)
(* Compute the invariant I_l associated to a location  *)
(* including renaming and time elapse. Uses cache.  *)
(*------------------------------------------------------------*)
let compute_invariant location =
	(* Retrieve the model *)
(* 	let model = Input.get_model() in *)

	(* Strip off discrete for caching scheme  *)
	let locations = Location.get_locations location in
	(* check in cache *)
	let entry = Cache.find inv_cache locations in
	match entry with
		| Some inv -> inv
		| None -> (
			(* Build plain invariant I_l(X) *)
			let invariant = compute_plain_continuous_invariant location in
			(* Store in cache *)
			Cache.store inv_cache locations invariant;
			invariant
		)


(*------------------------------------------------------------*)
(* Compute the invariant associated to a location and valuate the value of the discrete variables   *)
(*------------------------------------------------------------*)
let compute_valuated_invariant (location : Location.global_location) : LinearConstraint.px_linear_constraint =
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* Compute the invariant with the discrete variables *)
	let invariant = compute_plain_continuous_invariant location in

	(* Valuate the discrete variables *)
	let discrete_constraint = discrete_constraint_of_global_location location in

	(* Perform intersection of C(X) and I_l0(X) and D_i = d_i *)
	print_message Verbose_high ("Performing intersection of I_l(X) and D_i = d_i");
	let current_constraint = LinearConstraint.pxd_intersection [invariant ; discrete_constraint ] in
	(* Print some information *)
	if verbose_mode_greater Verbose_total then
		print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_constraint);

	(* Eliminate the discrete variables *)
	print_message Verbose_high ("Hide discrete");
	LinearConstraint.pxd_hide_discrete_and_collapse current_constraint


(*------------------------------------------------------------*)
(* Get the list of clocks concerned by an AbstractModel.clock_updates *)
(*------------------------------------------------------------*)
let get_clocks_in_update (update : AbstractModel.clock_updates) : Automaton.clock_index list = match update with
	(* No update at all *)
	| No_update -> []
	(* Reset to 0 only *)
	| Resets clocks -> clocks
	(* Reset to arbitrary value (including discrete, parameters and clocks) *)
	| Updates updates ->
		(* Keep only the clock members, and discard the linear terms *)
		let clocks, _ = List.split updates in clocks

let get_clocks_in_updates (updates : AbstractModel.clock_updates list) : Automaton.clock_index list =
	list_only_once (List.fold_left (fun current_list clock_update -> List.rev_append current_list (get_clocks_in_update clock_update) ) [] updates)



(*------------------------------------------------------------*)
(* Check whether there are some complex updates of the form clock' = linear_term *)
(*------------------------------------------------------------*)


(*------------------------------------------------------------*)
(* Generic function to apply the updates to a linear constraint (either by intersection with the updates, or by existential quantification) *)
(* time_direction   : if Forward, then apply updates; if Backward, apply 'inverted' updates *)
(* linear_constraint: the linear constraint (modified by this function) *)
(* clock_updates    : the list of clock updates to apply *)
(*------------------------------------------------------------*)
(*** TO OPTIMIZE: use cache (?) *)
let apply_updates_assign_gen (time_direction: time_direction) (linear_constraint : LinearConstraint.pxd_linear_constraint) (clock_updates : AbstractModel.clock_updates list) =
	(* Retrieve the model *)
	let model = Input.get_model() in

	if clock_updates <> [] then(
		(* Merge updates *)

		(*** TO OPTIMIZE: only create the hash if there are indeed some resets/updates ***)

		let clocks_hash = Hashtbl.create model.nb_clocks in

		(* Check wether there are some complex updates of the form clock' = linear_term *)
		let arbitrary_updates = ref false in
		(* Iterate on the lists of clocks for all synchronized automata *)
		List.iter (fun local_updates ->
			match local_updates with
			| No_update -> ()
			| Resets list_of_clocks ->
				(* Iterate on the clocks, for a given automaton *)
				List.iter (fun clock_id ->
					(* Assign this clock to true in the table *)
					Hashtbl.replace clocks_hash clock_id (LinearConstraint.make_pxd_linear_term [] NumConst.zero);
				) list_of_clocks;
			| Updates list_of_clocks_lt ->
				(* Set the flag *)
				arbitrary_updates := true;
				(* Iterate on the clocks, for a given automaton *)
				List.iter (fun (clock_id, linear_term) ->
					(* Check if already updated *)
					if Hashtbl.mem clocks_hash clock_id then (
						(* Find its previous value *)
						let previous_update = Hashtbl.find clocks_hash clock_id in
						(* Compare with the new one *)
						if previous_update <> linear_term then (
						(* If different: warning *)
							print_warning ("The clock `" ^ (model.variable_names clock_id) ^ "` is updated several times with different values for the same synchronized action. The behavior of the system is now unspecified.");
						)
					);
					(* Update the update *)
					Hashtbl.replace clocks_hash clock_id linear_term;
				) list_of_clocks_lt;
		) clock_updates;

		(* THREE CASES: no updates, only resets (to 0) or updates (to linear terms) *)

		(* CASE 1: no update nor reset *)
		if Hashtbl.length clocks_hash = 0 then (

			(* do nothing! *)

			(* Print some information *)
			print_message Verbose_total ("\n -- No resets to handle here");

		(* CASE 2: only resets *)
		)else(if not !arbitrary_updates then(

			(* Print some information *)
			print_message Verbose_total ("\n -- Case only resets");


			(*** TODO : add "reset" function to LinearConstraint ***)


			(*** TO OPTIMIZE: Hashtbl.fold and List.map should be merged into one function ***)

			(* Compute the list of clocks to update from the hashtable *)
			let list_of_clocks_to_update = Hashtbl.fold (fun clock_id _ list_of_clocks -> clock_id :: list_of_clocks) clocks_hash [] in

			(* Hide clocks updated within the linear constraint, viz., exists X' : lc, for X' in rho(X) *)
			(* Print some information *)
			print_message Verbose_total ("\n -- Remove reset clocks");

			(* Eliminate variables *)
			LinearConstraint.pxd_hide_assign list_of_clocks_to_update linear_constraint;

			(* Print some information *)
			if verbose_mode_greater Verbose_total then(
				print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names linear_constraint);
			);

			(* Case 2a: forward updates, i.e., add `X = 0` *)
			if time_direction = Forward then(
				(* Compute X = 0 for the variables appearing in resets *)
				print_message Verbose_total ("\n -- Computing resets of the form `X = 0`");
				let updates =
					(List.map (fun variable_index ->
						(* Consider cases for clocks *)
						match model.type_of_variables variable_index with
						(* Clocks: X = 0 *)
						| DiscreteValue.Var_type_clock ->
							let x_lt = LinearConstraint.make_pxd_linear_term [
								NumConst.one, variable_index;
							] NumConst.zero in
							LinearConstraint.make_pxd_linear_inequality x_lt LinearConstraint.Op_eq
						| _ -> raise (InternalError "Only clocks can be updated.")
					) list_of_clocks_to_update) in
				(* Create the constraint *)
				let updates = LinearConstraint.make_pxd_constraint updates in
				(* Print some information *)
				if verbose_mode_greater Verbose_total then(
					print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names updates);
				);

				(* Add the constraints X = 0 *)
				(* Print some information *)
				print_message Verbose_total ("\n -- Adding `X = 0` for reset clocks");

				(* Apply intersection *)
				LinearConstraint.pxd_intersection_assign linear_constraint [updates];

				(* Print some information *)
				if verbose_mode_greater Verbose_total then(
					print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names linear_constraint);
				);
			); (* end if Forward *)

		(* CASE 3: updates to linear terms *)
		)else(

			print_message Verbose_total ("\n -- Case updates to linear terms");

			(*** TODO (not urgent) : add "update" function to LinearConstraint ***)

			(* Compute the pairs (x_i , linear_term) from the hashtable *)
			let updates : (Automaton.clock_index * LinearConstraint.pxd_linear_term) list = Hashtbl.fold (fun clock_id linear_term current_updates -> (clock_id, linear_term) :: current_updates) clocks_hash [] in

			(* Case 3a: existential quantification requires to create primed variables *)

			(** TO OPTIMIZE (?): could be performed statically (when converting the model).
				PRO: save time because no need to compute this for each constraint;
				CON: lose time & memory (but maybe not that much) at some point because operations on constraints will have all dimensions instead of just the updated prime variables
				TO OPTIMIZE (other option): merge all operations together, so that no need for hashtable
			*)

			(* CASE 3, step 1: Compute the correspondance between clocks X_i and renamed clocks X_i' *)
			let prime_of_variable = Hashtbl.create (List.length updates) in
			let variable_of_prime = Hashtbl.create (List.length updates) in
			let clock_prime_id = ref model.nb_variables in
			List.iter (fun (clock_id, _) ->
				Hashtbl.add prime_of_variable clock_id !clock_prime_id;
				Hashtbl.add variable_of_prime !clock_prime_id clock_id;
				(* Debug message *)
				if verbose_mode_greater Verbose_total then(
					print_message Verbose_total ("\nThe primed index of variable `" ^ (model.variable_names clock_id) ^ "` (index = " ^ (string_of_int clock_id) ^ ") is set to " ^ (string_of_int !clock_prime_id) ^ ".")
				);
				(* Increment the prime id for next variable *)
				clock_prime_id := !clock_prime_id + 1;
				()
			) updates;
			let new_max_dimension = !clock_prime_id in
			let extra_dimensions = new_max_dimension - model.nb_variables in
			print_message Verbose_total ("\nNew dimension for constraints: " ^ (string_of_int new_max_dimension) ^ "; extra dimensions : " ^ (string_of_int extra_dimensions) ^ ".");
			(* Extend the number of dimensions *)
			LinearConstraint.set_dimensions model.nb_parameters (model.nb_clocks + extra_dimensions) model.nb_discrete;
			LinearConstraint.pxd_add_dimensions extra_dimensions linear_constraint;

			(* Compute pairs (X_i', X_i) *)
			let clocks_and_primes = Hashtbl.fold (fun clock_id clock_prime_id pairs -> (clock_id, clock_prime_id) :: pairs) prime_of_variable [] in

			(* CASE 3, step 2: Create primed constraints *)
			let inequalities = List.map (fun (clock_id, linear_term) ->

				let possibly_primed_clock_index, possibly_primed_linear_term =
				(* Forward update: create `X_i' = linear_term` *)
				if time_direction = Forward then(
					(Hashtbl.find prime_of_variable clock_id),
					linear_term
				)else(
				(* Backward update: create `X_i = linear_term'` *)
					clock_id,
					(LinearConstraint.rename_pxd_linear_term clocks_and_primes linear_term)
				) in

				(* Build `linear_term - clock_id' = 0` or  `linear_term' - clock_id = 0` *)
				LinearConstraint.make_pxd_linear_inequality (
					LinearConstraint.add_pxd_linear_terms
						(* 1: The update linear term *)
						possibly_primed_linear_term
						(* 2: - clock_id' *)
						(LinearConstraint.make_pxd_linear_term [
								NumConst.minus_one, possibly_primed_clock_index;
							] NumConst.zero)
				) LinearConstraint.Op_eq
			) updates in

			(* Create the constraint *)
			let inequalities = LinearConstraint.make_pxd_constraint inequalities in

			(* Print some information *)
			let print_constraint c =
				if verbose_mode_greater Verbose_total then(
					let all_variable_names = fun variable_id ->
						if variable_id < model.nb_variables then
							model.variable_names variable_id
						else
							(model.variable_names (Hashtbl.find variable_of_prime variable_id)) ^ "'"
					in
					print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint all_variable_names c);
				)else(
					()
				)
			in

			print_constraint inequalities;

			(* Add the constraints X_i' = linear_term *)

			(* Print some information *)
			print_message Verbose_total ("\n -- Adding `X_i' = linear_term` for updated clocks");
			(* Apply intersection *)
			LinearConstraint.pxd_intersection_assign linear_constraint [inequalities];
			(* Print some information *)
			print_constraint linear_constraint;

			(* Remove the variables X_i *)
			let list_of_clocks_to_hide, _ = List.split updates in
			(* Hide clocks updated within the linear constraint, viz., exists X_i : lc, for X_i in rho(X) *)
			print_message Verbose_total ("\n -- Computing exists `X : lc` for updated clocks");
			LinearConstraint.pxd_hide_assign list_of_clocks_to_hide linear_constraint;
			(* Print some information *)
			if verbose_mode_greater Verbose_total then(
				print_constraint linear_constraint;
			);

			(* Renames clock X_i' into X_i *)
			(** TO OPTIMIZE !! *)
			print_message Verbose_total ("\n -- Renaming clocks X_i' into X_i for updated clocks");
			LinearConstraint.pxd_rename_variables_assign clocks_and_primes linear_constraint;
			(* Print some information *)
			if verbose_mode_greater Verbose_total then(
				print_constraint linear_constraint;
			);

			(* Go back to the original number of dimensions *)
			print_message Verbose_total ("\nGo back to standard dimension for constraints: " ^ (string_of_int model.nb_variables) ^ ".");
			LinearConstraint.set_dimensions model.nb_parameters model.nb_clocks model.nb_discrete;
			LinearConstraint.pxd_remove_dimensions extra_dimensions linear_constraint;
			(* Print some information *)
			if verbose_mode_greater Verbose_total then(
				print_constraint linear_constraint;
			);
			
(*			(* Case 3b: without existential quantification, just intersect with updates *)
			) else (
			
				(* Create constraints X_i = linear_term *)
				let inequalities = List.map (fun (clock_id, linear_term) ->
					(* Build linear_term - clock_id = 0 *)
					LinearConstraint.make_pxd_linear_inequality (
						LinearConstraint.add_pxd_linear_terms
							(* 1: The update linear term *)
							linear_term
							(* 2: - clock_id *)
							(LinearConstraint.make_pxd_linear_term [
									NumConst.minus_one, clock_id;
								] NumConst.zero)
					) LinearConstraint.Op_eq
				) updates in
				
				(* Create the constraint *)
				let inequalities = LinearConstraint.make_pxd_constraint inequalities in

				(* Print some information *)
				if verbose_mode_greater Verbose_total then(
					print_message Verbose_total ("\nConstraint before intersection with update constraint…");
					print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names inequalities);
				);

				(* Apply intersection *)
				LinearConstraint.pxd_intersection_assign linear_constraint [inequalities];
				
				(* Print some information *)
				if verbose_mode_greater Verbose_total then(
					print_message Verbose_total ("\nConstraint after intersection with update constraint…");
					print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names inequalities);
				);

			
			)*)

			(*** TODO: check what about discrete variables ?!! ***)
		) (* end CASE 3 *)
		)
	) (* end if some clock updates *)


(*------------------------------------------------------------*)
(* Apply the updates to a linear constraint by existential quantification (that is, when applying x := x+y+i+1, "x" is replaced with "x+y+i+1" *)
(*------------------------------------------------------------*)
let apply_updates_assign = apply_updates_assign_gen Forward


(*------------------------------------------------------------*)
(* Apply the updates to a linear constraint by existential quantification and with backward direction (that is, when applying x := x+y+i+1, "x+y+i+1" is replaced with "x" *)
(*------------------------------------------------------------*)
let apply_updates_assign_backward = apply_updates_assign_gen Backward


(*------------------------------------------------------------*)
(* Apply the updates to a linear constraint by intersection (that is, when applying x := y+1, we simply intersect the existing constraint with x = y+1 *)
(*------------------------------------------------------------*)
(* let intersect_updates_assign = apply_updates_assign_gen false *)


(*------------------------------------------------------------*)
(* Compute the list of stopped and elapsing clocks in a location *)
(* Returns a pair (stopped clocks, elapsing clocks)           *)
(*------------------------------------------------------------*)
let compute_stopwatches (location : Location.global_location) : (Automaton.clock_index list * Automaton.clock_index list) =
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* If no stopwatches at all: just return the set of clocks *)
	if not model.has_non_1rate_clocks then ([], model.clocks) else(
		(* Hashtbl clock_id --> true if clock should be stopped by some automaton *)
		let stopwatches_hashtable = Hashtbl.create (List.length model.clocks) in
		let stopwatch_mode = ref false in
		(* Update hash table *)
		List.iter (fun automaton_index ->
			(* Get the current location *)
			let location_index = Location.get_location location automaton_index in
			(* Get the list of stopped clocks *)
			let stopped = model.stopwatches automaton_index location_index in
			(* If list non null: we have stopwatches here *)
			if stopped <> [] then stopwatch_mode := true;
			(* Add each clock *)
			List.iter (fun stopwatch_id ->
				Hashtbl.replace stopwatches_hashtable stopwatch_id true
			) stopped;
		) model.automata;
		(* If there are no stopwatches then just return the set of clocks *)
		if (not !stopwatch_mode) then ([], model.clocks) else (
			(* Computing the list of stopped clocks, and the list of elapsing clocks *)
			List.fold_left (fun (stopped_clocks, elapsing_clocks) clock_id ->
				(* Test if the clock should be stopped *)
				if Hashtbl.mem stopwatches_hashtable clock_id then
					clock_id :: stopped_clocks, elapsing_clocks
				else
					stopped_clocks, clock_id :: elapsing_clocks
			) ([], []) model.clocks
		) (* if no stopwatch for this location *)
	) (* if no stopwatch in the model *)


(*------------------------------------------------------------*)
(* Compute the list of clocks with their flow in a location   *)
(* Returns a list of pairs (clock_index, flow)                *)
(* Raises a warning whenever a clock is assigned to TWO different flows *)
(*------------------------------------------------------------*)
let compute_flows (location : Location.global_location) : ((Automaton.clock_index * NumConst.t) list) =
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* Hashtbl clock_id --> flow *)
	let flows_hashtable = Hashtbl.create (List.length model.clocks) in
	
	(* Maintain a Boolean to see if any clock has a rate different from 1 *)
	let flow_mode = ref false in
	
	(* Update hash table *)
	List.iter (fun automaton_index ->
		(* Get the current location *)
		let location_index = Location.get_location location automaton_index in
		
		(* 1. Manage the list of stopped clocks *)
		let stopped = model.stopwatches automaton_index location_index in
		(* If list non null: we have flows <> 1 *)
		if stopped <> [] then flow_mode := true;
		(* Add each clock *)
		List.iter (fun stopwatch_id ->
			Hashtbl.replace flows_hashtable stopwatch_id NumConst.zero
		) stopped;
		
		(* 2. Manage the explicit flows *)
		let flows = model.flow automaton_index location_index in
		(* Add each clock *)
		List.iter (fun (clock_id, flow_value) ->
			(* If flow <> 1, update Boolean *)
			if NumConst.neq flow_value NumConst.one then flow_mode := true;

			(* Compare with previous value *)
			try(
				(* Get former value *)
				let former_flow_value = Hashtbl.find flows_hashtable clock_id in
				(* Compare *)
				if NumConst.neq former_flow_value flow_value then(
					
					(*** TODO: a flag should be raised somewhere so that the result is said to be perhaps wrong! (or unspecified) ***)
					
					print_warning ("Clock `" ^ (model.variable_names clock_id) ^ "` is assigned to two different flow values at the same time (`" ^ (NumConst.string_of_numconst flow_value) ^ "` in location `" ^ (model.location_names automaton_index location_index) ^ "`, as well as `" ^ (NumConst.string_of_numconst former_flow_value) ^ "`). The behavior becomes unspecified!");
				);
				(* Do not add *)
				()
			) with Not_found ->(
			(* Not found: not yet defined => add *)
				Hashtbl.add flows_hashtable clock_id flow_value
			);
			
		) flows;
		
	) model.automata;
	
	(* If there are no explicit flows then just return the set of clocks with flow 1 *)
	if (not !flow_mode) then (List.map (fun clock_id -> clock_id, NumConst.one) model.clocks) else (
		(* Computing the list of clocks with their flow *)
		List.map (fun clock_id ->
			(* Try to get the clock explicit flow *)
			try(
				(* Get value *)
				let flow_value = Hashtbl.find flows_hashtable clock_id in
				(* Return *)
				clock_id, flow_value
			) with Not_found ->
				(* Absent: flow is 1 *)
				clock_id, NumConst.one
		) model.clocks
	) (* if no explicit flow for this location *)



(*------------------------------------------------------------*)
(* Generic function to apply either time elapsing or time past to a constraint in a location *)
(*------------------------------------------------------------*)




(*** WARNING: bad prog! Duplicate function with 2 different types ***)
let pxd_create_inequalities_constant variables_constant =
	(* Create the inequalities var = 0, for var in variables_constant *)
	List.map (fun variable ->
		(* Create a linear term *)
		let linear_term = LinearConstraint.make_pxd_linear_term [(NumConst.one, variable)] NumConst.zero in
		(* Create the inequality *)
		LinearConstraint.make_pxd_linear_inequality linear_term LinearConstraint.Op_eq
	) variables_constant

(*** WARNING: bad prog! Duplicate function with 2 different types ***)
let px_create_inequalities_constant variables_constant =
	(* Create the inequalities var = 0, for var in variables_constant *)
	List.map (fun variable ->
		(* Create a linear term *)
		let linear_term = LinearConstraint.make_px_linear_term [(NumConst.one, variable)] NumConst.zero in
		(* Create the inequality *)
		LinearConstraint.make_px_linear_inequality linear_term LinearConstraint.Op_eq
	) variables_constant


(* Generate a polyhedron for computing the time elapsing for (parametric) timed automata, i.e., without stopwatches nor flows. *)
let generate_polyhedron_time_elapsing_pta time_direction variables_elapse variables_constant =
	(* Create the inequalities var = 1, for var in variables_elapse *)
	let inequalities_elapse = List.map (fun variable ->
		(* Create a linear term of the form `var + (-1 | 1) = 0`, with `-1` for elapsing, or `1` for past *)
		let linear_term = LinearConstraint.make_pxd_linear_term [(NumConst.one, variable)] (match time_direction with Forward -> NumConst.minus_one | Backward -> NumConst.one) in
		(* Create the inequality *)
		LinearConstraint.make_pxd_linear_inequality linear_term LinearConstraint.Op_eq
	) variables_elapse in
	
	(* Create the inequalities `var = 0`, for var in variables_constant *)
	let inequalities_constant = pxd_create_inequalities_constant variables_constant in
	
	(* Print some information *)
	print_message Verbose_total ("Creating linear constraint for standard time elapsing…");
	
	(* Convert both sets of inequalities to a constraint *)
	LinearConstraint.make_pxd_constraint (List.rev_append inequalities_elapse inequalities_constant)


(*** HACK: should be an object!!! ***)
(*** WARNING: won't work if NESTED analyses are performed! i.e., a AlgoStateBased calls another AlgoStateBased ***)
(* Static polyhedron used for time elapsing computation, for "normal" PTAs, i.e., without stopwatches nor explicit flows *)
let time_elapsing_polyhedron : LinearConstraint.pxd_linear_constraint option ref = ref None
(* Static polyhedron used for time past computation, for "normal" PTAs, i.e., without stopwatches nor explicit flows *)
let time_past_polyhedron : LinearConstraint.pxd_linear_constraint option ref = ref None


(*** WARNING: bad prog! Duplicate function with 2 different types ***)
let pxd_compute_time_polyhedron (direction : time_direction) (location : Location.global_location) : LinearConstraint.pxd_linear_constraint =
	(* Get the model *)
	let model = Input.get_model() in

	(* Print some information *)
	print_message Verbose_high ("Computing list of explicit flows…");
	
	let flows = compute_flows location in
	
	(* Print some information *)
	if verbose_mode_greater Verbose_total then(
		let list_of_flows = List.map (fun (clock_id, flow_value) -> (model.variable_names clock_id) ^ "' = " ^ (NumConst.string_of_numconst flow_value)) flows in
		print_message Verbose_total ("Flows: " ^ (string_of_list_of_string_with_sep ", " list_of_flows));
	);

	(* Compute polyhedron *)
	(* Create the inequalities `clock_id = flow_value` *)
	let inequalities_flows = List.map (fun (clock_id, flow_value) ->
		(* Create a linear term `clock_id + (-)flow_value`; the value is negated iff direction is foward, to create `clock_id - flow_value = 0`, equivalent to `clock_id = flow_value` *)
		let negated_flow_value = match direction with
		| Forward	-> NumConst.neg flow_value
		| Backward	-> flow_value
		in
		let linear_term = LinearConstraint.make_pxd_linear_term [(NumConst.one, clock_id)] negated_flow_value in
		(* Create the inequality *)
		LinearConstraint.make_pxd_linear_inequality linear_term LinearConstraint.Op_eq
	) flows in
	
	(* Create the inequalities `var = 0`, for var in variables_constant *)
	let inequalities_constant = pxd_create_inequalities_constant model.parameters_and_discrete in

	(* Convert both sets of inequalities to a constraint *)
	let time_polyhedron = LinearConstraint.make_pxd_constraint (List.rev_append inequalities_flows inequalities_constant) in
	
	(* Print some information *)
	if verbose_mode_greater Verbose_total then(
		print_message Verbose_total ("Creating linear constraint for time elapsing with explicit flows…");
		print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names time_polyhedron);
	);
	
	(* Return result *)
	time_polyhedron

(*** WARNING: bad prog! Duplicate function with 2 different types ***)
let px_compute_time_polyhedron (direction : time_direction) (location : Location.global_location) : LinearConstraint.px_linear_constraint =
	(* Get the model *)
	let model = Input.get_model() in

	(* Print some information *)
	print_message Verbose_high ("Computing list of explicit flows…");
	
	let flows = compute_flows location in
	
	(* Print some information *)
	if verbose_mode_greater Verbose_total then(
		let list_of_flows = List.map (fun (clock_id, flow_value) -> (model.variable_names clock_id) ^ "' = " ^ (NumConst.string_of_numconst flow_value)) flows in
		print_message Verbose_total ("Flows: " ^ (string_of_list_of_string_with_sep ", " list_of_flows));
	);

	(* Compute polyhedron *)
	(* Create the inequalities `clock_id = flow_value` *)
	let inequalities_flows = List.map (fun (clock_id, flow_value) ->
		(* Create a linear term `clock_id + (-)flow_value`; the value is negated iff direction is foward, to create `clock_id - flow_value = 0`, equivalent to `clock_id = flow_value` *)
		let negated_flow_value = match direction with
		| Forward	-> NumConst.neg flow_value
		| Backward	-> flow_value
		in
		let linear_term = LinearConstraint.make_px_linear_term [(NumConst.one, clock_id)] negated_flow_value in
		(* Create the inequality *)
		LinearConstraint.make_px_linear_inequality linear_term LinearConstraint.Op_eq
	) flows in
	
	(* Create the inequalities `var = 0`, for var in variables_constant *)
	let inequalities_constant = px_create_inequalities_constant model.parameters in

	(* Convert both sets of inequalities to a constraint *)
	let time_polyhedron = LinearConstraint.make_px_constraint (List.rev_append inequalities_flows inequalities_constant) in
	
	(* Print some information *)
	if verbose_mode_greater Verbose_total then(
		print_message Verbose_total ("Creating linear constraint for time elapsing with explicit flows…");
		print_message Verbose_total (LinearConstraint.string_of_px_linear_constraint model.variable_names time_polyhedron);
	);
	
	(* Return result *)
	time_polyhedron



let apply_time_shift (direction : time_direction) (location : Location.global_location) (the_constraint : LinearConstraint.pxd_linear_constraint) =
	(* Get the model *)
	let model = Input.get_model() in

	(* If urgent: no time elapsing *)
	if is_location_urgent location then (
		print_message Verbose_high ("Location urgent: NO time " ^ (string_of_time_direction direction));
		()
	(* If not urgent: apply time elapsing *)
	)else(
		(* If normal PTA, i.e., without stopwatches nor flows: directly call using the static polyhedron *)
		if not model.has_non_1rate_clocks then(
			(* Get the statically computed time elapsing polyhedron *)
			let time_polyhedron =
				(* Choose the right variable depending on time direction *)
				let appropriate_variable = match direction with
					| Forward	-> !time_elapsing_polyhedron
					| Backward	-> !time_past_polyhedron
				in
				match appropriate_variable with
				| Some polyedron -> polyedron
				| None -> raise (InternalError "The static polyhedron for time elapsing should have been computed in function `apply_time_shift`.")
			in
			
			(* Apply time elapsing *)
			LinearConstraint.pxd_time_elapse_assign_wrt_polyhedron time_polyhedron the_constraint;
		
		)else(			
			(* Otherwise, compute dynamically the list of clocks with their respective flow *)
			
			(* Create the time polyhedron depending on the clocks *)
			let time_polyhedron = pxd_compute_time_polyhedron direction location in
			
			(* Perform time elapsing *)
			print_message Verbose_high ("Now applying time " ^ (string_of_time_direction direction) ^ "…");
			
			(* Apply time elapsing *)
			LinearConstraint.pxd_time_elapse_assign_wrt_polyhedron time_polyhedron the_constraint;
			
			(* Print some information *)
			if verbose_mode_greater Verbose_total then(
				print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names the_constraint);
			);
			()
		)
	)


(*------------------------------------------------------------*)
(** Apply time elapsing in location to the_constraint (the location is needed to retrieve the stopwatches stopped in this location) *)
(*------------------------------------------------------------*)
let apply_time_elapsing = apply_time_shift Forward


(*------------------------------------------------------------*)
(** Apply time past in location to the_constraint (the location is needed to retrieve the stopwatches stopped in this location) *)
(*------------------------------------------------------------*)
let apply_time_past = apply_time_shift Backward





(*------------------------------------------------------------*)
(** Apply time elapsing in location to a concrete valuation (the location is needed to retrieve the stopwatches stopped in this location) *)
(*------------------------------------------------------------*)
let apply_time_elapsing_to_concrete_valuation (location : Location.global_location) (time_elapsing : NumConst.t) (px_valuation : LinearConstraint.px_valuation) =
	(* Get the model *)
	let model = Input.get_model() in

	(* If urgent location: nothing to change, i.e., copy *)
	if is_location_urgent location then(
		print_message Verbose_medium ("Urgent location: do not apply time elapsing");
		px_valuation
	)
	else(
		(* First, recreate a data structure *)
		let valuation_array = Array.make (model.nb_parameters + model.nb_clocks) NumConst.zero in
		
		(* Copy parameters (unchanged) *)
		(*** WARNING: depends on the internal representation of IMITATOR (first parameters, then clocks) ***)
		for variable_index = 0 to model.nb_parameters - 1 do
			valuation_array.(variable_index) <- px_valuation variable_index;
		done;

		(* Compute the set of stopped and elapsing clocks in this location *)
		let stopped_clocks, _ = compute_stopwatches location in
		
		(* Iterate on clocks *)
		for variable_index = model.nb_parameters to model.nb_parameters + model.nb_clocks - 1 do
			if List.mem variable_index stopped_clocks then(
				(* Clock stopped: copy *)
				valuation_array.(variable_index) <- px_valuation variable_index;
			)else(
				(* Elapsing clock: increment px_valuation by time_elapsing *)
				valuation_array.(variable_index) <- NumConst.add (px_valuation variable_index) time_elapsing;
			);
		done;
		
		(* Return a functional view *)
		(fun variable_index -> valuation_array.(variable_index))
	)



	
	
(*------------------------------------------------------------*)
(** Compute the initial state with the initial invariants and time elapsing *)
(*------------------------------------------------------------*)
let create_initial_state () : state =
	(* Retrieve the model *)
	let model = Input.get_model() in
	(* Retrieve the input options *)
	let options = Input.get_options () in

	(* Get the declared init state with initial constraint C_0(X) *)
	let initial_location = model.initial_location in
	let initial_constraint = model.initial_constraint in

    (* Get model invariants for the target location *)
    let initial_invariants = get_model_invariants initial_location in
    (* Check if the discrete invariants are all satisfied *)
    let is_discrete_initial_invariants_satisfied = is_discrete_guards_satisfied initial_location initial_invariants in

    (* Initial invariant is not satisfied, we raise an exception ! *)
    if not (is_discrete_initial_invariants_satisfied) then(
        raise UnsatisfiableInitialState
    );

	(* Extend dimensions for discrete *)
	let initial_constraint = LinearConstraint.pxd_of_px_constraint initial_constraint in

	(* Compute the invariants I_l0(X) for the initial locations *)
	print_message Verbose_high ("\nComputing initial invariant I_l0(X)");
	(* Create the invariant *)
	let invariant = compute_plain_continuous_invariant initial_location in
	(* Print some information *)
	if verbose_mode_greater Verbose_total then
		print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names invariant);

	(* Compute constraint for assigning a (constant) value to discrete variables *)
	print_message Verbose_high ("Computing constraint for discrete variables");
	let discrete_constraint = discrete_constraint_of_global_location initial_location in
	(* Print some information *)
	if verbose_mode_greater Verbose_total then
		print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names discrete_constraint);

	(* Perform intersection of C(X) and I_l0(X) and D_i = d_i *)
	print_message Verbose_high ("Performing intersection of C0(X) and I_l0(X) and D_i = d_i");
	let current_constraint = LinearConstraint.pxd_intersection [initial_constraint ; invariant ; discrete_constraint (*** TO OPTIMIZE: could be removed ***)] in
	(* Print some information *)
	if verbose_mode_greater Verbose_total then
		print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_constraint);


	(*--- BEGIN only if time elapsing ---*)
	if not options#no_time_elapsing then(
		(* Perform time elapsing *)
		print_message Verbose_high ("Applying time elapsing to [ C0(X) and I_l0(X) and D_i = d_i ]");
		apply_time_elapsing initial_location current_constraint;

(*		(* Compute the list of stopwatches *)
		let stopped_clocks, elapsing_clocks = compute_stopwatches initial_location in
		print_message Verbose_high ("Computing list of stopwatches");
		if verbose_mode_greater Verbose_total then(
			let list_of_names = List.map model.variable_names stopped_clocks in
			print_message Verbose_total ("Stopped clocks : " ^ (string_of_list_of_string_with_sep ", " list_of_names));
			let list_of_names = List.map model.variable_names elapsing_clocks in
			print_message Verbose_total ("Elapsing clocks: " ^ (string_of_list_of_string_with_sep ", " list_of_names));
		);

		LinearConstraint.pxd_time_elapse_assign (*model.clocks model.parameters_and_discrete*)
			elapsing_clocks
			(List.rev_append stopped_clocks model.parameters_and_discrete)
			current_constraint
		;
		(* Print some information *)
		if verbose_mode_greater Verbose_total then
			print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_constraint);*)


		(* Perform intersection of [C(X) and I_l0(X) and D_i = d_i]time with I_l0(X) and D_i = d_i *)
		(*** NOTE: intersection NOT necessary in absence of time elapsing, because the same I_l0(X) and D_i = d_i were intersected earlier ***)
		print_message Verbose_high ("Performing intersection of [C0(X) and I_l0(X) and D_i = d_i]time and I_l0(X) and D_i = d_i");
		LinearConstraint.pxd_intersection_assign current_constraint [invariant ; discrete_constraint];
		(* Print some information *)
		if verbose_mode_greater Verbose_total then
			print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_constraint);
	);

	(*--- END only if time elapsing ---*)

	(* Hide discrete *)
	print_message Verbose_high ("Hide discrete");
	let current_constraint = LinearConstraint.pxd_hide_discrete_and_collapse (*model.discrete*) current_constraint in
	(* Print some information *)
	if verbose_mode_greater Verbose_total then
		print_message Verbose_total (LinearConstraint.string_of_px_linear_constraint model.variable_names current_constraint);


	(* Remove useless clocks (if option activated) *)
	if options#dynamic_clock_elimination then(
		ClocksElimination.dynamic_clock_elimination initial_location current_constraint;
	);


	(* Return the initial state *)
	{global_location = initial_location; px_constraint = current_constraint}



(*------------------------------------------------------------*)
(* Compute the initial state with the initial invariants and time elapsing, and check whether it is satisfiable; if not, raise UnsatisfiableInitialState *)
(*------------------------------------------------------------*)
let compute_initial_state_or_abort () : state =
	(* Retrieve the model *)
	let model = Input.get_model() in
	(* Retrieve the input options *)
	let options = Input.get_options () in
	
	(*** QUITE A HACK! Strange to have it here ***)
	(* If normal PTA, i.e., without stopwatches nor flows, compute once for all the static time elapsing polyhedron *)
	if not model.has_non_1rate_clocks then(
		let variables_elapse		= model.clocks in
		let variables_constant		= model.parameters_and_discrete in
		let time_el_polyhedron		= generate_polyhedron_time_elapsing_pta Forward variables_elapse variables_constant in
		let time_pa_polyhedron		= generate_polyhedron_time_elapsing_pta Backward variables_elapse variables_constant in
		
		(* Print some information *)
		if verbose_mode_greater Verbose_high then(
			print_message Verbose_high "Computed the static time elapsing polyhedron:";
			print_message Verbose_high (LinearConstraint.string_of_pxd_linear_constraint model.variable_names time_el_polyhedron);
			print_message Verbose_high "";
			print_message Verbose_high "Computed the static time past polyhedron:";
			print_message Verbose_high (LinearConstraint.string_of_pxd_linear_constraint model.variable_names time_pa_polyhedron);
			print_message Verbose_high "";
		);
		
		(* Save them *)
		time_elapsing_polyhedron	:= Some time_el_polyhedron;
		time_past_polyhedron 		:= Some time_pa_polyhedron;
	
	);


	(* Print the initial state *)
	if verbose_mode_greater Verbose_medium then
		print_message Verbose_medium ("\nInitial state:\n" ^ (ModelPrinter.string_of_state model {global_location = model.initial_location; px_constraint = model.initial_constraint}) ^ "\n");

	(* Check the satisfiability *)
	if not (LinearConstraint.px_is_satisfiable model.initial_constraint) then (
		print_warning "The initial constraint of the model is not satisfiable.";
		raise (UnsatisfiableInitialState);
	)else(
		print_message Verbose_total ("\nThe initial constraint of the model is satisfiable.");
	);

	(* Get the initial state after time elapsing *)
	let init_state_after_time_elapsing : state = create_initial_state () in
	let initial_constraint_after_time_elapsing = init_state_after_time_elapsing.px_constraint in


	(* Check the satisfiability *)
	let begin_message = "The initial constraint of the model after invariant " ^ (if not options#no_time_elapsing then "and time elapsing " else "") in
	if not (LinearConstraint.px_is_satisfiable initial_constraint_after_time_elapsing) then (
		print_warning (begin_message ^ "is not satisfiable.");
		raise (UnsatisfiableInitialState);
	)else(
		print_message Verbose_total ("\n" ^ begin_message ^ "is satisfiable.");
	);
	(* Print the initial state after time elapsing *)
	if verbose_mode_greater Verbose_medium then
		print_message Verbose_medium ("\nInitial state computed:\n" ^ (ModelPrinter.string_of_state model init_state_after_time_elapsing) ^ "\n");

	(* Return the initial state *)
	init_state_after_time_elapsing


(*------------------------------------------------------------*)
(* Compute a list of possible actions for a state   *)
(*------------------------------------------------------------*)
let compute_possible_actions source_location =
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* Create a boolean array for the possible actions *)
	let possible_actions = Array.make model.nb_actions false in
	(* Fill it with all the possible actions per location *)
	for automaton_index = 0 to model.nb_automata - 1 do
		(* Get the current location for automaton_index *)
		let location_index = Location.get_location source_location automaton_index in
		(* Print some information *)
		print_message Verbose_total ("Considering automaton " ^ (model.automata_names automaton_index) ^ " with location " ^ (model.location_names automaton_index location_index) ^ ".");
		(* Get the possible actions for this location *)
		let possible_actions_for_this_automaton =
			model.actions_per_location automaton_index location_index
		in
		(* Add all the actions to our array *)
		List.iter (fun action_index ->
			(* Add the action *)
			possible_actions.(action_index) <- true;
			(* Print some information *)
			print_message Verbose_total ("Adding action " ^ (model.action_names action_index) ^ " for automaton " ^ (model.automata_names automaton_index) ^ " with location " ^ (model.location_names automaton_index location_index) ^ ".");
		) possible_actions_for_this_automaton;
	done;
	(* Print some information *)
	if verbose_mode_greater Verbose_total then (
		print_message Verbose_total ("Possible actions for all the locations are:");
		Array.iteri (fun action_index possible ->
			if possible then (print_message Verbose_total (" - " ^ (model.action_names action_index)));
		) possible_actions;
	);
	(* Remove every action where an automaton can not take this action in its *)
	(*  location although the action was declared for this automaton          *)
	let possible_actions = Array.mapi (fun action_index possible ->
		(* If this action is not possible, then false *)
		if not possible then false else(
		let automata_for_this_action = model.automata_per_action action_index in
		(* Check if the action is possible for all the automata for which it is defined *)
		(**** TO OPTIMIZE: no need to keep searching if not "still_possible" anymore ****)
		let action_possible =
			List.fold_left (fun still_possible automaton_index ->
				still_possible
				&& (List.mem action_index (model.actions_per_location automaton_index (Location.get_location source_location automaton_index)))
			) possible automata_for_this_action in
		(* Print some information *)
		if not action_possible && (verbose_mode_greater Verbose_total) then (
			print_message Verbose_total ("But action '" ^ (model.action_names action_index) ^ "' is not possible for all declared automata.")
		);
		(* Replace the previous value by the new one *)
		action_possible
		)
	) possible_actions in
	(* Make a list *)
	true_indexes possible_actions

(* interface with the NumConst module for discrete comparisons *)
let compute_discrete_comparisons (relop : DiscreteExpressions.relop) =
	match relop with
	| OP_L		-> NumConst.l
	| OP_LEQ	-> NumConst.le
	| OP_EQ		->  NumConst.equal
	| OP_NEQ	-> NumConst.neq
	| OP_GEQ	-> NumConst.ge
	| OP_G		-> NumConst.g

(** Merge two clock_updates - NOTE: conflict resolution done by apply_updates_assign *)
let merge_clock_updates first_update second_update : clock_updates =
  match first_update, second_update with
  | No_update, _ -> second_update
  | _ , No_update -> first_update
  | Resets r1, Resets r2 -> Resets (list_append r1 r2)
  | Updates u1, Updates u2 -> Updates (list_append u2 u2)
  (** convert resets into updates *)
  | Resets r, Updates u
  | Updates u, Resets r -> let members = List.map (fun i -> (i, LinearConstraint.make_pxd_linear_term [(NumConst.one, i)] NumConst.zero)) r in
    Updates (list_append members u)

(*------------------------------------------------------------------*)
(* Get the list of updates from ONE transition                      *)
(* Function by Jaime Arias (moved by Étienne André)                 *)
(* source_location   : the original location, needed to test the Boolean expressions*)
(* updates           : the list of updates                          *)
(*------------------------------------------------------------------*)
(* Returns a pair of the list of clock updates and discrete updates *)
(*------------------------------------------------------------------*)
(** Collecting the updates by evaluating the conditions, if there is any *)
let get_updates (source_location : Location.global_location) (updates : AbstractModel.updates) =
	List.fold_left (
	fun (acc_clock, acc_discrete) (conditional_update : AbstractModel.conditional_update) ->
		let boolean_expr, if_updates, else_updates = conditional_update in
		let filter_updates = if (DiscreteExpressionEvaluator.is_boolean_expression_satisfied (Location.get_discrete_value source_location) boolean_expr) then if_updates else else_updates in
		(merge_clock_updates acc_clock filter_updates.clock, list_append acc_discrete filter_updates.discrete)
	) (updates.clock, updates.discrete) updates.conditional


(*------------------------------------------------------------------*)
(* Get the list of updates from a combined transition               *)
(* Function by Étienne André                                        *)
(* source_location  : the original location, needed to test the Boolean expressions*)
(* combined_transition: the combined_transition in which the updates are sought *)
(*------------------------------------------------------------------*)
(* Returns a pair of the list of clock updates and discrete updates *)
(*------------------------------------------------------------------*)
(** Collecting the updates by evaluating the conditions, if there is any *)
let get_updates_in_combined_transition (source_location : Location.global_location) (combined_transition : StateSpace.combined_transition) =
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* Iterate on each transition of the combined_transition *)
	List.fold_left (
	fun (current_clock_updates, current_discrete_updates) (transition : AbstractModel.transition_index) ->
		(* Get updates *)
		let updates = (model.transitions_description transition).updates in
		(* Call dedicated function *)
		let new_clock_updates, new_discrete_updates = get_updates source_location updates in
		(* Append and merge *)
		(merge_clock_updates current_clock_updates new_clock_updates) , (list_append current_discrete_updates new_discrete_updates)
	) (No_update, []) combined_transition


(*------------------------------------------------------------------*)
(* Compute a new location for a combined_transition                 *)
(* combined_transition: the transition involved                     *)
(* source_location    : the source location                         *)
(*------------------------------------------------------------------*)
(* returns the new location, the discrete guards (a list of d_linear_constraint), the continuous guards (a list of pxd_linear_constraint) and the updates *)
(*------------------------------------------------------------------*)
let compute_new_location_guards_updates (source_location: Location.global_location) (combined_transition : StateSpace.combined_transition) : (Location.global_location * NonlinearConstraint.nonlinear_constraint list * LinearConstraint.pxd_linear_constraint list * AbstractModel.clock_updates list) =
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* make a copy of the location *)
	let location = Location.copy_location source_location in
	(* Create a temporary hashtbl for discrete values *)
	let updated_discrete = Hashtbl.create model.nb_discrete in
	(* Check if we actually have updates *)
	let has_updates = ref false in
	(* Update the location for the automata synchronized with 'action_index'; return the list of guards and updates *)
	let guards_and_updates = List.map (fun transition_index ->
		(* Get the automaton concerned *)
		let automaton_index = model.automaton_of_transition transition_index in
		
		(* Access the transition and get the components *)
		let transition = model.transitions_description transition_index in
		let guard, updates, target_index = transition.guard, transition.updates, transition.target in

		(** Collecting the updates by evaluating the conditions, if there is any *)
		let clock_updates, discrete_updates = get_updates source_location updates in
      
		(* Update discrete *)
		List.iter (fun (discrete_index, global_expression) ->

			(* Compute its new value *)
			let new_value =
			DiscreteExpressionEvaluator.eval_global_expression (Location.get_discrete_value source_location) global_expression
			in

			(* Check if already updated *)
			if Hashtbl.mem updated_discrete discrete_index then (
				(* Find its value *)
				let previous_new_value = Hashtbl.find updated_discrete discrete_index in
				(* Compare with the new one *)
				if DiscreteValue.neq previous_new_value new_value then (
				(* If different: warning *)
					let action_index = StateSpace.get_action_from_combined_transition combined_transition in
					print_warning ("The discrete variable '" ^ (model.variable_names discrete_index) ^ "' is updated several times with different values for the same synchronized action '" ^ (model.action_names action_index) ^ "'. The behavior of the system is now unspecified.");
				);
			) else (
				(* Else keep it in memory for update *)
				Hashtbl.add updated_discrete discrete_index new_value;
			);
		) discrete_updates;
		(* Update the global location *)
		Location.update_location_with [automaton_index, target_index] [] location;
		(* Update the update flag *)
		begin
		match clock_updates with
			(* Some updates? *)
			| Resets (_ :: _)
			| Updates (_ :: _) -> has_updates := true
			(* Otherwise: no update *)
			| No_update
			| Resets []
			| Updates [] -> ()
		end;
		(* Keep the guard and updates  *)
		(guard, clock_updates)
	) combined_transition in
	
	(* Split the list of guards and updates *)
	let guards, clock_updates = List.split guards_and_updates in
	
	(* Compute pairs to update the discrete variables *)
	let updated_discrete_pairs = ref [] in
	Hashtbl.iter (fun discrete_index discrete_value ->
		updated_discrete_pairs := (discrete_index, discrete_value) :: !updated_discrete_pairs;
	) updated_discrete;

	(* Update the global location *)
	Location.update_location_with [] !updated_discrete_pairs location;

	(* Split guards between discrete and continuous *)
	let discrete_guards, continuous_guards = split_guards_into_discrete_and_continuous guards in

	(* Return the new location, the guards, and the clock updates (if any!) *)
	location, discrete_guards, continuous_guards, (if !has_updates then clock_updates else [])




(*------------------------------------------------------------*)
(* Compute the new constraint for a transition                *)
(* source_constraint : contraint in source location           *)
(* discrete_constr_src : contraint D_i = d_i in source location (discrete variables) *)
(* orig_location   : source location                          *)
(* target_location : target location                          *)
(* guards          : guard constraints per automaton          *)
(* clock_updates   : updated clock variables                  *)
(*------------------------------------------------------------*)
(*** TODO: remove the model from the arguments, and retrieve it ***)
let compute_new_constraint (source_constraint : LinearConstraint.px_linear_constraint) (discrete_constr_src : LinearConstraint.pxd_linear_constraint) (orig_location : Location.global_location) (target_location : Location.global_location) guards clock_updates =
	(* Retrieve the model *)
	let model = Input.get_model() in
	(* Retrieve the input options *)
	let options = Input.get_options () in

	if verbose_mode_greater Verbose_total then(
		print_message Verbose_total ("\n***********************************");
		print_message Verbose_total ("Entering compute_new_constraint");
		print_message Verbose_total ("***********************************");
		print_message Verbose_total ("C = " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names source_constraint ));
	);
	(* The constraint is checked on the fly for satisfiability -> exception mechanism *)
	try (
		(* Retrieve the original constraint *)
		(*** WARNING / VERY IMPORTANT: copy!!! (in fact convert, which is also a copy) ***)
		let source_constraint_with_maybe_time_elapsing = LinearConstraint.pxd_of_px_constraint source_constraint in

		(* Alternative IMITATOR semantics for time-elapsing: apply time-elapsing NOW, and intersect with invariant *)
		if options#no_time_elapsing then(

			(* If special clock to be reset at each transition: reset it now! *)
			begin
			match model.special_reset_clock with
				| None -> ()
				| Some clock_index ->
				(* Reset it *)
					print_message Verbose_medium "Resetting the special reset clock…";
					apply_updates_assign source_constraint_with_maybe_time_elapsing [Resets [clock_index]];
			end;

			print_message Verbose_total ("\nAlternative time elapsing: Applying time elapsing NOW");
			apply_time_elapsing orig_location source_constraint_with_maybe_time_elapsing;

			(* Compute the invariant in the source location I_l(X) *)
			(*** TO OPTIMIZE!!! This should be done only once in the function calling this function!! ***)
			print_message Verbose_total ("\nComputing invariant I_l(X)");
			let invariant = compute_invariant orig_location in
			(* Print some information *)
			if verbose_mode_greater Verbose_total then(
				print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names invariant);
			);

			(* Perform the intersection *)
			print_message Verbose_total ("\nAlternative time elapsing: performing intersection of C(X)time and I_l(X)");
			LinearConstraint.pxd_intersection_assign source_constraint_with_maybe_time_elapsing [invariant];
		);


		let current_constraint = LinearConstraint.pxd_copy discrete_constr_src in

		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total ("\nComputing the guards g(x)");
			List.iter (fun guard ->
				print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names guard);
			) guards;
		);

		print_message Verbose_total ("\nPerforming intersection of Di = di and C(X) and g(X)");
		(* Add the (old) value for discrete to the guards D_i = d_i and g(X) *)
		LinearConstraint.pxd_intersection_assign current_constraint (source_constraint_with_maybe_time_elapsing :: guards);
		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_constraint);
		);

		(* Check here for unsatisfiability *)
		if not (LinearConstraint.pxd_is_satisfiable current_constraint) then (
			(* Statistics *)
			counter_nb_unsat1#increment;
			print_message Verbose_high "skip transition";
			raise Unsat_exception
		);

		print_message Verbose_total ("\nEliminate the discrete variables in C(X) and g(X)");
		(* Remove the discrete variables (Exists D_i : D_i = d_i and g(X)) *)
		LinearConstraint.pxd_hide_assign model.discrete current_constraint;
		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_constraint);
		);

		print_message Verbose_total ("\nProjecting C(X) and g(X) onto rho");
		apply_updates_assign current_constraint clock_updates;
		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total ("\nResult:");
			print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_constraint);
		);

		(* Compute the invariant in the target location I_l'(X) *)
		print_message Verbose_total ("\nComputing invariant I_l'(X)");
		let invariant = compute_invariant target_location in
		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names invariant);
		);

		(* Perform the intersection *)
		print_message Verbose_total ("\nPerforming intersection of [C(X) and g(X)]rho and I_l'(X)");
		(* (Exists D_i : D_i = d_i and g(X)) *)
		LinearConstraint.pxd_intersection_assign current_constraint [invariant];
		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_constraint);
			if not (LinearConstraint.pxd_is_satisfiable current_constraint) then
				print_message Verbose_total ("This constraint is NOT satisfiable (after intersection of [C(X) and g(X)] rho and I_l'(X) ).");
		);
		(*** NOTE: NO USE FOR TESTING HERE FOR SATISFIABILITY (almost always satisfiable from my experiments) -- ÉA ***)


		(* Normal IMITATOR semantics for time-elapsing: apply time-elapsing now *)
		if not options#no_time_elapsing then(
			print_message Verbose_high ("Applying time elapsing to [C(X) and g(X)]rho and I_l'(X) ]");
			apply_time_elapsing target_location current_constraint;
		);


		(* Compute the equalities for the discrete variables in target location *)
		let discrete_constraint_target = discrete_constraint_of_global_location target_location in

		(* Perform the intersection *)
		print_message Verbose_total ("\nPerforming intersection of the constraint with D_i = d_i and I_l'(X) ");
		LinearConstraint.pxd_intersection_assign current_constraint
			[
				discrete_constraint_target;
				(*** NOTE: in principle, no need to intersect with invariant if time elapsing was NOT applied (alternating semantics). This could be improved (and tested) in the future. ***)
				invariant;
			];

		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_constraint);
			if not (LinearConstraint.pxd_is_satisfiable current_constraint) then
				print_message Verbose_total ("This constraint is NOT satisfiable (after intersection of the constraint with D_i = d_i and I_l'(X)).");
		);

(*		(* Check here for unsatisfiability *)
		if not (LinearConstraint.is_satisfiable current_constraint) then (
			(* Statistics *)
			nb_unsat2 := !nb_unsat2 + 1;
			print_message Verbose_high "skip transition";
			raise Unsat_exception
		);*)

		(* AGAIN, NO USE FOR TESTING HERE FOR SATISFIABILITY (almost always satisfiable) *)

		(* Hide discrete' *)
		print_message Verbose_total ("\nHide discrete variables ");
		let current_constraint = LinearConstraint.pxd_hide_discrete_and_collapse (*(model.discrete)*) current_constraint in
		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total (LinearConstraint.string_of_px_linear_constraint model.variable_names current_constraint);
			if not (LinearConstraint.px_is_satisfiable current_constraint) then
				print_message Verbose_total ("This constraint is NOT satisfiable (after hiding discrete variables).");
		);


		(* Remove useless clocks (if option activated) *)
		(*** WARNING: code duplication!!! ***)
		if options#dynamic_clock_elimination then(
			ClocksElimination.dynamic_clock_elimination target_location current_constraint;
		);


		(* return the final constraint *)
		Some current_constraint
	) with Unsat_exception -> None


(*------------------------------------------------------------*)
(* Computes next combination of indices           *)
(* current_indexes : combination                  *)
(* max_indexes     : maximum indices              *)
(*------------------------------------------------------------*)
(* returns a boolean, indicating that the         *)
(* new combination is valid (false if the old     *)
(* combination was the last one)                  *)
(*------------------------------------------------------------*)
let next_combination combination max_indexes =
	let len = Array.length combination in
	let valid_combination = ref true in
	let not_is_max = ref true in
	let local_index = ref 0 in
	while !not_is_max do
		(* Look for the first index to be incremented *)
		if combination.(!local_index) < max_indexes.(!local_index) then(
			(* Increment this index *)
			combination.(!local_index) <- combination.(!local_index) + 1;
			(* Reset the smaller indexes to 0 *)
			for i = 0 to !local_index - 1 do
				combination.(i) <- 0;
			done;
			(* Stop the loop *)
			not_is_max := false;
		) else (
			local_index := !local_index + 1;
			if !local_index >= len then(
				valid_combination := false;
				not_is_max := false;
			)
		)
	done; (* end while *)
	!valid_combination

(*------------------------------------------------------------*)
(* Computes all possible transition combinations for the *)
(* involved automata.                                    *)
(* constr               : current state constraint       *)
(* action index         : index of current action        *)
(* automata             : involved automata              *)
(* aut_table            : array of automata              *)
(* max_indexes          : array of maximal trans. indices*)
(* possible_transitions : array of transition indices    *)
(*------------------------------------------------------------*)
(* returns a bool, indicating iff at least one legal     *)
(* combination exists.                                   *)
(*------------------------------------------------------------*)
let compute_transitions location constr action_index automata involved_automata_indices max_indexes possible_transitions  =
	(* Retrieve the model *)
	let model = Input.get_model() in

	let current_index = ref 0 in
	(* Stop computation as soon as one automaton has no legal transition left. *)
	try (
		List.iter (fun automaton_index ->
			(* Tabulate the real index *)
			involved_automata_indices.(!current_index) <- automaton_index;
			(* Get the current location for this automaton *)
			let location_index = Location.get_location location automaton_index in
			(* Get transitions for this automaton *)
			let transitions = List.map model.transitions_description (model.transitions automaton_index location_index action_index) in

			(* REMOVED 2011/11/21 : computation always slower ; might be faster for strongly branching systems? EXCEPT FOR LSV.imi --> put it back! *)
			(* Keep only possible transitions *)
			let is_possible = fun trans -> (
				let guard = trans.guard in

				(* First check whether the discrete part is possible *)
				let discrete_part_possible = is_discrete_guard_satisfied location guard in

				if not discrete_part_possible then(
					(* Statistics *)
					counter_nb_early_unsatisfiable_discrete#increment;
					print_message Verbose_medium "** early skip transition (discrete guard unsatisfiable) **";
					false
				)else(
				(* Else: the discrete part is satisfiable; so now we check the continuous intersection between the current constraint and the discrete + continuous outgoing guard *)
				(*** TODO: check if this test is really worth it ***)
					let is_possible = is_constraint_and_continuous_guard_satisfiable constr guard in
					if not is_possible then (
						(* Statistics *)
						counter_nb_early_unsatisfiable#increment;
						print_message Verbose_medium "** early skip transition (constraint+guard unsatisfiable) **"
					);
					is_possible
				)
			) in
			let legal_transitions = ref [] in
			let trans_index = ref 0 in
			List.iter (fun trans ->
				if is_possible trans then(
					legal_transitions := !trans_index :: !legal_transitions;
				);
				trans_index := !trans_index + 1
			) transitions;
			(* Stop computation if no legal transition exists *)
			if !legal_transitions = [] then (
				(* Statistics *)
				counter_nb_early_skip#increment;
				print_message Verbose_medium "*** early skip action ***";
				raise Unsat_exception
			);
			(* Store possible transitions *)
			possible_transitions.(!current_index) <- !legal_transitions;
			(* Tabulate the number of transitions for this location *)
			max_indexes.(!current_index) <-	List.length !legal_transitions - 1;
			(* Increment the index *)
			current_index := !current_index + 1;
		) automata;
		(* arrived here, so each automaton must have at least one legal transition *)
		true
	) with Unsat_exception -> false



(*------------------------------------------------------------*)
(* Computes the (unique) successor via a combined transition. *)
(* source_location      : the source location                 *)
(* source_constraint    : the source px-constraint            *)
(* discrete_constr      : the source state D_i=d_i            *)
(* combined_transition  : the combined transition             *)
(*------------------------------------------------------------*)
(* returns Some state if satisfiable, None otherwise          *)
(*------------------------------------------------------------*)

let post_from_one_state_via_one_transition (source_location : Location.global_location) (source_constraint : LinearConstraint.px_linear_constraint) (discrete_constr : LinearConstraint.pxd_linear_constraint) (combined_transition : StateSpace.combined_transition) : State.state option =

	(* Compute the new location for the current combination of transitions *)
	let target_location, (discrete_guards : NonlinearConstraint.nonlinear_constraint list), (continuous_guards : LinearConstraint.pxd_linear_constraint list), clock_updates = compute_new_location_guards_updates source_location combined_transition in

	(* Statistics *)
	tcounter_compute_location_guards_discrete#stop;

	(* Check if the discrete guards are satisfied *)
	if not (List.for_all (evaluate_d_nonlinear_constraint_in_location source_location) discrete_guards) then(
		(* Statistics *)
		counter_nb_unsatisfiable_discrete#increment;
		(* Print some information *)
		print_message Verbose_high ("\nThis combination of discrete guards is not satisfiable.");

		(* Return *)
		None
		
	(* Else: the discrete part of guards is satisfied *)
	)else(

	    (* Get model invariants for the target location *)
	    let target_invariants = get_model_invariants target_location in
	    (* Check if the discrete invariants are all satisfied *)
        let is_discrete_target_invariants_satisfied = is_discrete_guards_satisfied target_location target_invariants in

        (* Check if the discrete invariants are satisfied *)
        if not (is_discrete_target_invariants_satisfied) then(
            (* Statistics *)
            counter_nb_unsatisfiable_discrete_invariants#increment;
            (* Print some information *)
            print_message Verbose_high ("\nThis combination of discrete target invariants is not satisfiable.");

            (* Return *)
            None

        (* Else: the discrete part of target invariant is satisfied *)
        )else(

		(* Compute the new constraint for the current transition *)
		let new_constraint = compute_new_constraint source_constraint discrete_constr source_location target_location continuous_guards clock_updates in

		(* Check the satisfiability *)
		match new_constraint with
			| None ->
				(* Statistics *)
				counter_nb_unsatisfiable#increment;

				(* Print some information *)
				print_message Verbose_high ("\nThis constraint is not satisfiable ('None').");
				
				(* Return *)
				None

			| Some (final_constraint : LinearConstraint.px_linear_constraint) -> (
				if not (LinearConstraint.px_is_satisfiable final_constraint) then(
					(* Statistics *)
					counter_nb_unsatisfiable#increment;

					(* Print some information *)
					print_message Verbose_high ("\nThis constraint is not satisfiable ('Some unsatisfiable').");
					
					(* Return *)
					None
				) else (
					(* Return the constraint *)
					Some { global_location = target_location ; px_constraint = final_constraint }
				); (* end if satisfiable *)
			) (* end if Some constraint *)
	    ) (* end discrete part of target invariant is satisfied *)
	) (* end discrete part of the guard is satisfied *)





(************************************************************)
(** Reconstruct a (valid) concrete run from a symbolic run *)
(************************************************************)


(*------------------------------------------------------------*)
(** Compute the predecessors of a zone *)
(*------------------------------------------------------------*)

(* `continuous_predecessor location_n initial_z_n z_n z_n_post` (where `z_n_post` is a set of "final" valuations of location n, `z_n` is the symbolic zone of location n, and `initial_z_n` is the set of admissible initial valuations for location n) computes the set of valuations at location n that are initial admissible valuations *and* that are predecessor (via time past) of valuations of `z_n_post`. If `z_n_post` is a single point, note that the result is a single point (or possibly a set of points) corresponding to valuations right when entering location n. *)
let continuous_predecessors
	(location_n			: Location.global_location)
	(initial_z_n		: LinearConstraint.px_linear_constraint)
	(z_n				: LinearConstraint.px_linear_constraint)
	(z_n_post			: LinearConstraint.px_linear_constraint)
		: LinearConstraint.px_linear_constraint
		=
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* Copy (for safety concerns) *)
	let current_pxd_constraint = LinearConstraint.px_copy z_n_post in

	(* Print some information *)
	if verbose_mode_greater Verbose_high then(
		print_message Verbose_medium ("Initial constraint: " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names current_pxd_constraint ) ^ "");
	);

	(* Step 1: Apply time past *)

	(* Create the time polyhedron at location n depending on the clocks *)
	let time_polyhedron : LinearConstraint.px_linear_constraint = px_compute_time_polyhedron Backward location_n in

	(* Apply time past *)
	print_message Verbose_total ("Applying time past…");

	(* Apply time past *)
	LinearConstraint.px_time_elapse_assign_wrt_polyhedron time_polyhedron current_pxd_constraint;

	(* Print some information *)
	if verbose_mode_greater Verbose_high then(
		print_message Verbose_high ("Applied timed past at state n:\n " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names current_pxd_constraint) ^ "");
	);

	(* Step 2: Intersect with invariant and admissible initial valuations *)

	(* Intersect with invariant n (NOTE: shorter: we can fact intersect with the symbolic state, that already contains the invariant!) AND intersect with initial admissible valuations *)
	(*** NOTE: if `initial_z_n` is already included into `z_n`, this latter could be used alone ***)
	LinearConstraint.px_intersection_assign current_pxd_constraint [z_n; initial_z_n];

	(* Return the constraint *)
	current_pxd_constraint


(* `discrete_predecessors state_n_minus_1 transition_n_minus_1_n initial_z_n` (where `initial_z_n` is a set of "initial" valuations of location n, `transition_n_minus_1_n` is the transition from n-1 to n, and `state_n_minus_1` is the symbolic state n-1) computes the set of valuations at location n-1 that are "final" admissible valuations *and* that are predecessor (via discrete successor) of valuations of `initial_z_n`. That is, the result is the set of points corresponding to valuations right before taking the transition from n-1 to n, and leading to `initial_z_n`. *)

let discrete_predecessors
	(state_n_minus_1		: State.state)
	(transition_n_minus_1_n	: StateSpace.combined_transition)
	(initial_z_n			: LinearConstraint.px_linear_constraint)
		: LinearConstraint.px_linear_constraint
		=
	(* Retrieve the model *)
	let model = Input.get_model() in

	(* Get location and constraint*)
	let location_n_minus_1 : Location.global_location					= state_n_minus_1.global_location in
	let z_n_minus_1			: LinearConstraint.px_linear_constraint		= state_n_minus_1.px_constraint in

	(*** BADPROG: multiple computations! ***)
	let _, _, (guards_n_minus_1_n : LinearConstraint.pxd_linear_constraint list), (updates_n_minus_1_n : AbstractModel.clock_updates list) = compute_new_location_guards_updates location_n_minus_1 transition_n_minus_1_n in

	(* Copy the constraint and convert to PXD *)
	let current_pxd_constraint = LinearConstraint.pxd_of_px_constraint initial_z_n in


	(* Step 1: Apply inverted updates *)

	(* Print some information *)
	if verbose_mode_greater Verbose_high then(
		print_message Verbose_medium ("Now applying updates backwards…");
	);

	(* Apply the inverted updates (from n-1 to n) *)
	apply_updates_assign_backward current_pxd_constraint updates_n_minus_1_n;

	(* Print some information *)
	if verbose_mode_greater Verbose_high then(
		print_message Verbose_high ("Updates were applied: " ^ (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_pxd_constraint) ^ "");
	);


	(* Step 2: Intersect with source guard and invariant *)

	(* Print some information *)
	if verbose_mode_greater Verbose_total then(
		print_message Verbose_total ("Now intersecting with source guard and source invariant…");
	);

	(* Intersect with the guard from n-1 to n, AND with the invariant at n-1 (NOTE: to simplify, we intersect with z_n_minus_1) *)
	LinearConstraint.pxd_intersection_assign current_pxd_constraint ((LinearConstraint.pxd_of_px_constraint z_n_minus_1) :: guards_n_minus_1_n);

	(* Print some information *)
	if verbose_mode_greater Verbose_high then(
		print_message Verbose_high ("After intersection with source guard and source invariant: " ^ (LinearConstraint.string_of_pxd_linear_constraint model.variable_names current_pxd_constraint) ^ "");
	);


	(* Step 3: Remove discrete *)

	(* Print some information *)
	if verbose_mode_greater Verbose_total then(
		print_message Verbose_total ("Removing discrete variables…");
	);

	(* Return a px-constraint *)
	let final_px_constraint = LinearConstraint.pxd_hide_discrete_and_collapse current_pxd_constraint in

	(* Print some information *)
	if verbose_mode_greater Verbose_high then(
		print_message Verbose_high ("After removing discrete variables: " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names final_px_constraint) ^ "");
	);

	(* Return result *)
	final_px_constraint



(* Rebuild the "initial admissible valuations" after taking a transition from state n-1 to n, i.e., apply guard and updates to z_n-1, and intersect with z_n *)
let compute_admissible_valuations_after_transition
		(state_n_minus_1		: State.state)
		(transition_n_minus_1_n	: StateSpace.combined_transition)
		(state_n				: State.state)
		: LinearConstraint.px_linear_constraint
	=

	(* Get location and constraint at n-1 and n *)
	let location_n_minus_1	: Location.global_location					= state_n_minus_1.global_location in
	let z_n_minus_1			: LinearConstraint.px_linear_constraint		= state_n_minus_1.px_constraint in
	let z_n					: LinearConstraint.px_linear_constraint		= state_n.px_constraint in

	(* Reconstruct guards and updates *)
	(*** BADPROG: multiple computations! ***)
	let _, _, (continuous_guards : LinearConstraint.pxd_linear_constraint list), (updates_n_minus_1 : AbstractModel.clock_updates list) = compute_new_location_guards_updates location_n_minus_1 transition_n_minus_1_n in

	(* Our goal: intersect the previous state (z_n_minus_1) with the guard, and then apply updates *)

	(* Compute the intersection of z_n-1 (mostly to get the invariant I_n-1) with the outgoing guard from n-1 to n *)
	let z_n_minus_1_and_continuous_guard : LinearConstraint.pxd_linear_constraint = LinearConstraint.pxd_intersection ((LinearConstraint.pxd_of_px_constraint z_n_minus_1) :: continuous_guards) in

	(* Apply updates *)
	apply_updates_assign z_n_minus_1_and_continuous_guard updates_n_minus_1;

	(* Remove discrete from n, as they can be different from discrete at n+1 *)
	let z_n_minus_1_and_continuous_guard_without_discrete : LinearConstraint.px_linear_constraint = LinearConstraint.pxd_hide_discrete_and_collapse z_n_minus_1_and_continuous_guard in

	(* Intersect with Z *)
	LinearConstraint.px_intersection_assign z_n_minus_1_and_continuous_guard_without_discrete [z_n];

	(* Return result *)
	z_n_minus_1_and_continuous_guard_without_discrete





(*------------------------------------------------------------*)
(** Convert a symbolic  run into a (valid) concrete run *)
(*------------------------------------------------------------*)

(*** NOTE: this function could be in StateSpace but that would create a circular dependency with ModelPrinter ***)

let concrete_run_of_symbolic_run (state_space : StateSpace.state_space) (predecessors : StateSpace.predecessors_table) (symbolic_run : StateSpace.symbolic_run) (concrete_target_px_valuation : LinearConstraint.px_valuation ) : StateSpace.concrete_run =
	(* Retrieve the model *)
	let model = Input.get_model() in
	
	(*** BEGIN CODE THAT WON'T WORK DUE TO THE DIMENSION HANDLING IN LINEAR.CONSTRAINT ***)
	(*
	(* 1. we backup the model *)
	let original_model = model in
	
	(* 2. We rebuild a model with one more clock *)
	(*** HACK (quite!) ***)
	let extra_clock = model.nb_variables in
	
	
	let px_clocks_non_negative = LinearConstraint.px_constraint_of_nonnegative_variables (original_model.clocks @ [extra_clock]) in
	
	(* Add >= 0 to the initial constraint *)
	let initial_constraint = LinearConstraint.px_intersection [original_model.initial_constraint ; TODO ] in
	
	let px_clocks_non_negative_and_initial_p_constraint = LinearConstraint.px_intersection [px_clocks_non_negative; (LinearConstraint.px_of_p_constraint original_model.initial_p_constraint)
	
	
	let model_with_one_extra_clock =
	{
		(* Cardinality *)
		nb_automata    = original_model.nb_automata;
		nb_actions     = original_model.nb_actions;
		nb_clocks      = original_model.nb_clocks + 1;
		nb_discrete    = original_model.nb_discrete;
		nb_parameters  = original_model.nb_parameters;
		nb_variables   = original_model.nb_variables + 1;
		nb_locations   = original_model.nb_locations;
		nb_transitions = original_model.nb_transitions;

		(* Is there any stopwatch in the model? *)
		has_non_1rate_clocks = original_model.has_non_1rate_clocks;
		(* Is the model an L/U-PTA? *)
		lu_status = original_model.lu_status;


		(* The observer *)
		observer_pta = original_model.observer_automaton;
		is_observer = original_model.is_observer;

		(* The list of clock indexes *)
		clocks = list_append original_model.clocks [extra_clock];
		(* True for clocks, false otherwise *)
		is_clock = fun variable_index -> if variable_index = extra_clock then true else original_model.is_clock variable_index;
		(* Index of the special clock to be reset at each transition to measure time elapsing (only used in NZ checking) *)
		special_reset_clock = original_model.special_reset_clock;
		(* Index of a special clock meant to measure the global time (how this clock is actually used is up to the model designer *)
		global_time_clock = original_model.global_time_clock;
		(* The list of clock indexes except the reset clock (used, e.g., to print the model *)
		clocks_without_special_reset_clock = list_append original_model.clocks_without_special_reset_clock [extra_clock];
		(* The list of discrete indexes *)
		discrete = original_model.discrete;
		(* True for discrete, false otherwise *)
		is_discrete = original_model.is_discrete;
		(* The list of parameter indexes *)
		parameters = original_model.parameters;
		(* The non parameters (clocks and discrete) *)
		clocks_and_discrete = list_append (list_append clocks discrete) [extra_clock];
		(* The non clocks (parameters and discrete) *)
		parameters_and_discrete = list_append parameters discrete;
		(* The non discrete (clocks and parameters) *)
		parameters_and_clocks = list_append (list_append parameters clocks) [extra_clock];
		(* The function : variable_index -> variable name *)
		variable_names = fun variable_index -> if variable_index = extra_clock then "x_absolute" else original_model.variable_names variable_index;
		(* The type of variables *)
		type_of_variables = fun variable_index -> if variable_index = extra_clock then Var_type_clock else original_model.type_of_variables variable_index;

		(* The automata *)
		automata = original_model.automata;
		(* The automata names *)
		automata_names = original_model.automata_names;

		(* The locations for each automaton *)
		locations_per_automaton = original_model.locations_per_automaton;
		(* The location names for each automaton *)
		location_names = original_model.location_names;
		(* The location names for each automaton *)
		(*** HACK ***)
		is_urgent = original_model.is_urgent;

		(* All action indexes *)
		actions = original_model.actions;
		(* Action names *)
		action_names = original_model.action_names;
		(* The type of actions *)
		action_types = original_model.action_types;
		(* The list of actions for each automaton *)
		actions_per_automaton = original_model.actions_per_automaton;
		(* The list of automatons for each action *)
		automata_per_action = original_model.automata_per_action;
		(* The list of actions for each automaton for each location *)
		actions_per_location = original_model.actions_per_location;

		(* The cost for each automaton and each location *)
		costs = original_model.costs;

		(* The invariant for each automaton and each location *)
		invariants = original_model.invariants;
		(* The transitions for each automaton and each location and each action *)
		transitions = original_model.transitions;
		(* The list of clocks stopped for each automaton and each location *)
		stopwatches = original_model.stopwatches;
		(* An array transition_index -> transition *)
		transitions_description = original_model.transitions_description;
		(* An array transition_index -> automaton_index *)
		automaton_of_transition = original_model.automaton_of_transition;

		(* All clocks non-negative *)
		px_clocks_non_negative = px_clocks_non_negative;
		(* Initial location of the model *)
		initial_location = original_model.initial_location;
		(* Initial constraint of the model *)
		initial_constraint = initial_constraint;
		(* Initial constraint of the model projected onto P *)
		initial_p_constraint = original_model.initial_p_constraint;
		(* Initial constraint of the model projected onto P and all clocks non-negative *)
		px_clocks_non_negative_and_initial_p_constraint = px_clocks_non_negative_and_initial_p_constraint;


		(* Property defined by the user *)
		user_property = original_model.property;
		(* Property defined by the model *)
		correctness_condition = original_model.correctness_condition;
		(* List of parameters to project the result onto *)
		projection = original_model.projection;
		(* Parameter to be minimized or maximized *)
		optimized_parameter = original_model.optimization;
	}
	in
	
	*)
	(*** END CODE THAT WON'T WORK DUE TO THE DIMENSION HANDLING IN LINEAR.CONSTRAINT ***)
	
	(* Get the final state *)
	let target_state_index = symbolic_run.final_state in
	let target_state = StateSpace.get_state state_space target_state_index in
	
	(* Reminder: symbolic_run contains n steps, followed by a final state (called n+1 in the following) *)


	(*------------------------------------------------------------*)
	(* Find the "initial" valuations of zn+1 *)
	(*------------------------------------------------------------*)

	(* Print some information *)
	if verbose_mode_greater Verbose_low then(
		print_message Verbose_medium ("");
		print_message Verbose_low ("Cancelling the time elapsing of the last valuation of the symbolic run…:\n " ^ (ModelPrinter.string_of_px_valuation model concrete_target_px_valuation) ^ "");
	);

	(* Step 0: get variables *)

	(* Get the location state_n_plus_1 *)
	let location_n_plus_1 = target_state.global_location in
	(* Print some information *)
	if verbose_mode_greater Verbose_medium then(
		print_message Verbose_medium ("Location n+1: " ^ (Location.string_of_location model.automata_names model.location_names model.variable_names Location.Exact_display location_n_plus_1));
	);
	
	(* Get the constraint at n+1 *)
	let z_n_plus_1 = target_state.px_constraint in
	(* Print some information *)
	if verbose_mode_greater Verbose_medium then(
		print_message Verbose_medium ("Z n+1: " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names z_n_plus_1) ^ "");
	);
	
	(* Get the "final" locations at n+1, i.e., the conversion into a polyhedron of the target point (after time elapsing) *)
	let z_n_plus_1_final : LinearConstraint.px_linear_constraint = LinearConstraint.px_constraint_of_point (List.map (fun variable_index -> variable_index , concrete_target_px_valuation variable_index) model.parameters_and_clocks) in
	(* Print some information *)
	if verbose_mode_greater Verbose_high then(
		print_message Verbose_high ("Starting from target valuations after time elapsing:\n " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names z_n_plus_1_final) ^ "");
	);
	

	(* Step 1: compute the set of admissible initial valuations at n+1 *)

	let admissible_initial_valuations : LinearConstraint.px_linear_constraint =
	(* Case of an empty run: just keep the initial constraint *)
	if symbolic_run.symbolic_steps = [] then(
		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total ("Symbolic run of length 0: the admissible initial valuations are given by the initial constraint:\n " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names model.initial_constraint) ^ "");
		);

		(* Re-intersect with the *initial* continuous valuations to indeed get an initial valuation *)
		model.initial_constraint
	)else(
	(* Case of a non-empty run: the initial admissible valuations are the predecessor constraint (location n) intersected with the guard from n to n+1, to which we apply updates from n to n+1, and then intersected with the constraint at location n+1 (mainly to have the invariant) *)
	
		let symbolic_step_n : StateSpace.symbolic_step 				= List.nth symbolic_run.symbolic_steps (List.length symbolic_run.symbolic_steps - 1) in
		let transition_n_n_plus_1 : StateSpace.combined_transition	= symbolic_step_n.transition in
		let state_n			: State.state							= StateSpace.get_state state_space symbolic_step_n.source in

		(* Call dedicated function *)
		let admissible_initial_valuations : LinearConstraint.px_linear_constraint = compute_admissible_valuations_after_transition state_n transition_n_n_plus_1 target_state in
		
		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total ("Intersected state n+1 with Z_n, and its incoming guard, and updated variables to n+1:\n " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names admissible_initial_valuations) ^ "");
		);

		admissible_initial_valuations
	)

	in

	(* Print some information *)
	if verbose_mode_greater Verbose_high then(
		print_message Verbose_high ("Admissible valuations:\n " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names admissible_initial_valuations) ^ "");
	);

	
	(* Step 2: cancelling time elapsing, i.e., compute continuous predecessors *)

	let valuations_n_plus_1_before_time_elapsing : LinearConstraint.px_linear_constraint = continuous_predecessors location_n_plus_1 admissible_initial_valuations z_n_plus_1 z_n_plus_1_final in

	(* Print some information *)
	if verbose_mode_greater Verbose_high then(
		print_message Verbose_high ("Valuations before time elapsing:\n " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names valuations_n_plus_1_before_time_elapsing) ^ "");
	);



	(*------------------------------------------------------------*)
	(* Pick one "initial" valuation of zn+1 *)
	(*------------------------------------------------------------*)

	(* To make things more human-friendly, we change the initial valuation only if it did not belong to the admissible "initial points" before time elapsing *)
	
	(* Print some information *)
	print_message Verbose_high ("Trying to make the valuation more friendly…");
	
	let concrete_target_px_valuation_before_time_elapsing =
		let recomputation_needed =
		(* If some non-1 flow clocks: might be wrong the keep the valuation, so recompute it (2021/03/11) *)
		if model.has_non_1rate_clocks then(
			(* Print some information *)
			print_message Verbose_high ("Oops! Non-1 flow clocks detected: better recompute a valuation within z_n_plus_1…");
			true
		)else(
			(* If intersection is empty, find new valuation *)
			if LinearConstraint.px_is_false (
				LinearConstraint.px_intersection[
					LinearConstraint.px_constraint_of_point (List.map (fun variable_index -> variable_index , concrete_target_px_valuation variable_index) model.parameters_and_clocks)
					;
					valuations_n_plus_1_before_time_elapsing
				]
			) then(
			(* Print some information *)
			print_message Verbose_high ("Oops! Intersection of the chosen point with z_n_plus_1 is empty… re-choose a valuation within z_n_plus_1…");
			true
			) else false
		) in
		
		if recomputation_needed then(
			(* Re-choose a valuation in this constraint *)
			LinearConstraint.px_exhibit_point valuations_n_plus_1_before_time_elapsing
		(* Otherwise, keep the original valuation *)
		)else(
			(* Print some information *)
			print_message Verbose_high ("Intersection of the chosen point with z_n_plus_1 is non-empty… keep it.");

			concrete_target_px_valuation
		)
	in
	
	(* Print some information *)
	if verbose_mode_greater Verbose_low then(
		print_message Verbose_low ("New final valuation of the symbolic run before time elapsing:\n " ^ (ModelPrinter.string_of_px_valuation model concrete_target_px_valuation_before_time_elapsing) ^ "");
	);
	

	(*------------------------------------------------------------*)
	(* Reconstruct concrete run *)
	(*------------------------------------------------------------*)

	(* We reconstruct a concrete run, for which we need absolute time *)
	

	(* Now construct valuations for the whole run, i.e. pair (time elapsed, valuation) *)
	
	print_message Verbose_low "\nBuilding concrete run:";
	
	(*** TODO: change this system one day, as it costs us one more clock in the ENTIRE analysis, although it would only be used in the run regeneration ***)
	
	(* Get the absolute time clock *)
	let absolute_time_clock = match model.global_time_clock with
		| Some clock_index -> clock_index
		| None -> raise (InternalError ("No absolute time clock is defined in the model, which is (so far) necessary to reconstruct the counterexample."))
	in
	

	(* Iterate starting from s_n and going backward *)
	
	(* Reminder: valuation_n_plus_1 is the initial valuation *after* the transition from the current state n *)
	let valuation_n_plus_1 : LinearConstraint.px_valuation ref = ref concrete_target_px_valuation_before_time_elapsing in

	(* List to maintain the valuations for the concrete run *)
	let te_and_valuations = ref [] in
	

	(*------------------------------------------------------------*)
	(* For n to length-1 to 0 *)
	(*------------------------------------------------------------*)
	for n = List.length symbolic_run.symbolic_steps - 1 downto 0 do
	
		print_message Verbose_low ("\n\nComputing concrete valuation in symbolic run at position " ^ (string_of_int n) ^ "…");
		
		(* Get the values *)

		let symbolic_step_n : StateSpace.symbolic_step = List.nth symbolic_run.symbolic_steps n in
		
		(* Get state n *)
		let state_n : State.state = StateSpace.get_state state_space symbolic_step_n.source in
		
		(* Get the location and zone for state_n *)
		let location_n	: Location.global_location				= state_n.global_location in
		let z_n			: LinearConstraint.px_linear_constraint	= state_n.px_constraint in


		(* Zn+1 is the *initial* valuation at n+1 (i.e., before time elapsing) *)

		let z_n_plus_1 : LinearConstraint.px_linear_constraint = LinearConstraint.px_constraint_of_point (List.map (fun variable_index -> variable_index , !valuation_n_plus_1 variable_index) model.parameters_and_clocks) in
		

		(* Step 1: apply discrete predecessor from n+1 to n, i.e., compute the valuations just before the discrete step *)
		let valuations_n_after_time_elapsing : LinearConstraint.px_linear_constraint = discrete_predecessors state_n symbolic_step_n.transition z_n_plus_1 in


		(* Step 2: compute the initial admissible valuations *)

		let admissible_initial_valuations_at_n : LinearConstraint.px_linear_constraint =
		(* Case first state: just keep the initial constraint *)
		if n = 0 then(
			(* Print some information *)
			if verbose_mode_greater Verbose_total then(
				print_message Verbose_total ("Found state 0: the admissible initial valuations are given by the initial constraint:\n " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names model.initial_constraint) ^ "");
			);

			(* Re-intersect with the *initial* continuous valuations to indeed get an initial valuation *)
			model.initial_constraint
		)else(
		(* Case non-first state: the initial admissible valuations are the predecessor constraint (location n) intersected with the guard from n-1 to n, to which we apply updates from n-1 to n, and then intersected with the constraint at location n (mainly to have the invariant) *)

			let symbolic_step_n_minus_1	: StateSpace.symbolic_step 			= List.nth symbolic_run.symbolic_steps (n - 1) in
			let transition_n_minus_1_n	: StateSpace.combined_transition	= symbolic_step_n_minus_1.transition in
			let state_n_minus_1			: State.state						= StateSpace.get_state state_space symbolic_step_n_minus_1.source in

			(* Call dedicated function *)
			let admissible_initial_valuations_at_n : LinearConstraint.px_linear_constraint = compute_admissible_valuations_after_transition state_n_minus_1 transition_n_minus_1_n state_n in

			admissible_initial_valuations_at_n
		)
		in

		(* Print some information *)
		if verbose_mode_greater Verbose_high then(
			print_message Verbose_high ("Admissible valuations:\n " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names admissible_initial_valuations_at_n) ^ "");
		);
		

		(* Step 3: apply continuous predecessor at state n *)
		
		let valuations_n_before_time_elapsing = continuous_predecessors location_n admissible_initial_valuations_at_n z_n valuations_n_after_time_elapsing in
		
		(* Print some information *)
		if verbose_mode_greater Verbose_high then(
			print_message Verbose_high ("Valuations before time elapsing:\n " ^ (LinearConstraint.string_of_px_linear_constraint model.variable_names valuations_n_before_time_elapsing) ^ "");
		);



		(* Pick a valuation *)
		let valuation_n =
			try(
				LinearConstraint.px_exhibit_point valuations_n_before_time_elapsing
			) with LinearConstraint.EmptyConstraint ->(
				raise (InternalError "Empty constraint found when picking a point in the predecessors of n+1!")
			)
		in
		
		(* Now compute the time spent between the previous and the new valuation *)

		(* Compute the time elapsing *)
		let time_elapsed_n = NumConst.sub (!valuation_n_plus_1 absolute_time_clock) (valuation_n absolute_time_clock) in
		
		(*** DEBUG: test that it is indeed a good valuation, belonging to n! ***)
		(*** TODO ***)
		
		(* Print some information *)
		if verbose_mode_greater Verbose_medium then(
			print_message Verbose_medium ("Valuation " ^ (string_of_int n) ^ " just computed:\n" ^ (ModelPrinter.string_of_px_valuation model valuation_n));
		);
		
		(*** NOTE: we need a px AND d valuation, therefore a bit a hack here ***)
		let pxd_valuation = fun variable_index ->
			match model.type_of_variables variable_index with
			| DiscreteValue.Var_type_clock
			| DiscreteValue.Var_type_parameter -> valuation_n variable_index
			| DiscreteValue.Var_type_discrete _ -> Location.get_discrete_rational_value location_n variable_index (* TODO benjamin : check with étienne, what is it ? is it computing of linear part ? *)
		in
		
		(* Add the valuation to the list, and replace n+1 with n *)
		te_and_valuations := (time_elapsed_n , symbolic_step_n.transition, location_n, pxd_valuation) :: !te_and_valuations;
		valuation_n_plus_1 := valuation_n;
		
	(*------------------------------------------------------------*)
	done;
	(*------------------------------------------------------------*)

	
	(* Print some information *)
	if verbose_mode_greater Verbose_medium then(
		(* Print the list*)
	
		(* Dummy counter for printing *)
		let i = ref 0 in
		List.iter (fun (time_elapsed, _, _, valuation) -> 
			incr i;
			print_message Verbose_low ("Valuation " ^ (string_of_int !i) ^ ":");
			print_message Verbose_low (ModelPrinter.string_of_px_valuation model valuation);
			print_message Verbose_low ("Time elapsing: " ^ (NumConst.string_of_numconst time_elapsed) ^ "");
		) !te_and_valuations;
		(* Print last one *)
		print_message Verbose_low (ModelPrinter.string_of_px_valuation model concrete_target_px_valuation_before_time_elapsing);
	);
	
	
	(* We now reformat the !te_and_valuations into a proper run *)
	(*** TODO: it might have been possible to do it from the first construction? ***)

	(* Retrieve the initial state index of the run *)
	let initial_state_index = match symbolic_run.symbolic_steps with
		(* If the list of steps is not empty: pick the first one *)
		| first_step :: _ -> first_step.source
		(* If the list of steps is empty: pick the final state *)
		| [] -> symbolic_run.final_state
	in
	
	(* Build the initial state of the run *)
	let run_initial_state : State.concrete_state = {
		(* The global location is that of the symbolic initial state *)
		global_location = (StateSpace.get_state state_space initial_state_index).global_location;
		(* The discrete clock+discrete valuation is that of the concrete initial state computed above *)
		px_valuation = 
			(* Case empty list: take from final state *)
			if !te_and_valuations = [] then concrete_target_px_valuation_before_time_elapsing
			else(
			try (let (_ , _, _, pxd_valuation) = List.nth !te_and_valuations 0 in pxd_valuation)
				with Failure _ -> raise (InternalError "List !te_and_valuations expected to be non-empty in function reconstruct_counterexample")
			)
			;
	} in

	(* Build the steps of the run *)
	let reversed_run_steps : (StateSpace.concrete_step list) ref = ref [] in
	(* We explore from first position to the last-1 position (the last state will be handled separately) *)
	for i = 0 to List.length !te_and_valuations - 2 do
		let time_elapsed_i, combined_transition_i, _, _ = List.nth !te_and_valuations i in
		let _, _, target_location, target_valuation = List.nth !te_and_valuations (i+1) in
		let concrete_step : StateSpace.concrete_step = {
			time		= time_elapsed_i;
			transition	= combined_transition_i;
			target		= {global_location = target_location; px_valuation = target_valuation};
		} in
		
		(* Add *)
		reversed_run_steps := concrete_step :: !reversed_run_steps
	done;
	
	let run_steps = 
		(* Case empty list of steps *)
		if !te_and_valuations = [] then []
		else(
			(* Create the last step separately *)
			let time_elapsed_n, combined_transition_n, _, _ = List.nth !te_and_valuations (List.length (!te_and_valuations) -1) in
			let last_step : StateSpace.concrete_step = {
				time		= time_elapsed_n;
				transition	= combined_transition_n;
				target		= {global_location = target_state.global_location; px_valuation = concrete_target_px_valuation_before_time_elapsing};
			} in
			
			(* Put the list in right order *)
			List.rev (last_step :: !reversed_run_steps)
		)
	in
	
	(* (Re)create the PVal *)
	let pval = PVal.pval_from_valuation_function concrete_target_px_valuation_before_time_elapsing in

	(* Return the concrete run *)
	{
		p_valuation		= pval;
		initial_state	= run_initial_state;
		steps			= run_steps;
	}
	


(************************************************************)
(** Reconstruct a whole counterexample from the initial state to a given target state. Return a concrete run *)
(************************************************************)
let reconstruct_counterexample state_space (target_state_index : State.state_index) : StateSpace.concrete_run =
	(* Retrieve the model *)
	let model = Input.get_model() in
	
	(* Print some information *)
	print_message Verbose_medium "Counterexample found: reconstructing counterexample…";
	
	(* First build the predecessors table *)
	let predecessors = StateSpace.compute_predecessors_with_combined_transitions state_space in
	
	(* Print some information *)
	print_message Verbose_medium "Predecessor table built";

	(* Also retrieve the initial state *)
	let initial_state_index = StateSpace.get_initial_state_index state_space in
	
	(* Get the symbolic run, i.e., a list of a pair of a symbolic state *followed* by a combined transition *)
	let symbolic_run : StateSpace.symbolic_run = StateSpace.backward_symbolic_run state_space target_state_index initial_state_index (Some predecessors) in
	
	(* Print some information *)
	if verbose_mode_greater Verbose_low then (
		print_message Verbose_low "\nSymbolic run reconstructed:";
		
		(* Debug print *)
		print_message Verbose_low (ModelPrinter.debug_string_of_symbolic_run model state_space symbolic_run);
	);
	
	(* Get the final state *)
	let target_state = StateSpace.get_state state_space target_state_index in

	(* Exhibit a concrete clock+parameter valuation in the final state *)
	let concrete_target_px_valuation : LinearConstraint.px_valuation = LinearConstraint.px_exhibit_point target_state.px_constraint in
	
	(* Print it *)
	if verbose_mode_greater Verbose_low then(
		print_message Verbose_low "Example of px-valuation:";
		print_message Verbose_low (ModelPrinter.string_of_px_valuation model concrete_target_px_valuation);
	);
	
	(* Exhibit a concrete parameter valuation in the final state *)
(*	let p_constraint = LinearConstraint.px_hide_nonparameters_and_collapse target_state.px_constraint in
	let concrete_p_valuation = LinearConstraint.p_exhibit_point p_constraint in*)
	
	
	(* Print it *)
	if verbose_mode_greater Verbose_standard then(
		let pval = PVal.pval_from_valuation_function concrete_target_px_valuation in
		
		print_message Verbose_standard "Example of parameter valuation:";
		print_message Verbose_standard (ModelPrinter.string_of_pval model pval);
	);
	
	(* Exhibit a concrete run from the symbolic run *)
	concrete_run_of_symbolic_run state_space (predecessors : StateSpace.predecessors_table) (symbolic_run : StateSpace.symbolic_run) concrete_target_px_valuation



(************************************************************)
(************************************************************)
(* Types *)
(************************************************************)
(************************************************************)

(* Type to define the state_index that have unexplored successors in case of premature termination *)
type unexplored_successors =
	(* Not defined (i.e., not yet defined, or no premature termination) *)
	| UnexSucc_undef
	(* A list of states with unexplored successors *)
	| UnexSucc_some of state_index list



(************************************************************)
(************************************************************)
(* Types and exceptions for queue-based BFS *)
(************************************************************)
(************************************************************)
(*(* state struct for constructing set type *)
module State = struct
	type t = state_index
	let compare = compare
end

(* set of states for efficient lookup *)
module StateindexQueue = Queue.Make(State)*)




(************************************************************)
(************************************************************)
(* Types and exceptions for layer-based BFS *)
(************************************************************)
(************************************************************)

type bfs_limit_reached =
	(* No limit *)
	| Keep_going

	(* Termination due to time limit reached *)
	| Time_limit_reached

	(* Termination due to state space depth limit reached *)
	| Depth_limit_reached

	(* Termination due to a number of explored states reached *)
	| States_limit_reached

	(* Termination because a witness has been found *)
	| Witness_found


exception BFS_Limit_detected of bfs_limit_reached


(*GIA**)
type rank_value =
    | Infinity
    | Int of int



type new_maximum =
	| No_new_maximum
	| New_maximum of int


exception FoundInfiniteRank of state_index

exception FoundLargerZone



(************************************************************)
(************************************************************)
(* Class definition for state_index waiting lists *)
(************************************************************)
(************************************************************)
class waiting_list =
	object(self)

	(************************************************************)
	(* Class variables *)
	(************************************************************)
	val mutable waiting_list = []
	

	(************************************************************)
	(* Class methods *)
	(************************************************************)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Add a state to the waiting list *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method add (state_index : State.state_index) =
		waiting_list <- state_index :: waiting_list;
		()

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get all states from the waiting list (in the form of a list) *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method private to_list =
		waiting_list


(************************************************************)
(************************************************************)
end;;
(************************************************************)
(************************************************************)


(************************************************************)
(************************************************************)
(* Class definition *)
(************************************************************)
(************************************************************)

class virtual algoStateBased =
	object (self) inherit algoGeneric as super

	(************************************************************)
	(* Class variables *)
	(************************************************************)

	(*** TODO: better have some option, or better initialize it to the good value from now on ***)
	val mutable state_space = StateSpace.make 0

	(* Nature of the state space according to a property *)
	val mutable statespace_nature = StateSpace.Unknown


(*	(* Clock that may be reset at each transition *)
	val mutable reset_clock : Automaton.clock_index option = None*)

	(* Function to be called from the distributed IMITATOR *)
	(*** NOTE: public ***)
	val mutable patator_termination_function : (unit -> unit) option = None

	(* Status of the analysis *)
	(*** NOTE: public ***)
	val mutable termination_status : Result.bfs_algorithm_termination option = None

	(* Constraint of the initial state (used by some algorithms to initialize their variables) *)
	(*** NOTE: public ***)
	val mutable initial_constraint : LinearConstraint.px_linear_constraint option = None

	(* List of state_index that have unexplored successors in case of premature termination *)
	(*** NOTE: public ***)
	val mutable unexplored_successors : unexplored_successors = UnexSucc_undef


	(* Depth in the explored state space *)
	(*** NOTE: private ***)
	val mutable bfs_current_depth = 0
	
	(* The current new state indexes *)
	val mutable new_states_indexes : State.state_index list = []

	(* Variable to remind of the termination *)
	(*** NOTE: public only for AlgoEFoptQueue ***)
	(*** TODO: merge with termination_status… ***)
	val mutable limit_reached = Keep_going
	
	(* Variable to denote whether the analysis may continue, or whether the analysis should terminate; useful to terminate, e.g., when a witness is found (at least for BFS algorithms) *)
	val mutable algorithm_keep_going = true
	
	
	(* Non-necessarily convex constraint storing the parameter synthesis result (for selected algorithm) *)
	val mutable synthesized_constraint : LinearConstraint.p_nnconvex_constraint = LinearConstraint.false_p_nnconvex_constraint ()
		
	(* Mini cache system: keep in memory the current p-constraint to save computation time (for selected algorithms such as EFsynth) *)
	(*** WARNING: a bit dangerous, as its handling is not very very strictly controlled ***)
	val mutable cached_p_constraint : LinearConstraint.p_linear_constraint option = None
	

	
	(* Counters *)
	(*** NOTE: if the algorithm is called several times sequentially, then each call will create a counter ***)

	val counter_compute_p_constraint_with_cache = create_hybrid_counter_and_register "AlgoStateBased.compute_p_constraint_with_cache" States_counter Verbose_experiments

	(* How many times the cache was useful *)
	val counter_cache = create_discrete_counter_and_register "cache (EF)" PPL_counter Verbose_low
	(* Number of cache misses *)
	val counter_cache_miss = create_discrete_counter_and_register "cache miss (EF)" PPL_counter Verbose_low
	(* The constraint of a new state is smaller than the bad constraint: cut branch *)
	val counter_cut_branch = create_discrete_counter_and_register "cut branch (constraint <= bad)" PPL_counter Verbose_low


	(************************************************************)
	(* Class methods *)
	(************************************************************)


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Variable initialization *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method initialize_variables =
		statespace_nature <- StateSpace.Unknown;
		unexplored_successors <- UnexSucc_undef;
		
(*		(* If normal PTA, i.e., without stopwatches nor flows, compute once for all the static time elapsing polyhedron *)
		if not model.has_non_1rate_clocks then(
			let variables_elapse	= model.clocks in
			let variables_constant	= model.parameters_and_discrete in
			let time_el_polyhedron		= generate_polyhedron_time_elapsing_pta Forward variables_elapse variables_constant in
			let time_pa_polyhedron		= generate_polyhedron_time_elapsing_pta Backward variables_elapse variables_constant in
			
			(* Print some information *)
			if verbose_mode_greater Verbose_high then(
				print_message Verbose_high "Computed the static time elapsing polyhedron:";
				print_message Verbose_high (LinearConstraint.string_of_pxd_linear_constraint model.variable_names time_el_polyhedron);
				print_message Verbose_high "";
				print_message Verbose_high "Computed the static time past polyhedron:";
				print_message Verbose_high (LinearConstraint.string_of_pxd_linear_constraint model.variable_names time_pa_polyhedron);
				print_message Verbose_high "";
			);
			
			(* Save them *)
			time_elapsing_polyhedron	:= Some time_el_polyhedron;
			time_past_polyhedron 		:= Some time_pa_polyhedron;
		
		);*)

		()
		(* The end *)


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Set the PaTATOR termination function *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method set_patator_termination_function (f : unit -> unit) =
		patator_termination_function <- Some f



	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Compute the p-constraint only if it is not cached using the mini-cache system *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method compute_p_constraint_with_minicache px_linear_constraint =

		(* Statistics *)
		counter_compute_p_constraint_with_cache#increment;
		counter_compute_p_constraint_with_cache#start;
		
		let result =
		match cached_p_constraint with
		(* Cache empty: *)
		| None ->
			(* Compute the p_constraint *)
			let p_constraint = LinearConstraint.px_hide_nonparameters_and_collapse px_linear_constraint in
			(* Statistics *)
			counter_cache_miss#increment;
			(* Print some information *)
			if verbose_mode_greater Verbose_medium then(
				self#print_algo_message Verbose_medium "\nCache miss!";
			);
			(* Update cache *)
			cached_p_constraint <- Some p_constraint;
			(* Return result *)
			p_constraint
		(* Cache not empty: directly use it *)
		| Some p_constraint ->
			(* Statistics *)
			counter_cache#increment;
			(* Print some information *)
			if verbose_mode_greater Verbose_medium then(
				self#print_algo_message Verbose_medium "\nCache hit!";
			);
			(* Return the value in cache *)
			p_constraint
		in
		
		(* Statistics *)
		counter_compute_p_constraint_with_cache#stop;

		result

	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Reset the mini-cache *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method reset_minicache : unit =
		cached_p_constraint <- None;
		()

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Check whether the projection of a PX-constraint is included into the `synthesized_constraint` *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method check_whether_px_included_into_synthesized_constraint (px_linear_constraint : LinearConstraint.px_linear_constraint) : bool =
		(* First project onto the parameters *)

		(* Print some information *)
		if verbose_mode_greater Verbose_medium then(
			self#print_algo_message Verbose_medium "Projecting onto the parameters…";
		);

		(*** NOTE: here, we use the mini-cache system ***)
		let p_constraint = self#compute_p_constraint_with_minicache px_linear_constraint in
		
		(* Print some information *)
		self#print_algo_message Verbose_medium "Checking whether the new state is included into known synthesized valuations…";
		if verbose_mode_greater Verbose_high then(
			self#print_algo_message Verbose_high "\nNew constraint:";
			print_message Verbose_high (LinearConstraint.string_of_p_linear_constraint model.variable_names p_constraint);
			
			self#print_algo_message Verbose_high "\nCurrent synthesized constraint:";
			print_message Verbose_high (LinearConstraint.string_of_p_nnconvex_constraint model.variable_names synthesized_constraint);
		);

		(* return p_constraint <= synthesized_constraint *)
		if LinearConstraint.p_nnconvex_constraint_is_leq (LinearConstraint.p_nnconvex_constraint_of_p_linear_constraint p_constraint) synthesized_constraint then(
			(* Statistics *)
			counter_cut_branch#increment;
			
			true
		)else(
			false
		)


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Update the nature of the trace set *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method update_statespace_nature (state : state) =
		if Input.has_property() then(
			let property = Input.get_property() in
			
			match property.property with
				(* Reachability *)
				| EF state_predicate
				| AGnot state_predicate
				| EFexemplify state_predicate
				| EFpmin (state_predicate, _)
				| EFpmax (state_predicate, _)
				| EFtmin state_predicate
				| Cycle_through state_predicate
				| PRP (state_predicate , _)
				| PRPC (state_predicate , _, _)
				->
					(* Check whether the current state matches the state predicate *)
					if State.match_state_predicate model.is_accepting state_predicate state then(
						statespace_nature <- StateSpace.Bad;
					);
	
				
				| NZ_Cycle
				
				| Deadlock_Freeness
				
				(* Inverse method *)
				| IM _
				| ConvexIM _
				| IMK _
				| IMunion _
				
				(* Cartography *)
				| Cover_cartography _
				| Learning_cartography _
				| Shuffle_cartography _
				| Border_cartography _
				| Random_cartography _
				| RandomSeq_cartography _
					->
					(* Cannot conclude anything from a single state yet *)
					()

			(*		| Some (Unreachable unreachable_global_locations) ->
				(* Check whether the current location matches one of the unreachable global locations *)
				if State.match_unreachable_global_locations unreachable_global_locations state.global_location then(
					statespace_nature <- StateSpace.Bad;
				);*)
(* 				| _ -> raise (NotImplemented("AlgoStateBased > IMITATOR currently only implements selected algorithms in update_statespace_nature.")) *)
		)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Actions to perform with the initial state; returns true unless the initial state cannot be kept (in which case the algorithm will stop immediately) *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method virtual process_initial_state : State.state -> bool


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Add a new state to the reachability_graph (if indeed needed) *)
	(* Return true if the state is not discarded by the algorithm, i.e., if it is either added OR was already present before *)
	(* Can raise an exception TerminateAnalysis to lead to an immediate termination *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(*** TODO: return the list of actually added states ***)
	method virtual add_a_new_state : state_index -> StateSpace.combined_transition -> State.state -> bool

	
	
	

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Compute the list of successor states of a given state, and update the state space; returns the list of new states' indexes actually added *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** TODO: to get a more abstract method, and update the state space from another function ***)
	(*** NOTE: made public only for EFoptQueue ***)
	method post_from_one_state source_state_index =

		(* Statistics *)
		counter_post_from_one_state#increment;
		counter_post_from_one_state#start;

		(* Source location: static *)
		let source_location = (StateSpace.get_state state_space source_state_index).global_location in
		(* Dynamic version of the original px_constraint (can change!) *)
		(*** NOTE / TO OPTIMIZE: OK but not in all algorithms !! ***)
		let recompute_source_constraint () = (StateSpace.get_state state_space source_state_index).px_constraint in

		(* Print some information *)
		if verbose_mode_greater Verbose_high then(
			let source_state = StateSpace.get_state state_space source_state_index in
			let source_constraint = source_state.px_constraint in
			let source_constraint_projection = LinearConstraint.px_hide_nonparameters_and_collapse source_constraint in
			print_message Verbose_high ("Performing post from "
				^ (if Location.is_accepting model.is_accepting source_state.global_location then "accepting " else "")
				^ "state:");
			print_message Verbose_high (ModelPrinter.string_of_state model source_state);
			print_message Verbose_high ("\nThe projection of this constraint onto the parameters is:");
			print_message Verbose_high (LinearConstraint.string_of_p_linear_constraint model.variable_names source_constraint_projection);
		);

		(* Statistics *)
		tcounter_next_transitions#start;
		(* get possible actions originating from current state *)
		let list_of_possible_actions = compute_possible_actions source_location in
		(* Statistics *)
		tcounter_next_transitions#stop;

		(* Print some information *)
		if verbose_mode_greater Verbose_high then (
			let actions_string = List.map (fun action_index -> model.action_names action_index) list_of_possible_actions in
			print_message Verbose_high ("Possible synchronized actions are: " ^ (string_of_list_of_string_with_sep ", " actions_string));
		);

		(* Build the list of new states indexes *)
		new_states_indexes <- [];

		(* Flag to check whether the state of which the successors are computed is a deadlock or not *)
		let has_successors = ref false in

		(* Create a constraint D_i = d_i for the discrete variables *)
		let discrete_constr : LinearConstraint.pxd_linear_constraint = discrete_constraint_of_global_location source_location in

		(* FOR ALL ACTION DO: *)
		List.iter (fun action_index ->

			(* Statistics *)
			tcounter_next_transitions#start;

			(* Print some information *)
			print_message Verbose_medium ("\nComputing target states for action '" ^ (model.action_names action_index) ^ "'");
			(* Get the automata declaring the action *)
			let automata_for_this_action = model.automata_per_action action_index in
			let nb_automata_for_this_action = List.length automata_for_this_action in

			(* Statistics *)
			tcounter_next_transitions#stop;

			(*------------------------------------------------------------*)
			(* Compute the reachable states on the fly: i.e., all the possible transitions for all the automata belonging to 'automata' *)
			(*------------------------------------------------------------*)

			(* Compute conjunction with current constraint *)
			(*** To optimize: it seems intersection_assign could be used instead ***)
			let orig_plus_discrete = LinearConstraint.pxd_intersection [LinearConstraint.pxd_of_px_constraint (recompute_source_constraint ()); discrete_constr] in

			(* In alternative semantics, apply time elapsing NOW, so as to factor this operation once for all *)
			(*** WARNING: time elapsing is AGAIN performed in compute_new_constraint, which is a loss of efficiency ***)
			if options#no_time_elapsing then(
				print_message Verbose_total ("\nAlternative time elapsing: Applying time elapsing NOW");
				apply_time_elapsing source_location orig_plus_discrete;
			);

			(* Statistics *)
			tcounter_next_transitions#start;

			(* Give a new index to those automata *)
			let involved_automata_indices = Array.make nb_automata_for_this_action 0 in
			(* Keep an array of possible transition indices for each automaton *)
			let possible_transitions = Array.make nb_automata_for_this_action [] in
			(* Use an array of transition indices for the search (start with 0), indicating the current index within the possible transitions for each automaton *)
			let current_indexes = Array.make nb_automata_for_this_action 0 in
			(* Keep the maximum index of possible transitions for each automaton *)
			let max_indexes = Array.make nb_automata_for_this_action 0 in
			(* Array for the currently selected transition indices *)
			let current_transitions = Array.make nb_automata_for_this_action 0 in

			(* Statistics *)
			tcounter_next_transitions#stop;

			(* Statistics *)
			tcounter_legal_transitions_exist#start;

			(* compute the possible combinations of transitions *)
			let legal_transitions_exist = compute_transitions source_location orig_plus_discrete action_index automata_for_this_action involved_automata_indices max_indexes possible_transitions in

			(* Statistics *)
			tcounter_legal_transitions_exist#stop;

			(* Print some information: compute the number of combinations *)
			if verbose_mode_greater Verbose_medium || options#statistics then(
				let new_nb_combinations = Array.fold_left (fun sum max -> sum * (max + 1)) 1 max_indexes in
				print_message Verbose_medium ("" ^ (string_of_int new_nb_combinations) ^ " combination" ^ (s_of_int new_nb_combinations) ^ " will be considered for this state and this action\n");
				(* Update for statistics *)
				counter_nb_combinations#increment_by new_nb_combinations;
			);

			(* Loop on all the transition combinations *)
			let more_combinations = ref legal_transitions_exist in
			let debug_i = ref 0 in
			
			(* ------------------------------------------------------------ *)
			while !more_combinations do
			(* ------------------------------------------------------------ *)
				(* Statistics *)
				tcounter_next_transitions#start;

				debug_i := !debug_i +1;
				(* Print some information *)
				if verbose_mode_greater Verbose_high then (
					print_message Verbose_high ("------------------------------------------------------------");
					self#print_algo_message_newline Verbose_high ("Consider the combination #" ^ (string_of_int !debug_i) ^ "");
					print_message Verbose_high ("------------------------------------------------------------");
				);
				if verbose_mode_greater Verbose_total then (
					let local_indexes = string_of_array_of_string_with_sep "\n\t" (
					Array.mapi (fun local_index real_index ->
						(string_of_int local_index) ^ " -> " ^ (string_of_int real_index) ^ " : " ^ (string_of_int current_indexes.(local_index)) ^ "; ";
					) involved_automata_indices) in
					print_message Verbose_high ("\n--- This combination is:\n\t" ^ local_indexes);
					print_message Verbose_high ("\n------------------------------------------------------------");
				);

				(* build the current combination of transitions *)
				for i=0 to Array.length current_transitions -1 do
					current_transitions.(i) <- List.nth (possible_transitions.(i)) (current_indexes.(i))
				done;

				(* Statistics *)
				tcounter_next_transitions#stop;

				(* Statistics *)
				tcounter_compute_location_guards_discrete#start;
				
				(* Create the combined transition *)
				let combined_transition = Array.to_list (Array.mapi (fun local_automaton_index real_automaton_index ->
					(* Get the current location for this automaton *)
					let location_index = Location.get_location source_location real_automaton_index in
					(* Find the transitions for this automaton *)
					let transitions = model.transitions real_automaton_index location_index action_index in
					(* Get the index of the examined transition for this automaton *)
					let current_index = current_transitions.(local_automaton_index) in
					(* Keep the 'current_index'th transition *)
					let transition_index = List.nth transitions current_index in
					(* This is the transition index we are interested in *)
					transition_index
				) involved_automata_indices) in

				begin
				(* Compute the successor constraint from the current state via this combined_transition *)
				match post_from_one_state_via_one_transition source_location (recompute_source_constraint ()) discrete_constr combined_transition with
				(* No result: constraint unsatisfiable: do nothing *)
				| None -> ()
				
				(* Some state with its (satisfiable) constraint: *)
				| Some new_state ->
					(* Increment a counter: this state IS generated (although maybe it will be discarded because equal / merged / algorithmic discarding …) *)
					StateSpace.increment_nb_gen_states state_space;

					(* Print some information *)
					if verbose_mode_greater Verbose_total then(
						self#print_algo_message Verbose_total ("Consider the state \n" ^ (ModelPrinter.string_of_state model new_state));
					);

					(* Try to add the state to the state space *)
					let added = self#add_a_new_state source_state_index combined_transition new_state in

					(* Update *)
					has_successors := !has_successors || added;
				end;

				(* Update the next combination *)
				more_combinations := next_combination current_indexes max_indexes;

			done; (* while more new states *)
			(* ------------------------------------------------------------ *)
		) list_of_possible_actions;

		(* Algorithm-specific handling of deadlock states, i.e., states without successors *)
		if not !has_successors then (
			(* Virtual function to be defined in subclasses *)
			self#process_deadlock_state source_state_index;
		);

		(* Statistics *)
		counter_post_from_one_state#stop;

		(* Return the list of (really) new states *)
		(*** NOTE: List.rev really useful??!!!! ***)
		List.rev (new_states_indexes)




	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Add a transition to the state space *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method add_transition_to_state_space transition addition_result =

		(* Statistics *)
		counter_add_transition_to_state_space#increment;
		counter_add_transition_to_state_space#start;

		(* Expand the transition *)
		let source_state_index, combined_transition, target_state_index = transition in

		(* Print some information *)
(*  		print_message Verbose_total ("About to update the state space…");  *)
 		
		(* Update state space *)
		StateSpace.add_transition state_space (source_state_index, combined_transition, target_state_index);

		(* Print some information *)
(*  		print_message Verbose_total ("State space updated");  *)

 		(* Print some information *)
		if verbose_mode_greater Verbose_high then (
			(* Retrieve the target state *)
			let new_target_state = StateSpace.get_state state_space target_state_index in

			let beginning_message = match addition_result with
				| StateSpace.New_state _ -> "NEW STATE"
				| StateSpace.State_already_present _ -> "Old state"
				| StateSpace.State_replacing _ -> "BIGGER STATE than a former state"
			 in
			print_message Verbose_high ("\n" ^ beginning_message ^ " s_" ^ (string_of_int target_state_index) ^ " reachable from s_" ^ (string_of_int source_state_index) ^ " via action '" ^ (model.action_names (StateSpace.get_action_from_combined_transition combined_transition)) ^ "': ");
			print_message Verbose_high (ModelPrinter.string_of_state model new_target_state);
		);

		(* Statistics *)
		counter_add_transition_to_state_space#stop;

		(* The end *)
		()


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Actions to perform when meeting a state with no successors: virtual method to be defined in subclasses *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method virtual process_deadlock_state : state_index -> unit


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Actions to perform at the end of the computation of the *successors* of post^n (i.e., when this method is called, the successors were just computed) *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method virtual process_post_n : state_index list -> unit


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Check whether the algorithm should terminate at the end of some post, independently of the number of states to be processed (e.g., if the constraint is already true or false) *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method virtual check_termination_at_post_n : bool
	
	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Check whether the property is a #witness mode; if so, raise TerminateAnalysis *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method terminate_if_witness : unit =
		let property = Input.get_property() in
		if property.synthesis_type = Witness then(
			(* Update termination status *)
			(*** NOTE/HACK: the number of unexplored states is not known, therefore we do not add it… ***)
			self#print_algo_message Verbose_standard "Target state found! Terminating…";
			termination_status <- Some Target_found;
		
			raise TerminateAnalysis;
		)


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Check whether the limit of an BFS exploration has been reached, according to the analysis options *)
	(*** NOTE: May raise an exception when used in PaTATOR mode (the exception will be caught by PaTATOR) ***)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method private check_and_update_layer_bfs_limit =
		(* Check all limits *)

		(* Depth limit *)
		try(
		begin
		match options#depth_limit with
			| None -> ()
			| Some limit -> if bfs_current_depth >= limit then(
(* 				termination_status <- Depth_limit; *)
				raise (BFS_Limit_detected Depth_limit_reached)
			)
		end
		;
		(* States limit *)
		begin
		match options#states_limit with
			| None -> ()
			| Some limit -> if StateSpace.nb_states state_space > limit then(
(* 				termination_status <- States_limit; *)
				raise (BFS_Limit_detected States_limit_reached)
			)
		end
		;
		(* Time limit *)
		begin
		match options#time_limit with
			| None -> ()
			| Some limit -> if time_from start_time > (float_of_int limit) then(
(* 				termination_status <- Time_limit; *)
				raise (BFS_Limit_detected Time_limit_reached)
			)
		end
		;
		(* External function for PaTATOR (would raise an exception in case of stop needed) *)
		begin
		match patator_termination_function with
			| None -> ()
			| Some f -> f (); () (*** NOTE/BADPROG: Does nothing but in fact will directly raise an exception in case of required termination, caught at a higher level (PaTATOR) ***)
		end
		;
		(* If reached here, then everything is fine: keep going *)
		()
		)
		(* If exception caught, then update termination status *)
		with BFS_Limit_detected reason ->
			limit_reached <- reason


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Check whether the limit of an BFS exploration has been reached, according to the analysis options *)
	(*** NOTE: May raise an exception when used in PaTATOR mode (the exception will be caught by PaTATOR) ***)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method private check_and_update_queue_bfs_limit =
		(* Check all limits *)

		(* Depth limit *)
		try(
		(* States limit *)
		begin
		match options#states_limit with
			| None -> ()
			| Some limit -> if StateSpace.nb_states state_space > limit then(
(* 				termination_status <- States_limit; *)
				raise (BFS_Limit_detected States_limit_reached)
			)
		end
		;
		(* Time limit *)
		begin
		match options#time_limit with
			| None -> ()
			| Some limit -> if time_from start_time > (float_of_int limit) then(
(* 				termination_status <- Time_limit; *)
				raise (BFS_Limit_detected Time_limit_reached)
			)
		end
		;
		(* External function for PaTATOR (would raise an exception in case of stop needed) *)
		begin
		match patator_termination_function with
			| None -> ()
			| Some f -> f (); () (*** NOTE/BADPROG: Does nothing but in fact will directly raise an exception in case of required termination, caught at a higher level (PaTATOR) ***)
		end
		;
		(* If reached here, then everything is fine: keep going *)
		()
		)
		(* If exception caught, then update termination status, and return the reason *)
		with BFS_Limit_detected reason ->
			limit_reached <- reason



	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Print warning(s) if the limit of an exploration has been reached, according to the analysis options *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method private bfs_print_warnings_limit () =
		match termination_status with
			| Some Result.Regular_termination -> ()

			| Some (Result.Depth_limit nb_unexplored_successors) -> print_warning (
				"The limit depth has been reached. The exploration now stops, although there " ^ (waswere_of_int nb_unexplored_successors) ^ " still " ^ (string_of_int nb_unexplored_successors) ^ " state" ^ (s_of_int nb_unexplored_successors) ^ " to explore."
			)

			| Some (Result.States_limit nb_unexplored_successors) -> print_warning (
				"The limit number of states has been reached. The exploration now stops, although there " ^ (waswere_of_int nb_unexplored_successors) ^ " still " ^ (string_of_int nb_unexplored_successors) ^ " state" ^ (s_of_int nb_unexplored_successors) ^ " to explore."
			)

			| Some (Result.Time_limit nb_unexplored_successors) -> print_warning (
				"The time limit has been reached. The exploration now stops, although there " ^ (waswere_of_int nb_unexplored_successors) ^ " still " ^ (string_of_int nb_unexplored_successors) ^ " state" ^ (s_of_int nb_unexplored_successors) ^ " to explore at this iteration."
					(* (" ^ (string_of_int limit) ^ " second" ^ (s_of_int limit) ^ ")*)
			)

			| Some (Result.Target_found) -> print_warning (
				"A target state has been found. The exploration now stops, although there are still some unexplored states."
			)

			| None -> raise (InternalError "The termination status should be set when displaying warnings concerning early termination.")


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Main method to run the queue-based BFS algorithm  *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* method private explore_queue_bfs init_state_index = *)
	(* 09-10-2017: Changed to public for distributed version - Files related: AlgoNZCUBdist *)
	method explore_queue_bfs init_state_index =

		(* Statistics *)
		counter_explore_using_strategy#increment;
		counter_explore_using_strategy#start;

		print_message Verbose_medium("Entering explore_queue_bfs!!!");






(*		(* List of states computed before *)
		let queueWaiting = ref [init_state_index] in
		let queueVisited = ref [] in*)


		(* List of states computed before *)
		(*** NOTE: we encode the queue using a list, with the LAST element of the list being the first of the queue ***)
		(*** NOTE: we don't use module Queue so as to filter easily the list when needed ***)

		let queue = ref [] in

		(* Set the limit *)
		limit_reached <- Keep_going;
		
		(* Flag modified by the algorithm to perhaps terminate earlier *)
		algorithm_keep_going <- true;

		(* Count the states for verbose purpose: *)
		let num_state = ref 0 in



		(*** BEGIN: code for ranking system ***)
		(*** TODO: move one day ***)




		(*****************************************************RANKING TBL******************************************************)
		(* Hashtable: state_index -> rank *)
		let rank_hashtable = Hashtbl.create Constants.guessed_nb_states_for_hashtable in


		let initial_rank state_index state_space =
			print_message Verbose_low ("Access Initial Ranking!");
			if verbose_mode_greater Verbose_low then(
			print_message Verbose_low ("Ranking State: " ^ (StateSpace.string_of_state_index state_index) ^"!");
			);
			(* popped state information *)
			(* location: static , constraint*)
			let state = StateSpace.get_state state_space state_index in
			let constr = state.px_constraint in

			if verbose_mode_greater Verbose_low then(
				print_message Verbose_low ( ModelPrinter.string_of_state model state );
			);

			let checkTrueConstr = LinearConstraint.px_is_equal constr model.px_clocks_non_negative_and_initial_p_constraint in

			let rank = if checkTrueConstr
			then
				(
				print_message Verbose_low ("Rank: Infinity!");
				Infinity
				)
			else
				(
				print_message Verbose_low ("Rank: 0!");
				Int 0
				)
			in
			print_message Verbose_low ("End Initial Ranking!");
			rank
		in

		(*
		let isRanked state_index =
			(* try to find in the hashtbl *)
			try(
				let rank = Hashtbl.find rank_hashtable state_index in
				true
			) with Not_found -> false;
		in
		*)

		let printrank rank = match rank with
							| Infinity -> ("Infinity")
							| Int value -> (string_of_int value);
		in

		(*****************************************************RANKING TBL END**************************************************)





		(*****************************************************RANKINK**********************************************************)

		let uncheckAgainStates = ref [] in

		let checkLargerVisitedLocation state_index1 rank_hashtable =
			(* Print some information *)
			print_message Verbose_total ("Entering checkLargerVisitedLocation(" ^ (string_of_int state_index1) ^ ")…");

			let state = StateSpace.get_state state_space state_index1 in
			let loc1, constr1 = state.global_location, state.px_constraint in

			(* Print some information *)
			print_message Verbose_total ("Retrieved state information");
			(
				try(
					Hashtbl.iter (fun state_index2 rank ->

						(* Print some information *)
						print_message Verbose_total ("Comparing with state " ^ (string_of_int state_index2) ^ "…");

						let state = StateSpace.get_state state_space state_index2 in
						let loc2, constr2 = state.global_location, state.px_constraint in
						if (Location.location_equal loc1 loc2) && not (LinearConstraint.px_is_leq constr2 constr1)
						then  raise (FoundLargerZone);
					) rank_hashtable;
					false;
				) with FoundLargerZone -> true;
			);
		in


		let getSmallerVisitedLocations state_index1 rank_hashtable =
			let state = StateSpace.get_state state_space state_index1 in
			let loc1, constr1 = state.global_location, state.px_constraint in

			let smallers = Hashtbl.fold (fun state_index2 rank smaller_state_index ->
				let state = StateSpace.get_state state_space state_index2 in
				let loc2, constr2 = state.global_location, state.px_constraint in
				(* if (loc1 == loc2) && not (LinearConstraint.px_is_leq constr1 constr2) *)
				if (Location.location_equal loc1 loc2) && not (LinearConstraint.px_is_leq constr1 constr2) && not (List.mem state_index2 !uncheckAgainStates)
				then  (state_index2)::smaller_state_index
				else smaller_state_index;
			) rank_hashtable [];
			in
			smallers
		in


		let getMaxRank rank1 rank2 = match (rank1, rank2) with
									| (Int x1, Int x2) ->  if x1 < x2 then Int x2 else Int x1
									| (_, _) -> Infinity;
		in


		(*
		let getMaxRankStateIndex state_index1 state_index2 =
			let rank1 = Hashtbl.find rank_hashtable state_index1 in
			let rank2 = Hashtbl.find rank_hashtable state_index2 in
			match (rank1, rank2) with
			| (Int x1, Int x2) ->  if x1 < x2 then state_index2 else state_index1
			| (Infinity, Infinity) -> state_index1
			| (Infinity, Int x2) -> state_index1
			| (Int x1, Infinity) -> state_index2;
		in
		*)



		(* Small helpful function for getHighestRank: compare a rank with the current maximum; return a new_maximum result *)
		let compare_index_with_max current_max state_index =
			(* Get the rank from the hash table *)
			(*** WARNING: is that safe?? ***)
			let rank = Hashtbl.find rank_hashtable state_index in
			(* Get the integer value (which cannot be infinity because it was tested before *)
			let value = match rank with
			| Int value -> value
			| Infinity -> raise (InternalError("No state should have a rank Infinity in compare_index_with_max 2"))
			in
			(* Did we find a new maximum? *)
			if value > current_max then New_maximum value else No_new_maximum
		in


		let get_highest_rank_index queue =

			(*
			let highestRank_state_index = ref (List.hd queue) in

			List.iter ( fun state_index ->
							highestRank_state_index := (getMaxRankStateIndex state_index !highestRank_state_index);
						) queue;
			!highestRank_state_index;
			*)

			let init_state_index = List.hd queue in

			let init_max_value = match (Hashtbl.find rank_hashtable init_state_index) with
			| Int value -> value
			| Infinity -> raise (InternalError("No state should have a rank Infinity in compare_index_with_max 1"))
			in

			let max, max_index =
			List.fold_left (fun (current_max, current_max_index) current_index ->
				(* If we found a new maximum *)
				match compare_index_with_max current_max current_index with
				(* We update the maximum *)
				| New_maximum new_value -> new_value, current_index
				(* Otherwise we do not change it *)
				| No_new_maximum -> current_max, current_max_index
			(* Initially, the maximum is 0 *)
			(*** HACK: use -1 for index ***)
			) (init_max_value, init_state_index) queue
			in max_index
		in


		(*
		let getVisitedStates rank_hashtable = Hashtbl.fold ( fun state_index rank acc -> state_index::acc ) rank_hashtable [] in
		*)


		let getHighestRankSuccessor state_index =
			print_message Verbose_low ("Get the highest rank of successors");

			let rank = ref (Hashtbl.find rank_hashtable state_index) in
			(*if successor is in the waiting queue then return the rank*)
			if (List.mem state_index !queue)
			then (
					!rank;
				)
			else
				(
				(*let successors = ref (StateSpace.get_successors state_space state_index ) in*)
				let successors = ref [state_index] in
				let count = ref (List.length !successors) in

				let elem = ref 0 in

				if (!count > 0) && verbose_mode_greater Verbose_low then(
					print_message Verbose_low ("Found the subtree at State: " ^ (StateSpace.string_of_state_index state_index) ^"!");
				);

				while (!count > 0) do
					(

				 	let successor = List.nth !successors !elem in

				 	let nextSuccessors = (StateSpace.get_successors state_space successor) in
				 	List.iter (fun successor2 ->

				 		if not (List.mem successor2 (!successors)) && (Hashtbl.mem rank_hashtable successor2 ) (* && (successor2 <> state_index) *)
				 		then (

				 				if verbose_mode_greater Verbose_low then(
								print_message Verbose_low ("Found the subtree State: " ^ (StateSpace.string_of_state_index successor2)
															^ " with rank value: " ^ printrank (Hashtbl.find rank_hashtable successor2)^ "!");
															);

				 				successors := list_append !successors [successor2];
				 				count := !count + 1;
				 			);
				 	) nextSuccessors;

				 	(* successors := (List.tl !successors); *)

				 	rank := getMaxRank !rank (Hashtbl.find rank_hashtable successor);
				 	count := !count - 1;
				 	elem := !elem + 1;
				 	);
				done;
				!rank;
				);
		in



		let rankingSuccessors successors from_state_index=

			(* The Successors are always ranked before adding into queue and hastbl. Because after that we need exploring the highest rank one *)
			List.iter (fun state_index ->
				(*** NOTE: here, we ALWAYS add (and compute) the rank; would it be smarter to add it on the fly, i.e., to only compute it when it is needed? ***)
				let rank = ref (Int 0) in
				(
					if (Hashtbl.mem rank_hashtable state_index)
					then (
							rank := Hashtbl.find rank_hashtable state_index;
						)
					else (
							rank := initial_rank state_index state_space;

							(* Print some information *)
							print_message Verbose_total ("rankingSuccessors: Initial rank computed for state " ^ (string_of_int state_index));

							Hashtbl.add rank_hashtable state_index !rank;

							(* Print some information *)
							print_message Verbose_total ("rankingSuccessors: Initial rank added to hashtable for state " ^ (string_of_int state_index));
						);
				);


				if not (checkLargerVisitedLocation state_index rank_hashtable) then
				(


					(* finding the previous smaller visited zone with the same location (exploring mistakes) *)
					let smallers = getSmallerVisitedLocations state_index rank_hashtable in

					if smallers = []
					then
						(
							print_message Verbose_low ("There is no smaller zone with the same location");
							(* If no state is smaller, we compute the initial rank *)
							(*
							let rank = initial_rank state_index state_space in
							Hashtbl.add rank_hashtable state_index rank;
							*)
						)
					else
						(
							print_message Verbose_low ("Found " ^ string_of_int (List.length smallers) ^ " smaller zone with the same location");
							let rank = ref (Hashtbl.find rank_hashtable state_index) in

							let rerank = ref false in

							List.iter ( fun state_index_smaller ->
								(* to be sure not a leaf on the search tree*)
								if not (List.mem state_index_smaller !queue)
								then (

									if verbose_mode_greater Verbose_low then(
										print_message Verbose_low ("Smaller State: " ^ (StateSpace.string_of_state_index state_index_smaller) ^ " with rank value: " ^printrank (Hashtbl.find rank_hashtable state_index_smaller)^ "!");
									);

									rerank := true;

									(* This method is from the paper, it's not really efficient in practice *)

									let rank2 = (match (getHighestRankSuccessor state_index_smaller) with
										| Infinity -> Infinity
										| Int value -> Int (value + 1);
									)
									in

									rank := getMaxRank !rank rank2;

									);

								(* in order to adapt to IMITATOR, this code will be commented *)
								(*reomove the state_index_smaller n the hastable*)
								(* Hashtbl.remove rank_hashtable state_index_smaller; *)

								(*Hashtbl.replace rank_hashtable state_index_smaller (Int 0);*)

								(* remove smaller state in the waiting list: may be cause bugs *)
								(* queue := list_remove_first_occurence state_index_smaller !queue; *)

								(*
								(*Add transition*)
								let lsTransitions = StateSpace.find_transitions_in state_space (state_index_smaller::(getVisitedStates rank_hashtable)) in

								List.iter ( fun (pre, actions, smaller) ->
									if (state_index_smaller == smaller) then
									StateSpace.add_transition state_space (pre, actions, state_index);

									(* remove smaller state *)
									(*
									let abstract_state = Hashtbl.find (state_space.all_states) smaller in
									Hashtbl.remove (state_space.all_states) (s,abstract_state);
									*)

								) lsTransitions;
								*)

								(*
								Hashtbl.remove rank_hashtable state_index_smaller;
								queue := list_remove_first_occurence state_index_smaller !queue;
								*)

								uncheckAgainStates := state_index_smaller::(!uncheckAgainStates);

							) smallers;

							if !rerank = true
							then (
							Hashtbl.replace rank_hashtable state_index !rank;
							);



							if verbose_mode_greater Verbose_low then(
								match !rank with
								| Infinity -> print_message Verbose_low ("Return max rank: Infinity!");
								| Int value -> print_message Verbose_low ("Return max rank: " ^ string_of_int value ^"!");
							);
						);
				 );


				queue := list_append [state_index] !queue;

			) successors;
			!queue;
		in

		(*****************************************************RANKINK END******************************************************)





		(*****************************************************PRIOR**********************************************************)
		(*It will sort the queue from largest to snmallest zone*)
		(*
		let addToPriorQueue state_index queue =
			[state_index]@queue
		in
		*)

		let rec addInfinityToPriorQueue state_index queue =
			match queue with
			  | [] -> [state_index]
			  | x :: l -> (
							let rank = Hashtbl.find rank_hashtable x in
							if rank = Infinity
							then
								x :: (addInfinityToPriorQueue state_index l)
							else
								state_index :: x :: l
							);
		in

		let rec addNonInfinityToPriorQueue state_index queue =
			match queue with
			  | [] -> [state_index]
			  | x :: l -> (
							let rank = Hashtbl.find rank_hashtable x in
							match rank with
							| Infinity -> x :: (addNonInfinityToPriorQueue state_index l)
							| Int r -> 	

										let state = StateSpace.get_state state_space state_index in
										let loc1, constr1 = state.global_location, state.px_constraint in
										let state = StateSpace.get_state state_space x in
										let loc2, constr2 = state.global_location, state.px_constraint in
										(
										if not (LinearConstraint.px_is_leq constr2 constr1)
										then
											(
											x :: (addNonInfinityToPriorQueue state_index l);
											)
										else
											(
											state_index :: x :: l
											);
										);
							);
		in

		let addToPriorQueue successors queue=
			(* initial ranking and sorting *)
			let q = ref queue in
			List.iter (fun state_index ->	let rank = initial_rank state_index state_space in
											(* Print some information *)
											print_message Verbose_high ("addToPriorQueue: Initial rank computed for state " ^ (string_of_int state_index));
											Hashtbl.add rank_hashtable state_index rank;


											(*first version of prior*)
											(*
											match rank with
												| Infinity -> q := addInfinityToPriorQueue state_index !q
												| Int _ -> q := addNonInfinityToPriorQueue state_index !q;
											*)

											(*Priority +: if a successor is visited before and has larger zone than the previous
												then it will be considered as mistake and sorted right after the infinity rank in the queue *)

											match rank with
												| Infinity -> q := addInfinityToPriorQueue state_index !q
												| Int _ -> q :=
												(
													if (Hashtbl.mem rank_hashtable state_index)
													then
														addInfinityToPriorQueue state_index !q
														(* addToPriorQueue state_index !q *)
													else
														addNonInfinityToPriorQueue state_index !q;
												);


			) successors;
			!q
		in
		(*****************************************************PRIOR END******************************************************)



		(*** TODO Gia ***)
		let select_from_queue () = match options#exploration_order with
			| Exploration_queue_BFS_RS -> 	(
											try(
												(* First look for infinite rank *)
												List.iter (fun state_index ->
													(* Get the rank from the hashtable (or compute it if necessarily) *)
													let rank = Hashtbl.find rank_hashtable state_index in
													(* If infinite: found *)
													if rank = Infinity then raise (FoundInfiniteRank state_index)
												) !queue;
												(* raise (NotImplemented("Gia")) *)
												(* get the highest rank *)

												let state_index2 = get_highest_rank_index !queue in
												state_index2;
												(* List.hd !queue;*)
											) with FoundInfiniteRank state_index -> state_index
											);

			| Exploration_queue_BFS_PRIOR -> List.hd !queue;
			|  _ -> raise (InternalError ("Impossible situation: at that point, it should be a (variant of) queue BFS"));

		in




		(*** END: code for ranking system ***)


		queue := [init_state_index];

		(* for ranking algo *)
		let rank = initial_rank init_state_index state_space in
		(* Print some information *)
		print_message Verbose_high ("Ranking algorithm: Initial rank computed for state " ^ (string_of_int init_state_index));
		Hashtbl.add rank_hashtable init_state_index rank;







		(* Explore further until the limit is reached or the queue is empty *)
		while limit_reached = Keep_going && !queue <> [] && algorithm_keep_going do
			print_message Verbose_low ("I am here!!!!!!");
			(* Print some information *)
			if verbose_mode_greater Verbose_low then (
				print_message Verbose_low ("\n");
				print_message Verbose_low ("Computing successors of state #" ^ (string_of_int !num_state)
											^ " (" ^ (string_of_int (List.length !queue)) ^ " state" ^ (s_of_int (List.length !queue))
											^ " in the queue).");
			);





			(* Take the first element, i.e., last from the list *)
			(*** NOTE: no test for emptiness, as it was performed just above in the while loop condition ***)
			let new_queue, popped_from_queue = match options#exploration_order with
				(* Classical queue: just pop! *)
				| Exploration_queue_BFS -> OCamlUtilities.list_split_last !queue
				(* Ranking system: TODO *)
				| Exploration_queue_BFS_RS -> 	(* Find the state to be selected *)
												let state_index = select_from_queue () in
												(* Remove from queue *)
												let updated_queue = list_remove_first_occurence state_index !queue in
												(* Return new queue, popped state *)
												updated_queue, state_index
				(* Priority: TODO *)
				| Exploration_queue_BFS_PRIOR -> 	(* Find the state to be selected *)
													let state_index = select_from_queue () in
													(* Remove from queue *)
													let updated_queue = list_remove_first_occurence state_index !queue in
													(* Return new queue, popped state *)
													updated_queue, state_index
				(* Impossible *)
				| _ -> raise (InternalError ("Impossible situation: at that point, it should be a (variant of) queue BFS"))
			in


			(* Remove from the queue *)
			queue := new_queue;

			(* Count the states for verbose purpose: *)
			num_state := !num_state + 1;

			(* Compute successors *)
			(* The concrete function post_from_one_state may raise exception TerminateAnalysis, and update termination_status *)
			let successors =
			try(
				self#post_from_one_state popped_from_queue
			)
			with TerminateAnalysis ->
				(*** HACK: empty the queue to force termination… ***)
				(*** TODO: improve the termination mechanism (by unifying limit_reached and termination_status) ***)
				queue := [];

				(* Return an empty list of successors *)
				[]
			in

			if verbose_mode_greater Verbose_low then(
					print_message Verbose_low ("Poped State: " ^ (StateSpace.string_of_state_index popped_from_queue) ^" from queue!");
					print_message Verbose_low ("States in queue!");
					List.iter ( fun state_index ->
						print_message Verbose_low ("State: " ^ (StateSpace.string_of_state_index state_index) ^" \n");
					) !queue;
			);


			(* Add to queue *)
			queue :=
				(match options#exploration_order with
				| Exploration_queue_BFS -> list_append successors !queue
				(* Ranking system: TODO *)
				| Exploration_queue_BFS_RS -> 	rankingSuccessors successors popped_from_queue;
												(* list_append successors !queue *)
				(* Priority system: TODO *)
				| Exploration_queue_BFS_PRIOR -> addToPriorQueue successors !queue
				(* Impossible *)
				| _ -> raise (InternalError ("Impossible situation: at that point, it should be a (variant of) queue BFS"))
			);


			(* Merge states! *)
			
(*			(*** CASE mergeq ***)
			if options#mergeq then(
				queue := StateSpace.merge state_space !queue;
				(*** TODO: the following code belongs to StateSpace ***)
				(match options#exploration_order with
					| Exploration_queue_BFS_RS -> hashtbl_filter (StateSpace.test_state_index state_space) rank_hashtable
					| _ -> ();
				)
			)
			(*** CASE merge (classical) ***)
			else if options#merge then(
			(*** Here, we merge only the queue ***)
			(*** TODO: merge something else? ***)
			let new_states_after_merging = ref (!queue) in
			if options#merge (*|| options#merge_before*) then (
				(* New version *)
				let eaten_states = StateSpace.merge state_space !new_states_after_merging in
				new_states_after_merging := list_diff !new_states_after_merging eaten_states;
				
				(match options#exploration_order with
				
				| Exploration_queue_BFS_RS -> List.iter ( fun state_index -> Hashtbl.remove rank_hashtable state_index;
					) eaten_states;
				| _ -> ();
				)
			);
			(* Copy back the merged queue *)
			queue := !new_states_after_merging;
			);*)
			
			
			(*** BEGIN OLD MIXED VERSION (2020-09) ***)
			if options#merge (*|| options#merge_before*) then (
				queue := StateSpace.merge state_space !queue;
				(* TODO: the following code belongs in StateSpace *)
				(match options#exploration_order with
					| Exploration_queue_BFS_RS -> hashtbl_filter (StateSpace.test_state_index state_space) rank_hashtable
					| _ -> ();
				)
			)
			else if options#merge212 then(
				raise (NotImplemented "merge v.2.12");
			);
			(*** END OLD MIXED VERSION (2020-09) ***)

			(* Check if the limit has been reached *)
			self#check_and_update_queue_bfs_limit;

			(* If still going, ask the concrete algorithm whether it wants to terminate for other reasons *)
			if limit_reached = Keep_going then(
				(* Print some information *)
				(*** HACK: 'bfs_current_depth - 1' because bfs_current_depth was just incremented… ***)
				self#print_algo_message Verbose_low("Checking termination at post^" ^ (string_of_int (bfs_current_depth - 1)) ^ "…");

				if self#check_termination_at_post_n then(
					algorithm_keep_going <- false;
				);
			);

		done;

		print_message Verbose_medium ("End of Ordering!!! \n");

		(* Were they any more states to explore? *)
		let nb_unexplored_successors = List.length !queue in

		(* Set the list of states with unexplored successors, if any *)
		if nb_unexplored_successors > 0 then(
			unexplored_successors <- UnexSucc_some !queue;
		);

		(* Update termination condition *)
		begin
		match limit_reached with
			(*** NOTE: check None, as it may have been edited from outside, in which case it should not be Regular_termination ***)
			| Keep_going when termination_status = None -> termination_status <- Some (Result.Regular_termination)
			(*** NOTE: obliged to comment out the condition below, otherwise there is a compiling warning… ***)
			| Keep_going (*when termination_status <> None*) -> ()

			(* Termination due to time limit reached *)
			| Time_limit_reached -> termination_status <- Some (Result.Time_limit nb_unexplored_successors)

			(* Termination due to state space depth limit reached *)
			| Depth_limit_reached -> raise (InternalError("A depth limit should not be met in Queue-based BFS"))

			(* Termination due to a number of explored states reached *)
			| States_limit_reached -> termination_status <- Some (Result.States_limit nb_unexplored_successors)
			
			(* Termination because a witness has been found *)
			(*** NOTE/TODO: add a new result termination type? ***)
			| Witness_found -> termination_status <- Some (Result.Regular_termination)
		end
		;

		(* Print some information *)
		(*** NOTE: must be done after setting the limit (above) ***)
		self#bfs_print_warnings_limit ();

		if not algorithm_keep_going && nb_unexplored_successors > 0 then(
			self#print_algo_message Verbose_standard ("A sufficient condition to ensure termination was met although there were still " ^ (string_of_int nb_unexplored_successors) ^ " state" ^ (s_of_int nb_unexplored_successors) ^ " to explore");
		);


		print_message Verbose_standard (
			let nb_states = StateSpace.nb_states state_space in
			let nb_transitions = StateSpace.nb_transitions state_space in
			let fixpoint_str = if nb_unexplored_successors > 0 then "State space exploration stopped" else "Fixpoint reached" in
			"\n" ^ fixpoint_str ^ (*" at a depth of "
			^ (string_of_int bfs_current_depth) ^ ""
			^ *)": "
			^ (string_of_int nb_states) ^ " state" ^ (s_of_int nb_states)
			^ " with "
			^ (string_of_int nb_transitions) ^ " transition" ^ (s_of_int nb_transitions) ^ " in the final state space.");
			(*** NOTE: in fact, more states and transitions may have been explored (and deleted); here, these figures are the number of states in the state space. ***)



		print_message Verbose_medium("Exiting explore_queue_bfs!!!");

		(* Statistics *)
		counter_explore_using_strategy#stop;

		(* The end *)
		()



	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Main method to run the BFS algorithm  *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* 09-10-2017: Changed to public for distributed version - Files related: AlgoNZCUBdist *)
	(* method private explore_layer_bfs init_state_index = *)
	method explore_layer_bfs init_state_index =

		(* Statistics *)
		counter_explore_using_strategy#increment;
		counter_explore_using_strategy#start;

		(* Set the depth to 1 *)
		bfs_current_depth <- 1;

		(* To check whether the time limit / state limit is reached *)
		limit_reached <- Keep_going;

		(* Flag modified by the algorithm to perhaps terminate earlier *)
		algorithm_keep_going <- true;


		(*------------------------------------------------------------*)
		(* Perform the post^* *)
		(*------------------------------------------------------------*)
		(* Set of states computed at the previous depth *)
		let post_n = ref [init_state_index] in

		(* Explore further until the limit is reached or the list of states computed at the previous depth is empty *)
		while limit_reached = Keep_going && !post_n <> [] && algorithm_keep_going do
			(* Print some information *)
			if verbose_mode_greater Verbose_standard then (
				print_message Verbose_low ("\n");
				print_message Verbose_standard ("Computing post^" ^ (string_of_int bfs_current_depth) ^ " from "  ^ (string_of_int (List.length !post_n)) ^ " state" ^ (s_of_int (List.length !post_n)) ^ ".");
			);

			(* Count the states for verbose purpose: *)
			let num_state = ref 0 in

			(* Statistics *)
			counter_nplus1#increment;
			counter_nplus1#start;

			(* The concrete function post_from_one_state may raise exception TerminateAnalysis, and update termination_status *)
			let post_n_plus_1 =
			try(
			(* For each newly found state: *)
			List.fold_left (fun current_post_n_plus_1 source_state_index ->
				(* Count the states for verbose purpose: *)
				num_state := !num_state + 1;

				(* Perform the post *)
				let new_states = self#post_from_one_state source_state_index in

				(* Print some information *)
				if verbose_mode_greater Verbose_medium then (
					let beginning_message = if new_states = [] then "Found no new state" else ("Found " ^ (string_of_int (List.length new_states)) ^ " new state" ^ (s_of_int (List.length new_states)) ^ "") in
					print_message Verbose_medium (beginning_message ^ " for the post of state " ^ (string_of_int !num_state) ^ " / " ^ (string_of_int (List.length !post_n)) ^ " in post^" ^ (string_of_int bfs_current_depth) ^ ".\n");
				);

				(* Return the concatenation of the new states *)
				(**** OPTIMIZED: do not care about order (else shoud consider 'list_append current_post_n_plus_1 (List.rev new_states)') *)
				List.rev_append current_post_n_plus_1 new_states
			) [] !post_n
			)
			with TerminateAnalysis ->(
				(* Set the flag *)
				algorithm_keep_going <- false;
				(* If analysis terminated: successors are just the empty list *)
				(*** TODO: it should be possible to change the flag algorithm_keep_going from inside the function instead of deleting this list ***)
				[]
			)

			in

			(* Statistics *)
			counter_nplus1#stop;

			(* Statistics *)
			counter_process_post_n#increment;
			counter_process_post_n#start;

			self#process_post_n !post_n;

			(* Statistics *)
			counter_process_post_n#stop;

			(*------------------------------------------------------------*)
			(* Begin merging *)
			(*------------------------------------------------------------*)
			(* Merge states! *)
			let new_states_after_merging = ref post_n_plus_1 in
			(*** HACK here! For #merge_before, we should ONLY merge here; but, in order not to change the full structure of the post computation, we first merge locally before the pi0-compatibility test, then again here ***)
			
(*			if options#mergeq then(
				new_states_after_merging := StateSpace.merge state_space !new_states_after_merging;
			) else if options#merge then (
	(* 			new_states_after_merging := try_to_merge_states state_space !new_states_after_merging; *)
				(* New version *)
				let eaten_states = StateSpace.merge state_space !new_states_after_merging in
				new_states_after_merging := list_diff !new_states_after_merging eaten_states;
			);*)
			
			(*** BEGIN OLD MIXED VERSION (2020-09) ***)

			if options#merge (*|| options#merge_before*) then(
				new_states_after_merging := StateSpace.merge state_space !new_states_after_merging;
			)
			else if options#merge212 then(
				raise (NotImplemented "merge v.2.12");
			);
			(*** END OLD MIXED VERSION (2020-09) ***)
				
			(* Update the post_n, i.e., at that point we replace the post^n by post^n+1 in our BFS algorithm, and go one step deeper in the state space *)
			post_n := !new_states_after_merging;
			(*------------------------------------------------------------*)
			(* End merging *)
			(*------------------------------------------------------------*)

			(* Print some information *)
			if verbose_mode_greater Verbose_medium then (
				let beginning_message = if !post_n = [] then "\nFound no new state" else ("\nFound " ^ (string_of_int (List.length !post_n)) ^ " new state" ^ (s_of_int (List.length !post_n)) ^ "") in
				print_message Verbose_medium (beginning_message ^ " for post^" ^ (string_of_int bfs_current_depth) ^ ".\n");
			);

			(* If acyclic option: empty the list of already reached states for comparison with former states *)
			if options#acyclic then(
				print_message Verbose_low ("\nMode acyclic: empty the list of states to be compared.");
				StateSpace.empty_states_for_comparison state_space;
			);

	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(***                                        BEGIN ALGORITHM-SPECIFIC CODE                                             ***)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
(*			(* If check-point option: check if the constraint is equal to pi0 *)
			(*** TO OPTIMIZE !!! (at least compute pi0_constraint once for all) ***)
			(*** WARNING!! ONLY works for the classical inverse method (not for variants) ***)
			(*** TODO: also allow for BC ***)
			if options#imitator_mode = Inverse_method  && options#check_point then(
				print_message Verbose_low ("\nMode check-point: checking whether the resulting constraint is restricted to pi0…");
				(* Get all constraints *)
				let all_p_constraints = StateSpace.all_p_constraints state_space in
				(* Computing the constraint intersection *)
				let current_intersection = LinearConstraint.p_intersection all_p_constraints in
				(* Get pi0 *)
				let pi0 = Input.get_pi0() in
				(* Converting pi0 to a list *)
				let pi0_list = List.map (fun p -> (p, pi0#get_value p)) model.parameters in
				(* Converting pi0 to a constraint *)
				let pi0_constraint = LinearConstraint.p_constraint_of_point pi0_list in
				(* Print *)
				if verbose_mode_greater Verbose_medium then(
					print_message Verbose_medium ("\nPi0: " ^ (LinearConstraint.string_of_p_linear_constraint model.variable_names pi0_constraint));
				);
				(* Checking whether the constraint is *included* within pi0 *)
				if LinearConstraint.p_is_leq current_intersection pi0_constraint then(
					(* Print message *)
					print_message Verbose_standard ("\nCurrent accumulated constraint is now restricted to pi0. Analysis can safely terminate.");
					(* Stop *)
					limit_reached := true;
				);
			);*)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(***                                          END ALGORITHM-SPECIFIC CODE                                             ***)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)
	(**********************************************************************************************************************)

			(* Print some memory information *)
			if options#statistics then(
				(*** TODO ***)
			);

			(* Statistics *)
			counter_gcmajor#increment;
			counter_gcmajor#start;

			(* Clean up a little *)
			(*** NOTE: LOOKS LIKE COMPLETELY USELESS !!! it even increases memory x-( ***)
(* 			Gc.major (); *)

			(* Statistics *)
			counter_gcmajor#stop;


			(* Go one step deeper *)
			bfs_current_depth <- bfs_current_depth + 1;

			(* Check if the limit has been reached *)
			self#check_and_update_layer_bfs_limit;

			(* If still going, ask the concrete algorithm whether it wants to terminate for other reasons *)
			if limit_reached = Keep_going then(
				(* Print some information *)
				(*** HACK: 'bfs_current_depth - 1' because bfs_current_depth was just incremented… ***)
				self#print_algo_message Verbose_low("Checking termination at post^" ^ (string_of_int (bfs_current_depth - 1)) ^ " with a queue of " ^ (string_of_int (List.length !post_n)) ^ " unexplored state" ^ (s_of_int (List.length !post_n)) ^ "…");

				if self#check_termination_at_post_n then(
					algorithm_keep_going <- false;
				);
			);

		done; (* END WHILE *)

		(* Were they any more states to explore? *)
		let nb_unexplored_successors = List.length !post_n in

		(* Set the list of states with unexplored successors, if any *)
		if nb_unexplored_successors > 0 then(
			(*** NOTE: if an exception TerminateAnalysis was raised, this list is empty :( ***)
			unexplored_successors <- UnexSucc_some !post_n;
		);

		(* Update termination condition *)
		begin
		match limit_reached with
			(* No limit: regular termination *)
			(*** NOTE: check None, as it may have been edited from outside, in which case it should not be Regular_termination ***)
			| Keep_going when termination_status = None -> termination_status <- Some (Result.Regular_termination)
			(*** NOTE: obliged to comment out the condition below, otherwise there is a compiling warning… ***)
			| Keep_going (*when termination_status <> None*) -> ()

			(* Termination due to time limit reached *)
			| Time_limit_reached -> termination_status <- Some (Result.Time_limit nb_unexplored_successors)

			(* Termination due to state space depth limit reached *)
			| Depth_limit_reached -> termination_status <- Some (Result.Depth_limit nb_unexplored_successors)

			(* Termination due to a number of explored states reached *)
			| States_limit_reached -> termination_status <- Some (Result.States_limit nb_unexplored_successors)
			
			(* Termination because a witness has been found *)
			(*** NOTE/TODO: add a new result termination type? ***)
			| Witness_found -> termination_status <- Some (Result.Regular_termination)
		end
		;

		(* Print some information *)
		(*** NOTE: must be done after setting the limit (above) ***)
		self#bfs_print_warnings_limit ();

		if not algorithm_keep_going && nb_unexplored_successors > 0 then(
			self#print_algo_message Verbose_standard ("A sufficient condition to ensure termination was met although there were still " ^ (string_of_int nb_unexplored_successors) ^ " state" ^ (s_of_int nb_unexplored_successors) ^ " to explore");
		);


		print_message Verbose_standard (
			let nb_states = StateSpace.nb_states state_space in
			let nb_transitions = StateSpace.nb_transitions state_space in
			let fixpoint_str = if nb_unexplored_successors > 0 then "State space exploration stopped" else "Fixpoint reached" in
			"\n" ^ fixpoint_str ^ " at a depth of "
			^ (string_of_int bfs_current_depth) ^ ""
			^ ": "
			^ (string_of_int nb_states) ^ " state" ^ (s_of_int nb_states)
			^ " with "
			^ (string_of_int nb_transitions) ^ " transition" ^ (s_of_int nb_transitions) ^ " in the final state space."
		);
		(*** NOTE: in fact, more states and transitions may have been explored (and deleted); here, these figures are the number of states in the state space. ***)

		(* Statistics *)
		counter_explore_using_strategy#stop;

		(* The end *)
		()


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Main method to run the algorithm *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method run () =
		(* Get some variables *)
		let nb_actions = model.nb_actions in
		let nb_variables = model.nb_variables in
		let nb_automata = model.nb_automata in

		(* Time counter for the algorithm *)
		start_time <- Unix.gettimeofday();

		(* Compute initial state *)
		let init_state = compute_initial_state_or_abort() in
		
		(* copy init state, as it might be destroyed later *)
		(*** NOTE: this operation appears to be here totally useless ***)
		let init_loc, init_constr = init_state.global_location, init_state.px_constraint in
		let init_state : state = { global_location = init_loc; px_constraint = LinearConstraint.px_copy init_constr} in

		(* Set up the initial state constraint *)
		initial_constraint <- Some init_constr;

		(* Variable initialization *)
		(*** NOTE: must be done *after* the initial state computation (for PRP notably) ***)
		print_message Verbose_low ("Initializing the algorithm local variables…");
		self#initialize_variables;

		(* Print some information *)
		print_message Verbose_standard ("Starting running algorithm " ^ self#algorithm_name ^ "…\n");

		(* Debut prints *)
		print_message Verbose_low ("Starting exploring the parametric zone graph from the following initial state:");
		print_message Verbose_low (ModelPrinter.string_of_state model init_state);
		(* Guess the number of reachable states *)
		let guessed_nb_states = 10 * (nb_actions + nb_automata + nb_variables) in
		let guessed_nb_transitions = guessed_nb_states * nb_actions in
		print_message Verbose_high ("I guess I will reach about " ^ (string_of_int guessed_nb_states) ^ " states with " ^ (string_of_int guessed_nb_transitions) ^ " transitions.");

		(* Create the state space *)
		state_space <- StateSpace.make guessed_nb_transitions;

		(* Check if the initial state should be kept according to the algorithm *)
		let initial_state_added = self#process_initial_state init_state in

		(* Degenerate case: initial state cannot be kept: terminate *)
		if not initial_state_added then(
			(* Output a warning because this situation is still a little strange *)
			print_warning "The initial state is not kept. Analysis will now terminate.";

			(* Set the termination status *)
			termination_status <- Some (Result.Regular_termination);

			(* Return the algorithm-dependent result and terminate *)
			self#compute_result
		(* Else: start the algorithm in a regular manner *)
		)else(

		(* Add the initial state to the reachable states; no need to check whether the state is present since it is the first state anyway *)
		let init_state_index = match StateSpace.add_state state_space AbstractAlgorithm.No_check init_state with
			(* The state is necessarily new as the state space was empty *)
			| StateSpace.New_state state_index -> state_index
			| _ -> raise (InternalError "The result of adding the initial state to the state space should be New_state")
		in

		(* Increment the number of computed states *)
		StateSpace.increment_nb_gen_states state_space;

		(* Call generic method handling BFS *)
		begin
		match options#exploration_order with
			| Exploration_layer_BFS -> self#explore_layer_bfs init_state_index;
			| Exploration_queue_BFS -> self#explore_queue_bfs init_state_index;
			| Exploration_queue_BFS_RS -> self#explore_queue_bfs init_state_index;
			| Exploration_queue_BFS_PRIOR -> self#explore_queue_bfs init_state_index;
(*			| Exploration_NDFS -> self#explore_layer_bfs init_state_index;
            | Exploration_NDFS_sub -> self#explore_layer_bfs init_state_index;
            | Exploration_layer_NDFS -> self#explore_layer_bfs init_state_index;
            | Exploration_layer_NDFS_sub -> self#explore_layer_bfs init_state_index;*)
		end;

		(* Return the algorithm-dependent result *)
		self#compute_result

		(*** TODO: split between process result and return result; in between, add some info (algo_name finished after….., etc.) ***)
		) (* end if initial state added *)


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Packaging the result at the end of the exploration (to be defined in subclasses) *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method virtual compute_result : Result.imitator_result



(************************************************************)
(************************************************************)
end;;
(************************************************************)
(************************************************************)
