# CloudTUI-FTS (BETA)

### Authors
Andrea Lombardo<br/>
Davide Monfrecola

### Institute
Department of Science and Innovation Technology (DiSIT) - University of Piemonte Orientale - ITALY

### Superadvisor
Massimo Canonico

### Contact info
massimo.canonico@uniupo.it

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

1. Install the required libraries
  1. boto (the following command should work on most of the linux distos: "sudo pip install boto")
  2. python-novaclient ("sudo pip install pythom-novaclient")
  3. python-ceilometerclient ("sudo pip install python-ceilometerclient")
  4. antlr3 ("sudo pip install http://www.antlr3.org/download/Python/antlr_python_runtime-3.1.3.tar.gz") 


2. Download the source code from git repository by using one of the following tw methods:
  1. git clone https://github.com/trampfox/CloudTUI-advanced.git
  2. wget https://github.com/trampfox/CloudTUI-advanced/archive/master.zip

For support or any comment: massimo.canonico@uniupo.it
