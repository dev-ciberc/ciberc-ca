ttp_template_services = """
<group name="services">
 service instance {{service_instance}} {{type_instance}}
  <group name="data">
  description {{description | ORPHRASE}}
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
 description {{description | ORPHRASE}}
 </group>
 <group name="vrf">
 ip vrf forwarding {{vrf}}
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

ttp_template_ports = """
<group name="ports">
{{num}}  {{vlan}}  {{mac_address}}   {{type}}  {{learn}}          {{age}}   {{port | ORPHRASE}}
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
