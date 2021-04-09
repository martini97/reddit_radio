outputs = $(objects:.in=.txt)
sync-targets = $(objects:%.in=sync-%)
upgrade-targets = $(objects:%.in=upgrade-%)

.PHONY: all check clean $(sync-targets) $(upgrade-targets)

all: $(outputs)

%.txt: %.in
	@pip-compile -v --output-file $@ $<

dev.txt: main.txt

check:
	@which pip-compile > /dev/null

clean: check
	-@rm *.txt

$(sync-targets): sync-%: %.txt
	@pip-sync $<

$(upgrade-targets): upgrade-%: %.in
	@pip-compile --upgrade $<

upgrade-dev: upgrade-main
