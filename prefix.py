from sys import argv

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.next_column = 1

    def insert(self, word):
        """Insert a word into the Trie."""
        node = self.root
        for char in word.upper():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def get_prefix_columns(self):
        """Generate column numbers for each prefix."""
        prefix_columns = {}  # Maps prefixes to column numbers
        prefix_words = {}  # Maps column numbers to words
        letter_columns = {}  # Maps letters to their column references

        def traverse(node, prefix="", letter_start=""):
            nonlocal prefix_columns, prefix_words

            # Updated definition for identifying prefixes
            if len(node.children) > 1 or (node.is_end_of_word and len(node.children) > 0) and prefix:
                if prefix not in prefix_columns:
                    prefix_columns[prefix] = self.next_column
                    self.next_column += 1
                    prefix_words[prefix_columns[prefix]] = {"prefix": prefix, "words": {}}

                if letter_start and letter_start not in letter_columns:
                    letter_columns[letter_start] = prefix_columns[prefix]

            for char, child in sorted(node.children.items()):
                traverse(child, prefix + char, letter_start or prefix or char)

        traverse(self.root)
        return prefix_columns, prefix_words, letter_columns

        prefixes = collect_prefixes(self.root)
        print("Prefixes in the Trie:")
        for prefix in prefixes:
            print(prefix)
        return prefixes

    def visualize_trie(self):
        """Print the visualization of the Trie."""
        prefix_columns, prefix_words, letter_columns = self.get_prefix_columns()

        # Collect words
        def collect_words(node, prefix=""):
            result = []
            if node.is_end_of_word:
                result.append(prefix)
            for char, child in sorted(node.children.items()):
                result.extend(collect_words(child, prefix + char))
            return result

        all_words = collect_words(self.root)

        # Organize words by prefix and next letter
        for word in all_words:
            for i in range(1, len(word) + 1):
                prefix = word[:i].upper()
                if prefix in prefix_columns:
                    col_num = prefix_columns[prefix]
                    next_letter = word[i:i + 1].upper() if i < len(word) else ""
                    if next_letter not in prefix_words[col_num]["words"]:
                        prefix_words[col_num]["words"][next_letter] = []
                    prefix_words[col_num]["words"][next_letter].append(word)

        max_column = max(prefix_columns.values()) if prefix_columns else 1

        # Print each row
        all_rows = ['blank'] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        first_letter_words = {}  # Words that start with each letter

        # First collect single-letter words and words without a prefix
        for word in all_words:
            first_letter = word[0].upper()
            if len(word) == 1 or word not in prefix_columns:  # Words that don't need a separate prefix column
                if first_letter not in first_letter_words:
                    first_letter_words[first_letter] = []
                first_letter_words[first_letter].append(word)

        for row in all_rows:
            display_row = row.upper() if row != 'blank' else row
            print(f"{display_row:<10}", end="")

            row_data = ["0"] * max_column  # Initialize with "0" for all columns

            # Handle first column - either show words or point to next column
            if row != 'blank':
                if row in letter_columns:
                    row_data[0] = str(letter_columns[row])  # Reference to next column
                elif row in first_letter_words:
                    # Update row_data with the words
                    words_to_print = first_letter_words[row]
                    if words_to_print:
                        row_data[0] = ", ".join(words_to_print)

            # Fill in word data for other columns
            for col_num, data in prefix_words.items():
                if col_num > 1:  # Skip first column as it's handled above
                    # Only show words in the "blank" row if they are full prefixes
                    if row == 'blank' and data["prefix"] in all_words:
                        row_data[col_num - 1] = data["prefix"]  # Show prefix in blank row
                    elif row != 'blank':
                        next_letter = row
                        if next_letter in data["words"]:
                            # Only include words that are starting with the current letter
                            new_words = data["words"][next_letter]
                            if new_words:
                                # If there's more than one word, indicate a new column
                                if len(new_words) > 1:
                                    row_data[col_num - 1] = str(col_num +1)  # Correct the column index
                                else:
                                    row_data[col_num - 1] = ", ".join(new_words)

            # Print row data
            print(row_data)  # Print row data in columns

def build_trie_from_file(filename):
    trie = Trie()
    with open(filename, 'r') as file:
        words = file.read().splitlines()
        for word in words:
            trie.insert(word)
    return trie

# Example usage
filename = argv[1]
trie = build_trie_from_file(filename)

# Visualize
trie.visualize_trie()
