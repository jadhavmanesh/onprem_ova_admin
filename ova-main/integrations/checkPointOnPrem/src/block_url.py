import check_point_firewall_v2

SERVER_URL = ""
HTTPS_WWW_BASE_URL = f"https://{SERVER_URL}"


class BlockURL:
    def __init__(self, config):
        self.config = config
        self.client = check_point_firewall_v2.Client(base_url=HTTPS_WWW_BASE_URL, use_ssl=False, use_proxy=False)

    def run(self, **inputs):
        try:
            # 1. add application site category
            add_application_site_category = self.client.add_application_site_category(
                identifier=inputs["category_name"],
                groups=None)
            print(add_application_site_category)

            # 2. Add URL into the added category
            add_site_to_category = self.client.add_application_site(
                name=inputs["site_name"],
                primary_category=inputs["category_name"],
                identifier=inputs["url_list"],
                groups=None)
            print(add_site_to_category)

            # 3. add the access rule
            add_access_rule = self.client.add_rule(
                layer=inputs["layer"],
                position=inputs["position"],
                action="Drop",
                name=inputs["access_rule_name"],
                vpn=None,
                destination=inputs["url_list"],
                service=inputs["category_name"],
                source=inputs["site_name"]
            )
            print(add_access_rule)

            # 4. install the policy
            install_policy = self.client.install_policy(
                policy_package=inputs["policy_name"],
                targets=inputs["category_name"],
                access=False)
            print(install_policy)

            return {"add_application_site_category": add_application_site_category,
                    "add_site_to_category": add_site_to_category,
                    "add_access_rule": add_access_rule,
                    "install_policy": install_policy}
        except Exception as e:
            return {"status": "failed"}
