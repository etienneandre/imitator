(************************************************************
 *
 *                       IMITATOR
 *
 * Laboratoire Spécification et Vérification (ENS Cachan & CNRS, France)
 * Université Paris 13, LIPN, CNRS, France
 * Université de Lorraine, CNRS, Inria, LORIA, Nancy, France
 *
 * Module description: Main file for IMITATOR
 *
 * File contributors : Ulrich Kühne, Étienne André, Laure Petrucci, Dylan Marinho
 * Created           : 2009/09/07
 * Last modified     : 2021/04/20
 *
 ************************************************************)



(************************************************************)
(* Internal modules *)
(************************************************************)
open Exceptions
open OCamlUtilities

open ImitatorUtilities
open AbstractModel
open AbstractAlgorithm
open AbstractProperty
open Result
open Options
open Statistics


(**************************************************
TAGS USED THROUGHOUT THIS PROJECT
- (*** BADPROG ***)
- (*** NOTE ***)
- (*** OPTIMIZED ***)
- (*** QUESTION ***)
- (*** TO OPTIMIZE ***)
- (*** TODO ***)
- (*** WARNING ***)
**************************************************)


;;


(************************************************************)
(************************************************************)
(* STARTING PROGRAM *)
(************************************************************)
(************************************************************)


(************************************************************)
(* Start the global counters *)
(************************************************************)
(* Counter counting everything from beginning to the end *)
let global_counter = create_time_counter_and_register "total" Global_counter Verbose_standard in
global_counter#start;

(* Counter counting everything except the final processing (graphics, external files generation, etc.) *)
let counter_algorithm_and_parsing = create_time_counter_and_register "main algorithm + parsing" Algorithm_counter Verbose_standard in
counter_algorithm_and_parsing#start;

(* Counter counting everything except the final processing (graphics, external files generation, etc.) and the parsing *)
let counter_main_algorithm = create_time_counter_and_register "main algorithm" Algorithm_counter Verbose_standard in



(************************************************************)
(* BEGIN EXCEPTION MECHANISM *)
(************************************************************)

begin
try(

(************************************************************)
(************************************************************)
(* Print startup message *)
(************************************************************)
(************************************************************)

(* Print header *)
print_header_string();


(************************************************************)
(* Get the arguments *)
(************************************************************)

(* let options_parsing_counter = create_time_counter_and_register "options parsing" Parsing_counter Verbose_low in
options_parsing_counter#start;*)

(* object with command line options *)
let options = new imitator_options in

options#parse;

(* Set the options (for other modules) *)
Input.set_options options;

(*** BUG: verbose mode has been set before the start and the stop; this particular counter may never stop! ***)
(* options_parsing_counter#stop; *)


(* Print date *)
print_message Verbose_experiments ("Analysis time: " ^ (now()) ^ "\n");


(************************************************************)
(* Record backtrace if verbose > standard *)
(************************************************************)
if verbose_mode_greater Verbose_low then(
	Printexc.record_backtrace true;
);



(************************************************************)
(* Get input *)
(************************************************************)
let parsing_counter = create_time_counter_and_register "model parsing and converting" Parsing_counter Verbose_standard in
parsing_counter#start;



(*------------------------------------------------------------*)
(* Parse the model and the property *)
(*------------------------------------------------------------*)

let model, property_option = ParsingUtility.compile_model_and_property options in

(*------------------------------------------------------------*)
(* Set both abstract structures *)
(*------------------------------------------------------------*)

print_message Verbose_low "Set the model.";
Input.set_model model;

begin
match property_option with
	| None ->
		print_message Verbose_low "No property to set.";
		()
	| Some property ->
		print_message Verbose_low "Set the property.";
		Input.set_property property;
end;



(* End of parsing *)
parsing_counter#stop;


(************************************************************)
(* Set some (default) options *)
(************************************************************)

(* Set default options depending on the IMITATOR mode *)

(*------------------------------------------------------------*)
(* Output-result *)
(*------------------------------------------------------------*)

(* Update if not yet set *)
if not options#is_set_output_result then(
	let default_value = match options#imitator_mode with
		| Algorithm | Syntax_check | State_space_computation
			-> true

		| Translation _
			-> false
	in

	(* Print some information *)
	print_message Verbose_high ("Set option `-output-result` to its default value: `" ^ (string_of_bool default_value) ^ "`");

	options#set_output_result default_value;
);





(*------------------------------------------------------------*)
(* Merge *)
(*------------------------------------------------------------*)

(* Get value depending on the algorithm *)
begin match property_option, options#imitator_mode with
	| Some property, _ ->
		(* Update if not yet set *)
		if not options#is_set_mergeq then (
			let merge_needed = AlgorithmOptions.merge_needed property in

			(* Print some information *)
			print_message Verbose_high ("Case option `-mergeq` not set");

			options#set_mergeq(false);

			if not options#is_set_merge then(
				(* Print some information *)
				print_message Verbose_high ("Set option `-merge` to its default value: `" ^ (string_of_bool merge_needed) ^ "`");

				options#set_merge (merge_needed);
			);
		);
		(* Update if not yet set *)
		if not options#is_set_merge212 then (
			(* Print some information *)
			print_message Verbose_high ("Case option `-merge212` not set");

			options#set_merge212(false);
		);

	| _, State_space_computation
		->
		(* Update if not yet set *)
		if not options#is_set_mergeq then (
			(* Print some information *)
			print_message Verbose_high ("Case option `-mergeq` not set");

			options#set_mergeq(false);

			if not options#is_set_merge then(
				(* Print some information *)
				print_message Verbose_high ("Set option `-merge` to its default value: `false`");

				(*** BADPROG: this default option value should not be hard-coded here ***)
				options#set_merge(false);
			);
		);
		(* Update if not yet set *)
		if not options#is_set_merge212 then (
			(* Print some information *)
			print_message Verbose_high ("Case option `-merge212` not set");

			options#set_merge212(false);
		);
	| None, _ -> ()
end;


(*(*------------------------------------------------------------*)
(* Exploration order *)
(*------------------------------------------------------------*)

(* Get value depending on the algorithm *)
begin match property_option, options#imitator_mode with
	| Some property, _
		->
		let default_exploration_order = AlgorithmOptions.default_exploration_order property in
		(* Update if not yet set *)
		if not options#is_set_exploration_order then(
			(* Print some information *)
			print_message Verbose_high ("Set option `-expl-order` to its default value: `" ^ (AbstractAlgorithm.string_of_exploration_order default_exploration_order) ^ "`");

			options#set_exploration_order (default_exploration_order);
		);

	| _, State_space_computation
		->
		(* Update if not yet set *)
		if not options#is_set_exploration_order then(
			(* Print some information *)
			print_message Verbose_high ("Set option `-expl-order` to its default value: `layerBFS`");

			(*** BADPROG: this default option value should not be hard-coded here ***)
			options#set_exploration_order (Exploration_layer_BFS);
		);

	| None, _ -> ()

end;*)


(*------------------------------------------------------------*)
(* Cycle Algorithm *)
(*------------------------------------------------------------*)

(* Get value depending on the algorithm *)
begin match property_option, options#imitator_mode with
	| Some property, _
		->
		(* Update if not yet set *)
		if not options#is_set_cycle_algorithm then(
			(*** HACK: hard-coded directly ***)
			let default_cycle_algorithm_option = match property.property with
				| Cycle_through _ -> Some NDFS
				| _ -> None
			in

			match default_cycle_algorithm_option with
			| Some default_cycle_algorithm ->
				(* Print some information *)
				print_message Verbose_high ("Set option `-cycle-algo` to its default value: `" ^ (AbstractAlgorithm.string_of_cycle_algorithm default_cycle_algorithm) ^ "`");

				options#set_cycle_algorithm default_cycle_algorithm;
			| None -> ()
		);

	| _, State_space_computation
	| None, _ ->
		(* Nothing to do *)
		()
end;


(*------------------------------------------------------------*)
(* Comparison operator between states *)
(*------------------------------------------------------------*)
(*** NOTE: important to do it AFTER the cycle algorithm has been set! ***)

(* Get value depending on the algorithm *)
begin match property_option, options#imitator_mode with
	| Some property, _
		->
		(* Update if not yet set *)
		if not options#is_set_comparison_operator then(

			let default_state_comparison = AlgorithmOptions.default_state_comparison property in

			let overwritten_default_state_comparison =

(*			(*** HACK! Hard-code / force the default value for cycle algorithms ***)
			match property.property with
			| Cycle_through _ ->
				let result =
				match options#cycle_algorithm with
					| NDFS -> Equality_check
					| BFS  -> Including_check
				in result

			| _ ->*)
			(* Rely on default value *)
				default_state_comparison

			in

			(* Print some information *)
			print_message Verbose_high ("Set option `-comparison` to its default value: `" ^ (AbstractAlgorithm.string_of_state_comparison_operator overwritten_default_state_comparison) ^ "`");

			(* Set *)
			options#set_comparison_operator overwritten_default_state_comparison;
		);

	| _, State_space_computation
		->
		(* Update if not yet set *)
		if not options#is_set_comparison_operator then(
			(* Print some information *)
			print_message Verbose_high ("Set option `-comparison` to its default value: `equality`");

			(*** BADPROG: this default option value should not be hard-coded here ***)
			options#set_comparison_operator Equality_check;
		);

	| None, _ -> ()

end;


(*------------------------------------------------------------*)
(* Layer (for NDFS) *)
(*------------------------------------------------------------*)

(* Get value depending on the algorithm *)
begin match property_option, options#imitator_mode with
	| Some property, _ ->
		(*** HACK: hard-coded directly ***)
		let layer_needed = match property.property with
			| Cycle_through _ when options#cycle_algorithm = NDFS -> Some false
			| _ -> None
		in
		(* Update if not yet set *)
		if not options#is_set_layer then (
			(* Print some information *)
			print_message Verbose_high ("Case option `-layer` not set");

			match layer_needed with
			| Some b -> options#set_layer (b);
			| None -> ()
		);

	(* Otherwise: leave unchanged *)
	| _, State_space_computation
	| None, _ -> ()
end;


(*------------------------------------------------------------*)
(* Subsumption (for NDFS) *)
(*------------------------------------------------------------*)

(* Get value depending on the algorithm *)
begin match property_option, options#imitator_mode with
	| Some property, _ ->
		(*** HACK: hard-coded directly ***)
		let subsumption_needed = match property.property with
			| Cycle_through _ when options#cycle_algorithm = NDFS -> Some true
			| _ -> None
		in
		(* Update if not yet set *)
		if not options#is_set_subsumption then (
			(* Print some information *)
			print_message Verbose_high ("Case option `-subsumption` not set");

			match subsumption_needed with
			| Some b -> options#set_subsumption (b);
			| None -> ()
		);

	(* Otherwise: leave unchanged *)
	| _, State_space_computation
	| None, _ -> ()
end;


(*------------------------------------------------------------*)
(* NZ Algorithm *)
(*------------------------------------------------------------*)

(* Get value depending on the algorithm *)
begin match property_option, options#imitator_mode with
	| Some property, _
		->
		(*** HACK: hard-coded directly ***)
		let default_nz_method_option = match property.property with
			| NZ_Cycle -> Some NZ_transform
			| _ -> None
		in

		(* Update if not yet set *)
		if not options#is_set_nz_method then(
			match default_nz_method_option with
			| Some default_nz_method ->
				(* Print some information *)
				print_message Verbose_high ("Set option `-nz-method` to its default value: `transform`");

				options#set_nz_method (default_nz_method);
			| None -> ()
		);

	| _, State_space_computation
	| None, _ ->
		(* Nothing to do *)
		()
end;



(*------------------------------------------------------------*)
(* Special cartography options *)
(*------------------------------------------------------------*)

(* Set some options depending on the IMITATOR mode *)
let is_cartography = match property_option with
	| None -> false
	| Some property -> AlgorithmOptions.is_cartography property
in
options#set_options_for_cartography is_cartography;


(************************************************************)
(* Recall options and print some warnings if needed *)
(************************************************************)

(* Recall the arguments *)
options#recall_and_warn model property_option;


(************************************************************)
(* Debug print: model *)
(************************************************************)
if verbose_mode_greater Verbose_high then(
	print_message Verbose_total ("\nPreparing to print the model…");
	let model_string = ModelPrinter.string_of_model model in
	print_message Verbose_high ("\nThe input model is the following one:\n" ^ model_string ^ "\n");
);


(************************************************************)
(* Debug print: property *)
(************************************************************)
begin
match options#property_file_name with
	| Some _ ->
		let property = Input.get_property() in

		print_message Verbose_total ("\nPreparing to print the property…");
		let property_string = ModelPrinter.string_of_abstract_property model property in

		print_message Verbose_low ("\nThe property is the following one:\n" ^ property_string ^ "\n");

	| None ->
		()

end;




(* Statistics *)
counter_main_algorithm#start;


(************************************************************)
(* Dynamic clock elimination *)
(************************************************************)
(* Need to be called before initial state is created! *)
if options#dynamic_clock_elimination then (
	print_message Verbose_low "Initializing clock elimination…";
	ClocksElimination.prepare_clocks_elimination ()
);



(************************************************************)
(************************************************************)
(* Start branching depending on the algorithm *)
(************************************************************)
(************************************************************)

begin
match options#imitator_mode with
	| Syntax_check ->

	(************************************************************)
	(* Case no analysis *)
	(************************************************************)
	(* If arrived here, syntax is correct *)
	print_message Verbose_standard "Syntax is correct. Have fun!";

	(* Generate directly the "empty" result for syntax check *)
	ResultProcessor.process_result_and_terminate Syntax_check_result "syntax check" None global_counter


	(************************************************************)
	(* Case translation *)
	(************************************************************)
	(* Translation to text language (IMITATOR, other model checker, TikZ) *)
	| Translation IMI | Translation HyTech | Translation TikZ | Translation Uppaal | Translation JaniSpec | Translation DOT ->

		(*** NOTE: not super nice… ***)
		let printer = match options#imitator_mode with
			| Translation IMI		-> ModelPrinter.string_of_model
			| Translation HyTech	-> PTA2HyTech.string_of_model
			| Translation TikZ		-> PTA2TikZ.tikz_string_of_model
			| Translation Uppaal	-> PTA2Uppaal.string_of_model
      | Translation JaniSpec	-> PTA2JaniSpec.string_of_model
			| Translation DOT       -> PTA2JPG.string_of_model
			| _						-> raise (InternalError ("Impossible situation: No target for translation was found, although it should have been"))
		in

		(*** NOTE: not super nice… ***)
		let suffix = match options#imitator_mode with
			| Translation IMI		-> "-regenerated" ^ Constants.model_extension
			| Translation HyTech	-> ".hy"
			| Translation TikZ		-> ".tex"
			| Translation Uppaal	-> "-uppaal.xml"
      | Translation JaniSpec	-> ".jani"
			| Translation DOT       -> ".dot"
			| _						-> raise (InternalError ("Impossible situation: No target for translation was found, although it should have been"))
		in

		print_message Verbose_standard ("Regenerating the input model to a new model.");
		let translated_model = printer model in
		let target_language_file = options#files_prefix ^ suffix in
		if verbose_mode_greater Verbose_total then(
			print_message Verbose_total ("\n" ^ translated_model ^ "\n");
		);
		(* Write *)
		write_to_file target_language_file translated_model;
		print_message Verbose_standard ("File '" ^ target_language_file ^ "' successfully created.");

		(* Create a file with some statistics on the origina model if requested *)
		ResultProcessor.process_result Translation_result ("translation to " ^ (AbstractAlgorithm.string_of_translation
			(match options#imitator_mode with Translation translation -> translation | _ -> raise (InternalError ("Impossible situation: No target for translation was found, although it should have been"))
			)) ) None;

		terminate_program()

	(* Translation to a graphics *)
	| Translation JPG | Translation PDF | Translation PNG ->
		print_message Verbose_medium ("Translating model to a graphics…");
		let translated_model = PTA2JPG.string_of_model model in
		if verbose_mode_greater Verbose_high then(
			print_message Verbose_high ("\n" ^ translated_model ^ "\n");
		);
		(*** NOTE: not so nice… ***)
		let extension = match options#imitator_mode with
			| Translation JPG	-> "jpg"
			| Translation PDF	-> "pdf"
			| Translation PNG	-> "png"
			| _					-> raise (InternalError ("Impossible situation: No graphic extension found although JPG/PDF/PNG was expected"))
		in
		let dot_created_file_option = Graphics.dot extension (options#files_prefix ^ "-pta") translated_model in
		begin
		match dot_created_file_option with
		| None -> print_error "Oops…! Something went wrong with dot."
		| Some created_file -> print_message Verbose_standard ("File `" ^ created_file ^ "` successfully created.");
		end;

		(* Create a file with some statistics on the original model if requested *)
		ResultProcessor.process_result_and_terminate Translation_result "translation to graphics" None global_counter


	(************************************************************)
	(* Computation of the whole state space *)
	(************************************************************)
	| State_space_computation ->

		(*** NOTE: this is static subclass coercition; see https://ocaml.org/learn/tutorials/objects.html ***)
		let concrete_algorithm :> AlgoGeneric.algoGeneric = new AlgoPostStar.algoPostStar in

		(*** NOTE: duplicate code with what follows ***)

		let result = concrete_algorithm#run() in

		(* Stop the main algorithm counters *)
		counter_algorithm_and_parsing#stop;
		counter_main_algorithm#stop;

		(* Process and terminate *)
		ResultProcessor.process_result_and_terminate result concrete_algorithm#algorithm_name None global_counter


	(************************************************************)
	(* Some algorithm *)
	(************************************************************)
	(** Synthesis algorithm *)
	| Algorithm ->
	begin
		(* Retrieve the algorithm *)
		(*** NOTE: at this stage, we are sure to have defined a property ***)
		let abstract_property = Input.get_property() in

		let emptiness_only =
			match abstract_property.synthesis_type with
			| Witness   -> true
			| Synthesis -> false
		in


		(************************************************************)
		(* Preliminary checks *)
		(************************************************************)

		begin
		match abstract_property.property with
		| EFexemplify _ | EFtmin _ ->
			begin
			match model.global_time_clock with
				| Some _ -> ()
				| _ ->
					print_error ("An absolute time clock `" ^ Constants.global_time_clock_name ^ "` must be defined in the model to run this algorithm.");
					abort_program();
			end;

		| _ -> ()

		end;




		(************************************************************)
		(************************************************************)
		(* Run IMITATOR *)
		(************************************************************)
		(************************************************************)

		(* Find the correct concrete algorithm to execute *)
		let concrete_algorithm : AlgoGeneric.algoGeneric = match abstract_property.property with


		(*------------------------------------------------------------*)
		(* Non-nested CTL *)
		(*------------------------------------------------------------*)
			(************************************************************)
			(* Reachability *)
			(************************************************************)
			| EF state_predicate ->

				let myalgo :> AlgoGeneric.algoGeneric = new AlgoEFunsafeSynth.algoEFunsafeSynth state_predicate in myalgo


			(************************************************************)
			(* Safety *)
			(************************************************************)
			| AGnot state_predicate ->

				(*** NOTE: witness not supported (we need to compute everything to make sure the system is safe) ***)
				if abstract_property.synthesis_type = Witness then(
					print_warning "Exhibition of a subset of parameter valuations is not yet supported by this algorithm; either the whole set of valuations will be computed, or an over-approximation of this set.";
				);

				let myalgo :> AlgoGeneric.algoGeneric = new AlgoAGsafeSynth.algoAGsafeSynth state_predicate in myalgo


		(*------------------------------------------------------------*)
		(* Reachability and specification illustration *)
		(*------------------------------------------------------------*)
			| EFexemplify state_predicate ->
				let myalgo :> AlgoGeneric.algoGeneric = new AlgoEFexemplify.algoEFexemplify state_predicate in myalgo


		(*------------------------------------------------------------*)
		(* Optimized reachability *)
		(*------------------------------------------------------------*)
			(************************************************************)
			(* Reachability with minimization of a parameter valuation *)
			(************************************************************)
			| EFpmin (state_predicate , parameter_index) ->
				let efopt_algo = new AlgoEFmin.algoEFmin state_predicate parameter_index in
				(*** NOTE: very important: must set NOW the parameters ***)
				efopt_algo#set_synthesize_valuations (not emptiness_only); (* Synthesis of valuations out of the desired parameter *)
				let myalgo :> AlgoGeneric.algoGeneric = efopt_algo in
				myalgo


			(************************************************************)
			(* Reachability with maximization of a parameter valuation *)
			(************************************************************)
			| EFpmax (state_predicate , parameter_index) ->
				let efopt_algo = new AlgoEFmax.algoEFmax state_predicate parameter_index  in
				(*** NOTE: very important: must set NOW the parameters ***)
				efopt_algo#set_synthesize_valuations (not emptiness_only); (* Synthesis of valuations out of the desired parameter *)
				let myalgo :> AlgoGeneric.algoGeneric = efopt_algo in
				myalgo


			(************************************************************)
			(* Reachability with minimal-time *)
			(************************************************************)
			| EFtmin state_predicate ->
				let myalgo :> AlgoGeneric.algoGeneric = new AlgoEFtminQueue.algoEFtminQueue state_predicate in myalgo



		(*------------------------------------------------------------*)
		(* Cycles *)
		(*------------------------------------------------------------*)

			(************************************************************)
			(* Parametric loop synthesis *)
			(************************************************************)

			(** Accepting infinite-run (cycle) using an accepting keyword *)
			| Cycle_through state_predicate ->
				let myalgo :> AlgoGeneric.algoGeneric =
				(* Branching depending on the requested algorithm *)
				match options#cycle_algorithm with
					| AbstractAlgorithm.BFS -> let myalgo :> AlgoGeneric.algoGeneric = new AlgoAccLoopSynth.algoAccLoopSynth state_predicate in myalgo
					| AbstractAlgorithm.NDFS -> let myalgo :> AlgoGeneric.algoGeneric = new AlgoNDFS.algoNDFS state_predicate in myalgo
				in myalgo


			(** Infinite-run (cycle) with non-Zeno assumption *)
 			| NZ_Cycle ->
				(* Important! Set the no-time-elapsing option *)
				options#set_no_time_elapsing;

				let algo =

				(* Branch depending on the NZ method *)
				match options#nz_method with
				(** Method by checking whether the PTA is already a CUB-PTA for some valuation *)
				| NZ_check ->
					(* Computing a constraint for which the PTA is CUB *)
					print_message Verbose_standard ("Checking whether the PTA is CUB for some parameter valuations…");

					let cub_constraint = CUBchecker.check_cub model in

					if verbose_mode_greater Verbose_low then(
						(* Computing a constraint for which the PTA is CUB *)
						print_message Verbose_low ("Computed CUB constraint");
						print_message Verbose_low (LinearConstraint.string_of_p_linear_constraint model.variable_names cub_constraint);
						print_message Verbose_low ("Comparing the computed constraint with the initial constraint:");
						print_message Verbose_low (LinearConstraint.string_of_p_linear_constraint model.variable_names model.initial_p_constraint);

					);

					(* Compare if the model is CUB for *all* valuations *)
					let is_universally_cub = LinearConstraint.p_is_equal cub_constraint model.initial_p_constraint in

					if is_universally_cub then(
						print_message Verbose_standard ("The model is a CUB-PTA for all defined parameter valuations, i.e.:");
					)else(
						print_message Verbose_standard ("The model is a CUB-PTA for the following parameter valuations:");
					);
					print_message Verbose_standard (LinearConstraint.string_of_p_linear_constraint model.variable_names cub_constraint);

					(*** TODO: check if the constraint is stricter than the original constraint; if yes, the result can only be an under-approximation ***)

					(* Update the model *)
					LinearConstraint.px_intersection_assign_p model.initial_constraint [cub_constraint];
					(* Update the initial p constraint too *)
					LinearConstraint.p_intersection_assign model.initial_p_constraint [cub_constraint];

					(* Call the NZ emptiness check *)
					let nz_algo = new AlgoNZCUB.algoNZCUB in

					(* Force under-approximation if not universally CUB *)
					if not is_universally_cub then(
						nz_algo#force_underapproximation;
					);

					let myalgo :> AlgoGeneric.algoGeneric = nz_algo in myalgo

				(** Method by transforming the PTA into a CUB-PTA *)
				| NZ_transform ->
					print_message Verbose_standard ("Generating the transformed model…");

					let cub_model = CUBchecker.cubpta_of_pta model in
					(*** HACK: set the model in the input module too ***)
					Input.set_model cub_model;

					print_message Verbose_standard ("Transformation completed");

					(* Only export to file in graphics for >= Verbose_low *)
					if verbose_mode_greater Verbose_low then(
						(* Export the model to a file *)
						(*** TODO: not necessary? (but so far useful to test) ***)

						(* Print some information *)
						print_message Verbose_low ("Preparing the transformed model conversion to string…");

						let translated_model = ModelPrinter.string_of_model cub_model in

						(* Print some information *)
						print_message Verbose_medium ("About to write the transformed model to file…");

						let imi_file = options#files_prefix ^ "-cub" ^ Constants.model_extension in
						if verbose_mode_greater Verbose_total then(
							print_message Verbose_total ("\n" ^ translated_model ^ "\n");
						);

						(* Write *)
						write_to_file imi_file translated_model;
						print_message Verbose_low ("File '" ^ imi_file ^ "' successfully created.");


						(* Then transform to a graphics *)
						(*** TODO: not necessary? (but so far useful to test) ***)

						let translated_model = PTA2JPG.string_of_model cub_model in
						if verbose_mode_greater Verbose_high then(
							print_message Verbose_high ("\n" ^ translated_model ^ "\n");
						);

						let dot_created_file_option = Graphics.dot Constants.pta_default_image_format (options#files_prefix ^ "-cubpta") translated_model in

						begin
						match dot_created_file_option with
						| None -> print_error "Oops…! Something went wrong with dot."
						| Some created_file -> print_message Verbose_low ("Graphic export `" ^ created_file ^ "` successfully created.");
						end;

					); (* end export *)

					(* Call the NZ emptiness check *)
					let myalgo :> AlgoGeneric.algoGeneric = new AlgoNZCUB.algoNZCUB in myalgo


				(** Method assuming the PTA is already a CUB-PTA *)
				| NZ_already ->
					(* Just call the NZ emptiness check *)
					let myalgo :> AlgoGeneric.algoGeneric = new AlgoNZCUB.algoNZCUB in myalgo

				in algo



		(*------------------------------------------------------------*)
		(* Deadlock-freeness *)
		(*------------------------------------------------------------*)

			(************************************************************)
			(* Parametric deadlock checking *)
			(************************************************************)
			| Deadlock_Freeness ->
				let myalgo :> AlgoGeneric.algoGeneric = new AlgoDeadlockFree.algoDeadlockFree in myalgo

		(*------------------------------------------------------------*)
		(* Inverse method, trace preservation, robustness *)
		(*------------------------------------------------------------*)

			(************************************************************)
			(* Inverse method *)
			(************************************************************)

			(* Inverse method with complete, non-convex result *)
			| IM pval ->
					let myalgo :> AlgoGeneric.algoGeneric = new AlgoIMcomplete.algoIMcomplete pval in myalgo

			(* Non-complete, non-deterministic inverse method with convex result *)
			| ConvexIM pval ->
					let myalgo :> AlgoGeneric.algoGeneric = new AlgoIM.algoIM pval in myalgo

			(* Parametric reachability preservation *)
			| PRP (state_predicate, pval) ->
					let myalgo :> AlgoGeneric.algoGeneric = new AlgoPRP.algoPRP pval state_predicate in myalgo

			(* Variant IMK of the Inverse method *)
			| IMK pval ->
					let myalgo :> AlgoGeneric.algoGeneric = new AlgoIMK.algoIMK pval in myalgo

			(* Variant IMunion of the Inverse method *)
			| IMunion pval ->
					let myalgo :> AlgoGeneric.algoGeneric = new AlgoIMunion.algoIMunion pval in myalgo


		(*------------------------------------------------------------*)
		(* Cartography algorithms *)
		(*------------------------------------------------------------*)

			(* Cartography *)
			| Cover_cartography (hyper_rectangle, step) when options#distribution_mode = Non_distributed ->
				let bc_algo = new AlgoBCCover.algoBCCover hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
				let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
				myalgo

			(** Cover the whole cartography using learning-based abstractions *)
			| Learning_cartography (state_predicate, hyper_rectangle, step) ->
			(*** NOTE: cannot reintroduce it unless the compositional verifier "CV" is updated to the IMITATOR 3.0 syntax ***)
				raise (NotImplemented("Learning_cartography is temporarily disabled"))
(*				let bc_algo = new AlgoBCCoverLearning.algoBCCoverLearning state_predicate hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_good_bad_constraint in
				let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
				myalgo*)

			(** Cover the whole cartography after shuffling point (mostly useful for the distributed IMITATOR) *)
			| Shuffle_cartography (hyper_rectangle, step) ->
				let bc_algo = new AlgoBCShuffle.algoBCShuffle hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
				let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
				myalgo

			(** Look for the border using the cartography*)
			| Border_cartography (hyper_rectangle, step) ->
				raise (NotImplemented("Border cartography is disabled"))

			(** Randomly pick up values for a given number of iterations *)
			| Random_cartography (hyper_rectangle, max_tries, step) ->
				let bc_algo = new AlgoBCRandom.algoBCRandom hyper_rectangle step max_tries (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
				let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
				myalgo

			(** Randomly pick up values for a given number of iterations, then switch to sequential algorithm once no more point has been found after a given max number of attempts (mostly useful for the distributed IMITATOR) *)
			| RandomSeq_cartography (hyper_rectangle, max_tries, step) ->
				let bc_algo = new AlgoBCRandomSeq.algoBCRandomSeq hyper_rectangle step max_tries (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
				let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
				myalgo

			(* Parametric reachability preservation *)
			| PRPC (state_predicate, hyper_rectangle, step) ->
				let bc_algo = new AlgoBCCover.algoBCCover hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoPRP.algoPRP pval state_predicate in myalgo) AlgoCartoGeneric.Tiles_good_bad_constraint in
				let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
				myalgo



			(************************************************************)
			(* Begin distributed cartography *)
			(************************************************************)

			(*** WARNING:  Do not modify the following lines! (used by an external script to compile the non-distributed version of IMITATOR) ***)
			(*(* ** *** **** ***** ******    BEGIN FORK PaTATOR    ****** ***** **** *** ** *)

			(** TODO: add conditions to CUB
			| Parametric_NZ_CUBtransformDistributed ->
				print_message Verbose_standard ("Generating the transformed model…");

				let cub_model = CUBchecker.cubpta_of_pta model in
				(*** HACK: set the model in the input module too ***)
				Input.set_model cub_model;

				print_message Verbose_standard ("Transformation completed");

				(* Only export to file in graphics for >= Verbose_low *)
				if verbose_mode_greater Verbose_low then(
					(* Export the model to a file *)
					(*** TODO: not necessary? (but so far useful to test) ***)

					let translated_model = ModelPrinter.string_of_model cub_model in

					let imi_file = options#files_prefix ^ "-cub.imi" in
					if verbose_mode_greater Verbose_total then(
						print_message Verbose_total ("\n" ^ translated_model ^ "\n");
					);

					(* Write *)
					write_to_file imi_file translated_model;
					print_message Verbose_low ("File '" ^ imi_file ^ "' successfully created.");


					(* Then transform to a graphics *)
					(*** TODO: not necessary? (but so far useful to test) ***)

					let translated_model = PTA2JPG.string_of_model cub_model in
					if verbose_mode_greater Verbose_high then(
						print_message Verbose_high ("\n" ^ translated_model ^ "\n");
					);

					let dot_created_file_option = Graphics.dot Constants.pta_default_image_format (options#files_prefix ^ "-cubpta") translated_model in

					begin
					match dot_created_file_option with
						| None -> print_error "Oops…! Something went wrong with dot."
						| Some created_file -> print_message Verbose_low ("Graphic export `" ^ created_file ^ "` successfully created.");
					end;
				); (* end export *)

				(* Call the NZ emptiness check *)
				let myalgo :> AlgoGeneric.algoGeneric = new AlgoNZCUBdist.algoNZCUBdist in myalgo
			*)

			(*** NOTE: only one distribution mode so far ***)
			| Cover_cartography (hyper_rectangle, step) when options#distribution_mode <> Non_distributed ->
				let algo = match options#distribution_mode with

				(** Distributed mode: Master worker with sequential pi0 *)
				| Distributed_ms_sequential ->
					(* Branch between master and worker *)
					if DistributedUtilities.is_master() then
						let bc_algo = new AlgoBCCoverDistributedMSSeqMaster.algoBCCoverDistributedMSSeqMaster hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo
					else
						let bc_algo = new AlgoBCCoverDistributedMSSeqWorker.algoBCCoverDistributedMSSeqWorker hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo
				(** Distributed mode: Master worker with sequential pi0 shuffled *)
				| Distributed_ms_shuffle ->
					(* Branch between master and worker *)
					if DistributedUtilities.is_master() then
						let bc_algo = new AlgoBCCoverDistributedMSShuffleMaster.algoBCCoverDistributedMSShuffleMaster hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo
					else
						let bc_algo = new AlgoBCCoverDistributedMSShuffleWorker.algoBCCoverDistributedMSShuffleWorker hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo

				(** Distributed mode: Master worker with random pi0 and n retries before switching to sequential mode *)
				| Distributed_ms_random nb_tries ->
					(* Branch between master and worker *)
					if DistributedUtilities.is_master() then
						let bc_algo = new AlgoBCCoverDistributedMSRandomSeqMaster.algoBCCoverDistributedMSRandomSeqMaster hyper_rectangle step nb_tries (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo
					else
						let bc_algo = new AlgoBCCoverDistributedMSRandomSeqWorker.algoBCCoverDistributedMSRandomSeqWorker hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo

				(** Distributed mode: Master worker with subdomain distribution *)
				| Distributed_ms_subpart ->
					(* Branch between master and worker *)
					if DistributedUtilities.is_master() then
						let bc_algo = new AlgoBCCoverDistributedSubdomainDynamicCoordinator.algoBCCoverDistributedSubdomainDynamicCoordinator hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo
					else
						let bc_algo = new AlgoBCCoverDistributedSubdomainDynamicCollaborator.algoBCCoverDistributedSubdomainDynamicCollaborator hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo

				(** Distributed mode: static distribution mode (each node has its own subdomain with no communication) *)
				| Distributed_static ->
					(* Branch between collaborator and coordinator *)
					if DistributedUtilities.is_coordinator() then
						let bc_algo = new AlgoBCCoverDistributedSubdomainStaticCoordinator.algoBCCoverDistributedSubdomainStaticCoordinator hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo
					else
						let bc_algo = new AlgoBCCoverDistributedSubdomainStaticCollaborator.algoBCCoverDistributedSubdomainStaticCollaborator hyper_rectangle step (fun pval -> let myalgo :> AlgoStateBased.algoStateBased = new AlgoIM.algoIM pval in myalgo) AlgoCartoGeneric.Tiles_list in
						let myalgo :> AlgoGeneric.algoGeneric = bc_algo in
						myalgo

				| _ -> raise (InternalError("Other distribution modes not yet implemented"))

				in algo


			(* ** *** **** ***** ******    END FORK PaTATOR    ****** ***** **** *** ** *)*)
			(*** WARNING:  Do not modify the previous lines! (used by an external script to compile the non-distributed version of IMITATOR) ***)

			(************************************************************)
			(* End distributed cartography *)
			(************************************************************)



			(*** NOTE: safety to avoid a warning when compiling the non-distributed version of IMITATOR ***)
			| Cover_cartography _ (*when options#distribution_mode <> Non_distributed *)->
				(* Situation that can happen when using the -distributed version *)
				print_error ("A distributed mode has been set, but this is the non-distributed version of `" ^ (Constants.program_name) ^ "`");
				abort_program();
				exit 1;
			in



		(* Run! *)
		let result = concrete_algorithm#run() in

		(* Stop the main algorithm counters *)
		counter_algorithm_and_parsing#stop;
		counter_main_algorithm#stop;

		(* Process *)
		ResultProcessor.process_result result concrete_algorithm#algorithm_name None;

	end; (* match type of abstract algorithm *)

(************************************************************)
(************************************************************)
(* End branching depending on the algorithm *)
(************************************************************)
(************************************************************)
end;



(************************************************************)
(* END EXCEPTION MECHANISM *)
(************************************************************)
) with
	e ->(

	(* Actions to perform for "bad" exceptions, i.e., that should NOT happen *)
	let abort_with_bad_exception (error_message : string) =
		(* Stop the main algorithm counters *)
		counter_algorithm_and_parsing#stop;
		counter_main_algorithm#stop;

		print_error (error_message ^ "\nPlease (politely) insult the developers.");
		Printexc.print_backtrace stderr;

		abort_program ();
		(* Safety *)
		exit 1
	in

	(* Actions to perform for "good" exceptions, i.e., that depend on the user model *)
	let abort_with_good_exception error_type error_message =
		(* Stop the main algorithm counters *)
		counter_algorithm_and_parsing#stop;
		counter_main_algorithm#stop;

		(* Print error *)
		print_error (error_message);

		(* Force output result if not set *)
		(*** NOTE: probably useless check ***)
		let options = Input.get_options () in
		if not options#is_set_output_result then(
			options#set_output_result true;
		);

		(* Process result (including file export, if possible) and fail *)
		ResultProcessor.process_result_and_abort error_type "unknown algorithm" (* because we lost this information somewhere… *) None global_counter;
	in

	begin match e with
		(* "Good" (at least not bad) exceptions *)

		| Division_by_0 msg -> abort_with_good_exception (Result.Division_by_zero msg) msg

		| UnsatisfiableInitialState -> abort_with_good_exception (Result.Unsatisfiable_initial_state) "Unsatisfiable initial state"



		(* "Bad" exceptions *)

		| Failure msg -> abort_with_bad_exception ("`Failure` exception: `" ^ msg ^ "`")

		| InterfacingError msg -> abort_with_bad_exception ("Interfacing error: " ^ msg ^ "")

		| InternalError msg -> abort_with_bad_exception ("Fatal internal error: " ^ msg ^ "")

		| Invalid_argument msg -> abort_with_bad_exception ("`Invalid_argument` exception: `" ^ msg ^ "`")

		| Not_found -> abort_with_bad_exception ("`Not_found` exception!")

		| NotImplemented msg -> abort_with_bad_exception ("A non-implemented feature has been called: " ^ msg ^ "")

		| Random_generator_initialization_exception-> abort_with_bad_exception("A fatal error occurred during the random generator initialization.")

		| SerializationError msg -> abort_with_bad_exception ("Serialization error: " ^ msg ^ "")

		| _ -> abort_with_bad_exception ("Fatal exception `" ^ (Printexc.to_string e) ^ "`.")
	end;

	(* Safety *)
	exit 1

	)
end; (* try *)




(************************************************************)
(* Handling statistics *)
(************************************************************)
global_counter#stop;

(* Only print counters if statistics are required, or experiments verbose mode *)
if (try (Input.get_options())#statistics with _ -> false) || verbose_mode_greater Verbose_experiments then
	print_message Verbose_standard (string_of_all_counters());


(************************************************************)
(* Bye bye! *)
(************************************************************)

terminate_program()
