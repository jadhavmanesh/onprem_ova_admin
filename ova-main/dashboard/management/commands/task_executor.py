import imp
import json
import os.path
import time
import sys
import traceback
import importlib

import requests
from django.core.management.base import BaseCommand
from dashboard.models import OnpremModule


class Command(BaseCommand):
    help = 'To execute the task in the redis'

    def handle(self, *args, **options):
        try:
            while True:
                poll_object = OnpremModule.objects.all()
                webhook_url_list = []
                for each_poll_obj in poll_object:
                    webhook_url_list.append(
                        {"SPORACT_URL": each_poll_obj.sporact_webhook_url,
                         "API_KEY": each_poll_obj.api_key,
                         "config": {"user": each_poll_obj.user,
                                    "device_prodcut": each_poll_obj.device_prodcut,
                                    "hostname": each_poll_obj.hostname,
                                    "port": each_poll_obj.port,
                                    "username": each_poll_obj.username,
                                    "device_password": each_poll_obj.device_password
                                    }})

                if len(webhook_url_list) > 0:
                    for each_webhook in webhook_url_list:
                        config = each_webhook["config"]
                        headers = {"X-Api-Key": each_webhook["API_KEY"]}
                        res = requests.get(
                            each_webhook["SPORACT_URL"], headers=headers)
                        res = res.json()
                        if "message" in res:
                            message_list = res["message"]
                            if len(message_list) > 0 and type(message_list) is list:
                                for each_task in message_list:
                                    task_id = each_task["task_id"]
                                    inputs = each_task["inputs"]
                                    module = inputs["module"]
                                    module_list = module.split(".")
                                    if len(message_list) > 0:

                                        module_name = module_list[0]
                                        file_name = module_list[2]
                                        class_name = module_list[-1]
                                        # Remove any modules cached by python
                                        module_to_remove = ""
                                        for module in module_list[1:-1]:
                                            module_to_remove = f"{module_to_remove}{'.' if module_to_remove else ''}{module}"
                                            sys.modules.pop(
                                                module_to_remove, None)

                                        file_path = os.path.join(
                                            "integrations", module_name, 'src', file_name + ".py")

                                        sys.path.append(
                                            os.path.dirname(file_path))

                                        spec = importlib.util.spec_from_file_location(
                                            "".join(
                                                module_list[0:-2]), file_path
                                        )
                                        all_package = importlib.util.module_from_spec(
                                            spec)
                                        spec.loader.exec_module(all_package)
                                        integration = getattr(
                                            all_package, class_name)
                                        obj = integration(config)
                                        response = obj.run(**inputs)
                                        response_dict = dict(response)
                                        requests.post(each_webhook["SPORACT_URL"],
                                                      json={"task_id": task_id,
                                                            "outputs": response_dict},
                                                      headers=headers)
                                        self.stdout.write(
                                            self.style.SUCCESS('Successfully posted the result'))
                time.sleep(60)
        except Exception as e:
            traceback.print_exc()
            raise Exception

    def load_from_file(self, filepath, expected_class):
        class_inst = None
        mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])
        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, filepath)

        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)

        if hasattr(py_mod, expected_class):
            class_inst = getattr(py_mod, expected_class)

        return class_inst
