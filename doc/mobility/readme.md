# Thoughts on mobility

This folder and this file should receive thoughts on the issue of mobility for MEC. I started it because some ideas showed up while reading general platforms. These are very early thoughts and are prone to be either incorrect or already explored by the current litterature.

## General mobility procedure

When UE changes its Access Point (AP) - in this text, AP and base station have the same connotation - and its MEC host, a procedure should be done to make sure the application is available and active in the new MEC host, and a second procedure should make sure the UE is connected to this application. How much of this can be done before the user has changed its MEC host? What is the cost? What should be the caching policy of applications? What should be the caching policy of applications' images?

## User mobility vs application migration

### Application migration
It is not wise to migrate the whole application to another MEC host if more than one user is interacting with it. How to make sure the migration is valid for one user - and one user only - without affecting the application?

Applications sometimes interact with services that are outside the network. Can migrations affect these services?

What is the benefit of application-triggered migration, instead of network-triggered migration? Can both cohexist? Why would they?

# Related work

## Follow-me
In [Follow-me cloud](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/mobility/07399400.pdf), the cloud nodes follow users. I believe this paper is the closest to our objective.


# Proposing a strategy
Each MEC host is responsible for a certain number of MEC apps (app), each of them serving a number of UEs. Every MEC host should hold the sequence number of requests for each pair (UE, app). They communicate this sequence number to their MEC host neighbours. When a new request arrives, the MEC host verifies whether this (user,application) was already being served by a neighbour. If yes, it forwards the request to the original MEC host and then starts the migration procedure.

The migration procedure is still a difficult task in my head. How to isolate a user inside an unknown application, using only network-level tools? 
