from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

text = '''
# Parent class
class Animal:
    def speak(self):
        print("This animal makes a sound.")

# Child class (inherits from Animal)
class Dog(Animal):
    def speak(self):
        print("The dog barks.")

# Example usage
a = Animal()
a.speak()

d = Dog()
d.speak()

'''

splitter = RecursiveCharacterTextSplitter.from_language(
    language= Language.PYTHON,
    chunk_size = 300,
    chunk_overlap =0 
)

chunks = splitter.split_text(text)

print(len(chunks))
print(chunks)