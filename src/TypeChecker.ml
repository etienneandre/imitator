(************************************************************
 *
 *                       IMITATOR
 *
 * Laboratoire Spécification et Vérification (ENS Cachan & CNRS, France)
 * Université Paris 13, LIPN, CNRS, France
 * Université de Lorraine, CNRS, Inria, LORIA, Nancy, France
 *
 * Module description: Contain all functions making type checking or type operations on a parsing structure
 *
 * File contributors : Benjamin L.
 * Created           : 2021/03/17
 * Last modified     : 2021/03/17
 *
 ************************************************************)

open ParsingStructure
open ParsingStructureUtilities
open ImitatorUtilities
open OCamlUtilities
open Exceptions

type variable_name = string
type variable_index = int

(** Error messages **)

(* Error message when mixin of different types *)
let get_type_mixin_error_message l_type r_type str_expr =
    "The expression \""
    ^ str_expr
    ^ "\" mix different types: "
    ^ (DiscreteValue.string_of_var_type_discrete l_type)
    ^ ", "
    ^ (DiscreteValue.string_of_var_type_discrete r_type)

(* Error message when mixin of different types *)
let get_triplet_type_mixin_error_message type1 type2 type3 str_expr =
    "The expression \""
    ^ str_expr
    ^ "\" mix different types: "
    ^ (DiscreteValue.string_of_var_type_discrete type1)
    ^ ", "
    ^ (DiscreteValue.string_of_var_type_discrete type2)
    ^ ", "
    ^ (DiscreteValue.string_of_var_type_discrete type3)

let get_infer_message str_expr target_type =
    print_message Verbose_high (
        "\tInfer literals of expression "
        ^ str_expr
        ^ " as "
        ^ DiscreteValue.string_of_var_type_discrete target_type
    )

(** Get variables types **)

(* Get var type of a variable given it's index *)
let get_type_of_variable variable_infos variable_index =
    variable_infos.type_of_variables variable_index

(* Get discrete type of a variable given it's index *)
let get_discrete_type_of_variable variable_infos variable_index =
    let var_type = get_type_of_variable variable_infos variable_index in
    DiscreteValue.discrete_type_of_var_type var_type

(* Get var type of a variable given it's name *)
let get_type_of_variable_by_name variable_infos variable_name =
    if Hashtbl.mem variable_infos.index_of_variables variable_name then (
        (* Get type of variable *)
        let variable_index = Hashtbl.find variable_infos.index_of_variables variable_name in
        let variable_type = get_type_of_variable variable_infos variable_index in
        variable_type
    ) else if Hashtbl.mem variable_infos.constants variable_name then (
        (* Retrieve the value of the global constant *)
        let value = Hashtbl.find variable_infos.constants variable_name in
        (* Get type of constant *)
        DiscreteValue.var_type_of_value value
    ) else
        raise (InternalError ("Impossible to find the index of variable `" ^ variable_name ^ "` although this should have been checked before."))


(* Get discrete type of a variable given it's name *)
let get_discrete_type_of_variable_by_name variable_infos variable_name =
    let var_type = get_type_of_variable_by_name variable_infos variable_name in
    DiscreteValue.discrete_type_of_var_type var_type

(** Conversions of expressions **)


(* Convert literals types of an expression to a given target type *)
let rec convert_literal_types_of_expression variable_infos target_type = function
    | Parsed_global_expression expr ->
        Parsed_global_expression (convert_literal_types_of_parsed_boolean_expression variable_infos target_type expr)

(* Convert literals types of a boolean expression to a given target type *)
and convert_literal_types_of_parsed_boolean_expression variable_infos target_type = function
    | Parsed_True -> Parsed_True
    | Parsed_False -> Parsed_False
    | Parsed_And (l_expr, r_expr) ->
        let convert_l_expr = convert_literal_types_of_parsed_boolean_expression variable_infos target_type l_expr in
        let convert_r_expr = convert_literal_types_of_parsed_boolean_expression variable_infos target_type r_expr in
        Parsed_And (convert_l_expr, convert_r_expr)
    | Parsed_Or (l_expr, r_expr) ->
        let convert_l_expr = convert_literal_types_of_parsed_boolean_expression variable_infos target_type l_expr in
        let convert_r_expr = convert_literal_types_of_parsed_boolean_expression variable_infos target_type r_expr in
        Parsed_Or (convert_l_expr, convert_r_expr)
    | Parsed_Discrete_boolean_expression expr ->
        Parsed_Discrete_boolean_expression (convert_literal_types_of_parsed_discrete_boolean_expression variable_infos target_type expr)

(* Convert literals types of a discrete boolean expression to a given target type *)
and convert_literal_types_of_parsed_discrete_boolean_expression variable_infos target_type = function
    | Parsed_arithmetic_expression expr ->
        Parsed_arithmetic_expression (convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr)
    | Parsed_boolean_expression expr ->
        Parsed_boolean_expression (convert_literal_types_of_parsed_boolean_expression variable_infos target_type expr)
    | Parsed_Not expr ->
        Parsed_Not (convert_literal_types_of_parsed_boolean_expression variable_infos target_type expr)
    | Parsed_expression (l_expr, relop, r_expr) ->
        let convert_l_expr = convert_literal_types_of_parsed_discrete_boolean_expression variable_infos target_type l_expr in
        let convert_r_expr = convert_literal_types_of_parsed_discrete_boolean_expression variable_infos target_type r_expr in
        Parsed_expression (convert_l_expr, relop, convert_r_expr)
    | Parsed_expression_in (expr, lower_expr, upper_expr) ->
        let convert_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr in
        let convert_lower = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type lower_expr in
        let convert_upper = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type upper_expr  in
        Parsed_expression_in (convert_expr, convert_lower, convert_upper)

(* Convert literals types of an arithmetic expression to a given target type *)
and convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type = function
    | Parsed_DAE_plus (expr, term) ->
        let convert_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr in
        let convert_term = convert_literal_types_of_parsed_discrete_term variable_infos target_type term in
        Parsed_DAE_plus (convert_expr, convert_term)
    | Parsed_DAE_minus (expr, term) ->
        let convert_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr in
        let convert_term = convert_literal_types_of_parsed_discrete_term variable_infos target_type term in
        Parsed_DAE_minus (convert_expr, convert_term)
    | Parsed_DAE_term term ->
        Parsed_DAE_term (convert_literal_types_of_parsed_discrete_term variable_infos target_type term)

(* Convert literals types of a term to a given target type *)
and convert_literal_types_of_parsed_discrete_term variable_infos target_type = function
    | Parsed_DT_mul (term, factor) ->
        let convert_term = convert_literal_types_of_parsed_discrete_term variable_infos target_type term in
        let convert_factor = convert_literal_types_of_parsed_discrete_factor variable_infos target_type factor in
        Parsed_DT_mul (convert_term, convert_factor)
    | Parsed_DT_div (term, factor) ->
        let convert_term = convert_literal_types_of_parsed_discrete_term variable_infos target_type term in
        let convert_factor = convert_literal_types_of_parsed_discrete_factor variable_infos target_type factor in
        Parsed_DT_div (convert_term, convert_factor)
    | Parsed_DT_factor factor ->
        Parsed_DT_factor (convert_literal_types_of_parsed_discrete_factor variable_infos target_type factor)

(* Convert literals types of a factor to a given target type *)
and convert_literal_types_of_parsed_discrete_factor variable_infos target_type = function
    | Parsed_DF_variable _ as variable -> variable
    | Parsed_DF_constant var_value as constant ->
        let discrete_type = DiscreteValue.discrete_type_of_value var_value in
        (* TODO benjamin quick fix because it seems that certain converted value are re-converted by top expression *)
        (* for example a * pow(a, 2) with a rational, reconvert 2 to rational, it's bad, check if there is another way to avoid it ! *)
        if DiscreteValue.is_discrete_type_unknown_number_type discrete_type then (
            print_message Verbose_high ("\tInfer literal number value " ^ (DiscreteValue.string_of_value var_value) ^ " as " ^ (DiscreteValue.string_of_var_type_discrete target_type));
            Parsed_DF_constant (DiscreteValue.convert_value_to_discrete_type var_value target_type)
        ) else
            constant
    | Parsed_DF_expression expr ->
        Parsed_DF_expression (convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr)
    | Parsed_rational_of_int_function expr ->
        (* As it was already type checked, we can convert inner expression literal numbers of the function to int *)
        let inner_target_type = DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_int in
        Parsed_rational_of_int_function (convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos inner_target_type expr)
    | Parsed_pow_function (expr, exp_expr) ->
        Parsed_pow_function (
            convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr,
            convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type exp_expr
        )
    | Parsed_shift_left (factor, expr) ->
        Parsed_shift_left (
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type factor,
            convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr
        )
    | Parsed_shift_right (factor, expr) ->
        Parsed_shift_right (
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type factor,
            convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr
        )
    | Parsed_fill_left (factor, expr) ->
        Parsed_fill_left (
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type factor,
            convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr
        )
    | Parsed_fill_right (factor, expr) ->
        Parsed_fill_right (
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type factor,
            convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr
        )
    | Parsed_log_and (l_factor, r_factor) ->
        Parsed_log_and (
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type l_factor,
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type r_factor
        )
    | Parsed_log_or (l_factor, r_factor) ->
        Parsed_log_or (
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type l_factor,
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type r_factor
        )
    | Parsed_log_xor (l_factor, r_factor) ->
        Parsed_log_xor (
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type l_factor,
            convert_literal_types_of_parsed_discrete_factor variable_infos target_type r_factor
        )
    | Parsed_log_not factor ->
        Parsed_log_not
            (convert_literal_types_of_parsed_discrete_factor variable_infos target_type factor)

    | Parsed_DF_unary_min factor ->
        Parsed_DF_unary_min (convert_literal_types_of_parsed_discrete_factor variable_infos target_type factor)

(* Convert literals types of a non-linear constraint to a given target type *)
let convert_literal_types_of_nonlinear_constraint variable_infos target_type = function
    (* It's ok non-linear constraint is of boolean type *)
    | Parsed_true_nonlinear_constraint -> Parsed_true_nonlinear_constraint
    | Parsed_false_nonlinear_constraint -> Parsed_false_nonlinear_constraint
    | Parsed_nonlinear_constraint expr ->
        Parsed_nonlinear_constraint (convert_literal_types_of_parsed_discrete_boolean_expression variable_infos target_type expr)

(** Type checking and inference **)

(* Type checking error types that can arise on arithmetic expression *)
type arithmetic_expression_type_error =
    | Not_arithmetic_error
    | Mixin_type_error
    | Both_unknown_number_error
    | Left_unknown_number_error
    | Right_unknown_number_error

(* Check arithmetic expression types and return convenient error type *)
let check_arithmetic_expression l_type r_type =
    if not (DiscreteValue.is_discrete_type_number_type l_type && DiscreteValue.is_discrete_type_number_type r_type) then
        Not_arithmetic_error
    else if DiscreteValue.is_discrete_type_known_number_type l_type && DiscreteValue.is_discrete_type_known_number_type r_type && l_type <> r_type then
        Mixin_type_error
    else if DiscreteValue.is_discrete_type_unknown_number_type l_type && DiscreteValue.is_discrete_type_unknown_number_type r_type then
        Both_unknown_number_error
    else if DiscreteValue.is_discrete_type_unknown_number_type l_type then
        Left_unknown_number_error
    else
        Right_unknown_number_error


let checkus
    variable_infos
    l_expr
    r_expr
    expr
    infer_l_fun
    infer_r_fun
    convert_l_fun
    convert_r_fun
    string_fun
    =

    let infer_l_expr, l_type = infer_l_fun variable_infos l_expr in
    let infer_r_expr, r_type = infer_r_fun variable_infos r_expr in

    let error_type = check_arithmetic_expression l_type r_type in
    match error_type with
    | Not_arithmetic_error ->
        raise (TypeError (
            "The expression \""
            ^ (string_fun variable_infos expr)
            ^ "\" is not an arithmetic expression: "
            ^ (DiscreteValue.string_of_var_type_discrete l_type)
            ^ ", "
            ^ (DiscreteValue.string_of_var_type_discrete r_type)
        ))
    | Mixin_type_error ->
        raise (TypeError (get_type_mixin_error_message l_type r_type (string_fun variable_infos expr)))
    | Both_unknown_number_error ->
        (infer_l_expr, infer_r_expr), DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_unknown_number
    | Left_unknown_number_error ->
        (* Convert *)
        let convert_l_expr = convert_l_fun variable_infos r_type infer_l_expr in
        (convert_l_expr, infer_r_expr), r_type
    | Right_unknown_number_error ->
        (* Convert *)
        let convert_r_expr = convert_r_fun variable_infos l_type infer_r_expr in
        (infer_l_expr, convert_r_expr), l_type


(* Type check and infer literal numbers of global expression *)
let rec infer_expression variable_infos = function
    | Parsed_global_expression expr ->
        let convert_expr, discrete_type = infer_parsed_boolean_expression variable_infos expr in
        Parsed_global_expression convert_expr, discrete_type

(* Type check and infer literal numbers of boolean expression *)
and infer_parsed_boolean_expression variable_infos = function

    | Parsed_True -> Parsed_True, DiscreteValue.Var_type_discrete_bool
    | Parsed_False -> Parsed_False, DiscreteValue.Var_type_discrete_bool

    | Parsed_And (l_expr, r_expr) as expr ->
        let (convert_l_expr, convert_r_expr), discrete_type = check_and_convert_boolean_expression variable_infos l_expr r_expr expr in
        Parsed_And (convert_l_expr, convert_r_expr), discrete_type

    | Parsed_Or (l_expr, r_expr) as expr ->
        let (convert_l_expr, convert_r_expr), discrete_type = check_and_convert_boolean_expression variable_infos l_expr r_expr expr in
        Parsed_Or (convert_l_expr, convert_r_expr), discrete_type

    | Parsed_Discrete_boolean_expression expr ->
        let infer_expr, discrete_type = infer_parsed_discrete_boolean_expression variable_infos expr in
        Parsed_Discrete_boolean_expression infer_expr, discrete_type

and check_and_convert_boolean_expression variable_infos l_expr r_expr expr =
        let infer_l_expr, l_type = infer_parsed_boolean_expression variable_infos l_expr in
        let infer_r_expr, r_type = infer_parsed_boolean_expression variable_infos r_expr in

        (* Check if two types are bool *)
        if not (DiscreteValue.is_discrete_type_bool_type l_type && DiscreteValue.is_discrete_type_bool_type r_type) then
            raise (TypeError (
                "The expression \""
                ^ (string_of_parsed_boolean_expression variable_infos expr)
                ^ "\" is not of type bool: "
                ^ (DiscreteValue.string_of_var_type_discrete l_type)
                ^ ", "
                ^ (DiscreteValue.string_of_var_type_discrete r_type)
            ))
        else
            (infer_l_expr, infer_r_expr), DiscreteValue.Var_type_discrete_bool

(* Type checking and infer literal numbers of discrete boolean expression *)
and infer_parsed_discrete_boolean_expression variable_infos = function
    | Parsed_arithmetic_expression expr ->
        let infer_expr, discrete_type = infer_parsed_discrete_arithmetic_expression variable_infos expr in
        Parsed_arithmetic_expression (infer_expr), discrete_type

    | Parsed_boolean_expression expr ->
        let infer_expr, discrete_type = infer_parsed_boolean_expression variable_infos expr in
        Parsed_boolean_expression (infer_expr), discrete_type

    | Parsed_Not expr as not_expr ->
        let infer_expr, discrete_type = infer_parsed_boolean_expression variable_infos expr in

        (* Check if 'not' contains a bool expression *)
        if not (DiscreteValue.is_discrete_type_bool_type discrete_type) then
            raise (TypeError (
                "The expression \""
                ^ string_of_parsed_boolean_expression variable_infos expr
                ^ "\" contained in \""
                ^ string_of_parsed_discrete_boolean_expression variable_infos not_expr
                ^ "\" expression, is not of type bool: "
                ^ DiscreteValue.string_of_var_type_discrete discrete_type
            ))
        else
            Parsed_Not (infer_expr), discrete_type

    | Parsed_expression (l_expr, relop, r_expr) as expr ->

        (* Infer left / right expressions *)
        let infer_l_expr, l_type = infer_parsed_discrete_boolean_expression variable_infos l_expr in
        let infer_r_expr, r_type = infer_parsed_discrete_boolean_expression variable_infos r_expr in

        (* Prepare inference message *)
        let get_infer_expr_message = get_infer_message (string_of_parsed_discrete_boolean_expression variable_infos expr) in

        print_message Verbose_high (
            "\tInfer expression type of \""
            ^ string_of_parsed_discrete_boolean_expression variable_infos expr
            ^ "\" as "
            ^ DiscreteValue.string_of_var_type_discrete DiscreteValue.Var_type_discrete_bool
        );

        (* Check if two types are compatibles : bool, bool or int, int or number, int; etc. *)
        if not (DiscreteValue.is_discrete_type_compatibles l_type r_type) then
            raise (TypeError (get_type_mixin_error_message l_type r_type (string_of_parsed_discrete_boolean_expression variable_infos expr)))
        (* Check if two types are unknown number *)
        else if (DiscreteValue.is_discrete_type_unknown_number_type l_type && DiscreteValue.is_discrete_type_unknown_number_type r_type) then (
            (* No number type are deduced from tree, because there is only literal numbers *)
            (* So at this point, we convert all literals to rationals *)
            let target_type = DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_rational in
            get_infer_expr_message target_type;

            (* Convert left / right expression to rational *)
            let convert_l_expr = convert_literal_types_of_parsed_discrete_boolean_expression variable_infos target_type infer_l_expr in
            let convert_r_expr = convert_literal_types_of_parsed_discrete_boolean_expression variable_infos target_type infer_r_expr in

            Parsed_expression (convert_l_expr, relop, convert_r_expr), DiscreteValue.Var_type_discrete_bool
        )
        (* Check if only left type is unknown number *)
        else if (DiscreteValue.is_discrete_type_unknown_number_type l_type) then (

            get_infer_expr_message r_type;

            (* Convert left expression to right expression type *)
            let convert_l_expr = convert_literal_types_of_parsed_discrete_boolean_expression variable_infos r_type infer_l_expr in
            Parsed_expression (convert_l_expr, relop, infer_r_expr), DiscreteValue.Var_type_discrete_bool
        )
        (* Check if only right type is unknown number *)
        else if (DiscreteValue.is_discrete_type_unknown_number_type r_type) then (

            get_infer_expr_message l_type;

            (* Convert right expression to left expression type *)
            let convert_r_expr = convert_literal_types_of_parsed_discrete_boolean_expression variable_infos l_type infer_r_expr in
            Parsed_expression (infer_l_expr, relop, convert_r_expr), DiscreteValue.Var_type_discrete_bool
        )
        (* Here left and right types are compatible and not literals unknown number type, so just return *)
        else (
            Parsed_expression (infer_l_expr, relop, infer_r_expr), DiscreteValue.Var_type_discrete_bool
        )

    | Parsed_expression_in (expr, lower_expr, upper_expr) as in_expr ->

        let infer_expr, expr_type = infer_parsed_discrete_arithmetic_expression variable_infos expr in
        let infer_lower_expr, lower_type = infer_parsed_discrete_arithmetic_expression variable_infos lower_expr in
        let infer_upper_expr, upper_type = infer_parsed_discrete_arithmetic_expression variable_infos upper_expr in

        (* Prepare checkings for readability *)
        let all_types = [expr_type; lower_type; upper_type] in
        let types_combination = list_combination all_types all_types in

        let is_all_number = lazy (List.for_all (fun t -> DiscreteValue.is_discrete_type_number_type t) all_types) in
        let is_all_unknown_number = lazy (List.for_all (fun t -> DiscreteValue.is_discrete_type_unknown_number_type t) all_types) in
        let is_type_conflict = lazy (List.exists (fun (t1, t2) -> not (DiscreteValue.is_discrete_type_unknown_number_type t1 || DiscreteValue.is_discrete_type_unknown_number_type t2) && t1 <> t2) types_combination) in

        if not (Lazy.force is_all_number) then
            raise (TypeError (
                "One term of \""
                ^ string_of_parsed_discrete_boolean_expression variable_infos in_expr
                ^ "\" expression, is not an arithmetic expression: "
                ^ DiscreteValue.string_of_var_type_discrete expr_type
                ^ ", "
                ^ DiscreteValue.string_of_var_type_discrete lower_type
                ^ ", "
                ^ DiscreteValue.string_of_var_type_discrete upper_type
            )) (* One of theses are not a number *)

        else if Lazy.force is_type_conflict then
            raise (TypeError (
                "The expression \""
                ^ string_of_parsed_discrete_boolean_expression variable_infos in_expr
                ^ "\" mix different types: "
                ^ (DiscreteValue.string_of_var_type_discrete expr_type)
                ^ ", "
                ^ (DiscreteValue.string_of_var_type_discrete lower_type)
                ^ ", "
                ^ (DiscreteValue.string_of_var_type_discrete upper_type)
            )) (* Types are differents *)

        (* All are unknown numbers *)
        else if (Lazy.force is_all_unknown_number) then (
            (* No number type are deduced from tree, because there is only literal numbers *)
            (* So at this point, we convert all literals to rationals *)
            let target_type = DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_rational in

            print_message Verbose_high (
                "\tInfer literals of expression \"" ^
                string_of_parsed_discrete_boolean_expression variable_infos in_expr ^
                "\" as " ^
                DiscreteValue.string_of_var_type_discrete target_type
            );

            let convert_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type infer_expr in
            let convert_lower_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type infer_lower_expr in
            let convert_upper_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type infer_upper_expr in

            Parsed_expression_in (convert_expr, convert_lower_expr, convert_upper_expr), DiscreteValue.Var_type_discrete_bool
        )
        else if not (DiscreteValue.is_discrete_type_unknown_number_type expr_type) then (

            print_message Verbose_high (
                "\tInfer literals of expression \"" ^
                string_of_parsed_discrete_boolean_expression variable_infos in_expr ^
                "\" as " ^
                DiscreteValue.string_of_var_type_discrete expr_type
            );

            (* Convert lower and upper expression to expr_type *)
            let convert_lower_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos expr_type infer_lower_expr in
            let convert_upper_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos expr_type infer_upper_expr in

            Parsed_expression_in (infer_expr, convert_lower_expr, convert_upper_expr), DiscreteValue.Var_type_discrete_bool
        )
        else if not (DiscreteValue.is_discrete_type_unknown_number_type lower_type) then (

            print_message Verbose_high (
                "\tInfer literals of expression \"" ^
                string_of_parsed_discrete_boolean_expression variable_infos in_expr ^
                "\" as " ^
                DiscreteValue.string_of_var_type_discrete lower_type
            );

            (* Convert expr and upper expression to lower_type *)
            let convert_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos lower_type infer_expr in
            let convert_upper_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos lower_type infer_upper_expr in

            Parsed_expression_in (convert_expr, infer_lower_expr, convert_upper_expr), DiscreteValue.Var_type_discrete_bool
        )
        else (

            print_message Verbose_high (
                "\tInfer literals of expression \"" ^
                string_of_parsed_discrete_boolean_expression variable_infos in_expr ^
                "\" as " ^
                DiscreteValue.string_of_var_type_discrete upper_type
            );

            (* Convert expr and lower expression to upper_type *)
            let convert_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos upper_type infer_expr in
            let convert_lower_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos upper_type infer_lower_expr in

            Parsed_expression_in (convert_expr, convert_lower_expr, infer_upper_expr), DiscreteValue.Var_type_discrete_bool
        )


(* Type checking and infer literal numbers of arithmetic expression *)
and infer_parsed_discrete_arithmetic_expression variable_infos =

    let rec inner_infer_parsed_discrete_arithmetic_expression = function
        | Parsed_DAE_plus (expr, term) as arithmetic_expr ->
            let (convert_l_expr, convert_r_expr), discrete_type = checkus
                variable_infos
                expr
                term
                arithmetic_expr
                infer_parsed_discrete_arithmetic_expression
                infer_parsed_discrete_term
                convert_literal_types_of_parsed_discrete_arithmetic_expression
                convert_literal_types_of_parsed_discrete_term
                string_of_parsed_arithmetic_expression
            in
(*            let (convert_l_expr, convert_r_expr), discrete_type = check_and_convert_arithmetic_expression variable_infos expr term arithmetic_expr in*)
            Parsed_DAE_plus (convert_l_expr, convert_r_expr), discrete_type

        | Parsed_DAE_minus (expr, term) as arithmetic_expr ->
            let (convert_l_expr, convert_r_expr), discrete_type = check_and_convert_arithmetic_expression variable_infos expr term arithmetic_expr in
            Parsed_DAE_minus (convert_l_expr, convert_r_expr), discrete_type

        | Parsed_DAE_term term ->
            let infer_term, discrete_type = infer_parsed_discrete_term variable_infos term in
            Parsed_DAE_term infer_term, discrete_type

    and check_and_convert_arithmetic_expression variable_infos expr term arithmetic_expr =
            let infer_expr, l_type = infer_parsed_discrete_arithmetic_expression variable_infos expr in
            let infer_term, r_type = infer_parsed_discrete_term variable_infos term in

            let error_type = check_arithmetic_expression l_type r_type in
            match error_type with
            | Not_arithmetic_error ->
                raise (TypeError (
                    "The expression \""
                    ^ (string_of_parsed_arithmetic_expression variable_infos arithmetic_expr)
                    ^ "\" is not an arithmetic expression: "
                    ^ (DiscreteValue.string_of_var_type_discrete l_type)
                    ^ ", "
                    ^ (DiscreteValue.string_of_var_type_discrete r_type)
                ))
            | Mixin_type_error ->
                raise (TypeError (get_type_mixin_error_message l_type r_type (string_of_parsed_arithmetic_expression variable_infos arithmetic_expr)))
            | Both_unknown_number_error ->
                (infer_expr, infer_term), DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_unknown_number
            | Left_unknown_number_error ->
                (* Convert *)
                let convert_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos r_type infer_expr in
                (convert_expr, infer_term), r_type
            | Right_unknown_number_error ->
                (* Convert *)
                let convert_term = convert_literal_types_of_parsed_discrete_term variable_infos l_type infer_term in
                (infer_expr, convert_term), l_type

    in
    inner_infer_parsed_discrete_arithmetic_expression

(* Type checking and infer literal numbers of term *)
and infer_parsed_discrete_term variable_infos = function
    | Parsed_DT_mul (term, factor) as expr_term ->
(*        let (convert_l_expr, convert_r_expr), discrete_type = check_and_convert_term variable_infos term factor expr_term in*)

        let (convert_l_expr, convert_r_expr), discrete_type = checkus
            variable_infos
            term
            factor
            expr_term
            infer_parsed_discrete_term
            infer_parsed_discrete_factor
            convert_literal_types_of_parsed_discrete_term
            convert_literal_types_of_parsed_discrete_factor
            string_of_parsed_term
        in

        Parsed_DT_mul (convert_l_expr, convert_r_expr), discrete_type

    | Parsed_DT_div (term, factor) as expr_term ->
        let (convert_l_expr, convert_r_expr), discrete_type = check_and_convert_term variable_infos term factor expr_term in
        Parsed_DT_div (convert_l_expr, convert_r_expr), discrete_type

    | Parsed_DT_factor factor ->
        let infer_factor, factor_type = infer_parsed_discrete_factor variable_infos factor in
        Parsed_DT_factor infer_factor, factor_type



and check_and_convert_term variable_infos term factor expr_term =
        let infer_term, l_type = infer_parsed_discrete_term variable_infos term in
        let infer_factor, r_type = infer_parsed_discrete_factor variable_infos factor in

        let error_type = check_arithmetic_expression l_type r_type in
        match error_type with
        | Not_arithmetic_error ->
            raise (TypeError (
                "The term \""
                ^ (string_of_parsed_term variable_infos expr_term)
                ^ "\" is not an arithmetic expression: "
                ^ (DiscreteValue.string_of_var_type_discrete l_type)
                ^ ", "
                ^ (DiscreteValue.string_of_var_type_discrete r_type)
            ))
        | Mixin_type_error ->
            raise (TypeError (get_type_mixin_error_message l_type r_type (string_of_parsed_term variable_infos expr_term)))
        | Both_unknown_number_error ->
            (infer_term, infer_factor), DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_unknown_number
        | Left_unknown_number_error ->
            (* Convert *)
            let convert_term = convert_literal_types_of_parsed_discrete_term variable_infos r_type infer_term in
            (convert_term, infer_factor), r_type
        | Right_unknown_number_error ->
            (* Convert *)
            let convert_factor = convert_literal_types_of_parsed_discrete_factor variable_infos l_type infer_factor in
            (infer_term, convert_factor), l_type

(* Type checking and infer literal numbers of factor *)
and infer_parsed_discrete_factor variable_infos = function
    | Parsed_DF_variable variable_name ->
        (* Get discrete type of variable *)
        let discrete_type = get_discrete_type_of_variable_by_name variable_infos variable_name in
        Parsed_DF_variable variable_name, discrete_type

    | Parsed_DF_constant var_value ->
        let discrete_type = DiscreteValue.discrete_type_of_value var_value in
        Parsed_DF_constant var_value, discrete_type

    | Parsed_DF_expression expr ->
        let infer_expr, expr_type = infer_parsed_discrete_arithmetic_expression variable_infos expr in
        Parsed_DF_expression infer_expr, expr_type

    | Parsed_rational_of_int_function expr as int_expr ->
        let infer_expr, expr_type = infer_parsed_discrete_arithmetic_expression variable_infos expr in

        (* Check that expr type is a int type *)
        if not (DiscreteValue.is_discrete_type_int_type expr_type || DiscreteValue.is_discrete_type_unknown_number_type expr_type) then
            raise (TypeError (
                "The expression \""
                ^ string_of_parsed_arithmetic_expression variable_infos expr
                ^ "\" contained in \""
                ^ string_of_parsed_factor variable_infos int_expr
                ^ "\" expression, is not of type int: "
                ^ DiscreteValue.string_of_var_type_discrete expr_type
            ))
        else (
            (* Set target type to int *)
            let target_type = DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_int in

            print_message Verbose_high (
                "\tInfer expression type of \""
                ^ string_of_parsed_factor variable_infos int_expr
                ^ "\" as "
                ^ DiscreteValue.string_of_var_type_discrete (DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_rational)
            );

            print_message Verbose_high (
                "\tInfer literals of expression \"" ^
                string_of_parsed_factor variable_infos int_expr ^
                "\" as " ^
                DiscreteValue.string_of_var_type_discrete target_type
            );

            (* Convert all literal of the expression to int *)
            let convert_expr = convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr in

            (* Return converted expression and it's type *)
            Parsed_rational_of_int_function convert_expr, DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_rational
        )

    | Parsed_pow_function (expr, exp) as pow_expr ->
        let infer_expr, l_type = infer_parsed_discrete_arithmetic_expression variable_infos expr in
        let infer_exp, r_type = infer_parsed_discrete_arithmetic_expression variable_infos exp in

        (* Check that two expression are arithmetic *)
        if not (DiscreteValue.is_discrete_type_number_type l_type && DiscreteValue.is_discrete_type_number_type r_type) then (
            raise (TypeError (
                "The left or right expression contained \""
                ^ (string_of_parsed_factor variable_infos pow_expr)
                ^ "\" is not an arithmetic expression: "
                ^ (DiscreteValue.string_of_var_type_discrete l_type)
                ^ ", "
                ^ (DiscreteValue.string_of_var_type_discrete r_type)
            ));
        )
        (* Check that right expression (exponent) is int, otherwise raise an error *)
        else if not (DiscreteValue.is_discrete_type_unknown_number_type r_type || DiscreteValue.is_discrete_type_int_type r_type) then (
            raise (TypeError (
                    "Exponent of expression \""
                    ^ ParsingStructureUtilities.string_of_parsed_factor variable_infos pow_expr
                    ^ "\" is not an integer"
                )
            );
        );

        (* If right expression unknown convert auto to int *)
        let converted_exp = if DiscreteValue.is_discrete_type_unknown_number_type r_type then (
            (* convert *)
            let target_type = DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_int in
            convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type exp
        ) else
            infer_exp
        in
        (* If left expression unknown convert auto to rational *)
        (* Moreover result type depend on the type of left expression: *)
        (* it has the same number type as left expression type *)
        let converted_expr, result_type = if DiscreteValue.is_discrete_type_unknown_number_type l_type then (
            (* convert *)
            let target_type = DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_rational in
            convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr, target_type
        ) else
            infer_expr, l_type
        in

        print_message Verbose_high (
            "\tInfer expression type of \""
            ^ (string_of_parsed_factor variable_infos pow_expr)
            ^ "\" as "
            ^ (DiscreteValue.string_of_var_type_discrete result_type)
        );

        (* Return converted expression and it's type *)
        Parsed_pow_function (converted_expr, converted_exp), result_type

    | Parsed_shift_left (factor, expr)
    | Parsed_shift_right (factor, expr)
    | Parsed_fill_left (factor, expr)
    | Parsed_fill_right (factor, expr) as shift ->

        let infer_factor, l_type = infer_parsed_discrete_factor variable_infos factor in
        let infer_expr, r_type = infer_parsed_discrete_arithmetic_expression variable_infos expr in

        (* factor should be binary word *)
        if not (DiscreteValue.is_discrete_type_binary_word_type l_type) then (
            raise (TypeError (
                "Left member of expression \""
                ^ ParsingStructureUtilities.string_of_parsed_factor variable_infos shift
                ^ "\" is not a binary word"
            ))
        );

        (* expr should be int *)
        if not (DiscreteValue.is_discrete_type_unknown_number_type r_type || DiscreteValue.is_discrete_type_int_type r_type) then (
            raise (TypeError (
                "Right member of expression \""
                ^ ParsingStructureUtilities.string_of_parsed_factor variable_infos shift
                ^ "\" is not an int expression"
            ))
        );

        (* If right expression unknown convert auto to int *)
        let converted_expr = if DiscreteValue.is_discrete_type_unknown_number_type r_type then (
            (* convert *)
            let target_type = DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_int in

            print_message Verbose_high (
                "\tInfer expression \""
                ^ (string_of_parsed_arithmetic_expression variable_infos expr)
                ^ "\" as "
                ^ (DiscreteValue.string_of_var_type_discrete target_type)
            );

            convert_literal_types_of_parsed_discrete_arithmetic_expression variable_infos target_type expr
        ) else
            infer_expr
        in



        let typed_shift =
        (match shift with
        | Parsed_shift_left _ ->
            Parsed_shift_left (infer_factor, converted_expr), l_type
        | Parsed_shift_right _ ->
            Parsed_shift_right (infer_factor, converted_expr), l_type
        (* TODO benjamin REFACTOR ugly copy / paste *)
        | Parsed_fill_left _ ->
            (* As we have to deduce length of binary word according to it's shifting value, *)
            (* only constant expression can be use as value of shifting *)

            if not (ParsingStructureUtilities.is_parsed_arithmetic_expression_constant variable_infos converted_expr) then
                raise (TypeError (
                    "Shift parameter of "
                    ^ string_of_parsed_factor_constructor shift
                    ^ " function should be a constant expression."
                    ^ " Expression \""
                    ^ ParsingStructureUtilities.string_of_parsed_arithmetic_expression variable_infos converted_expr
                    ^ "\" is not constant."
                ));

            let shift_value = ParsingStructureUtilities.try_reduce_parsed_arithmetic_expression variable_infos.constants converted_expr in
            let base_length = (match l_type with DiscreteValue.Var_type_discrete_binary_word l -> l | _ -> raise (InternalError "never happen")) in
            let length = base_length + Int32.to_int (DiscreteValue.int_value shift_value) in
            Parsed_fill_left (infer_factor, converted_expr), DiscreteValue.Var_type_discrete_binary_word length
        | Parsed_fill_right _ ->
            (* As we have to deduce length of binary word according to it's shifting value, *)
            (* only constant expression can be use as value of shifting *)

            if not (ParsingStructureUtilities.is_parsed_arithmetic_expression_constant variable_infos converted_expr) then
                raise (TypeError (
                    "Shift parameter of "
                    ^ string_of_parsed_factor_constructor shift
                    ^ " should be a constant expression."
                    ^ " Expression \""
                    ^ ParsingStructureUtilities.string_of_parsed_arithmetic_expression variable_infos converted_expr
                    ^ "\" is not constant."
                ));

            let shift_value = ParsingStructureUtilities.try_reduce_parsed_arithmetic_expression variable_infos.constants converted_expr in
            let base_length = (match l_type with DiscreteValue.Var_type_discrete_binary_word l -> l | _ -> raise (InternalError "never happen")) in
            let length = base_length + Int32.to_int (DiscreteValue.int_value shift_value) in
            Parsed_fill_right (infer_factor, converted_expr), DiscreteValue.Var_type_discrete_binary_word length
        | _ ->
            raise (InternalError "Never happen !")
        )
        in

        let _, t = typed_shift in
        print_message Verbose_high (
            "\tInfer expression \""
            ^ (string_of_parsed_factor variable_infos shift)
            ^ "\" as "
            ^ (DiscreteValue.string_of_var_type_discrete t)
        );

        typed_shift

    | Parsed_log_and (l_factor, r_factor)
    | Parsed_log_or (l_factor, r_factor)
    | Parsed_log_xor (l_factor, r_factor) as log_op ->

        let infer_l_factor, l_type = infer_parsed_discrete_factor variable_infos l_factor in
        let infer_r_factor, r_type = infer_parsed_discrete_factor variable_infos r_factor in

        (* factors should be binary words of the same length *)
        if not (DiscreteValue.is_discrete_type_binary_word_type l_type && DiscreteValue.is_discrete_type_binary_word_type r_type) then (
            raise (TypeError (
                "Left or right member of expression \""
                ^ ParsingStructureUtilities.string_of_parsed_factor variable_infos log_op
                ^ "\" is not a binary word: "
                ^ DiscreteValue.string_of_var_type_discrete l_type
                ^ ", "
                ^ DiscreteValue.string_of_var_type_discrete r_type
            ))
        );

        if l_type <> r_type then (
            raise (TypeError (
                "Expression \""
                ^ ParsingStructureUtilities.string_of_parsed_factor variable_infos log_op
                ^ "\" mix different types: "
                ^ DiscreteValue.string_of_var_type_discrete l_type
                ^ ", "
                ^ DiscreteValue.string_of_var_type_discrete r_type
            ))
        );

        print_message Verbose_high (
            "\tInfer expression \""
            ^ (string_of_parsed_factor variable_infos log_op)
            ^ "\" as "
            ^ (DiscreteValue.string_of_var_type_discrete l_type)
        );

        (match log_op with
        | Parsed_log_and _ ->
            Parsed_log_and (infer_l_factor, infer_r_factor), l_type
        | Parsed_log_or _ ->
            Parsed_log_or (infer_l_factor, infer_r_factor), l_type
        | Parsed_log_xor _ ->
            Parsed_log_xor (infer_l_factor, infer_r_factor), l_type
        | _ ->
            raise (InternalError "Never happen !")
        )
    | Parsed_log_not factor as log_op ->
        let infer_factor, discrete_type = infer_parsed_discrete_factor variable_infos factor in

        (* factors should be binary words of the same length *)
        if not (DiscreteValue.is_discrete_type_binary_word_type discrete_type) then (
            raise (TypeError (
                "Member of expression \""
                ^ ParsingStructureUtilities.string_of_parsed_factor variable_infos log_op
                ^ "\" is not a binary word: "
                ^ DiscreteValue.string_of_var_type_discrete discrete_type
            ))
        ) else (
            Parsed_log_not infer_factor, discrete_type
        )
    | Parsed_DF_unary_min factor ->
        let infer_factor, factor_type = infer_parsed_discrete_factor variable_infos factor in
        Parsed_DF_unary_min infer_factor, factor_type

(* Type checking and infer literal numbers of non-linear constraint *)
and infer_nonlinear_constraint variable_infos = function
    (* It's ok non-linear constraint is of boolean type *)
    | Parsed_true_nonlinear_constraint -> Parsed_true_nonlinear_constraint, DiscreteValue.Var_type_discrete_bool
    | Parsed_false_nonlinear_constraint -> Parsed_false_nonlinear_constraint, DiscreteValue.Var_type_discrete_bool
    | Parsed_nonlinear_constraint expr ->
        let convert_expr, discrete_type = infer_parsed_discrete_boolean_expression variable_infos expr in
        Parsed_nonlinear_constraint convert_expr, discrete_type

(** Resolve expression discrete type **)

let rec discrete_type_of_expression variable_infos = function
    | Parsed_global_expression expr ->
        discrete_type_of_parsed_boolean_expression variable_infos expr

and discrete_type_of_parsed_boolean_expression variable_infos = function
	| Parsed_True
	| Parsed_False
	| Parsed_And _
	| Parsed_Or _ -> DiscreteValue.Var_type_discrete_bool
	| Parsed_Discrete_boolean_expression expr ->
	    discrete_type_of_parsed_discrete_boolean_expression variable_infos expr

and discrete_type_of_parsed_discrete_boolean_expression variable_infos = function
    | Parsed_arithmetic_expression expr ->
        discrete_type_of_parsed_discrete_arithmetic_expression variable_infos expr
	| Parsed_expression _
	| Parsed_expression_in _
	| Parsed_Not _ ->
	    DiscreteValue.Var_type_discrete_bool
	| Parsed_boolean_expression expr ->
	    discrete_type_of_parsed_boolean_expression variable_infos expr

and discrete_type_of_parsed_discrete_arithmetic_expression variable_infos = function
	| Parsed_DAE_plus (_, term)
	| Parsed_DAE_minus (_, term)
	| Parsed_DAE_term term ->
        discrete_type_of_parsed_discrete_term variable_infos term

and discrete_type_of_parsed_discrete_term variable_infos = function
	| Parsed_DT_mul (_, factor)
	| Parsed_DT_div (_, factor)
	| Parsed_DT_factor factor ->
	    discrete_type_of_parsed_discrete_factor variable_infos factor

and discrete_type_of_parsed_discrete_factor variable_infos = function
	| Parsed_DF_variable variable_name ->
	    get_discrete_type_of_variable_by_name variable_infos variable_name
	| Parsed_DF_constant value ->
	    DiscreteValue.discrete_type_of_value value

	| Parsed_DF_unary_min factor ->
	    discrete_type_of_parsed_discrete_factor variable_infos factor
	| Parsed_DF_expression expr
	| Parsed_rational_of_int_function expr ->
	    DiscreteValue.Var_type_discrete_number DiscreteValue.Var_type_discrete_rational
    | Parsed_pow_function (expr, exp) ->
        (* Pow function result type depends of the left member type *)
        discrete_type_of_parsed_discrete_arithmetic_expression variable_infos expr
    | Parsed_shift_left (factor, _)
    | Parsed_shift_right (factor, _)
    | Parsed_fill_left (factor, _)
    | Parsed_fill_right (factor, _)
    | Parsed_log_and (factor, _)
    | Parsed_log_or (factor, _)
    | Parsed_log_xor (factor, _)
    | Parsed_log_not factor ->
        (* Shift result type is a binary word of length depending on the left member length *)
        (* Logical and, or, xor, not depend on one member length (arbitrary, because already type checked !) *)
        discrete_type_of_parsed_discrete_factor variable_infos factor


(** Checking functions **)

(* Type non-linear constraint *)
(* return a tuple containing the non-linear constraint uniformly typed and the resolved type of the expression *)
let check_nonlinear_constraint variable_infos nonlinear_constraint =

    let uniformly_typed_nonlinear_constraint, discrete_type = infer_nonlinear_constraint variable_infos nonlinear_constraint in
    print_message Verbose_high ("nonlinear constraint " ^ (string_of_parsed_nonlinear_constraint variable_infos nonlinear_constraint) ^ " was checked ");
    (* Check that non-linear constraint is a boolean expression *)
    match discrete_type with
    | DiscreteValue.Var_type_discrete_bool -> uniformly_typed_nonlinear_constraint, discrete_type
    | _ -> raise (TypeError (
        "Guard or invariant expression \""
        ^ (string_of_parsed_nonlinear_constraint variable_infos nonlinear_constraint)
        ^ "\" is not a boolean expression"
    ))


(* Type check guard / invariant *)
(* return a tuple containing the expression uniformly typed and the resolved type of the expression *)
let check_guard variable_infos guard =

    let resolved_nonlinear_constraints = List.map (check_nonlinear_constraint variable_infos) guard in

    let uniformly_typed_nonlinear_constraints = List.map (fun (u, _) -> u) resolved_nonlinear_constraints in
    let nonlinear_constraint_types = List.map (fun (_, t) -> t) resolved_nonlinear_constraints in

    uniformly_typed_nonlinear_constraints, List.hd nonlinear_constraint_types


(* Type check an update *)
(* return a tuple containing the update uniformly typed and the resolved type of the expression *)
let check_update variable_infos variable_name expr =

    (* Resolve expression type and get uniformly typed expression *)
    let uniformly_typed_expr, expr_type = infer_expression variable_infos expr in
    (* Get assigned variable type *)
    let var_type = get_type_of_variable_by_name variable_infos variable_name in
    let var_type_discrete = DiscreteValue.discrete_type_of_var_type var_type in

    (*  *)
    let typed_expr =
        (* Check var_type_discrete is compatible with expression type, if yes, convert expression *)
         if not (DiscreteValue.is_discrete_type_compatibles var_type_discrete expr_type) then (
            raise (TypeError (
                "Variable \""
                ^ variable_name
                ^ "\" of type "
                ^ (DiscreteValue.string_of_var_type var_type)
                ^ " is not compatible with expression \""
                ^ (ParsingStructureUtilities.string_of_parsed_global_expression variable_infos uniformly_typed_expr)
                ^ "\" of type "
                ^ (DiscreteValue.string_of_var_type_discrete expr_type)
                )
            )
        )
        else if DiscreteValue.is_discrete_type_number_type var_type_discrete && DiscreteValue.is_discrete_type_number_type expr_type then (

            (* If the expression type is a number, and as expression type and var type are compatibles *)
            (* convert expression type to variable type (infer to variable type) *)
            print_message Verbose_high (
                "\tInfer update expression \""
                ^ (string_of_parsed_global_expression variable_infos expr)
                ^ "\" to variable type "
                ^ (DiscreteValue.string_of_var_type_discrete var_type_discrete)
            );

            convert_literal_types_of_expression variable_infos var_type_discrete uniformly_typed_expr

        ) else
            uniformly_typed_expr
    in
    variable_name, typed_expr


(* Type check a conditional expression *)
(* return a tuple containing the conditional expression uniformly typed and the resolved type of the expression *)
let check_conditional variable_infos expr =

    let uniformly_typed_bool_expr, expr_type = infer_parsed_boolean_expression variable_infos expr in

    (* Check that non-linear constraint is a boolean expression *)
    if DiscreteValue.is_discrete_type_bool_type expr_type then
        uniformly_typed_bool_expr, expr_type
    else (
        raise (TypeError (
            "Expression \""
            ^ (string_of_parsed_boolean_expression variable_infos expr)
            ^ "\" in conditional statement, is not a boolean expression"
            )
        )
    )

(* Check that an expression assigned to a variable is of the same type *)
(* If not, raise a TypeError exception with an error message *)
let check_type_assignment variable_infos variable_name expr =

    (* Function that construct type error message *)
    let get_error_message variable_name variable_type expr_type expr =
        "Variable "
        ^ variable_name
        ^ " of type "
        ^ (DiscreteValue.string_of_var_type_discrete variable_type)
        ^ " is not compatible with expression : \""
        ^ (string_of_parsed_global_expression variable_infos expr)
        ^ "\""
        ^ " of type "
        ^ (DiscreteValue.string_of_var_type_discrete expr_type)
    in



    (* Get variable type *)
    let variable_type = get_discrete_type_of_variable_by_name variable_infos variable_name in
    (* Resolve expression type *)
    let infer_expr, expr_var_type_discrete = infer_expression variable_infos expr in

    (* Check expression / variable type consistency *)
    let is_consistent = DiscreteValue.is_discrete_type_compatibles variable_type expr_var_type_discrete in

    (* Not consistent ? raise a type error with appropriate message*)
    if not (is_consistent) then (
        raise (TypeError (get_error_message variable_name variable_type expr_var_type_discrete infer_expr))
    )
    else
        infer_expr, expr_var_type_discrete


let check_constant_expression initialized_constants expr =
    let variable_infos = {
        constants = initialized_constants;
        variable_names = [];
        index_of_variables = Hashtbl.create 0;
        removed_variable_names = [];
        type_of_variables = (fun _ -> raise (TypeError "oups !"));
    }
    in
    infer_expression variable_infos expr

let check_constant_declaration (name, _, value, var_type) =
    let is_compatible = DiscreteValue.check_value_compatible_with_type value var_type in
    (* If not compatibles, display an error message *)
    if not (is_compatible) then (
        print_error ("Constant "
            ^ name
            ^ " of type "
            ^ (DiscreteValue.string_of_var_type var_type)
            ^ " is not compatible with value "
            ^ (DiscreteValue.string_of_value value)
            ^ " of type "
            ^ (DiscreteValue.string_of_var_type_discrete (DiscreteValue.discrete_type_of_value value))
        );
        raise (TypeError "Bad constant declaration(s)")
    );

    let discrete_type = DiscreteValue.discrete_type_of_var_type var_type in
    name, DiscreteValue.convert_value_to_discrete_type value discrete_type

(* Check that constant declarations are well typed *)
let check_constant_declarations evaluated_constants =

    (* Check type consistency between constant type and value *)
    let is_types_consistents = List.for_all (fun (name, _, value, var_type) ->
        let is_compatible = DiscreteValue.check_value_compatible_with_type value var_type in
        (* If not compatibles, display an error message *)
        if not (is_compatible) then (
            print_error ("Constant "
                ^ name
                ^ " of type "
                ^ (DiscreteValue.string_of_var_type var_type)
                ^ " is not compatible with value "
                ^ (DiscreteValue.string_of_value value)
                ^ " of type "
                ^ (DiscreteValue.string_of_var_type_discrete (DiscreteValue.discrete_type_of_value value))
            )
        );
        is_compatible
    ) evaluated_constants in

    if not (is_types_consistents) then (
        raise (TypeError "Bad constant declaration(s)")
    );

    (* Convert value assigned to the constant to the type of the constant *)
    (* and create tuples for representing constants as name * value *)
    let constant_tuples = List.map (fun (name, _, value, var_type) ->
        let discrete_type = DiscreteValue.discrete_type_of_var_type var_type in
        name, DiscreteValue.convert_value_to_discrete_type value discrete_type
    ) evaluated_constants in


    constant_tuples

(* Check that a discrete variable initialization is well typed *)
let check_discrete_init variable_infos variable_name expr =

    (* Get the variable index *)
    let discrete_index = Hashtbl.find variable_infos.index_of_variables variable_name in
    (* Get variable type *)
    let var_type = get_type_of_variable variable_infos discrete_index in
    let var_discrete_type = DiscreteValue.discrete_type_of_var_type var_type in

    (* Check whether variable is clock or parameter *)
    let is_clock_or_parameter = var_type == DiscreteValue.Var_type_clock || var_type == DiscreteValue.Var_type_parameter in

    (* Check if variable is clock or parameter, it's forbidden to init clock or parameter in discrete section *)
    if (is_clock_or_parameter) then (
        raise (TypeError ("Initialisation of a " ^ (DiscreteValue.string_of_var_type var_type) ^ " in discrete init state section is forbidden"))
    );

    (* Check expression / variable type consistency *)
    let infer_expr, expr_type = check_type_assignment variable_infos variable_name expr in

    (* If expression type was unknown number, *)
    (* and as we had already check the compatibility of variable type and expression type above *)
    (* we should convert expression type to variable type *)
    let converted_expr =
        if DiscreteValue.is_discrete_type_unknown_number_type expr_type then (
            print_message Verbose_high (
                "\tInfer expression type of \""
                ^ ParsingStructureUtilities.string_of_parsed_global_expression variable_infos infer_expr
                ^ "\" as the same as assigned variable type: " ^ DiscreteValue.string_of_var_type_discrete var_discrete_type
            );
            convert_literal_types_of_expression variable_infos var_discrete_type infer_expr
        )
        else
            infer_expr
    in

    converted_expr
