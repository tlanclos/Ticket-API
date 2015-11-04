include ../vars.mk

WSGI_CONFIGS += ticketapi.wsgi
WSGI_CONFIGS += nossl.wsgi

PACKAGES += apps
PACKAGES += data
PACKAGES += datalayer

# The real file must be named <somename>.example, but here
# do not append the ".example" extension, this will be considered
SETTINGS = settings.json

build:
	@echo "No build required"

install: server-root wsgi-config packages $(SETTINGS)

server-root:
	@install -v -m $(SERVER_ROOT_CHMOD) $(SERVER_INSTALL_FLAGS) -d $(SERVER_ROOT)

wsgi-config: $(WSGI_CONFIGS)
	@install -v -m $(SERVER_BIN_CHMOD) $(SERVER_INSTALL_FLAGS) $^ $(SERVER_ROOT)/.

packages: $(PACKAGES)
	@cp -vr $^ $(SERVER_ROOT)/.
	@chown -vR $(SERVER_CHOWN) $(SERVER_ROOT)/.
	@chmod -vR $(SERVER_BIN_CHMOD) $(SERVER_ROOT)/.
	@find $(SERVER_ROOT) -type d -exec chmod $(SERVER_ROOT_CHMOD) {} \;

$(SETTINGS): $(SETTINGS).example
	@[ -f $(SERVER_ROOT)/$@ ] || install -m $(SECURE_CHMOD) $(SECURE_INSTALL_FLAGS) $< $(SERVER_ROOT)/$@

clean:
	@echo "Nothing to clean"
