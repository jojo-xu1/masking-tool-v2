# Quickstart: ユーザー向け操作手順書

## Create or Update the Markdown Guide

Create the source guide:

```powershell
docs\user-guide.md
```

Verify it covers:

1. Tool purpose.
2. Supported and excluded scope.
3. Replacement table requirements.
4. Single-file flow.
5. Folder flow.
6. Result review.
7. Troubleshooting.
8. Pre-use checklist.
9. Review questions and elapsed-time recording.

## Generate PDF

Generate the distribution copy from the Markdown source:

```powershell
python -m masking_tool.docgen docs\user-guide.md docs\user-guide.pdf
```

Expected output:

```text
docs\user-guide.pdf
```

Retention decision: `docs\user-guide.pdf` is a tracked distribution artifact for
this feature. It is generated from `docs\user-guide.md` and should be committed
with the Markdown source when the guide changes.

## Validate

Run guide contract tests:

```powershell
python -m pytest tests\contract\test_user_guide_contract.py
```

Manual review:

1. Open `docs\user-guide.md`.
2. Open `docs\user-guide.pdf`.
3. Confirm both contain the same required workflow, scope, troubleshooting, and
   pre-use checklist content.
4. Confirm the PDF is readable for a business user who has only
   `MaskingTool.exe`.
5. Confirm the guide body includes fields to record single-file and folder
   sample run times.
6. Confirm the guide body includes review questions and the 90% correctness
   threshold.

Latest validation result:

- 2026-06-02: `python -m pytest tests\contract\test_user_guide_contract.py`
  completed with 15 passed.

## Known Non-Goals

- No installer guide.
- No developer build guide.
- No separate review checklist document.
- No multilingual documentation.
