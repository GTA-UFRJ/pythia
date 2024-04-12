from pythia.structures import *
import xml.etree.ElementTree as ET


def parse_scenario(filename):
  """This method reads a file representing an experiment
  and returns the structures represented in the file"""
  tree = ET.parse(filename)
  root = tree.getroot()

  UEs = {}

  mec_hosts = {}
  mec_apps = {}

  base_stations = {}
  
  
  # Creating UEs
  for ue_xml in root.iter('ue'):
    # Creating UE Apps
    ue = PythiaUEHost(ue_xml.attrib['name'],
                      ue_xml.attrib['positions_file'])
    for ue_app_tag in ue_xml.iter('ue_app'):
      volumes = []
      devices = []
      environments = []
      parameters = {}
      for volume_tag in ue_app_tag.iter('volume'):
        volumes.append(volume_tag.text)
      for device_tag in ue_app_tag.iter('device'):
        devices.append(device_tag.text)
      for environment_tag in ue_app_tag.iter('environment'):
        environments.append(environment_tag.text)

      parameters = get_parameters(ue_app_tag)
      ue.apps.append(PythiaUEApp(ue_app_tag.attrib['name'],
                                ue_app_tag.attrib['image'],
                                ue_app_tag.attrib['command'],
                                volume=volumes,
                                devices=devices,
                                environment=environments,
                                params = parameters))
    UEs[ue.name] = ue

  #Creating MEC hosts
  for mh_xml in root.iter('mec_host'):
    mec_hosts[mh_xml.attrib['name']] = PythiaMECHost(
                                        mh_xml.attrib['name'],
                                        mh_xml.attrib['cpu'],
                                        mh_xml.attrib['memmory'])

  # Creating MEC apps
  environments = []
  for environment_tag in ue_app_tag.iter('environment'):
    environments.append(environment_tag.text)
  for ma_xml in root.iter('mec_app'):
    mec_apps[ma_xml.attrib['name']] = PythiaMECApp(ma_xml.attrib['name'],
                                 ma_xml.attrib['image'],
                                 ma_xml.attrib['ip'],
                                 ma_xml.attrib['host'],                  
                                 ma_xml.attrib['command'],
                                 environment=environments)

  # Creating base stations
  """for bs_xml in root.iter('base_station'):
    # Creating links between base stations and MEC Hosts
    bs = PythiaBS(bs_xml.attrib['name'],
                  (float(bs_xml.attrib['lat']), float(bs_xml.attrib['lng'])))
    for link_tag in bs_xml.iter('link'):
      bs.links.append(PythiaLink(bs.name,
                                 mec_hosts[link_tag.attrib['dest']].stub_name,
                                 link_tag.attrib['latency'],
                                 link_tag.attrib['upload'],
                                 link_tag.attrib['download']))

    base_stations[bs.name] = bs
  """

  links = []

  for link_xml in root.iter('link'):
    links.append(PythiaLink(UEs[link_xml.attrib['ue']],
                            mec_hosts[link_xml.attrib['mec_host']],
                            link_xml.attrib['latency'],
                            link_xml.attrib['upload'],
                            link_xml.attrib['download'],
                            time=float(link_xml.attrib['time'])))

  return mec_hosts, UEs, mec_apps, links

def write_link_states(filename):

  return 0

def get_parameters(app_tag):
  params = {}
  for parameter_tag in app_tag.iter('parameter'):
    key = parameter_tag.attrib['key']
    value = parameter_tag.attrib['value']
    logging.info(f"The parameter values are {value}")
    if params.get(key) is not None:
      if isinstance(params.get(key), list):
        params[key].append(value)
      else:
        params[key] = [params[key], value]
    else:
      params[key] = value
    logging.info(f"The parameter values are {params['volumes']}")
  return params
