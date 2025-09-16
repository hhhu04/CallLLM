import google.generativeai as genai
from typing import List, Dict, Any

class GeminiService:

    def __init__(self, key, version):
        # api_key = 'AIzaSyDKVOyY4Lds4PqNLzXedZlzI6veDORY50I'
        if key:
            genai.configure(api_key=key)
            self.model = genai.GenerativeModel(version)
            self.use_gemini = True
        else:
            self.use_gemini = False
            print("Gemini API 키가 없습니다. 기본 키워드 기반 답변을 사용합니다.")

        # 간단한 템플릿 기반 답변 시스템을 fallback으로 유지
        self.use_simple_mode = not self.use_gemini

    def generate_answer_gemini(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Gemini API를 사용한 답변 생성"""
        if not retrieved_docs:
            return "관련된 문서를 찾을 수 없어 답변을 제공할 수 없습니다."

        try:
            # 관련 문서들의 내용 결합
            context = ""
            referenced_files = set()

            for i, doc in enumerate(retrieved_docs[:5]):
                # API 응답 구조에 맞게 수정
                # doc가 직접 content와 metadata를 가지고 있는 경우
                if 'content' in doc and 'metadata' in doc:
                    filename = doc['metadata'].get('filename', f'문서_{i+1}')
                    content = doc['content']
                # doc가 다른 구조인 경우 (예: text, source 등)
                elif 'text' in doc:
                    filename = doc.get('source', doc.get('filename', f'문서_{i+1}'))
                    content = doc['text']
                # 기본 구조
                else:
                    filename = f'문서_{i+1}'
                    content = str(doc)

                context += f"\n\n[문서 {i + 1}: {filename}]\n"
                context += content
                referenced_files.add(filename)

            # Gemini에게 전달할 프롬프트 구성
            prompt = f"""다음 문서들을 참조하여 사용자의 질문에 대해 정확하고 도움이 되는 답변을 해주세요.

                    질문: {query}
                
                    참조 문서들:
                    {context}
                
                    답변 요구사항:
                    1. 질문에 직접적으로 관련된 정보를 우선적으로 활용해주세요
                    2. 한국어로 자연스럽게 답변해주세요
                    3. 구체적인 정보와 예시를 포함해주세요
                    4. 답변 끝에 참조한 문서 목록을 포함해주세요
                    5. 연관없는 문서는 목록에서 제외해주세요
                    6. 연관없는 문서는 언급하지 말아주세요
                
                    답변:"""

            response = self.model.generate_content(prompt)

            if response and response.text:
                answer = response.text.strip()

                # 참조 문서 정보 추가
                answer += f"\n\n**참조된 문서:**\n"
                for filename in sorted(referenced_files):
                    answer += f"• {filename}\n"

                return answer
            else:
                return "Gemini API 호출 오류"

        except Exception as e:
            print(f"Gemini API 호출 오류: {e}")
            # Gemini 실패 시 기본 방식으로 fallback
            return "Gemini API 호출 오류"
