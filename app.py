#!/usr/bin/env python3

import os
import json
import yaml
import argparse
from typing import Union


parser = argparse.ArgumentParser()

parser.add_argument(
    "-c",
    "--config",
    required=True,
    help="ABSOLUTE path to xray json config file.",
)

parser.add_argument(
    "-t",
    "--template",
    required=True,
    help="Template file for building clash config for each user.",
)


class XrayToClash:

    def __init__(self,
                 xray_config_path: str = "/usr/local/etc/xray/config.json",
                 template_file_path: str = "./template.yaml",
                 where_to_save: str    = "~/clash_confs"
                 ) -> None:
        self.xray_config_path = xray_config_path
        self.template_file_path = template_file_path
        self.where_to_save    = os.path.expanduser(where_to_save)

        if os.path.exists(self.template_file_path) is False:
            raise FileExistsError("Sample file does not exist.")

        if os.path.exists(self.where_to_save) is False:
            os.makedirs(self.where_to_save)

        with open(self.template_file_path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    
    def get_proxy_index_by_id(self,
                              identifier:str
                              ) -> Union[int, None]:
        proxies: list = self.data["proxies"]
        for proxy in proxies:
            if "uuid" in proxy:
                if proxy["uuid"] == identifier:
                    return proxies.index(proxy)
            elif "password" in proxy:
                if proxy["password"] == identifier:
                    return proxies.index(proxy)
        return None


    def init_new_clash_config(self,
                              identifier: str,
                              name: Union[str, None] = None
                              ) -> None:
        proxies = self.data["proxies"]
        for proxy in proxies:
            if "uuid" in proxy:
                proxy["uuid"] = identifier
            elif "password" in proxy:
                proxy["password"] = identifier

        if name is None:
            with open(f"{self.where_to_save}/{identifier}.yaml", "w", encoding="utf-8") as f:
                f.truncate(0)
                yaml.safe_dump(self.data, f, indent=2, sort_keys=False)
        else:
            with open(f"{self.where_to_save}/{name}_{identifier}.yaml", "w", encoding="utf-8") as f:
                f.truncate(0)
                yaml.safe_dump(self.data, f, indent=2, sort_keys=False)


    def init_new_clash_config_from_json(self,
                                        inbounds_index: int = 0,
                                        ) -> None:
        with open(self.xray_config_path, "r", encoding="utf-8") as f:
            jdata = json.load(f)

        users = jdata["inbounds"][inbounds_index]["settings"]["clients"]
        for user in users:
            if "id" in user:
                if "email" in user:
                    identifier = user["id"]
                    name = user["email"].split("@")[1]
                    self.init_new_clash_config(identifier, name=name)
                else:
                    identifier = user["id"]
                    self.init_new_clash_config(identifier)
            elif "password" in user:
                if "email" in user:
                    identifier = user["password"]
                    name = user["email"].split("@")[1]
                    self.init_new_clash_config(identifier, name=name)
                else:
                    identifier = user["password"]
                    self.init_new_clash_config(identifier)


if __name__ == "__main__":
    args = parser.parse_args()

    x = XrayToClash(xray_config_path=args.config,
                    template_file_path=args.template,
                    where_to_save="~/clash_confs")

    x.init_new_clash_config_from_json()

