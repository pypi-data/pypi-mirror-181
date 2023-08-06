#!/usr/bin/python3
import requests
import json


class IcingaFetcher:
    def __init__(self, config):
        self.config = config
        if not "exclude" in self.config:
            self.config["exclude"] = {}

    def send_request(self, call):
        try:
            r = requests.get(
                self.config["base_url"] + "monitoring/" + call,
                auth=(self.config["user"], self.config["password"]),
                headers={"Accept": "application/json"},
                verify=self.config["ssl_verify"],
            )
            if r.status_code == 200:
                return r.content
            else:
                return None
        except:
            return False

    def get_services(self, groups):
        services = []
        for group in groups:
            json_data = self.send_request("list/services?hostgroup_name=" + group)
            if json_data == False or json_data == None:
                return json_data
            data = json.loads(json_data)
            services += data
        return services

    def build_url(self, host, service):
        if service.startswith("Diskspace"):
            service = service.replace("Diskspace ", "Apply-Diskchecks").replace(
                "/", "%2F"
            )
        return f"{self.config['base_url']}monitoring/service/show?host={host}&service={service}"

    def is_excluded(self, service):
        if service["host_name"] in self.config["exclude"]:
            exclude_list = self.config["exclude"][service["host_name"]]
            if (
                len(exclude_list) == 0
                or service["service_display_name"] in exclude_list
            ):
                return True
        return False

    def get_data(self):
        data = {"ok": {}, "warn": {}, "crit": {}, "ignore": {}, "unknown": {}}
        services = self.get_services(self.config["host_groups"])
        if not services or services is None:
            return services
        for service in services:
            if self.is_excluded(service):
                data["ignore"][
                    f'{service["host_name"]}{service["service_display_name"]}'
                ] = "."
            else:
                key = "ok"
                state = int(service["service_state"])
                if state == 3:
                    key = "unknown"
                elif state == 2:
                    key = "crit"
                elif state == 1:
                    key = "warn"
                title = f'{service["host_name"]} ({service["service_display_name"]})'
                if service["service_output"] is None:
                    msg = "No message"
                else:
                    msg = service["service_output"].split(":")[-1].split(" - ")[-1]
                data[key][title] = {
                    "msg": msg,
                    "url": self.build_url(
                        service["host_name"], service["service_display_name"]
                    ),
                }
        return data


if __name__ == "__main__":
    config = json.load(open("config.json", "r"))
    config["ssl_verify"] = False
    fetcher = IcingaFetcher(config)
    data = fetcher.get_data()
