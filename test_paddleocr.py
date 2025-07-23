import paddle
try:
    from paddleocr import PaddleOCR
    print("PaddleOCR imported successfully!")
except ImportError as e:
    print(f"Import error: {e}")
    # Suggestion: Run 'pip install paddleocr' if import fails
    exit(1)  # Stop if import fails

# Check CUDA/GPU support
if paddle.is_compiled_with_cuda():
    print("GPU is available.")
else:
    print("Using CPU.")

# Initialize PaddleOCR (updated to avoid deprecation warning)
ocr = PaddleOCR(use_textline_orientation=True, lang='en')  # Use this for newer versions

# Test with your image (use raw string for Windows path)
image_path = r'D:\CLONEProjects\Projects\GROCERYTRACKERPERP\test_image.jpg'

try:
    result = ocr.ocr(image_path, cls=True)
    if result and result[0]:
        print("\nDetected text:")
        for line in result[0]:
            print(line[1][0])  # Print detected text
    else:
        print("No text detected in the image.")
except Exception as e:
    print(f"Error during OCR processing: {e}")
