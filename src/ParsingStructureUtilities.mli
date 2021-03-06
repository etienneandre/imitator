(************************************************************
 *
 *                       IMITATOR
 *
 * Université de Lorraine, CNRS, Inria, LORIA, Nancy, France
 *
 * Module description: General fonctions for map, filter, traverse parsing structure tree
 *
 * File contributors : Benjamin L.
 * Created           : 2021/03/05
 * Last modified     : 2021/03/05
 *
 ************************************************************)

open ParsingStructure

(* Map the leafs of an arithmetic expression according to map_function *)
(* Leafs are Parsed_DF_variable, Parsed_DF_constant *)
(*val map_parsed_arithmetic_expression_leafs : (parsed_discrete_factor -> 'a) -> parsed_discrete_arithmetic_expression -> 'a list*)

(*val map_global_expression_leafs : (parsed_discrete_factor -> 'a) -> global_expression -> 'a list*)

(* Parsed expression to string *)
val string_of_parsed_global_expression : useful_parsing_model_information -> global_expression -> string
val string_of_parsed_boolean_expression : useful_parsing_model_information -> parsed_boolean_expression -> string
val string_of_parsed_discrete_boolean_expression : useful_parsing_model_information -> parsed_discrete_boolean_expression -> string
val string_of_parsed_arithmetic_expression : useful_parsing_model_information -> parsed_discrete_arithmetic_expression -> string
val string_of_parsed_term : useful_parsing_model_information -> parsed_discrete_term -> string
val string_of_parsed_factor : useful_parsing_model_information -> parsed_discrete_factor -> string
val string_of_parsed_relop : parsed_relop -> string -> string -> string

val string_of_parsed_nonlinear_constraint : useful_parsing_model_information -> nonlinear_constraint -> string

val try_reduce_parsed_global_expression : (variable_name, DiscreteValue.discrete_value) Hashtbl.t -> global_expression -> DiscreteValue.discrete_value
val try_reduce_parsed_global_expression_with_model : useful_parsing_model_information -> global_expression -> DiscreteValue.discrete_value

val try_reduce_parsed_term : (variable_name, DiscreteValue.discrete_value) Hashtbl.t -> parsed_discrete_term -> DiscreteValue.discrete_value
val try_reduce_parsed_factor : (variable_name, DiscreteValue.discrete_value) Hashtbl.t -> parsed_discrete_factor -> DiscreteValue.discrete_value