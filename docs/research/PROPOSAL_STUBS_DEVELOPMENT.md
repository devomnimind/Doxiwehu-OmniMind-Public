# Proposal for Robust Community Stubs (OmniMind)

## 1. Objective
Eliminate "Bandaids" (`# type: ignore`) and false positives in static analysis by providing high-quality Type Stubs (`.pyi`) for key libraries that lack native type support. This improves the developer experience for the community.

## 2. Targeted Libraries (Critical)

| Library | Issue | Status |
| :--- | :--- | :--- |
| **`qdrant-client`** | `QdrantClient` lacks `search`, `query_points` attributes in static analysis. | 🔴 High Priority |
| **`sentence-transformers`** | `SentenceTransformer` lacks `encode` attribute. | 🔴 High Priority |
| **`datasets`** | `load_from_disk`, `load_dataset` not recognized. | 🔴 High Priority |
| **`numpy`** | `float(np.clip)` and other converters fail strict type check. | 🟡 Medium Priority |

## 3. Implementation Plan

### A. Structure
We will create a `src/stubs` directory in `omnimind_public` that matches the PEP 561 standard or simple local extension pattern.

```text
omnimind_public/
└── src/
    └── stubs/
        ├── qdrant_client/
        │   └── __init__.pyi
        ├── sentence_transformers/
        │   └── __init__.pyi
        └── datasets/
            └── __init__.pyi
```

### B. Stub Development Strategy

#### 1. Qdrant Client Stub
We will define the `QdrantClient` class with explicit signatures for `search`, `scroll`, `upsert`, matching the latest API but exposing them to MyPy.

#### 2. Sentence Transformers Stub
We will define `SentenceTransformer.encode` to accept `Union[str, List[str]]` and return `Union[List[float], ndarray]`.

#### 3. Datasets Stub
We will type `load_from_disk` and `load_dataset` to return `Dataset` or `DatasetDict` objects properly.

### C. Validation
We will add a `mypy.ini` configuration to `omnimind_public` that points to `src/stubs` as `mypy_path`.

```ini
[mypy]
mypy_path = src/stubs
explicit_package_bases = True
```

## 4. Execution Steps
1. Create `src/stubs/qdrant_client/__init__.pyi`
2. Create `src/stubs/sentence_transformers/__init__.pyi`
3. Create `src/stubs/datasets/__init__.pyi`
4. Add `mypy.ini` to root.
5. Verify checks pass.
