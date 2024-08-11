
# use Case 1
def analyze_text_with_walrus(text):
    details: dict = {
        'words': (words := text.split()),
        'amount': len(words),
        'chars': len(''.join(words)),
        'reversed': words[::-1]
    }
    return details

# print(analyze_text("Hello, World!"))
print(analyze_text_with_walrus("Hello, World!"))

