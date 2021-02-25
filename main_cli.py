import extraction, crop, compare

print("\nSelect an option:\n1. Signature Extraction only.\n2. Signature Comparison only.\n3. Both Signature Extraction and Comparison.\n4. Exit")

option = int(input("\nEnter an option (1 - 4): "))

if (option in (1, 2, 3, 4)):
    if (option == 1):
        src_img_path = input("\nEnter the name or path of the source image file: ")
        print(extraction.extract(src_img_path))
    elif (option == 2):
        src_img_path = input("\nEnter the name or path of the source image file: ")
        ref_img_path = input("\nEnter the name or path of the reference image file: ")
        print(compare.compare(src_img_path, ref_img_path))
    elif (option == 3):
        print("\nSignature Extraction:")
        src_img_path = input("\nEnter the name or path of the source image file: ")
        print(extraction.extract(src_img_path))

        print("\nSignature Comparison:")
        src_img_path = input("\nEnter the name or path of the source image file: ")
        ref_img_path = input("\nEnter the name or path of the reference image file: ")
        print(compare.compare(src_img_path, ref_img_path))
else:
    print("\nEnter a valid option.")