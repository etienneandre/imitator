(*****************************************************************
 *
 *                       IMITATOR
 * 
 * LIPN, Universite Paris 13, Sorbonne Paris Cite (France)
 * 
 * Author:        Etienne Andre
 * 
 * Created:       2015/03/24
 * Last modified: 2015/03/24
 *
 ****************************************************************)

open Exceptions
open AbstractModel
open CamlUtilities




(************************************************************
 Functions
************************************************************)

(** Escape strings for LaTeX names *)
let escape_latex str =
	Str.global_replace (Str.regexp "_") ("\\_") str


let variable_names_with_style variable_index =
	(* Get the model *)
	let model = Input.get_model() in
	let name = escape_latex (model.variable_names variable_index) in
	match model.type_of_variables variable_index with
	| Var_type_clock -> "\styleclock{" ^ name ^ "}"
	| Var_type_discrete -> "\styledisc{" ^ name ^ "}"
	| Var_type_parameter -> "\styleparam{" ^ name ^ "}"


(** Proper form for constraints *)
let tikz_string_of_lc_gen lc_fun lc =
	let lc_string = lc_fun variable_names_with_style lc in
	(* Do some replacements *)
	"& $" ^ Str.global_replace (Str.regexp ">=") ("\geq")
		(Str.global_replace (Str.regexp "&") ("$\\\\\n\t\t\\$land$ & $")
			(Str.global_replace (Str.regexp "a") ("a") lc_string)
		)
	^ "$"

(** Proper form for constraints *)
let tikz_string_of_linear_constraint =
	tikz_string_of_lc_gen LinearConstraint.string_of_pxd_linear_constraint



(* Create the array of dot colors *)
let dot_colors = Array.of_list Graphics.dot_colors

(* Coloring function for each thing *)
let color = fun index ->
	(* If more colors than our array: white *)
	try dot_colors.(index) with Invalid_argument _ -> "white"


let id_of_location automaton_index location_index =
	"s_" ^ (string_of_int automaton_index) ^ "_" ^ (string_of_int location_index)

let string_of_list_of_variables variable_names variables =
	let variables = List.map variable_names variables in
	string_of_list_of_string_with_sep "," variables

let escape_string_for_dot str =
	(** BUG: cannot work with global replace *)
(*		Str.global_substitute (Str.regexp ">\\|&") (fun s -> if s = ">" then "\\>" else if s = "&" then "\\&" else s)
			str*)
(* 		Str.global_replace (Str.regexp "\\(>\\|&\\)") ("\\" ^ "\\(\\1\\)") *)
	Str.global_replace (Str.regexp "\n") (" \\n ")
		(Str.global_replace (Str.regexp ">") ("\\>")
			(Str.global_replace (Str.regexp "&") ("\\&") str)
		)

	
	
	
(* Add a header to the model *)
let string_of_header model =
	(* Retrieve the input options *)
	let options = Input.get_options () in
	          "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	^ "\n" ^" % Model " ^ options#file
	^ "\n" ^" % Converted by " ^ Constants.program_name ^ " " ^ Constants.version_string
	^ "\n" ^" % Generated at time " ^ (now()) ^ ""
	^ "\n" ^" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	

(** Convert a sync into a string *)
let string_of_sync model action_index =
	match model.action_types action_index with
	| Action_type_sync -> "\n\t\t & $\styleact{" ^ (escape_latex (model.action_names action_index)) ^ "}$\\\\"
	| Action_type_nosync -> ""


let string_of_clock_updates model = function
	| No_update -> ""
	| Resets list_of_clocks -> 
		string_of_list_of_string_with_sep "\\n" (List.map (fun variable_index ->
			"\n\t\t & $"
			^ (variable_names_with_style variable_index)
			^ ":=0$\\\\"
		) list_of_clocks)
	| Updates list_of_clocks_lt -> 
		string_of_list_of_string_with_sep "\\n" (List.map (fun (variable_index, linear_term) ->
						"\n\t\t & $"
			^ (variable_names_with_style variable_index)
			^ ":="
			^ (LinearConstraint.string_of_pxd_linear_term variable_names_with_style linear_term)
			^ "$\\\\"
		) list_of_clocks_lt)

	
(* Convert a list of updates into a string *)
let string_of_updates model updates =
	string_of_list_of_string_with_sep "\\n" (List.map (fun (variable_index, linear_term) ->
		(* Convert the variable name *)
		(model.variable_names variable_index)
		^ ":="
		(* Convert the linear_term *)
		^ (LinearConstraint.string_of_pxd_linear_term model.variable_names linear_term)
	) updates)


(* Convert a transition of a location into a string *)
let string_of_transition model automaton_index source_location action_index (guard, clock_updates, discrete_updates, destination_location) =
	let source_location_name = model.location_names automaton_index source_location in
	let destination_location_name = model.location_names automaton_index destination_location in

	(*	\path (Q0) edge node{\begin{tabular}{c}
			\coulact{press?} \\
			$\coulclock{x} := 0$ \\
			$\coulclock{y} := 0$ \\
			\end{tabular}} (Q1);*)
	"\n\n\t\t\\path (" ^ source_location_name ^ ") edge node{\\begin{tabular}{c @{\\ } c}"
	
	(* GUARD *)
	^ (if not (LinearConstraint.pxd_is_true guard) then (
		"\n\t\t" ^ (tikz_string_of_linear_constraint guard) ^ "\\\\"
	) else "" )
	
	(* ACTION *)
	^ (string_of_sync model action_index)
	
	(* UPDATES *)
	(* Clock updates *)
	^ (string_of_clock_updates model clock_updates)
	(* Discrete updates *)
(* 	^ (string_of_updates model discrete_updates) *)
	
	(* The end *)
	^ "\n\t\t\end{tabular}} (" ^ destination_location_name ^ ");"
	
	
(*(* s_12 -> s_5 [label="bUp"]; *)
	"\n\t"
	(* Source *)
	^ (id_of_location automaton_index source_location)
	(* Destination *)
	^ " -> "
	^ (id_of_location automaton_index destination_location)
	
	^ " ["
	(* Color for sync label *)
	(* Check if the label is shared *)
	^ (if List.length (model.automata_per_action action_index) > 1 then
		let color = color action_index in
		"style=bold, color=" ^ color ^ ", "
		else "")
	(* LABEL *)
	^ "label=\""
	(* Guard *)
	^ (
		if not (LinearConstraint.pxd_is_true guard) then
			(escape_string_for_dot (LinearConstraint.string_of_pxd_linear_constraint model.variable_names guard)) ^ "\\n"
		else ""
		)
	(* Sync *)
	^ (string_of_sync model action_index)
	(* Clock updates *)
	^ (string_of_clock_updates model clock_updates)
	(* Add a \n in case of both clocks and discrete *)
	^ (if clock_updates != No_update && discrete_updates != [] then "\\n" else "")
	(* Discrete updates *)
	^ (string_of_updates model discrete_updates)
	^ "\"];"*)
	
	(* Convert the guard *)
(* 	^ (LinearConstraint.string_of_linear_constraint model.variable_names guard) *)
	(* Convert the updates *)
(* 	^ " do {" *)
(* 	^ (string_of_clock_updates model clock_updates) *)
	
	
(*	^ (string_of_updates model discrete_updates)
	^ "} "
	(* Convert the sync *)
	^ (string_of_sync model action_index)
	(* Convert the destination location *)
	^ " goto " ^ (model.location_names automaton_index destination_location)
	^ ";"*)


(* Convert the transitions of a location into a string *)
let string_of_transitions_per_location model automaton_index location_index =
	string_of_list_of_string (
	(* For each action *)
	List.map (fun action_index -> 
		(* Get the list of transitions *)
		let transitions = model.transitions automaton_index location_index action_index in
		(* Convert to string *)
		string_of_list_of_string (
			(* For each transition *)
			List.map (string_of_transition model automaton_index location_index action_index) transitions
			)
		) (model.actions_per_location automaton_index location_index)
	)


(* Convert the transitions of an automaton into a string *)
let string_of_transitions model automaton_index =
	string_of_list_of_string_with_sep "\n " (List.map (fun location_index ->
		string_of_transitions_per_location model automaton_index location_index
	) (model.locations_per_automaton automaton_index))


(* Convert a location of an automaton into a string *)
let string_of_location model automaton_index location_index =
	(* LOCATION *)
(* 	\node[location, fill=cpale2] (Q0) {\coulloc{l0}}; *)

	let location_name = model.location_names automaton_index location_index in
	let invariant = model.invariants automaton_index location_index in
	let color_id = ((location_index) mod LatexHeader.nb_colors) + 1 in
	
	(*** TODO: better positioning! (from dot?) ***)
	let pos_x = location_index in
	let pos_y = 0 in
	
	"\n\t\t\\node[location, fill=loccolor" ^ (string_of_int color_id) ^ "] at (" ^ (string_of_int pos_x) ^ "," ^ (string_of_int pos_y) ^ ") (" ^ location_name ^ ") {\styleloc{" ^ (escape_latex location_name) ^ "}};"
	
	(* INVARIANT *)
(*			% Invariant of location Q1
		\node [above] at (Q1.north) {
			\begin{tabular}{c @{\ } c}
				& $\coulclock{y} \leq \coulparam{p1}$\\
				$\land$ & $\coulclock{x} \geq 5 \couldisc{i}$\\
			\end{tabular}
		};*)
	
	^ (if (not (LinearConstraint.pxd_is_true invariant)) then (
		"\n\t\t% Invariant of location " ^ location_name
		^ "\n\t\t\\node [above] at (" ^ location_name ^ ".north) {\\begin{tabular}{c @{\\ } c}"
		^ (tikz_string_of_linear_constraint invariant)
		^ "\end{tabular}};"
	) else "" )

(*	
	
	^ "|{" ^ (escape_string_for_dot (LinearConstraint.string_of_pxd_linear_constraint model.variable_names (model.invariants automaton_index location_index)))
	(* Label: stopwatches *)
	^ (if model.has_stopwatches then (
		let stopwatches = model.stopwatches automaton_index location_index in
		"|" ^
		(if stopwatches != [] then "stop " ^ string_of_list_of_variables model.variable_names stopwatches else "")
	) else "") *)
	
(*	(* Transitions *)
	^ (string_of_transitions model automaton_index location_index)*)


(* Convert the locations of an automaton into a string *)
let string_of_locations model automaton_index =
	string_of_list_of_string_with_sep "\n " (List.map (fun location_index ->
		string_of_location model automaton_index location_index
	) (model.locations_per_automaton automaton_index))


(* Convert an automaton into a string *)
let string_of_automaton model automaton_index =
	(* Finding the initial location *)
(* 	let inital_global_location  = model.initial_location in *)
(* 	let initial_location = Automaton.get_location inital_global_location automaton_index in *)
	
	let automaton_name = escape_latex (model.automata_names automaton_index) in

	"\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	^ "\n% automaton " ^ automaton_name ^ ""
	^ "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	
	^ "\n\t\\begin{subfigure}[b]{\\ratio}"
	^ "\n\t\\begin{tikzpicture}[scale=2, auto, ->, >=stealth', thin]"
	
(*	TODO
	(* Handling the initial arrow *)
	^ "\n init" ^ (string_of_int automaton_index) ^ "[shape=none, label=\"" ^ (model.automata_names automaton_index) ^ "\"];"
	^ "\n init" ^ (string_of_int automaton_index) ^ " -> " ^ (id_of_location automaton_index initial_location) ^ ";"
	*)

	(* Handling locations *)
	^ "\n " ^ (string_of_locations model automaton_index)
	
	(* Handling transitions *)
	^ "\n " ^ (string_of_transitions model automaton_index)
	
	^ "\n\t\end{tikzpicture}"
	^ "\n\t\caption{PTA " ^ automaton_name ^ "}"
	^ "\n\t\label{pta:" ^ automaton_name ^ "}"
	^ "\n\t\end{subfigure}"


(* Convert the automata into a string *)
let string_of_automata model =
	(* Retrieve the input options *)
(*	let options = Input.get_options () in
	
	let vertical_string_of_list_of_variables variables =
		let variables = List.map model.variable_names variables in
		string_of_list_of_string_with_sep "\\n" variables
	in

	
	"\n/**************************************************/"
	^ "\n/* Starting general graph */"
	^ "\n/**************************************************/"
	^ "\n digraph G {\n"
	^ "\n node [shape=Mrecord, fontsize=12];"
(* 	^ "\n rankdir=LR" *)
	^ "\n"
	(* General information *)
(* 	s_0[fillcolor=red, style=filled, shape=Mrecord, label="s_0|{InputInit|And111|Or111}"]; *)
^ "\nname[shape=none, style=bold, fontsize=24, label=\"" ^ options#file ^ "\"];"
	^ "\ngeneral_info[shape=record, label=\"" (*Model|{*)
	^ "{Clocks|" ^ (vertical_string_of_list_of_variables model.clocks) ^ "}"
	^ "|{Parameters|" ^ (vertical_string_of_list_of_variables model.parameters) ^ "}"
	^ (if model.discrete != [] then
		"|{Discrete|" ^ (vertical_string_of_list_of_variables model.discrete) ^ "}"
		else "")
	^ "|{Initial|" ^ (escape_string_for_dot (LinearConstraint.string_of_px_linear_constraint model.variable_names model.initial_constraint)) ^ "}"
	^ "\"];" (*}*)
	(* To ensure that the name is above general info *)
	^ "\n name -> general_info [color=white];"
	^ "\ndate[shape=none, style=bold, fontsize=10, label=\"Generated: " ^ (now()) ^ "\"];"*)

	""
	^ (string_of_list_of_string_with_sep "\n\n" (
		List.map (fun automaton_index -> string_of_automaton model automaton_index
	) model.automata))


(* Convert the model into a string *)
let tikz_string_of_model model =
	let tikz_model =
	(* The small personnalized header *)
	string_of_header model
	(* The big LaTeX header *)
	^ LatexHeader.latex_header
(* 	^  "\n" ^ string_of_declarations model *)
	^  "\n" ^ string_of_automata model
	(* Footer *)
	^ "
\end{figure}

\end{document}
"
	in
	(* Replace escaped characters! *)
	(*String.escaped*) (*Scanf.unescaped *)
		tikz_model
(* 	Str.global_replace (Str.regexp_string "\\\n") "(ploufplouf)" tikz_model *)
(* 	Str.global_substitute (Str.regexp_string "command") (fun s -> print_string s; "(ploufplouf)") tikz_model *)
(* 	[^ \\t\\n] *)

