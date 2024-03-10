src = src/
test_dir = test/

TEST = PYTHONPATH=$(src) python3 -m pytest
TEST_ARGS = -s --verbose --color=yes --cov=$(src)
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
STYLE_CHECK = flake8


.PHONY: all
all: check-style check-type run-test clean

.PHONY: check-type
check-type:
	$(TYPE_CHECK) .

.PHONY: check-style
check-style:
	$(STYLE_CHECK) .

.PHONY: fix-style
fix-style:
	autopep8 --in-place --recursive --aggressive --aggressive $(src)

.PHONY: test # alias for run-test
test: run-test

# discover and run all tests
.PHONY: run-test
run-test:
	$(TEST) $(TEST_ARGS) $(test_dir)


.PHONY: clean
clean:
# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -type d -name .coverage` # remove all coverage cache
