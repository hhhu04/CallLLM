import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from client import APIClient
from llm import GeminiService

# .env 파일 로드
load_dotenv()

app = FastAPI()


@app.get("/gemini")
async def gemini(query: str, index_name:str, path:str):
    client = APIClient(base_url=os.getenv("SEARCH_API_BASE_URL", "http://localhost:8000"))
    uri = '/search?file_path='+path+'&index_name='+index_name+'&query='+query

    print(uri)

    result = await client.get(uri)

    gemini_service = GeminiService(
        key=os.getenv("GEMINI_API_KEY"),
        version=os.getenv("GEMINI_MODEL_VERSION", "gemini-1.5-flash")
    )

    # result가 딕셔너리인 경우 리스트로 변환
    # API 응답이 {"results": [...]} 형태라면 result.get("results", [])를 사용
    if isinstance(result, dict):
        # 만약 result에 'results' 키가 있다면
        if "results" in result:
            retrieved_docs = result["results"]
        # 아니면 단일 결과를 리스트로 감싸기
        else:
            retrieved_docs = [result]
    elif isinstance(result, list):
        retrieved_docs = result
    else:
        retrieved_docs = []

    answer = gemini_service.generate_answer_gemini(query, retrieved_docs)

    print(answer)

    return {"message": answer}


@app.get("/call-external-api")
async def call_external_api():
    try:
        # Example: Call another API server
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        result = await client.get("/posts/1")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
