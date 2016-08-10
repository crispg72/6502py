
APPNAME=eunit

SUB_DIRECTORIES = 

all: subdirs

subdirs:
	@for d in *.erl; do \
        (erlc $$d); \
	done

clean:
	@for d in *.erl; do \
        (rm $$d.beam); \
	done

docs:
	erl -noshell -eval "edoc:application($(APPNAME), \".\", [$(DOC_OPTS)])" -s init stop

test: subdirs
	@echo Testing...
	erl -noshell -pa ebin -eval 'eunit:test(opcode,[verbose])' -s init stop