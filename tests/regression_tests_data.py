#!/usr/bin/python
# -*- coding: utf-8 -*-
#************************************************************
#
#                       IMITATOR
#
#             Data for non-regression tests
#
# Université Paris 13, LIPN, CNRS, France
# Université de Lorraine, CNRS, Inria, LORIA, Nancy, France
#
# File description  : non-regression tests data
#
# File contributors : Étienne André, Jaime Arias, Benjamin Loillier
#
# Created           : 2015/10/23
# Last modified     : 2021/07/09
#************************************************************



#************************************************************
# TESTS TO CARRY
#************************************************************
tests = [

	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	# TEMPLATE
	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

	##------------------------------------------------------------
	#{
		## Test version             : 1
		## Test since               : 2021/03/33
		## Last modified            : 2021/03/33
		## Test for IMITATOR version: 3.1
		#'purpose'    : 'Test something',
		#'input_files': ['somemodel.imi'],
		#'options'    : '-mode checksyntax ',
		#'expectations' : [
			#{'file': 'somemodel.res' , 'content' : """
#here the content to check
		#"""
			#} # end result file
			#,
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------

	#,

	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	# FILE NOT FOUND TESTS
	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/01/22
		# Last modified            : 2021/01/22
		# Test for IMITATOR version: 3
		'purpose'    : 'Test the absence of model',
		'input_files': ['thisfiledoesnotexist.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'thisfiledoesnotexist.res' , 'content' : """
Error                                   : model file not found
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/01/22
		# Last modified            : 2021/01/22
		# Test for IMITATOR version: 3
		'purpose'    : 'Test the absence of property',
		'input_files': ['testL.imi', 'thisfiledoesnotexist.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testL.res' , 'content' : """
Error                                   : property file not found
		"""
			} # end result file
			,
		] # end expectations
	} # end test casearithmetic_expressions
	#------------------------------------------------------------

	,
	
	# TODO: same + `-mode checksyntax`

	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	# TESTS TO CHECK THE SYNTAX
	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/02/02
		# Last modified            : 2021/02/05
		# Test for IMITATOR version: 3
		'purpose'    : 'Test syntax rejection: non-linear clock',
		'input_files': ['testSyntaxNonLinearClock.imi'],
		'options'    : '-mode checksyntax',
		'expectations' : [
			{'file': 'testSyntaxNonLinearClock.res' , 'content' : """
Error                                   : invalid model
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	# SYNTACTIC TESTS (statistics on models)
	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Last modified            : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the L/U-nature (L-PTA)',
		'input_files': ['testL.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testL.res' , 'content' : """
L/U subclass                            : L-PTA
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/06/25
		# Last modified            : 2021/06/25
		# Test for IMITATOR version: 3.1
		'purpose'    : 'Test model syntax check even when a (non-existing) property is passed',
		'input_files': ['testL.imi', 'nonexistingfile.imiprop'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testL.res' , 'content' : """
L/U subclass                            : L-PTA
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the L/U-nature (U-PTA)',
		'input_files': ['testU.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testU.res' , 'content' : """
L/U subclass                            : U-PTA
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the L/U-nature (L/U-PTA)',
		'input_files': ['testLU.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testLU.res' , 'content' : """
L/U subclass                            : L/U-PTA
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the L/U-nature (none)',
		'input_files': ['testNotLU.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testNotLU.res' , 'content' : """
L/U subclass                            : not L/U
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the L/U-nature (flip-flop: U)',
		'input_files': ['flipflop.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'flipflop.res' , 'content' : """
L/U subclass                            : U-PTA
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the L/U-nature (JR15: L/U)',
		'input_files': ['JLR-TACAS13.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'JLR-TACAS13.res' , 'content' : """
L/U subclass                            : L/U-PTA
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Last modified            : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the L/U-nature (L-PTA with negative coefficients)',
		'input_files': ['testLneg.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testLneg.res' , 'content' : """
L/U subclass                            : L-PTA
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	##------------------------------------------------------------
	#{
		## Test version             : 1
		## Test since               : 2019/07/09
		## Last modified            : 2019/07/09
		## Test disabled            : 2021/04/27
		## Test for IMITATOR version: 2.12
		#'purpose'    : 'Test the L/U-nature (L-PTA with p > d)',
		#'input_files': ['testLdiscrete.imi'],
		#'options'    : '-mode checksyntax ',
		#'expectations' : [
			#{'file': 'testLdiscrete.res' , 'content' : """
#L/U subclass                            : L-PTA
		#"""
			#} # end result file
			#,
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------

	#,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the detection of silent actions: no',
		'input_files': ['testLU.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testLU.res' , 'content' : """
Has silent actions?                            : false
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the detection of silent actions: yes',
		'input_files': ['testNotLU.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testNotLU.res' , 'content' : """
Has silent actions?                            : true
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the detection of silent actions: JR15',
		'input_files': ['JLR-TACAS13.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'JLR-TACAS13.res' , 'content' : """
Has silent actions?                            : true
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the detection of strong determinism: yes',
		'input_files': ['testLU.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testLU.res' , 'content' : """
Is strongly deterministic?              : true
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the detection of strong determinism: yes',
		'input_files': ['testStrongDet.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testStrongDet.res' , 'content' : """
Is strongly deterministic?              : true
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the detection of strong determinism: yes',
		'input_files': ['testStrongDet2.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testStrongDet2.res' , 'content' : """
Is strongly deterministic?              : true
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/07/09
		# Test for IMITATOR version: 2.12
		'purpose'    : 'Test the detection of strong determinism: no',
		'input_files': ['testNotStrongDet.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'testNotStrongDet.res' , 'content' : """
Is strongly deterministic?              : false
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	# TESTS ON UNSATISFIABLE INITIAL STATE
	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/02/05
		# Last modified            : 2021/02/05
		# Test for IMITATOR version: 3
		'purpose'    : 'Test unsatisfiable initial state (clock constraint)',
		'input_files': ['unsatisfiableInitStateClocks.imi'],
		'options'    : '-mode statespace',
		'expectations' : [
			{'file': 'unsatisfiableInitStateClocks.res' , 'content' : """
Error                                   : unsatisfiable initial state
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/07/05
		# Last modified            : 2021/07/05
		# Test for IMITATOR version: 3.1
		'purpose'    : 'Test state space (unsatisfiable initial state) even when a (useless, and non-existing) property is passed',
		'input_files': ['unsatisfiableInitStateClocks.imi', 'nonexistingfile.imiprop'],
		'options'    : '-mode statespace',
		'expectations' : [
			{'file': 'unsatisfiableInitStateClocks.res' , 'content' : """
Error                                   : unsatisfiable initial state
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/02/05
		# Last modified            : 2021/02/05
		# Test for IMITATOR version: 3
		'purpose'    : 'Test unsatisfiable initial state (clock constraint + invariant)',
		'input_files': ['unsatisfiableInitStateClocksInv.imi'],
		'options'    : '-mode statespace',
		'expectations' : [
			{'file': 'unsatisfiableInitStateClocksInv.res' , 'content' : """
Error                                   : unsatisfiable initial state
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/02/05
		# Last modified            : 2021/02/05
		# Test for IMITATOR version: 3
		'purpose'    : 'Test unsatisfiable initial state (discrete+clock constraint)',
		'input_files': ['unsatisfiableInitStateDiscrete.imi'],
		'options'    : '-mode statespace',
		'expectations' : [
			{'file': 'unsatisfiableInitStateDiscrete.res' , 'content' : """
Error                                   : unsatisfiable initial state
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/02/05
		# Last modified            : 2021/02/05
		# Test for IMITATOR version: 3
		'purpose'    : 'Test unsatisfiable initial state (incompatible discrete invariant)',
		'input_files': ['unsatisfiableInitStateDiscreteInv.imi'],
		'options'    : '-mode statespace',
		'expectations' : [
			{'file': 'unsatisfiableInitStateDiscreteInv.res' , 'content' : """
Error                                   : unsatisfiable initial state
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	# TESTS ON DISCRETE VARIABLES
	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/02/05
		# Last modified            : 2021/02/05
		# Test for IMITATOR version: 3
		'purpose'    : 'Test division by 0',
		'input_files': ['divisionby0.imi'],
		'options'    : '-mode statespace',
		'expectations' : [
			{'file': 'divisionby0.res' , 'content' : """
Error                                   : division by 0
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	##------------------------------------------------------------
	{
		'purpose'    : 'Test variable elimination in Boolean expressions',
		'input_files': ['testConditions.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'testConditions-statespace.states' , 'content' : """
  STATE 0:
  pta: l1, i = 0, j = 0, l = 0 ==>
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	##------------------------------------------------------------]

	,

	##------------------------------------------------------------
	{
		'purpose'    : 'Test evaluation of <if> branch in conditional update',
		'input_files': ['testConditions.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'testConditions-statespace.states' , 'content' : """
	STATE 1:
	pta: l2, i = 0, j = 0, l = 15 ==>
	& x >= 0
	& p = 1
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	##------------------------------------------------------------]

	,

	##------------------------------------------------------------
	{
		'purpose'    : 'Test evaluation of <else> branch in conditional update',
		'input_files': ['testConditions.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'testConditions-statespace.states' , 'content' : """
	STATE 2:
  pta: l1, i = 2, j = 0, l = 15 ==>
	& x >= 2
	& p = 1
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	##------------------------------------------------------------]

	,

	##------------------------------------------------------------
	{
		'purpose'    : 'Test include files [1]',
		'input_files': ['tests_include_model/example-include-1a.imi'],
		'options'    : '-imi2IMI -no-var-autoremove',
		'expectations' : [
			{'file': 'example-include-1a-regenerated.imi' , 'content' : """
var
	x
		: clock;

	i
		: rational;

	p
		: parameter;


(************************************************************)
 automaton pta1
(************************************************************)
 synclabs: a;

loc l1: invariant True
	when  x = 1 do {x := 0}  sync a goto l1;
 end (* pta1 *)
(************************************************************)


(************************************************************)
 automaton pta2
(************************************************************)
 synclabs: a;

loc l1: invariant True
	when  x = 1 do {x := 0}  sync a goto l1;
 end (* pta2 *)
(************************************************************)


(************************************************************)
(* Initial state *)
(************************************************************)

init := {

	discrete = 
		(*------------------------------------------------------------*)
		(* Initial location *)
		(*------------------------------------------------------------*)
		loc[pta1] := l1, 
		loc[pta2] := l1,
		(*------------------------------------------------------------*)
		(* Initial discrete variables assignments *)
		(*------------------------------------------------------------*)
		i := 0
	;

	(*------------------------------------------------------------*)
	(* Initial continuous constraint *)
	(*------------------------------------------------------------*)
	continuous = 
		&  p >= 0
		& x = 0
	;
}


(************************************************************)
(* The end *)
(************************************************************)
end
			"""
			} # end result file
			,
		] # end expectations
	} # end test case
	##------------------------------------------------------------]

	,

	##------------------------------------------------------------
	{
		'purpose'    : 'Test include files [2]',
		'input_files': ['tests_include_model/example-include-2a.imi'],
		'options'    : '-imi2IMI -no-var-autoremove',
		'expectations' : [
			{'file': 'example-include-2a-regenerated.imi' , 'content' : """
var
	y, x
		: clock;

	j, i
		: rational;

	p
		: parameter;



(************************************************************)
 automaton pta1
(************************************************************)
 synclabs: a;

loc l1: invariant True
	when  p + 1 = x do {x := 0}  sync a goto l1;
 end (* pta1 *)
(************************************************************)

(************************************************************)
 automaton pta2
(************************************************************)
 synclabs: a;

loc l1: invariant True
	when  y = 1 do {y := p}  sync a goto l1;
 end (* pta2 *)
(************************************************************)


(************************************************************)
(* Initial state *)
(************************************************************)

init := {

	discrete = 
		(*------------------------------------------------------------*)
		(* Initial location *)
		(*------------------------------------------------------------*)
		loc[pta1] := l1, 
		loc[pta2] := l1,
		(*------------------------------------------------------------*)
		(* Initial discrete variables assignments *)
		(*------------------------------------------------------------*)
		j := 0, 
		i := 0
	;

	(*------------------------------------------------------------*)
	(* Initial continuous constraint *)
	(*------------------------------------------------------------*)
	continuous = 
		&  p >= 1
		& y = 0
		& x = 0
	;
}



(************************************************************)
(* The end *)
(************************************************************)
end
			"""
			} # end result file
			,
		] # end expectations
	} # end test case
	##------------------------------------------------------------]

	,

	##------------------------------------------------------------
	{
		'purpose'    : 'Test include files [3]',
		'input_files': ['tests_include_model/example-include-3a.imi'],
		'options'    : '-imi2IMI -no-var-autoremove',
		'expectations' : [
			{'file': 'example-include-3a-regenerated.imi' , 'content' : """
var
	y, x
		: clock;

	j, i
		: rational;

	p
		: parameter;

(************************************************************)
 automaton pta1
(************************************************************)
 synclabs: a;

loc l1: invariant True
	when  p + 1 = x do {x := 0}  sync a goto l1;
 end (* pta1 *)
(************************************************************)


(************************************************************)
 automaton pta2
(************************************************************)
 synclabs: a;

loc l1: invariant True
	when  y = 1 do {y := p}  sync a goto l1;
 end (* pta2 *)
(************************************************************)



(************************************************************)
(* Initial state *)
(************************************************************)

init := {

	discrete = 
		(*------------------------------------------------------------*)
		(* Initial location *)
		(*------------------------------------------------------------*)
		loc[pta1] := l1, 
		loc[pta2] := l1,
		(*------------------------------------------------------------*)
		(* Initial discrete variables assignments *)
		(*------------------------------------------------------------*)
		j := 0, 
		i := 0
	;

	(*------------------------------------------------------------*)
	(* Initial continuous constraint *)
	(*------------------------------------------------------------*)
	continuous = 
		&  p >= 1
		& y = 0
		& x = 0
	;
}

(************************************************************)
(* The end *)
(************************************************************)
end
			"""
			} # end result file
			,
		] # end expectations
	} # end test case
	##------------------------------------------------------------]

	,


	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	# AUTOMATIC VARIABLES REMOVAL
	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

	#------------------------------------------------------------
	{
		'purpose'    : 'Test discrete variable automatic removal',
		'input_files': ['testVarElim.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			# NOTE: we just parse the beginning of state 1 to check that the variables are properly removed
			{'file': 'testVarElim-statespace.states' , 'content' : """
  STATE 1:
  pta: l1, i = 0, j = 0 ==>
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test absence of discrete variable automatic removal',
		'input_files': ['testVarElim.imi'],
		'options'    : '-mode statespace -states-description -no-var-autoremove',
		'expectations' : [
			# NOTE: we just parse the beginning of state 1 to check that the variables are properly removed
			{'file': 'testVarElim-statespace.states' , 'content' : """
  STATE 1:
  pta: l1, i = 0, j = 0, k = 0, l = 0 ==>
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/07/01
		# Last modified            : 2021/07/01
		# Test for IMITATOR version: 3.1
		'purpose'    : 'Test no clock removal for x=y with x used in the model but not y',
		'tags' : 'auto remove',
		'input_files': ['test_var_remove.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'test_var_remove.res' , 'content' : """
Number of clocks                        : 2
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/07/01
		# Last modified            : 2021/07/01
		# Test for IMITATOR version: 3.1
		'purpose'    : 'Test correct variable removal for more complex dependencies',
		'tags' : 'auto remove',
		'input_files': ['test_var_remove_2.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'test_var_remove_2.res' , 'content' : """
Number of clocks                        : 3
		""" # TODO: add check for rational and parameter too, etc., perhaps using a -mode statespace -states-description -depth-limit 2
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/07/08
		# Last modified            : 2021/07/08
		# Test for IMITATOR version: 3.1
		'purpose'    : 'Test variable removal for event-recording automata',
		'input_files': ['LALSD14_AIP.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'LALSD14_AIP.res' , 'content' : """
Number of clocks                        : 4
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/07/08
		# Last modified            : 2021/07/08
		# Test for IMITATOR version: 3.1
		'purpose'    : 'Test variable removal for various types',
		'input_files': ['test_removal.imi'],
		'options'    : '-mode checksyntax ',
		'expectations' : [
			{'file': 'test_removal.res' , 'content' : """
Number of clocks                        : 1
		"""
			} # end result file
			,
			{'file': 'test_removal.res' , 'content' : """
Number of parameters                    : 1
Number of discrete variables            : 1
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
	# STATE SPACE GENERATION
	#*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

	#------------------------------------------------------------
	{
		# Test version             : TODO
		# Test since               : TODO
		# Test for IMITATOR version: TODO
		'purpose'    : 'Test the state space',
		'input_files': ['flipflop.imi'],
		'options'    : '-mode statespace -states-description -no-var-autoremove', #TODO: re-do without '-no-var-autoremove'
		'expectations' : [
			{'file': 'flipflop-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  input: Input0, g1: G10011, g2: G2101, g3: G30011, g4: G410 ==>
& 5 >= s
& dG3_u >= 8
& dG4_u >= 3
& s >= 0
& ckG1 >= s
& ckG2 >= s
& ckG3 >= s
& ckG4 >= s

  Projection onto the parameters:
   dG4_u >= 3
& dG3_u >= 8

  /************************************************************/
  STATE 1:
  input: Input1, g1: G11011, g2: G2101, g3: G30011, g4: G410 ==>
& 12 >= s
& dG3_u >= 8
& dG4_u >= 3
& s >= 5
& ckG2 >= s
& ckG3 >= s
& ckG4 >= s
& s = 5 + ckG1

  Projection onto the parameters:
   dG4_u >= 3
& dG3_u >= 8

  /************************************************************/
  STATE 2:
  input: Input1, g1: G11010, g2: G2001, g3: G30011, g4: G410 ==>
& 15 >= s
& dG3_u >= 8
& dG4_u >= 3
& s >= 12
& ckG2 >= s
& ckG3 >= s
& ckG4 >= s
& s = 5 + ckG1

  Projection onto the parameters:
   dG4_u >= 3
& dG3_u >= 8

  /************************************************************/
  STATE 3:
  input: Input2, g1: G11110, g2: G2011, g3: G30111, g4: G410 ==>
& dG3_u + 15 >= s
& 32 >= s
& dG3_u >= 8
& dG4_u >= 3
& ckG2 >= s
& s >= 15
& ckG4 >= s
& s = 5 + ckG1
& s = 15 + ckG3

  Projection onto the parameters:
   dG3_u >= 8
& dG4_u >= 3

  /************************************************************/
  STATE 4:
  input: Input3, g1: G10110, g2: G2011, g3: G30111, g4: G410 ==>
& 39 >= s
& dG3_u + 15 >= s
& dG4_u >= 3
& ckG2 >= s
& s >= 32
& ckG4 >= s
& s = 5 + ckG1
& s = 15 + ckG3

  Projection onto the parameters:
   dG3_u >= 17
& dG4_u >= 3

  /************************************************************/
  STATE 5:
  input: Input2, g1: G11110, g2: G2011, g3: G30110, g4: G400 ==>
& 32 >= s
& dG3_u + ckG4 + 15 >= s
& dG4_u >= 3
& s >= 23 + ckG4
& ckG4 >= 0
& ckG2 >= s
& dG4_u >= ckG4
& s = 5 + ckG1
& s = 15 + ckG3

  Projection onto the parameters:
   dG3_u >= 8
& dG4_u >= 3

  /************************************************************/
  STATE 6:
  input: Input4, g1: G10010, g2: G2001, g3: G30011, g4: G410 ==>
& dG3_u >= 24
& dG4_u >= 3
& ckG2 >= 39
& ckG4 >= 39
& s = 0
& ckG1 = 0
& ckG3 = 24

  Projection onto the parameters:
   dG4_u >= 3
& dG3_u >= 24

  /************************************************************/
  STATE 7:
  input: Input3, g1: G10110, g2: G2011, g3: G30110, g4: G400 ==>
& 39 >= s
& dG3_u + ckG4 + 15 >= s
& dG4_u >= 3
& s >= 32 + ckG4
& ckG4 >= 0
& ckG2 >= s
& dG4_u >= ckG4
& s = 5 + ckG1
& s = 15 + ckG3

  Projection onto the parameters:
   dG3_u >= 17
& dG4_u >= 3

  /************************************************************/
  STATE 8:
  input: Input3, g1: G10110, g2: G2011, g3: G30110, g4: G400 ==>
& 39 >= s
& dG3_u + ckG4 + 15 >= s
& dG4_u >= ckG4
& dG4_u >= 3
& ckG2 >= s
& s >= 32
& s >= 23 + ckG4
& ckG4 + 32 >= s
& s = 5 + ckG1
& s = 15 + ckG3

  Projection onto the parameters:
   dG3_u + dG4_u >= 17
& dG4_u >= 3
& dG3_u >= 8

  /************************************************************/
  STATE 9:
  input: Input2, g1: G11110, g2: G2011, g3: G31110, g4: G401 ==>
& dG3_u + ckG4 + 15 >= s
& dG4_u >= 3
& s >= 23 + ckG4
& ckG4 >= 3
& ckG2 >= s
& 32 >= s
& s = 5 + ckG1
& s = 15 + ckG3

  Projection onto the parameters:
   dG3_u >= 8
& dG4_u >= 3

  /************************************************************/
  STATE 10:
  input: Input4, g1: G10010, g2: G2001, g3: G30010, g4: G400 ==>
& dG3_u + ckG4 >= 24
& dG4_u >= ckG4
& dG4_u >= 3
& ckG2 >= 39
& ckG4 >= 0
& 7 >= ckG4
& s = 0
& ckG1 = 0
& ckG3 = 0

  Projection onto the parameters:
   dG3_u + dG4_u >= 24
& dG3_u >= 17
& dG4_u >= 3

  /************************************************************/
  STATE 11:
  input: Input3, g1: G10110, g2: G2011, g3: G31110, g4: G401 ==>
& dG3_u + ckG4 + 15 >= s
& dG4_u >= 3
& s >= 32 + ckG4
& ckG4 >= 3
& ckG2 >= s
& 39 >= s
& s = 5 + ckG1
& s = 15 + ckG3

  Projection onto the parameters:
   dG3_u >= 17
& dG4_u >= 3

  /************************************************************/
  STATE 12:
  input: Input4, g1: G10010, g2: G2001, g3: G30010, g4: G400 ==>
& dG3_u + ckG4 >= 24
& dG4_u >= ckG4
& ckG2 >= 39
& ckG4 >= 7
& 16 >= ckG4
& s = 0
& ckG1 = 0
& ckG3 = 0

  Projection onto the parameters:
   dG4_u >= 7
& dG3_u >= 8
& dG3_u + dG4_u >= 24

  /************************************************************/
  STATE 13:
  input: Input3, g1: G10110, g2: G2011, g3: G31110, g4: G401 ==>
& 39 >= s
& dG3_u + ckG4 + 15 >= s
& dG4_u + s >= 32 + ckG4
& dG4_u >= 3
& s >= 32
& s >= 23 + ckG4
& ckG4 >= 3
& ckG2 >= s
& ckG4 + 32 >= s
& s = 5 + ckG1
& s = 15 + ckG3

  Projection onto the parameters:
   dG3_u + dG4_u >= 17
& dG3_u >= 8
& dG4_u >= 3

  /************************************************************/
  STATE 14:
  input: Input3, g1: G10110, g2: G2011, g3: G31110, g4: G401 ==>
& 39 >= s
& dG3_u + ckG4 + 15 >= s
& dG4_u >= 3
& ckG2 >= s
& s >= 32
& s >= 23 + ckG4
& ckG4 + 29 >= s
& s = 5 + ckG1
& s = 15 + ckG3

  Projection onto the parameters:
   dG3_u >= 8
& dG4_u >= 3

  /************************************************************/
  STATE 15:
  input: Input4, g1: G10010, g2: G2001, g3: G31010, g4: G401 ==>
& dG3_u + ckG4 >= 24
& dG4_u + 7 >= ckG4
& dG4_u >= 3
& ckG2 >= 39
& ckG4 >= 7
& 16 >= ckG4
& s = 0
& ckG1 = 0
& ckG3 = 24

  Projection onto the parameters:
   dG3_u + dG4_u >= 17
& dG3_u >= 8
& dG4_u >= 3

  /************************************************************/
  STATE 16:
  input: Input4, g1: G10010, g2: G2001, g3: G31010, g4: G401 ==>
& dG3_u + ckG4 >= 24
& dG4_u >= ckG4
& ckG2 >= 39
& ckG4 >= 7
& 16 >= ckG4
& s = 0
& ckG1 = 0
& ckG3 = 0

  Projection onto the parameters:
   dG4_u >= 7
& dG3_u >= 8
& dG3_u + dG4_u >= 24

  /************************************************************/
  STATE 17:
  input: Input4, g1: G10010, g2: G2001, g3: G31010, g4: G401 ==>
& dG3_u + ckG4 >= 24
& dG4_u >= 3
& ckG2 >= 39
& ckG4 >= 3
& 7 >= ckG4
& s = 0
& ckG1 = 0
& ckG3 = 24

  Projection onto the parameters:
   dG3_u >= 17
& dG4_u >= 3

  /************************************************************/
  STATE 18:
  input: Input4, g1: G10010, g2: G2001, g3: G31010, g4: G401 ==>
& dG3_u + ckG4 >= 24
& dG4_u >= ckG4
& ckG2 >= 39
& ckG4 >= 3
& 7 >= ckG4
& s = 0
& ckG1 = 0
& ckG3 = 0

  Projection onto the parameters:
   dG4_u >= 3
& dG3_u >= 17
& dG3_u + dG4_u >= 24

  /************************************************************/
  STATE 19:
  input: Input4, g1: G10010, g2: G2001, g3: G31010, g4: G401 ==>
& dG3_u + ckG4 >= 24
& dG4_u >= 3
& ckG2 >= 39
& ckG4 >= 10
& 16 >= ckG4
& s = 0
& ckG1 = 0
& ckG3 = 24

  Projection onto the parameters:
   dG3_u >= 8
& dG4_u >= 3

/************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "dUp"
  s_1 -> s_2 via "qG1Down"
  s_2 -> s_3 via "ckUp"
  s_3 -> s_4 via "dDown"
  s_3 -> s_5 via "qG3Down"
  s_4 -> s_6 via "ckDown"
  s_4 -> s_7 via "qG3Down"
  s_5 -> s_8 via "dDown"
  s_5 -> s_9 via "qUp"
  s_7 -> s_10 via "ckDown"
  s_7 -> s_11 via "qUp"
  s_8 -> s_12 via "ckDown"
  s_8 -> s_13 via "qUp"
  s_9 -> s_14 via "dDown"
  s_10 -> s_18 via "qUp"
  s_11 -> s_17 via "ckDown"
  s_12 -> s_16 via "qUp"
  s_13 -> s_15 via "ckDown"
  s_14 -> s_19 via "ckDown"
			"""
			} #end statespace file
		] # end expectations
	} # end test case
	,
	##------------------------------------------------------------
	#{
		## Test version: 2.11
		## Test since  : 2019/03/07
		## Test until  : 2020/03/20
		## Reason for removal: projectresult is now in the property, so a state space cannot be projected
		#'purpose'    : 'Test state space with projection',
		#'input_files': ['testProjectP.imi'],
		#'options'    : '-mode statespace -states-description',
		#'expectations' : [
			#{'file': 'testProjectP-statespace.states' , 'content' : """
  #DESCRIPTION OF THE STATES

  #/************************************************************/
  #INITIAL
  #STATE 0:
  #pta: l1 ==>
#& pabs >= 0
#& p1 >= x
#& p3 >= 0
#& x >= 0
#& x = xabs

  #Projection onto the parameters:
   #p3 >= 0
#& p1 >= 0
#& pabs >= 0

  #Projection onto selected parameters {pabs}:
   #pabs >= 0

  #/************************************************************/
  #STATE 1:
  #pta: l2 ==>
#& pabs >= 0
#& p1 >= 0
#& p3 >= x
#& x >= 0
#& p1 + x = xabs

  #Projection onto the parameters:
   #p3 >= 0
#& p1 >= 0
#& pabs >= 0

  #Projection onto selected parameters {pabs}:
   #pabs >= 0

  #/************************************************************/
  #STATE 2:
  #pta: lfinal ==>
#& pabs >= 0
#& p3 >= 0
#& pabs = p1
#& x = 0
#& pabs = xabs

  #Projection onto the parameters:
   #p3 >= 0
#& p1 >= 0
#& pabs = p1

  #Projection onto selected parameters {pabs}:
   #pabs >= 0

  #/************************************************************/
  #STATE 3:
  #pta: l3 ==>
#& 2 >= x
#& pabs >= 0
#& p1 >= 0
#& p3 >= 0
#& x >= 0
#& p1 + p3 + x = xabs

  #Projection onto the parameters:
   #p3 >= 0
#& p1 >= 0
#& pabs >= 0

  #Projection onto selected parameters {pabs}:
   #pabs >= 0

  #/************************************************************/
  #STATE 4:
  #pta: lfinal ==>
#& pabs >= p1
#& p1 >= 0
#& pabs = p1 + p3
#& x = 0
#& pabs = xabs

  #Projection onto the parameters:
   #p3 >= 0
#& p1 >= 0
#& pabs = p1 + p3

  #Projection onto selected parameters {pabs}:
   #pabs >= 0

  #/************************************************************/
  #STATE 5:
  #pta: l4 ==>
#& 2 >= x
#& pabs >= 0
#& p1 >= 0
#& p3 >= 2
#& x >= 0
#& p1 + x + 2 = xabs

  #Projection onto the parameters:
   #p3 >= 2
#& p1 >= 0
#& pabs >= 0

  #Projection onto selected parameters {pabs}:
   #pabs >= 0

  #/************************************************************/
  #STATE 6:
  #pta: lfinal ==>
#& pabs >= 2
#& p3 >= 2
#& pabs = 2 + p1
#& x = 0
#& pabs = xabs

  #Projection onto the parameters:
   #p3 >= 2
#& pabs >= 2
#& pabs = 2 + p1

  #Projection onto selected parameters {pabs}:
   #pabs >= 2

  #/************************************************************/
  #STATE 7:
  #pta: l4 ==>
#& 2 >= x
#& pabs >= 0
#& p1 + p3 + x + 2 >= xabs
#& p1 >= 0
#& p3 >= 0
#& x >= 0
#& xabs >= p1 + p3 + x

  #Projection onto the parameters:
   #p3 >= 0
#& p1 >= 0
#& pabs >= 0

  #Projection onto selected parameters {pabs}:
   #pabs >= 0

  #/************************************************************/
  #STATE 8:
  #pta: lfinal ==>
#& p1 + p3 + 2 >= pabs
#& pabs >= p1 + p3
#& p1 >= 0
#& p3 >= 0
#& x = 0
#& pabs = xabs

  #Projection onto the parameters:
   #p1 + p3 + 2 >= pabs
#& pabs >= p1 + p3
#& p3 >= 0
#& p1 >= 0

  #Projection onto selected parameters {pabs}:
   #pabs >= 0

  #DESCRIPTION OF THE TRANSITIONS
  #s_0 -> s_1 via "a"
  #s_0 -> s_2 via "a"
  #s_1 -> s_3 via "a"
  #s_1 -> s_4 via "a"
  #s_1 -> s_5 via "b"
  #s_1 -> s_6 via "b"
  #s_3 -> s_7 via "a"
  #s_3 -> s_8 via "a"
#"""
			#} # end result file
			#,
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------

	#,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/28
		# Last modified            : 2020/09/28
		# Test for IMITATOR version: 3
		'purpose'    : 'Test the state space (no float conversion)',
		'input_files': ['testFloat.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'testFloat-statespace.states' , 'content' : """
pta: l2, i = 5/4, j = 1/3
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/28
		# Last modified            : 2020/09/28
		# Test for IMITATOR version: 3
		'purpose'    : 'Test the state space (with float conversion)',
		'input_files': ['testFloat.imi'],
		'options'    : '-mode statespace -states-description -output-float',
		'expectations' : [
		# NOTE: cut the end of the float just in case the OS doesn't represent them the same way…
			{'file': 'testFloat-statespace.states' , 'content' : """
pta: l2, i = 5/4 (~ 1.25), j = 1/3 (~ 0.3333333333
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test urgency',
		'input_files': ['testUrgency.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'testUrgency-statespace.states' , 'content' : """
		  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_0 via "a"
  s_0 -> s_1 via "b"
  s_0 -> s_2 via "b"
  s_1 -> s_3 via "c"
  s_2 -> s_4 via "b"
  s_2 -> s_4 via "c"
  s_3 -> s_1 via "b"
  s_3 -> s_3 via "a"
  s_4 -> s_4 via "a"
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test synchronization model',
		'input_files': ['testSynchro.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'testSynchro-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta1: l1, pta2: l1, pta3: l1 ==>
& 3 >= x
& x >= 0

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 1:
  pta1: l1, pta2: l1, pta3: l2 ==>
& 3 >= x
& x >= 0

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 2:
  pta1: l1, pta2: l1, pta3: l3 ==>
& x >= 0

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 3:
  pta1: l2, pta2: l2, pta3: l3 ==>
& x >= 4

  Projection onto the parameters:
  True

/************************************************************/
DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "c"
  s_1 -> s_2 via "a"
  s_2 -> s_3 via "b"
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test updates (printing)',
		'input_files': ['testUpdates.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'testUpdates-regenerated.imi' , 'content' : """
  urgent loc idle: invariant True
	when True do {x := 1/2*p + x + -7*i + -1, y := y + 1, i := (3 * i - 1) / (5 * i * i)}  sync a goto idle;
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test updates and inequalities printing order (printing)',
		'input_files': ['testUpdatesInequalitiesOrder.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'testUpdatesInequalitiesOrder-regenerated.imi' , 'content' : """
	when  a > 0
& b > 0
& c > 0 do {a := 0, b := 0, c := 0}  sync a goto idle;
	when True do {a := 2, b := 3 + 3, c := 0}  sync a goto idle;
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (linear D reachable)',
		'input_files': ['linear_expressions/linear-invariant-d-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'linear-invariant-d-reachable.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (linear PD reachable)',
		'input_files': ['linear_expressions/linear-invariant-pd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'linear-invariant-pd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
 10 > p1
& p1 > 0
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (linear XD reachable)',
		'input_files': ['linear_expressions/linear-invariant-xd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'linear-invariant-xd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (linear PXD reachable)',
		'input_files': ['linear_expressions/linear-invariant-pxd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'linear-invariant-pxd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
 p1 > 0
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (linear D reachable)',
		'input_files': ['linear_expressions/linear-invariant-d-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'linear-invariant-d-reachable.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (linear PD reachable)',
		'input_files': ['linear_expressions/linear-invariant-pd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'linear-invariant-pd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
 10 > p1
& p1 > 0
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (linear XD reachable)',
		'input_files': ['linear_expressions/linear-invariant-xd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'linear-invariant-xd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (linear PXD reachable)',
		'input_files': ['linear_expressions/linear-invariant-pxd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'linear-invariant-pxd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
 p1 > 0
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (non-linear D reachable)',
		'input_files': ['nonlinear_expressions/nonlinear-guard-d-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-guard-d-reachable.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (non-linear PD reachable)',
		'input_files': ['nonlinear_expressions/nonlinear-guard-pd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-guard-pd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
 10 > p1
& p1 > 0
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (non-linear XD reachable)',
		'input_files': ['nonlinear_expressions/nonlinear-guard-xd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-guard-xd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (non-linear PXD reachable)',
		'input_files': ['nonlinear_expressions/nonlinear-guard-pxd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-guard-pxd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
 p1 > 0
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (non-linear PD semantic error)',
		'input_files': ['nonlinear_expressions/nonlinear-guard-pd-semantic-error.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-guard-pd-semantic-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (non-linear XD semantic error)',
		'input_files': ['nonlinear_expressions/nonlinear-guard-xd-semantic-error.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-guard-xd-semantic-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in guards (non-linear PXD semantic error)',
		'input_files': ['nonlinear_expressions/nonlinear-guard-pxd-semantic-error.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-guard-pxd-semantic-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (non-linear D reachable)',
		'input_files': ['nonlinear_expressions/nonlinear-invariant-d-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-invariant-d-reachable.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (non-linear PD reachable)',
		'input_files': ['nonlinear_expressions/nonlinear-invariant-pd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-invariant-pd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
 10 > p1
& p1 > 0
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (non-linear XD reachable)',
		'input_files': ['nonlinear_expressions/nonlinear-invariant-xd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-invariant-xd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (non-linear PXD reachable)',
		'input_files': ['nonlinear_expressions/nonlinear-invariant-pxd-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-invariant-pxd-reachable.res' , 'content' : """
BEGIN CONSTRAINT
 p1 > 0
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (non-linear PD semantic error)',
		'input_files': ['nonlinear_expressions/nonlinear-invariant-pd-semantic-error.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-invariant-pd-semantic-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (non-linear XD semantic error)',
		'input_files': ['nonlinear_expressions/nonlinear-invariant-xd-semantic-error.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-invariant-xd-semantic-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test expression consistency in invariants (non-linear PXD semantic error)',
		'input_files': ['nonlinear_expressions/nonlinear-invariant-pxd-semantic-error.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'nonlinear-invariant-pxd-semantic-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test linear expression unary minus in guard (computing)',
		'input_files': ['linear_expressions/unary-minus-linear-expression.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'unary-minus-linear-expression.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test linear expression unary minus in guard (printing)',
		'input_files': ['linear_expressions/unary-minus-linear-expression.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'unary-minus-linear-expression-regenerated.imi' , 'content' : """
when  y + 7 > 2*x
& x + y = 5 + i
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test arithmetic expression unary minus in guard (computing)',
		'input_files': ['arithmetic_expressions/unary-minus-guard.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'unary-minus-guard.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test arithmetic expression unary minus in guard (printing)',
		'input_files': ['arithmetic_expressions/unary-minus-guard.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'unary-minus-guard-regenerated.imi' , 'content' : """
when  -(i * 2) = -2 * i
& -(i * -2) = 2 * i
& -(i / 2) = (-i) / 2
& -(i / -2) = i / 2
& -(i + i) = -2 * i
& -(i - i) = 0
& -(2 * i - i) = -i
& -(-(i)) = i
& -(-(-(i))) = i do {}  sync a goto lend;
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test arithmetic expression unary minus in update (printing)',
		'input_files': ['arithmetic_expressions/unary-minus-update.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'unary-minus-update-regenerated.imi' , 'content' : """
when  i = 0 do {i := -(i * 2), i := -2 * i, i := -(i * -2), i := -(i / 2), i := (-i) / 2, i := -(i / -2), i := -(i + i), i := -(i - i), i := -(2 * i - i), i := -(-(i)), i := -(-(-(i))), i := -1 + 1, i := -1 - 1}  sync a goto lend;
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test arithmetic expression with parenthesis (printing)',
		'input_files': ['arithmetic_expressions/arithmetic-expr-printing-1.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'arithmetic-expr-printing-1-regenerated.imi' , 'content' : """
when  z * x / y > x do {}  sync a1 goto lend;
        when  z / (x * y) > x do {}  sync a1 goto lend;
        when  z / (x - y) > x do {}  sync a1 goto lend;
        when  z / (x + y) > x do {}  sync a1 goto lend;
        when  z * (x - y) > x do {}  sync a1 goto lend;
        when  z * (x + y) > x do {}  sync a1 goto lend;
        when  (x - y) / z > x do {}  sync a1 goto lend;
        when  (x + y) / z > x do {}  sync a1 goto lend;
        when  (x - y) * z > x do {}  sync a1 goto lend;
        when  (x + y) * z > x do {}  sync a1 goto lend;
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/02/10
		## Last modified            : 2021/02/10
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test arithmetic expression without parenthesis (printing)',
		'input_files': ['arithmetic_expressions/arithmetic-expr-printing-2.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'arithmetic-expr-printing-2-regenerated.imi' , 'content' : """
when  z * x / y > x do {}  sync a1 goto lend;
        when  z / x * y > x do {}  sync a1 goto lend;
        when  z / x - y > x do {}  sync a1 goto lend;
        when  z / x + y > x do {}  sync a1 goto lend;
        when  z * x - y > x do {}  sync a1 goto lend;
        when  z * x + y > x do {}  sync a1 goto lend;
        when  x - y / z > x do {}  sync a1 goto lend;
        when  x + y / z > x do {}  sync a1 goto lend;
        when  x - y * z > x do {}  sync a1 goto lend;
        when  x + y * z > x do {}  sync a1 goto lend;
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	# BEGIN : Test boolean expressions
	#------------------------------------------------------------

	#------------------------------------------------------------
	{
		'purpose'    : 'Test boolean True constant (computing)',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/bool-constant-reachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'bool-constant-reachable.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test boolean False constant (computing)',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/bool-constant-unreachable.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'bool-constant-unreachable.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test boolean negation (computing)',
		'tags':'boolean, computing, semantic',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/bool-negation.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'bool-negation.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test that a boolean variable is correctly updated (computing)',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/bool-discrete-var-update.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'bool-discrete-var-update.res' , 'content' : """
BEGIN CONSTRAINT
True
END CONSTRAINT
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test boolean variable update conversion to Uppaal (printing)',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/bool-discrete-var-update.imi'],
		'options'    : '-imi2Uppaal',
		'expectations' : [
			{'file': 'bool-discrete-var-update-uppaal.xml' , 'content' : """
/* Discrete variables declarations (WARNING: these variables can be rational-valued in IMITATOR, but they become integer-valued in Uppaal) */
bool b = true;

/* Action declarations */



	/*------------------------------------------------------------*/
	/* Initial constraint (not interpreted by Uppaal)             */
	/*------------------------------------------------------------*/
	 /* true */
</declaration>

<template><name x="0" y="0">pta</name><declaration>// No local declaration for automaton 'pta'
</declaration>
 
<location id="id_pta0_loc0" x="0" y="0">
	<name x="0" y="-40">l1</name>
	<label kind="invariant" x="0" y="40"></label></location>
 
<location id="id_pta0_loc1" x="200" y="0">
	<name x="200" y="-40">l2</name>
	<label kind="invariant" x="200" y="40"></label></location>
 
<location id="id_pta0_loc2" x="400" y="0">
	<name x="400" y="-40">lend</name>
	<label kind="invariant" x="400" y="40"> b</label></location>
 <init ref="id_pta0_loc0"/>
 
	<transition>
		<source ref="id_pta0_loc0"/>
		<target ref="id_pta0_loc1"/>
		<label kind="guard" x="100" y="40"> b</label>
		<label kind="assignment" x="100" y="-40">b = false</label>
	</transition>
	<transition>
		<source ref="id_pta0_loc1"/>
		<target ref="id_pta0_loc2"/>
		<label kind="guard" x="300" y="40"> (! (b))</label>
		<label kind="assignment" x="300" y="-40">b = 1 &lt; 2</label>
	</transition>
 </template>
<system>
// List one or more processes to be composed into a system.

system pta;
</system></nta>
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test that a boolean constant is initialized with consistant type',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/bool-constant-init-type-error.imi'],
		'options'    : '',
		'expectations' : [
			{'file': 'bool-constant-init-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test that a boolean variable is initialized with consistant type',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/bool-variable-init-type-error.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'bool-variable-init-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/11
		## Last modified            : 2021/03/11
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a boolean variable is updated with a consistent typed expression',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/bool-variable-update-type-error.imi', 'acceptingReachable.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'bool-variable-update-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

    #------------------------------------------------------------
    {
        ## Test version             : 1
        ## Test since               : 2021/05/12
        ## Last modified            : 2021/05/31
        ## Test for IMITATOR version: 3.1.0
        ## Author 					: lbinria
        'purpose'    : 'Test that "not" boolean operator is effective and correct (computing)',
		'tags':'boolean, computing, semantic',
        'input_files': ['boolean_expressions/not-operator.imi'],
        'options'    : '-mode statespace -states-description',
        'expectations' : [
            {'file': 'not-operator-statespace.states' , 'content' : """
  /************************************************************/
  STATE 1:
  pta: lend, b1 = False, b2 = True ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
		"""
             } # end result file
            ,
        ] # end expectations
    } # end test case
    #------------------------------------------------------------

    ,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/31
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test a complex boolean comparison (computing)',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/complex-bool-comparison.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'complex-bool-comparison-statespace.states' , 'content' : """
  /************************************************************/
  STATE 1:
  pta: l1, b1 = True, b2 = False ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 2:
  pta: lend, b1 = True, b2 = False ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/31
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test logical operator priority (computing)',
		'tags':'boolean, computing, semantic',
		'input_files': ['boolean_expressions/logical-operator-priority.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'logical-operator-priority-statespace.states' , 'content' : """
  /************************************************************/
  STATE 1:
  pta: l2, b1 = False, b2 = True ==> 
& x > 5 + p
& p >= 0

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "a1"
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	# END : Test boolean expressions
	#------------------------------------------------------------

	#------------------------------------------------------------
	# BEGIN : Test type checking
	#------------------------------------------------------------

	# BEGIN : Test type checking on constant declarations

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/12
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a constant is not initialized with a rational literal',
		'tags' : 'type checking, semantic, constants, declarations',
		'input_files': ['type_checking/constants_declarations/constant-int-divide-type-error.imi'],
		'options'    : '',
		'expectations' : [
			{'file': 'constant-int-divide-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/12
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that constant declaration is type checked',
		'tags' : 'type checking, semantic, constants, declarations',
		'input_files': ['type_checking/constants_declarations/constant-declaration-bad-type-error.imi'],
		'options'    : '',
		'expectations' : [
			{'file': 'constant-declaration-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	# END : Test type checking on constant declarations

	# BEGIN : Test type checking on updates

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/12
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.0.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that update of an int variable by a literal rational is forbidden',
		'tags': 'type checking, update',
		'input_files': ['type_checking/updates/update-variable-bad-type-error.imi'],
		'options'    : '',
		'expectations' : [
			{'file': 'update-variable-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/04/02
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.0.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a clock isn’t updated with a bad type',
		'tags': 'type checking, update',
		'input_files': ['type_checking/updates/clock-update-type-error.imi'],
		'options'    : '-no-var-autoremove',
		'expectations' : [
			{'file': 'clock-update-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	# END : Test type checking on updates


	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/12
		## Last modified            : 2021/03/12
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that an update expression doesn’t mix different types in addition',
		'input_files': ['type_checking/expression-mixin-type-error-1.imi'],
		'options'    : '',
		'expectations' : [
			{'file': 'expression-mixin-type-error-1.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/12
		## Last modified            : 2021/03/12
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that an update expression doesn’t mix different types in multiplication',
		'input_files': ['type_checking/expression-mixin-type-error-2.imi'],
		'options'    : '',
		'expectations' : [
			{'file': 'expression-mixin-type-error-2.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/12
		## Last modified            : 2021/03/12
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that an update expression doesn’t mix different types in comparison',
		'input_files': ['type_checking/expression-mixin-type-error-3.imi'],
		'options'    : '-no-var-autoremove',
		'expectations' : [
			{'file': 'expression-mixin-type-error-3.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/12
		## Last modified            : 2021/03/12
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that an update expression doesn’t mix different types in "in" expression',
		'input_files': ['type_checking/expression-mixin-type-error-4.imi'],
		'options'    : '',
		'expectations' : [
			{'file': 'expression-mixin-type-error-4.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	# BEGIN : Type checking complex tests

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/27
		## Last modified            : 2021/05/27
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test type checking by making a lot of complex operations on multiple types',
		'input_files': ['type_checking/complex-type-checking.imi'],
		'tags':'type checking',
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'complex-type-checking-statespace.states' , 'content' : """
  INITIAL
  STATE 0:
  pta: l1, b1 = True, b2 = False, k = 0, j = 1, i = 0 ==> 
& x >= 0
& p >= 0

  Projection onto the parameters:
   p >= 0
		"""
			 } # end result file
			,
			{'file': 'complex-type-checking-statespace.states' , 'content' : """
  STATE 23:
  pta: l2, b1 = False, b2 = True, k = 10, j = 0, i = 1 ==> 
& x >= 0
& p > 10

  Projection onto the parameters:
   p > 10
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	# END : Type checking complex test

	# BEGIN : Type checking on variable initializations

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/12
		## Last modified            : 2021/04/14
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a variable is not initialized with a rational literal',
		'tags': 'type checking, init',
		'input_files': ['type_checking/inits/variable-int-divide-type-error.imi'],
		'options'    : '-no-var-autoremove',
		'expectations' : [
			{'file': 'variable-int-divide-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/28
		## Last modified            : 2021/05/28
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a variable of type X cannot be initialized by an expression of type Y',
		'input_files': ['type_checking/inits/init-discrete-bad-type-error.imi'],
		'tags': 'type checking, init',
		'options'    : '',
		'expectations' : [
			{'file': 'init-discrete-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/28
		## Last modified            : 2021/05/28
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a init expression cannot be ill-typed',
		'input_files': ['type_checking/inits/init-discrete-expression-bad-type-error.imi'],
		'tags': 'type checking, init',
		'options'    : '',
		'expectations' : [
			{'file': 'init-discrete-expression-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/28
		## Last modified            : 2021/05/28
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a init expression cannot mix different types',
		'input_files': ['type_checking/inits/init-discrete-expression-mixin-type-error.imi'],
		'tags': 'type checking, init',
		'options'    : '',
		'expectations' : [
			{'file': 'init-discrete-expression-mixin-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/28
		## Last modified            : 2021/05/28
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a init constraint on clock cannot use non rational valued variable(s) or constant(s)',
		'tags': 'type checking, init',
		'input_files': ['type_checking/inits/init-continuous-clock-type-error.imi'],
		'options'    : '-no-var-autoremove',
		'expectations' : [
			{'file': 'init-continuous-clock-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/28
		## Last modified            : 2021/05/28
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a init constraint on parameter cannot use non rational valued variable(s) or constant(s)',
		'tags':'type checking, init',
		'input_files': ['type_checking/inits/init-continuous-parameter-type-error.imi'],
		'options'    : '-no-var-autoremove',
		'expectations' : [
			{'file': 'init-continuous-parameter-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/27
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test init a variable with a complex expression',
		'input_files': ['type_checking/inits/init-expression-complex.imi'],
		'tags': 'type checking, init',
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'init-expression-complex-statespace.states' , 'content' : """
  STATE 1:
  pta: lend, b = True, r2 = 7/3 ==> 
& 3*p > 7

  Projection onto the parameters:
   3*p > 7
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

# TODO benjamin remove, we can now use int in continuous init
# 	#------------------------------------------------------------
# 	{
# 		## Test version             : 1
# 		## Test since               : 2021/06/21
# 		## Last modified            : 2021/06/21
# 		## Test for IMITATOR version: 3.1.0
# 		## Author 					: lbinria
# 		'author': 'lbinria',
# 		'purpose'    : 'Test that init of non rational valued discrete variables in continuous init section raise an error',
# 		'input_files': ['type_checking/inits/init-non-rational-discrete-in-continuous-error.imi'],
# 		'tags': 'type checking, init',
# 		'options'    : '',
# 		'expectations' : [
# 			{'file': 'init-non-rational-discrete-in-continuous-error.res' , 'content' : """
# Error                                   : invalid model
# 		"""
# 			 } # end result file
# 			,
# 		] # end expectations
# 	} # end test case
# 	#------------------------------------------------------------
#
# 	,

	# END : Type checking on variable initializations

	# BEGIN : Type checking on conditional clauses

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/12
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that the use of a bad typed expression in conditional expression is forbidden',
		'input_files': ['type_checking/conditionals/conditional-expression-bad-type-error.imi'],
		'tags':'type checking, conditional',
		'options'    : '',
		'expectations' : [
			{'file': 'conditional-expression-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	# END : Type checking on conditional clauses

	# BEGIN : Type checking on guards tests

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a term cannot compute on a bad type',
		'input_files': ['type_checking/guards/term-bad-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'term-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a term cannot mix of different types',
		'input_files': ['type_checking/guards/term-mixin-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'term-mixin-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a factor cannot mix of different types',
		'input_files': ['type_checking/guards/factor-mixin-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'factor-mixin-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a factor cannot compute on a bad type',
		'input_files': ['type_checking/guards/factor-bad-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'factor-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a comparison cannot compute on a bad type',
		'input_files': ['type_checking/guards/compare-operator-bad-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'compare-operator-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a comparison cannot mix different types',
		'input_files': ['type_checking/guards/compare-operator-mixin-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'compare-operator-mixin-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a "in" expression cannot compute on a bad type',
		'input_files': ['type_checking/guards/in-operator-bad-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'in-operator-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a "in" expression cannot mix different types',
		'input_files': ['type_checking/guards/in-operator-mixin-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'in-operator-mixin-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a logical expression cannot compute on a bad type (other than bool)',
		'input_files': ['type_checking/guards/logical-operator-bad-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'logical-operator-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a "not" expression cannot compute on a bad type (other than bool)',
		'input_files': ['type_checking/guards/not-operator-bad-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'not-operator-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a "rational_of_int" function cannot compute on a bad type',
		'input_files': ['type_checking/guards/rational-of-int-bad-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'rational-of-int-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/25
		## Last modified            : 2021/05/25
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that a "rational_of_int" function cannot mix different types',
		'input_files': ['type_checking/guards/rational-of-int-mixin-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'rational-of-int-mixin-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/06/07
		## Last modified            : 2021/06/07
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that use of a rational expression as exponent in "pow" function raise an error',
		'input_files': ['type_checking/guards/pow-exponent-bad-type-error.imi'],
		'tags':'type checking',
		'options'    : '',
		'expectations' : [
			{'file': 'pow-exponent-bad-type-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	# END : Type checking on guards tests

	#------------------------------------------------------------
	# END : Test type checking
	#------------------------------------------------------------

	#------------------------------------------------------------
	# BEGIN : Test custom function
	#------------------------------------------------------------

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/06/07
		## Last modified            : 2021/06/07
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that behavior of pow function is correct',
		'input_files': ['functions/pow.imi'],
		'tags': 'semantic, behavior, function',
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'pow-statespace.states' , 'content' : """
  /************************************************************/
  INITIAL
  STATE 0:
  pta: l1, r1 = 3, r2 = 4, projected_result_1 = 0, projected_result_2 = 0, n = 0, i = 3, j = 4 ==> 
& p1 >= 0

  Projection onto the parameters:
   p1 >= 0

  /************************************************************/
  STATE 1:
  pta: l1, r1 = 3, r2 = 4, projected_result_1 = 82, projected_result_2 = 65, n = 1, i = 3, j = 4 ==> 
& p1 >= 0

  Projection onto the parameters:
   p1 >= 0

  /************************************************************/
  STATE 2:
  pta: l1, r1 = 3, r2 = 4, projected_result_1 = 82, projected_result_2 = 65, n = 2, i = 3, j = 4 ==> 
& p1 >= 0

  Projection onto the parameters:
   p1 >= 0

  /************************************************************/
  STATE 3:
  pta: lend, r1 = 3, r2 = 4, projected_result_1 = 82, projected_result_2 = 65, n = 3, i = 3, j = 4 ==> 
& p1 = 82
& p2 = 65

  Projection onto the parameters:
   p1 = 82
& p2 = 65
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/06/30
		## Last modified            : 2021/06/30
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that behaviors of all possible functions on binary word are correct ',
		'input_files': ['functions/binary-word.imi'],
		'tags': 'semantic, behavior, function',
		'options'    : '-mode statespace -states-description -no-var-autoremove',
		'expectations' : [
			{'file': 'binary-word-statespace.states' , 'content' : """
  /************************************************************/
  INITIAL
  STATE 0:
  pta: loc_init, r = 0, i = 0, j = 0, bin_result2 = 0b00000000, bin1 = 0b10101, bin2 = 0b10110, bin_result = 0b00000 ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 1:
  pta: loc_land, r = 0, i = 0, j = 0, bin_result2 = 0b00000000, bin1 = 0b10101, bin2 = 0b10110, bin_result = 0b10100 ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 2:
  pta: loc_lor, r = 0, i = 0, j = 0, bin_result2 = 0b00000000, bin1 = 0b10101, bin2 = 0b10110, bin_result = 0b10111 ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 3:
  pta: loc_lxor, r = 0, i = 0, j = 0, bin_result2 = 0b00000000, bin1 = 0b10101, bin2 = 0b10110, bin_result = 0b00011 ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 4:
  pta: loc_lnot, r = 0, i = 0, j = 0, bin_result2 = 0b00000000, bin1 = 0b10101, bin2 = 0b10110, bin_result = 0b01010 ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 5:
  pta: loc_shift_left, r = 0, i = 0, j = 0, bin_result2 = 0b00000000, bin1 = 0b10101, bin2 = 0b10110, bin_result = 0b10100 ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 6:
  pta: loc_shift_right, r = 0, i = 0, j = 0, bin_result2 = 0b00000000, bin1 = 0b10101, bin2 = 0b10110, bin_result = 0b00101 ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 7:
  pta: loc_fill_left, r = 0, i = 0, j = 0, bin_result2 = 0b10101000, bin1 = 0b10101, bin2 = 0b10110, bin_result = 0b00101 ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 8:
  pta: loc_fill_right, r = 0, i = 0, j = 0, bin_result2 = 0b00010101, bin1 = 0b10101, bin2 = 0b10110, bin_result = 0b00101 ==> 
&True

  Projection onto the parameters:
  True

  /************************************************************/
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	# END : Test custom function
	#------------------------------------------------------------

	#------------------------------------------------------------
	{
		'purpose'    : 'Test updates (state space)',
		'input_files': ['testUpdates.imi'],
		'options'    : '-mode statespace -depth-limit 4 -states-description',
		'expectations' : [
			{'file': 'testUpdates-statespace.states' , 'content' : """

  /************************************************************/
  INITIAL
  STATE 0:
  autom: idle, i = 1 ==>
& p >= 0
& x = 0
& y = 0

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  STATE 1:
  autom: idle, i = 2/5 ==>
& p >= 0
& 5*p = 38 + 10*x
& y = 1

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  STATE 2:
  autom: idle, i = 1/4 ==>
& p >= 0
& 20*p = 131 + 20*x
& y = 2

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  STATE 3:
  autom: idle, i = -4/5 ==>
& p >= 0
& 30*p = 39 + 20*x
& y = 3

  Projection onto the parameters:
   p >= 0
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/14
		# Last modified            : 2020/09/14
		# Test for IMITATOR version: 3
		'purpose'    : 'Test stopwatches',
		'input_files': ['testStopwatches.imi', 'testStopwatches.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testStopwatches.res' , 'content' : """
BEGIN CONSTRAINT
p = 10
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/17
		# Last modified            : 2020/09/17
		# Test for IMITATOR version: 3
		'purpose'    : 'Test flows',
		'input_files': ['testFlows.imi', 'testFlows.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testFlows.res' , 'content' : """
BEGIN CONSTRAINT
p = 2046
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test clock elimination',
		'input_files': ['loopingTAdyn.imi'],
		'options'    : '-mode statespace -dynamic-elimination -states-description -depth-limit 10', # NOTE: depth-limit is just a safety to avoid yielding a loop if the test fails!
		'expectations' : [
			{'file': 'loopingTAdyn-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: l0 ==>
&True

  Projection onto the parameters:
  True

  /************************************************************/
  STATE 1:
  pta: l1 ==>
& x >= 0

  Projection onto the parameters:
  True

  /************************************************************/
DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1
  s_1 -> s_1 via "a"
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test EF (old version) with bad initial state',
		#'input_files': ['testEFdegenerate1.imi', 'testEFdegenerate1.imiprop'],
		#'options'    : '-merge -incl ',
		#'expectations' : [
			#{'file': 'testEFdegenerate1.res' , 'content' : """
#BEGIN CONSTRAINT
 #p2 >= 0
#& p1 >= 0
#END CONSTRAINT

#------------------------------------------------------------
#Constraint soundness                    : exact
#Termination                             : regular termination
#Constraint nature                       : good
#------------------------------------------------------------
#Number of states                        : 0
#Number of transitions                   : 0
#Number of computed states               : 0
#"""
			#} #end result file
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------

	#,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with bad initial state',
		'input_files': ['testEFdegenerate1.imi', 'testEFdegenerate1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFdegenerate1.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Number of states                        : 0
Number of transitions                   : 0
Number of computed states               : 0
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test EF (old version) with bad initial state and some constrained valuations',
		#'input_files': ['testEFdegenerate2.imi'],
		#'options'    : '-mode EFold -merge -incl ',
		#'expectations' : [
			#{'file': 'testEFdegenerate2.res' , 'content' : """
#BEGIN CONSTRAINT
 #p1 >= p2
#& p2 >= 0
#END CONSTRAINT

#------------------------------------------------------------
#Constraint soundness                    : exact
#Termination                             : regular termination
#Constraint nature                       : good
#------------------------------------------------------------
#Number of states                        : 0
#Number of transitions                   : 0
#Number of computed states               : 0
#"""
			#} #end result file
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------

	#,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with bad initial state and some constrained valuations',
		'input_files': ['testEFdegenerate2.imi', 'testEFdegenerate2.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFdegenerate2.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Number of states                        : 0
Number of transitions                   : 0
Number of computed states               : 0
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with the new syntax from 2.10.1',
		'input_files': ['fischer_2.imi', 'fischer_2.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'fischer_2.res' , 'content' : """
BEGIN CONSTRAINT
 a >= 0
& b > a
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test EF (old version) with basic safety property for Fischer:3',
		#'input_files': ['F3.imi'],
		#'options'    : '-mode EFold -merge -incl ',
		#'expectations' : [
			#{'file': 'F3.res' , 'content' : """
#BEGIN CONSTRAINT
 #Delta > delta
#& delta >= 0
 #OR
 #Delta > 2*delta
#& delta >= 0
#END CONSTRAINT
#"""
			#} #end result file
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------
	#,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EF on toy example: witness',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge-witness.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : terminated after reaching a target state (some states may have been unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EF on toy example: synthesis',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
OR
  5 > p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EF on toy example: synthesis (syntax without parentheses)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge-noparen.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
OR
  5 > p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EF on toy example: synthesis (-output-prefix)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge.imiprop'],
		'options'    : '-output-prefix mypersonnalizedprefix',
		'expectations' : [
			{'file': 'mypersonnalizedprefix.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
OR
  5 > p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EF on toy example: synthesis (explicit -merge -comparison inclusion)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge.imiprop'],
		'options'    : '-merge -comparison inclusion',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
OR
  5 > p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EF on toy example: synthesis (-no-merge)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge.imiprop'],
		'options'    : '-no-merge',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
OR
  5 > p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EF on toy example: synthesis (-no-merge -comparison equality)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge.imiprop'],
		'options'    : '-no-merge -comparison equality',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
OR
  5 > p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	# TODO: merge without inclusion (for now: loops forever)

	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EF on toy example: synthesis (-no-merge -comparison equality -no-cumulative-pruning)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge.imiprop'],
		'options'    : '-no-merge -comparison equality -no-cumulative-pruning',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
OR
  5 > p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with basic safety property for Fischer:3',
		'input_files': ['F3.imi', 'F3.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'F3.res' , 'content' : """
BEGIN CONSTRAINT
delta >= Delta
    & Delta >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with basic safety property for Fischer:3 (double-directional inclusion)',
		'input_files': ['F3.imi', 'F3.imiprop'],
		'options'    : '-merge -comparison doubleinclusion',
		'expectations' : [
			{'file': 'F3.res' , 'content' : """
BEGIN CONSTRAINT
delta >= Delta
    & Delta >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with basic safety property for Fischer:3 (queueBFS exploration order)',
		'input_files': ['F3.imi', 'F3.imiprop'],
		'options'    : '-expl-order queueBFS',
		'expectations' : [
			{'file': 'F3.res' , 'content' : """
BEGIN CONSTRAINT
delta >= Delta
    & Delta >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with basic safety property for Fischer:3 (layerBFS exploration order) with counterexample',
		'input_files': ['F3.imi', 'F3-witness.imiprop'],
		'options'    : '-expl-order layerBFS',
		'expectations' : [
			{'file': 'F3.res' , 'content' : """
BEGIN CONSTRAINT
 2*delta >= Delta
& Delta >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible over-approximation
Termination                             : terminated after reaching a target state (some states may have been unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with basic safety property for Fischer:3 (queueBFS exploration order) with counterexample',
		'input_files': ['F3.imi', 'F3-witness.imiprop'],
		'options'    : '-expl-order queueBFS',
		'expectations' : [
			{'file': 'F3.res' , 'content' : """
BEGIN CONSTRAINT
 2*delta >= Delta
& Delta >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible over-approximation
Termination                             : terminated after reaching a target state (some states may have been unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test EF (old version) with complex safety property',
		#'input_files': ['coffeeDrinker.imi'],
		#'options'    : '-mode EFold -merge ',
		#'expectations' : [
			#{'file': 'coffeeDrinker.res' , 'content' : """
#BEGIN CONSTRAINT
 #15 >= p_add_sugar
#& p_button > 0
#& p_add_sugar + p_coffee >= 15
#& p_add_sugar >= 3*p_button
#& p_coffee > 0
 #OR
 #p_add_sugar + p_coffee >= 15
#& p_button >= 5
#& 15 >= p_add_sugar
#& p_coffee > 0
#& p_add_sugar >= 2*p_button
 #OR
 #3*p_button >= p_add_sugar + p_coffee
#& p_add_sugar >= 2*p_button
#& 15 >= p_add_sugar + p_coffee
#& p_coffee > 0
 #OR
 #5 >= p_button
#& p_button > 0
#& p_add_sugar >= 15
#& p_coffee > 0
 #OR
 #15 >= 2*p_button
#& p_button >= 5
#& p_add_sugar >= 15
#& p_coffee > 0
 #OR
 #p_add_sugar + p_coffee >= 15
#& p_add_sugar >= p_button
#& 15 >= p_add_sugar
#& p_coffee > 0
#& 2*p_button >= 15
 #OR
 #p_add_sugar >= p_button
#& p_coffee > 0
#& 15 >= p_add_sugar + p_coffee
#& 2*p_button >= p_add_sugar + p_coffee
 #OR
 #p_coffee > 0
#& 15 >= p_add_sugar
#& p_add_sugar > 0
#& p_add_sugar + p_coffee >= 15
#& p_button >= 15
 #OR
 #p_add_sugar > 0
#& 15 >= p_add_sugar + p_coffee
#& p_coffee > 0
#& p_button >= p_add_sugar + p_coffee
 #OR
 #2*p_button >= 15
#& 15 >= p_button
#& p_add_sugar >= 15
#& p_coffee > 0
 #OR
 #p_button >= 15
#& p_coffee > 0
#& p_add_sugar >= 15
#END CONSTRAINT
#"""
			#} #end result file
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------
	#,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with complex safety property',
		'input_files': ['coffeeDrinker.imi', 'coffeeDrinker.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'coffeeDrinker.res' , 'content' : """
BEGIN CONSTRAINT
 p_add_sugar > 0
& 2*p_button > p_add_sugar
& p_add_sugar + p_coffee > 2*p_button
& 15 > 2*p_button
OR
  p_add_sugar >= 2*p_button
& p_add_sugar + p_coffee > 3*p_button
& 3*p_button > p_add_sugar
& 5 > p_button
OR
  p_add_sugar > 0
& 2*p_button >= 15
& p_add_sugar + p_coffee > 15
& 15 > p_button
& p_button > p_add_sugar
OR
  2*p_button >= p_add_sugar + p_coffee
& p_add_sugar > 0
& p_add_sugar + p_coffee > p_button
& p_button > p_add_sugar
& 15 >= p_add_sugar + p_coffee
OR
  15 > p_add_sugar + p_coffee
& p_coffee > 0
& p_button > 0
& 5 > p_button
& p_add_sugar >= 3*p_button
END CONSTRAINT
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/07/02
		# Last modified            : 2021/07/02
		# Test for IMITATOR version: 3.1
		'purpose'    : 'Test EF with a parameter not used in the model (but still useful) + negative clock + negative flow',
		'tags' : 'auto remove',
		'input_files': ['test_param_unused.imi' , 'EFaccepting.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'test_param_unused.res' , 'content' : """
BEGIN CONSTRAINT
 14 > p
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with complex safety property on coffee drinker with int',
		'input_files': ['coffeeDrinker-int.imi', 'coffeeDrinker.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'coffeeDrinker-int.res' , 'content' : """
BEGIN CONSTRAINT
 p_add_sugar > 0
& 2*p_button > p_add_sugar
& p_add_sugar + p_coffee > 2*p_button
& 15 > 2*p_button
OR
  p_add_sugar >= 2*p_button
& p_add_sugar + p_coffee > 3*p_button
& 3*p_button > p_add_sugar
& 5 > p_button
OR
  p_add_sugar > 0
& 2*p_button >= 15
& p_add_sugar + p_coffee > 15
& 15 > p_button
& p_button > p_add_sugar
OR
  2*p_button >= p_add_sugar + p_coffee
& p_add_sugar > 0
& p_add_sugar + p_coffee > p_button
& p_button > p_add_sugar
& 15 >= p_add_sugar + p_coffee
OR
  15 > p_add_sugar + p_coffee
& p_coffee > 0
& p_button > 0
& 5 > p_button
& p_add_sugar >= 3*p_button
END CONSTRAINT
"""
			 } #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test EF (old version) with observer + depth-limit + project-result (quite basic)',
		#'input_files': ['coffeeDrinker-within.imi'],
		#'options'    : '-mode EFold -merge -depth-limit 10 ',
		#'expectations' : [
			#{'file': 'coffeeDrinker-within.res' , 'content' : """
#BEGIN CONSTRAINT
 #p_coffee > 0
#END CONSTRAINT
#"""
			#} # end result file
			#,
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------
	
	#,
	
	#------------------------------------------------------------
	{
		'purpose'    : 'Test EF with observer + depth-limit + project-result (quite basic)',
		'input_files': ['coffeeDrinker.imi', 'coffeeDrinker-within.imiprop'],
		'options'    : '-depth-limit 10',
		'expectations' : [
			{'file': 'coffeeDrinker.res' , 'content' : """
BEGIN CONSTRAINT
 False
END CONSTRAINT
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/04
		# Test for IMITATOR version: 3.0
		'purpose'    : 'Test EF (difference between emptiness and synthesis, here emptiness)',
		'input_files': ['testEFemptiness.imi', 'testEFemptiness-empt.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFemptiness.res' , 'content' : """
BEGIN CONSTRAINT
 p = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : terminated after reaching a target state (some states may have been unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/04
		# Last modified            : 2020/09/04
		# Test for IMITATOR version: 3.0
		'purpose'    : 'Test EF (difference between emptiness and synthesis, here synthesis)',
		'input_files': ['testEFemptiness.imi', 'testEFemptiness-synth.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFemptiness.res' , 'content' : """
BEGIN CONSTRAINT
 p = 1
 OR
 p >= 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/22
		# Last modified            : 2020/09/22
		# Test for IMITATOR version: 3.0
		'purpose'    : 'Test EF (without option -no-cumulative-pruning)',
		'input_files': ['testInclusionEF.imi', 'testInclusionEF-EF.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testInclusionEF.res' , 'content' : """
BEGIN CONSTRAINT
 5 >= p
& p >= 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Number of states                        : 3
Number of transitions                   : 2
Number of computed states               : 3
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/22
		# Last modified            : 2020/09/22
		# Test for IMITATOR version: 3.0
		'purpose'    : 'Test EF (with option -no-cumulative-pruning)',
		'input_files': ['testInclusionEF.imi', 'testInclusionEF-EF.imiprop'],
		'options'    : '-no-cumulative-pruning',
		'expectations' : [
			{'file': 'testInclusionEF.res' , 'content' : """
BEGIN CONSTRAINT
 5 >= p
& p >= 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Number of states                        : 14
Number of transitions                   : 13
Number of computed states               : 14
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/05/30
		# Test for IMITATOR version: 2.11
		'purpose'    : 'Test EFunsafe',
		'input_files': ['testEFcounterex.imi', 'testEFcounterex.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFcounterex.res' , 'content' : """
BEGIN CONSTRAINT
 p = 1
 OR
 p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2019/05/30
		# Test for IMITATOR version: 2.11
		'purpose'    : 'Test EFunsafe with counterexample',
		'input_files': ['testEFcounterex.imi', 'testEFcounterex-witness.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFcounterex.res' , 'content' : """
BEGIN CONSTRAINT
 p = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : terminated after reaching a target state (some states may have been unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "if a2 then a1 has happened before"',
		'input_files': ['testPattern1.imi', 'testPattern1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern1.res' , 'content' : """
BEGIN CONSTRAINT
 2 >= p1
& p1 >= 0
& p2 >= 0
& p2 + 1 >= p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "if a2 then a1 has happened before" on a model for 3 patterns',
		'input_files': ['testPattern2.imi', 'testPattern2-if.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern2.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 0
& 1 > p
OR
  p > 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "everytime a2 then a1 has happened before" on a model for 3 patterns',
		'input_files': ['testPattern2.imi', 'testPattern2-everytime.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern2.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 0
& 1 > p
OR
  p > 3
OR
  p > 2
& 3 > p
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "everytime a2 then a1 has happened once before" on a model for 3 patterns',
		'input_files': ['testPattern2.imi', 'testPattern2-everytimeonce.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern2.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 0
& 1 > p
OR
  p > 5
OR
  p > 3
& 5 > p
OR
  p > 2
& 3 > p
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	# WARNING: the expected result is different from the (mathematically) sound result, due to a time-lock; observer patterns are incorrect in presence of time-locks
	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "a within d"',
		'input_files': ['testPattern3.imi', 'testPattern3.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern3.res' , 'content' : """
BEGIN CONSTRAINT
 3 >= p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	# WARNING: the expected result is different from the (mathematically) sound result, due to a time-lock; observer patterns are incorrect in presence of time-locks
	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "a within d"',
		'input_files': ['testPattern4.imi', 'testPattern4.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern4.res' , 'content' : """
BEGIN CONSTRAINT
 p > 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "a within d" with a parametric d',
		'input_files': ['testPattern5.imi', 'testPattern5.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern5.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 3
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "if a2 then a1 has happened within d before"',
		'input_files': ['testPattern6.imi', 'testPattern6-if.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern6.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 0
& p2 >= 0
& 1 > p1
OR
  p1 > 5
& p2 >= 0
OR
  5 > p1
& p1 > 2
& p2 >= 0
OR
  p2 >= 2015
& p1 = 5
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "everytime a2 then a1 has happened within d before"',
		'input_files': ['testPattern6.imi', 'testPattern6-everytime.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern6.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 0
& p2 >= 0
& 1 > p1
OR
  p1 > 5
& p2 >= 0
OR
  p1 > 4
& p2 >= 0
& 5 > p1
OR
  p1 > 3
& p2 >= 0
& 4 > p1
OR
  p2 >= 4
& p1 = 4
OR
  p2 >= 2015
& p1 = 5
OR
  p1 > 2
& p2 >= 0
& 3 > p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "everytime a2 then a1 has happened once within d before"',
		'input_files': ['testPattern6.imi', 'testPattern6-everytimeonce.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern6.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 0
& p2 >= 0
& 1 > p1
OR
  p1 > 5
& p2 >= 0
OR
  p1 > 4
& p2 >= 0
& 5 > p1
OR
  p1 > 3
& p2 >= 0
& 4 > p1
OR
  p2 >= 4
& p1 = 4
OR
  p1 > 2
& p2 >= 0
& 3 > p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "if a1 then eventually a2 within d"',
		'input_files': ['testPattern7.imi', 'testPattern7-if.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern7.res' , 'content' : """
BEGIN CONSTRAINT
  p1 > 1
 & p2 >= p1
 OR
   p1 >= 0
 & 1 > p1
 & p2 >= p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "everytime a1 then eventually a2 within d"',
		'input_files': ['testPattern7.imi', 'testPattern7-everytime.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern7.res' , 'content' : """
BEGIN CONSTRAINT
  p1 > 1
 & 2 > p1
 & p2 >= p1
 OR
   p2 >= 3
 & p1 >= 2
 & p2 >= p1
 OR
   p1 >= 0
 & p2 >= p1
 & 1 > p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "everytime a1 then eventually a2 within d once before next"',
		'input_files': ['testPattern7.imi', 'testPattern7-everytimeonce.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern7.res' , 'content' : """
BEGIN CONSTRAINT
  p1 > 4
 & p2 >= p1
 OR
   p1 > 1
 & p2 >= p1
 & 2 > p1
 OR
   p2 >= 3
 & p1 >= 2
 & p2 >= p1
 & 4 > p1
 OR
   p1 >= 0
 & p2 >= p1
 & 1 > p1

END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "sequence a1, …, an"',
		'input_files': ['testPattern8.imi', 'testPattern8-sequence.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern8.res' , 'content' : """
BEGIN CONSTRAINT
  4 > p
 & p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test observer pattern "always sequence a1, …, an"',
		'input_files': ['testPattern8.imi', 'testPattern8-alwayssequence.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testPattern8.res' , 'content' : """
BEGIN CONSTRAINT
  p > 3
 & 4 > p
 OR
   p >= 0
 & 3 > p
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFmin on a toy example',
		'input_files': ['testEFmin.imi', 'testEFmin.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFmin.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Number of states                        : 10
Number of transitions                   : 9
Number of computed states               : 12
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFmax on a toy example',
		'input_files': ['testEFmin.imi', 'testEFmax.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFmin.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 0
& 11 >= p
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Number of states                        : 10
Number of transitions                   : 9
Number of computed states               : 20
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmin on a clock-free toy example 1',
		'input_files': ['testEFsynthminParams1.imi', 'testEFsynthminParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthminParams1.res' , 'content' : """
BEGIN CONSTRAINT
 p1 = 1
& p2 = 2
OR
  p1 = 1
& p2 = 3
OR
  p1 = 1
& p2 = 4
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmin on a clock-free toy example 2',
		'input_files': ['testEFsynthminParams2.imi', 'testEFsynthminParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthminParams2.res' , 'content' : """
BEGIN CONSTRAINT
 p1 = 1
& p2 = 2
OR
  p1 = 1
& p2 = 3
OR
  p1 = 1
& p2 = 4
OR
  p1 = 1
& p2 = 5
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmin on a clock-free toy example 3',
		'input_files': ['testEFsynthminParams3.imi', 'testEFsynthminParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthminParams3.res' , 'content' : """
BEGIN CONSTRAINT
 3*p1 > 1
& 1 > p1
& p2 = 4
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmin on a clock-free toy example 4',
		'input_files': ['testEFsynthminParams4.imi', 'testEFsynthminParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthminParams4.res' , 'content' : """
BEGIN CONSTRAINT
 3*p1 > 1
& 1 > p1
& 2*p1 = p2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmin on a clock-free toy example 5',
		'input_files': ['testEFsynthminParams5.imi', 'testEFsynthminParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthminParams5.res' , 'content' : """
BEGIN CONSTRAINT
 p1 = 0
& p2 = 4
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmin on a clock-free toy example 6',
		'input_files': ['testEFsynthminParams6.imi', 'testEFsynthminParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthminParams6.res' , 'content' : """
BEGIN CONSTRAINT
 p1 > 0
& p1 + 1 = p2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmin on a toy example',
		'input_files': ['testEFsynthmin.imi', 'testEFsynthmin.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthmin.res' , 'content' : """
BEGIN CONSTRAINT
 3 >= p2
& p2 >= 2
& p1 = 3
OR
  p1 = 3
& p2 = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmax on a clock-free toy example 1',
		'input_files': ['testEFsynthmaxParams1.imi', 'testEFsynthmaxParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthmaxParams1.res' , 'content' : """
BEGIN CONSTRAINT
 p1 = 1
& p2 = 2
OR
  p1 = 1
& p2 = 3
OR
  p1 = 1
& p2 = 4
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmax on a clock-free toy example 2',
		'input_files': ['testEFsynthmaxParams2.imi', 'testEFsynthmaxParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthmaxParams2.res' , 'content' : """

BEGIN CONSTRAINT
 p1 = 1
& p2 = 2
OR
  p1 = 1
& p2 = 3
OR
  p1 = 1
& p2 = 4
OR
  p1 = 1
& p2 = 5
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmax on a clock-free toy example 3',
		'input_files': ['testEFsynthmaxParams3.imi', 'testEFsynthmaxParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthmaxParams3.res' , 'content' : """
BEGIN CONSTRAINT
 3*p1 > 4
& 2 > p1
& p2 = 4
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmax on a clock-free toy example 4',
		'input_files': ['testEFsynthmaxParams4.imi', 'testEFsynthmaxParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthmaxParams4.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 0
& 5 > 3*p1
& 2*p1 = p2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmax on a clock-free toy example 5',
		'input_files': ['testEFsynthmaxParams5.imi', 'testEFsynthmaxParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthmaxParams5.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 1
& p2 = 3
OR
  p1 >= 2
& p2 = 5
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmax on a clock-free toy example 6',
		'input_files': ['testEFsynthmaxParams6.imi', 'testEFsynthmaxParams1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthmaxParams6.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= p2
& p1 > 0
& p2 >= 0
OR
  p1 >= 1
& p2 = 3
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFsynthmax on a toy example',
		'input_files': ['testEFsynthmax.imi', 'testEFsynthmax.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFsynthmax.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 10
& p2 >= 0
OR
  p1 >= 3
& p2 = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/04/01
		# Last modified            : 2021/04/01
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EFexemplify on a toy example with only discrete',
		'input_files': ['testEFexemplify-discrete.imi', 'testEFexemplify-discrete.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testEFexemplify-discrete.res' , 'content' : """
BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  

 Other valuations with equivalent (discrete) run:
True

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  

pta: l1, i = 0 ==> 
global_time = 0
 | 
 | via d = 1/2
 | followed by combined transition [PTA pta: guard{True} updates{i := 3}  (* sync nosync_1*)  Target l2] 
 | 
 v  pta: l2, i = 3 ==> 
global_time = 1/2

 | 
 | via d = 1/2
 | followed by combined transition [PTA pta: guard{True} updates{i := i + 1}  (* sync nosync_2*)  Target lTarget] 
 | 
 v  pta: lTarget, i = 4 ==> 
global_time = 1
(************************************************************)

END RESULT

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/04/01
		# Last modified            : 2021/04/01
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EFexemplify on a toy example with only 1 clock',
		'input_files': ['testEFexemplify-1clock.imi', 'testEFexemplify-1clock.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testEFexemplify-1clock.res' , 'content' : """
BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  

 Other valuations with equivalent (discrete) run:
True

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  

pta: l1 ==> 
x = 0 & global_time = 0
 | 
 | via d = 2
 | followed by combined transition [PTA pta: guard{ x = 2} updates{x := 0}  (* sync nosync_1*)  Target l2] 
 | 
 v  pta: l2 ==> 
x = 0 & global_time = 2

 | 
 | via d = 3
 | followed by combined transition [PTA pta: guard{ x = 3} updates{x := x}  (* sync nosync_2*)  Target lTarget] 
 | 
 v  pta: lTarget ==> 
x = 3 & global_time = 5
(************************************************************)

END RESULT

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/04/01
		# Last modified            : 2021/04/01
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EFexemplify on a toy example with only 1 clock (+ non-1 flows, non-0 resets)',
		'input_files': ['testEFexemplify-1complexclock.imi', 'testEFexemplify-1complexclock.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testEFexemplify-1complexclock.res' , 'content' : """
BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  

 Other valuations with equivalent (discrete) run:
True

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  

pta: l1 ==> 
x = 0 & global_time = 0
 | 
 | via d = 2
 | followed by combined transition [PTA pta: guard{ x = 2} updates{x := 5}  (* sync nosync_1*)  Target l2] 
 | 
 v  pta: l2 ==> 
x = 5 & global_time = 2

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ x = 8} updates{x := 2*x}  (* sync nosync_2*)  Target l3] 
 | 
 v  pta: l3 ==> 
x = 16 & global_time = 3

 | 
 | via d = 10
 | followed by combined transition [PTA pta: guard{ x = 6} updates{x := x + -3}  (* sync nosync_3*)  Target lTarget] 
 | 
 v  pta: lTarget ==> 
x = 3 & global_time = 13
(************************************************************)

END RESULT

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/04/01
		# Last modified            : 2021/04/01
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EFexemplify on a toy example with 2 clocks (+ non-1 flows, non-0 resets)',
		'input_files': ['testEFexemplify-2complexclocks.imi', 'testEFexemplify-2complexclocks.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testEFexemplify-2complexclocks.res' , 'content' : """
BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  

 Other valuations with equivalent (discrete) run:
True

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  

pta: l1 ==> 
x = 0 & y = 0 & global_time = 0
 | 
 | via d = 2
 | followed by combined transition [PTA pta: guard{ x = 2} updates{y := 5}  (* sync nosync_1*)  Target l2] 
 | 
 v  pta: l2 ==> 
x = 2 & y = 5 & global_time = 2

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ x = 5} updates{x := y, y := x}  (* sync nosync_2*)  Target l3] 
 | 
 v  pta: l3 ==> 
x = 7 & y = 5 & global_time = 3

 | 
 | via d = 1/2
 | followed by combined transition [PTA pta: guard{ x = 1} updates{y := -1*x + y}  (* sync nosync_3*)  Target lTarget] 
 | 
 v  pta: lTarget ==> 
x = 1 & y = 9/2 & global_time = 7/2
(************************************************************)

END RESULT

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/04/01
		# Last modified            : 2021/04/01
		# Test for IMITATOR version: 3
		'purpose'    : 'Test EFexemplify on a toy example with 1 clock and 2 bounded signals',
		'input_files': ['testEFexemplify-2signals.imi', 'testEFexemplify-2signals.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			# WARNING: there is a lot of non-determinism, so a failure on this test does not necessarily mean the algorithm is wrong! It should then be manually inspected
			{'file': 'testEFexemplify-2signals.res' , 'content' : """
(************************************************************)
 Run #1

 Valuation:
  

 Other valuations with equivalent (discrete) run:
True

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  

pta: l1, signal_1: increasing_slow, signal_2: increasing_slow ==> 
x = 0 & s_1 = 37/4 & s_2 = 29/8 & global_time = 0
 | 
 | via d = 1
 | followed by combined transition [PTA signal_1: guard{True} updates{}  sync stabilize_1 Target stabilized] 
 | 
 v  pta: l1, signal_1: stabilized, signal_2: increasing_slow ==> 
x = 1 & s_1 = 41/4 & s_2 = 37/8 & global_time = 1

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ s_1 > s_2
& x = 2} updates{x := 0}  (* sync nosync_1*)  Target l2] 
 | 
 v  pta: l2, signal_1: stabilized, signal_2: increasing_slow ==> 
x = 0 & s_1 = 41/4 & s_2 = 45/8 & global_time = 2

 | 
 | via d = 17/4
 | followed by combined transition [PTA pta: guard{ x > 4
& 10 > s_2} updates{}  (* sync nosync_2*)  Target l3] 
 | 
 v  pta: l3, signal_1: stabilized, signal_2: increasing_slow ==> 
x = 17/4 & s_1 = 41/4 & s_2 = 79/8 & global_time = 25/4

 | 
 | via d = 83/8
 | followed by combined transition [PTA pta: guard{ x > 20
& s_1 > 10
& s_1 + 10 = s_2} updates{}  (* sync nosync_3*)  Target lTarget] 
 | 
 v  pta: lTarget, signal_1: stabilized, signal_2: increasing_slow ==> 
x = 25 & s_1 = 41/4 & s_2 = 81/4 & global_time = 133/8
(************************************************************)

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example',
		'input_files': ['testCounterExSimple-3.imi', 'testCounterExSimple-3.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testCounterExSimple-3.res' , 'content' : """
BEGIN RESULT
(************************************************************)
 Run #1


 Valuation:
  p = 1/2

 Other valuations with equivalent (discrete) run:
 2*p = 1

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p = 1/2

pta: l1 ==> 
p = 1/2 & x = 0 & global_time = 0
 | 
 | via d = 3
 | followed by combined transition [PTA pta: guard{ 2*p = 1
& x = 3} updates{x := 0}  sync a Target ltarget] 
 | 
 v  pta: ltarget ==> 
p = 1/2 & x = 0 & global_time = 3
(************************************************************)


(************************************************************)
 Run #2

 Valuation:
  p = 0

 Other valuations with equivalent (discrete) run:
 2*p > 1
OR
  p >= 0
& 1 > 2*p

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 0

pta: l1 ==> 
p = 0 & x = 0 & global_time = 0
 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l1 ==> 
p = 0 & x = 1 & global_time = 1
(************************************************************)


(************************************************************)
 Run #3

 Valuation:
  p = 1/2

 Other valuations with equivalent (discrete) run:
 2*p = 1

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 1/2

pta: l1 ==> 
p = 1/2 & x = 0 & global_time = 0
 | 
 | via d = 0
 | followed by impossible transition labeled with a
 | 
 v  pta: ltarget ==> 
p = 1/2 & x = 0 & global_time = 0
(************************************************************)
END RESULT
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example (clock initially non-zero, strict constraints)',
		'input_files': ['testCounterExSimple-4.imi', 'testCounterExSimple-4.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testCounterExSimple-4.res' , 'content' : """
BEGIN RESULT
(************************************************************)
 Run #1


 Valuation:
  p = 4095/2

 Other valuations with equivalent (discrete) run:
 2048 > p
& p > 2047

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p = 4095/2

pta: l1 ==> 
p = 4095/2 & x = 1 & global_time = 0
 | 
 | via d = 1/2
 | followed by combined transition [PTA pta: guard{True
&  p = 2046 + x} updates{}  sync a Target ltarget] 
 | 
 v  pta: ltarget ==> 
p = 4095/2 & x = 3/2 & global_time = 1/2
(************************************************************)


(************************************************************)
 Run #2

 Valuation:
  p = 0

 Other valuations with equivalent (discrete) run:
 2047 >= p
& p >= 0
OR
  p >= 2048

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 0

pta: l1 ==> 
p = 0 & x = 1 & global_time = 0
 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l1 ==> 
p = 0 & x = 2 & global_time = 1
(************************************************************)


(************************************************************)
 Run #3

 Valuation:
  p = 4095/2

 Other valuations with equivalent (discrete) run:
 2048 > p
& p > 2047

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 4095/2

pta: l1 ==> 
p = 4095/2 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by impossible transition labeled with a
 | 
 v  pta: ltarget ==> 
p = 4095/2 & x = 1 & global_time = 0
(************************************************************)
END RESULT

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example (violation possible only in the initial state)',
		'input_files': ['testCounterExSimple-5.imi', 'testCounterExSimple-5.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testCounterExSimple-5.res' , 'content' : """
BEGIN RESULT
(************************************************************)
 Run #1

 Valuation:
  p = 1

 Other valuations with equivalent (discrete) run:
 p > 0

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p = 1

pta: l1 ==> 
p = 1 & x = 1 & global_time = 0
 | 
 | via d = 1/4
 | followed by combined transition [PTA pta: guard{ p > 0} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 1 & x = 5/4 & global_time = 1/4

 | 
 | via d = 1/4
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p = 1 & x = 3/2 & global_time = 1/2

 | 
 | via d = 1/2
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target ltarget] 
 | 
 v  pta: ltarget ==> 
p = 1 & x = 2 & global_time = 1
(************************************************************)


(************************************************************)
 Run #2

 Valuation:
  p = 0

 Other valuations with equivalent (discrete) run:
 p = 0

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 0

pta: l1 ==> 
p = 0 & x = 1 & global_time = 0
 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l1 ==> 
p = 0 & x = 2 & global_time = 1

 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l2 ==> 
p = 0 & x = 3 & global_time = 2

 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l3 ==> 
p = 0 & x = 4 & global_time = 3
(************************************************************)


(************************************************************)
 Run #3

 Valuation:
  p = 1

 Other valuations with equivalent (discrete) run:
 p > 0

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 1

pta: l1 ==> 
p = 1 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by impossible transition labeled with a
 | 
 v  pta: l2 ==> 
p = 1 & x = 1 & global_time = 0

 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l2 ==> 
p = 1 & x = 2 & global_time = 1

 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l3 ==> 
p = 1 & x = 3 & global_time = 2
(************************************************************)
END RESULT

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example (violation possible only at position 2)',
		'input_files': ['testCounterExSimple-5b.imi', 'testCounterExSimple-5b.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testCounterExSimple-5b.res' , 'content' : """
BEGIN RESULT
(************************************************************)
 Run #1

 Valuation:
  p = 1

 Other valuations with equivalent (discrete) run:
 p > 0

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p = 1

pta: l1 ==> 
p = 1 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 1 & x = 1 & global_time = 0

 | 
 | via d = 1/2
 | followed by combined transition [PTA pta: guard{ p > 0} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p = 1 & x = 3/2 & global_time = 1/2

 | 
 | via d = 1/2
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target ltarget] 
 | 
 v  pta: ltarget ==> 
p = 1 & x = 2 & global_time = 1
(************************************************************)


(************************************************************)
 Run #2

 Valuation:
  p = 0

 Other valuations with equivalent (discrete) run:
 p = 0

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 0

pta: l1 ==> 
p = 0 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 0 & x = 1 & global_time = 0
 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l2 ==> 
p = 0 & x = 2 & global_time = 1

 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l3 ==> 
p = 0 & x = 3 & global_time = 2
(************************************************************)


(************************************************************)
 Run #3

 Valuation:
  p = 1

 Other valuations with equivalent (discrete) run:
 p > 0

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 1

pta: l1 ==> 
p = 1 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 1 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by impossible transition labeled with a
 | 
 v  pta: l3 ==> 
p = 1 & x = 1 & global_time = 0

 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l3 ==> 
p = 1 & x = 2 & global_time = 1
(************************************************************)
END RESULT

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,
	
	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example (violation possible only at last position)',
		'input_files': ['testCounterExSimple-5c.imi', 'testCounterExSimple-5c.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testCounterExSimple-5c.res' , 'content' : """
BEGIN RESULT
(************************************************************)
 Run #1

 Valuation:
  p = 1

 Other valuations with equivalent (discrete) run:
 p > 0

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p = 1

pta: l1 ==> 
p = 1 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 1 & x = 1 & global_time = 0

 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p = 1 & x = 1 & global_time = 0

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ p > 0} updates{}  sync a Target ltarget] 
 | 
 v  pta: ltarget ==> 
p = 1 & x = 2 & global_time = 1
(************************************************************)


(************************************************************)
 Run #2

 Valuation:
  p = 0

 Other valuations with equivalent (discrete) run:
 p = 0

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 0

pta: l1 ==> 
p = 0 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 0 & x = 1 & global_time = 0

 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p = 0 & x = 1 & global_time = 0
 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l3 ==> 
p = 0 & x = 2 & global_time = 1
(************************************************************)


(************************************************************)
 Run #3

 Valuation:
  p = 1

 Other valuations with equivalent (discrete) run:
 p > 0

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 1

pta: l1 ==> 
p = 1 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 1 & x = 1 & global_time = 0

 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p = 1 & x = 1 & global_time = 0
 | 
 | via d = 0
 | followed by impossible transition labeled with a
 | 
 v  pta: ltarget ==> 
p = 1 & x = 1 & global_time = 0
(************************************************************)
END RESULT
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example (no bad parameter valuation derived)',
		'input_files': ['testCounterExSimple-6.imi', 'testCounterExSimple-6.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
				# NOTE / TODO: the NEGATIVE run is disabled so far! due to a BUG …
			{'file': 'testCounterExSimple-6.res' , 'content' : """
BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  p = 2

 Other valuations with equivalent (discrete) run:
 p > 1

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p = 2

pta: l1 ==> 
p = 2 & x = 2 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{ p > 0} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 2 & x = 2 & global_time = 0

 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p = 2 & x = 2 & global_time = 0

 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{x := 0}  sync a Target ltarget] 
 | 
 v  pta: ltarget ==> 
p = 2 & x = 0 & global_time = 0
(************************************************************)
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example (no bad parameter nor clock valuation derived)',
		'input_files': ['testCounterExSimple-7.imi', 'testCounterExSimple-7.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testCounterExSimple-7.res' , 'content' : """

BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  p = 2

 Other valuations with equivalent (discrete) run:
 p > 1

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p = 2

pta: l1 ==> 
p = 2 & x = 3/2 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{ p > 0} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 2 & x = 3/2 & global_time = 0

 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p = 2 & x = 3/2 & global_time = 0

 | 
 | via d = 1/2
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target ltarget] 
 | 
 v  pta: ltarget ==> 
p = 2 & x = 2 & global_time = 1/2
(************************************************************)

END RESULT

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example (no bad parameter nor clock valuation derived)',
		'input_files': ['testCounterExSimple-8.imi', 'testCounterExSimple-8.imiprop'],
		'options'    : '-no-merge -comparison none -draw-cart',
		'expectations' : [
			{'file': 'testCounterExSimple-8.res' , 'content' : """

BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  p1 = 1
& p2 = 1/2

 Other valuations with equivalent (discrete) run:
 p1 > p2
& p2 > 0
& 6 > p2

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p1 = 1
& p2 = 1/2

pta: l1 ==> 
p1 = 1 & p2 = 1/2 & x = 2 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{ p2 > 0} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p1 = 1 & p2 = 1/2 & x = 2 & global_time = 0

 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p1 = 1 & p2 = 1/2 & x = 2 & global_time = 0

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ p1 > p2
& p2 + x > p1} updates{}  sync a Target ltarget] 
 | 
 v  pta: ltarget ==> 
p1 = 1 & p2 = 1/2 & x = 3 & global_time = 1
(************************************************************)


(************************************************************)
 Run #2

 Valuation:
  p1 = 3
& p2 = 3

 Other valuations with equivalent (discrete) run:
 p1 > 0
& p2 >= p1
& 6 > p2

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p1 = 3
& p2 = 3

pta: l1 ==> 
p1 = 3 & p2 = 3 & x = 3/2 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{ p2 > 0} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p1 = 3 & p2 = 3 & x = 3/2 & global_time = 0

 | 
 | via d = 1/2
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p1 = 3 & p2 = 3 & x = 2 & global_time = 1/2
 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l3 ==> 
p1 = 3 & p2 = 3 & x = 3 & global_time = 3/2
(************************************************************)


(************************************************************)
 Run #3

 Valuation:
  p1 = 1
& p2 = 1/2

 Other valuations with equivalent (discrete) run:
 p1 > p2
& p2 > 0
& 6 > p2

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p1 = 1
& p2 = 1/2

pta: l1 ==> 
p1 = 1 & p2 = 1/2 & x = 3/2 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{ p2 > 0} updates{}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p1 = 1 & p2 = 1/2 & x = 3/2 & global_time = 0

 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{}  sync a Target l3] 
 | 
 v  pta: l3 ==> 
p1 = 1 & p2 = 1/2 & x = 3/2 & global_time = 0
 | 
 | via d = 0
 | followed by impossible transition labeled with a
 | 
 v  pta: ltarget ==> 
p1 = 1 & p2 = 1/2 & x = 3/2 & global_time = 0
(************************************************************)
END RESULT

"""
			} # end result file
			,
			# NOTE: Just check its existence
			{'file': 'testCounterExSimple-8_ex_3_neg.png' , 'content' : ""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy monitoring-style example',
		'input_files': ['testCounterExSimple-9.imi', 'testCounterExSimple-9.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testCounterExSimple-9.res' , 'content' : """

BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  p = 1

 Other valuations with equivalent (discrete) run:
 p >= 0

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p = 1

pta: l1 ==> 
p = 1 & x = 0 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{x := 0}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 1 & x = 0 & global_time = 0

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ p = x} updates{x := 0}  sync b Target l3] 
 | 
 v  pta: l3 ==> 
p = 1 & x = 0 & global_time = 1

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ p = x} updates{}  sync b Target ltarget] 
 | 
 v  pta: ltarget ==> 
p = 1 & x = 1 & global_time = 2
(************************************************************)


(************************************************************)
 Run #2

 Valuation:
  p = 1

 Other valuations with equivalent (discrete) run:
 p >= 0

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 1

pta: l1 ==> 
p = 1 & x = 0 & global_time = 0
 | 
 | via d = 0
 | followed by combined transition [PTA pta: guard{True} updates{x := 0}  sync a Target l2] 
 | 
 v  pta: l2 ==> 
p = 1 & x = 0 & global_time = 0

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ p = x} updates{x := 0}  sync b Target l3] 
 | 
 v  pta: l3 ==> 
p = 1 & x = 0 & global_time = 1
 | 
 | via d = 0
 | followed by impossible transition labeled with b
 | 
 v  pta: ltarget ==> 
p = 1 & x = 0 & global_time = 1
(************************************************************)
END RESULT

"""
			} # end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example without parameter',
		'input_files': ['testCounterExSimple.imi', 'testCounterExSimple.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testCounterExSimple.res' , 'content' : """

BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  

 Other valuations with equivalent (discrete) run:
True

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  

pta: l1, d1 = 1/2, d2 = 50 ==> 
x = 0 & global_time = 0
 | 
 | via d = 3
 | followed by combined transition [PTA pta: guard{ x = 3} updates{x := 0}  sync a Target l2] 
 | 
 v  pta: l2, d1 = 1/2, d2 = 50 ==> 
x = 0 & global_time = 3

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ x = 1} updates{x := 0, d1 := d1 + 2}  sync a Target l3] 
 | 
 v  pta: l3, d1 = 5/2, d2 = 50 ==> 
x = 0 & global_time = 4

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ x = 1} updates{d2 := d2 / 2}  sync a Target l4] 
 | 
 v  pta: l4, d1 = 5/2, d2 = 25 ==> 
x = 1 & global_time = 5

 | 
 | via d = 7
 | followed by combined transition [PTA pta: guard{ x = 8} updates{}  sync a Target lbad] 
 | 
 v  pta: lbad, d1 = 5/2, d2 = 25 ==> 
x = 8 & global_time = 12
(************************************************************)


(************************************************************)
 Run #2

 Valuation:
  

 Other valuations with equivalent (discrete) run:
True

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  

pta: l1, d1 = 1/2, d2 = 50 ==> 
x = 0 & global_time = 0
 | 
 | via d = 3
 | followed by combined transition [PTA pta: guard{ x = 3} updates{x := 0}  sync a Target l2] 
 | 
 v  pta: l2, d1 = 1/2, d2 = 50 ==> 
x = 0 & global_time = 3

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ x = 1} updates{x := 0, d1 := d1 + 2}  sync a Target l3] 
 | 
 v  pta: l3, d1 = 5/2, d2 = 50 ==> 
x = 0 & global_time = 4

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ x = 1} updates{d2 := d2 / 2}  sync a Target l4] 
 | 
 v  pta: l4, d1 = 5/2, d2 = 25 ==> 
x = 1 & global_time = 5
 | 
 | via d = 0
 | followed by impossible transition labeled with a
 | 
 v  pta: lbad, d1 = 5/2, d2 = 25 ==> 
x = 1 & global_time = 5
(************************************************************)

END RESULT

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test EFexemplify on a toy example with parameters and discrete variables',
		'input_files': ['testCounterExSimple-2.imi', 'testCounterExSimple-2.imiprop'],
		'options'    : '-no-merge -comparison none',
		'expectations' : [
			{'file': 'testCounterExSimple-2.res' , 'content' : """

BEGIN RESULT

(************************************************************)
 Run #1

 Valuation:
  p = 1/2

 Other valuations with equivalent (discrete) run:
 1 > p
& p >= 0

 Run nature: valid run

 Run:
Concrete run for parameter valuation:
  p = 1/2

pta: l1, d1 = 1/2 ==> 
p = 1/2 & x = 0 & global_time = 0
 | 
 | via d = 3
 | followed by combined transition [PTA pta: guard{ x = 3} updates{x := 0}  sync a Target l2] 
 | 
 v  pta: l2, d1 = 1/2 ==> 
p = 1/2 & x = 0 & global_time = 3

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ x = 1} updates{x := 0, d1 := d1 + 2}  sync a Target l3] 
 | 
 v  pta: l3, d1 = 5/2 ==> 
p = 1/2 & x = 0 & global_time = 4

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ 1 > p
& x = 1} updates{d1 := d1 / 2}  sync a Target l4] 
 | 
 v  pta: l4, d1 = 5/4 ==> 
p = 1/2 & x = 1 & global_time = 5

 | 
 | via d = 7
 | followed by combined transition [PTA pta: guard{ x = 8} updates{}  sync a Target lbad] 
 | 
 v  pta: lbad, d1 = 5/4 ==> 
p = 1/2 & x = 8 & global_time = 12
(************************************************************)


(************************************************************)
 Run #2

 Valuation:
  p = 1

 Other valuations with equivalent (discrete) run:
 p >= 1

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 1

pta: l1, d1 = 1/2 ==> 
p = 1 & x = 0 & global_time = 0
 | 
 | via d = 3
 | followed by combined transition [PTA pta: guard{ x = 3} updates{x := 0}  sync a Target l2] 
 | 
 v  pta: l2, d1 = 1/2 ==> 
p = 1 & x = 0 & global_time = 3

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ x = 1} updates{x := 0, d1 := d1 + 2}  sync a Target l3] 
 | 
 v  pta: l3, d1 = 5/2 ==> 
p = 1 & x = 0 & global_time = 4
 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l3, d1 = 5/2 ==> 
p = 1 & x = 1 & global_time = 5

 | 
 | via d = 1
 | followed by impossible transition labeled with a
 | 
 v  pta: l4, d1 = 5/4 ==> 
p = 1 & x = 2 & global_time = 6
(************************************************************)


(************************************************************)
 Run #3

 Valuation:
  p = 1/2

 Other valuations with equivalent (discrete) run:
 1 > p
& p >= 0

 Run nature: impossible run

 Run:
Impossible concrete run for parameter valuation:
  p = 1/2

pta: l1, d1 = 1/2 ==> 
p = 1/2 & x = 0 & global_time = 0
 | 
 | via d = 3
 | followed by combined transition [PTA pta: guard{ x = 3} updates{x := 0}  sync a Target l2] 
 | 
 v  pta: l2, d1 = 1/2 ==> 
p = 1/2 & x = 0 & global_time = 3

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ x = 1} updates{x := 0, d1 := d1 + 2}  sync a Target l3] 
 | 
 v  pta: l3, d1 = 5/2 ==> 
p = 1/2 & x = 0 & global_time = 4

 | 
 | via d = 1
 | followed by combined transition [PTA pta: guard{ 1 > p
& x = 1} updates{d1 := d1 / 2}  sync a Target l4] 
 | 
 v  pta: l4, d1 = 5/4 ==> 
p = 1/2 & x = 1 & global_time = 5
 | 
 | via d = 0
 | followed by impossible transition labeled with a
 | 
 v  pta: lbad, d1 = 5/4 ==> 
p = 1/2 & x = 1 & global_time = 5
(************************************************************)
END RESULT
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test LoopSynth: BlT09-fig1',
		'input_files': ['BlT09-fig1.imi', 'BlT09-fig1.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'BlT09-fig1.res' , 'content' : """
BEGIN CONSTRAINT
 u + 2 > l
& l >= 0
& u > 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test LoopSynth: flip-flop (no loop)',
		'input_files': ['flipflop.imi', 'flipflop-loop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'flipflop.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test LoopSynth: simple example with loop',
		'input_files': ['PDFC4.imi', 'PDFC-loop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'PDFC4.res' , 'content' : """
BEGIN CONSTRAINT
 10 >= p2
& p2 >= 0
& p1 >= 0
& p1 + 5 >= p2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/24
		# Last modified            : 2020/09/24
		# Test for IMITATOR version: 3
		'purpose'    : 'Test LoopSynth: simple example with no real loop (1a)',
		'input_files': ['testNoCycle-1a.imi', 'loop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testNoCycle-1a.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/24
		# Last modified            : 2020/09/24
		# Test for IMITATOR version: 3
		'purpose'    : 'Test LoopSynth: simple example with no real loop (1b)',
		'input_files': ['testNoCycle-1b.imi', 'loop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testNoCycle-1b.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test LoopSynth: simple example with loop for any valuation',
		'input_files': ['PDFC5.imi', 'PDFC-loop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'PDFC5.res' , 'content' : """
BEGIN CONSTRAINT
 p3 >= 0
& p2 >= 0
& p1 >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test LoopSynth: witness vs. synthesis (witness)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge-loop-witness.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : terminated after reaching a target state (some states may have been unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test LoopSynth: witness vs. synthesis (synthesis)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge-loop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
OR
  5 > p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test LoopSynth: simple example with 1 real loop',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-loop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test LoopSynth: simple example with 1 real loop (over-approx with -comparison inclusion)',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-loop.imiprop'],
		'options'    : '-comparison inclusion -cycle-algo BFS',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
OR
  p = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible over-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test LoopSynth: simple example with 1 real loop (over-approx with -comparison inclusion -merge)',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-loop.imiprop'],
		'options'    : '-cycle-algo BFS -comparison inclusion -merge',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
OR
  p = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible over-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	# TODO: do -merge only! (so far does not terminate)

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test LoopSynth: simple example with 1 real loop (under-approx with -depth-limit)',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-loop.imiprop'],
		'options'    : '-cycle-algo BFS -depth-limit 3 -no-cumulative-pruning',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : depth limit (2 successors unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/09
		# Test for IMITATOR version: 3
		'purpose'    : 'Test LoopSynth: simple example with 1 real loop (invalid with -comparison inclusion -depth-limit)',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-loop.imiprop'],
		'options'    : '-cycle-algo BFS -comparison inclusion -depth-limit 3',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possibly invalid
Termination                             : depth limit (1 successor unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: witness vs. synthesis (witness)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge-accloop-witness.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : terminated after reaching a target state (some states may have been unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: witness vs. synthesis (synthesis)',
		'input_files': ['testEFInclMerge.imi', 'testEFInclMerge-accloop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFInclMerge.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2046
OR
  5 > p
& p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/24
		# Last modified            : 2020/09/24
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example with no real loop (1a)',
		'input_files': ['testNoCycle-1a.imi', 'acceptingLoop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testNoCycle-1a.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/24
		# Last modified            : 2020/09/24
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example with no real loop (1b)',
		'input_files': ['testNoCycle-1b.imi', 'acceptingLoop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testNoCycle-1b.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example with 1 real loop',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-accloop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example with 1 real loop (syntax variant without parentheses)',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-accloop-noparen.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example with 1 real loop (over-approx with -comparison inclusion)',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-accloop.imiprop'],
		'options'    : '-cycle-algo BFS -comparison inclusion',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
OR
  p = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible over-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example with 1 real loop (over-approx with -comparison inclusion -merge)',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-accloop.imiprop'],
		'options'    : '-cycle-algo BFS -comparison inclusion -merge',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
OR
  p = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible over-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	# TODO: do -merge only! (so far does not terminate)

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example with 1 real loop (under-approx with -depth-limit)',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-accloop.imiprop'],
		'options'    : '-cycle-algo BFS -depth-limit 3 -no-cumulative-pruning',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : depth limit (2 successors unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/09
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example with 1 real loop (invalid with -comparison inclusion -depth-limit)',
		'input_files': ['exLoopIncl.imi', 'exLoopIncl-accloop.imiprop'],
		'options'    : '-cycle-algo BFS -comparison inclusion -depth-limit 3',
		'expectations' : [
			{'file': 'exLoopIncl.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possibly invalid
Termination                             : depth limit (1 successor unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	,

	# NOTE: test removed since there is no accepting loop synthesis + observer patterns as of version 3
	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test AccLoopSynth: flipflop (no loop)',
		#'input_files': ['flipflop.imi', 'flipflop-accloop.imiprop'],
		#'options'    : '',
		#'expectations' : [
			#{'file': 'flipflop.res' , 'content' : """
#BEGIN CONSTRAINT
#False
#END CONSTRAINT

#------------------------------------------------------------
#Constraint soundness                    : exact
#Termination                             : regular termination
#Constraint nature                       : good
#------------------------------------------------------------
#Number of states                        : 20
#Number of transitions                   : 19
#Number of computed states               : 20
#"""
			#} #end result file
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------

	#,

	#------------------------------------------------------------
	{
		# Test version             : 2
		# Test since               : 2019/07/22
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example 1',
		'input_files': ['testNDFS-1.imi', 'testNDFS1-accloop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testNDFS-1.res' , 'content' : """
BEGIN CONSTRAINT
 p = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 2
		# Test since               : 2019/07/22
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example 2',
		'input_files': ['testNDFS-2.imi', 'testNDFS2-accloop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testNDFS-2.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
OR
  p = 1
OR
  p = 4
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 2
		# Test since               : 2019/07/22
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynth: simple example 3 (accepting for all valuations)',
		'input_files': ['PDFC5.imi', 'PDFC5-accloop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'PDFC5.res' , 'content' : """
BEGIN CONSTRAINT
 p3 >= 0
& p2 >= 0
& p1 >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/22
		# Last modified            : 2020/09/22
		# Test for IMITATOR version: 3.0
		'purpose'    : 'Test AccLoopSynth (without option -no-cumulative-pruning)',
		'input_files': ['testInclusionEF.imi', 'testInclusionEF-loop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testInclusionEF.res' , 'content' : """
BEGIN CONSTRAINT
 5 >= p
& p >= 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Number of states                        : 4
Number of transitions                   : 4
Number of computed states               : 5
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/22
		# Last modified            : 2020/09/22
		# Test for IMITATOR version: 3.0
		'purpose'    : 'Test AccLoopSynth (with option -no-cumulative-pruning)',
		'input_files': ['testInclusionEF.imi', 'testInclusionEF-loop.imiprop'],
		'options'    : '-cycle-algo BFS -no-cumulative-pruning',
		'expectations' : [
			{'file': 'testInclusionEF.res' , 'content' : """
BEGIN CONSTRAINT
 5 >= p
& p >= 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Number of states                        : 14
Number of transitions                   : 15
Number of computed states               : 16
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test AccLoopSynthNDFS emptiness: flipflop (no loop)',
		'input_files': ['flipflop.imi', 'flipflop-accloop-witness.imiprop'],
		'options'    : '-cycle-algo NDFS',
		'expectations' : [
			{'file': 'flipflop.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test AccLoopSynthNDFS synthesis: flipflop (no loop)',
		'input_files': ['flipflop.imi', 'flipflop-accloop.imiprop'],
		'options'    : '-cycle-algo NDFS',
		'expectations' : [
			{'file': 'flipflop.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/24
		# Last modified            : 2020/09/24
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynthNDFS: simple example with no real loop (1a)',
		'input_files': ['testNoCycle-1a.imi', 'acceptingLoop.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testNoCycle-1a.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/24
		# Last modified            : 2020/09/24
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynthNDFS: simple example with no real loop (1b)',
		'input_files': ['testNoCycle-1b.imi', 'acceptingLoop.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testNoCycle-1b.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 2
		# Test since               : 2019/07/22
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynthNDFS emptiness: simple example 1',
		'input_files': ['testNDFS-1.imi', 'testNDFS1-accloop-witness.imiprop'],
		'options'    : '-cycle-algo NDFS',
		'expectations' : [
			{'file': 'testNDFS-1.res' , 'content' : """
BEGIN CONSTRAINT
 p = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : terminated after reaching a target state (some states may have been unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 2
		# Test since               : 2019/08/01
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynthNDFS synthesis: simple example 1',
		'input_files': ['testNDFS-1.imi', 'testNDFS1-accloop.imiprop'],
		'options'    : '-cycle-algo NDFS',
		'expectations' : [
			{'file': 'testNDFS-1.res' , 'content' : """
BEGIN CONSTRAINT
 p = 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 2
		# Test since               : 2019/08/01
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynthNDFS emptiness: simple example 2',
		'input_files': ['testNDFS-2.imi', 'testNDFS2-accloop-witness.imiprop'],
		'options'    : '-cycle-algo NDFS',
		'expectations' : [
			{'file': 'testNDFS-2.res' , 'content' :
# NOTE: p = 4 would also be an acceptable result
"""
BEGIN CONSTRAINT
 p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : terminated after reaching a target state (some states may have been unexplored)
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 2
		# Test since               : 2019/08/01
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test AccLoopSynthNDFS synthesis: simple example 2',
		'input_files': ['testNDFS-2.imi', 'testNDFS2-accloop.imiprop'],
		'options'    : '-cycle-algo NDFS',
		'expectations' : [
			{'file': 'testNDFS-2.res' , 'content' : """
BEGIN CONSTRAINT
 p = 2
OR
  p = 1
OR
  p = 4
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/10
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test state predicate with `accepting` keyword and location predicate in property: EF',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-EF.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
 OR
   p = 4

END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/14
		# Last modified            : 2020/09/14
		# Test for IMITATOR version: 3
		'purpose'    : 'Test only `accepting` keyword: EF',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-EFaccepting.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/10
		# Last modified            : 2020/09/14
		# Test for IMITATOR version: 3
		'purpose'    : 'Test empty state predicate: EF',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-EFnopred.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/14
		# Last modified            : 2020/09/14
		# Test for IMITATOR version: 3
		'purpose'    : 'Test complex state predicate: EF',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-EFcomplex.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
	p = 2
OR
	p = 3
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/10
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test state predicate with `accepting` keyword and location predicate in property: Loop',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-accloop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
 OR
   p = 4

END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/10
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test only `accepting` keyword: Loop',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-accloop-nopred.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/03/12
		# Last modified            : 2021/03/12
		# Test for IMITATOR version: 3
		'purpose'    : 'Test only `accepting` keyword: Loop [alias AccCycle]',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-accloop-nopred-acccycle.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/03/12
		# Last modified            : 2021/03/12
		# Test for IMITATOR version: 3
		'purpose'    : 'Test only `accepting` keyword: Loop [alias AcceptingCycle]',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-accloop-nopred-acceptingcycle.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/03/12
		# Last modified            : 2021/03/12
		# Test for IMITATOR version: 3
		'purpose'    : 'Test only `accepting` keyword: Loop [alias AccLoop]',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-accloop-nopred-accloop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/03/12
		# Last modified            : 2021/03/12
		# Test for IMITATOR version: 3
		'purpose'    : 'Test only `accepting` keyword: Loop [alias AcceptingLoop]',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-accloop-nopred-acceptingloop.imiprop'],
		'options'    : '-cycle-algo BFS',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/10
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test state predicate with `accepting` keyword and location predicate in property: NDFS',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-accloop.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
 OR
   p = 4

END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/10
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test only `accepting` keyword: NDFS',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-accloop-nopred.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
  p = 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/10
		# Last modified            : 2020/09/10
		# Test for IMITATOR version: 3
		'purpose'    : 'Test state predicate with `accepting` keyword and location predicate in property: PRPC',
		'input_files': ['testEFaccepting.imi', 'testEFaccepting-PRPC.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFaccepting.res' , 'content' : """
BEGIN CONSTRAINT
 2 > p
& p >= 0
OR
  4 > p
& p > 2
OR
  p > 4
<good|bad>
 p = 2
OR
  p = 4
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact <good|bad> exact
Termination                             : regular termination
Constraint nature                       : good/bad

------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test NZCUB: flip-flop (no loop)',
		'input_files': ['flipflop.imi', 'flipflop-NZCUB.imiprop'],
		'options'    : '-nz-method already',
		'expectations' : [
			{'file': 'flipflop.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test NZCUB: PDFC4 (loop but Zeno)',
		'input_files': ['PDFC4.imi', 'PDFC4-NZCUB.imiprop'],
		'options'    : '-nz-method already',
		'expectations' : [
			{'file': 'PDFC4.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test NZCUB: PDFC4 (loop but Zeno); check',
		'input_files': ['PDFC4.imi', 'PDFC4-NZCUB.imiprop'],
		'options'    : '-nz-method check',
		'expectations' : [
			{'file': 'PDFC4.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test NZCUB: PDFC4 (loop but Zeno); transform',
		'input_files': ['PDFC4.imi', 'PDFC4-NZCUB.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'PDFC4.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test NZCUB: CUBPTA1 (non-Zeno loop)',
		'input_files': ['CUBPTA1.imi', 'CUBPTA-NZCUB.imiprop'],
		'options'    : '-nz-method already',
		'expectations' : [
			{'file': 'CUBPTA1.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 0
& p2 >= 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test NZCUB: CUBPTA2 (2 non-Zeno loops)',
		'input_files': ['CUBPTA2.imi', 'CUBPTA-NZCUB.imiprop'],
		'options'    : '-nz-method already',
		'expectations' : [
			{'file': 'CUBPTA2.res' , 'content' : """
BEGIN CONSTRAINT
 p2 >= 0
& p1 >= 5
OR
  p1 >= 0
& p2 >= 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test infinite run on one example (Zeno version)',
		'input_files': ['testInfiniteRun.imi', 'testInfiniteRun-Zeno.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testInfiniteRun.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test infinite run on one example (non-Zeno version)',
		'input_files': ['testInfiniteRun.imi', 'testInfiniteRun-nonZeno.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testInfiniteRun.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: very basic example without clocks',
		'input_files': ['PDFC1.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : '-states-description',
		'expectations' : [
			{'file': 'PDFC1.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 0
& p2 >= p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} #end result file
			,
			{'file': 'PDFC1-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: l1 ==>
& p1 >= 0
& p2 >= 0

  Projection onto the parameters:
   p1 >= 0
& p2 >= 0

  /************************************************************/
  STATE 1:
  pta: l2 ==>
& p1 >= 0
& p2 >= p1

  Projection onto the parameters:
   p1 >= 0
& p2 >= p1

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "a"
  s_1 -> s_1 via "a"
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: very basic example (false result)',
		'input_files': ['PDFC3.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : ' -states-description',
		'expectations' : [
			{'file': 'PDFC3.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Number of states              : 2
Number of transitions         : 1
Number of computed states     : 2
"""
			} #end result file
			,
			{'file': 'PDFC3-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: l1 ==>
& p1 + 5 >= x
& p1 >= 0
& p2 >= 0
& x >= 0

  Projection onto the parameters:
   p2 >= 0
& p1 >= 0

  /************************************************************/
  STATE 1:
  pta: l2 ==>
& p1 >= 0
& p1 + 5 >= p2
& p2 >= 0
& x >= p2
& 10 >= x

  Projection onto the parameters:
   10 >= p2
& p2 >= 0
& p1 >= 0
& p1 + 5 >= p2

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "a"
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: very basic example (normal result)',
		'input_files': ['PDFC4.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : ' -states-description',
		'expectations' : [
			{'file': 'PDFC4.res' , 'content' : """
BEGIN CONSTRAINT
 p1 + 5 >= p2
& p1 >= 0
& p2 >= 0
& 10 >= p2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Number of states              : 2
Number of transitions         : 2
Number of computed states     : 3
"""
			} #end result file
			,
			{'file': 'PDFC4-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: l1 ==>
& p1 + 5 >= x
& p1 >= 0
& p2 >= 0
& x >= 0

  Projection onto the parameters:
   p2 >= 0
& p1 >= 0

  /************************************************************/
  STATE 1:
  pta: l2 ==>
& p1 >= 0
& p1 + 5 >= p2
& p2 >= 0
& x >= p2
& 10 >= x

  Projection onto the parameters:
   10 >= p2
& p2 >= 0
& p1 >= 0
& p1 + 5 >= p2

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "a"
  s_1 -> s_1 via "a"
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: very basic example (false result)',
		'input_files': ['PDFC6.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : ' -states-description -no-var-autoremove',
		'expectations' : [
			{'file': 'PDFC6.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Number of states              : 2
Number of transitions         : 1
Number of computed states     : 2
"""
			} #end result file
			,
			{'file': 'PDFC6-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: l1 ==>
& p >= 0
& x1 >= 0

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  STATE 1:
  pta: l2 ==>
& p >= 0
& x1 >= 0

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "a"
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: very basic example (true result)',
		'input_files': ['PDFC7.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : ' -states-description',
		'expectations' : [
			{'file': 'PDFC7.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Number of states              : 2
Number of transitions         : 2
Number of computed states     : 3
"""
			} #end result file
			,
			{'file': 'PDFC7-statespace.states' , 'content' : """

  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: l1 ==>
& p >= 0
& x1 >= 0

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  STATE 1:
  pta: l2 ==>
& p >= 0
& x1 >= p

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "a"
  s_1 -> s_1 via "a"
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: basic example with disjunction',
		'input_files': ['PDFC5.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'PDFC5.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 0
& p2 >= 0
& p1 + 5 = p3
OR
  p1 >= 0
& p3 > 5 + p1
& p2 >= 5 + p1
OR
  p1 >= 0
& p1 + 5 > p3
& p3 >= 0
& p2 >= 5 + p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: basic example with disjunction (no inclusion)',
		'input_files': ['PDFC5.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : '-comparison equality',
		'expectations' : [
			{'file': 'PDFC5.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 0
& p2 >= 0
& p1 + 5 = p3
OR
  p1 >= 0
& p3 > 5 + p1
& p2 >= 5 + p1
OR
  p1 >= 0
& p1 + 5 > p3
& p3 >= 0
& p2 >= 5 + p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: basic example with disjunction (explicit inclusion)',
		'input_files': ['PDFC5.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : '-comparison inclusion',
		'expectations' : [
			{'file': 'PDFC5.res' , 'content' : """
BEGIN CONSTRAINT
 p1 >= 0
& p2 >= 0
& p1 + 5 = p3
OR
  p1 >= 0
& p3 > 5 + p1
& p2 >= 5 + p1
OR
  p1 >= 0
& p1 + 5 > p3
& p3 >= 0
& p2 >= 5 + p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: example with early termination due to false constraint',
		'input_files': ['flipflop.imi', 'flipflop-deadlockfree.imiprop'],
		'options'    : ' -states-description',
		'expectations' : [
			{'file': 'flipflop.res' , 'content' : """
BEGIN CONSTRAINT
False
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: example with basic backward under-approximation',
		'input_files': ['PDFC8.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : '-depth-limit 5 -no-var-autoremove',
		'expectations' : [
			{'file': 'PDFC8.res' , 'content' : """
BEGIN CONSTRAINT
 p1 > 2
& 3 >= p1
OR
  p1 > 0
& 2 > p1
<good|bad>
 p1 > 3
OR
  p1 = 2
OR
  p1 = 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : possible under-approximation <good|bad> possible over-approximation
Termination                   : depth limit (1 successor unexplored)
Constraint nature             : good/bad
------------------------------------------------------------
Number of states              : 7
Number of transitions         : 7
Number of computed states     : 8
"""
			} #end result file
		] # end expectations
	} # end test case
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: example with basic backward under-approximation and exact result',
		'input_files': ['PDFC8b.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : '-depth-limit 5 -no-var-autoremove', #TODO: re-do without '-no-var-autoremove'
		'expectations' : [
			{'file': 'PDFC8b.res' , 'content' : """
BEGIN CONSTRAINT
 p1 > 2
& 3 >= p1
OR
  p1 > 0
& 2 > p1
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : depth limit (1 successor unexplored)
Constraint nature             : good
------------------------------------------------------------
Number of states              : 7
Number of transitions         : 7
Number of computed states     : 8
"""
			} #end result file
		] # end expectations
	} # end test case
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: another example with basic backward under-approximation',
		'input_files': ['PDFC9.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : '-depth-limit 5 -no-var-autoremove', #TODO: re-do without '-no-var-autoremove'
		'expectations' : [
			{'file': 'PDFC9.res' , 'content' : """
BEGIN CONSTRAINT
 p1 > 2
<good|bad>
 2 >= p1
& p1 >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : possible under-approximation <good|bad> possible over-approximation
Termination                   : depth limit (1 successor unexplored)
Constraint nature             : good/bad
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test PDFC: again another example with basic backward under-approximation',
		'input_files': ['PDFC9b.imi', 'PDFC-deadlockfree.imiprop'],
		'options'    : '-depth-limit 5 -no-var-autoremove', #TODO: re-do without '-no-var-autoremove'
		'expectations' : [
			{'file': 'PDFC9b.res' , 'content' : """
BEGIN CONSTRAINT
 p1 > 2
<good|bad>
 2 >= p1
& p1 >= 0
END CONSTRAINT

------------------------------------------------------------
Constraint soundness          : possible under-approximation <good|bad> possible over-approximation
Termination                   : depth limit (1 successor unexplored)
Constraint nature             : good/bad
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
			
	,
	
	#------------------------------------------------------------
	{
		'purpose'    : 'Test the inverse method (flip-flop)',
		'input_files': ['flipflop.imi', 'flipflop.pi0'],
		'options'    : '',
		'expectations' : [
			{'file': 'flipflop.res' , 'content' : """
BEGIN CONSTRAINT
dG3_u + dG4_u >= 17 & dG3_u >= 8 & dG4_u >= 3 & 17 > dG3_u & 24 > dG3_u + dG4_u
END CONSTRAINT
			"""
			} #end result file
		] # end expectations
	} # end test case
	
	,
	
	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/21
		# Last modified            : 2020/09/21
		# Test for IMITATOR version: 3
		'purpose'    : 'Test the inverse method (flip-flop) #witness',
		'input_files': ['flipflop.imi', 'flipflop-witness.pi0'],
		'options'    : '',
		'expectations' : [
# NOTE: witness is not recognized by IM, therefore will raise a warning and give the same result as synthesis
			{'file': 'flipflop.res' , 'content' : """
BEGIN CONSTRAINT
dG3_u + dG4_u >= 17 & dG3_u >= 8 & dG4_u >= 3 & 17 > dG3_u & 24 > dG3_u + dG4_u
END CONSTRAINT
			"""
			} #end result file
		] # end expectations
	} # end test case
	
	,
	
	#------------------------------------------------------------
	{
		'purpose'    : 'Test the convex inverse method (SIMOP)',
		'input_files': ['simop.imi', 'simop.pi0'],
		'options'    : '-merge -no-random -comparison inclusion',
		'expectations' : [
			{'file': 'simop.res' , 'content' : """
BEGIN CONSTRAINT
500 >= COMct
    & COMct > 495
    & SIGmrt > 70 + 4*COMct
END CONSTRAINT
			"""
			} #end result file
		] # end expectations
	} # end test case
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test variants of IM: here IM',
		'input_files': ['testIM-IMK-IMunion.imi', 'testIM-IMK-IMunion-IM.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testIM-IMK-IMunion.res' , 'content' : """
		  p = 2
		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test variants of IM: here IMconvex',
		'input_files': ['testIM-IMK-IMunion.imi', 'testIM-IMK-IMunion-IMconvex.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testIM-IMK-IMunion.res' , 'content' : """
		  p = 2
		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test variants of IM: here IMK',
		'input_files': ['testIM-IMK-IMunion.imi', 'testIM-IMK-IMunion-IMK.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testIM-IMK-IMunion.res' , 'content' : """
		 p > 1
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test variants of IM: here IMunion',
		'input_files': ['testIM-IMK-IMunion.imi', 'testIM-IMK-IMunion-IMunion.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testIM-IMK-IMunion.res' , 'content' : """
		4 >= p & p > 1
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test variants of IM (bis): here IM',
		'input_files': ['exVariantes.imi', 'exVariantes-IM.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'exVariantes.res' , 'content' : """
	BEGIN CONSTRAINT
 5*p1 > p2
& p2 >= 3
& p2 >= 4*p1
END CONSTRAINT
		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test variants of IM (bis): here IMconvex',
		'input_files': ['exVariantes.imi', 'exVariantes-IMconvex.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'exVariantes.res' , 'content' : """
	p2 >= 3 & 5*p1 > p2 & p2 >= 4*p1
		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test variants of IM (bis): here IMK',
		'input_files': ['exVariantes.imi', 'exVariantes-IMK.imiprop'],
		'options'    : '-no-random',
		'expectations' : [
			{'file': 'exVariantes.res' , 'content' : """
 p2 > 2
& 5*p1 > p2
		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test variants of IM (bis): here IMunion',
		'input_files': ['exVariantes.imi', 'exVariantes-IMunion.imiprop'],
		'options'    : '-no-random',
		'expectations' : [
			{'file': 'exVariantes.res' , 'content' : """
		 5*p1 > p2 & p2 >= 3 OR 5*p1 > p2 & p2 > 2 & p2 >= 4*p1
		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test IM on an incomplete example',
		'input_files': ['exIMnoncomplete.imi', 'exIMnoncomplete-IMconvex.imiprop'],
		'options'    : '-no-random',
		'expectations' : [
			{'file': 'exIMnoncomplete.res' , 'content' : """
BEGIN CONSTRAINT
p1 >= 0
& p2 >= 0
& p3 > p1
END CONSTRAINT		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test IMcomplete on an incomplete example',
		'input_files': ['exIMnoncomplete.imi', 'exIMnoncomplete-IM.imiprop'],
		'options'    : '-no-random',
		'expectations' : [
			{'file': 'exIMnoncomplete.res' , 'content' : """
BEGIN CONSTRAINT
     p1 >= 0
    & p2 > p1
    & p3 >= 0
    OR
      p3 > p1
    & p2 >= 0
    & p1 >= p2
END CONSTRAINT		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 2
		# Test since               : 2019/05/30
		# Test for IMITATOR version: 2.11
		'purpose'    : 'Test PRP on a very simple example',
		'input_files': ['testEFcounterex.imi', 'testEFcounterex-prp.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testEFcounterex.res' , 'content' : """
BEGIN CONSTRAINT
 p >= 0
& 1 > p
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} #end result file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test PRP (old version) on a simple example (good reference valuation)',
		#'input_files': ['testPRP.imi', 'testPRP.pigood'],
		#'options'    : '-PRP  -states-description',
		#'expectations' : [
			#{'file': 'testPRP.res' , 'content' : """
#BEGIN CONSTRAINT
	#4 > p2
    #& 3 > p1
    #& p1 >= 0
    #& p2 >= 0
#END CONSTRAINT
		  #"""
			#} # end result file
			#,
			#{'file': 'testPRP-statespace.states' , 'content' : """
  #DESCRIPTION OF THE STATES

  #/************************************************************/
  #INITIAL
  #STATE 0:
  #pta: l1 ==>
#& p1 >= 0
#& p2 >= 0
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 0
#& p1 >= 0

  #/************************************************************/
  #STATE 1:
  #pta: l2 ==>
#& p1 >= 0
#& p2 >= 0
#& x >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 0
#& p1 >= 0

  #/************************************************************/
  #STATE 2:
  #pta: l3 ==>
#& p1 >= x
#& p2 >= 0
#& x >= 0
#& 1 >= p2
#& x = y

  #Projection onto the parameters:
   #1 >= p2
#& p2 >= 0
#& p1 >= 0

  #/************************************************************/
  #STATE 3:
  #pta: l4 ==>
#& p1 >= p2
#& p2 >= 0
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p1 >= p2
#& p2 >= 0

  #/************************************************************/
  #DESCRIPTION OF THE TRANSITIONS
  #s_0 -> s_1
  #s_1 -> s_2
  #s_1 -> s_3
  #s_2 -> s_2
#"""
			#} # end result file
			#,
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------
	#,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test PRP on a simple example (good reference valuation)',
		'input_files': ['testPRP.imi', 'testPRP-good.imiprop'],
		'options'    : '-states-description',
		'expectations' : [
			{'file': 'testPRP.res' , 'content' : """
BEGIN CONSTRAINT
	4 > p2
    & 3 > p1
    & p1 >= 0
    & p2 >= 0
END CONSTRAINT
		  """
			} # end result file
			,
			{'file': 'testPRP-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: l1 ==>
& p1 >= 0
& p2 >= 0
& y >= 0
& x = y

  Projection onto the parameters:
   p2 >= 0
& p1 >= 0

  /************************************************************/
  STATE 1:
  pta: l2 ==>
& p1 >= 0
& p2 >= 0
& x >= 0
& x = y

  Projection onto the parameters:
   p2 >= 0
& p1 >= 0

  /************************************************************/
  STATE 2:
  pta: l3 ==>
& p1 >= x
& p2 >= 0
& x >= 0
& 1 >= p2
& x = y

  Projection onto the parameters:
   1 >= p2
& p2 >= 0
& p1 >= 0

  /************************************************************/
  STATE 3:
  pta: l4 ==>
& p1 >= p2
& p2 >= 0
& y >= 0
& x = y

  Projection onto the parameters:
   p1 >= p2
& p2 >= 0

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1
  s_1 -> s_2
  s_1 -> s_3
  s_2 -> s_2
		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test PRP (old version) on a simple example (bad reference valuation)',
		#'input_files': ['testPRP.imi', 'testPRP.pibad'],
		#'options'    : '-PRP  -states-description',
		#'expectations' : [
			#{'file': 'testPRP.res' , 'content' : """
		 #& p1 >= 0
#OR
  #p2 >= 0
#& p1 >= 3
		  #"""
			#} # end result file
			#,
			#{'file': 'testPRP-statespace.states' , 'content' : """
  #DESCRIPTION OF THE STATES

  #/************************************************************/
  #INITIAL
  #STATE 0:
  #pta: l1 ==>
#& p1 >= 0
#& p2 >= 0
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 0
#& p1 >= 0

  #/************************************************************/
  #STATE 1:
  #pta: l2 ==>
#& p1 >= 0
#& p2 >= 0
#& x >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 0
#& p1 >= 0

  #/************************************************************/
  #STATE 2:
  #pta: locBad1 ==>
#& p1 >= 0
#& p2 >= 4
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 4
#& p1 >= 0

  #/************************************************************/
  #STATE 3:
  #pta: l4 ==>
#& p1 >= p2
#& p2 >= 0
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p1 >= p2
#& p2 >= 0

  #/************************************************************/
  #STATE 4:
  #pta: locBad2 ==>
#& p1 >= 3
#& p2 >= 0
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 0
#& p1 >= 3

  #/************************************************************/
  #DESCRIPTION OF THE TRANSITIONS
  #s_0 -> s_1
  #s_0 -> s_2
  #s_1 -> s_3
  #s_1 -> s_4
		  #"""
			#} # end result file
			#,
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------
	#,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test PRP on a simple example (bad reference valuation)',
		'input_files': ['testPRP.imi', 'testPRP-bad.imiprop'],
		'options'    : '-states-description',
		'expectations' : [
			{'file': 'testPRP.res' , 'content' : """
		 & p1 >= 0
OR
  p2 >= 0
& p1 >= 3
		  """
			} # end result file
			,
			{'file': 'testPRP-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: l1 ==>
& p1 >= 0
& p2 >= 0
& y >= 0
& x = y

  Projection onto the parameters:
   p2 >= 0
& p1 >= 0

  /************************************************************/
  STATE 1:
  pta: l2 ==>
& p1 >= 0
& p2 >= 0
& x >= 0
& x = y

  Projection onto the parameters:
   p2 >= 0
& p1 >= 0

  /************************************************************/
  STATE 2:
  pta: locBad1 ==>
& p1 >= 0
& p2 >= 4
& y >= 0
& x = y

  Projection onto the parameters:
   p2 >= 4
& p1 >= 0

  /************************************************************/
  STATE 3:
  pta: l4 ==>
& p1 >= p2
& p2 >= 0
& y >= 0
& x = y

  Projection onto the parameters:
   p1 >= p2
& p2 >= 0

  /************************************************************/
  STATE 4:
  pta: locBad2 ==>
& p1 >= 3
& p2 >= 0
& y >= 0
& x = y

  Projection onto the parameters:
   p2 >= 0
& p1 >= 3

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1
  s_0 -> s_2
  s_1 -> s_3
  s_1 -> s_4
		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test PRP (old version) on a simple example (looping reference valuation)',
		#'input_files': ['testPRP.imi', 'testPRP.piloop'],
		#'options'    : '-PRP  -depth-limit 10 -states-description',
		#'expectations' : [
			#{'file': 'testPRP.res' , 'content' : """
 #p2 >= 4
    #& p1 >= 0
    #OR
      #p2 >= 0
    #& p1 >= 3
		  #"""
			#} # end result file
			#,
			#{'file': 'testPRP-statespace.states' , 'content' : """
  #DESCRIPTION OF THE STATES

  #/************************************************************/
  #INITIAL
  #STATE 0:
  #pta: l1 ==>
#& p1 >= 0
#& p2 >= 0
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 0
#& p1 >= 0

  #/************************************************************/
  #STATE 1:
  #pta: l2 ==>
#& p1 >= 0
#& p2 >= 0
#& x >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 0
#& p1 >= 0

  #/************************************************************/
  #STATE 2:
  #pta: locBad1 ==>
#& p1 >= 0
#& p2 >= 4
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 4
#& p1 >= 0

  #/************************************************************/
  #STATE 3:
  #pta: infiniteLoop ==>
#& 1 >= x
#& p1 >= 0
#& p2 >= 5
#& x >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 5
#& p1 >= 0

  #/************************************************************/
  #STATE 4:
  #pta: l4 ==>
#& p1 >= p2
#& p2 >= 0
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p1 >= p2
#& p2 >= 0

  #/************************************************************/
  #STATE 5:
  #pta: locBad2 ==>
#& p1 >= 3
#& p2 >= 0
#& y >= 0
#& x = y

  #Projection onto the parameters:
   #p2 >= 0
#& p1 >= 3

  #/************************************************************/
  #STATE 6:
  #pta: infiniteLoop ==>
#& 1 >= x
#& p1 >= 0
#& p2 >= 5
#& x >= 0
#& x + 1 = y

  #Projection onto the parameters:
   #p2 >= 5
#& p1 >= 0

  #/************************************************************/
  #STATE 7:
  #pta: infiniteLoop ==>
#& 1 >= x
#& p1 >= 0
#& p2 >= 5
#& x >= 0
#& x + 2 = y

  #Projection onto the parameters:
   #p2 >= 5
#& p1 >= 0

  #/************************************************************/
  #STATE 8:
  #pta: infiniteLoop ==>
#& 1 >= x
#& p1 >= 0
#& p2 >= 5
#& x >= 0
#& x + 3 = y

  #Projection onto the parameters:
   #p2 >= 5
#& p1 >= 0

  #/************************************************************/
  #STATE 9:
  #pta: infiniteLoop ==>
#& 1 >= x
#& p1 >= 0
#& p2 >= 5
#& x >= 0
#& x + 4 = y

  #Projection onto the parameters:
   #p2 >= 5
#& p1 >= 0

  #/************************************************************/
  #STATE 10:
  #pta: infiniteLoop ==>
#& 1 >= x
#& p1 >= 0
#& p2 >= 5
#& x >= 0
#& x + 5 = y

  #Projection onto the parameters:
   #p2 >= 5
#& p1 >= 0

  #/************************************************************/
  #STATE 11:
  #pta: infiniteLoop ==>
#& 1 >= x
#& p1 >= 0
#& p2 >= 5
#& x >= 0
#& x + 6 = y

  #Projection onto the parameters:
   #p2 >= 5
#& p1 >= 0

  #/************************************************************/
  #STATE 12:
  #pta: infiniteLoop ==>
#& 1 >= x
#& p1 >= 0
#& p2 >= 5
#& x >= 0
#& x + 7 = y

  #Projection onto the parameters:
   #p2 >= 5
#& p1 >= 0

  #/************************************************************/
  #STATE 13:
  #pta: infiniteLoop ==>
#& 1 >= x
#& p1 >= 0
#& p2 >= 5
#& x >= 0
#& x + 8 = y

  #Projection onto the parameters:
   #p2 >= 5
#& p1 >= 0

  #/************************************************************/
  #DESCRIPTION OF THE TRANSITIONS
  #s_0 -> s_1
  #s_0 -> s_2
  #s_0 -> s_3
  #s_1 -> s_4
  #s_1 -> s_5
  #s_3 -> s_6
  #s_6 -> s_7
  #s_7 -> s_8
  #s_8 -> s_9
  #s_9 -> s_10
  #s_10 -> s_11
  #s_11 -> s_12
  #s_12 -> s_13


		  #"""
			#} # end result file
			#,
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------

	#,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PRP on a simple example (looping reference valuation)',
		'input_files': ['testPRP.imi', 'testPRP-loop.imiprop'],
		'options'    : '-depth-limit 10 -states-description',
		'expectations' : [
			{'file': 'testPRP.res' , 'content' : """
 p2 >= 4
    & p1 >= 0
    OR
      p2 >= 0
    & p1 >= 3
		  """
			} # end result file
			,
			{'file': 'testPRP-statespace.states' , 'content' : """
  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: l1 ==>
& p1 >= 0
& p2 >= 0
& y >= 0
& x = y

  Projection onto the parameters:
   p2 >= 0
& p1 >= 0

  /************************************************************/
  STATE 1:
  pta: l2 ==>
& p1 >= 0
& p2 >= 0
& x >= 0
& x = y

  Projection onto the parameters:
   p2 >= 0
& p1 >= 0

  /************************************************************/
  STATE 2:
  pta: locBad1 ==>
& p1 >= 0
& p2 >= 4
& y >= 0
& x = y

  Projection onto the parameters:
   p2 >= 4
& p1 >= 0

  /************************************************************/
  STATE 3:
  pta: infiniteLoop ==>
& 1 >= x
& p1 >= 0
& p2 >= 5
& x >= 0
& x = y

  Projection onto the parameters:
   p2 >= 5
& p1 >= 0

  /************************************************************/
  STATE 4:
  pta: l4 ==>
& p1 >= p2
& p2 >= 0
& y >= 0
& x = y

  Projection onto the parameters:
   p1 >= p2
& p2 >= 0

  /************************************************************/
  STATE 5:
  pta: locBad2 ==>
& p1 >= 3
& p2 >= 0
& y >= 0
& x = y

  Projection onto the parameters:
   p2 >= 0
& p1 >= 3

  /************************************************************/
  STATE 6:
  pta: infiniteLoop ==>
& 1 >= x
& p1 >= 0
& p2 >= 5
& x >= 0
& x + 1 = y

  Projection onto the parameters:
   p2 >= 5
& p1 >= 0

  /************************************************************/
  STATE 7:
  pta: infiniteLoop ==>
& 1 >= x
& p1 >= 0
& p2 >= 5
& x >= 0
& x + 2 = y

  Projection onto the parameters:
   p2 >= 5
& p1 >= 0

  /************************************************************/
  STATE 8:
  pta: infiniteLoop ==>
& 1 >= x
& p1 >= 0
& p2 >= 5
& x >= 0
& x + 3 = y

  Projection onto the parameters:
   p2 >= 5
& p1 >= 0

  /************************************************************/
  STATE 9:
  pta: infiniteLoop ==>
& 1 >= x
& p1 >= 0
& p2 >= 5
& x >= 0
& x + 4 = y

  Projection onto the parameters:
   p2 >= 5
& p1 >= 0

  /************************************************************/
  STATE 10:
  pta: infiniteLoop ==>
& 1 >= x
& p1 >= 0
& p2 >= 5
& x >= 0
& x + 5 = y

  Projection onto the parameters:
   p2 >= 5
& p1 >= 0

  /************************************************************/
  STATE 11:
  pta: infiniteLoop ==>
& 1 >= x
& p1 >= 0
& p2 >= 5
& x >= 0
& x + 6 = y

  Projection onto the parameters:
   p2 >= 5
& p1 >= 0

  /************************************************************/
  STATE 12:
  pta: infiniteLoop ==>
& 1 >= x
& p1 >= 0
& p2 >= 5
& x >= 0
& x + 7 = y

  Projection onto the parameters:
   p2 >= 5
& p1 >= 0

  /************************************************************/
  STATE 13:
  pta: infiniteLoop ==>
& 1 >= x
& p1 >= 0
& p2 >= 5
& x >= 0
& x + 8 = y

  Projection onto the parameters:
   p2 >= 5
& p1 >= 0

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1
  s_0 -> s_2
  s_0 -> s_3
  s_1 -> s_4
  s_1 -> s_5
  s_3 -> s_6
  s_6 -> s_7
  s_7 -> s_8
  s_8 -> s_9
  s_9 -> s_10
  s_10 -> s_11
  s_11 -> s_12
  s_12 -> s_13


		  """
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode cover (grid)',
		'input_files': ['testBC-grid-plain.imi', 'testBC-grid4x4-cover.imiprop'],
		'options'    : '',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #1

 Pi1:
  p1 = 1
& p2 = 1

 K1:
 p2 >= 1
& p1 >= 1
& 2 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #2

 Pi2:
  p1 = 2
& p2 = 1

 K2:
 p2 >= 1
& p1 >= 2
& 2 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #3

 Pi3:
  p1 = 3
& p2 = 1

 K3:
 p2 >= 1
& p1 >= 3
& 2 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #4

 Pi4:
  p1 = 4
& p2 = 1

 K4:
 p2 >= 1
& p1 >= 4
& 2 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #5

 Pi5:
  p1 = 1
& p2 = 2

 K5:
 p2 >= 2
& p1 >= 1
& 3 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #6

 Pi6:
  p1 = 2
& p2 = 2

 K6:
 p2 >= 2
& p1 >= 2
& 3 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #7

 Pi7:
  p1 = 3
& p2 = 2

 K7:
 p2 >= 2
& p1 >= 3
& 3 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #8

 Pi8:
  p1 = 4
& p2 = 2

 K8:
 p2 >= 2
& p1 >= 4
& 3 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 9
Local number of transitions   : 8
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #9

 Pi9:
  p1 = 1
& p2 = 3

 K9:
 p2 >= 3
& p1 >= 1
& 4 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #10

 Pi10:
  p1 = 2
& p2 = 3

 K10:
 p2 >= 3
& p1 >= 2
& 4 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #11

 Pi11:
  p1 = 3
& p2 = 3

 K11:
 p2 >= 3
& p1 >= 3
& 4 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 9
Local number of transitions   : 8
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #12

 Pi12:
  p1 = 4
& p2 = 3

 K12:
 p2 >= 3
& p1 >= 4
& 4 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 10
Local number of transitions   : 9
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #13

 Pi13:
  p1 = 1
& p2 = 4

 K13:
 p2 >= 4
& p1 >= 1
& 5 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #14

 Pi14:
  p1 = 2
& p2 = 4

 K14:
 p2 >= 4
& p1 >= 2
& 5 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 9
Local number of transitions   : 8
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #15

 Pi15:
  p1 = 3
& p2 = 4

 K15:
 p2 >= 4
& p1 >= 3
& 5 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 10
Local number of transitions   : 9
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
 Tile #16

 Pi16:
  p1 = 4
& p2 = 4

 K16:
 p2 >= 4
& p1 >= 4
& 5 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 11
Local number of transitions   : 10
"""
			} # end BC file
			,
			# NOTE: actual result
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
GENERAL STATISTICS
(************************************************************)
------------------------------------------------------------
Number of integers in v0      : 16
Number of tiles computed      : 16
Coverage                      : integer-complete
Termination                   : regular termination
Number of unsuccessful points : 0
Average number of states      : 8.0
Average number of transitions : 7.0

"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2020/09/04
		# Test for IMITATOR version: 3
		'purpose'    : 'Test BC in mode cover (grid) with step=2',
		'input_files': ['testBC-grid-plain.imi', 'testBC-grid4x4-cover-step2.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'testBC-grid-plain.res' , 'content' : """
------------------------------------------------------------
Number of integers in v0                : 4
Number of tiles computed                : 4
Coverage                                : integer-complete
Termination                             : regular termination
Number of unsuccessful points           : 0
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,


	{
		'purpose'    : 'Test BC in mode cover (grid2)',
		'input_files': ['testBC-grid2-plain.imi', 'testBC-grid5x5-cover.imiprop'],
		'options'    : '',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
 Tile #1

 Pi1:
  p1 = 0
& p2 = 0

 K1:
 p1 >= 0
& p2 >= 0
& 2 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 3
Local number of transitions   : 2
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
 Tile #2

 Pi2:
  p1 = 2
& p2 = 0

 K2:
 p1 >= 2
& p2 >= 0
& 2 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 4
Local number of transitions   : 3
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
 Tile #3

 Pi3:
  p1 = 4
& p2 = 0

 K3:
 p1 >= 4
& p2 >= 0
& 2 > p2
& 6 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
 Tile #4

 Pi4:
  p1 = 0
& p2 = 2

 K4:
 p1 >= 0
& p2 >= 2
& 4 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 4
Local number of transitions   : 3
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
 Tile #5

 Pi5:
  p1 = 2
& p2 = 2

 K5:
 p1 >= 2
& p2 >= 2
& 4 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
 Tile #6

 Pi6:
  p1 = 4
& p2 = 2

 K6:
 p1 >= 4
& p2 >= 2
& 4 > p2
& 6 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
 Tile #7

 Pi7:
  p1 = 0
& p2 = 4

 K7:
 p1 >= 0
& p2 >= 4
& 6 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
 Tile #8

 Pi8:
  p1 = 2
& p2 = 4

 K8:
 p1 >= 2
& p2 >= 4
& 6 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
 Tile #9

 Pi9:
  p1 = 4
& p2 = 4

 K9:
 p1 >= 4
& p2 >= 4
& 6 > p2
& 6 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			# NOTE: actual result
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
GENERAL STATISTICS
(************************************************************)
------------------------------------------------------------
Number of integers in v0      : 36
Number of tiles computed      : 9
Coverage                      : integer-complete
Termination                   : regular termination
Number of unsuccessful points : 27
Average number of states      : 5.0
Average number of transitions : 4.0

"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode cover + depth-limit (grid)',
		'input_files': ['testBC-grid-plain.imi', 'testBC-grid4x4-cover.imiprop'],
		'options'    : '-depth-limit 5 ',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			#{'file': 'testBC-grid-plain.res' , 'content' : """
#(************************************************************)
 #Tile #1

 #Pi1:
  #p1 = 1
#& p2 = 1

 #K1:
 #p2 >= 1
#& p1 >= 1
#& 2 > p2
#& 2 > p1

#------------------------------------------------------------
#Constraint soundness          : possible over-approximation
#Termination                   : depth limit (1 successor unexplored)
#Constraint nature             : good
#------------------------------------------------------------
#Local number of states        : 5
#Local number of transitions   : 4
#"""
			#} # end BC file
			#,
			#{'file': 'testBC-grid-plain.res' , 'content' : """
#(************************************************************)
 #Tile #2

 #Pi2:
  #p1 = 2
#& p2 = 1

 #K2:
 #p2 >= 1
#& p1 >= 2
#& 3 > p1

#------------------------------------------------------------
#Constraint soundness          : possible over-approximation
#Termination                   : depth limit (1 successor unexplored)
#Constraint nature             : good
#------------------------------------------------------------
#Local number of states        : 5
#Local number of transitions   : 4
#"""
			#} # end BC file
			#,
			#{'file': 'testBC-grid-plain.res' , 'content' : """
#(************************************************************)
 #Tile #3

 #Pi3:
  #p1 = 3
#& p2 = 1

 #K3:
 #p2 >= 0
#& p1 >= 3
#& 4 > p1

#------------------------------------------------------------
#Constraint soundness          : possible over-approximation
#Termination                   : depth limit (1 successor unexplored)
#Constraint nature             : good
#------------------------------------------------------------
#Local number of states        : 5
#Local number of transitions   : 4
#"""
			#} # end BC file
			#,
			#{'file': 'testBC-grid-plain.res' , 'content' : """
#(************************************************************)
 #Tile #4

 #Pi4:
  #p1 = 4
#& p2 = 1

 #K4:
 #p1 >= 4
#& p2 >= 0

#------------------------------------------------------------
#Constraint soundness          : possible over-approximation
#Termination                   : depth limit (1 successor unexplored)
#Constraint nature             : good
#------------------------------------------------------------
#Local number of states        : 5
#Local number of transitions   : 4
#"""
			#} # end BC file
			#,
			#{'file': 'testBC-grid-plain.res' , 'content' : """
#(************************************************************)
 #Tile #5

 #Pi5:
  #p1 = 1
#& p2 = 2

 #K5:
 #p2 >= 2
#& p1 >= 1
#& 2 > p1

#------------------------------------------------------------
#Constraint soundness          : possible over-approximation
#Termination                   : depth limit (1 successor unexplored)
#Constraint nature             : good
#------------------------------------------------------------
#Local number of states        : 5
#Local number of transitions   : 4
#"""
			#} # end BC file
			#,
			# NOTE: actual result
			#{'file': 'testBC-grid-plain.res' , 'content' : """
#(************************************************************)
#GENERAL STATISTICS
#(************************************************************)
#------------------------------------------------------------
#Number of integers in v0      : 16
#Number of tiles computed      : 5
#Coverage                      : unknown
#Termination                   : regular termination
#Number of unsuccessful points : 11
#Average number of states      : 5.0
#Average number of transitions : 4.0
#"""
			#} # end BC file
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
GENERAL STATISTICS
(************************************************************)
------------------------------------------------------------
Number of integers in v0                : 16
Number of tiles computed                : 0
Coverage                                : empty
Termination                             : regular termination
Number of unsuccessful points           : 16
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode cover with depth limit (JLR15)',
		'input_files': ['JLR-TACAS13.imi', 'JLR-TACAS13-cover.imiprop'],
		'options'    : '-depth-limit 10 ',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'JLR-TACAS13.res' , 'content' : """
(************************************************************)
 Tile #1

 Pi1:
  a = 1
& b = 0

 K1:
 a > b
& b >= 0
& 2 > b
& 10 >= a

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 1
Local number of transitions             : 0
"""
			} # end BC file
			,
			{'file': 'JLR-TACAS13.res' , 'content' : """
(************************************************************)
 Tile #2

 Pi2:
  a = 3
& b = 2

 K2:
 a > b
& b >= 2
& 10 >= a

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 2
Local number of transitions             : 1
"""
			} # end BC file
			,
			{'file': 'JLR-TACAS13.res' , 'content' : """
    Number of integers in v0                : 121
    Number of tiles computed                : 2
    Coverage                                : unknown
    Termination                             : regular termination
    Number of unsuccessful points           : 119
    Average number of states                : 1.5
    Average number of transitions           : 0.5
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode sequential + depth limit (grid with loop)',
		'input_files': ['testBC-grid-plain-loop.imi', 'testBC-grid3x3-cover.imiprop'],
		'options'    : '-depth-limit 10 ',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'testBC-grid-plain-loop.res' , 'content' : """
(************************************************************)
 Tile #1

 Pi1:
  p1 = 2
& p2 = 1

 K1:
 p2 >= 1
& p1 >= 2
& 2 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 6
Local number of transitions             : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain-loop.res' , 'content' : """
(************************************************************)
 Tile #2

 Pi2:
  p1 = 3
& p2 = 1

 K2:
 p2 >= 1
& p1 >= 3
& 2 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 7
Local number of transitions             : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain-loop.res' , 'content' : """
(************************************************************)
 Tile #3

 Pi3:
  p1 = 1
& p2 = 2

 K3:
 p2 >= 2
& p1 >= 1
& 3 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 6
Local number of transitions             : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain-loop.res' , 'content' : """
(************************************************************)
 Tile #4

 Pi4:
  p1 = 2
& p2 = 2

 K4:
 p2 >= 2
& p1 >= 2
& 3 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 7
Local number of transitions             : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain-loop.res' , 'content' : """
(************************************************************)
 Tile #5

 Pi5:
  p1 = 3
& p2 = 2

 K5:
 p2 >= 2
& p1 >= 3
& 3 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 8
Local number of transitions             : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain-loop.res' , 'content' : """
(************************************************************)
 Tile #6

 Pi6:
  p1 = 1
& p2 = 3

 K6:
 p2 >= 3
& p1 >= 1
& 4 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 7
Local number of transitions             : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain-loop.res' , 'content' : """
(************************************************************)
 Tile #7

 Pi7:
  p1 = 2
& p2 = 3

 K7:
 p2 >= 3
& p1 >= 2
& 4 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 8
Local number of transitions             : 7
"""
			} # end BC file
			,
			# NOTE: actual result
			{'file': 'testBC-grid-plain-loop.res' , 'content' : """
(************************************************************)
GENERAL STATISTICS
(************************************************************)
------------------------------------------------------------
Number of integers in v0                : 9
Number of tiles computed                : 7
Coverage                                : unknown
Termination                             : regular termination
Number of unsuccessful points           : 2
Average number of states                : 7.0
Average number of transitions           : 6.0
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode cover + graphical output (flip-flop)',
		'input_files': ['flipflop.imi', 'flipflop-cover.imiprop'],
		'options'    : '-draw-cart -graphics-source',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'flipflop.res' , 'content' : """
 Pi1:
  dG3_u = 8
& dG4_u = 3

 K1:
 dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u + dG4_u

"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
Tile #2

 Pi2:
  dG3_u = 14
& dG4_u = 3

 K2:
 dG3_u + dG4_u >= 17
& dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u
& 24 > dG3_u + dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 Tile #3

 Pi3:
  dG3_u = 17
& dG4_u = 3

 K3:
 dG3_u >= 17
& dG4_u >= 3
& 24 > dG3_u + dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
Tile #4

 Pi4:
  dG3_u = 21
& dG4_u = 3

 K4:
 dG3_u + dG4_u >= 24
& dG4_u >= 3
& 7 > dG4_u
& 24 > dG3_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
Tile #5

 Pi5:
  dG3_u = 24
& dG4_u = 3

 K5:
 dG3_u >= 24
& dG4_u >= 3
& 7 > dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
Tile #6

 Pi6:
  dG3_u = 17
& dG4_u = 7

 K6:
 dG3_u >= 17
& dG4_u >= 7
& 24 > dG3_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
Tile #7

 Pi7:
  dG3_u = 24
& dG4_u = 7

 K7:
 dG3_u >= 24
& dG4_u >= 7

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 Tile #8

 Pi8:
  dG3_u = 16
& dG4_u = 8

 K8:
 dG3_u >= 8
& dG3_u + dG4_u >= 24
& 17 > dG3_u

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
Number of integers in v0      : 644
Number of tiles computed      : 8
Coverage                      : integer-complete
Termination                   : regular termination
Number of unsuccessful points : 636
Average number of states      : 15.1
Average number of transitions : 14.1
"""
			} # end BC file
			,
			{'file': 'flipflop_cart_points_2.txt' , 'content' : """8. 9.
8. 16.
17. 7.
17. 3.
14. 3.
8. 9.
# """
			} # end tile file
			,
			{'file': 'flipflop_cart_points_8.txt' , 'content' : """17. 31.
17. 7.
8. 16.
8. 31.
17. 31.
# """
			} # end tile file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode cover with tiles limit (flip-flop)',
		'input_files': ['flipflop.imi', 'flipflop-cover.imiprop'],
		'options'    : '-cart-tiles-limit 4 ',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'flipflop.res' , 'content' : """
(************************************************************)
 Tile #1

 Pi1:
  dG3_u = 8
& dG4_u = 3

 K1:
 dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u + dG4_u

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
(************************************************************)
 Tile #2

 Pi2:
  dG3_u = 14
& dG4_u = 3

 K2:
 dG3_u + dG4_u >= 17
& dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u
& 24 > dG3_u + dG4_u

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 11
Local number of transitions   : 10
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
(************************************************************)
 Tile #3

 Pi3:
  dG3_u = 17
& dG4_u = 3

 K3:
 dG3_u >= 17
& dG4_u >= 3
& 24 > dG3_u + dG4_u

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 15
Local number of transitions   : 14
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
(************************************************************)
 Tile #4

 Pi4:
  dG3_u = 21
& dG4_u = 3

 K4:
 dG3_u + dG4_u >= 24
& dG4_u >= 3
& 7 > dG4_u
& 24 > dG3_u

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 17
Local number of transitions   : 16
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
------------------------------------------------------------
Number of integers in v0      : 644
Number of tiles computed      : 4
Coverage                      : unknown
Termination                   : tiles limit
Number of unsuccessful points : 10
Average number of states      : 12.7
Average number of transitions : 11.7
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode random (grid)',
		'input_files': ['testBC-grid-plain.imi', 'testBC-grid4x4-random.imiprop'],
		'options'    : '',
		'expectations' : [
			# WARNING: this algorithm is… random! hence no absolute guarantee to find the result (this said, a max_tries of 20 generally allows one to find all tiles with a good probability)
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 1
& p1 >= 1
& 2 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 1
& p1 >= 2
& 2 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 1
& p1 >= 3
& 2 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 1
& p1 >= 4
& 2 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 2
& p1 >= 1
& 3 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 2
& p1 >= 2
& 3 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 2
& p1 >= 3
& 3 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 2
& p1 >= 4
& 3 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 9
Local number of transitions   : 8
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 3
& p1 >= 1
& 4 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 3
& p1 >= 2
& 4 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 3
& p1 >= 3
& 4 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 9
Local number of transitions   : 8
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 3
& p1 >= 4
& 4 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 10
Local number of transitions   : 9
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 4
& p1 >= 1
& 5 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 4
& p1 >= 2
& 5 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 9
Local number of transitions   : 8
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 4
& p1 >= 3
& 5 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 10
Local number of transitions   : 9
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 4
& p1 >= 4
& 5 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 11
Local number of transitions   : 10
"""
			} # end BC file
			,
			# NOTE: actual result
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
GENERAL STATISTICS
(************************************************************)
------------------------------------------------------------
Number of integers in v0      : 16
Number of tiles computed      : 16
Coverage                      : unknown
Termination                   : regular termination

"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode random (grid2)',
		'input_files': ['testBC-grid2-plain.imi', 'testBC-grid5x5-random.imiprop'],
		'options'    : '',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 0
& p2 >= 0
& 2 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 3
Local number of transitions   : 2
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 2
& p2 >= 0
& 2 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 4
Local number of transitions   : 3
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 4
& p2 >= 0
& 2 > p2
& 6 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 0
& p2 >= 2
& 4 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 4
Local number of transitions   : 3
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 2
& p2 >= 2
& 4 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 4
& p2 >= 2
& 4 > p2
& 6 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 0
& p2 >= 4
& 6 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 2
& p2 >= 4
& 6 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 4
& p2 >= 4
& 6 > p2
& 6 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			# NOTE: actual result
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
GENERAL STATISTICS
(************************************************************)
------------------------------------------------------------
Number of integers in v0      : 36
Number of tiles computed      : 9
Coverage                      : unknown
Termination                   : regular termination
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode random (flip-flop)',
		'input_files': ['flipflop.imi', 'flipflop-random.imiprop'],
		'options'    : '',
		'expectations' : [
			# WARNING: this algorithm is… random! hence no absolute guarantee to find the result (this said, a max_tries of 200 generally allows one to find all tiles with a good probability)
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)… and to check them separately as the order is of course unknown
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u + dG4_u

"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u + dG4_u >= 17
& dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u
& 24 > dG3_u + dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 17
& dG4_u >= 3
& 24 > dG3_u + dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u + dG4_u >= 24
& dG4_u >= 3
& 7 > dG4_u
& 24 > dG3_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 24
& dG4_u >= 3
& 7 > dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 17
& dG4_u >= 7
& 24 > dG3_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 24
& dG4_u >= 7

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 8
& dG3_u + dG4_u >= 24
& 17 > dG3_u

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
Average number of states      : 15.1
Average number of transitions : 14.1
"""
			} # end BC file
			,
			# NOTE: impossible to check graphics source, as the order of the tiles is not known
			#{'file': 'flipflop_cart_points_2.txt' , 'content' : """14. 3.
#8. 9.
#8. 16.
#17. 7.
#17. 3.
#14. 3.
## """
			#} # end tile file
			#,
			#{'file': 'flipflop_cart_points_8.txt' , 'content' : """17. 31.
#17. 7.
#8. 16.
#8. 31.
#17. 31.
## """
			#} # end tile file
			#,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode random+seq',
		'input_files': ['flipflop.imi', 'flipflop-randomseq.imiprop'],
		'options'    : '',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)… and to check them separately as the order is of course unknown
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u + dG4_u

"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u + dG4_u >= 17
& dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u
& 24 > dG3_u + dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 17
& dG4_u >= 3
& 24 > dG3_u + dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u + dG4_u >= 24
& dG4_u >= 3
& 7 > dG4_u
& 24 > dG3_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 24
& dG4_u >= 3
& 7 > dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 17
& dG4_u >= 7
& 24 > dG3_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 24
& dG4_u >= 7

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 8
& dG3_u + dG4_u >= 24
& 17 > dG3_u

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
Number of integers in v0      : 644
Number of tiles computed      : 8
Coverage                      : integer-complete
Termination                   : regular termination
"""
			} # end BC file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode shuffle (grid)',
		'input_files': ['testBC-grid-plain.imi', 'testBC-grid4x4-shuffle.imiprop'],
		'options'    : '',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 1
& p1 >= 1
& 2 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 1
& p1 >= 2
& 2 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 1
& p1 >= 3
& 2 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 1
& p1 >= 4
& 2 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 2
& p1 >= 1
& 3 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 2
& p1 >= 2
& 3 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 2
& p1 >= 3
& 3 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 2
& p1 >= 4
& 3 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 9
Local number of transitions   : 8
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 3
& p1 >= 1
& 4 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 3
& p1 >= 2
& 4 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 3
& p1 >= 3
& 4 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 9
Local number of transitions   : 8
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 3
& p1 >= 4
& 4 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 10
Local number of transitions   : 9
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 4
& p1 >= 1
& 5 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 8
Local number of transitions   : 7
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 4
& p1 >= 2
& 5 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 9
Local number of transitions   : 8
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 4
& p1 >= 3
& 5 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 10
Local number of transitions   : 9
"""
			} # end BC file
			,
			{'file': 'testBC-grid-plain.res' , 'content' : """
:
 p2 >= 4
& p1 >= 4
& 5 > p2
& 5 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 11
Local number of transitions   : 10
"""
			} # end BC file
			,
			# NOTE: actual result
			{'file': 'testBC-grid-plain.res' , 'content' : """
(************************************************************)
GENERAL STATISTICS
(************************************************************)
------------------------------------------------------------
Number of integers in v0      : 16
Number of tiles computed      : 16
Coverage                      : integer-complete
Termination                   : regular termination
Number of unsuccessful points : 0
Average number of states      : 8.0
Average number of transitions : 7.0
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode shuffle (grid2)',
		'input_files': ['testBC-grid2-plain.imi', 'testBC-grid5x5-shuffle.imiprop'],
		'options'    : '',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 0
& p2 >= 0
& 2 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 3
Local number of transitions   : 2
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 2
& p2 >= 0
& 2 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 4
Local number of transitions   : 3
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 4
& p2 >= 0
& 2 > p2
& 6 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 0
& p2 >= 2
& 4 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 4
Local number of transitions   : 3
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 2
& p2 >= 2
& 4 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 4
& p2 >= 2
& 4 > p2
& 6 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 0
& p2 >= 4
& 6 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 5
Local number of transitions   : 4
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 2
& p2 >= 4
& 6 > p2
& 4 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 6
Local number of transitions   : 5
"""
			} # end BC file
			,
			{'file': 'testBC-grid2-plain.res' , 'content' : """
:
 p1 >= 4
& p2 >= 4
& 6 > p2
& 6 > p1

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
Local number of states        : 7
Local number of transitions   : 6
"""
			} # end BC file
			,
			# NOTE: actual result
			{'file': 'testBC-grid2-plain.res' , 'content' : """
(************************************************************)
GENERAL STATISTICS
(************************************************************)
------------------------------------------------------------
Number of integers in v0      : 36
Number of tiles computed      : 9
Coverage                      : integer-complete
Termination                   : regular termination
Number of unsuccessful points : 27
Average number of states      : 5.0
Average number of transitions : 4.0
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode shuffle (flip-flop)',
		'input_files': ['flipflop.imi', 'flipflop-shuffle.imiprop'],
		'options'    : '',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)… and to check them separately as the order is of course unknown
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u + dG4_u

"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u + dG4_u >= 17
& dG3_u >= 8
& dG4_u >= 3
& 17 > dG3_u
& 24 > dG3_u + dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 17
& dG4_u >= 3
& 24 > dG3_u + dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u + dG4_u >= 24
& dG4_u >= 3
& 7 > dG4_u
& 24 > dG3_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 24
& dG4_u >= 3
& 7 > dG4_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 17
& dG4_u >= 7
& 24 > dG3_u
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 24
& dG4_u >= 7

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} # end BC file
			,
			{'file': 'flipflop.res' , 'content' : """
 dG3_u >= 8
& dG3_u + dG4_u >= 24
& 17 > dG3_u

------------------------------------------------------------
Constraint soundness          : exact
Termination                   : regular termination
Constraint nature             : good
------------------------------------------------------------
"""
			} # end BC file
			,
			# NOTE: the actual result
			{'file': 'flipflop.res' , 'content' : """
Number of integers in v0      : 644
Number of tiles computed      : 8
Coverage                      : integer-complete
Termination                   : regular termination
Number of unsuccessful points : 636
Average number of states      : 15.1
Average number of transitions : 14.1
"""
			} # end BC file			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test BC in mode cover (on the case study BC vs. PRPC)',
		'input_files': ['diffBCPRPC.imi', 'diffBCPRPC-cover.imiprop'],
		'options'    : '-no-random ',
		'expectations' : [
			# NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #1

 Pi1:
  p1 = 0
& p2 = 0

 K1:
 p2 >= 0
& p1 >= 0
& 1 > p2
& 1 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 8
Local number of transitions             : 12
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #2

 Pi2:
  p1 = 1
& p2 = 0

 K2:
 p2 >= 0
& p1 >= 1
& 1 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 8
Local number of transitions             : 12
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #3

 Pi3:
  p1 = 2
& p2 = 0

 K3:
 p2 >= 0
& p1 >= 2
& 1 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 7
Local number of transitions             : 10
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #4

 Pi4:
  p1 = 3
& p2 = 0

 K4:
 p2 >= 0
& p1 >= 3
& 1 > p2
& 4 >= p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 7
Local number of transitions             : 10
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #5

 Pi5:
  p1 = 0
& p2 = 1

 K5:
 p2 >= 1
& p1 >= 0
& 2 > p2
& 1 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 7
Local number of transitions             : 11
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #6

 Pi6:
  p1 = 1
& p2 = 1

 K6:
 p2 >= 1
& p1 >= 1
& 2 > p2
& 2 > p1

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 8
Local number of transitions             : 12
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #7

 Pi7:
  p1 = 2
& p2 = 1

 K7:
 p2 >= 1
& p1 >= 2
& 2 > p2
& 3 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 7
Local number of transitions             : 10
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #8

 Pi8:
  p1 = 3
& p2 = 1

 K8:
 p2 >= 1
& p1 >= 3
& 2 > p2
& 4 >= p1

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 7
Local number of transitions             : 10
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #9

 Pi9:
  p1 = 0
& p2 = 2

 K9:
 p1 >= 0
& p2 >= 2
& 4 >= p2
& 2 > p1

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 7
Local number of transitions             : 10
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
(************************************************************)
 Tile #10

 Pi10:
  p1 = 2
& p2 = 2

 K10:
 p1 >= 2
& p2 >= 2
& 4 >= p2
& 4 >= p1

------------------------------------------------------------
Constraint soundness                    : possible under-approximation
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
Local number of states                  : 8
Local number of transitions             : 11
"""
			} # end BC file
			,
			{'file': 'diffBCPRPC.res' , 'content' : """
------------------------------------------------------------
Number of integers in v0                : 25
Number of tiles computed                : 10
Coverage                                : integer-complete
Termination                             : regular termination
Number of unsuccessful points           : 15
Average number of states                : 7.4
Average number of transitions           : 10.8
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test PRPC (on the case study BC vs. PRPC)',
		'input_files': ['diffBCPRPC.imi', 'diffBCPRPC-PRPC.imiprop'],
		'options'    : '-no-random ',
		'expectations' : [
			{'file': 'diffBCPRPC.res' , 'content' : """
BEGIN CONSTRAINT
 2 > p1
& p2 >= 0
& 2 > p2
& p1 >= 0
<good|bad>
 p2 >= 0
& p1 >= 2
& 4 >= p1
& 4 >= p2
OR
  p2 >= 2
& p1 >= 0
& 4 >= p1
& 4 >= p2
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact <good|bad> exact
Termination                             : regular termination
Constraint nature                       : good/bad
"""
			} # end BC file
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	##------------------------------------------------------------
	#{
		#'purpose'    : 'Test PRPC (old version) in mode cover with depth limit (JLR15)',
		#'input_files': ['JLR-TACAS13.imi', 'JLR-TACAS13.v0'],
		#'options'    : '-mode cover -PRP -depth-limit 10 ',
		#'expectations' : [
			## NOTE: no other way for now that checking separately the constraints (because the computation times may of course differ)
			#{'file': 'JLR-TACAS13.res' , 'content' : """
#(************************************************************)
 #Tile #1

 #Pi1:
  #a = 1
#& b = 0

 #K1:
 #2 > b
#& b >= 0
#& a > b
#& 10 >= a

#------------------------------------------------------------
#Constraint soundness                    : exact
#Termination                             : regular termination
#Constraint nature                       : good
#------------------------------------------------------------
#Local number of states                  : 1
#Local number of transitions             : 0
#"""
			#} # end BC file
			#,
			#{'file': 'JLR-TACAS13.res' , 'content' : """
#(************************************************************)
 #Tile #2

 #Pi2:
  #a = 0
#& b = 1

 #K2:
 #a >= 0
#& 9*b >= 2
#& 10 >= b
#& b >= a


#------------------------------------------------------------
#Constraint soundness                    : possible under-approximation
#Termination                             : depth limit (1 successor unexplored)
#Constraint nature                       : bad
#------------------------------------------------------------
#Local number of states                  : 18
#Local number of transitions             : 17
#"""
			#} # end BC file
			#,
			#{'file': 'JLR-TACAS13.res' , 'content' : """
#(************************************************************)
 #Tile #3

 #Pi3:
  #a = 3
#& b = 2

 #K3:
 #b >= 2
#& a >= 0
#& 10 >= a
#& 10 >= b

#------------------------------------------------------------
#Constraint soundness                    : exact
#Termination                             : regular termination
#Constraint nature                       : bad
#------------------------------------------------------------
#Local number of states                  : 2
#Local number of transitions             : 1
#"""
			#} # end BC file
			#,
			#{'file': 'JLR-TACAS13.res' , 'content' : """
#(************************************************************)
#GENERAL STATISTICS
#(************************************************************)
#------------------------------------------------------------
#Number of integers in v0                : 121
#Number of tiles computed                : 3
#Coverage                                : unknown
#Termination                             : regular termination
#Number of unsuccessful points           : 118
#Average number of states                : 7.0
#Average number of transitions           : 6.0
#"""
			#} # end BC file
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------

	#,

	#------------------------------------------------------------
	{
		'purpose'    : 'Testing state space + merging on a trivial example: -no-merge',
		'input_files': ['exActionsNonPreserved.imi'],
		'options'    : '-mode statespace -states-description -no-merge',
		'expectations' : [
			{'file': 'exActionsNonPreserved-statespace.states' , 'content' : """
		*/

  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: L1 ==>
& 2 >= x
& p >= 0
& x >= 0

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  STATE 1:
  pta: L2 ==>
& p >= 0
& x >= 2
& 2 >= p

  Projection onto the parameters:
   2 >= p
& p >= 0

  /************************************************************/
  STATE 2:
  pta: L2 ==>
& p >= 2
& x >= 2

  Projection onto the parameters:
   p >= 2

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "a"
  s_0 -> s_2 via "b"
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	,
	
	#------------------------------------------------------------
	{
		'purpose'    : 'Testing state space + merging on a trivial example: -merge',
		'input_files': ['exActionsNonPreserved.imi'],
		'options'    : '-mode statespace -states-description -merge',
		'expectations' : [
			{'file': 'exActionsNonPreserved-statespace.states' , 'content' : """
		*/

  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: L1 ==>
& 2 >= x
& p >= 0
& x >= 0

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  STATE 2:
  pta: L2 ==> 
& p >= 0
& x >= 2

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_2 via "b"
  s_0 -> s_2 via "a"
  """ 
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	,
	
	#------------------------------------------------------------
	{
		'purpose'    : 'Testing state space + merging on a trivial example: testing no option = -no-merge',
		'input_files': ['exActionsNonPreserved.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'exActionsNonPreserved-statespace.states' , 'content' : """
		*/

  DESCRIPTION OF THE STATES

  /************************************************************/
  INITIAL
  STATE 0:
  pta: L1 ==>
& 2 >= x
& p >= 0
& x >= 0

  Projection onto the parameters:
   p >= 0

  /************************************************************/
  STATE 1:
  pta: L2 ==>
& p >= 0
& x >= 2
& 2 >= p

  Projection onto the parameters:
   2 >= p
& p >= 0

  /************************************************************/
  STATE 2:
  pta: L2 ==>
& p >= 2
& x >= 2

  Projection onto the parameters:
   p >= 2

  /************************************************************/
  DESCRIPTION OF THE TRANSITIONS
  s_0 -> s_1 via "a"
  s_0 -> s_2 via "b"
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	
	,
	
	#------------------------------------------------------------
	{
		'purpose'    : 'Test the model printer',
		'input_files': ['Sched5.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'Sched5-regenerated.imi' , 'content' : """
 ************************************************************)
var
	t1_c, t1_d, t1_urgent, t1_arr_x, t2_c, t2_d, t2_urgent, t2_arr_x, t3_c, t3_d, t3_urgent, t3_arr_x, t4_c, t4_d, t4_urgent, t4_arr_x, t5_c, t5_d, t5_urgent, t5_arr_x, CPU1_urgent
		: clock;

	t4_C, t5_C
		: parameter;


(************************************************************)
 automaton Task_t1
(************************************************************)
 synclabs: t1_arr_event, t1_arr, t1_dis, t1_miss, t1_end;


loc t1_loc_idle: invariant True
	when True do {t1_urgent := 0}  sync t1_arr_event goto t1_loc_act_event;

loc t1_loc_act_event: invariant 0 >= t1_urgent
	when  t1_urgent = 0 do {t1_c := 0, t1_d := 0} sync t1_arr goto t1_loc_act;

loc t1_loc_act: invariant 8 >= t1_d stop{t1_c}
	when True do {} sync t1_dis goto t1_loc_exe;
	when  t1_d >= 8 do {} sync t1_miss goto t1_loc_miss;

loc t1_loc_exe: invariant 8 >= t1_d
& 2 >= t1_c
	when  t1_d >= 8
& 2 > t1_c do {}  sync t1_miss goto t1_loc_miss;
	when  t1_c = 2 do {} sync t1_end goto t1_loc_idle;

loc t1_loc_miss: invariant True
 end (* Task_t1 *)
(************************************************************)


(************************************************************)
 automaton Periodic_t1_arr
(************************************************************)
 synclabs: t1_arr_event;


loc t1_arr_loc_arr: invariant  8 >= t1_arr_x
	when  t1_arr_x = 8 do {t1_arr_x := 0}  sync t1_arr_event goto t1_arr_loc_arr;
 end (* Periodic_t1_arr *)
(************************************************************)


(************************************************************)
 automaton Task_t2
(************************************************************)
 synclabs: t2_arr_event, t2_arr, t2_dis, t2_miss, t2_pre, t2_end;


loc t2_loc_idle: invariant True
	when True do {t2_urgent := 0}  sync t2_arr_event goto t2_loc_act_event;

loc t2_loc_act_event: invariant  0 >= t2_urgent
	when  t2_urgent = 0 do {t2_c := 0, t2_d := 0}  sync t2_arr goto t2_loc_act;

loc t2_loc_act: invariant  20 >= t2_d stop{t2_c}
	when True do {}  sync t2_dis goto t2_loc_exe;
	when  t2_d >= 20 do {}  sync t2_miss goto t2_loc_miss;

loc t2_loc_exe: invariant  20 >= t2_d
& 5 >= t2_c
	when  5 > t2_c do {}  sync t2_pre goto t2_loc_act;
	when  t2_d >= 20
& 5 > t2_c do {}  sync t2_miss goto t2_loc_miss;
	when  t2_c = 5 do {}  sync t2_end goto t2_loc_idle;

loc t2_loc_miss: invariant True
 end (* Task_t2 *)
(************************************************************)


(************************************************************)
 automaton Periodic_t2_arr
(************************************************************)
 synclabs: t2_arr_event;


loc t2_arr_loc_arr: invariant  20 >= t2_arr_x
	when  t2_arr_x = 20 do {t2_arr_x := 0}  sync t2_arr_event goto t2_arr_loc_arr;
 end (* Periodic_t2_arr *)
(************************************************************)


(************************************************************)
 automaton Task_t3
(************************************************************)
 synclabs: t3_arr_event, t3_arr, t3_dis, t3_miss, t3_pre, t3_end;


loc t3_loc_idle: invariant True
	when True do {t3_urgent := 0}  sync t3_arr_event goto t3_loc_act_event;

loc t3_loc_act_event: invariant  0 >= t3_urgent
	when  t3_urgent = 0 do {t3_c := 0, t3_d := 0}  sync t3_arr goto t3_loc_act;

loc t3_loc_act: invariant  50 >= t3_d stop{t3_c}
	when True do {}  sync t3_dis goto t3_loc_exe;
	when  t3_d >= 50 do {}  sync t3_miss goto t3_loc_miss;

loc t3_loc_exe: invariant  50 >= t3_d
& 8 >= t3_c
	when  8 > t3_c do {}  sync t3_pre goto t3_loc_act;
	when  t3_d >= 50
& 8 > t3_c do {}  sync t3_miss goto t3_loc_miss;
	when  t3_c = 8 do {}  sync t3_end goto t3_loc_idle;

loc t3_loc_miss: invariant True
 end (* Task_t3 *)
(************************************************************)


(************************************************************)
 automaton Periodic_t3_arr
(************************************************************)
 synclabs: t3_arr_event;


loc t3_arr_loc_arr: invariant  50 >= t3_arr_x
	when  t3_arr_x = 50 do {t3_arr_x := 0}  sync t3_arr_event goto t3_arr_loc_arr;
 end (* Periodic_t3_arr *)
(************************************************************)


(************************************************************)
 automaton Task_t4
(************************************************************)
 synclabs: t4_arr_event, t4_arr, t4_dis, t4_miss, t4_pre, t4_end;


loc t4_loc_idle: invariant True
	when True do {t4_urgent := 0}  sync t4_arr_event goto t4_loc_act_event;

loc t4_loc_act_event: invariant  0 >= t4_urgent
	when  t4_urgent = 0 do {t4_c := 0, t4_d := 0}  sync t4_arr goto t4_loc_act;

loc t4_loc_act: invariant  100 >= t4_d stop{t4_c}
	when True do {}  sync t4_dis goto t4_loc_exe;
	when  t4_d >= 100 do {}  sync t4_miss goto t4_loc_miss;

loc t4_loc_exe: invariant  t4_C >= t4_c
& 100 >= t4_d
	when  t4_C > t4_c do {}  sync t4_pre goto t4_loc_act;
	when  t4_C > t4_c
& t4_d >= 100 do {}  sync t4_miss goto t4_loc_miss;
	when  t4_C = t4_c do {}  sync t4_end goto t4_loc_idle;

loc t4_loc_miss: invariant True
 end (* Task_t4 *)
(************************************************************)


(************************************************************)
 automaton Periodic_t4_arr
(************************************************************)
 synclabs: t4_arr_event;


loc t4_arr_loc_arr: invariant  100 >= t4_arr_x
	when  t4_arr_x = 100 do {t4_arr_x := 0}  sync t4_arr_event goto t4_arr_loc_arr;
 end (* Periodic_t4_arr *)
(************************************************************)


(************************************************************)
 automaton Task_t5
(************************************************************)
 synclabs: t5_arr_event, t5_arr, t5_dis, t5_miss, t5_pre, t5_end;


loc t5_loc_idle: invariant True
	when True do {t5_urgent := 0}  sync t5_arr_event goto t5_loc_act_event;

loc t5_loc_act_event: invariant  0 >= t5_urgent
	when  t5_urgent = 0 do {t5_c := 0, t5_d := 0}  sync t5_arr goto t5_loc_act;

loc t5_loc_act: invariant  200 >= t5_d stop{t5_c}
	when True do {}  sync t5_dis goto t5_loc_exe;
	when  t5_d >= 200 do {}  sync t5_miss goto t5_loc_miss;

loc t5_loc_exe: invariant  t5_C >= t5_c
& 200 >= t5_d
	when  t5_C > t5_c do {}  sync t5_pre goto t5_loc_act;
	when  t5_C > t5_c
& t5_d >= 200 do {}  sync t5_miss goto t5_loc_miss;
	when  t5_C = t5_c do {}  sync t5_end goto t5_loc_idle;

loc t5_loc_miss: invariant True
 end (* Task_t5 *)
(************************************************************)


(************************************************************)
 automaton Periodic_t5_arr
(************************************************************)
 synclabs: t5_arr_event;


loc t5_arr_loc_arr: invariant  200 >= t5_arr_x
	when  t5_arr_x = 200 do {t5_arr_x := 0}  sync t5_arr_event goto t5_arr_loc_arr;
 end (* Periodic_t5_arr *)
(************************************************************)


(************************************************************)
 automaton sched_CPU1
(************************************************************)
 synclabs: t1_arr, t2_arr, t3_arr, t4_arr, t5_arr, t1_dis, t2_dis, t3_dis, t4_dis, t5_dis, t5_end, t5_pre, t4_end, t4_pre, t3_end, t3_pre, t2_end, t2_pre, t1_end;


loc CPU1_loc_: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1;
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_At2;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_At3;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_At4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_At5;

loc CPU1_loc_At1: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1;

loc CPU1_loc_At2: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2;

loc CPU1_loc_At3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3;

loc CPU1_loc_At4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_dis goto CPU1_loc_Rt4;

loc CPU1_loc_At5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t5_dis goto CPU1_loc_Rt5;

loc CPU1_loc_Rt5: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt5;
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_At2Rt5;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_At3Rt5;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_At4Rt5;
	when True do {CPU1_urgent := 0}  sync t5_end goto CPU1_loc_Et5;

loc CPU1_loc_Et5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  (* sync nosync_1*)  goto CPU1_loc_stop;

loc CPU1_loc_At1Rt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t5_pre goto CPU1_loc_At1Wt5;

loc CPU1_loc_At1Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt5;

loc CPU1_loc_At2Rt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t5_pre goto CPU1_loc_At2Wt5;

loc CPU1_loc_At2Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt5;

loc CPU1_loc_At3Rt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t5_pre goto CPU1_loc_At3Wt5;

loc CPU1_loc_At3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3Wt5;

loc CPU1_loc_At4Rt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t5_pre goto CPU1_loc_At4Wt5;

loc CPU1_loc_At4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_dis goto CPU1_loc_Rt4Wt5;

loc CPU1_loc_Rt4: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt4;
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_At2Rt4;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_At3Rt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt4Wt5;
	when True do {CPU1_urgent := 0}  sync t4_end goto CPU1_loc_Et4;

loc CPU1_loc_Et4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  (* sync nosync_2*)  goto CPU1_loc_stop;

loc CPU1_loc_At1Rt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_pre goto CPU1_loc_At1Wt4;

loc CPU1_loc_At1Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt4;

loc CPU1_loc_At2Rt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_pre goto CPU1_loc_At2Wt4;

loc CPU1_loc_At2Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt4;

loc CPU1_loc_At3Rt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_pre goto CPU1_loc_At3Wt4;

loc CPU1_loc_At3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3Wt4;

loc CPU1_loc_Rt4Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt4Wt5;
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_At2Rt4Wt5;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_At3Rt4Wt5;
	when True do {CPU1_urgent := 0}  sync t4_end goto CPU1_loc_Et4Wt5;

loc CPU1_loc_Et4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t5_dis goto CPU1_loc_Rt5;

loc CPU1_loc_At1Rt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_pre goto CPU1_loc_At1Wt4Wt5;

loc CPU1_loc_At1Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt4Wt5;

loc CPU1_loc_At2Rt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_pre goto CPU1_loc_At2Wt4Wt5;

loc CPU1_loc_At2Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt4Wt5;

loc CPU1_loc_At3Rt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_pre goto CPU1_loc_At3Wt4Wt5;

loc CPU1_loc_At3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3Wt4Wt5;

loc CPU1_loc_Rt3: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt3;
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_At2Rt3;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt3Wt5;
	when True do {CPU1_urgent := 0}  sync t3_end goto CPU1_loc_Et3;

loc CPU1_loc_Et3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  (* sync nosync_3*)  goto CPU1_loc_stop;

loc CPU1_loc_At1Rt3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_pre goto CPU1_loc_At1Wt3;

loc CPU1_loc_At1Wt3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt3;

loc CPU1_loc_At2Rt3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_pre goto CPU1_loc_At2Wt3;

loc CPU1_loc_At2Wt3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt3;

loc CPU1_loc_Rt3Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt3Wt5;
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_At2Rt3Wt5;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t3_end goto CPU1_loc_Et3Wt5;

loc CPU1_loc_Et3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t5_dis goto CPU1_loc_Rt5;

loc CPU1_loc_At1Rt3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_pre goto CPU1_loc_At1Wt3Wt5;

loc CPU1_loc_At1Wt3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt3Wt5;

loc CPU1_loc_At2Rt3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_pre goto CPU1_loc_At2Wt3Wt5;

loc CPU1_loc_At2Wt3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt3Wt5;

loc CPU1_loc_Rt3Wt4: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt3Wt4;
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_At2Rt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t3_end goto CPU1_loc_Et3Wt4;

loc CPU1_loc_Et3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_dis goto CPU1_loc_Rt4;

loc CPU1_loc_At1Rt3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_pre goto CPU1_loc_At1Wt3Wt4;

loc CPU1_loc_At1Wt3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt3Wt4;

loc CPU1_loc_At2Rt3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_pre goto CPU1_loc_At2Wt3Wt4;

loc CPU1_loc_At2Wt3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt3Wt4;

loc CPU1_loc_Rt3Wt4Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_At2Rt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t3_end goto CPU1_loc_Et3Wt4Wt5;

loc CPU1_loc_Et3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_dis goto CPU1_loc_Rt4Wt5;

loc CPU1_loc_At1Rt3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_pre goto CPU1_loc_At1Wt3Wt4Wt5;

loc CPU1_loc_At1Wt3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt3Wt4Wt5;

loc CPU1_loc_At2Rt3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_pre goto CPU1_loc_At2Wt3Wt4Wt5;

loc CPU1_loc_At2Wt3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt3Wt4Wt5;

loc CPU1_loc_Rt2: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt2;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt2Wt3;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt2Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt2Wt5;
	when True do {CPU1_urgent := 0}  sync t2_end goto CPU1_loc_Et2;

loc CPU1_loc_Et2: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  (* sync nosync_4*)  goto CPU1_loc_stop;

loc CPU1_loc_At1Rt2: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_pre goto CPU1_loc_At1Wt2;

loc CPU1_loc_At1Wt2: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt2;

loc CPU1_loc_Rt2Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt2Wt5;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt2Wt3Wt5;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt2Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t2_end goto CPU1_loc_Et2Wt5;

loc CPU1_loc_Et2Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t5_dis goto CPU1_loc_Rt5;

loc CPU1_loc_At1Rt2Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_pre goto CPU1_loc_At1Wt2Wt5;

loc CPU1_loc_At1Wt2Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt2Wt5;

loc CPU1_loc_Rt2Wt4: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt2Wt4;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt2Wt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt2Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t2_end goto CPU1_loc_Et2Wt4;

loc CPU1_loc_Et2Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_dis goto CPU1_loc_Rt4;

loc CPU1_loc_At1Rt2Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_pre goto CPU1_loc_At1Wt2Wt4;

loc CPU1_loc_At1Wt2Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt2Wt4;

loc CPU1_loc_Rt2Wt4Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt2Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt2Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t2_end goto CPU1_loc_Et2Wt4Wt5;

loc CPU1_loc_Et2Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_dis goto CPU1_loc_Rt4Wt5;

loc CPU1_loc_At1Rt2Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_pre goto CPU1_loc_At1Wt2Wt4Wt5;

loc CPU1_loc_At1Wt2Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt2Wt4Wt5;

loc CPU1_loc_Rt2Wt3: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt2Wt3;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt2Wt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt2Wt3Wt5;
	when True do {CPU1_urgent := 0}  sync t2_end goto CPU1_loc_Et2Wt3;

loc CPU1_loc_Et2Wt3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3;

loc CPU1_loc_At1Rt2Wt3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_pre goto CPU1_loc_At1Wt2Wt3;

loc CPU1_loc_At1Wt2Wt3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt2Wt3;

loc CPU1_loc_Rt2Wt3Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt2Wt3Wt5;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt2Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t2_end goto CPU1_loc_Et2Wt3Wt5;

loc CPU1_loc_Et2Wt3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3Wt5;

loc CPU1_loc_At1Rt2Wt3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_pre goto CPU1_loc_At1Wt2Wt3Wt5;

loc CPU1_loc_At1Wt2Wt3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt2Wt3Wt5;

loc CPU1_loc_Rt2Wt3Wt4: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt2Wt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt2Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t2_end goto CPU1_loc_Et2Wt3Wt4;

loc CPU1_loc_Et2Wt3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3Wt4;

loc CPU1_loc_At1Rt2Wt3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_pre goto CPU1_loc_At1Wt2Wt3Wt4;

loc CPU1_loc_At1Wt2Wt3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt2Wt3Wt4;

loc CPU1_loc_Rt2Wt3Wt4Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t1_arr goto CPU1_loc_At1Rt2Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t2_end goto CPU1_loc_Et2Wt3Wt4Wt5;

loc CPU1_loc_Et2Wt3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3Wt4Wt5;

loc CPU1_loc_At1Rt2Wt3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_pre goto CPU1_loc_At1Wt2Wt3Wt4Wt5;

loc CPU1_loc_At1Wt2Wt3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t1_dis goto CPU1_loc_Rt1Wt2Wt3Wt4Wt5;

loc CPU1_loc_Rt1: invariant True
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_Rt1Wt2;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt1Wt3;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt1Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt1Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1;

loc CPU1_loc_Et1: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  (* sync nosync_5*)  goto CPU1_loc_stop;

loc CPU1_loc_Rt1Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_Rt1Wt2Wt5;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt1Wt3Wt5;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt1Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt5;

loc CPU1_loc_Et1Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t5_dis goto CPU1_loc_Rt5;

loc CPU1_loc_Rt1Wt4: invariant True
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_Rt1Wt2Wt4;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt1Wt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt1Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt4;

loc CPU1_loc_Et1Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_dis goto CPU1_loc_Rt4;

loc CPU1_loc_Rt1Wt4Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_Rt1Wt2Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt1Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt4Wt5;

loc CPU1_loc_Et1Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t4_dis goto CPU1_loc_Rt4Wt5;

loc CPU1_loc_Rt1Wt3: invariant True
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_Rt1Wt2Wt3;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt1Wt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt1Wt3Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt3;

loc CPU1_loc_Et1Wt3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3;

loc CPU1_loc_Rt1Wt3Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_Rt1Wt2Wt3Wt5;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt1Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt3Wt5;

loc CPU1_loc_Et1Wt3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3Wt5;

loc CPU1_loc_Rt1Wt3Wt4: invariant True
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_Rt1Wt2Wt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt1Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt3Wt4;

loc CPU1_loc_Et1Wt3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3Wt4;

loc CPU1_loc_Rt1Wt3Wt4Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t2_arr goto CPU1_loc_Rt1Wt2Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt3Wt4Wt5;

loc CPU1_loc_Et1Wt3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t3_dis goto CPU1_loc_Rt3Wt4Wt5;

loc CPU1_loc_Rt1Wt2: invariant True
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt1Wt2Wt3;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt1Wt2Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt1Wt2Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt2;

loc CPU1_loc_Et1Wt2: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2;

loc CPU1_loc_Rt1Wt2Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt1Wt2Wt3Wt5;
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt1Wt2Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt2Wt5;

loc CPU1_loc_Et1Wt2Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt5;

loc CPU1_loc_Rt1Wt2Wt4: invariant True
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt1Wt2Wt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt1Wt2Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt2Wt4;

loc CPU1_loc_Et1Wt2Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt4;

loc CPU1_loc_Rt1Wt2Wt4Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t3_arr goto CPU1_loc_Rt1Wt2Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt2Wt4Wt5;

loc CPU1_loc_Et1Wt2Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt4Wt5;

loc CPU1_loc_Rt1Wt2Wt3: invariant True
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt1Wt2Wt3Wt4;
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt1Wt2Wt3Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt2Wt3;

loc CPU1_loc_Et1Wt2Wt3: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt3;

loc CPU1_loc_Rt1Wt2Wt3Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t4_arr goto CPU1_loc_Rt1Wt2Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt2Wt3Wt5;

loc CPU1_loc_Et1Wt2Wt3Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt3Wt5;

loc CPU1_loc_Rt1Wt2Wt3Wt4: invariant True
	when True do {CPU1_urgent := 0}  sync t5_arr goto CPU1_loc_Rt1Wt2Wt3Wt4Wt5;
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt2Wt3Wt4;

loc CPU1_loc_Et1Wt2Wt3Wt4: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt3Wt4;

loc CPU1_loc_Rt1Wt2Wt3Wt4Wt5: invariant True
	when True do {CPU1_urgent := 0}  sync t1_end goto CPU1_loc_Et1Wt2Wt3Wt4Wt5;

loc CPU1_loc_Et1Wt2Wt3Wt4Wt5: invariant  0 >= CPU1_urgent
	when  CPU1_urgent = 0 do {}  sync t2_dis goto CPU1_loc_Rt2Wt3Wt4Wt5;

loc CPU1_loc_stop: invariant True
 end (* sched_CPU1 *)
(************************************************************)


(************************************************************)
 automaton OBS_dline
(************************************************************)
 synclabs: t1_miss, t2_miss, t3_miss, t4_miss, t5_miss;


loc dline_loc_nomiss: invariant True
	when True do {t1_d := 0}  sync t1_miss goto dline_loc_miss;
	when True do {t1_d := 0}  sync t2_miss goto dline_loc_miss;
	when True do {t1_d := 0}  sync t3_miss goto dline_loc_miss;
	when True do {t1_d := 0}  sync t4_miss goto dline_loc_miss;
	when True do {t1_d := 0}  sync t5_miss goto dline_loc_miss;

loc dline_loc_miss: invariant  t1_d = 0 stop{t1_d}
 end (* OBS_dline *)
(************************************************************)

(************************************************************)
(* Initial state *)
(************************************************************)

init := {

	discrete = 
		(*------------------------------------------------------------*)
		(* Initial location *)
		(*------------------------------------------------------------*)
		loc[Task_t1] := t1_loc_idle, 
		loc[Periodic_t1_arr] := t1_arr_loc_arr, 
		loc[Task_t2] := t2_loc_idle, 
		loc[Periodic_t2_arr] := t2_arr_loc_arr, 
		loc[Task_t3] := t3_loc_idle, 
		loc[Periodic_t3_arr] := t3_arr_loc_arr, 
		loc[Task_t4] := t4_loc_idle, 
		loc[Periodic_t4_arr] := t4_arr_loc_arr, 
		loc[Task_t5] := t5_loc_idle, 
		loc[Periodic_t5_arr] := t5_arr_loc_arr, 
		loc[sched_CPU1] := CPU1_loc_, 
		loc[OBS_dline] := dline_loc_nomiss,
		(*------------------------------------------------------------*)
		(* Initial discrete variables assignments *)
		(*------------------------------------------------------------*)
	;

	(*------------------------------------------------------------*)
	(* Initial continuous constraint *)
	(*------------------------------------------------------------*)
	continuous = 
		& t5_C >= 10
		& t4_C >= 10
		& 50 >= t5_C
		& 50 >= t4_C
		& t1_c = 0
		& t1_d = 0
		& t1_urgent = 0
		& t1_arr_x = 8
		& t2_c = 0
		& t2_d = 0
		& t2_urgent = 0
		& t2_arr_x = 20
		& t3_c = 0
		& t3_d = 0
		& t3_urgent = 0
		& t3_arr_x = 50
		& t4_c = 0
		& t4_d = 0
		& t4_urgent = 0
		& t4_arr_x = 100
		& t5_c = 0
		& t5_d = 0
		& t5_urgent = 0
		& t5_arr_x = 200
		& CPU1_urgent = 0
	;
}


(************************************************************)
(* The end *)
(************************************************************)
end
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,

	#------------------------------------------------------------
	# BEGIN : Test new init state section
	#------------------------------------------------------------

# 	#------------------------------------------------------------
# 	{
# 		## Test version             : 1
# 		## Test since               : 2021/03/10
# 		## Last modified            : 2021/03/10
# 		## Test disabled            : 2021/06/01
# 		## Test for IMITATOR version: > 3.0
# 		## Author 					: lbinria
# 		'author': 'lbinria',
# 		'purpose'    : 'Test init state printing - old state zone (printing)',
# 		'tags' : 'semantic, printing, init',
# 		'input_files': ['init_state/old-init-state-printing.imi'],
# 		'options'    : '-imi2IMI',
# 		'expectations' : [
# 			{'file': 'old-init-state-printing-regenerated.imi' , 'content' : """
# var
# 	i, j
# 		: discrete;
#
#
# (************************************************************)
#  automaton pta
# (************************************************************)
#  synclabs: ;
#
# loc l1: invariant True
# 	when  i = 0
# & j = 0 do {}  (* sync nosync_1*)  goto lend;
#
# accepting loc lend: invariant True
#  end (* pta *)
# (************************************************************)
#
#
# (************************************************************)
#  automaton pta2
# (************************************************************)
#  synclabs: ;
#
# loc l2: invariant True
# 	when  i = 0
# & j = 0 do {}  (* sync nosync_2*)  goto lend2;
#
# accepting loc lend2: invariant True
#  end (* pta2 *)
# (************************************************************)
#
#
# (************************************************************)
# (* Initial state *)
# (************************************************************)
#
# init := True
# 	(*------------------------------------------------------------*)
# 	(* Initial location *)
# 	(*------------------------------------------------------------*)
# 	& loc[pta] = l1
# 	& loc[pta2] = l2
#
# 	(*------------------------------------------------------------*)
# 	(* Initial discrete assignments *)
# 	(*------------------------------------------------------------*)
# 	& i = 1
# 	& j = 2
#
# 	(*------------------------------------------------------------*)
# 	(* Initial constraint *)
# 	(*------------------------------------------------------------*)
# 	 & True
#
# ;
#
#
# (************************************************************)
# (* The end *)
# (************************************************************)
# end
# 		"""
# 			 } # end result file
# 			,
# 		] # end expectations
# 	} # end test case
# 	#------------------------------------------------------------
#
# 	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/10
		## Last modified            : 2021/06/01
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test imi2IMI for initial state v3.1',
		'tags' : 'semantic, printing, init',
		'input_files': ['init_state/new-init-state-printing.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'new-init-state-printing-regenerated.imi' , 'content' : """
var 
	b
		: bool;

	k, l
		: int;

	i, j
		: rational;


(************************************************************)
 automaton pta
(************************************************************)
 synclabs: ;
 
loc l1: invariant True 
	when  b
& i = 0
& j = 0
& k = 0
& l = 0 do {}  (* sync nosync_1*)  goto lend;
 
accepting loc lend: invariant True 
 end (* pta *)
(************************************************************)


(************************************************************)
 automaton pta2
(************************************************************)
 synclabs: ;
 
loc l2: invariant True 
	when  b
& i = 0
& j = 0
& k = 0
& l = 0 do {}  (* sync nosync_2*)  goto lend2;
 
accepting loc lend2: invariant True 
 end (* pta2 *)
(************************************************************)


(************************************************************)
(* Initial state *)
(************************************************************)

init := {

	discrete = 
		(*------------------------------------------------------------*)
		(* Initial location *)
		(*------------------------------------------------------------*)
		loc[pta] := l1, 
		loc[pta2] := l2,
		(*------------------------------------------------------------*)
		(* Initial discrete variables assignments *)
		(*------------------------------------------------------------*)
		b := False, 
		k := 0, 
		l := 0, 
		i := 1, 
		j := 2
	;

	(*------------------------------------------------------------*)
	(* Initial continuous constraint *)
	(*------------------------------------------------------------*)
	continuous = 
		& True
	;

}


(************************************************************)
(* The end *)
(************************************************************)
end
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/04/16
		## Last modified            : 2021/04/16
		## Test for IMITATOR version: 3.0.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that init of a clock in discrete state section is forbidden - new init state (behavior)',
		'tags' : 'semantic, behavior, init',
		'input_files': ['init_state/init-clock-in-discrete-state-section-error.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'init-clock-in-discrete-state-section-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/04/16
		## Last modified            : 2021/04/16
		## Test for IMITATOR version: > 3.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that init of a parameter in discrete state section is forbidden - new init state (behavior)',
		'tags' : 'semantic, behavior, init',
		'input_files': ['init_state/init-parameter-in-discrete-state-section-error.imi'],
		'options'    : '-imi2IMI',
		'expectations' : [
			{'file': 'init-parameter-in-discrete-state-section-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/09
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that init of a discrete variable in discrete and continuous section at the same time is forbidden - new init state (behavior)',
		'tags' : 'semantic, behavior, init',
		'input_files': ['init_state/init-variable-at-discrete-and-continuous.imi'],
		'options'    : '',
		'expectations' : [
			{'file': 'init-variable-at-discrete-and-continuous.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

# 	#------------------------------------------------------------
# 	{
# 		## Test version             : 1
# 		## Test since               : 2021/03/04
# 		## Last modified            : 2021/05/31
# 		## Test for IMITATOR version: 3.1.0
# 		## Author 					: lbinria
# 		'purpose'    : 'Test that init of an undeclared variable is forbidden - new init state (behavior)',
# 		'tags' : 'semantic, behavior, init',
# 		'input_files': ['init_state/init-discrete-section-not-declared-error.imi'],
# 		'options'    : '',
# 		'expectations' : [
# 			{'file': 'init-discrete-section-not-declared-error.res' , 'content' : """
# Error                                   : invalid model
# 		"""
# 			 } # end result file
# 			,
# 		] # end expectations
# 	} # end test case
# 	#------------------------------------------------------------
#
# 	,


	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/03/04
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that init of a variable with a constant is accepted - new init state (behavior)',
		'tags' : 'semantic, behavior, init',
		'input_files': ['init_state/init-variable-with-constant.imi'],
		'options'    : '-mode statespace -states-description',
		'expectations' : [
			{'file': 'init-variable-with-constant-statespace.states' , 'content' : """
  STATE 1:
  pta: lend, b = True ==> 
&True

  Projection onto the parameters:
  True
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/05/27
		## Last modified            : 2021/05/31
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that init of a variable with a variable is forbidden - new init state',
		'tags' : 'semantic, behavior, init',
		'input_files': ['init_state/init-variable-with-variable.imi'],
		'options'    : '-no-var-autoremove -mode statespace -states-description',
		'expectations' : [
			{'file': 'init-variable-with-variable.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		## Test version             : 1
		## Test since               : 2021/06/21
		## Last modified            : 2021/06/21
		## Test for IMITATOR version: 3.1.0
		## Author 					: lbinria
		'author': 'lbinria',
		'purpose'    : 'Test that init a variable with another variable in continuous init section is forbidden',
		'tags' : 'semantic, behavior, init',
		'input_files': ['init_state/init-using-variable-in-continuous-error.imi'],
		'options'    : '',
		'expectations' : [
			{'file': 'init-using-variable-in-continuous-error.res' , 'content' : """
Error                                   : invalid model
		"""
			 } # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	# END : Test new init state section
	#------------------------------------------------------------


	#------------------------------------------------------------
	{
		'purpose'    : 'Test the graphical state space generation (no details)',
		'input_files': ['CUBPTA1.imi'],
		'options'    : '-mode statespace -draw-statespace undetailed -graphics-source',
		'expectations' : [
			{'file': 'CUBPTA1-statespace.dot' , 'content' : """
  s_0 -> s_1 [label="a"];
  s_1 -> s_2 [label="a"];
  s_2 -> s_3 [label="a"];
  s_3 -> s_2 [label="a"];

/* Initial state */
  s_init [shape=none, label="init"];
  s_init -> s_0;

/* Colors */

  s_0 [color=blue, style=filled];
  s_1 [color=yellow, style=filled];
  s_2 [color=blue, style=filled];
  s_3 [color=yellow, style=filled];
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test the graphical state space generation (normal)',
		'input_files': ['CUBPTA1.imi'],
		'options'    : '-mode statespace -draw-statespace normal -graphics-source',
		'expectations' : [
			{'file': 'CUBPTA1-statespace.dot' , 'content' : """
  s_0 -> s_1 [label="a"];
  s_1 -> s_2 [label="a"];
  s_2 -> s_3 [label="a"];
  s_3 -> s_2 [label="a"];

/* Initial state */
  s_init [shape=none, label="init"];
  s_init -> s_0;

/* Colors */

  s_0[fillcolor=blue, style=filled, shape=Mrecord, label="s_0|{pta : l1}"];
  s_1[fillcolor=yellow, style=filled, shape=Mrecord, label="s_1|{pta : l2}"];
  s_2[fillcolor=blue, style=filled, shape=Mrecord, label="s_2|{pta : l1}"];
  s_3[fillcolor=yellow, style=filled, shape=Mrecord, label="s_3|{pta : l2}"];
		"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	#------------------------------------------------------------
	{
		'purpose'    : 'Test the graphical state space generation (verbose)',
		'input_files': ['CUBPTA1.imi'],
		'options'    : '-mode statespace -draw-statespace full -graphics-source',
		'expectations' : [
			{'file': 'CUBPTA1-statespace.dot' , 'content' : """
  s_0 -> s_1 [label="a"];
  s_1 -> s_2 [label="a"];
  s_2 -> s_3 [label="a"];
  s_3 -> s_2 [label="a"];

/* Initial state */
  s_init [shape=none, label="init"];
  s_init -> s_0;

/* Colors */

  s_0[fillcolor=blue, style=filled, shape=Mrecord, label="s_0|{pta : l1}|{ p1 \>= x \\n \& p2 \>= 0 \\n \& x \>= 0 \\n \& x = y| p2 \>= 0 \\n \& p1 \>= 0}"];
  s_1[fillcolor=yellow, style=filled, shape=Mrecord, label="s_1|{pta : l2}|{ p1 + x \>= y \\n \& p2 \>= y \\n \& x \>= 0 \\n \& y \>= x| p2 \>= 0 \\n \& p1 \>= 0}"];
  s_2[fillcolor=blue, style=filled, shape=Mrecord, label="s_2|{pta : l1}|{ p1 \>= x \\n \& p2 \>= 1 \\n \& x \>= 0 \\n \& x = y| p2 \>= 1 \\n \& p1 \>= 0}"];
  s_3[fillcolor=yellow, style=filled, shape=Mrecord, label="s_3|{pta : l2}|{ p1 + x \>= y \\n \& p2 \>= y \\n \& p2 \>= 1 \\n \& x \>= 0 \\n \& y \>= x| p1 \>= 0 \\n \& p2 \>= 1}"];
		"""
			} # end result file
			# NOTE (ÉA, 2018/06/05): I had to manually replace '\n' with '\\n' to make this test pass
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------
	,
	##------------------------------------------------------------
	#{
		## Test version: 2.11
		## Test since  : 2019/03/07
		## Test until  : 2020/04/10
		#'purpose'    : 'Test the graphical state space generation (verbose with projection)',
		#'input_files': ['CUBPTA1project.imi'],
		#'options'    : '-mode statespace -draw-statespace full -graphics-source',
		#'expectations' : [
			#{'file': 'CUBPTA1project-statespace.dot' , 'content' : """
  #s_0 -> s_1 [label="a"];
  #s_1 -> s_2 [label="a"];
  #s_2 -> s_3 [label="a"];
  #s_3 -> s_2 [label="a"];

#/* Initial state */
  #s_init [shape=none, label="init"];
  #s_init -> s_0;

#/* Colors */

  #s_0[fillcolor=blue, style=filled, shape=Mrecord, label="s_0|{pta : l1}|{ p1 \>= x \\n \& p2 \>= 0 \\n \& x \>= 0 \\n \& x = y| p2 \>= 0 \\n \& p1 \>= 0| p2 \>= 0}"];
  #s_1[fillcolor=yellow, style=filled, shape=Mrecord, label="s_1|{pta : l2}|{ p1 + x \>= y \\n \& p2 \>= y \\n \& x \>= 0 \\n \& y \>= x| p2 \>= 0 \\n \& p1 \>= 0| p2 \>= 0}"];
  #s_2[fillcolor=blue, style=filled, shape=Mrecord, label="s_2|{pta : l1}|{ p1 \>= x \\n \& p2 \>= 1 \\n \& x \>= 0 \\n \& x = y| p2 \>= 1 \\n \& p1 \>= 0| p2 \>= 1}"];
  #s_3[fillcolor=yellow, style=filled, shape=Mrecord, label="s_3|{pta : l2}|{ p1 + x \>= y \\n \& p2 \>= y \\n \& p2 \>= 1 \\n \& x \>= 0 \\n \& y \>= x| p1 \>= 0 \\n \& p2 \>= 1| p2 \>= 1}"];
		#"""
			#} # end result file
			## NOTE (ÉA, 2019/03/07): I had to manually replace '\n' with '\\n' to make this test pass
			#,
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------

	#,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test translation to HyTech',
		'input_files': ['flipflop.imi'],
		'options'    : '-imi2HyTech -no-var-autoremove', #TODO: re-do without '-no-var-autoremove'
		'expectations' : [
			{'file': 'flipflop.hy' , 'content' : """
 -- Created to be compatible with 'hytech-v1.04f-Linux_static'
 --************************************************************
var
	s, ckG1, ckG2, ckG3, ckG4
		: clock;

	dG3_u, dG4_u
		: parameter;


--************************************************************
 automaton input
--************************************************************
 synclabs: dUp, ckUp, dDown, ckDown;
 initially Input0;

loc Input0: while  5 >= s wait{}
	when  s = 5 do {}  sync dUp goto Input1;

loc Input1: while  15 >= s wait{}
	when  s = 15 do {}  sync ckUp goto Input2;

loc Input2: while  32 >= s wait{}
	when  s = 32 do {}  sync dDown goto Input3;

loc Input3: while  39 >= s wait{}
	when  s = 39 do {s' = 0}  sync ckDown goto Input4;

loc Input4: while  0 >= s wait{}
 end -- input
--************************************************************


--************************************************************
 automaton g1
--************************************************************
 synclabs: dUp, ckUp, qG2Up, qG1Up, qG2Down, ckDown, qG1Down, dDown;
 initially G10011;

loc G10000: while  7 >= ckG1 wait{}
	when True do {ckG1' = 0}  sync dUp goto G11000;
	when True do {ckG1' = 0}  sync ckUp goto G10100;
	when True do {ckG1' = 0}  sync qG2Up goto G10010;
	when  ckG1 >= 7 do {}  sync qG1Up goto G10001;

loc G10001: while  ckG1 >= 0 wait{}
	when True do {}  sync dUp goto G11001;
	when True do {}  sync ckUp goto G10101;
	when True do {}  sync qG2Up goto G10011;

loc G10010: while  7 >= ckG1 wait{}
	when True do {}  sync dUp goto G11010;
	when True do {}  sync ckUp goto G10110;
	when True do {ckG1' = 0}  sync qG2Down goto G10000;
	when  ckG1 >= 7 do {}  sync qG1Up goto G10011;

loc G10011: while  ckG1 >= 0 wait{}
	when True do {ckG1' = 0}  sync dUp goto G11011;
	when True do {ckG1' = 0}  sync ckUp goto G10111;
	when True do {}  sync qG2Down goto G10001;

loc G10100: while  7 >= ckG1 wait{}
	when True do {ckG1' = 0}  sync dUp goto G11100;
	when True do {ckG1' = 0}  sync ckDown goto G10000;
	when True do {}  sync qG2Up goto G10110;
	when  ckG1 >= 7 do {}  sync qG1Up goto G10101;

loc G10101: while  ckG1 >= 0 wait{}
	when True do {}  sync dUp goto G11101;
	when True do {}  sync ckDown goto G10001;
	when True do {ckG1' = 0}  sync qG2Up goto G10111;

loc G10110: while  ckG1 >= 0 wait{}
	when True do {}  sync dUp goto G11110;
	when True do {ckG1' = 0}  sync ckDown goto G10010;
	when True do {ckG1' = 0}  sync qG2Down goto G10100;

loc G10111: while  7 >= ckG1 wait{}
	when True do {ckG1' = 0}  sync dUp goto G11111;
	when True do {}  sync ckDown goto G10011;
	when True do {}  sync qG2Down goto G10101;
	when  ckG1 >= 7 do {}  sync qG1Down goto G10110;

loc G11000: while  7 >= ckG1 wait{}
	when True do {ckG1' = 0}  sync dDown goto G10000;
	when True do {ckG1' = 0}  sync ckUp goto G11100;
	when True do {}  sync qG2Up goto G11010;
	when  ckG1 >= 7 do {}  sync qG1Up goto G11001;

loc G11001: while  ckG1 >= 0 wait{}
	when True do {}  sync dDown goto G10001;
	when True do {}  sync ckUp goto G11101;
	when True do {ckG1' = 0}  sync qG2Up goto G11011;

loc G11010: while  ckG1 >= 0 wait{}
	when True do {ckG1' = 0}  sync dDown goto G10010;
	when True do {}  sync ckUp goto G11110;
	when True do {ckG1' = 0}  sync qG2Down goto G11000;

loc G11011: while  7 >= ckG1 wait{}
	when True do {}  sync dDown goto G10011;
	when True do {ckG1' = 0}  sync ckUp goto G11111;
	when True do {}  sync qG2Down goto G11001;
	when  ckG1 >= 7 do {}  sync qG1Down goto G11010;

loc G11100: while  7 >= ckG1 wait{}
	when True do {ckG1' = 0}  sync dDown goto G10100;
	when True do {ckG1' = 0}  sync ckDown goto G11000;
	when True do {}  sync qG2Up goto G11110;
	when  ckG1 >= 7 do {}  sync qG1Up goto G11101;

loc G11101: while  ckG1 >= 0 wait{}
	when True do {}  sync dDown goto G10101;
	when True do {}  sync ckDown goto G11001;
	when True do {ckG1' = 0}  sync qG2Up goto G11111;

loc G11110: while  ckG1 >= 0 wait{}
	when True do {}  sync dDown goto G10110;
	when True do {}  sync ckDown goto G11010;
	when True do {ckG1' = 0}  sync qG2Down goto G11100;

loc G11111: while  7 >= ckG1 wait{}
	when True do {ckG1' = 0}  sync dDown goto G10111;
	when True do {ckG1' = 0}  sync ckDown goto G11011;
	when True do {}  sync qG2Down goto G11101;
	when  ckG1 >= 7 do {}  sync qG1Down goto G11110;
 end -- g1
--************************************************************


--************************************************************
 automaton g2
--************************************************************
 synclabs: qG1Up, ckUp, qG2Up, ckDown, qG1Down, qG2Down;
 initially G2101;

loc G2001: while  ckG2 >= 0 wait{}
	when True do {}  sync qG1Up goto G2101;
	when True do {}  sync ckUp goto G2011;

loc G2000: while  6 >= ckG2 wait{}
	when True do {ckG2' = 0}  sync qG1Up goto G2100;
	when True do {ckG2' = 0}  sync ckUp goto G2010;
	when  ckG2 >= 5 do {}  sync qG2Up goto G2001;

loc G2011: while  ckG2 >= 0 wait{}
	when True do {ckG2' = 0}  sync qG1Up goto G2111;
	when True do {}  sync ckDown goto G2001;

loc G2010: while  6 >= ckG2 wait{}
	when True do {}  sync qG1Up goto G2110;
	when True do {ckG2' = 0}  sync ckDown goto G2000;
	when  ckG2 >= 5 do {}  sync qG2Up goto G2011;

loc G2101: while  ckG2 >= 0 wait{}
	when True do {}  sync qG1Down goto G2001;
	when True do {ckG2' = 0}  sync ckUp goto G2111;

loc G2100: while  6 >= ckG2 wait{}
	when True do {ckG2' = 0}  sync qG1Down goto G2000;
	when True do {}  sync ckUp goto G2110;
	when  ckG2 >= 5 do {}  sync qG2Up goto G2101;

loc G2111: while  6 >= ckG2 wait{}
	when True do {}  sync qG1Down goto G2011;
	when True do {}  sync ckDown goto G2101;
	when  ckG2 >= 5 do {}  sync qG2Down goto G2110;

loc G2110: while  ckG2 >= 0 wait{}
	when True do {ckG2' = 0}  sync qG1Down goto G2010;
	when True do {ckG2' = 0}  sync ckDown goto G2100;
 end -- g2
--************************************************************


--************************************************************
 automaton g3
--************************************************************
 synclabs: qUp, ckUp, qG2Up, qG3Up, qG2Down, ckDown, qG3Down, qDown;
 initially G30011;

loc G30000: while  dG3_u >= ckG3 wait{}
	when True do {ckG3' = 0}  sync qUp goto G31000;
	when True do {ckG3' = 0}  sync ckUp goto G30100;
	when True do {ckG3' = 0}  sync qG2Up goto G30010;
	when  ckG3 >= 8 do {}  sync qG3Up goto G30001;

loc G30001: while  ckG3 >= 0 wait{}
	when True do {}  sync qUp goto G31001;
	when True do {}  sync ckUp goto G30101;
	when True do {}  sync qG2Up goto G30011;

loc G30010: while  dG3_u >= ckG3 wait{}
	when True do {}  sync qUp goto G31010;
	when True do {}  sync ckUp goto G30110;
	when True do {ckG3' = 0}  sync qG2Down goto G30000;
	when  ckG3 >= 8 do {}  sync qG3Up goto G30011;

loc G30011: while  ckG3 >= 0 wait{}
	when True do {ckG3' = 0}  sync qUp goto G31011;
	when True do {ckG3' = 0}  sync ckUp goto G30111;
	when True do {}  sync qG2Down goto G30001;

loc G30100: while  dG3_u >= ckG3 wait{}
	when True do {ckG3' = 0}  sync qUp goto G31100;
	when True do {ckG3' = 0}  sync ckDown goto G30000;
	when True do {}  sync qG2Up goto G30110;
	when  ckG3 >= 8 do {}  sync qG3Up goto G30101;

loc G30101: while  ckG3 >= 0 wait{}
	when True do {}  sync qUp goto G31101;
	when True do {}  sync ckDown goto G30001;
	when True do {ckG3' = 0}  sync qG2Up goto G30111;

loc G30110: while  ckG3 >= 0 wait{}
	when True do {}  sync qUp goto G31110;
	when True do {ckG3' = 0}  sync ckDown goto G30010;
	when True do {ckG3' = 0}  sync qG2Down goto G30100;

loc G30111: while  dG3_u >= ckG3 wait{}
	when True do {ckG3' = 0}  sync qUp goto G31111;
	when True do {}  sync ckDown goto G30011;
	when True do {}  sync qG2Down goto G30101;
	when  ckG3 >= 8 do {}  sync qG3Down goto G30110;

loc G31000: while  dG3_u >= ckG3 wait{}
	when True do {ckG3' = 0}  sync qDown goto G30000;
	when True do {ckG3' = 0}  sync ckUp goto G31100;
	when True do {}  sync qG2Up goto G31010;
	when  ckG3 >= 8 do {}  sync qG3Up goto G31001;

loc G31001: while  ckG3 >= 0 wait{}
	when True do {}  sync qDown goto G30001;
	when True do {}  sync ckUp goto G31101;
	when True do {ckG3' = 0}  sync qG2Up goto G31011;

loc G31010: while  ckG3 >= 0 wait{}
	when True do {ckG3' = 0}  sync qDown goto G30010;
	when True do {}  sync ckUp goto G31110;
	when True do {ckG3' = 0}  sync qG2Down goto G31000;

loc G31011: while  dG3_u >= ckG3 wait{}
	when True do {}  sync qDown goto G30011;
	when True do {ckG3' = 0}  sync ckUp goto G31111;
	when True do {}  sync qG2Down goto G31001;
	when  ckG3 >= 8 do {}  sync qG3Down goto G31010;

loc G31100: while  dG3_u >= ckG3 wait{}
	when True do {ckG3' = 0}  sync qDown goto G30100;
	when True do {ckG3' = 0}  sync ckDown goto G31000;
	when True do {}  sync qG2Up goto G31110;
	when  ckG3 >= 8 do {}  sync qG3Up goto G31101;

loc G31101: while  ckG3 >= 0 wait{}
	when True do {}  sync qDown goto G30101;
	when True do {}  sync ckDown goto G31001;
	when True do {ckG3' = 0}  sync qG2Up goto G31111;

loc G31110: while  ckG3 >= 0 wait{}
	when True do {}  sync qDown goto G30110;
	when True do {}  sync ckDown goto G31010;
	when True do {ckG3' = 0}  sync qG2Down goto G31100;

loc G31111: while  dG3_u >= ckG3 wait{}
	when True do {ckG3' = 0}  sync qDown goto G30111;
	when True do {ckG3' = 0}  sync ckDown goto G31011;
	when True do {}  sync qG2Down goto G31101;
	when  ckG3 >= 8 do {}  sync qG3Down goto G31110;
 end -- g3
--************************************************************


--************************************************************
 automaton g4
--************************************************************
 synclabs: qG3Up, qG3Down, qDown, qUp;
 initially G410;

loc G401: while  ckG4 >= 0 wait{}
	when True do {ckG4' = 0}  sync qG3Up goto G411;

loc G411: while  dG4_u >= ckG4 wait{}
	when True do {}  sync qG3Down goto G401;
	when  ckG4 >= 3 do {} sync qDown goto G410;

loc G410: while  ckG4 >= 0 wait{}
	when True do {ckG4' = 0}  sync qG3Down goto G400;

loc G400: while  dG4_u >= ckG4 wait{}
	when True do {}  sync qG3Up goto G410;
	when  ckG4 >= 3 do {} sync qUp goto G401;
 end -- g4
--************************************************************


--************************************************************
-- Initial state
--************************************************************
var init : region;

init := True
	------------------------------------------------------------
	-- Initial location
	------------------------------------------------------------
	& loc[input] = Input0
	& loc[g1] = G10011
	& loc[g2] = G2101
	& loc[g3] = G30011
	& loc[g4] = G410

	------------------------------------------------------------
	-- Initial discrete assignments
	------------------------------------------------------------

	------------------------------------------------------------
	-- Initial constraint
	------------------------------------------------------------
	 &  dG4_u >= 3
& ckG1 >= 0
& ckG2 >= 0
& ckG3 >= 0
& ckG4 >= 0
& dG3_u >= 8
& s = 0
;


--************************************************************
--* The end
--************************************************************

"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		# Test version             : 1
		# Test since               : 2021/07/05
		# Last modified            : 2021/07/05
		# Test for IMITATOR version: 3.1
		'purpose'    : 'Test translation to HyTech even when a (useless, non-existing) property file is passed',
		'input_files': ['flipflop.imi', 'nonexistingfile.imiprop'],
		'options'    : '-imi2HyTech',
		'expectations' : [
			{'file': 'flipflop.hy' , 'content' : """
var
	s, ckG1, ckG2, ckG3, ckG4
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'Test translation to Uppaal with synchronization model',
		'input_files': ['testSynchroUppaal.imi'],
		'options'    : '-imi2Uppaal',
		'expectations' : [
			{'file': 'testSynchroUppaal-uppaal.xml' , 'content' : """
/* Clocks declarations */
clock x;

/* Discrete variable declarations needed to encode IMITATOR's strong broadcast into Uppaal */
int nb__a = 3;

/* Action declarations */
broadcast chan a; /* This action is used in 3 automata: IMITATOR uses strong broadcast semantics, while Uppaal uses broadcast semantics; the correctness is ensured thanks to variable 'nb__a' */
chan b;
broadcast chan c;

	/*------------------------------------------------------------*/
	/* Initial constraint (not interpreted by Uppaal)             */
	/*------------------------------------------------------------*/
	 /*  x == 0 */
</declaration>

<template><name x="0" y="0">pta1</name><declaration>// No local declaration for automaton 'pta1'
</declaration>

<location id="id_pta0_loc0" x="0" y="0">
	<name x="0" y="-40">l1</name>
	<label kind="invariant" x="0" y="40">nb__a == 3</label></location>

<location id="id_pta0_loc1" x="200" y="0">
	<name x="200" y="-40">l2</name>
	<label kind="invariant" x="200" y="40">nb__a == 3</label></location>
 <init ref="id_pta0_loc0"/>

	<transition>
		<source ref="id_pta0_loc0"/>
		<target ref="id_pta0_loc0"/>
		<label kind="synchronisation" x="0" y="80">a!</label>
		<label kind="guard" x="0" y="40"> x == 3</label>
		<label kind="assignment" x="0" y="-40">x = 0, nb__a = 1</label>
	</transition>
	<transition>
		<source ref="id_pta0_loc0"/>
		<target ref="id_pta0_loc1"/>
		<label kind="synchronisation" x="100" y="80">b!</label>
		<label kind="guard" x="100" y="40"> x == 4</label>

	</transition>
 </template>


<template><name x="1" y="1">pta2</name><declaration>// No local declaration for automaton 'pta2'
</declaration>

<location id="id_pta1_loc0" x="0" y="0">
	<name x="0" y="-40">l1</name>
	<label kind="invariant" x="0" y="40">nb__a == 3</label></location>

<location id="id_pta1_loc1" x="200" y="0">
	<name x="200" y="-40">l2</name>
	<label kind="invariant" x="200" y="40">nb__a == 3</label></location>
 <init ref="id_pta1_loc0"/>

	<transition>
		<source ref="id_pta1_loc0"/>
		<target ref="id_pta1_loc0"/>
		<label kind="synchronisation" x="0" y="80">a?</label>
		<label kind="guard" x="0" y="40">true</label>
		<label kind="assignment" x="0" y="-40">x = 0, nb__a = nb__a + 1</label>
	</transition>
	<transition>
		<source ref="id_pta1_loc0"/>
		<target ref="id_pta1_loc1"/>
		<label kind="synchronisation" x="100" y="80">b?</label>
		<label kind="guard" x="100" y="40">true</label>

	</transition>
 </template>


<template><name x="2" y="2">pta3</name><declaration>// No local declaration for automaton 'pta3'
</declaration>

<location id="id_pta2_loc0" x="0" y="0">
	<name x="0" y="-40">l1</name>
	<label kind="invariant" x="0" y="40"> 3 &gt;= x &amp;&amp; nb__a == 3</label></location>

<location id="id_pta2_loc1" x="200" y="0">
	<name x="200" y="-40">l2</name>
	<label kind="invariant" x="200" y="40"> 3 &gt;= x &amp;&amp; nb__a == 3</label></location>

<location id="id_pta2_loc2" x="400" y="0">
	<name x="400" y="-40">l3</name>
	<label kind="invariant" x="400" y="40">nb__a == 3</label></location>
 <init ref="id_pta2_loc0"/>

	<transition>
		<source ref="id_pta2_loc0"/>
		<target ref="id_pta2_loc1"/>
		<label kind="synchronisation" x="100" y="80">c!</label>
		<label kind="guard" x="100" y="40"> x == 3</label>
		<label kind="assignment" x="100" y="-40">x = 0</label>
	</transition>
	<transition>
		<source ref="id_pta2_loc1"/>
		<target ref="id_pta2_loc2"/>
		<label kind="synchronisation" x="300" y="80">a?</label>
		<label kind="guard" x="300" y="40">true</label>
		<label kind="assignment" x="300" y="-40">x = 0, nb__a = nb__a + 1</label>
	</transition>
 </template>
<system>
// List one or more processes to be composed into a system.

system pta1, pta2, pta3;
</system></nta>
	"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'FMTV challenge: Test EF with project-result -verbose mute',
		'input_files': ['fmtv1A1-v2.imi', 'fmtv1A1-v2-EF.imiprop'],
		'options'    : '',
		'expectations' : [
			{'file': 'fmtv1A1-v2.res' , 'content' : """
BEGIN CONSTRAINT
 18126 >= 125*e2e
& e2e >= 63
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'FMTV challenge: Test EFmin',
		'input_files': ['fmtv1A1-v2.imi', 'fmtv1A1-v2-min.imiprop'],
		'options'    : '-verbose mute',
		'expectations' : [
			{'file': 'fmtv1A1-v2.res' , 'content' : """
BEGIN CONSTRAINT
 e2e >= 63
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	#------------------------------------------------------------
	{
		'purpose'    : 'FMTV challenge: Test EFmax',
		'input_files': ['fmtv1A1-v2.imi', 'fmtv1A1-v2-max.imiprop'],
		'options'    : '-verbose mute',
		'expectations' : [
			{'file': 'fmtv1A1-v2.res' , 'content' : """
BEGIN CONSTRAINT
 e2e >= 0
& 18126 >= 125*e2e
END CONSTRAINT

------------------------------------------------------------
Constraint soundness                    : exact
Termination                             : regular termination
Constraint nature                       : good
------------------------------------------------------------
"""
			} # end result file
			,
		] # end expectations
	} # end test case
	#------------------------------------------------------------

	,

	##------------------------------------------------------------
	#{
		#'purpose'    : 'XXXX',
		#'input_files': ['XXXX.imi', 'XXXX.pi0'],
		#'options'    : '-XXXX',
		#'expectations' : [
			#{'file': 'XXXX' , 'content' : """XXXX"""
			#} # end result file
			#,
		#] # end expectations
	#} # end test case
	##------------------------------------------------------------]

### THE END
]
