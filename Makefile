#Files
DEPS = rtleds.py
EXE = main.py

#RT Target Network Settings
IPADDR = 10.204.217.29
USR = admin

#App paths
HOME = /home/admin

#Rules +++++++++++++++++++++++++++++++++++++++++++++++

#+++ Network actions +++

deploy:
	@echo "Deploying <$(EXE)> to target <$(IPADDR)>..."
	@scp -q $(EXE) $(USR)@$(IPADDR):$(HOME)
	@echo "Deploying <$(DEPS)> to target <$(IPADDR)>..."
	@scp -q $(DEPS) $(USR)@$(IPADDR):$(HOME)
	@echo "Deployment completed! ----------------------"

connect:
	@echo "Connecting to target <$(IPADDR)>..."
	@ssh -q $(USR)@$(IPADDR)

#Deploy & Connect
cdeploy:
	clear
	@make deploy --no-print-directory
	@make connect --no-print-directory