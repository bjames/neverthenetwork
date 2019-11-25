# Practical Automation - mod_acl

Managing access lists is one of the more painful parts of being a network engineer. Once you've finishing working out what should or should not be allowed, you write the ACL and then paste it into all your devices. Around the time you finish, the requirements change or the business lets you know what just broke. In the future, SGTs and SDN promise to fix this problem, but you might not be there yet. mod_acl is a simple and fast way to manage ACLs. 

If you want to skip the fluff and get right to the code, you can clone my repo on github. 

## Implementation Goals

1. The script should be able to modify existing ACLs on both Nexus and IOS
2. The script should be reusable without any modifications to the script itself. 
3. The script should get it's job done without needless complication
4. Script configuration should be logical and easy 

## General Notes on ACLs

1. ACLs can be removed and re-added without any issues


## Installation
* Clone the repository
`git clone --rescurse-submodules https://gitlab.gmfinancial.com/BJAMES4/mod_acl`
* Initialize a new python virtual environment
`python -m virtualenv venv`
* Install the required python modules
`.\venv\bin\python -m pip -r requirements.txt`

## Usage
* Create or modify one of the YAML files in the repo as needed (see examples folder)
* device_list entries should have a hostname and device_type (either cisco_ios or cisco_nxos)
```
    - hostname: brs402
      device_type: cisco_ios
    - hostname: 10.18.0.2
      device_type: cisco_nxos
```
* acl_name should refer to an ACL that already exists
    * Creating new ACLs isn't currently supported, but will be added when needed
* if `append` is set to True, then the lines are added to the ACL. Otherwise the ACL is replaced
    * Line numbers can be specified in either instance, but should only be necessary when appending
    * When possible append False is preferred as this enforces consistancy
* Note on ACL lines the pipe prior to the list of ACEs must be present for the YAML to be parsed correctly
* Run the script with `./venv/bin/python mod_acl.py mod_acl.yml`