include vars.mk

build:
	@$(MAKE) -C config 		build
	@$(MAKE) -C ticketapi	build

install:
	@$(MAKE) -C config			install
	@$(MAKE) -C ticketapi		install

clean:
	@$(MAKE) -C config			clean
	@$(MAKE) -C ticketapi		clean
