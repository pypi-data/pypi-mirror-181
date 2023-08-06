run_manual_test:
	rm -fr tmp/*
	GITLAB_ACCESS_TOKEN=glpat-8Y1YCo8Ygb6uqgDWcX41 GITHUB_OAUTH_TOKEN=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 \
	git-multi-repo-updater -r repos.txt -v --clone-to=tmp -m "Update mypy version" examples/update_mypy_version.py
	# git-multi-repo-updater -r repos.txt -v --clone-to=tmp -m "Hello world" touch labas.txt
	# venv/bin/python gitmultirepoupdater/cli.py --repos https://github.com/albertas/git-multi-repo-updater

test_update_files:
	venv/bin/python3.9 update_version.py

test_throttled_tasks_executor:
	venv/bin/python reactor.py

venv:
	python3.9 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt --use-pep517
	venv/bin/pip install -e .

publish:
	venv/bin/hatch build
	venv/bin/hatch publish

flake8:
	venv/bin/flake8 gitmultirepoupdater

mypy:
	venv/bin/mypy gitmultirepoupdater

test:
	venv/bin/pytest $(PYTEST_ME_PLEASE)

check: test flake8 mypy
