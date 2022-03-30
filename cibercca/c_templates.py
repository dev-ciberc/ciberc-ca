ttp_template_services = """
<group name="services">
 service instance {{service_instance}} {{type_instance}}
  <group name="data">
  description {{description | re(".+")}}
  </group>
  <group name="data">
  encapsulation dot1q {{dot1q}}
  </group>
  <group name="data">
  rewrite ingress tag pop 1 {{rewrite_ingress}}
  </group>
  <group name="data">
  xconnect {{xconnect_ip}} {{xconnect_id}} {{xconnect_class}} {{xconnect_class_data}}
  </group>
  <group name="data">
  service-policy input {{service_policy_input}}
  </group>
  <group name="data">
  service-policy output {{service_policy_output}}
  </group>
  <group name="data">
  bridge-domain {{bridge_domain}}
  </group>
</group>
"""  # noqa


ttp_template_vlan_service = """
<group name="interface_vlan">
interface {{interface_vlan}}
 <group name="description">
 description {{description | re(".+")}}
 </group>
 <group name="vrf">
 ip vrf forwarding {{vrf}}
 </group>
 <group name="xconnect">
 xconnect {{xconnect_ip}} {{xconnect_id}} {{xconnect_class}} {{xconnect_class_data}}
 </group>
 <group name="ip_address_primary">
 ip address {{ip_address}} {{mask}}
 </group>
 <group name="ip_address_secundary">
 ip address {{ip_address}} {{mask}} {{type}}
 </group>
 <group name="ip_access_group">
 ip access-group {{access_group}} {{type}}
 </group>
 <group name="service_policy_input">
 service-policy input {{service_policy_input}}
 </group>
 <group name="service_policy_output">
 service-policy output {{service_policy_output}}
 </group>
 <group name="ip_helper_address">
 ip helper-address {{ip_helper_address}}
 </group>
 <group name="state">
 {{state}}
 </group>
</group>
"""  # noqa


ttp_template_bridge = """
<group name="bridges">
State: {{state}}                    Mac learning: {{mac_learning}}
    <group name="interfaces">
    {{interface}} {{type}} {{ins}} {{bridge_domain}}
    </group>
</group>
"""  # noqa

# --
# rename for save old version template
ttp_template_ports_old_version = """
<group name="ports">
{{num}}  {{vlan}}  {{mac_address}}   {{type}}  {{learn}}          {{age}}   {{port | re(".+")}}
</group>
"""  # noqa

ttp_template_ports = """
          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
<group name="ports">
 {{vlan}}    {{mac_address}}    {{type}}     {{port | ORPHRASE}}
</group>
"""  # noqa


ttp_template_trunk = """
<group name="services">
 <group name="data">
 switchport trunk encapsulation {{dot1q}}
 </group>
 <group name="data">
 switchport trunk allowed vlan {{switchport_vlans | | split(',')}}
 </group>
 <group name="data">
 switchport mode {{switchport_mode}}
 </group>
 <group name="data">
 mls {{mls}}
 </group>
</group>
"""


ttp_template_interfaces = """
<group name="interfaces">
{{interface}} is {{state | re(".+")}}, line protocol is {{protocol}} 
  Hardware is {{type_hardware}}, address is {{mac_address}} (bia {{bia_mac_address}})
  Description: {{description | re(".+")}}
  MTU {{mtu}} bytes, BW {{speed}} Kbit/sec, DLY 10 usec, 
</group>
"""  # noqa


ttp_template_interfaces_descriptions = \
"""
<group name="interfaces">
{{interface}}                         {{state}}             {{protocol}}       {{description | re(".+")}}
</group>
"""  # noqa


ttp_template_interaces_data = \
"""
<group>
{{name}} is {{ state | re(".+") }}, line protocol is {{protocol | re(".+") }} 
  <group name='hardware'>
  Hardware is {{type_hardware | re(".+")}}, address is {{mac_address}} (bia {{bia}})
  </group>
  <group name='mtu'>
  MTU {{mtu}} bytes, BW {{bw}} {{speed_type_bw}}, DLY {{dly}} usec, 
  </group>
</group>
"""  # noqa


ttp_template_multiple_vrf = \
"""
<group>
  {{vrf_name}}                              {{default_rd}}            {{protocols}}        {{interface}}
    <group name='interfaces'>
                                                                   {{interface}}
    </group>
  {{_end_}}
</group>
"""  # noqa

ttp_template_arp_vrf = \
"""
<group>
{{protocol}}  {{ip_address}}            {{age}}   {{mac}}  {{type}}   {{interface}}
</group>
<group>
{{protocol}}  {{ip_address}}            {{age}}   {{mac}}  {{type}}
</group>
"""  # noqa


ttp_template_arp_vrf_dst = \
"""
<group>
{{ip_address}}    {{age}}   {{mac}}  {{protocol}}    {{type}}  {{interface}}
</group>
"""  # noqa


ttp_template_ping_ip_arp = \
"""
<group>
Success rate is {{percent}} percent ({{rate}}/{{repeat}}){{extra | _line_}}
</group>
<group>
Success rate is {{percent}} percent ({{rate}}/{{repeat}})
</group>
"""  # noqa


ttp_template_vrf_dst = \
"""
<group>
{{vrf_name}}                {{rd}}
    <group name='import'>
                                         import  {{rt}}         {{afi}}  {{safi}}
    </group>
    <group name='export'>
                                         export  {{rt}}         {{afi}}  {{safi}}
    </group>
  {{_end_}}
</group>
"""  # noqa


class StringTemplates:

    def get_ttp_services(self):
        global ttp_template_services
        return ttp_template_services

    def get_ttp_trunk(self):
        global ttp_template_trunk
        return ttp_template_trunk

    def get_ttp_vlan(self):
        global ttp_template_vlan_service
        return ttp_template_vlan_service

    def get_ttp_bridge(self):
        global ttp_template_bridge
        return ttp_template_bridge

    def get_ttp_ports(self):
        global ttp_template_ports
        return ttp_template_ports

    def get_ttp_template_interfaces(self):
        global ttp_template_interfaces
        return ttp_template_interfaces

    def get_ttp_template_interfaces_descriptions(self):
        global ttp_template_interfaces_descriptions
        return ttp_template_interfaces_descriptions

    def get_ttp_template_interaces_data(self):
        global ttp_template_interaces_data
        return ttp_template_interaces_data

    def get_ttp_vrf(self):
        global ttp_template_multiple_vrf
        return ttp_template_multiple_vrf

    def get_ttp_arp_vrf(self):
        global ttp_template_arp_vrf
        return ttp_template_arp_vrf

    def get_ttp_ping_ip_arp(self):
        global ttp_template_ping_ip_arp
        return ttp_template_ping_ip_arp

    def get_ttp_vrf_dst(self):
        global ttp_template_vrf_dst
        return ttp_template_vrf_dst

    def get_ttp_arp_vrf_dst(self):
        global ttp_template_arp_vrf_dst
        return ttp_template_arp_vrf_dst
