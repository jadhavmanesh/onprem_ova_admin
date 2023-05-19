import check_point_firewall_v2

SERVER_URL = ""
HTTPS_WWW_BASE_URL = f"https://{SERVER_URL}"


class BlockIP:
    def __init__(self, config):
        self.config = config
        self.client = check_point_firewall_v2.Client(base_url=HTTPS_WWW_BASE_URL, use_ssl=False, use_proxy=False)

    def run(self, **inputs):
        try:
            # 1. add the group
            add_group = self.client.add_group(inputs["group_name"])
            print(add_group)

            # 2. add the access rule
            add_access_rule = self.client.add_rule(layer=inputs["layer"],
                                                   position=inputs["position"],
                                                   action="Drop",
                                                   name=inputs["access_rule_name"],
                                                   vpn=None,
                                                   destination=inputs["ip_to_block"],
                                                   service=inputs["group_name"],
                                                   source=inputs["hostname_for_ip"]
                                                   )
            print(add_access_rule)

            # 3. add host to group
            add_host_to_group = self.client.add_host(
                name=inputs["hostname_for_ip"],
                ip_address=inputs["ip_to_block"],
                groups=inputs["group_name"],
                ignore_warnings=False,
                ignore_errors=False)
            print(add_host_to_group)

            # 4. install the policy
            install_policy = self.client.install_policy(
                policy_package=inputs[
                    "policy_name"],
                targets=inputs["group_name"],
                access=False)
            print(install_policy)

            return {"add_group": add_group,
                    "add_access_rule": add_access_rule,
                    "install_policy": install_policy,
                    "add_host_to_group": add_host_to_group}
        except Exception as e:
            return {"status": "failed"}
