BASEDIR=$(CURDIR)
USRDBFILE=$(BASEDIR)/tmp/applyProject.db
APPLYPROJECT=$(BASEDIR)/applyProject.go
TMPDIR=$(BASEDIR)/tmp
SENDMAIL=$(BASEDIR)/sendEmail.py
#TIME=$(shell date "+%Y_%m_%d-%H:%M:%S")
TIME=$(shell date "+%Y_%m_%d-%H")
init:
	cp $(BASEDIR)/tmp/applyProject.db $(BASEDIR)/db_bak/applyProject.db.bak_$(TIME)
	chmod 777 $(TMPDIR)
	chmod 777 $(USRDBFILE)
	chmod +x $(DINNER)
	chmod +x $(SENDEMAIL)
build:
	go build --tags "libsqlite3 linux" $(APPLYPROJECT)

help:
	@echo 'Makefile for initialize dinner programe             '
	@echo '                                                    '
	@echo 'Usage:                                              '
	@echo '   make init        initialize applyPROJECT programe'
	@echo '   make build       build applyPROJECT programe     '
