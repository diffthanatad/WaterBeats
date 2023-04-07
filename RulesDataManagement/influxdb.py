import copy
import datetime
import os
import sys
import requests
from dotenv import load_dotenv


load_dotenv()

class InfluxDB:

    INFLUXDB_BASE_URL = os.getenv("INFLUXDB_BASE_URL")
    RULES_API_URL = os.getenv("RULES_API_URL")
    NOTIF_ENDPOINT_NAME = "twilio_endpoint"

    influxdb_org_id = ""
    influxdb_token = ""
    headers = ""

    alert_payload = {
        "name": None,
        "orgID": None,
        "query": {
            "text": "from(bucket: \"WaterBeats\")\n  \
                        |> range(start: v.timeRangeStart, stop: v.timeRangeStop)\n  \
                        |> filter(fn: (r) => r[\"_measurement\"] == \"sensor_data\")\n  \
                        |> filter(fn: (r) => r[\"_field\"] == \"data\")\n  \
                        |> filter(fn: (r) => r[\"sensor_id\"] == \"<sensor_id>\")\n  \
                        |> filter(fn: (r) => r[\"sensor_type\"] == \"<sensor_type>\")\n  \
                        |> aggregateWindow(every: 1m, fn: max, createEmpty: false)\n  \
                        |> yield(name: \"max\")",
            "editMode": "builder",
            "name": "",
            "builderConfig": {
                "buckets": [
                    "WaterBeats"
                ],
                "tags": [
                    {
                        "key": "_measurement",
                        "values": [
                            "sensor_data"
                        ],
                        "aggregateFunctionType": "filter"
                    },
                    {
                        "key": "_field",
                        "values": [
                            "data"
                        ],
                        "aggregateFunctionType": "filter"
                    },
                    {
                        "key": "sensor_id",
                        "values": [],
                        "aggregateFunctionType": "filter"
                    },
                    {
                        "key": "sensor_type",
                        "values": [],
                        "aggregateFunctionType": "filter"
                    }
                ],
                "functions": [
                    {
                        "name": "max"
                    }
                ],
                "aggregateWindow": {
                    "period": "1m",
                    "fillValues": False
                }
            }
        },
        "statusMessageTemplate": None,
        "every": "1m",
        "offset": "0s",
        "tags": [],
        "thresholds": [
            {
                "allValues": False,
                "level": "INFO",
                "value": None,
                "type": None
            }
        ],
        "type": "threshold",
        "labels": [],
        "status": "active"
    }

    endpoint_payload = {
        "name": NOTIF_ENDPOINT_NAME,
        "orgID": None,
        "status": "active",
        "type": "http",
        "authMethod": "none",
        "method": "POST",
        "url": RULES_API_URL,
    }

    rule_payload = {
        "name": "alert_rule",
        "endpointID": None,
        "orgID": None,
        "every": "1m",
        "offset": "0s",
        "statusRules": [
            {
            "currentLevel": "INFO",
            "previousLevel": "OK"
            }
        ],
        "status": "active",
        "type": "http"
    }

    def __init__(self):
        self.influxdb_org_id = self.get_org_id()
        self.influxdb_token = self.get_token()
        self.headers = {"Authorization": f"Bearer {self.influxdb_token}"}

        self.alert_payload["orgID"] = self.influxdb_org_id
        self.endpoint_payload["orgID"] = self.influxdb_org_id
        self.rule_payload["orgID"] = self.influxdb_org_id


    def get_alert(self, alert_name):
        response = requests.request("get", f"{self.INFLUXDB_BASE_URL}/api/v2/checks", headers=self.headers, params={"orgID": self.influxdb_org_id})
        if response.status_code != 200:
            return None

        alerts = response.json()
        for alert in alerts["checks"]:
            if alert["name"] == alert_name:
                return alert

        return None


    def create_alert(self, sensor_id, sensor_type, threshold, relation):
        endpoint_id = self.add_notification_endpoint(self.endpoint_payload)

        if endpoint_id:
            r_payload = copy.deepcopy(self.rule_payload)
            r_payload["endpointID"] = endpoint_id
            self.create_notification_rule(r_payload)

        alert_name = "alert_" + sensor_id
        alert = self.get_alert(alert_name)

        if alert:
            return alert["id"]

        a_payload = self.set_alert_payload(alert_name, sensor_id, sensor_type, threshold, relation)
        response = requests.request("post", f"{self.INFLUXDB_BASE_URL}/api/v2/checks", headers=self.headers, json=a_payload)

        if response.status_code != 201:
            return False

        return response.json()["id"]


    def update_alert(self, sensor_id, sensor_type, threshold, relation):
        alert_name = "alert_" + sensor_id
        alert = self.get_alert(alert_name)

        if not alert:
            return False

        alert_id = alert["id"]
        payload = self.set_alert_payload(alert_name, sensor_id, sensor_type, threshold, relation, alert_id)
        response = requests.request("put", f"{self.INFLUXDB_BASE_URL}/api/v2/checks/{alert_id}", headers=self.headers, json=payload)

        if response.status_code != 200:
            return False

        return True


    def delete_alert(self, sensor_id):
        alert_name = "alert_" + sensor_id
        alert = self.get_alert(alert_name)

        if not alert:
            return False

        alert_id = alert["id"]
        response = requests.request("delete", f"{self.INFLUXDB_BASE_URL}/api/v2/checks/{alert_id}", headers=self.headers)

        if response.status_code != 204:
            return False

        return True


    def get_notification_endpoint(self, endpoint_name):
        response = requests.request("get", f"{self.INFLUXDB_BASE_URL}/api/v2/notificationEndpoints", headers=self.headers, params={"orgID": self.influxdb_org_id})

        if response.status_code != 200:
            return None

        endpoints = response.json()
        for endpoint in endpoints["notificationEndpoints"]:
            if endpoint["name"] == endpoint_name:
                return endpoint["id"]

        return None


    def add_notification_endpoint(self, payload):
        endpoint_id = self.get_notification_endpoint(payload["name"])
        if endpoint_id:
            return endpoint_id

        response = requests.request("post", f"{self.INFLUXDB_BASE_URL}/api/v2/notificationEndpoints", headers=self.headers, json=payload)
        if response.status_code != 201:
            return False

        return response.json()["id"]


    def get_notification_rule(self, rule_name):
        response = requests.request("get", f"{self.INFLUXDB_BASE_URL}/api/v2/notificationRules", headers=self.headers, params={"orgID": self.influxdb_org_id})
        if response.status_code != 200:
            return None

        rules = response.json()
        for rule in rules["notificationRules"]:
            if rule["name"] == rule_name:
                return rule["id"]

        return None


    def create_notification_rule(self, payload):
        rule_name = payload["name"]
        rule_id = self.get_notification_rule(rule_name)

        if rule_id:
            return rule_id

        response = requests.request("post", f"{self.INFLUXDB_BASE_URL}/api/v2/notificationRules", headers=self.headers, json=payload)
        if response.status_code != 201:
            return False

        return response.json()["id"]


    def set_alert_payload(self, alert_name, sensor_id, sensor_type, threshold, relation, alert_id=None):
        payload = copy.deepcopy(self.alert_payload)

        if alert_id:
            payload["checkID"] = alert_id

        payload["name"] = alert_name
        payload["query"]["text"] = payload["query"]["text"].replace("<sensor_id>", sensor_id)
        payload["query"]["text"] = payload["query"]["text"].replace("<sensor_type>", sensor_type)

        for tag in payload["query"]["builderConfig"]["tags"]:
            if tag["key"] == "sensor_id":
                tag["values"] = [sensor_id]
            if tag["key"] == "sensor_type":
                tag["values"] = [sensor_type]

        if relation == ">=" or relation == ">":
            payload["thresholds"][0]["value"] = (threshold - 1) if relation == ">=" else threshold
            payload["thresholds"][0]["type"] = "greater"

        if relation == "<=" or relation == "<":
            payload["thresholds"][0]["value"] = (threshold + 1) if relation == "<=" else threshold
            payload["thresholds"][0]["type"] = "lesser"

        payload["statusMessageTemplate"] = f"ALERT TRIGGERED:\n\n{sensor_type.capitalize()} sensor with ID '{sensor_id}' {relation} {threshold}"

        return payload

    def get_org_id(self):
        headers = {
            "Authorization": "Basic V2F0ZXJCZWF0czpXYXRlckJlYXRz",
        }
        sign_in_response = requests.request("POST", f"{self.INFLUXDB_BASE_URL}/api/v2/signin", headers=headers)

        if "Set-Cookie" not in sign_in_response.headers:
            raise Exception(f"No cookie: {sign_in_response.status_code} {sign_in_response.text} {sign_in_response.headers}")

        cookie = sign_in_response.headers["Set-Cookie"]
        self.headers = {"Cookie": cookie, "Content-Type": "application/json"}

        get_buckets_response = requests.request("GET", f"{self.INFLUXDB_BASE_URL}/api/v2/buckets", headers=self.headers)
        if get_buckets_response.status_code != 200:
            raise Exception(f"Failed to get buckets: {get_buckets_response.status_code} {get_buckets_response.text}")

        data = get_buckets_response.json()
        waterbeats_bucket = [ bucket for bucket in data["buckets"] if bucket["name"] == "WaterBeats"][0]
        org_id = waterbeats_bucket["orgID"]

        return org_id

    def get_token(self):
        payload = {
            "description": f"WaterBeats DevAPI {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "orgID": self.influxdb_org_id,
            "permissions": [
                {"action": "read",  "resource": {"type": "checks", "orgID": self.influxdb_org_id}},
                {"action": "read",  "resource": {"type": "notificationEndpoints", "orgID": self.influxdb_org_id}},
                {"action": "read",  "resource": {"type": "notificationRules", "orgID": self.influxdb_org_id}},
                {"action": "write", "resource": {"type": "checks", "orgID": self.influxdb_org_id}},
                {"action": "write", "resource": {"type": "notificationEndpoints", "orgID": self.influxdb_org_id}},
                {"action": "write", "resource": {"type": "notificationRules", "orgID": self.influxdb_org_id}},
            ],
        }
        create_token_response = requests.request("POST", f"{self.INFLUXDB_BASE_URL}/api/v2/authorizations", headers=self.headers, json=payload)

        return create_token_response.json()["token"]
import copy
import datetime
import os
import sys
import requests
from dotenv import load_dotenv


load_dotenv()

class InfluxDB:

    INFLUXDB_BASE_URL = os.getenv("INFLUXDB_BASE_URL")
    RULES_API_URL = os.getenv("RULES_API_URL")
    NOTIF_ENDPOINT_NAME = "twilio_endpoint"

    influxdb_org_id = ""
    influxdb_token = ""
    headers = ""

    alert_payload = {
        "name": None,
        "orgID": None,
        "query": {
            "text": "from(bucket: \"WaterBeats\")\n  \
                        |> range(start: v.timeRangeStart, stop: v.timeRangeStop)\n  \
                        |> filter(fn: (r) => r[\"_measurement\"] == \"sensor_data\")\n  \
                        |> filter(fn: (r) => r[\"_field\"] == \"data\")\n  \
                        |> filter(fn: (r) => r[\"sensor_id\"] == \"<sensor_id>\")\n  \
                        |> filter(fn: (r) => r[\"sensor_type\"] == \"<sensor_type>\")\n  \
                        |> aggregateWindow(every: 1m, fn: max, createEmpty: false)\n  \
                        |> yield(name: \"max\")",
            "editMode": "builder",
            "name": "",
            "builderConfig": {
                "buckets": [
                    "WaterBeats"
                ],
                "tags": [
                    {
                        "key": "_measurement",
                        "values": [
                            "sensor_data"
                        ],
                        "aggregateFunctionType": "filter"
                    },
                    {
                        "key": "_field",
                        "values": [
                            "data"
                        ],
                        "aggregateFunctionType": "filter"
                    },
                    {
                        "key": "sensor_id",
                        "values": [],
                        "aggregateFunctionType": "filter"
                    },
                    {
                        "key": "sensor_type",
                        "values": [],
                        "aggregateFunctionType": "filter"
                    }
                ],
                "functions": [
                    {
                        "name": "max"
                    }
                ],
                "aggregateWindow": {
                    "period": "1m",
                    "fillValues": False
                }
            }
        },
        "statusMessageTemplate": None,
        "every": "1m",
        "offset": "0s",
        "tags": [],
        "thresholds": [
            {
                "allValues": False,
                "level": "INFO",
                "value": None,
                "type": None
            }
        ],
        "type": "threshold",
        "labels": [],
        "status": "active"
    }

    endpoint_payload = {
        "name": NOTIF_ENDPOINT_NAME,
        "orgID": None,
        "status": "active",
        "type": "http",
        "authMethod": "none",
        "method": "POST",
        "url": RULES_API_URL,
    }

    rule_payload = {
        "name": "alert_rule",
        "endpointID": None,
        "orgID": None,
        "every": "1m",
        "offset": "0s",
        "statusRules": [
            {
            "currentLevel": "INFO",
            "previousLevel": "OK"
            }
        ],
        "status": "active",
        "type": "http"
    }

    def __init__(self):
        self.influxdb_org_id = self.get_org_id()
        self.influxdb_token = self.get_token()
        self.headers = {"Authorization": f"Bearer {self.influxdb_token}"}

        self.alert_payload["orgID"] = self.influxdb_org_id
        self.endpoint_payload["orgID"] = self.influxdb_org_id
        self.rule_payload["orgID"] = self.influxdb_org_id


    def get_alert(self, alert_name):
        response = requests.request("get", f"{self.INFLUXDB_BASE_URL}/api/v2/checks", headers=self.headers, params={"orgID": self.influxdb_org_id})
        if response.status_code != 200:
            return None

        alerts = response.json()
        for alert in alerts["checks"]:
            if alert["name"] == alert_name:
                return alert

        return None


    def create_alert(self, sensor_id, sensor_type, threshold, relation):
        endpoint_id = self.add_notification_endpoint(self.endpoint_payload)

        if endpoint_id:
            r_payload = copy.deepcopy(self.rule_payload)
            r_payload["endpointID"] = endpoint_id
            self.create_notification_rule(r_payload)

        alert_name = "alert_" + sensor_id
        alert = self.get_alert(alert_name)

        if alert:
            return alert["id"]

        a_payload = self.set_alert_payload(alert_name, sensor_id, sensor_type, threshold, relation)
        response = requests.request("post", f"{self.INFLUXDB_BASE_URL}/api/v2/checks", headers=self.headers, json=a_payload)

        if response.status_code != 201:
            return False

        return response.json()["id"]


    def update_alert(self, sensor_id, sensor_type, threshold, relation):
        alert_name = "alert_" + sensor_id
        alert = self.get_alert(alert_name)

        if not alert:
            return False

        alert_id = alert["id"]
        payload = self.set_alert_payload(alert_name, sensor_id, sensor_type, threshold, relation, alert_id)
        response = requests.request("put", f"{self.INFLUXDB_BASE_URL}/api/v2/checks/{alert_id}", headers=self.headers, json=payload)

        if response.status_code != 200:
            return False

        return True


    def delete_alert(self, sensor_id):
        alert_name = "alert_" + sensor_id
        alert = self.get_alert(alert_name)

        if not alert:
            return False

        alert_id = alert["id"]
        response = requests.request("delete", f"{self.INFLUXDB_BASE_URL}/api/v2/checks/{alert_id}", headers=self.headers)

        if response.status_code != 204:
            return False

        return True


    def get_notification_endpoint(self, endpoint_name):
        response = requests.request("get", f"{self.INFLUXDB_BASE_URL}/api/v2/notificationEndpoints", headers=self.headers, params={"orgID": self.influxdb_org_id})

        if response.status_code != 200:
            return None

        endpoints = response.json()
        for endpoint in endpoints["notificationEndpoints"]:
            if endpoint["name"] == endpoint_name:
                return endpoint["id"]

        return None


    def add_notification_endpoint(self, payload):
        endpoint_id = self.get_notification_endpoint(payload["name"])
        if endpoint_id:
            return endpoint_id

        response = requests.request("post", f"{self.INFLUXDB_BASE_URL}/api/v2/notificationEndpoints", headers=self.headers, json=payload)
        if response.status_code != 201:
            return False

        return response.json()["id"]


    def get_notification_rule(self, rule_name):
        response = requests.request("get", f"{self.INFLUXDB_BASE_URL}/api/v2/notificationRules", headers=self.headers, params={"orgID": self.influxdb_org_id})
        if response.status_code != 200:
            return None

        rules = response.json()
        for rule in rules["notificationRules"]:
            if rule["name"] == rule_name:
                return rule["id"]

        return None


    def create_notification_rule(self, payload):
        rule_name = payload["name"]
        rule_id = self.get_notification_rule(rule_name)

        if rule_id:
            return rule_id

        response = requests.request("post", f"{self.INFLUXDB_BASE_URL}/api/v2/notificationRules", headers=self.headers, json=payload)
        if response.status_code != 201:
            return False

        return response.json()["id"]


    def set_alert_payload(self, alert_name, sensor_id, sensor_type, threshold, relation, alert_id=None):
        payload = copy.deepcopy(self.alert_payload)

        if alert_id:
            payload["checkID"] = alert_id

        payload["name"] = alert_name
        payload["query"]["text"] = payload["query"]["text"].replace("<sensor_id>", sensor_id)
        payload["query"]["text"] = payload["query"]["text"].replace("<sensor_type>", sensor_type)

        for tag in payload["query"]["builderConfig"]["tags"]:
            if tag["key"] == "sensor_id":
                tag["values"] = [sensor_id]
            if tag["key"] == "sensor_type":
                tag["values"] = [sensor_type]

        if relation == ">=" or relation == ">":
            payload["thresholds"][0]["value"] = (threshold - 1) if relation == ">=" else threshold
            payload["thresholds"][0]["type"] = "greater"

        if relation == "<=" or relation == "<":
            payload["thresholds"][0]["value"] = (threshold + 1) if relation == "<=" else threshold
            payload["thresholds"][0]["type"] = "lesser"

        payload["statusMessageTemplate"] = f"ALERT TRIGGERED:\n\n{sensor_type.capitalize()} sensor with ID '{sensor_id}' {relation} {threshold}"

        return payload

    def get_org_id(self):
        headers = {
            "Authorization": "Basic V2F0ZXJCZWF0czpXYXRlckJlYXRz",
        }
        sign_in_response = requests.request("POST", f"{self.INFLUXDB_BASE_URL}/api/v2/signin", headers=headers)

        if "Set-Cookie" not in sign_in_response.headers:
            raise Exception(f"No cookie: {sign_in_response.status_code} {sign_in_response.text} {sign_in_response.headers}")

        cookie = sign_in_response.headers["Set-Cookie"]
        self.headers = {"Cookie": cookie, "Content-Type": "application/json"}

        get_buckets_response = requests.request("GET", f"{self.INFLUXDB_BASE_URL}/api/v2/buckets", headers=self.headers)
        if get_buckets_response.status_code != 200:
            raise Exception(f"Failed to get buckets: {get_buckets_response.status_code} {get_buckets_response.text}")

        data = get_buckets_response.json()
        waterbeats_bucket = [ bucket for bucket in data["buckets"] if bucket["name"] == "WaterBeats"][0]
        org_id = waterbeats_bucket["orgID"]

        return org_id

    def get_token(self):
        payload = {
            "description": f"WaterBeats DevAPI {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "orgID": self.influxdb_org_id,
            "permissions": [
                {"action": "read",  "resource": {"type": "checks", "orgID": self.influxdb_org_id}},
                {"action": "read",  "resource": {"type": "notificationEndpoints", "orgID": self.influxdb_org_id}},
                {"action": "read",  "resource": {"type": "notificationRules", "orgID": self.influxdb_org_id}},
                {"action": "write", "resource": {"type": "checks", "orgID": self.influxdb_org_id}},
                {"action": "write", "resource": {"type": "notificationEndpoints", "orgID": self.influxdb_org_id}},
                {"action": "write", "resource": {"type": "notificationRules", "orgID": self.influxdb_org_id}},
            ],
        }
        create_token_response = requests.request("POST", f"{self.INFLUXDB_BASE_URL}/api/v2/authorizations", headers=self.headers, json=payload)

        return create_token_response.json()["token"]
