import openai as correct
correct.api_key = "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"
def correct_word(word):
    prompt = f"Correct the word: {word}\n\n"
    response = correct.Edit.create(
  model="text-davinci-edit-001",
  input=word,
  instruction="Correct this to standard English:",
  temperature=0,
  top_p=1
)

    corrected_word = response.choices[0].text.strip()
    return corrected_word

def main():
    word = input("Enter a word: ")
    corrected_word = correct_word(word)
    print("Corrected word:", corrected_word)

if __name__ == "__main__":
    # Set your OpenAI API key
    correct.api_key = "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"
    main()
