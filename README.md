# CloudTUI-FTS (BETA)

### Authors
Andrea Lombardo<br/>
Davide Monfrecola

### Institute
Department of Science and Innovation Technology (DiSIT) - University of Piemonte Orientale - ITALY

### Superadvisor
Massimo Canonico

### Contact info
massimo.canonico@unipmn.it

### Description
Cloud Text User Interface - Fault Tolerant Scalable (CloudTUI-FTS)
is text user interface able to interact with multiple
cloud platforms (such as OpenStack, Eucalytus, ...).

With CloudTUI-FTS, a user can:
- start/stop/clone a VM
- monitor the VM health status
- create/manage policies in order to prevent faults (i.e.,
"if the CPU utilization is higher than XX %, then clone it")

CloudTUI-FTS is an open source project written in python,
free available under GPL v.3 license.

		----
Quick start:

0.) Install the required libraries
	0.a) boto (the following command should work on most 
			of the linux distos:
	 		"sudo pip install boto")
	0.b) python-novaclient ("sudo pip install pythom-novaclient")
	0.c) python-ceilometerclient ("sudo pip install python-ceilometerclient")
	0.d) antlr3 ("sudo pip install http://www.antlr3.org/download/Python/antlr_python_runtime-3.1.3.tar.gz") 


1.) Download the source code from git repository by using one of the following tw methods:
	1.a) git clone https://github.com/trampfox/CloudTUI-advanced.git
	1.b) wget https://github.com/trampfox/CloudTUI-advanced/archive/master.zip

For support or any comment: massimo.canonico@unipmn.it
