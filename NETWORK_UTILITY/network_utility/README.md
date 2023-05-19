Network Utility
=========

Network utility is a used to configure the network to be DHCP or Static and view/update the proxy of the system

### Technologies

Developed using following features:

- Python 3.9
- flask
- Flask-Compress
- Flask-Cors
- PyYAML
- netifaces
- netaddr

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

A step by step series of examples that tell you how to get a development env running

**Start the python app in Linux environment**

```bash
pip install -r requirements.txt
chmod 777 app
./app
```

## Application configuration

**FLASK**
  - port: "application port"

**SQLITE**
  - db: "database name"

**PROXY**
  - path: "proxy file path" (default path: ```/etc/profile.d/proxy.sh```)
## Author

* **Vishnu Prasad** - [@vishnu] (vishnuprasadapps@gmail.com))

