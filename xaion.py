import httpx
from typing import List, Dict, Any, Optional


class ExaoneService:
    def __init__(self, base_url: str = "http://localhost:8080", timeout: int = 30):
        """
        EXAONE 로컬 서버 연결을 위한 서비스

        Args:
            base_url: EXAONE 로컬 서버 URL (기본값: http://localhost:8080)
            timeout: 요청 타임아웃 (초)
        """
        self.base_url = base_url
        self.timeout = timeout

    async def generate_answer_exaone(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """EXAONE API를 사용한 답변 생성"""
        if not retrieved_docs:
            return "관련된 문서를 찾을 수 없어 답변을 제공할 수 없습니다."

        try:
            # 관련 문서들의 내용 결합
            context = ""
            referenced_files = set()

            for i, doc in enumerate(retrieved_docs[:5]):
                # API 응답 구조에 맞게 수정
                if 'content' in doc and 'metadata' in doc:
                    filename = doc['metadata'].get('filename', f'문서_{i+1}')
                    content = doc['content']
                elif 'text' in doc:
                    filename = doc.get('source', doc.get('filename', f'문서_{i+1}'))
                    content = doc['text']
                else:
                    filename = f'문서_{i+1}'
                    content = str(doc)

                context += f"\n\n[{filename}]\n"
                context += content
                referenced_files.add(filename)

            # EXAONE에게 전달할 프롬프트 구성
            prompt = f"""다음 문서들을 참조하여 사용자의 질문에 대해 정확하고 도움이 되는 답변을 해주세요.

            질문: {query}

            참조 문서들:
            {context}

            답변 요구사항:
            1. 질문에 직접적으로 관련된 정보를 우선적으로 활용해주세요
            2. 한국어로 자연스럽게 답변해주세요
            3. 구체적인 정보와 예시를 포함해주세요
            4. 답변에서 문서를 언급할 때는 실제 파일명을 사용해주세요 (예: "sample.txt에 따르면...")
            5. 답변 끝에 참조한 문서 목록을 실제 파일명으로 포함해주세요
            6. 연관없는 문서는 목록에서 제외해주세요
            7. 연관없는 문서는 언급하지 말아주세요

            답변:"""

            # EXAONE 로컬 서버에 요청
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={
                        "prompt": prompt,
                        "max_tokens": 1000,
                        "temperature": 0.7,
                        "top_p": 0.9
                    },
                    timeout=self.timeout
                )

                response.raise_for_status()
                result = response.json()

                if 'text' in result:
                    answer = result['text'].strip()
                elif 'response' in result:
                    answer = result['response'].strip()
                else:
                    answer = str(result)

                return answer

        except httpx.RequestError as e:
            print(f"EXAONE 서버 연결 오류: {e}")
            return "EXAONE 서버에 연결할 수 없습니다."
        except httpx.HTTPStatusError as e:
            print(f"EXAONE API 호출 오류: {e}")
            return "EXAONE API 호출 중 오류가 발생했습니다."
        except Exception as e:
            print(f"EXAONE 처리 오류: {e}")
            return "EXAONE 처리 중 오류가 발생했습니다."

    async def check_health(self) -> bool:
        """EXAONE 서버 상태 확인"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/health",
                    timeout=5
                )
                return response.status_code == 200
        except:
            return False