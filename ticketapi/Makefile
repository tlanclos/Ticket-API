include ../vars.mk

WSGI_CONFIGS += ticketapi.wsgi
WSGI_CONFIGS += nossl.wsgi

APPLICATIONS += ticketapi.py
APPLICATIONS += nossl.py

build:
	@echo "Not implemented yet"

install: server-root wsgi-config application
	@echo "Not implemented yet"

server-root:
	@install -v -m $(SERVER_ROOT_CHMOD) $(SERVER_INSTALL_FLAGS) -d $(SERVER_ROOT)

wsgi-config: $(WSGI_CONFIGS)
	@install -v -m $(SERVER_BIN_CHMOD) $(SERVER_INSTALL_FLAGS) $^ $(SERVER_ROOT)/.

application: $(APPLICATIONS)
	@install -v -m $(SERVER_BIN_CHMOD) $(SERVER_INSTALL_FLAGS) $^ $(SERVER_ROOT)/.

clean:
	@echo "Not implemented yet"
