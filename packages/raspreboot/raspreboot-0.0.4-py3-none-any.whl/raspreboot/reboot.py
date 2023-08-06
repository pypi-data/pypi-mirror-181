import json
import os
import time
import urllib.request
from Shyna_speaks import Shyna_speaks


class RebootRasp:
    s_speak = Shyna_speaks.ShynaSpeak()
    data = {'reboot_count': 0, 'reboot_status': False}
    result = False
    user = str(os.popen("echo $USER").read()).strip("\n")
    out_dir = "/home/" + user
    path = os.path.join(out_dir, 'reboot.json')

    def where_json(self):
        return os.path.exists(self.path)

    def create_json(self):
        if self.where_json():
            return True
        else:
            with open(self.path, 'w') as outfile:
                json.dump(self.data, outfile)
            return True

    def open_url(self):
        try:
            x = urllib.request.urlopen(url='https://www.google.com', timeout=2)
            response = x.read()
            if response == b'':
                self.result = False
            else:
                self.result = True
        except Exception as e:
            print(e)
            self.result = False
        finally:
            print("Internet Connection", self.result)
            return self.result

    def reboot_now(self):
        if self.create_json():
            if self.open_url() is True:
                pass
            else:
                with open(self.path, 'r') as openfile:
                    json_object = json.load(openfile)
                add_count = json_object['reboot_count'] + 1
                if add_count <= 3:
                    with open(self.path, "w") as outfile:
                        json.dump({'reboot_count': add_count, 'reboot_status': False}, outfile)
                else:
                    with open(self.path, "w") as outfile:
                        json.dump(self.data, outfile)
                    self.s_speak.shyna_speaks(msg="Boss! Rebooting System, check internet")
                    time.sleep(2)
                    os.system("sudo shutdown -r now")


if __name__ == '__main__':
    RebootRasp().reboot_now()
