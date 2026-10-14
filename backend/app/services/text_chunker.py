# This class splits large text into smaller meaningful chunks.
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str):
    # Create the text splitter.
    # chunk_size: Maximum approximate size of each chunk.
    # chunk_overlap: Number of characters that can be repeated between neighbouring chunks.
    # The splitter tries these separators
        # in this order.
        # First: paragraph
        # Then:  line
        # Then: word
        # Finally: character
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
    )
    separators = ["\n\n", "\n", " ", ""]
    # Split the complete extracted document into smaller chunks.
    chunks = splitter.split_text(text)

    return chunks