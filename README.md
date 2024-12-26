# paw_feeder_ai
Stem project for a pet feeder with raspberry, thinkable for UI, firebase, and Azure cognitive services for image recognition 

This software is part of a STEM project for an automatic pet feeder.
The Pet feeder was built by hooking an electrict motor to a raspberry pi. The pet food is inside a pvc pipe, when the motor spin a device that looks like blades rotates and let the pet food fall through the pipe by gravity
and then delivered to tha pet's food plate. Sometime after the food has been delivered, a picture is taken of the plate and sent to Microsoft Azure Cognitive service for analysis. 
The cognitive service will tag elements found on the picture. If food is found it means that the pet did not ate the entire food. If not food is found means that our pet ate everything :)

The element connected to the electric motor that let the food to go through was designed with Fusion 3D and printed.

The motor is controlled by rapsberry pi.
