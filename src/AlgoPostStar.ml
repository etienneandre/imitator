(************************************************************
 *
 *                       IMITATOR
 * 
 * LIPN, Université Paris 13, Sorbonne Paris Cité (France)
 * 
 * Module description: PostStar algorithm, i.e., simple computation of all symbolic states
 * 
 * File contributors : Étienne André
 * Created           : 2015/11/25
 * Last modified     : 2016/01/08
 *
 ************************************************************)


(************************************************************)
(* Modules *)
(************************************************************)
open OCamlUtilities
open ImitatorUtilities
open Exceptions
open AbstractModel
open Result
open AlgoBFS



(************************************************************)
(************************************************************)
(* Class definition *)
(************************************************************)
(************************************************************)
class algoPostStar =
	object (self) inherit algoBFS as super
	
	
	(************************************************************)
	(* Class variables *)
	(************************************************************)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Name of the algorithm *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method algorithm_name = "Post*"
	

	
	(************************************************************)
	(* Class methods *)
	(************************************************************)
	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Variable initialization *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method initialize_variables =
		(* Nothing to do *)
		()
	

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Add a new state to the reachability_graph (if indeed needed) *)
	(* Also update tile_nature and slast *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method add_a_new_state reachability_graph orig_state_index new_states_indexes action_index location (final_constraint : LinearConstraint.px_linear_constraint) =
		(* Retrieve the model *)
		let model = Input.get_model () in

		(* Build the state *)
		let new_state = location, final_constraint in

		(* Print some information *)
		if verbose_mode_greater Verbose_total then(
			(*** TODO: move that comment to a higher level function? (post_from_one_state?) ***)
			print_message Verbose_total ("Consider the state \n" ^ (ModelPrinter.string_of_state model new_state));
		);

		let new_state_index, added = (
			StateSpace.add_state reachability_graph new_state
		) in
		
		(* If this is really a new state *)
		if added then (

			(* First check whether this is a bad tile according to the property and the nature of the state *)
			self#update_trace_set_nature new_state;
			
			(* Add the state_index to the list of new states (used to compute their successors at the next iteration) *)
			new_states_indexes := new_state_index :: !new_states_indexes;
			
		) (* end if new state *)
		;
		
		
		(*** TODO: move the rest to a higher level function? (post_from_one_state?) ***)
		
		(* Update the transitions *)
		StateSpace.add_transition reachability_graph (orig_state_index, action_index, new_state_index);
		(* Print some information *)
		if verbose_mode_greater Verbose_high then (
			let beginning_message = (if added then "NEW STATE" else "Old state") in
			print_message Verbose_high ("\n" ^ beginning_message ^ " reachable through action '" ^ (model.action_names action_index) ^ "': ");
			print_message Verbose_high (ModelPrinter.string_of_state model new_state);
		);
	
		(* The end: do nothing *)
		()
	

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Actions to perform when meeting a state with no successors: nothing to do for this algorithm *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method process_deadlock_state state_index = ()
	
	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(* Method packaging the result output by the algorithm *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method compute_result =
		PostStar_result
		{
			(* Explored state space *)
			state_space			= state_space;
			
			(* Nature of the state space (needed??) *)
		(* 	tile_nature			: AbstractModel.tile_nature; *)
			
			(* Total computation time of the algorithm *)
			computation_time	= time_from start_time;
			
			(* Termination *)
			termination			= 
				match termination_status with
				| None -> raise (InternalError "Termination status not set in PostStar.compute_result")
				| Some status -> status
			;
		}
	
(************************************************************)
(************************************************************)
end;;
(************************************************************)
(************************************************************)