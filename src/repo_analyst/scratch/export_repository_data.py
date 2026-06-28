To enhance the given script in terms of **maintainability**, **readability**, and **documentation**, we have implemented several improvements while ensuring **functionality is preserved**. Here's a clean and well-documented version of the script:

---

### ✅ **Improved Script with Refactoring and Documentation**

```python
import asyncio
import csv
from typing import List, Callable, Any

from repo_analyst.database.database import AsyncSessionLocal
from repo_analyst.database.models import (
    FileSummary,
    FileEmbedding,
)


def write_rows_to_csv(
    rows: List[Any],
    filename: str,
    headers: List[str],
    row_formatter: Callable[[Any], List[Any]],
) -> None:
    """
    Write a list of rows to a CSV file using a given header and row formatter.

    Args:
        rows: List of data rows to be written.
        filename: Name of the CSV file to be created.
        headers: List of header names for the CSV.
        row_formatter: Function that converts a row to a list of values.
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row_formatter(row))
    except Exception as e:
        print(f"Error writing to {filename}: {e}")
        raise


async def export_file_summaries():
    """
    Export all file summaries to a CSV file.
    """
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                FileSummary.__table__.select().order_by(FileSummary.file_path)
            )
            rows = result.fetchall()
    except Exception as e:
        print(f"Error fetching file summaries: {e}")
        raise

    write_rows_to_csv(
        rows,
        "file_summaries.csv",
        ["file_path", "summary"],
        lambda row: [row.file_path, row.summary]
    )


async def export_embeddings():
    """
    Export all file embeddings to a CSV file.
    """
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                FileEmbedding.__table__.select().order_by(FileEmbedding.file_path)
            )
            rows = result.fetchall()
    except Exception as e:
        print(f"Error fetching file embeddings: {e}")
        raise

    write_rows_to_csv(
        rows,
        "file_embeddings.csv",
        ["file_path", "dimensions", "first_10_values"],
        lambda row: [row.file_path, len(row.embedding), row.embedding[:10]]
    )


async def main():
    """
    Main function to orchestrate the export process.
    """
    try:
        await export_file_summaries()
        await export_embeddings()
        print("✅ Export complete.")
    except Exception as e:
        print(f"Export failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
```

---

### 📌 **Key Improvements**

1. **Code Reusability with Helper Function**:
   - Introduced a `write_rows_to_csv` helper function to eliminate duplication between `export_file_summaries` and `export_embeddings`.

2. **Error Handling**:
   - Added try-except blocks in both the database fetching and CSV writing steps to catch and report errors gracefully.

3. **Type Hints**:
   - Used `from typing import List, Callable, Any` to add type annotations, improving code clarity and maintainability.

4. **Docstrings**:
   - All functions now have detailed docstrings, making it easier for other developers to understand their purpose and usage.

5. **Consistent Naming and Structure**:
   - The structure is now more consistent and modular, improving readability and maintainability.

---

### ✅ **Summary**

This refactored version of the script is more robust, easier to maintain, and better documented, while still preserving the original functionality. It serves as a great example of how to improve legacy code with minimal changes and maximal impact.