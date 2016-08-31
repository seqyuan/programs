BASEDIR=$(CURDIR)
USRDBFILE=$(BASEDIR)/tmp/usr.db
DINNERMENU=$(BASEDIR)/menu.ini
USRDINNER=$(BASEDIR)/usrDinner.ini
DINNER=$(BASEDIR)/dinner
TMPDIR=$(BASEDIR)/tmp
DINNEREMAIL=$(BASEDIR)/dinnerEmail.py
#TIME=$(shell date "+%Y_%m_%d-%H:%M:%S")
TIME=$(shell date "+%Y_%m_%d-%H")
init:
	cp $(BASEDIR)/tmp/usr.db $(BASEDIR)/db_bak/usr.db.bak_$(TIME)
	chmod 777 $(USRDBFILE)
	chmod 777 $(TMPDIR)
	chmod 777 $(USRDBFILE)
	chmod 777 $(DINNERMENU)
	chmod 777 $(USRDINNER)
	chmod +x $(DINNER)
	chmod +x $(DINNEREMAIL)


help:
	@echo 'Makefile for initialize dinner programe       '
	@echo '                                              '
	@echo 'Usage:                                        '
	@echo '   make init        initialize dinner programe'
	@echo '                                              '
