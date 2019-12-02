# Practical Automation - mod_acl

Managing access lists is one of the more painful parts of being a network engineer. Once you've finishing working out what should or should not be allowed, you write the ACL and then paste it into all your devices. The minute you finish, the requirements change or the business lets you know what just broke. In the future, SGTs and SDN promise to fix this problem, but you might not be there yet. mod_acl is a simple and fast way to manage ACLs. 

If you want to skip the fluff and get right to the code, you can clone my repo on github. 

## Implementation Goals

1. The script should be able to modify existing ACLs on both Nexus and IOS
2. The script should be reusable without any modifications to the script itself
3. The script should get it's job done without needless complication
4. Script configuration should be logical and easy 

## Script Design


### A Couple Notes on ACLs

1. Cisco ACLs have an implicit __deny__ at the end.
2. An ACL that hasn't been created can be configured (ie applied to an interface, VTY line, etc.). In this case, the ACL is immediately used when created. Because of the implicit deny this means you can easily lock yourself out of a device with an ACL applied to the management interface.

### Pushing ACLs, two Options

1. Rip and Replace
	
	By rip and replace, I mean deleting the ACL and recreating it. This is what I prefer to do, it enforces consistency and line ordering. However, caution should be used when modifying ACLs on management interfaces and VTY using this method. I should note that this will result in *brief* packet loss as the ACL is being recreated. Depending on how the ACL is used, this could be perfectly acceptable.
	
	Here's how the rip and replace method looks on the CLI:
	
	```
	ntn(config)#no ip access-list extended TEST 
	ntn(config)#ip access-list extended TEST 
	ntn(config-ext-nacl)#permit ip host 192.168.1.1 any 
	ntn(config-ext-nacl)#permit ip host 192.168.1.2 any 
	ntn(config-ext-nacl)#deny ip any any log
	```
	
2. Modify in Place

	This is what I do with ACLs applied in places that either cannot handle short disruptions or when the rip and replace method could cause loss of management access to the network device. 

	Here's how the modify in place method looks on the CLI:
	
	```
	ntn(config)#ip access-list extended TEST
	ntn(config)#ip access-list extended TEST
	ntn(config)#ip access-list extended TEST
	ntn(config-ext-nacl)#do sh ip access-list TEST
	Extended IP access list TEST
	    10 permit ip host 192.168.1.1 any
	    20 permit ip host 192.168.1.2 any
	    21 permit ip any any log
	    30 deny ip any any log
	ntn(config-ext-nacl)#
	```

__mod_acl__ implements both of these methods.

### 

## Installation
* Clone the repository
`git clone https://github.com/bjames/mod_acl`
* Initialize a new python virtual environment
`python -m virtualenv venv`
* Install the required python modules
`.\venv\bin\python -m pip -r requirements.txt`

## Configuration

The YAML file defines

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