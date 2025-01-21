import re

def cap(text) -> str:
    # Use regular expression to split text into sentences.
    # Assumes that sentences end with '.', '!', or '?'.
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)

    # Capitalize the first letter of each sentence.
    capitalized_sentences = [sentence.capitalize() for sentence in sentences]

    # Join the sentences back into a single text with capitalized sentences.
    result_text = ' '.join(capitalized_sentences)
    return result_text