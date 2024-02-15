
## ~~ SAVE VARIABLE AS TXT USING SPECIAL __FILE__ VARIABLE ~~ ##


def save_as_txt(text, file_path):

    # Write to the file
    with open(file_path, 'w') as file:
        file.write(text)

    print("Data written to", file_path)
