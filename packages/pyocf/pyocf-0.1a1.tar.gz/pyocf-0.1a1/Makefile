root_dir := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
bin_dir := $(root_dir)/ve/bin
git_source := git@github.com:regebro/Open-Cap-Format-OCF.git
git_branch := python-branch

all: devenv fetch build release

build: generate check

# The fullrelease script is a part of zest.releaser, which is the last
# package installed, so if it exists, the devenv is installed.
devenv:	ve/bin/fullrelease

ve/bin/fullrelease:
	virtualenv ve --python python3.10
	$(bin_dir)/pip install -e .[build]

fetch: Open-Cap-Format-OCF update

Open-Cap-Format-OCF:
	git clone $(git_source)

update:
	cd Open-Cap-Format-OCF; \
	git checkout $(git_branch); \
	git pull

generate:
	$(bin_dir)/python3 utils/generate.py
	$(bin_dir)/black src/

check:
	$(bin_dir)/black src utils tests
	$(bin_dir)/flake8 src utils tests
	$(bin_dir)/pyroma -d .

coverage:
	$(bin_dir)/coverage run $(bin_dir)/pytest
	$(bin_dir)/coverage html
	$(bin_dir)/coverage report

tests/samples/Captable.zip: Open-Cap-Format-OCF/samples/*.json
	zip -j tests/samples/Captable.ocf.zip Open-Cap-Format-OCF/samples/*.json

test: tests/samples/Captable.ocf.zip
	$(bin_dir)/pytest

release:
	$(bin_dir)/fullrelease

clean:
	rm -rf Open-Cap-Format-OCF ve .coverage htmlcov .pytest_cache