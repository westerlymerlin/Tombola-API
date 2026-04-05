# Tombola API Controller Service

**An application to control the Riverbed Simulator.**
<br>
The River simulator consists of a large (1 metre diameter) drum that can contain water, cement blocks simulate rocks on the riverbed.
The drum is driven by a 1/4 hp 3 phase motor.

The 3 phase motor is controlled by a **Siemens V20** single phase to 3 phase invertor which is controlled via an RS485 
interface using the modbus protocol<br>
**V20 Datasheet:**
https://support.industry.siemens.com/cs/attachments/109824500/V20_op_instr_0823_en-US.pdf
  
The controller application runs on a **Raspberry Pi 3B, 4B or 5** single board computer. It is written in Python and uses 
Flask for the Web application server. A USB RS485 controller provides connectivity to the V20 Invertor and the python 
library **Minimal Modbus** is used for the Modbus protocol.<br>
**Minimal Modbus Library Documentation** https://minimalmodbus.readthedocs.io/en/stable/

Application documentation can be found in [readme.pdf](./README.pdf)

Python module documentation can be found in the folder: [docs](./docs/readme.md)

Change log can be found in the file [changelog.txt](./changelog.txt)


---
**Web Application**
<br>
Accessing the URL `http://[url to your server]` via a web browser will open that status web page. It has buttons to
allow starting the Tombola at a desired RPM, stopping it and setting an auto-stop time if it is being left unattended.

**Direct API Calls**
<br>
If you POST a json message to the `http://[url to your server]/api` end point the flask app will process the call and
return a json message containing the V20 status values.

**API Messages**
<br>
`{"setrpm": n.n}`  Start the tombola running and hold it at n.n rpm (0.1–74.9 rpm)<br>
`{"setrpm": 0}`  Stop the tombola<br>
`{"rpm": True}`  Read the tombola RPM<br>
`{"rpm_data": True}`  Read the tombola abs sensor timing data from three revolutions<br>
`{"write_register": rr, "word": ww}`  Write the word ww to the register rr<br>
`{"read_register": rr}`  Read the value from the register rr<br>
`{"stoptime": "HH:MM:SS", "autostop": true}` set the controller to auto shut off at HH:MM:SS<br>
`{"stoptime": "HH:MM:SS", "autostop": false}` Disable auto stop
`{"status_message": "message to be displayed on the web page"}`  Set a status message to be displayed on the web page

---

**Shell Commands**
<br>
These can be run from a the console (via ssh or direct on the raspberry pi) to upgrade to the latest version of the
python code:<br>
`deploy-from-git.sh`  Checks github for a newer version of the code and if there is, download, deploy, and restart the 
python web app<br>
<br>
Less often used comamnds used for troubelshooting:<br>
`stopservices.sh` Stop the gunicorn and nginx services<br>
`startservices.sh` Start the gunicorn and nginx services<br>
`restartservices.sh` Stop, then start the gunicorn and nginx services<br>
`status.sh` Show the status of the gunicorn and nginx services<br>
<br>

---

**settings.json changes for RS485 com port**
<br>
Run the MortorClass.py file first, it will generate a fresh settings.json file<br>
Plug in the USB RS485 controller and find the port number (*com1* to *com7* on a PC or */dev/ttyUSB0* to
*/dev/ttyUSB9* on a mac or Raspberry Pi). <br>
Change the value for `"port": "/dev/ttyUSB0",`  to suit your configuration and run again to pick up the new port.

---

**To create a new version of Tombola-API**

Clone the repo from Github using the command below:  
`git clone https://github.com/westerlymerlin/Tombola-API.git`  
you will need to have Python 3.12 installed with all the dependencies listed in [requirements.txt](./requirements.txt).  
`pip install -r requirements.txt`  

Please create a new branch in git for your edits do not commit them to the master branch. 
`git branch -b my-new-feature`    
Make your changes to the code in your favorite IDE and test them, once you are happy with the results you are ready to package the new version:  
1. Update the version number in the module app_control.py  
2. Add a new line to the `changelog.txt` detailing what new feature you have added 

Please commit the changes you have made to git and push to the repository to git for version control. Please make the commit message detailed
`git add .`  
`git commit -m "add the detail of your changes here"`  
`git push origin my-new-feature`

There is an automated workflow that will update the docs files and create a pull request for the code owner to review and merge to the main branch.

---

## License
[GNU GENERAL PUBLIC LICENSE](./LICENSE)

---
## Contributors
Dr Gary Twinn   
Dr Byron Adams  
Dr Jesse Zondervan  

&nbsp;   
&nbsp;    
&nbsp;  
&nbsp;   
&nbsp;   
&nbsp;   
--------------

#### Copyright © 2026 Gary Twinn

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.  

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  
GNU General Public License for more details.  

You should have received a copy of the GNU General Public License  
along with this program. If not, see <https://www.gnu.org/licenses/>.


Author:  Gary Twinn  
Repository:  [github.com/westerlymerlin](https://github)


