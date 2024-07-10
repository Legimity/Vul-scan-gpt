import re

def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |   # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)
    return ansi_escape.sub('', text)


if __name__ == '__main__':
    with open('result/Vulmap.txt', 'r') as file:
        content = file.read()

    clean_content = remove_ansi_escape_sequences(content)

    with open('result/Vulmap_clean.txt', 'w') as file:
        file.write(clean_content)

    print("ANSI escape sequences removed successfully.")
