#!/usr/bin/env python3

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
    "-s",
    "--server",
    required=False,
    help="Your server's IP address.",
)

parser.add_argument(
    "-d",
    "--domain",
    type=str,
    required=False,
    help="Your domain name (If you have one).",
)

parser.add_argument(
    "-b",
    "--base",
    required=True,
    help="Base file for building clash config.",
)

parser.add_argument(
    "-n",
    "--name",
    required=True,
    help="Set the name of the proxy that will be in clash config file.",
)

class Xary:
    
    def __init__(self,
                 config:str = "/usr/local/etc/xray/config.json",
                 serverIp: Union[str, None] = None,
                 domainName: Union[str, None] = None,
                 baseFile: str = "./base.yaml",
                 ) -> None:
        self.config = config
        self.base   = baseFile
        self.serverIp: Union[str, None] = serverIp
        self.domainName: Union[str, None] = domainName

        with open(self.config, "r", encoding="utf-8") as f:
            self.data = json.load(f)


    def build_base_clash_config(self, name:str = "conf"):
        inbounds = self.data["inbounds"]
        i = 0
        yaml_conf = []
        valid_tls = ("tls", "xtls")
        for inbound in inbounds:
            if inbound["protocol"] == "vless":
                continue
            if inbound["protocol"] == "vmess":
                tmp_conf = {
                    "name": f"{name}",
                    "port": inbound["port"],
                    "type": inbound["protocol"],
                    "server": self.serverIp,
                    "uuid": "ID",
                    "alterId": 0,
                    "cipher": "chacha20-poly1305",
                    "udp": False,
                    "tls": True if "security" in inbound["streamSettings"] and inbound["streamSettings"]["security"] in valid_tls else False,
                    "skip-cert-verify": True,
                    "servername": self.domainName,
                    "network": "PASS",
                }
                
                if self.domainName and self.serverIp is None:
                    tmp_conf["server"] = self.domainName
                elif self.serverIp and self.domainName is None:
                    tmp_conf["tls"] = False
                    tmp_conf["server"] = self.serverIp
                    del tmp_conf["servername"]
                elif self.serverIp and self.domainName:
                    tmp_conf["tls"] = True
                    tmp_conf["server"] = self.serverIp

                if inbound["streamSettings"]["network"] == "ws":
                    tmp_conf["network"] = "ws"
                    tmp_conf["ws-opts"] = {
                        "path": inbound["streamSettings"]["wsSettings"]["path"],
                        "headers": {
                            "Host": self.domainName
                        }
                    }

                elif inbound["streamSettings"]["network"] == "tcp":
                    tmp_conf["network"] = "http"
                    if "tcpSettings" in inbound["streamSettings"]:
                        if inbound["streamSettings"]["tcpSettings"]["header"]["type"] == "http":
                            tmp_conf["http-opts"] = {
                                "path": ["/"],
                                "headers": {
                                    "Connection": ["keep-alive"]
                                }
                            }

                yaml_conf.append(tmp_conf)
                i += 1

        proxy_groupes = []
        for conf in yaml_conf:
            proxy_groupes.append(conf["name"])

        with open(self.base, "r", encoding="utf-8") as f:
            ydata = yaml.safe_load(f)

        del ydata["proxies"]
        del ydata["proxy-groups"][0]["proxies"]
        ydata["proxies"] = yaml_conf
        ydata["proxy-groups"][0]["proxies"] = proxy_groupes
                
        with open("./template.yaml", "w", encoding="utf-8") as f:
            f.truncate(0)
            yaml.safe_dump(ydata, f, indent=2, sort_keys=False)

if __name__ == "__main__":
    args = parser.parse_args()
    x = Xary(config=args.config, domainName=args.domain, serverIp=args.server, baseFile=args.base)

    x.build_base_clash_config(args.name)

