#RT Target Network Settings
IPADDR = 10.204.217.29
USR = admin

#App paths ******************************************
MAKEFLAGS += --no-print-directory
HOME = /home/admin
EXE = main.py

# Find all Python files in current directory
PYTHON_FILES := $(wildcard *.py)

#Rules +++++++++++++++++++++++++++++++++++++++++++++++

#Deploy & Execute
run:
	cls
	@make deploy
	@echo Running $(EXE) ----------------------
	@ssh $(USR)@$(IPADDR) 'python $(EXE)'

#+++ Network actions +++

#Send every Python file of the project
.PHONY: deploy
deploy: $(PYTHON_FILES)
	@$(foreach file, $(PYTHON_FILES), $(info Deploying -> $(file)))
	@scp -q $? $(USR)@$(IPADDR):$(HOME)
	@echo Deployment completed! ----------------------

connect:
	@echo Connecting to target <$(IPADDR)>...
	@ssh -q $(USR)@$(IPADDR)

#Deploy & Connect
cdp:
	cls
	@make deploy --no-print-directory
	@make connect --no-print-directory

