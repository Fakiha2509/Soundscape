import Levenshtein
import matplotlib.pyplot as plt
import cv2
import pytesseract

def calculate_accuracy_levenshtein(extracted_text, reference_text):
    """Calculate the accuracy of the extracted text compared to the reference text using Levenshtein distance."""
    distance = Levenshtein.distance(extracted_text, reference_text)
    max_len = max(len(extracted_text), len(reference_text))
    accuracy = (1 - distance / max_len) * 100
    return accuracy

def calculate_accuracy_cer(extracted_text, reference_text):
    """Calculate the accuracy of the extracted text compared to the reference text using Character Error Rate (CER)."""
    distance = Levenshtein.distance(extracted_text, reference_text)
    cer = distance / len(reference_text) * 100
    accuracy = 100 - cer
    return accuracy

def calculate_accuracy_wer(extracted_text, reference_text):
    """Calculate the accuracy of the extracted text compared to the reference text using Word Error Rate (WER)."""
    extracted_words = extracted_text.split()
    reference_words = reference_text.split()
    distance = Levenshtein.distance(' '.join(extracted_words), ' '.join(reference_words))
    wer = distance / len(reference_words) * 100
    accuracy = 100 - wer
    return accuracy

def plot_accuracies(accuracies):
    """Plot the accuracies of the extracted text using different methods."""
    methods = list(accuracies.keys())
    values = list(accuracies.values())
    colors = ['blue', 'green', 'red']
    
    plt.figure(figsize=(8, 6))
    plt.bar(methods, values, color=colors, width=0.4)
    plt.ylim(0, 100)
    plt.xlabel('Accuracy Method')
    plt.ylabel('Accuracy (%)')
    plt.title('Text Extraction Accuracy Comparison')
    plt.show()

def extract_text(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(processed_image)
    return text.strip()    

# Example usage
reference_text = "VIRTUAL CANVAS"
extracted_text = extract_text("/Users/apple/Desktop/virtual/WhatsApp Image 2025-03-04 at 15.06.50.jpeg")
print("Extracted Text:", extracted_text)

accuracy_levenshtein = calculate_accuracy_levenshtein(extracted_text, reference_text)
accuracy_cer = calculate_accuracy_cer(extracted_text, reference_text)
accuracy_wer = calculate_accuracy_wer(extracted_text, reference_text)

print(f"Levenshtein Accuracy: {accuracy_levenshtein:.2f}%")
print(f"CER Accuracy: {accuracy_cer:.2f}%")
print(f"WER Accuracy: {accuracy_wer:.2f}%")

accuracies = {
    "Levenshtein": accuracy_levenshtein,
    "CER": accuracy_cer,
    "WER": accuracy_wer
}

plot_accuracies(accuracies)