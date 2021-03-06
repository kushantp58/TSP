# TSP(Travelling Salesman Problem using Metallurgy analogy of Annealing)

> Documentation by Kushant Patel [MASC Mechatronics, University of Waterloo]


## Please read this before execution of the code

### Import useful libraries
```
math,random,time,sys,matplotlib.pyplot.
use pip install matplotlib
```

### Some useful declarations -

**file_change** - you can use this to set file path you want to check this code with

**number_of_iterations** - set the number of iterations you want to use

**plot** - set this to 1 if you want to view detailed plot of travelling salesman problem

 **cooling factor , temperature start , temperature end** - change these to change your default annealing schedules.

A container class for place-

	a) __init__ - constructor with name,lattitudes and longitude.
	b) __str__ and __repr__- used for representation of strings.
	c) euc_dist - used for finding euclidean distance.
	d) euc_dist_km - used for finding distance to another city using precomputed distance.
## Member functions

**io_file** - your input/output function to be used for files, returns the places

**places_dist_pair** - used for computations of pairs of all distances

**pmap**- used for plotting of all locations

**dplot** - used for plotting of updated distance values

**swap_dist** - used for computation of distance after swapping of locations

**s_ann** - taking all parameters necessary for annealing algorithm.

## Description of the algorithm and code

This concept depicts simulated annealing, a combinatorial optimization technique which is used for 
finding global minimum of function. It's analogous to metallurgical process of annealing where metals
are heated to a relatively high temperature and gradually cooled down to reduce defects in them.Similarly,
we are using this to find global minimum.Applying this to travelling salesman problem which is from NP hard
space.The method of annealing is used to find precise solutions, tuning the parameters of the algorithms, we
can find an optimal path.
A Temperaure variable is used for determining the probability.At higher values of T, uphill moves are more likely
to occur. As T reduces to zero, moves become more and more unlikely, till the algorithm behaves like hill climbing.
In this optimization technique, T starts high and gradually decreased according to the annealing scehdule.

k is the boltzmann's constant relating temperature to energy..

## Algorithm
```
costprevious = infinite
temperature = temperature_start
while temperature > temperature_end:
    costnew = cost_function(...)
    difference = costnew - costprevious
    if difference < 0 or  e(-difference/temperature) > random(0,1):
        costprevious = costnew
    temperature = temperature * cooling_factor

```
[References used - Optimization by Simulated Annealing by Kirkpatrick, 1984]

## Travelling Salesman Problem
A famous problem of minimization, which invovles minimizing distance travelled by salesman during his travel
from a place A to place B.Cost function is this distance which needs to be minimized. 

Procedure of solving TSP
```
- Initialize a list of cities by shuffling the input list.
- Swap the cities in the list at every iteration
- Calculate distance travelled by using the cost function for whole tour
- Check the distance before and after swap
- If new distance > previous distance:
					keep it
   else:
	Keep it with certain probability.
- Modify/update the temperature by gradually cooling it down at every iteration
```
### Observations and conclusion
This algorithm seems convincing at finding optimal solutions for optimizations,however the 
parameters of the algorithm are very sensitive, finding those parameters is not easy.Implementation
of decay of starting temperature at every restart can be used for reducing randomness during convergence
of the solution. A global convergence should also appear in addition to convergence observed iin the 
boundaries of single iteration.
	
 
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
