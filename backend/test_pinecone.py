import pinecone
print(f"Pinecone file: {pinecone.__file__}")
try:
    from pinecone import Pinecone
    print("Success: Imported Pinecone class")
except ImportError as e:
    print(f"Error: {e}")
    print(f"Dir: {dir(pinecone)}")
