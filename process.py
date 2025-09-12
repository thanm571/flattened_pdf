import fitz  # PyMuPDF
import time
from pathlib import Path
from PIL import Image
import io
import os


def pdf_to_flattened_pdf(pdf_path, output_pdf, dpi=150, jpeg_quality=70):
    """
    Flatten a PDF into an image-based PDF, optimized for size.
    """
    start_time = time.time()
    src = fitz.open(pdf_path)
    out = fitz.open()

    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)

    for page_num, page in enumerate(src, start=1):
        pix = page.get_pixmap(matrix=mat)

        # Convert PyMuPDF pixmap → PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Save to JPEG with chosen quality
        img_bytes_io = io.BytesIO()
        img.save(img_bytes_io, format="JPEG", quality=jpeg_quality, optimize=True)
        img_bytes = img_bytes_io.getvalue()

        rect = page.rect
        new_page = out.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, stream=img_bytes)

        pix = None
        img.close()
        print(f"   ✔ Page {page_num}/{len(src)} done")

    out.save(output_pdf, deflate=True, garbage=4, clean=True)
    out.close()
    src.close()

    elapsed = time.time() - start_time
    print(f"✅ Flattened PDF saved as {output_pdf}")
    print(f"⏱ Time taken: {elapsed:.2f} seconds")


def batch_flatten_pdfs(input_folder, output_folder, dpi=150, jpeg_quality=70):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_path.glob("*.pdf"))
    if not pdf_files:
        print("⚠️ No PDF files found in", input_folder)
        return

    for pdf_file in pdf_files:
        try:
            out_file = output_path / f"{pdf_file.stem}_flat.pdf"
            print(f"\n📄 Processing: {pdf_file.name}")
            pdf_to_flattened_pdf(pdf_file, out_file, dpi=dpi, jpeg_quality=jpeg_quality)
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {type(e).__name__} - {e}")


if __name__ == "__main__":
    # Read paths from environment (set in Docker run)
    input_dir = os.getenv("INPUT_DIR", "input")
    output_dir = os.getenv("OUTPUT_DIR", "output")
    input_dpi = os.getenv("INPUT_DPI", "150")
    input_quality = os.getenv("INPUT_QUALITY", "70")

    batch_flatten_pdfs(
        input_folder=input_dir,
        output_folder=output_dir,
        dpi=int(input_dpi),
        jpeg_quality=int(input_quality)
    )
