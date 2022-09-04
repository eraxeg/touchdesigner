# Parameter Executor

When doing live video, I often want to edit many parameters and trigger all of them at once. This is a simple solution to do this for a single component in TouchDesigner.

## How to use

Drag the `exec_gen.tox` into your network. Create an executor by entering the operator you want an executor for as the Operator parameter for `exec_gen`, then pulse the Create Executor button.

### Example

You have an operator `comp_a` which has custom parameters. You want to change the value of several of these at the same time. To do this, you create an executor `comp_a_exec` with the `exec_gen.tox` component. The generated `comp_a_exec` is then docked to `comp_a`. 

To stay in sync, all parameter changes that are made on `comp_a` are copied to `comp_a_exec` at the end of each frame. 

To change multiple parameters on `comp_a` and apply them all at the same time, do the parameter changes on `comp_a_exec` and pulse the Execute button on the top of the first custom parameter page. 
