from huggingface_hub import snapshot_download

model_dir = snapshot_download("Qwen/Qwen3-Embedding-0.6B", cache_dir="./", revision="master")