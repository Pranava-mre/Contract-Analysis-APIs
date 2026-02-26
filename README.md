# Fence contract APIs

HTTP-triggered Azure Function to extract text from a base64-encoded PDF.

## Endpoint
- Route: `POST /api/extract-text`
- Auth level: `FUNCTION` (requires function key in Azure)

## Request body
```json
{
  "file_name": "sample.pdf",
  "file_content": "<base64-pdf-content>"
}
```

## Local development
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy settings template:
   - `local.settings.json.example` -> `local.settings.json`
4. Run Azure Functions host:
   ```bash
   func start
   ```

## Deploy to Azure Functions (later)
1. Create a Function App in Azure (Python runtime).
2. Ensure app settings include:
   - `FUNCTIONS_WORKER_RUNTIME=python`
   - `AzureWebJobsStorage=<your-storage-connection-string>`
3. Deploy from local project root:
   ```bash
   func azure functionapp publish <your-function-app-name>
   ```

## GitHub checklist
- Keep `local.settings.json` out of Git (already ignored).
- Commit: `function_app.py`, `requirements.txt`, `host.json`, `README.md`, `.funcignore`, `.gitignore`.
- Do not commit `.venv/`.
