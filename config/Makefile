include ../vars.mk

APACHE_CONFIG_FILE = ticket-api.conf

build:
	@echo "Nothing to build"

install: apache-config

apache-config: $(APACHE_CONFIG_FILE)
	@install -v -m $(APACHE_CONFIG_CHMOD) $(APACHE_CONFIG_INSTALL_FLAGS) $^ $(APACHE_CONFIG_ROOT)/conf-available/.
	@ln -svf $(APACHE_CONFIG_ROOT)/conf-available/$^ $(APACHE_CONFIG_ROOT)/conf-enabled/$^

clean:
	@echo "Nothing to clean"
