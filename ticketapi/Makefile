include ../vars.mk

WSGI_CONFIGS += ticketapi.wsgi
WSGI_CONFIGS += nossl.wsgi

SOURCE += ticketapi.py
SOURCE += nossl.py
SOURCE += response.py
SOURCE += fields.py
SOURCE += validators.py
SOURCE += __init__.py

build:
	@echo "Not implemented yet"

install: server-root wsgi-config application
	@echo "Not implemented yet"

server-root:
	@install -v -m $(SERVER_ROOT_CHMOD) $(SERVER_INSTALL_FLAGS) -d $(SERVER_ROOT)

wsgi-config: $(WSGI_CONFIGS)
	@install -v -m $(SERVER_BIN_CHMOD) $(SERVER_INSTALL_FLAGS) $^ $(SERVER_ROOT)/.

application: $(SOURCE)
	@install -v -m $(SERVER_BIN_CHMOD) $(SERVER_INSTALL_FLAGS) $^ $(SERVER_ROOT)/.

clean:
	@echo "Not implemented yet"
