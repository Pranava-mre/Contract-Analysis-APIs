import azure.functions as func
import logging
import base64
import fitz
import json
import time

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

MAX_FILE_SIZE_MB = 10
MAX_PAGES = 200


@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    response_body = {
        "status": "ok",
        "message": "Function app is running",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    return func.HttpResponse(
        json.dumps(response_body),
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="extract-text", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def extract_text(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.time()

    try:
        try:
            body = req.get_json()
        except ValueError:
            return func.HttpResponse("Invalid JSON body", status_code=400)
        file_name = body.get("file_name")
        base64_string = body.get("file_content")

        if not file_name or not base64_string:
            return func.HttpResponse(
                "Missing file_name or file_content",
                status_code=400
            )

        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        file_size_mb = len(base64_string) * 3 / 4 / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            return func.HttpResponse(
                f"File exceeds {MAX_FILE_SIZE_MB} MB limit",
                status_code=413
            )

        pdf_bytes = base64.b64decode(base64_string)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        if len(doc) > MAX_PAGES:
            doc.close()
            return func.HttpResponse(
                f"PDF exceeds {MAX_PAGES} page limit",
                status_code=413
            )

        text_list = []
        for page in doc:
            text_list.append(page.get_text("text"))

        doc.close()

        extracted_text = "\n".join(text_list)
        elapsed_ms = int((time.time() - start_time) * 1000)

        response_body = {
            "file_name": file_name,
            "page_count": len(text_list),
            "processing_time_ms": elapsed_ms,
            "text": extracted_text
        }
        logging.info(f"Processed {file_name}, pages={len(text_list)}, time_ms={elapsed_ms}")

        return func.HttpResponse(
            json.dumps(response_body),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.exception("Error processing PDF")
        return func.HttpResponse(
            str(e),
            status_code=500
        )
