from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/check")
def check_grammar(request: Request, user_text: str = Form(...)):
    response = requests.post(
        "https://api.languagetool.org/v2/check",
        data={"text": user_text, "language": "en-US"}
    )
    result = response.json()

    corrected_text = user_text
    for match in reversed(result["matches"]):
        if match["replacements"]:
            start = match["offset"]
            end = start + match["length"]
            replacement = match["replacements"][0]["value"]
            corrected_text = corrected_text[:start] + replacement + corrected_text[end:]

    return templates.TemplateResponse(request, "index.html", {
        "original": user_text,
        "corrected": corrected_text
    })