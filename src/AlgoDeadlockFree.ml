(************************************************************
 *
 *                       IMITATOR
 * 
 * LIPN, Université Paris 13, Sorbonne Paris Cité (France)
 * 
 * Module description: Parametric deadlock-freeness
 * 
 * File contributors : Étienne André
 * Created           : 2016/02/08
 * Last modified     : 2016/02/10
 *
 ************************************************************)


(************************************************************)
(************************************************************)
(* Modules *)
(************************************************************)
(************************************************************)
open OCamlUtilities
open ImitatorUtilities
open Exceptions
open AbstractModel
open Result
open AlgoPostStar


(************************************************************)
(************************************************************)
(* Class-independent functions *)
(************************************************************)
(************************************************************)

(*** WARNING! big hack: due to the fact that StateSpace only maintains the action, then we have to hope that the PTA is deterministic to retrieve the edge, and hence the guard ***)
let get_guard state_space state_index action_index state_index' =
	(* Retrieve the model *)
	let model = Input.get_model () in
	
	
	(*** WORK IN PROGRESS ***)
	
	(* Retrieve source and destination locations *)
	let (location : Location.global_location), _ = StateSpace.get_state state_space state_index in
	let (location' : Location.global_location), _ = StateSpace.get_state state_space state_index' in
	
	(* Create the list of local guards *)
	let local_guards = ref [] in
	
	(* For all PTA *)
	List.iter (fun automaton_index ->
		(* Retrieve source and destination location indexes *)
		let l : Automaton.location_index = Location.get_location location automaton_index in
		let l' : Automaton.location_index = Location.get_location location' automaton_index in
		
		(* Now, compute the local guard, i.e., the guard in the current PTA *)
		let local_guard =
		(* If source and destination are equal: either a self-loop (if there exists a self-loop with this action), or the current PTA is not concerned by the transition *)
		if l = l' then (
			(* Find the transitions l -> action_index -> l' *)
			(*** NOTE: type transition = guard * clock_updates * discrete_update list * location_index ***)
			let transitions = List.filter (fun (_,_,_, destination) -> destination = l') (model.transitions automaton_index l action_index) in
			
			(* If none: then not concerned -> true gard *)
			if List.length transitions = 0 then LinearConstraint.pxd_true_constraint()
			
			(* If exactly one: good situation: return the guard *)
			else if List.length transitions = 1 then let g,_,_,_ = List.nth transitions 0 in g
			(* If more than one: take the first one (*** HACK ***) and warn *)
			else(
				(* Warning *)
				print_warning ("Non-deterministic PTA! Selecting a guard arbitrarily among the " ^ (string_of_int (List.length transitions)) ^ " transitions from '" ^ (model.location_names automaton_index l) ^ "' to '" ^ (model.location_names automaton_index l') ^ "' with action to '" ^ (model.action_names action_index) ^ "' in automaton '" ^ (model.automata_names automaton_index) ^ "'.");
				
				(* Take arbitrarily the first element *)
				let g,_,_,_ = List.nth transitions 0 in g
			
			)

		(* Otherwise, if the source and destination locations differ: necessarily a transition with this action *)
		) else (
			(* Find the transitions l -> action_index -> l' *)
			let transitions = List.filter (fun (_,_,_, destination) -> destination = l') (model.transitions automaton_index l action_index) in
			
			(* There cannot be none *)
			if List.length transitions = 0 then raise (raise (InternalError("There cannot be no transition from '" ^ (model.location_names automaton_index l) ^ "' to '" ^ (model.location_names automaton_index l') ^ "' with action to '" ^ (model.action_names action_index) ^ "' in automaton '" ^ (model.automata_names automaton_index) ^ ".")))
			
			(* If exactly one: good situation: return the guard *)
			else if List.length transitions = 1 then let g,_,_,_ = List.nth transitions 0 in g
			(* If more than one: take the first one (*** HACK ***) and warn *)
			else(
				(* Warning *)
				print_warning ("Non-deterministic PTA! Selecting a guard arbitrarily among the " ^ (string_of_int (List.length transitions)) ^ " transitions from '" ^ (model.location_names automaton_index l) ^ "' to '" ^ (model.location_names automaton_index l') ^ "' with action to '" ^ (model.action_names action_index) ^ "' in automaton '" ^ (model.automata_names automaton_index) ^ "'.");
				
				(* Take arbitrarily the first element *)
				let g,_,_,_ = List.nth transitions 0 in g
			)
			
		) in
		
		(* Add the guard *)
		local_guards := local_guard :: !local_guards;
	
	) model.automata;
	
	(* Compute constraint for assigning a (constant) value to discrete variables *)
	print_message Verbose_high ("Computing constraint for discrete variables");
	let discrete_values = List.map (fun discrete_index -> discrete_index, (Location.get_discrete_value location discrete_index)) model.discrete in
	(* Constraint of the form D_i = d_i *)
	let discrete_constraint = LinearConstraint.pxd_constraint_of_point discrete_values in

	(* Create the constraint guard ^ D_i = d_i *)
	let guard = LinearConstraint.pxd_intersection (discrete_constraint :: !local_guards) in
	
	(* Finally! Return the guard *)
	guard


(************************************************************)
(************************************************************)
(* Class definition *)
(************************************************************)
(************************************************************)
class algoDeadlockFree =
	object (self) inherit algoPostStar as super
	
	(************************************************************)
	(* Class variables *)
	(************************************************************)
	
	(* Non-necessarily convex parameter constraint for which deadlocks may arise *)
	val mutable bad_constraint : LinearConstraint.p_nnconvex_constraint = LinearConstraint.false_p_nnconvex_constraint ()

	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Name of the algorithm *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method algorithm_name = "Parametric deadlock-freeness checking"
	
	
	
	(************************************************************)
	(* Class methods *)
	(************************************************************)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Variable initialization *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method initialize_variables =
		super#initialize_variables;
		
		self#print_algo_message Verbose_low "Initializing variables...";
		
		bad_constraint <- LinearConstraint.false_p_nnconvex_constraint ();

		(* Print some information *)
		if verbose_mode_greater Verbose_low then(
			(* Retrieve the model *)
			let model = Input.get_model () in
			self#print_algo_message Verbose_low ("The global bad constraint is now: " ^ (LinearConstraint.string_of_p_nnconvex_constraint model.variable_names bad_constraint));
		);
		
		(* The end *)
		()
	


(*	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Actions to perform when meeting a state with no successors: nothing to do for this algorithm *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method process_deadlock_state state_index = ()*)
	
	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Actions to perform at the end of the computation of the *successors* of post^n (i.e., when this method is called, the successors were just computed). Nothing to do for this algorithm. *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method process_post_n (post_n : StateSpace.state_index list) =
		(* Retrieve the model *)
		let model = Input.get_model () in
		
		self#print_algo_message Verbose_low "Entering process_post_n";
		
		(* For all state s in post^n *)
		List.iter (fun state_index ->
			(* Get the constraint of s *)
			let s_location, s_constraint = StateSpace.get_state state_space state_index in
		
			(* Define a local constraint storing the union of PX-constraints allowing to leave s *)
			let good_constraint_s = LinearConstraint.false_px_nnconvex_constraint () in
			
			(* Retrieve all successors of this state with their action *)
			let succs_of_s = StateSpace.get_successors_with_actions state_space state_index in
			
			(* For all state s' in the successors of s *)
			List.iter (fun (state_index', action_index) ->
			
				(* retrieve the guard *)
				(*** WARNING! big hack: due to the fact that StateSpace only maintains the action, then we have to hope that the PTA is deterministic to retrieve the edge, and hence the guard ***)
				let guard = get_guard state_space state_index action_index state_index' in
				
				(* Print some information *)
				if verbose_mode_greater Verbose_low then(
					self#print_algo_message Verbose_low ("Guard computed via action '" ^ (model.action_names action_index) ^ "': " ^ (LinearConstraint.string_of_pxd_linear_constraint model.variable_names guard));
				);
	
				(* Intersect with the guard with s *)
				(*** UGLY: conversion of dimensions..... ***)
				LinearConstraint.pxd_intersection_assign guard [LinearConstraint.pxd_of_px_constraint s_constraint];
				
				(* Print some information *)
				if verbose_mode_greater Verbose_low then(
					self#print_algo_message Verbose_low ("Intersection of guards: " ^ (LinearConstraint.string_of_pxd_linear_constraint model.variable_names guard));
				);
	
				(* Process past *)
				AlgoStateBased.apply_time_past s_location guard;
				
				(* Print some information *)
				if verbose_mode_greater Verbose_low then(
					self#print_algo_message Verbose_low ("After time past: " ^ (LinearConstraint.string_of_pxd_linear_constraint model.variable_names guard));
				);
	
				(* Update the local constraint by adding the new constraint as a union *)
				(*** WARNING: ugly (and expensive) to convert from pxd to px ***)
				(*** NOTE: still safe since discrete values are all instantiated ***)
				LinearConstraint.px_nnconvex_px_union good_constraint_s (LinearConstraint.pxd_hide_discrete_and_collapse guard);
				
				(* Print some information *)
				if verbose_mode_greater Verbose_low then(
					self#print_algo_message Verbose_low ("The local good constraint (allowing exit) is now: " ^ (LinearConstraint.string_of_px_nnconvex_constraint model.variable_names good_constraint_s));
				);
			) succs_of_s;
				
(*			(* Compute the difference True^+ \ good_constraint_s *)
			(*** TODO: add a field clocks_and_parameters to abstract_model ***)
			let trueplus = LinearConstraint.px_constraint_of_nonnegative_variables (list_union model.clocks model.parameters) in
			let px_bad_constraint_s = LinearConstraint.px_nnconvex_constraint_of_px_linear_constraint trueplus in
			
			(* Print some information *)
			if verbose_mode_greater Verbose_medium then(
				self#print_algo_message Verbose_medium ("px_bad_constraint_s ('trueplus') is now: " ^ (LinearConstraint.string_of_px_nnconvex_constraint model.variable_names px_bad_constraint_s));
			);

			LinearConstraint.px_nnconvex_difference px_bad_constraint_s good_constraint_s;

			(* Print some information *)
			if verbose_mode_greater Verbose_low then(
				self#print_algo_message Verbose_low ("px_bad_constraint_s (True \ good, not allowing exit) is now: " ^ (LinearConstraint.string_of_px_nnconvex_constraint model.variable_names px_bad_constraint_s));
			);
			
			*)

			(* Compute the difference s \ good_constraint_s *)
			(*** TODO: add a field clocks_and_parameters to abstract_model ***)
			let nnonvex_s = LinearConstraint.px_nnconvex_constraint_of_px_linear_constraint s_constraint in
			
			(* Print some information *)
			if verbose_mode_greater Verbose_medium then(
				self#print_algo_message Verbose_medium ("nnonvex_s (= s) is: " ^ (LinearConstraint.string_of_px_nnconvex_constraint model.variable_names nnonvex_s));
			);

			LinearConstraint.px_nnconvex_difference nnonvex_s good_constraint_s;
			
			
			(* Print some information *)
			if verbose_mode_greater Verbose_low then(
				self#print_algo_message Verbose_low ("nnonvex_s (s \ good, not allowing exit) is now: " ^ (LinearConstraint.string_of_px_nnconvex_constraint model.variable_names nnonvex_s));
			);
			

			
			(* Project onto the parameters *)
			let p_bad_constraint_s = LinearConstraint.px_nnconvex_hide_nonparameters_and_collapse nnonvex_s(*px_bad_constraint_s*) in
				
			(* Print some information *)
			if verbose_mode_greater Verbose_low then(
				self#print_algo_message Verbose_low ("p_bad_constraint_s (True \ good, not allowing exit, projected onto P) is now: " ^ (LinearConstraint.string_of_p_nnconvex_constraint model.variable_names p_bad_constraint_s));
			);

			(* Update the bad constraint using the local constraint *)
			LinearConstraint.p_nnconvex_union bad_constraint p_bad_constraint_s;
		
			(* Print some information *)
			if verbose_mode_greater Verbose_low then(
				self#print_algo_message Verbose_low ("The global bad constraint is now: " ^ (LinearConstraint.string_of_p_nnconvex_constraint model.variable_names bad_constraint));
			);
		) post_n;

		print_message Verbose_low ("");

		(* The end *)
		()

	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Actions to perform when meeting a state with no successors: in that case, negate the entire state *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method process_deadlock_state state_index =
		
		self#print_algo_message Verbose_low ("Entering process_deadlock_state " ^ (string_of_int state_index) ^ "...");
		
		(* Get the constraint of the state *)
		let _, s_constraint = StateSpace.get_state state_space state_index in
		
		(* Project onto P *)
		let p_constraint = LinearConstraint.px_hide_nonparameters_and_collapse s_constraint in
		
		(* Print some information *)
		if verbose_mode_greater Verbose_low then(
			(* Retrieve the model *)
			let model = Input.get_model () in
			self#print_algo_message Verbose_low ("Found a deadlock state! Adding " ^ (LinearConstraint.string_of_p_linear_constraint model.variable_names p_constraint) ^ ".");
		);
		
		(* Add union to bad_constraint *)
		LinearConstraint.p_nnconvex_p_union bad_constraint p_constraint;
		
		(* Print some information *)
		if verbose_mode_greater Verbose_low then(
			(* Retrieve the model *)
			let model = Input.get_model () in
			self#print_algo_message Verbose_low ("The global bad constraint is now: " ^ (LinearConstraint.string_of_p_nnconvex_constraint model.variable_names bad_constraint));
		);

		print_message Verbose_low ("");

		(* The end *)
		()
		

	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Method packaging the result output by the algorithm *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method compute_result =
		(* Retrieve the model *)
		let model = Input.get_model () in
		
		self#print_algo_message_newline Verbose_standard (
			"Algorithm completed " ^ (after_seconds ()) ^ "."
		);
		
		(* Perform result = initial_state|P \ bad_constraint *)
		
(* 		let initial_constraint =  *)
		
		
		
		(*** TODO ***)
		
		
		
		let trueplus = LinearConstraint.p_constraint_of_nonnegative_variables model.parameters in
		let result = LinearConstraint.p_nnconvex_constraint_of_p_linear_constraint trueplus in
		LinearConstraint.p_nnconvex_difference result bad_constraint;
			
		
		(* Get the termination status *)
		 let termination_status = match termination_status with
			| None -> raise (InternalError "Termination status not set in EFsynth.compute_result")
			| Some status -> status
		in

		(* The tile nature is good if 1) it is not bad, and 2) the analysis terminated normally *)
		let statespace_nature =
			if statespace_nature = StateSpace.Unknown && termination_status = Regular_termination then StateSpace.Good
			(* Otherwise: unchanged *)
			else statespace_nature
		in
		
		(* Constraint is exact if termination is normal, possibly under-approximated otherwise *)
		let soundness = if termination_status = Regular_termination then Constraint_exact else Constraint_maybe_under in

		(* Return the result *)
		PDFC_result
		{
			(* List of constraints ensuring potential deadlocks *)
			result				= result;
			
			(* Explored state space *)
			state_space			= state_space;
			
			(* Nature of the state space *)
			statespace_nature	= statespace_nature;
			
			(* Total computation time of the algorithm *)
			computation_time	= time_from start_time;
			
			(* Soudndness of the result *)
			soundness			= soundness;
	
			(* Termination *)
			termination			= termination_status;
		}
	
(************************************************************)
(************************************************************)
end;;
(************************************************************)
(************************************************************)
