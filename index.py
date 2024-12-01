import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv
import re

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepositoryRequest(BaseModel):
    url: str

    @field_validator('url')
    @classmethod
    def validate_github_url(cls, v):
        github_url_pattern = r'^https?://github\.com/[\w-]+/[\w.-]+/?$'
        if not re.match(github_url_pattern, v):
            raise HTTPException(status_code=400, detail=f"Invalid GitHub repository URL")
        return v

def fetch_github_contents(owner, repo, path='', tree=None):
    if tree is None:
        tree = {'name': repo, 'type': 'dir', 'children': []}
    
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'

    github_token = os.getenv('GITHUB_TOKEN')
    
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
        
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        contents = response.json()
        
        for item in contents:
            node = {
                'name': item['name'],
                'type': item['type'],
                'path': item['path']
            }
            
            if item['type'] == 'dir':
                node['children'] = []
                # Recursively fetch subdirectory contents
                fetch_github_contents(owner, repo, item['path'], node)
                tree['children'].append(node)
            else:
                tree['children'].append(node)
        
        return tree
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching repository: {str(e)}")

@app.post("/fetch-repo-tree")
def get_repository_tree(request: RepositoryRequest):
    parts = request.url.strip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    
    try:
        tree = fetch_github_contents(owner, repo)
        return tree
    except HTTPException as e:
        raise e

# For running the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)