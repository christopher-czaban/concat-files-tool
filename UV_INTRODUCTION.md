# UV: Modern Python Package Management

This guide provides a comprehensive introduction to uv, explaining its key features and advantages over traditional Python packaging methods.

## Table of Contents
1. [What is UV?](#what-is-uv)
2. [Key Features](#key-features)
3. [Package Management Comparison](#package-management-comparison)
4. [Project Structure](#project-structure)
5. [Development Workflow](#development-workflow)
6. [Building and Distribution](#building-and-distribution)
7. [Tool Installation System](#tool-installation-system)
8. [Best Practices](#best-practices)

## What is UV?

UV is a modern Python package manager and build system written in Rust. It's designed to be:
- Fast: Built in Rust for maximum performance
- Modern: Uses current best practices in Python packaging
- Developer-friendly: Optimized for development workflows
- Compatible: Works with existing Python packaging tools

## Key Features

### 1. Virtual Environments
**Traditional (venv):**
```bash
python -m venv .venv
source .venv/bin/activate
```

**UV:**
```bash
uv venv
source .venv/bin/activate
```

UV's virtual environments are faster to create and more lightweight.

### 2. Package Installation
**Traditional (pip):**
```bash
pip install package-name
```

**UV:**
```bash
uv pip install package-name
```

UV offers:
- Faster resolution of dependencies
- More reliable dependency resolution
- Better handling of conflicts

### 3. Tool Installation
**Traditional:**
```bash
pip install -e .
# Changes require reinstallation
```

**UV:**
```bash
uv tool install .
# Changes take effect immediately
```

## Package Management Comparison

### Traditional Workflow (pip/setuptools)
1. Create setup.py or pyproject.toml
2. Build package
3. Install package
4. For changes:
   - Rebuild package
   - Reinstall
   - Test changes

### UV Workflow
1. Create pyproject.toml
2. Install directly with uv tool
3. For changes:
   - Edit code
   - Changes take effect immediately
   - Test changes

## Project Structure

### Modern UV Project
```
project_name/
├── project_name/          # Package directory
│   ├── __init__.py
│   └── main.py
├── pyproject.toml        # Project configuration
└── README.md
```

### pyproject.toml Example
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.8"

[project.scripts]
command-name = "project_name.main:main"
```

## Development Workflow

### Traditional Development
1. Make changes
2. Build package:
   ```bash
   python setup.py develop
   # or
   pip install -e .
   ```
3. Test changes
4. Repeat

### UV Development
1. Initial setup:
   ```bash
   uv tool install .
   ```
2. Make changes
3. Test immediately
4. Repeat

## Building and Distribution

### What is a Wheel?
- A wheel (.whl) is a built package format
- Contains:
  - Python code files
  - Data files
  - Metadata
  - Entry points

### Building with UV
```bash
uv build
```
Creates:
- source distribution (.tar.gz)
- wheel distribution (.whl)

### Installation Methods

#### 1. Development Installation
```bash
uv tool install .
```
- Links directly to source code
- Changes take effect immediately
- Perfect for development

#### 2. Wheel Installation
```bash
uv pip install dist/*.whl
```
- Installs a copy of the code
- Changes require rebuild
- Better for distribution

## Tool Installation System

### How UV Tools Work
1. **Traditional Package Installation:**
   ```
   Your Code → Build Wheel → Copy to site-packages → Run copied code
   ```

2. **UV Tool Installation:**
   ```
   Your Code → Create command script → Run original code directly
   ```

### Advantages of UV Tools
1. **Development Speed**
   - No rebuild needed
   - Instant feedback
   - Direct code execution

2. **Simplicity**
   - Fewer steps
   - Less configuration
   - Clear workflow

3. **Reliability**
   - No version conflicts
   - Predictable behavior
   - Isolated environments

## Best Practices

### 1. Project Configuration
- Use `pyproject.toml` instead of setup.py
- Keep configuration minimal
- Use hatchling as build backend

### 2. Development
- Use `uv tool install` for development
- Keep source code in package directory
- Use clear entry points

### 3. Distribution
- Build wheels for distribution
- Include all necessary files
- Test installation from wheel

### 4. Virtual Environments
- Create one per project
- Use UV's venv command
- Keep environments isolated

## Common Issues and Solutions

1. **"No executables provided"**
   - Check project.scripts in pyproject.toml
   - Verify entry point function exists

2. **Import errors**
   - Check package structure
   - Verify file inclusion in pyproject.toml

3. **Changes not taking effect**
   - Ensure using uv tool install for development
   - Check file paths and imports

## Further Reading
- [UV Documentation](https://docs.astral.sh/uv/)
- [Python Packaging Guide](https://packaging.python.org/)
- [PEP 621 – Project Metadata](https://peps.python.org/pep-0621/) 