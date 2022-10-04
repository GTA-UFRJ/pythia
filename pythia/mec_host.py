"""This file is part of Pythia. It represents a MEC Host."""
import docker
import pythia.structures

class MECPlatform:
  """This class represents a MEC Platform, as defined by IETF.
  It is responsible for:
  - Traffic Rules Control;
  - DNS Handling;
  - Service registry;
  - MEC services."""

  def __init__(self, dns_service_name, dns_image_path):
    self.dns_image_name = dns_service_name
    self.dns_image_path = dns_image_path

    self.dns_instantiated = False
    self.dns_ip = ""

  def instantiate_dns(self):
    #Build dns image
    docker.build(path=self.dns_image_path,
                 tag=self.dns_image_name)

    #start dns server
    return 0


  def set_traffic_rules_and_dns(mec_host, application):
    print("todo")

class MECPlatformManager:
  """This class represents a MEC Platform Manager, as defined by IETF.
  It is responsible for:
  - MEC platform element management;
  - MEC app rules and requirements management;
  - MEC app life cycle management;
  - MEC services."""

  def __init__(self):
       return 0

  def start_application(app):
        #todo
        return 0

class VirtualizationInfrastructureManager:
  """This class represents the Virtualization Infrastructure
  Manager, as defined by IETF.
  It is responsible for:
  - Communication between Pythia and the manager."""

  def start_container(image):
      #todo
      return 0

class VirtualizationInfrastructure:
  """This class represents a Virtualization Infrastructure, as defined by IETF.
  It is responsible for nothing, for the moment."""
  def __init__(self):
    return 0

class DataPlane:
  """This class represents a Data Plane,
  as defined by IETF.
  It is responsible for:
  - Data plane between MEC applications."""
  def __init__(self):
    return 0

class MECHost:
  """This class represents a Pythia MEC Host.
  It holds all the entities that a MEC Host should have."""

  def __init__(self):
    self.platform = 0
    self.platform_manager = MECPlatformManager()
    self.virtualization_infrastructure_manager = VirtualizationInfrastructureManager()
    self.virtualization_infrastructure = VirtualizationInfrastructure()
    self.data_plane = DataPlane()