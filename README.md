# OCR_receipts
Run OCR on receipts to extract date, total amount

## Description
This script uses pictures of receipts to extract the total amount, date and shop name. The regex rules haven't been optimized yet. I tried using Name Entity Recognition to extract the same informations: it works quite well for the money, but doesn't pick up dates or shop names.

## Personal development goals:
- Practising implementing image pre-processing for OCR
- Setting up and using OCR (via tesseract)

## Status of development:
- :white_check_mark: Pre-process receipt image to enhance quality
- :white_check_mark: Run OCR Tesseract on image
- :white_check_mark: Add Regex rules for Money, Date and Org
- :white_check_mark: Save results in CSV
- [TO DO] Optimize the regex rules

## Requirements:
The main librairies are:
- `opencv`
- `numpy`
- `PIL`
- `pytesseract` + `Tesseract`
- `pandas`

## Execution:
`python3 main.py`