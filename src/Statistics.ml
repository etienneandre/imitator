(************************************************************
 *
 *                       IMITATOR
 * 
 * Laboratoire Spécification et Vérification (ENS Cachan & CNRS, France)
 * Université Paris 13, LIPN, CNRS, France
 * Université de Lorraine, CNRS, Inria, LORIA, Nancy, France
 * 
 * Module description: Timed counter, that depends on a level of verbosity (the counter will only update when the global verbose_mode is larger or equal to that of the counter). Also maintains a list of all counters, for obtaining statistics easily.
 * 
 * File contributors : Étienne André
 * Created           : 2014/04/27
 * Fork from         : Counter.ml
 * Fork date         : 2016/05/17
 * Last modified     : 2021/06/24
 *
 ************************************************************)


(************************************************************)
(************************************************************)
(* Modules *)
(************************************************************)
(************************************************************)
open OCamlUtilities
open ImitatorUtilities


(************************************************************)
(************************************************************)
(* Type *)
(************************************************************)
(************************************************************)

type counterCategory =
	(** Algorithm functions *)
	| Algorithm_counter
	
	(** Cache counters *)
	| Cache_counter
	
	(** The global counter *)
	(*** TODO: prevent more than one such counter to be created ***)
	| Global_counter
	
	(** Everything related to graphics generation *)
	| Graphics_counter
	
	(** Lexing and parsing *)
	| Parsing_counter

	(** All calls to PPL *)
	| PPL_counter
	
	(** States computations *)
	| States_counter
	

(************************************************************)
(************************************************************)
(* Global variable *)
(************************************************************)
(************************************************************)
let all_counters_enabled = ref false


(************************************************************)
(************************************************************)
(* Class definition for generic counters *)
(************************************************************)
(************************************************************)
class virtual counter (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	object(self)

	(************************************************************)
	(* Class variables *)
	(************************************************************)

	(* Counter attributes *)
	val name = name
	val counter_category = counter_category
	val level = level

	(************************************************************)
	(* Class methods *)
	(************************************************************)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the name *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method name = name
	
	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the level *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method level = level
	
	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the category *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method category = counter_category
	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the counter's value in the form of a string *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method virtual string_of_value : string
	

(************************************************************)
(************************************************************)
end;;
(************************************************************)
(************************************************************)


(************************************************************)
(************************************************************)
(* Class definition for time counters *)
(************************************************************)
(************************************************************)
class timeCounter (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	object(self) inherit counter name counter_category level as super

	(************************************************************)
	(* Class variables *)
	(************************************************************)
	
	(* Current value *)
	val mutable value = 0.0
	(* Latest start time *)
	val mutable start_time = 0.0
	(* Running or not? *)
	val mutable running = false
	
	
	(************************************************************)
	(* Class methods *)
	(************************************************************)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Start the counter *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method start =
		if !all_counters_enabled || verbose_mode_greater level then(
			running <- true;
			start_time <- Unix.gettimeofday()
		)
	
	
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Stop the counter *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method stop =
		if !all_counters_enabled || verbose_mode_greater level then(
			running <- false;
			value <- value +. Unix.gettimeofday() -. start_time
		)
			
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Reset the counter *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method reset =
		if !all_counters_enabled || verbose_mode_greater level then(
			value <- 0.0
		)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the counter's continuous value *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method value =
		(* if running: first stop the counter to update the value *)
		if running then(
			self#stop;
			(* then restart it *)
			self#start;
		);
		(* Now get the value *)
		value

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the counter's value in the form of a string *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method string_of_value =
		string_of_seconds self#value

	
(************************************************************)
(************************************************************)
end;;
(************************************************************)
(************************************************************)


(************************************************************)
(************************************************************)
(* Class definition for discrete counters *)
(************************************************************)
(************************************************************)
class discreteCounter (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	object(self) inherit counter name counter_category level as super
		
	(************************************************************)
	(* Class variables *)
	(************************************************************)
	val mutable discrete_counter = 0
	
	
	(************************************************************)
	(* Class methods *)
	(************************************************************)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Increment the discrete counter *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method increment =
		discrete_counter <- discrete_counter + 1
		
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Increment the discrete counter by some integer *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method increment_by n =
		discrete_counter <- discrete_counter + n
		
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the counter's discrete value *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method discrete_value = discrete_counter
		
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the counter's value in the form of a string: continuous value, number of calls, and average call excecution *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method string_of_value =
		(* Discrete value *)
		string_of_int discrete_counter


(************************************************************)
(************************************************************)
end
(************************************************************)
(************************************************************)



(************************************************************)
(************************************************************)
(* Class definition for hybrid counters (discrete increment + time counters) *)
(************************************************************)
(************************************************************)
(*** TODO: rather use multiple inheritance from discreteCounter? ***)
class hybridCounter (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	object(self) inherit timeCounter name counter_category level as super
		
	(************************************************************)
	(* Class variables *)
	(************************************************************)
	val mutable discrete_counter = 0
	
	
	(************************************************************)
	(* Class methods *)
	(************************************************************)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Increment the discrete part *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method increment =
		discrete_counter <- discrete_counter + 1
		
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the counter's discrete value *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
(* 	method discrete_value = discrete_counter *)
		
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the counter's value in the form of a string: continuous value, number of calls, and average call excecution *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method string_of_value =
		(* Continuous value *)
		(string_of_seconds value)
		(* Discrete value *)
		^ " (" ^ (string_of_int discrete_counter) ^ " call" ^ (s_of_int discrete_counter)
		(* If nb calls > 0: Compute average *)
		 ^ (if discrete_counter = 0 then "" else(
			let average = value /. (float_of_int discrete_counter) in
			" | "
			(* Note: no "string_of_seconds" because not precise enough *)
			^ (string_of_float average)
			^ " second/call"
			)
		)
		(* The end *)
		^ ")"

(************************************************************)
(************************************************************)
end
(************************************************************)
(************************************************************)



(************************************************************)
(************************************************************)
(* Class definition for data *)
(************************************************************)
(************************************************************)
class data_recorder (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	object(self) inherit counter name counter_category level as super

	(************************************************************)
	(* Class variables *)
	(************************************************************)
	val mutable recorded_data = ""
	
	
	(************************************************************)
	(* Class methods *)
	(************************************************************)

	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Add data *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method add_data (data : string) : unit =
		(* Enqueue new data to previously recorded data *)
		recorded_data <- recorded_data ^ data


	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	(** Get the available data *)
	(*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*)
	method string_of_value : string =
		recorded_data

(************************************************************)
(************************************************************)
end
(************************************************************)
(************************************************************)


(************************************************************)
(************************************************************)
(* Class-independent global variables *)
(************************************************************)
(************************************************************)

(* Shortcut to iterate on categories *)
(*** NOTE: counters will be printed in this order ***)
let all_categories = [Algorithm_counter ; Parsing_counter ; Cache_counter ; PPL_counter ; States_counter ;  Graphics_counter ; Global_counter]

(* Global variable listing all counters (useful to get all statistics at once) *)
let all_counters : counter list ref= ref []


(************************************************************)
(************************************************************)
(* Class-independent functions *)
(************************************************************)
(************************************************************)

let string_of_category = function
	(** Algorithm functions *)
	| Algorithm_counter -> "Algorithm counters"
	
	(** Cache counters *)
	| Cache_counter -> "Cache counters"
	
	(** The global counter *)
	(*** TODO: prevent more than one such counter to be created ***)
	| Global_counter -> "Global counter"
	
	(** Everything related to graphics generation *)
	| Graphics_counter -> "Graphics-related counters"
	
	(** Lexing and parsing *)
	| Parsing_counter -> "Parsing counters"

	(** All calls to PPL *)
	| PPL_counter -> "PPL counters"

	(** States computations *)
	| States_counter -> "State computation counters"
	


(* Register a counter *)
let register counter =
	let well_typed_counter :> counter = counter in
	all_counters := well_typed_counter :: !all_counters;
	()
(*
(** Shortcut: create new counter and register it *)
let create_gen_counter_and_register creation_function (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	(* Create counter *)
	let my_new_counter :> timeCounter = (creation_function()) name counter_category level in
	
	(* Only register if verbose mode allows for it *)
	(*** NOTE: for now, register all counters (as the verbose_mode may not be initialized when the counters are created ***)
(* 	if !all_counters_enabled || verbose_mode_greater level then( *)
		(* Print some information *)
		print_message Verbose_low ("Registered counter " ^ name ^ ".");
		register my_new_counter
(*	)else(
		(* Print some information *)
		print_message Verbose_low ("Counter " ^ name ^ " NOT registered.");
	)*);
	
	(* Return counter *)
	my_new_counter*)

let create_time_counter_and_register (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	(* Create counter *)
	let my_new_counter = new timeCounter name counter_category level in
	
	(* Only register if verbose mode allows for it *)
	(*** NOTE: for now, register all counters (as the verbose_mode may not be initialized when the counters are created ***)
(* 	if !all_counters_enabled || verbose_mode_greater level then( *)
		(* Print some information *)
		print_message Verbose_low ("Registered counter " ^ name ^ ".");
		register my_new_counter
(*	)else(
		(* Print some information *)
		print_message Verbose_low ("Counter " ^ name ^ " NOT registered.");
	)*);
	
	(* Return counter *)
	my_new_counter


let create_discrete_counter_and_register (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	(* Create counter *)
	let my_new_counter = new discreteCounter name counter_category level in

	(* Register *)
	register my_new_counter;

	(* Print some information *)
	print_message Verbose_low ("Registered counter " ^ name ^ ".");
	
	(* Return counter *)
	my_new_counter


let create_hybrid_counter_and_register (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	(* Create counter *)
	let my_new_counter = new hybridCounter name counter_category level in

	(* Only register if verbose mode allows for it *)
	(*** NOTE: for now, register all counters (as the verbose_mode may not be initialized when the counters are created ***)
(* 	if !all_counters_enabled || verbose_mode_greater level then( *)
		(* Print some information *)
		print_message Verbose_low ("Registered counter " ^ name ^ ".");
		register my_new_counter
(*	)else(
		(* Print some information *)
		print_message Verbose_low ("Counter " ^ name ^ " NOT registered.");
	)*);
	
	(* Return counter *)
	my_new_counter


let create_data_recorder_and_register (name : string) (counter_category : counterCategory) (level : ImitatorUtilities.verbose_mode) =
	(* Create data_recorder *)
	let my_new_data_recorder = new data_recorder name counter_category level in

	(* Register *)
	register my_new_data_recorder;
	
	(* Print some information *)
	print_message Verbose_low ("Registered data recorder " ^ name ^ ".");
	
	(* Return *)
	my_new_data_recorder


(** Retrieve all counters of a category *)
(*** NOTE: not smart programming (we have to go through the entire list of counters once for each category) but, come on, there are relatively few counters and few categories… ***)
let get_counters_by_category counter_category =
	List.filter (fun counter -> counter#category = counter_category) !all_counters

(** Enable all counters (past and future), independently of their verbose level; typically, this function will be called if -statistics option is enabled *)
let enable_all_counters () =
	all_counters_enabled := true


(** Get all counters values with a pretty-printed string *)
let string_of_all_counters () =
	(* Try to get something nicely justified *) 
	let max_name_size = 40 in

	let result = ref "" in
	
	(* Iterate on categories *)
	List.iter (fun category -> 
		(* Retrieve counters *)
		let counters = get_counters_by_category category in
		
		(* Filter active counters for this level of verbosity *)
		let active_counters = if !all_counters_enabled then counters else List.filter (fun counter -> verbose_mode_greater counter#level) counters in
		
		(* Only print non-empty categories *)
		if List.length active_counters > 0 then(
			result := !result ^ "\n------------------------------------------------------------"
				^ "\n Statistics: " ^ (string_of_category category)
				^ "\n------------------------------------------------------------";
			(* Print all counters *)
			List.iter (fun counter ->
				(* Only print suitable counters *)
				if !all_counters_enabled || verbose_mode_greater counter#level then(
					let counter_name_length = String.length counter#name in
					let name = if counter_name_length <= max_name_size then
						(counter#name ^ (string_n_times (max_name_size - counter_name_length) " "))
					else
						counter#name
					in
					result := !result ^ "\n" ^ name ^ ": " ^ counter#string_of_value;
				);
			(*** NOTE: the list is reversed for a nicer printing since newer registered counters were added to the head ***)
			) (List.rev active_counters)
		) (* end if |counters| > 0 *)
	) all_categories;
	
	(* Return the string *)
	!result
