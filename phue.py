

import requests
import json
from time import sleep

with open("phue_config.json") as file:
    config = json.load(file)
    if config["ip"] == "ENTER IP HERE":
        print("----------------------------------------------------------")
        print("Hue not connected.")
        ip = input("Enter the IP of the HueBridge: ")
        devicetype = input("Enter a unique name for this program: ")
        url = f"http://{ip}/api/"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "devicetype": devicetype
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response:
            print("Start pairing mode within 30 seconds!")
            print("(You can start the pairing mode by pressing the big button until it starts blinking)")
        sleep(30)
        token = json.loads(requests.post(url, headers=headers, data=json.dumps(data)).text)
        token = token[0]["success"]
        token = token["username"]

        data = {
            "ip": ip,
            "devicetype": devicetype,
            "token": token,
        }

        with open("phue_config.json", "w") as file:
            json.dump(data, file)

        with open("phue_config.json") as file:
            config = json.load(file)


class PHue:
    baseurl = str()
    devicetype = str()
    token = str()

    def __init__(self):
        ip = config["ip"]
        devicetype = config["devicetype"]
        token = config["token"]
        self.token = token
        self.baseurl = f"http://{ip}/api/{self.token}"

    def get_light_id_by_name(self, name):
        """ Lookup a light id based on string name. Case-sensitive. """
        lights = self.get_light()
        for light_id in lights:
            if name == lights[light_id]['name']:
                return light_id
        return False

    def get_group_id_by_name(self, name):
        """ Lookup a group id based on string name. Case-sensitive. """
        groups = self.get_group()
        for group_id in groups:
            if name == groups[group_id]['name']:
                return int(group_id)
        return False

    def get_scene_id_by_name(self, name):
        """ Lookup a scene id based on string name. Case-sensitive. """
        scenes = self.get_scene()
        for scene_id in scenes:
            if name == scenes[scene_id]['name']:
                return scene_id
        return False

    def get_sensor_id_by_name(self, name):
        """ Lookup a sensor id based on string name. Case-sensitive. """
        sensors = self.get_sensor()
        for sensor_id in sensors:
            if name == sensors[sensor_id]['name']:
                return sensor_id
        return False

    def get_light(self, id=None):
        addurl = "/lights"
        if type(id) is int:
            addurl = f"{addurl}/{id}"
        elif type(id) is str:
            addurl = f"{addurl}/{self.get_light_id_by_name(id)}"
        url = self.baseurl + addurl
        result = requests.get(url)
        return json.loads(result.text)

    def set_light(self, id, **kwargs):
        data = {}
        addurl = "/lights"
        if type(id) is int:
            addurl = f"{addurl}/{id}/state"
        elif type(id) is str:
            addurl = f"{addurl}/{self.get_light_id_by_name(id)}/state"
        for key, value in kwargs.items():
            data[key] = value
        url = self.baseurl + addurl
        data = json.dumps(data)
        result = requests.put(url, data=data)
        return json.loads(result.text)

    def get_group(self, id=None):
        addurl = "/groups"
        if type(id) is int:
            addurl = f"{addurl}/{id}"
        elif type(id) is str:
            addurl = f"{addurl}/{self.get_group_id_by_name(id)}"
        url = self.baseurl + addurl
        result = requests.get(url)
        return json.loads(result.text)

    def set_group(self, id, **kwargs):
        data = {}
        addurl = "/groups"
        if type(id) is int:
            addurl = f"{addurl}/{id}/action"
        elif type(id) is str:
            addurl = f"{addurl}/{self.get_group_id_by_name(id)}/action"
        for key, value in kwargs.items():
            if key == "scene":
                scene = self.get_scene_id_by_name(value)
                if scene is not False:
                    value = scene
                data[key] = value
            else:
                data[key] = value
        url = self.baseurl + addurl
        data = json.dumps(data)
        result = requests.put(url, data=data)
        return json.loads(result.text)

    def get_schedule(self):
        addurl = "/schedules"
        if id is int:
            addurl = f"{addurl}/{id}"
        url = self.baseurl + addurl
        result = requests.get(url)
        return json.loads(result.text)

    def get_scene(self):
        addurl = "/scenes"
        if type(id) is int:
            addurl = f"{addurl}/{id}"
        elif type(id) is str:
            addurl = f"{addurl}/{self.get_scene_id_by_name(id)}"
        url = self.baseurl + addurl
        result = requests.get(url)
        return json.loads(result.text)

    def get_sensor(self):
        addurl = "/sensors"
        if type(id) is int:
            addurl = f"{addurl}/{id}"
        elif type(id) is str:
            addurl = f"{addurl}/{self.get_sensor_id_by_name(id)}"
        url = self.baseurl + addurl
        result = requests.get(url)
        return json.loads(result.text)

    def get_rule(self):
        addurl = "/rules"
        if id is int:
            addurl = f"{addurl}/{id}"
        url = self.baseurl + addurl
        result = requests.get(url)
        return json.loads(result.text)
