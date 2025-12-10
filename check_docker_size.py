import requests
import json

def get_docker_hub_size(repo, tag):
    print(f"Checking Docker Hub for {repo}:{tag}")
    try:
        # Get token
        auth_url = f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repo}:pull"
        token_resp = requests.get(auth_url)
        token = token_resp.json().get('token')
        
        if not token:
            print("Failed to get token")
            return

        # Get manifest
        manifest_url = f"https://registry-1.docker.io/v2/{repo}/manifests/{tag}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.docker.distribution.manifest.v2+json"
        }
        manifest_resp = requests.get(manifest_url, headers=headers)
        
        if manifest_resp.status_code != 200:
            print(f"Failed to get manifest: {manifest_resp.status_code}")
            print(manifest_resp.text)
            return

        manifest = manifest_resp.json()
        # print(json.dumps(manifest, indent=2))
        
        layers = manifest.get('layers', [])
        config = manifest.get('config', {})
        
        total_size = 0
        for layer in layers:
            total_size += layer.get('size', 0)
            
        config_size = config.get('size', 0)
        total_size += config_size
        
        print(f"Total compressed size (layers + config): {total_size} bytes")
        print(f"Total compressed size: {total_size / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"Error: {e}")

def get_ecr_public_size(repo, tag):
    print(f"Checking ECR Public for {repo}:{tag}")
    try:
        # Get token
        token_url = "https://public.ecr.aws/token/"
        token_resp = requests.get(token_url)
        token = token_resp.json().get('token')
        
        if not token:
            print("Failed to get token")
            return

        # Get manifest
        # ECR Public API is a bit different, usually registry is public.ecr.aws
        # But the manifest URL is https://public.ecr.aws/v2/<repo>/manifests/<tag>
        
        manifest_url = f"https://public.ecr.aws/v2/{repo}/manifests/{tag}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.docker.distribution.manifest.v2+json"
        }
        manifest_resp = requests.get(manifest_url, headers=headers)
        
        if manifest_resp.status_code != 200:
            print(f"Failed to get manifest: {manifest_resp.status_code}")
            print(manifest_resp.text)
            return

        manifest = manifest_resp.json()
        
        layers = manifest.get('layers', [])
        config = manifest.get('config', {})
        
        total_size = 0
        for layer in layers:
            total_size += layer.get('size', 0)
            
        config_size = config.get('size', 0)
        total_size += config_size
        
        print(f"Total compressed size (layers + config): {total_size} bytes")
        print(f"Total compressed size: {total_size / (1024*1024):.2f} MB")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_docker_hub_size("agrigorev/model-2025-hairstyle", "v1")
    # get_ecr_public_size("lambda/python", "3.13")
