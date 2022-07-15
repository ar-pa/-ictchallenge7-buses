# Buses
A simple simulation for how buses can transmit their offline data and delivering it to the center.

## Implementation
* We start by creating a random graph of the buses.
* Then we run a bfs and remove redundant edges in the graph. This decreases the number of transmitted transactions from 19G to 2G. 
* Then we start the simulating.

Documentation is available in the code.

## Future works
* Adding a feature to control the tradeoff between speed of delivery and size of transmitted data.  