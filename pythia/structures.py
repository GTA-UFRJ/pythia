"""This file is part of Pythia. It stores classes that represent
the entities that Pythia emulates."""
import docker
from operator import itemgetter
import ipaddress
import pythia.id_converter as id_converter

class DockerContainer:
  """Represents everything that should be a docker container"""
  def __init__(self, image):
    self.id = id(self)
    self.id_str = id_converter.encode(self.id)
    self.image = image


class PythiaApp(DockerContainer):
  def __init__(self, name, image, command="", volume = False):
    super().__init__(image)
    self.host = None
    self.name = name
    self.command = command
    self.docker_id = ""
    self.ip = ""
    self.volume = volume
    
class PythiaServerApp(PythiaApp):
  def __init__(self, name, image, ip, command="", volume = False):
    super().__init__(name, image, command, volume)
    self.docker_id = "Server-" + self.id_str
    self.ip = ip
    
class PythiaMECApp(PythiaApp):
  def __init__(self, name, image, ip, host, command="", volume = False):
    super().__init__(name, image, command, volume)
    self.docker_id = "MECApp-" + self.id_str
    self.ip = ip
    self.host = host

class PythiaUEApp(PythiaApp):
  def __init__(self, name, image, command="", volume = False):
    super().__init__(name, image, command, volume)
    self.docker_id = "UEApp-" + self.id_str

class PythiaEmulationHost(DockerContainer):
  """A host represents either an UE or a MEC Host.
  It holds the applications that are subjected to the same 
  network requirements."""
  def __init__(self, name, image=None):
    super().__init__(image)
    self.name = name
    self.image = image
    self.command = ""
    self.stub_name = self.name
    #The ip to connect to other Hosts
    self.infra_ip = ""
    #The ip to connect to MEC/UE apps
    self.external_ip = ""
    self.docker_id = "" # id or name in docker
    self.queue_name = {}

  def add_new_peer(self, other_ip):
    self.queue_name[other_ip] = f"1:{len(self.queue_name)+1}"



class PythiaUEHost(PythiaEmulationHost):
  """A UE host represents the User Equipment. It must be capable
  of emulating the network aspects of UE mobility. The network
  characteristics are stored here.
  Every position in positions is a tuple (instant,lat,lng).
  Every link is a link to a MEC host.
  Every contact is a contact to a base station, in the format (instant, base_name)."""
  def __init__(self, name, positions_file):
    super().__init__(name)
    self.apps = []
    self.links = []
    self.contacts = []
    self.positions_file = positions_file
    self.positions = []
    self.docker_id = "vUE-" + self.id_str

  def clean_contacts(self):
    """This method sorts and eliminates repeated
    information from the contacts."""
    if not self.contacts:
      return
    sorted_contacts = sorted(self.contacts,key=itemgetter(0))
    self.contacts = [sorted_contacts[0]]
    for i in range(1, len(sorted_contacts)):
      if self.contacts[-1][1] != sorted_contacts[i][1]:
        self.contacts.append(sorted_contacts[i])

  def build_links_from_contacts(self,
                                latency,
                                upload,
                                download):
    """This method adds to self.links
    the links in contacts, with the values of latency, 
    upload, and download from the arguments. It 
    executes self.clean_contacts as first step."""
    self.clean_contacts()
    for c in self.contacts:
      self.links.append(PythiaLink(self.stub_name,
                                   c[1],
                                   latency,
                                   upload,
                                   download,
                                   time=c[0]))


  def get_positions_from_file(self, positions_file=None):
    """We assume that positions file is the path for a file
    containing the positions in the format (instant, lat, lng).
    instant : instant from the beginning of the experiment in seconds.
    lat : the latitude position in the instant.
    lng : the longitude position in the instant."""
    if positions_file:
      self.positions_file = positions_file

class PythiaMECHost(PythiaEmulationHost):
  """The MEC host emulates a MEC host. It means that the 
  applications stored in a same MEC host are subjected 
  to the same network characteristics."""
  def __init__(self, name, cpu, memmory):
    super().__init__(name)
    self.cpu = cpu
    self.memmory = memmory
    self.active_apps = set()
    self.docker_id = "vMEC-" + self.id_str

#class PythiaBS():
#  """This class represents a base station"""
#  def __init__(self, name, position):
#    self.name = name
#    self.position = position #(lat,lng)
#    self.links = []

class PythiaLink():
  def __init__(self,
               ue,
               mec_host,
               latency=None,
               upload=None,
               download=None,
               network=None,
               time=0):
    self.ue = ue
    self.mec_host = mec_host
    self.latency = latency
    self.upload = upload
    self.download = download
    self.network = network
    self.time = time


  def get_dict(self):
    d = {}

    d['ue'] = self.ue
    d['mec_host'] = self.mec_host
    if self.latency:
      d['latency'] = self.latency
    if self.upload:
      d['upload'] = self.upload
    if self.download:
      d['download'] = self.download
    if self.network:
      d['network'] = self.network.name
    if self.time:
      d['time'] = self.time
    return d


class PythiaBridge:
  """A bridge connects a UE to every MEC host.
  It is there to comply with Kollaps structures,
  but refers to UE."""
  def __init__(self, name, UE):
    self.name = name
    self.origin = UE

class PythiaNetwork:
  """A docker network"""
  def __init__(self, name, ip_range, interface_prefix):
    self.name = name
    self.ip_range = ip_range
    self.interface_prefix = interface_prefix
    self.interface = interface_prefix + "0"
    self.ip_network = ipaddress.ip_network(ip_range)
    self.allocated_ips = set()
    self.free_ips = set(ipaddress.ip_network(ip_range).hosts())
    self.docker_obj = None

  def allocate_ip(self, ip_addr=0):
    if (ip_addr):
      ip = ipaddress.IPv4Address(ip_addr)
      self.free_ips.remove(ip)
    else:
      ip = self.free_ips.pop()
    self.allocated_ips.add(ip)
    return format(ip)
