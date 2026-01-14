"""
Korean Localization Processor for AWS SAA Study Materials
콘텐츠 현지화 프로세서 - 한국어 콘텐츠 생성 및 자동 한영 병기
"""

import re
from typing import Dict, List, Optional, Set
from pathlib import Path

from src.generators.korean_term_dictionary import (
    get_korean_term_dictionary,
    KoreanTermDictionary,
    TermCategory
)
from src.daily_topics import DAILY_TOPICS


class KoreanLocalizationProcessor:
    """한국어 현지화 프로세서"""
    
    def __init__(self):
        self.dictionary = get_korean_term_dictionary()
        self._processed_terms: Set[str] = set()
    
    def localize_content(self, content: str, day_number: Optional[int] = None) -> str:
        """콘텐츠 현지화 - 영어 기술 용어에 한국어 번역 자동 추가
        
        Args:
            content: 원본 콘텐츠
            day_number: 일차 번호 (선택사항, 해당 일차 관련 용어 우선 처리)
            
        Returns:
            현지화된 콘텐츠
        """
        # 처리된 용어 초기화
        self._processed_terms.clear()
        
        # 해당 일차 관련 용어 우선 처리
        if day_number:
            day_terms = self.dictionary.search_by_day(day_number)
            for term in day_terms:
                content = self._apply_bilingual_notation_for_term(content, term.english)
        
        # AWS 서비스 용어 처리
        aws_services = self.dictionary.get_all_aws_services()
        for service in aws_services:
            content = self._apply_bilingual_notation_for_term(content, service.english)
        
        # 기타 카테고리 용어 처리
        for category in [TermCategory.ARCHITECTURE, TermCategory.NETWORKING, 
                        TermCategory.SECURITY, TermCategory.DATABASE,
                        TermCategory.STORAGE, TermCategory.COMPUTE]:
            terms = self.dictionary.search_by_category(category)
            for term in terms:
                content = self._apply_bilingual_notation_for_term(content, term.english)
        
        return content
    
    def _apply_bilingual_notation_for_term(self, content: str, english_term: str) -> str:
        """특정 용어에 대해 한영 병기 적용
        
        Args:
            content: 콘텐츠
            english_term: 영어 용어
            
        Returns:
            한영 병기가 적용된 콘텐츠
        """
        # 이미 처리된 용어는 스킵
        if english_term in self._processed_terms:
            return content
        
        term = self.dictionary.get_term(english_term)
        if not term:
            return content
        
        # 한영 병기 표기 생성
        bilingual = self.dictionary.get_bilingual_notation(english_term)
        
        # 이미 한영 병기가 있는 경우 스킵
        if bilingual in content:
            self._processed_terms.add(english_term)
            return content
        
        # 영어 용어만 있는 경우 한영 병기로 교체
        # 단어 경계를 고려하여 정확한 매칭
        pattern = r'\b' + re.escape(english_term) + r'\b'
        
        # 첫 번째 발견된 용어만 교체 (문서 내 첫 등장 시에만 병기)
        content = re.sub(pattern, bilingual, content, count=1)
        
        self._processed_terms.add(english_term)
        return content
    
    def apply_bilingual_notation(self, text: str) -> str:
        """텍스트에 자동으로 한영 병기 적용
        
        Args:
            text: 원본 텍스트
            
        Returns:
            한영 병기가 적용된 텍스트
        """
        return self.localize_content(text)
    
    def validate_term_consistency(self, content: str) -> List[Dict[str, str]]:
        """콘텐츠 내 용어 일관성 검증
        
        Args:
            content: 검증할 콘텐츠
            
        Returns:
            불일치 항목 리스트 [{"term": "...", "issue": "...", "suggestion": "..."}, ...]
        """
        issues = []
        
        # 용어 사전의 모든 영어 용어 확인
        for english_key, term in self.dictionary.terms.items():
            if english_key == term.english.lower():
                # 영어 용어가 콘텐츠에 있는지 확인
                if term.english in content:
                    bilingual = self.dictionary.get_bilingual_notation(term.english)
                    
                    # 한영 병기가 없는 경우
                    if bilingual not in content and term.korean not in content:
                        issues.append({
                            "term": term.english,
                            "issue": "한국어 번역 누락",
                            "suggestion": f"'{term.english}'를 '{bilingual}'로 변경"
                        })
                    
                    # 한국어만 있고 영어가 없는 경우
                    elif term.korean in content and f"({term.english})" not in content:
                        # 첫 등장 시에는 병기 필요
                        first_occurrence = content.find(term.korean)
                        if first_occurrence != -1:
                            # 괄호 안에 영어가 있는지 확인
                            next_paren = content.find("(", first_occurrence)
                            if next_paren == -1 or next_paren > first_occurrence + len(term.korean) + 5:
                                issues.append({
                                    "term": term.korean,
                                    "issue": "영어 원문 누락",
                                    "suggestion": f"'{term.korean}'를 '{bilingual}'로 변경"
                                })
        
        return issues
    
    def get_localized_template_vars(self, day_number: int) -> Dict[str, str]:
        """일차별 현지화된 템플릿 변수 생성
        
        Args:
            day_number: 일차 번호 (1-28)
            
        Returns:
            현지화된 템플릿 변수 딕셔너리
        """
        if day_number not in DAILY_TOPICS:
            raise ValueError(f"Invalid day number: {day_number}")
        
        config = DAILY_TOPICS[day_number]
        localized_vars = {}
        
        # 주요 서비스 현지화
        primary_services = config["primary_services"]
        localized_services = []
        for service in primary_services:
            term = self.dictionary.get_term(service)
            if term:
                localized_services.append(self.dictionary.get_bilingual_notation(service))
            else:
                localized_services.append(service)
        
        localized_vars["primary_services_localized"] = ", ".join(localized_services)
        localized_vars["primary_service_localized"] = localized_services[0] if localized_services else ""
        
        # 제목 현지화 (이미 한국어인 경우 그대로 사용)
        localized_vars["title_localized"] = config["title"]
        
        # 사례 연구 초점 현지화
        localized_vars["case_study_focus_localized"] = config["case_study_focus"]
        
        # 난이도 현지화
        difficulty_map = {
            "basic": "기초",
            "intermediate": "중급",
            "advanced": "고급"
        }
        localized_vars["difficulty_localized"] = difficulty_map.get(config["difficulty"], config["difficulty"])
        
        return localized_vars
    
    def localize_aws_service_name(self, service_name: str) -> str:
        """AWS 서비스명 현지화
        
        Args:
            service_name: AWS 서비스 영어명
            
        Returns:
            한영 병기 서비스명
        """
        return self.dictionary.get_bilingual_notation(service_name)
    
    def get_korean_only(self, english_term: str) -> str:
        """영어 용어의 한국어 번역만 반환
        
        Args:
            english_term: 영어 용어
            
        Returns:
            한국어 번역
        """
        return self.dictionary.get_korean_term(english_term)
    
    def get_english_only(self, korean_term: str) -> str:
        """한국어 용어의 영어 원문만 반환
        
        Args:
            korean_term: 한국어 용어
            
        Returns:
            영어 원문
        """
        return self.dictionary.get_english_term(korean_term)
    
    def generate_glossary_section(self, day_number: Optional[int] = None) -> str:
        """용어집 섹션 생성
        
        Args:
            day_number: 일차 번호 (선택사항, 해당 일차 관련 용어만 포함)
            
        Returns:
            마크다운 형식의 용어집 섹션
        """
        glossary = ["## 📚 용어집\n"]
        
        if day_number:
            terms = self.dictionary.search_by_day(day_number)
            glossary.append(f"### Day {day_number} 관련 용어\n")
        else:
            terms = list(set(self.dictionary.terms.values()))
            glossary.append("### 전체 용어\n")
        
        # 카테고리별로 그룹화
        terms_by_category = {}
        for term in terms:
            if term.category not in terms_by_category:
                terms_by_category[term.category] = []
            terms_by_category[term.category].append(term)
        
        # 카테고리별로 출력
        category_names = {
            TermCategory.AWS_SERVICE: "AWS 서비스",
            TermCategory.ARCHITECTURE: "아키텍처",
            TermCategory.NETWORKING: "네트워킹",
            TermCategory.SECURITY: "보안",
            TermCategory.DATABASE: "데이터베이스",
            TermCategory.STORAGE: "스토리지",
            TermCategory.COMPUTE: "컴퓨팅",
            TermCategory.MONITORING: "모니터링",
            TermCategory.GENERAL: "일반"
        }
        
        for category, category_terms in sorted(terms_by_category.items(), key=lambda x: x[0].value):
            glossary.append(f"\n#### {category_names[category]}\n")
            for term in sorted(category_terms, key=lambda t: t.korean):
                if term.abbreviation:
                    glossary.append(f"- **{term.korean}** ({term.english}, {term.abbreviation})")
                else:
                    glossary.append(f"- **{term.korean}** ({term.english})")
                if term.description:
                    glossary.append(f"  - {term.description}")
                glossary.append("")
        
        return "\n".join(glossary)
    
    def create_localization_report(self, content: str, day_number: Optional[int] = None) -> Dict:
        """현지화 보고서 생성
        
        Args:
            content: 분석할 콘텐츠
            day_number: 일차 번호 (선택사항)
            
        Returns:
            현지화 통계 및 이슈 보고서
        """
        report = {
            "day_number": day_number,
            "total_terms_in_dictionary": len(set(self.dictionary.terms.values())),
            "terms_found_in_content": 0,
            "terms_with_bilingual_notation": 0,
            "terms_without_bilingual_notation": 0,
            "consistency_issues": [],
            "recommendations": []
        }
        
        # 콘텐츠에서 발견된 용어 카운트
        found_terms = []
        for english_key, term in self.dictionary.terms.items():
            if english_key == term.english.lower():
                if term.english in content or term.korean in content:
                    found_terms.append(term)
                    report["terms_found_in_content"] += 1
                    
                    # 한영 병기 여부 확인
                    bilingual = self.dictionary.get_bilingual_notation(term.english)
                    if bilingual in content:
                        report["terms_with_bilingual_notation"] += 1
                    else:
                        report["terms_without_bilingual_notation"] += 1
        
        # 일관성 이슈 확인
        report["consistency_issues"] = self.validate_term_consistency(content)
        
        # 권장사항 생성
        if report["terms_without_bilingual_notation"] > 0:
            report["recommendations"].append(
                f"{report['terms_without_bilingual_notation']}개의 용어에 한영 병기가 필요합니다."
            )
        
        if len(report["consistency_issues"]) > 0:
            report["recommendations"].append(
                f"{len(report['consistency_issues'])}개의 용어 일관성 이슈가 발견되었습니다."
            )
        
        if report["terms_found_in_content"] == 0:
            report["recommendations"].append(
                "콘텐츠에서 용어 사전의 용어가 발견되지 않았습니다. 콘텐츠를 검토해주세요."
            )
        
        return report


# 전역 인스턴스 (싱글톤 패턴)
_processor_instance = None


def get_korean_localization_processor() -> KoreanLocalizationProcessor:
    """한국어 현지화 프로세서 싱글톤 인스턴스 반환"""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = KoreanLocalizationProcessor()
    return _processor_instance


# CLI 실행을 위한 메인 함수
def main():
    """CLI 실행 - 콘텐츠 현지화 테스트"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Korean Localization Processor for AWS SAA")
    parser.add_argument("--file", type=str, help="File to localize")
    parser.add_argument("--day", type=int, help="Day number (1-28) for context-aware localization")
    parser.add_argument("--validate", action="store_true", help="Validate term consistency")
    parser.add_argument("--report", action="store_true", help="Generate localization report")
    parser.add_argument("--glossary", action="store_true", help="Generate glossary section")
    parser.add_argument("--output", type=str, help="Output file path")
    
    args = parser.parse_args()
    
    processor = get_korean_localization_processor()
    
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"파일을 찾을 수 없습니다: {args.file}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if args.validate:
            # 용어 일관성 검증
            issues = processor.validate_term_consistency(content)
            print(f"\n용어 일관성 검증 결과: {len(issues)}개 이슈 발견\n")
            for issue in issues:
                print(f"  용어: {issue['term']}")
                print(f"  문제: {issue['issue']}")
                print(f"  제안: {issue['suggestion']}\n")
        
        elif args.report:
            # 현지화 보고서 생성
            report = processor.create_localization_report(content, args.day)
            print("\n현지화 보고서:")
            print(f"  일차: {report['day_number']}")
            print(f"  사전 총 용어 수: {report['total_terms_in_dictionary']}")
            print(f"  콘텐츠에서 발견된 용어: {report['terms_found_in_content']}")
            print(f"  한영 병기 적용된 용어: {report['terms_with_bilingual_notation']}")
            print(f"  한영 병기 미적용 용어: {report['terms_without_bilingual_notation']}")
            print(f"  일관성 이슈: {len(report['consistency_issues'])}")
            print("\n권장사항:")
            for rec in report['recommendations']:
                print(f"  - {rec}")
        
        else:
            # 콘텐츠 현지화
            localized = processor.localize_content(content, args.day)
            
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(localized)
                print(f"현지화된 콘텐츠가 저장되었습니다: {args.output}")
            else:
                print("\n현지화된 콘텐츠:")
                print(localized)
    
    elif args.glossary:
        # 용어집 생성
        glossary = processor.generate_glossary_section(args.day)
        
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(glossary)
            print(f"용어집이 저장되었습니다: {args.output}")
        else:
            print(glossary)
    
    else:
        print("사용법: python korean_localization_processor.py --file FILE [OPTIONS]")
        print("\n옵션:")
        print("  --file FILE         현지화할 파일")
        print("  --day DAY           일차 번호 (1-28)")
        print("  --validate          용어 일관성 검증")
        print("  --report            현지화 보고서 생성")
        print("  --glossary          용어집 생성")
        print("  --output FILE       출력 파일 경로")
        print("\n예시:")
        print("  python korean_localization_processor.py --file case-study.md --day 1")
        print("  python korean_localization_processor.py --file case-study.md --validate")
        print("  python korean_localization_processor.py --glossary --day 1 --output glossary.md")


if __name__ == "__main__":
    main()
