import argparse
from glob import glob
from app.dependency import ChromaInstance

DEFAULT_CHUNK_SIZE = 20
db = ChromaInstance()

def existGlobItems(path):
    images = glob(path)
    return len(images) > 0

def uploadByChunk(path, chunk_size=DEFAULT_CHUNK_SIZE):
    images = glob(path)
    ids = [image.split('/')[-1].split('.')[0] for image in images]
    total_chunks = len(images) // chunk_size + 1
    
    for i in range(0, len(images), chunk_size):
        print(f"Uploading chunk {i // chunk_size + 1} of {total_chunks}")
        chunk = images[i:i + chunk_size]
        ids_chunk = ids[i:i + chunk_size]
        db.insert_by_images(ids_chunk, chunk)

def main():
    parser = argparse.ArgumentParser(description='Upload images by chunks.')
    parser.add_argument('path', help='Path to the images.')
    parser.add_argument('--chunk', type=int, default=DEFAULT_CHUNK_SIZE, help='Size of the chunk (default: %(default)s)')
    args = parser.parse_args()
    
    path = args.path
    chunk_size = args.chunk
    
    print(f"Uploading images from {path} by chunks of {chunk_size}")
    
    if existGlobItems(path):
        uploadByChunk(path, chunk_size)
    else:
        print("No files found")

if __name__ == '__main__':
    main()
