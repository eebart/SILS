# Stepwise:
#### Step 1: toCausal
* Loads vensim model
* Gets the variable names
* Makes graph from varnames
* Finds causes for each variable
* Adds them to the nodes
* Saves the graphthing into a cpickle file
#### Step 2: Loopset (containing SILS) 
*Requires partitions.py functions*

* Opens the pickle file with network/graph info
* Removes some time variables
* Does something with the graphs
* Finds the shortest independent loop set (SILS)
* Prints all SILs
	
#### Step 3: Find Atomic Behaviors of default model
#### Step 4: Change Models to turn off loops
#### Step 5: find atomic behaviors for new models for each timeinterval
	

Extra info:
Github Quaquel - Vensim DLLwrapper https://github.com/quaquel/EMAworkbench/blob/09375629d0067211b9ddf1afefa2b5d332840bb5/src/ema_workbench/connectors/vensimDLLwrapper.py
	
External functions:
https://www.vensim.com/documentation/index.html?25845.htm
	
