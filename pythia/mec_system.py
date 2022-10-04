"""This file is part of Pythia. It represents a MEC system."""
import docker
import pythia.structures

class MECSystem:
  """This class represents a MEC System and its entities"""
  def __init__(self, mec_hosts):
    self.mec_hosts = mec_hosts
    self.MEO = MultiAccessEdgeOrchestrator(mec_hosts)

class MultiAccessEdgeOrchestrator:
  """This class holds information about MEC hosts, 
  deciding where to instantiate every MEC application"""
  def __init__(self, mec_hosts):
    self.start = True

  def instantiate(self, mec_hosts, mec_app, ue, ue_position):
    """This method instantiates MEC application
    mec_app in a MEC host under the request of ue.
    ue_position = (x, y)"""

    #Decide which mec host should run the app

    #Verify whether the app is instantiated in the mec host

    #if not, start the app
    #set
    return 0

