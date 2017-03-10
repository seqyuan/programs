BASEDIR=$(CURDIR)
USRDBFILE=$(BASEDIR)/../bin/tmp/applyProject.db
APPLYPROJECT=$(BASEDIR)/applyProject.go
APPLYPROJECT_PROGRAM=$(BASEDIR)/applyProject
TMPDIR=$(BASEDIR)/../bin/tmp
SENDMAIL=$(BASEDIR)/sendEmail.py
#TIME=$(shell date "+%Y_%m_%d-%H:%M:%S")
TIME=$(shell date "+%Y_%m_%d-%H")
init:
#	$(BASEDIR)/../bin/applyProject -creatdb
#$(BASEDIR)/../bin/applyProject -creatusrdb
	cp $(BASEDIR)/../bin/tmp/applyProject.db $(BASEDIR)/../bin/db_bak/applyProject.db.bak_$(TIME)
	chmod 777 $(TMPDIR)
	chmod 777 $(USRDBFILE)
	chmod +x $(BASEDIR)/../bin/applyProject
	chmod +x $(BASEDIR)/../bin/sendEmail.py

install:
	go build --tags "libsqlite3 linux" $(APPLYPROJECT)
	mkdir -p ../bin/tmp
	mkdir -p ../bin/db_bak
	mv $(APPLYPROJECT_PROGRAM) ../bin
	cp $(SENDMAIL) ../bin


help:
	@echo 'Makefile for initialize applyProject programe       '
	@echo '                                                    '
	@echo 'Usage:                                              '
	@echo '   make init        initialize applyPROJECT programe'
	@echo '   make install     build applyPROJECT programe     '
