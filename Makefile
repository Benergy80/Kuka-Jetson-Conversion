.PHONY: install install-dev test lint format clean docs

# Install production dependencies
install:
	pip install -e .

# Install development dependencies
install-dev:
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

# Run all tests
test:
	python3 -m pytest tests/ -v --cov=src --cov-report=term-missing

# Run unit tests only
test-unit:
	python3 -m pytest tests/unit/ -v

# Run integration tests only
test-integration:
	python3 -m pytest tests/integration/ -v

# Run safety tests
test-safety:
	python3 -m pytest tests/unit/test_safety.py tests/integration/test_safety_system.py -v

# Lint code
lint:
	flake8 src/ tests/ --max-line-length=100
	mypy src/ --ignore-missing-imports

# Format code
format:
	black src/ tests/
	isort src/ tests/

# Check formatting without changes
format-check:
	black --check src/ tests/
	isort --check-only src/ tests/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build documentation
docs:
	cd docs && make html

# Run development server (for testing)
run:
	python -m src.control.realtime_controller

# Train a model
train:
	python scripts/training/train_act.py --config config/ml/act_config.yaml

# Benchmark model
benchmark:
	python scripts/deployment/benchmark_model.py
