This directory stores Pythia Emulation Engine (PEE).

The documentation in this directory is about the tool, while the documentation in the Pythia project explains the role Pythia Emulation Engine plays.

# Models and objects
PEE works with a number of models, that represent different elements of the emulation.

## MEC application
An application that Pythia emulates, running them on MEC hosts. It represents a 3rd party application that a MEC system executes. Inside PEE, it is a class that stores the attributes needed to run the application accordingly.

## MEC host
A MEC host is a host capable of running MEC applications. It is implemented as a set of containers that suffer the same effects from the network.

## UE application
An application that Pythia emulates, running them on MEC hosts. In real life, it is a 3rd party application. Inside PEE, it is a class that stores the attributes needed to run the application accordingly.

## UE host
Is a host capable of running UE applications. It is implemented as a set of containers that suffer the same effects from the network. UE hosts emulate the mobility.

# Tasks of Pythia Emulation Engine

## Instalation of pre-requisites
Pythia must install Docker in the host. Additionally, it must install the python libs for Docker and netem.

## Instalation of hosts
First PEE must instantiate a container for each application. Then, PEE must install the .apk in the respective android containers.

## Start the data collection
PEE must start storing the packets.

## Start the network
PEE must install the initial network configuration.

## Starting the applications
PEE must start the applications.

## Start the emulation
PEE must start the network emulation.

## End the emulation
PEE must end the network emulation.

## Stop the applications
PEE must stop all the applications.
