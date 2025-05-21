# scripts/extract_spellings.py
import os, sys, argparse
from spelling_extractor.pdf_parser import extract_text_from_pdf
from spelling_extractor.llm_interface import extract_spellings
from spelling_extractor.word_export   import create_spelling_doc

def main():
    p = argparse.ArgumentParser(
        description="Extract next week's spellings from a newsletter PDF"
    )
    p.add_argument(
        "pdf_path",
        help="Path to the newsletter PDF"
    )
    args = p.parse_args()
    pdf = args.pdf_path

    if not os.path.exists(pdf):
        print(f"❌ PDF not found: {pdf}")
        sys.exit(1)

    # 1) extract text
    text = extract_text_from_pdf(pdf)
    print("🔍 First 200 chars of text:\n", text[:200], "…")   # DEBUG

    # 2) get spellings
    spellings = extract_spellings(text)
    print("📝 Spellings found:", spellings)                   # DEBUG

    # 3) build doc
    if spellings:
        out = create_spelling_doc(spellings)
        print(f"✅ Saved to {out}")
    else:
        print("⚠️  No spellings extracted.")

if __name__ == "__main__":
    main()
