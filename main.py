from handling_presentations import extract_text_from_presentation



def main():
    # Example usage
    presentation_path = 'Tests.pptx'
    extracted_text = extract_text_from_presentation(presentation_path)

    # Print the extracted text from each slide
    for i, slide_text in enumerate(extracted_text):
        print(f"Slide {i + 1}:")
        print(slide_text)
        print()


if __name__ == '__main__':
    main()


