# Test Suite Restructuring Implementation Plan

## Current State Analysis

### Existing Structure

```
tests/
├── __init__.py
├── fixtures/
│   ├── __init__.py
│   ├── sample_code.py (empty)
│   └── sample_docs.md (empty)
├── test_commands.py (empty)
├── test_config.py (672 lines, comprehensive)
├── test_cursor_setup.py (342 lines)
├── test_decorator_parser.py (351 lines)
├── test_template.py (464 lines)
└── test_validation.py (empty)
```

### Current Issues

1. **Monolithic test files**: Large test files with multiple concerns
2. **Flat structure**: No separation between unit, integration, and end-to-end tests
3. **Unused fixtures**: Empty fixture files and sample data
4. **Mixed concerns**: Tests mixing low-level units with higher-level workflows
5. **No shared utilities**: Repeated test setup patterns across files

## Proposed Modular Structure

### New Directory Layout

```
tests/
├── __init__.py
├── conftest.py                 # Global pytest configuration and fixtures
├── unit/                       # Pure unit tests (isolated, fast)
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── test_decorator_parser.py
│   │   ├── test_template_engine.py
│   │   ├── test_git_utils.py
│   │   └── test_validation_rules.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── test_config_management.py
│   │   ├── test_file_operations.py
│   │   ├── test_output_formatting.py
│   │   └── test_cursor_integration.py
│   └── cli/
│       ├── __init__.py
│       ├── test_command_parsing.py
│       ├── test_command_validation.py
│       └── test_exit_codes.py
├── integration/                # Component integration tests
│   ├── __init__.py
│   ├── test_config_loading.py
│   ├── test_template_creation.py
│   ├── test_decorator_scanning.py
│   ├── test_git_integration.py
│   └── test_cursor_setup.py
├── e2e/                       # End-to-end workflow tests
│   ├── __init__.py
│   ├── test_init_workflow.py
│   ├── test_validation_workflow.py
│   ├── test_review_workflow.py
│   ├── test_create_lore_workflow.py
│   └── test_map_workflow.py
├── fixtures/                  # Shared test data and utilities
│   ├── __init__.py
│   ├── configs/
│   │   ├── valid_config.json
│   │   ├── invalid_config.json
│   │   └── custom_config.json
│   ├── sample_code/
│   │   ├── python_with_decorators.py
│   │   ├── typescript_with_decorators.ts
│   │   ├── mixed_decorators.py
│   │   └── no_decorators.py
│   ├── sample_docs/
│   │   ├── complete_template.md
│   │   ├── partial_template.md
│   │   ├── empty_template.md
│   │   └── custom_template.md
│   └── repositories/
│       ├── simple_repo/
│       ├── complex_repo/
│       └── nested_repo/
├── utils/                     # Test utilities and helpers
│   ├── __init__.py
│   ├── assertions.py          # Custom assertion helpers
│   ├── builders.py            # Test data builders
│   ├── matchers.py           # Custom pytest matchers
│   ├── mocks.py              # Reusable mock objects
│   └── temp_environments.py   # Temporary environment setup
└── performance/              # Performance and load tests
    ├── __init__.py
    ├── test_large_repositories.py
    ├── test_many_decorators.py
    └── test_memory_usage.py
```

## Implementation Strategy

### Phase 1: Foundation Setup (2-3 hours)

#### 1.1 Create Base Structure

- Create new directory hierarchy
- Set up `conftest.py` with global fixtures
- Create shared utilities in `tests/utils/`

#### 1.2 Shared Fixtures (`conftest.py`)

```python
@pytest.fixture
def temp_project():
    """Create temporary project structure for testing."""

@pytest.fixture
def sample_config():
    """Load sample configuration for testing."""

@pytest.fixture
def mock_git_repo():
    """Create mock git repository."""

@pytest.fixture(scope="session")
def test_data_loader():
    """Load test data from fixtures directory."""
```

#### 1.3 Test Utilities (`tests/utils/`)

- **assertions.py**: Custom assertions for common patterns
- **builders.py**: Fluent builders for test objects
- **matchers.py**: Domain-specific matchers
- **mocks.py**: Reusable mock configurations
- **temp_environments.py**: Environment isolation helpers

### Phase 2: Unit Test Migration (4-5 hours)

#### 2.1 Core Module Unit Tests

Migrate and split existing tests into focused unit tests:

**From `test_config.py` →**

- `unit/utils/test_config_management.py` (config loading/saving/validation)
- `unit/utils/test_file_operations.py` (file system operations)
- `integration/test_config_loading.py` (environment integration)

**From `test_decorator_parser.py` →**

- `unit/core/test_decorator_parser.py` (regex parsing, file analysis)
- `integration/test_decorator_scanning.py` (repository scanning)

**From `test_template.py` →**

- `unit/core/test_template_engine.py` (template logic, population)
- `integration/test_template_creation.py` (file creation workflows)

**From `test_cursor_setup.py` →**

- `unit/utils/test_cursor_integration.py` (rule copying, validation)
- `integration/test_cursor_setup.py` (installation workflows)

#### 2.2 Test Class Decomposition

Break down large test classes by single responsibility:

```python
# Before: TestConfigurationBasics (mixed concerns)
# After:
class TestConfigPathResolution:
class TestConfigDefaults:
class TestConfigFileLoading:
class TestConfigValidation:
```

### Phase 3: Integration Test Creation (3-4 hours)

#### 3.1 Component Integration Tests

Create tests that verify components work together:

- **Config + Environment**: Configuration loading in different environments
- **Decorator Parser + Git**: Scanning changed files only
- **Template + Config**: Custom template loading and usage
- **Git + Validation**: Pre-commit hook integration

#### 3.2 Workflow Integration Tests

Test multi-step processes:

- **Template Creation Workflow**: Scan → Generate → Validate
- **Validation Workflow**: Load config → Scan files → Check git → Validate
- **Setup Workflow**: Create directories → Copy rules → Install hooks

### Phase 4: End-to-End Test Creation (2-3 hours)

#### 4.1 Command Workflow Tests

Test complete command executions:

```python
class TestInitWorkflow:
    def test_init_fresh_repository(self):
        """Test dm init on new repository."""

    def test_init_existing_lore(self):
        """Test dm init with existing .lore directory."""

class TestValidationWorkflow:
    def test_validation_blocks_commit_missing_docs(self):
        """Test that validation blocks commits when docs missing."""

    def test_validation_allows_commit_complete_docs(self):
        """Test that validation allows commits when docs complete."""
```

#### 4.2 Cross-Command Integration

Test command sequences that users actually perform:

```python
def test_complete_documentation_lifecycle(self):
    """Test: init → create-lore → edit docs → validate → commit."""
```

### Phase 5: Test Data and Fixtures (2-3 hours)

#### 5.1 Sample Code Fixtures

Create realistic sample code files:

- Python files with various decorator patterns
- TypeScript files with different comment styles
- Mixed language repositories
- Files with malformed decorators

#### 5.2 Configuration Fixtures

Create various configuration scenarios:

- Minimal valid configs
- Complete configs with all options
- Invalid configs for error testing
- Environment-specific configs

#### 5.3 Repository Fixtures

Create sample repository structures:

- Simple single-language repos
- Complex multi-language repos
- Repos with nested documentation structures

## Benefits of New Structure

### 1. Test Execution Speed

- **Unit tests**: Run in <5 seconds (no I/O, pure logic)
- **Integration tests**: Run in 10-30 seconds (limited I/O)
- **E2E tests**: Run in 30-60 seconds (full workflows)
- **Performance tests**: Run on-demand or in CI only

### 2. Test Clarity and Maintenance

- **Single responsibility**: Each test file has one clear purpose
- **Easier navigation**: Find tests by feature, not just by module
- **Reduced duplication**: Shared fixtures and utilities
- **Better coverage**: Clear separation between unit and integration coverage

### 3. Development Workflow

- **Fast feedback**: Run unit tests during development
- **Confidence building**: Integration tests for feature work
- **Release validation**: E2E tests before release
- **Performance monitoring**: Performance tests in CI

### 4. Test Quality

- **Better isolation**: Unit tests don't depend on file system
- **Realistic scenarios**: Integration tests use real workflows
- **User perspective**: E2E tests match actual usage patterns
- **Edge case coverage**: Dedicated files for error conditions

## Migration Guidelines

### Test Categorization Rules

**Unit Tests:**

- Test single functions or methods
- No file system operations (use mocks)
- No network operations
- No subprocess calls
- Fast execution (<100ms per test)

**Integration Tests:**

- Test 2-3 components working together
- Limited file system operations (temp directories)
- Mock external dependencies (git commands)
- Medium execution time (100ms-1s per test)

**E2E Tests:**

- Test complete user workflows
- Real file system operations
- Real git operations (in temp repos)
- Slower execution (1-10s per test)

### Code Organization Principles

1. **One concern per test file**
2. **Descriptive test class names** (TestConfigValidationRules, not TestConfig)
3. **Arrange-Act-Assert pattern** in all tests
4. **Shared setup in fixtures**, not in setUp methods
5. **Clear test names** that describe the scenario and expected outcome

### Fixture Design Patterns

```python
# Builder pattern for complex objects
@pytest.fixture
def config_builder():
    return ConfigBuilder().with_defaults()

# Parameterized fixtures for variations
@pytest.fixture(params=["python", "typescript", "javascript"])
def sample_code_file(request):
    return load_sample_code(request.param)

# Scope optimization
@pytest.fixture(scope="session")
def static_test_data():
    return load_static_data()
```

## Implementation Checklist

### Pre-Migration

- [ ] Create new directory structure
- [ ] Set up conftest.py with basic fixtures
- [ ] Create test utilities modules
- [ ] Set up sample test data files

### Migration Process

- [ ] Migrate config tests to new structure
- [ ] Migrate decorator parser tests
- [ ] Migrate template tests
- [ ] Migrate cursor setup tests
- [ ] Create new integration tests
- [ ] Create new E2E tests

### Post-Migration

- [ ] Update pytest configuration for new structure
- [ ] Update CI/CD to run different test categories
- [ ] Create test documentation for new structure
- [ ] Add performance test baseline measurements

### Validation

- [ ] All existing test functionality preserved
- [ ] Test execution time improved
- [ ] Coverage maintained or improved
- [ ] New test categories provide additional value

## Expected Timeline

- **Phase 1 (Foundation)**: 2-3 hours
- **Phase 2 (Unit Migration)**: 4-5 hours
- **Phase 3 (Integration)**: 3-4 hours
- **Phase 4 (E2E)**: 2-3 hours
- **Phase 5 (Fixtures)**: 2-3 hours
- **Validation & Documentation**: 1-2 hours

**Total Estimated Time**: 14-20 hours

This restructuring will create a more maintainable, faster, and more comprehensive test suite that better supports the development workflow and provides clearer feedback on different types of issues.
