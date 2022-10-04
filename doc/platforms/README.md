# Platforms for Multi-Access Edge Computing:
This part lists some platforms for MEC. ETSI also has a list of PoC's and MEC's ecossystem. Available [here](https://mecwiki.etsi.org/index.php?title=Main_Page).

## 1. OpenNESS

[OpenNESS](https://github.com/open-ness/specs) seems an usable platform. It could be used to make some tests in the Grid500 testbed. They already have an interesting 'demo' application based on emulated cameras (in a smart city): [https://github.com/OpenVisualCloud/Smart-City-Sample/tree/openness-k8s/deployment/openness](https://github.com/OpenVisualCloud/Smart-City-Sample/tree/openness-k8s/deployment/openness).

Open-ness has two distributions. [OpenNESS](https://github.com/open-ness/specs/blob/master/doc/architecture.md) is an open distribution. [Intel OpenNESS](https://networkbuilders.intel.com/university/coursescategory/open-network-edge-services-software-openness) is developed  by Intel. They even have courses about it.

OpenNESS is built on top of Kubernetes. They use "Enhanced Platform Awareness", an orchestration method that takes into consideration resources like NUMA topology, FPGA, among others.
They have a [whitepaper](https://builders.intel.com/docs/networkbuilders/edge-computing-from-standard-to-actual-infrastructure-deployment-and-software-development.pdf)

**Tools used**: Open Virtual Network for Open vSwitch (communication between apps), Kube-OVN (as CNI implementation for DPDK applications), Kubernetes.

**Offloading decision Level:** OpenNESS runs in the edge. It provides traffic steering tools so the MEC administrator can decide in the network level the offload policy. It does not limit other level decisions.

**Applications:** OpenNESS has an [application repository](https://github.com/open-ness/edgeapps/tree/master/applications) containing 15 applications by the time of this writing. The applications are related to: CDN caching, CDN transcoding, ClearBlade (synchronization, configuration, management, and deployment of IoT systems), Edge Insights Software (smart manufacturing), FPGA sample (?), MEC Location Service, OpenVINO (pedestrian and vehicles detection), Qwilt (CDN to the edge), Radisys (media server), SDEWAN CRD Controller, Smart city (media processing and analytics), telemetry, Video Analytics Services.


## 2. LightEdge:

[LightEdge](https://lightedge.io) claims to be a ETSI-compliant platform. "Re-provisioning of MME pools is avoided by intercepting relevant UE attachment, detachment, and mobility events. lightedge can keep serving users even when handovers occur.", "lightedge is in principle compatible with any standard compliant eNodeB and EPC. So far lightedge has been tested with several popular opensource 3GPP stacks including: srsLTE, Open5GS, and srsEPC."

[LightEdgeCommMag2020.pdf](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/LightEdgeIEEECommMag2020.pdf) states that LightEdge is aimed to work in the transition between 4G and 5g. LightEdge acts between the eNodeB (eNB) and the Serving Gateway (SGW). LighEdge hosts applications that can serve UE (user equipment). Users perform requests to their remote servers. LightEdge uses S1AP to capture the traffic containing these requests. LightEdge keeps a list of 3-tuples (protocol, server-side IP address, and port number) corresponding to the applications hosted by LighEdge. If a packet matches a 3-tuple in the list, the header is rewritten and the packet is redirected to an application hosted by LightEdge. They suggest a problem in the billing for 4G MEC. It happens because the Charging Trigger Function (CTF) is located in the PGW, and the LightEdge traffic does not reach the PGW. In their paper, they evaluate LightEdge using a connected, cooperative, and automated mobility (CCAM) appliaction, focusing on lane-tracking and on-road object recognition. 

**Tools used:** srsLTE, Open5GS, and srsEPC, Kubernetes, and 5G-EmPOWER

**Offloading decision Level:** LightEdge runs in the edge. It provides Traffic Rule Manager so the MEC administrator can decide in the network level the offload policy. It does not limit other level decisions.

**Applications:** Autonomous driving.

## 3. eRAM: 

[ERAM-Project](https://github.com/ERAM-Project). This platform is dedicated only to Android. There is no documentation, but we can discuss it with the Ph.D. student—here part of his manuscript when he describes the platform. Due to a lack of time, this platform was developed in a somewhat artisanal way by the student to assess his proposals. If we want to adopt this platform, it is essential to revise it to make it compatible with ETSI and cleaner in terms of code and documentation. 
A question: is [this paper](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/papers/comcom2019_nadjib.pdf) related to the project? I feel it was very similar to the piece of thesis I read.

**Tools used:** Raspberry Pi 3 Model B (RPi3) to offload computing.

**Offloading decision Level:**  eRAM uses an offloading policy executed by a middleware running in the OS of the UE. In the MEC host, another offloading middleware receives the offloading requests from the UE and performs the tasks.

**Applications:** CPUBENCH, PIBENCH and Linpack

## 4. 4G Middlebox approach
I found [this paper](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/Middleboxhotedge18.pdf) in HotEdge18. They propose MEC as middleboxes, installed in the S1 interface. They present 4 issues related to this approach: how to intercept and forward GTP packets; how to make MEC applications serve data packets that are in GTP tunnels; how to decide which traffic should be sent to MEC and which traffic should be left as it is; how to identify GTP tunnels.

Their approach uses local DNS to redirect UE's requests to the MEC (What if application uses hard coded IP's? Is that realistic?). They also keep track of the GTP tunnels of each UE in real time.

In their case, an application server running in MEC takes the place of the application server running in the cloud.

It uses [OpenAirInterface](https://www.openairinterface.org/) on its tests. Maybe it is worth taking a look.

**Tools used:** OpenAirInterface, for tests.

**Offloading decision Level:** The MEC system decides whether to offload a request or to send it to the cloud.

**Applications:** Web service, video streaming, audio streaming.

## 5. 5G Virtualized MEC Platform for IoT Applications
The paper by [Hsieh et al.](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/5GvMEC_JNCA2018.pdf) proposes the deployment of MEC as an NFV element. They implement an IoT gateway with edge computing functions. To be perfecly honest, I don't completely understand how this work was implemented. I will try to find some other papers from the same authors. I already read it 4 times. I tried my best to explain it on the paper.

**Tools used:** OVSwitch

**Offloading decision Level:** Hsieh et al. a MEC host in the gateway. They use this to implement a Traffic Offloading Function. When a UE makes a request, the gateway uses traffic information to decide whether to send the request to the local MEC host or to forward the request to the cloud.

**Applications:** IoT

## 6. LightMEC
[LightMEC](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/lightMECCNSM2018.pdf) is a prototype that follows ETSI architecture. This platform sits in the agregation points, intercepting the packets in the GTP tunnels. They use the messages exchanged in the attach and handover procedures to know the state of UE and to properly forward incoming packets. They have some mobility management.
Unfortunately, I could not find the source code. 

**Tools used:** Docker and Click unikernel for virtualization infrastructure; Click modular router to realize the services of the mobile edge platform; OpenFlow virtual switch to route traffic between the architecture elements,  Kubernetes, 5g-EmPOWER (mobile edge platform manager), lightMANO (orchestrator); srsLTE and nextEPC to emulate the network on tests.

**Offloading decision Level:** The system does not decide where to run and leaves the decision to some other entity.

**Applications:** Nothing =(

## 7. Picasso - Information-Centric MEC plaftorm for community mesh network
From the title of the [paper](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/PiCasso_SIGCAS2018.pdf) is possible to infer that this platform is not suitable (or at least, optimised) for 5G environment. Anyway, I added it to the paper, because it calls itself MEC and does an interesting job.

**Tools used:** Raspberry Pi 3, Hypriot OS, and Docker (to build the Service Execution Gateways); and NDN (Named Data Networking as an ICN implementation, to discover services).

**Offloading decision Level:** PiCasso runs on constrained and unreliable gateways, using an algoritm named HANET (HArdware and NETwork Resources). HANET uses information about the network bandwidth, node availability, and network resources to decide the best nodes to act as MEC hosts.

**Applications:** services delivery in a ICN.

## 8. MEC-ConPaaS
[MEC-ComPaaS](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/MECConPaaS2017.pdf) uses Raspberry PI's to make a very "primitive" MEC platform, using containers provided by LXC and orchestrated by OpenStack. MEC-ConPaaS works as a middleware between applications and the virtualized infrastructure. They model MEC applications as a collection of services and built a prototype that offers a number of popular services (SQL and non-SQL databases, web servers, map-reduce). Developers deploy their applications informing MEC-ComPaaS about the services they use. MEC-ComPaaS then instantiates the services, provisioning the containers and provisioning the elasticity.

**Tools used:** Raspberry Pi, LXC, OpenStack

**Offloading decision Level:** MEC-ConPaaS models each application as a collection of services. In this model, an application can be a web server, a database and some other service, provided by the application developer. The middleware layer of MEC-ConPaaS then decides the services each MEC host should run, based on the applications requested by the users. 

**Applications:** face recognition in a live video stream.

## 10. M^2EC
[M^2EC](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/zanziM2ECWCNW.pdf) is an orchestrator fo MEC systems. It is not a complete system, but can be integrated to other tools and provide a system. They propose a MEC Broker, an entity that can grant privileges for MEC tenants (i.e., third-party developers) over the infrastructure. The broker exposes to users the Mm1, Mm2 and Mm8 interfaces. This allows users to have access to the MEC orchestrator and to the MEC platform manager. Different users have different privileges and the broker decides which requests to fulfill based on the privileges and policies related to each user. MEC Broker is to be located between the UE and the rest of the ETSI architecture. M^2EC is, therefore, designed to change the ETSI architecture and the way applications interact with it. In this sense, it is reasonable to affirm that M^2EC is not ETSI-compatible. The authors suggest, though, that the broker can be implemented as an extension of MEC orchestrator, MEC platform, and the User APP LCM proxy or as an extension of the CFS portal or OSS. In that case, the solution could be ETSI compatible.

**Tools used:** no info

**Offloading decision Level:**  The MEC broker proposed by M^2EC exposes the ETSI MEC interfaces to the tenants. This means that the offloading decision can be performed by the UE, either the application or the OS level.

**Applications:** no info

## 11. ACACIA – Context-aware Edge Computing for Continuous Interactive Applications over Mobile Networks
ACACIA is a system developed for applications that demand continuous interaction. ACACIA offers a PaaS to these applications, but it also offers data to applications. Authors claim these information can lower even more the latency between UE request and the answer from the MEC.

**Tools used:** LTE-direct D2D (obtain user context), Open vSwitch (steer traffic from UE to the applications running on MEC), Ryu Controller (managing GTP flow rules), OpenEPC.

**Offloading decision Level:** ACACIA has a device manager installed in the UE. This manager discovers the available MEC services and informs them to the applications, based on preferences registered by the users. This means that ACACIA supports two levels of orchestration: it supports the OS and the application level, since the device manager and the applications must cooperate to decide whether or not the tasks are offloaded to the MEC.

**Applications:** Augmented reality

## 12. P4EC
[P4EC](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/p4ec_hotedge2020.pdf) does not directly claim to be a MEC platform. Nevertheless, it works on 4G and selects traffic to take a fast path in the network, avoiding the EPC. It is a middlebox. Their presentation is [available online](https://www.usenix.org/conference/hotedge20/presentation/hollingsworth).

**Tools used:** NextEPC, OpenVPN (create a private network between the eNB and the cloud-EPC)

**Offloading decision Level:** Their middlebox decides whether to send the packets through the EPC or straight to the internet.

**Applications:** traffic offload

## 13. NFV over MEC
The prototype by [Carella et al](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/NFV_MEC_OpenBaton_NetSoft2017.pdf) aims to integrate use a infrastructure MEC to deploy Virtual Network Functions (VNFs)~\cite. Their work implements an interface that allows the Management and Orchestration (MANO) domain to instantiate containers in the MEC infrastructure to run VNFs as MEC applications.

**Tools used:** Open Baton MANO, Docker.

**Offloading decision Level:** it owrks as a MANO, so it orchestrates at the edge.

Watch out! Not an implementation. I added something in the text, saying it is an architecture enhancement.

**Applications:** -

## 14. Mano+: A double-tier MEC-NFV Architecture
The paper by [Sciancalepore et al](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/mano_plus_CSCN2016.pdf) describes an architecture to deploy a MEC system as a VNF, named Mano+. The system is never implemented. The MEC VNF is capable of deploying MEC applications, that are VAF (Virtual Application Functions). While the NFV MANO orchestrates the VNFs, the MEC orchestrates the VAFs. This aproach makes it possible that MEC and NFV share the same infrastructure. Additionally, since NFV MANO and MEC are aware of each other, they can cooperate to achieve different levels of optimization.

**Applications:** Network QoS, gaming, user mobility (not developed)

## 15. Cattaneo et al.
This work proposes a modification into the NFVO to allow the deployment of MEC applications.
They run a video application thata runs in the cloud. There is also a device-level module.
The work compares itself with the work from Sciancalepore et al., claiming that it can be combined with other NFVO's, unlike MANO+.
It uses a “Distributed SGW with Local Breakout (SGWLBO)” approach. I should understand this better. This paper focus in the deployment of a MEC app. The MEC implementation expects a MEC application package and a descriptor of the application (AppD).

**Tools used:** Open Baton (as NFVO and life cycle management for the MEC platform and apps), KVM (as NFVI), OpenStack Pike (as VIM), Athonet's SGWLBO VNF and the Element Management System (as MEC platform and dataplane).

**Offloading decision Level:** -

**Applications:** Italtel i-Enhanced Video System (EVS), a MEC application that provides video services to consumers that are in crowded events. Video is uploaded to the edge, reducing the upload time. Then, the edge can transcode the video if needed, using dedicated GPUs.


# Edge, but not MEC systems
The following systems are meant to be edge computing, but not necessarily MEC. They are listed here because they share many aspects with MEC systems and might give usefull insight on MEC systems.

## 1. StarlingX
[StarlingX](https://www.starlingx.io) is an opensource cloud orchestrator optimized for edge environment. It is based on OpenStack and could be our choice to develop a contribution. It does not claim to be a MEC, but it is targeted at 5G.  There is some relationship between OpenNESS and StarlingX in the beginning of their develpment.

## 2. KubeEdge
[KubeEdge](https://gitlab.inria.fr/pcruzcam/pythia/-/blob/master/doc/platforms/papers/kubeedge.pdf) is a Kubernetes-based edge computing solutions. It is opensource and their website can be found [here](https://kubeedge.io/en/). KubeEdge works on the seamless integration of application components that run in the clound and in the application components that run in the edge. To solve the conectivity problem between different application components, KubeEdge provides KubeBus, a virtual network to make the components adressable to each other. An interesting remark is that KubeEdge makes sure that edge nodes work properly even when connectivity to the cloud is limited or inexistent.

## 3. Kubefed
[Kubefed](https://github.com/kubernetes-sigs/kubefed) is a tool to deploy Kubernetes on a federation of clusters. It is designed to use heterogeneous and geographically distributed clusters to build a virtually unique Kubernetes instance. Kubefed it not inherently  connected to edge computing, since the hosts can be far from the edge. Nevertheless, the edge computing research community works on different ways to bring Kubefed to the edge. [Larsson et al.](https://ieeexplore.ieee.org/abstract/document/9302768?casa_token=PuRn93Mq7iIAAAAA:PYMzIwm4jzd7bt_3gQBsh0sDRlqU0tVZOideF5i5HRSfrk8Xy-lLOwpJrqbBKfgot9xxmREsXjGB), for instance, propose a strategy do decentralize the control of Kubefed, mitigating scaling problems related to the bottleneck of a centralized controller.

## 4. Baetyl
[Baetyl](https://github.com/baetyl/baetyl) is an edge computing framework from the Linux Foundation. Its objective is to integrate the cloud and edge devices seamlessly from the point of view of the application. Baetyl is capable of managing cloud and edge resources, and its architecture includes a cloud management module and an edge management module. Therefore, cloud and edge hosts are treated separately. According to its documentation, Baetyl can offer low-latency computing services for device connection, message routing, remote synchronization, function computing, video capture, AI inference, and status reporting.

## 5. Submariner
[Submariner](https://github.com/submariner-io/submariner) provides connectivity to different kubernetes instances.

**Tools used:** K3S, the light kubernetes.

# Commercial platforms

In this section, I am listing a few commercial platforms. Since they are strictly commercial, their developers make available information about their functionality, but not about their inner mechanisms. These platforms are listed by [Dalia Adib](https://stlpartners.com/edge-computing/edge-computing-companies-2020/).

## 1. Mutable
The platform [Mutable](https://mutable.io) is a public edge cloud (not MEC) claiming to be able to deliver applications related to AR/VR, IoT, drone, autonomous vehicles and cloud gaming. They build a PaaS using operators' and service providers' underutilized resources. Mutable is composed by a MutableOS, a Mutable node, a Mutable mesh and a Mutable k8s plt. The MutableOS is a NixOS-based operating system to manage and orchestrate containers in multiple datacenters; Mutable mesh deploys a VPN to enable communication between nodes and data sources; Mutable k8s plt is a kubernetes cluster for developers to deploy their applications.

## 2. MobiledgeX

[MobiledgeX](https://www.mobiledgex.com/product/architecture) provides a PaaS that aggregates operators' edge and cloud resources, offering these resources to developers on a transparent way, as if it was a single cloud. MobiledgeX uses its Distributed Matching Engine to deploy applications to optimal locations, according to their definition of optimallity.

## 3. Affirmed Cloud Edge
According to the architecture presented [in their website](https://www.affirmednetworks.com/products-solutions/mec-solutions/), their solution is an ETSI-compliant MEC platform. It remains unclear what is exposed to the developer, but their cloud edge sits on S1, intercepting data and sending it to MEC applications.

## 4. Section
[Section](https://www.section.io) offers an edge PaaS. developers place their application, Section decides where to place them. Section uses kubernetes to offer containers. They claim that their edge can reduce latency up to 7 times. One interesting thing is that they offer a 'developer' plan, where one can deploy an application for free. Maybe a nice test.

## 4. Equinix metal
Equinix metal offers the physical infrastructure for cloud and edge computing. Latency derived from communication is not a focus on their [whitepaper](https://metal.equinix.com/white-paper/ESG-White-Paper-Equinix.pdf?utm_campaign=ESG%20Whitepaper%20&utm_medium=email&_hsmi=100393677&_hsenc=p2ANqtz-8gR9ujJXQQ3VhLozeSw5qS8AgKfR0shQaGVEggebTC6-ljJHsL4AMJFEw6ZoBgETnhPfenfuTqZcc7R0SR3Wd6XdTaXGjec77KmfXsa7pe0wYl5Cc&utm_content=100393677&utm_source=hs_automation)

## 5. Wind River Titanium Cloud
(Wind River Titanium Cloud)[https://www.windriver.com/products/titanium-cloud/] is a commercial distribution of StarlingX. The product integrates OpenStack services to deliver a virtualization system more suited to the needs of MNOs.



## -. Oncite
[Oncite](https://oncite.io) is a german company that offers industrial edge solutions. They don't seem to be ready to receive 3rd party applications. Funny thing: their website offers the language options DE and EN, but everything is in DE anyway.

## -.EdgeInfra
[EdgeInfra](https://www.edgeinfra.net) is focused on hardware and physical infrastructure.

## -. EdgeConneX
[This company](https://www.edgeconnex.com/data-centers/edge/) offers physical infrastructure for edge computing.

## -. EdgeX Foundry
This platform connects to IoT objects and provides services related to the command and control of devices, data storage, and data processing on the edge.
This tool is very IoT-specific, I am not sure we should stick to it.

## -. Ericsson's Edge Gravity
This initiative was stopped by Ericsson. It is here on this list, but it should not be anywhere else.

# Not platforms, but relevant work

### The Unavoidable Convergence of NFV, 5G, and Fog: A Model-Driven Approach to Bridge Cloud and Edge
[Van Lingen et al.](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8004150) propose an architecture to integrate cloud and fog resources as a same service, to be prospected by the applications.

### Latency and availability driven VNF placement in a MEC-NFV environment
[This](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8647858&tag=1) is not a platform, but an optimization method for NFV placement that takes into account the latency. I believe it is strongly related and could be mentioned in our paper.

### Cost-Efficient NFV-Enabled Mobile Edge-Cloud for Low Latency Mobile Applications
[Yang et al.](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8247219&tag=1) propose a method for MEC server alocation on a NFV-based MEC plaftorm. This is not a platform at all, so why is it here? These guys developed a method that supports MEC mobility, but that is only valid if applications are stateless. This will be important for us in the future.

### SimGrid
Simulation of cloud-edge environment.

### MAUI
[MAUI](https://dl.acm.org/doi/abs/10.1145/1814433.1814441?casa_token=MKhn8gegdS8AAAAA:88RPXL5C7LmdLkZda_qICFNLmG2dj6e33I17OsKsA9VMgeYdXV48KDuk5iRAhOd0jfjyEs-or28HCEs) splits the code of an smartphone application and decides which methods should be executed in the cloud and which methodes should e executed in the smartphone itself.


# Approaches
In this section, I'll try to propose a classification the approaches we see in the litterature.

## Server reroute
In this approach, the MEC receives UE requests as if the MEC was the server in the cloud. Since MEC is closer to the edge, it is able to answer requests with less networking-related delay.  LightEdge follows this approach.

## Application-aware
Application-aware approaches leave to the application running in the UE the role of deciding whether and when to use the MEC. In this scenario, applications would have to re-architected from the paradigm UE-cloud to a paradigm UE-MEC-Cloud. This means that new applications can take the full potential of the MEC, but old applications are not able to profit from MEC.

## OS aware
