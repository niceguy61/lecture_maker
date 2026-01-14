"""
Best Practices Generator for AWS SAA Study Materials
각 일별 best-practices.md 파일 생성
"""

from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.models import (
    BestPracticesContent,
    IntegrationPattern,
    EvolutionPath,
    CostOptimizationStrategy,
    SecurityBestPractice,
    OperationalPractice
)
from src.daily_topics import DAILY_TOPICS
from src.config import (
    TEMPLATES_ROOT,
    STUDY_MATERIALS_ROOT,
    DEFAULT_AWS_REGION,
    AWS_DOCS_BASE_URL,
    AWS_PRICING_BASE_URL,
    AWS_ARCHITECTURE_CENTER_URL
)
from src.generators.korean_localization_processor import get_korean_localization_processor


class BestPracticesGenerator:
    """베스트 프랙티스 문서 생성기"""
    
    def __init__(self, template_path: Optional[Path] = None, output_base_path: Optional[Path] = None):
        """
        Args:
            template_path: 템플릿 파일 경로 (기본값: templates/best-practices-template.md)
            output_base_path: 출력 기본 경로 (기본값: aws-saa-study-materials)
        """
        self.template_path = template_path or TEMPLATES_ROOT / "best-practices-template.md"
        self.output_base_path = output_base_path or STUDY_MATERIALS_ROOT
        self.template_content = self.load_template()
        self.localization_processor = get_korean_localization_processor()
    
    def load_template(self) -> str:
        """템플릿 파일 로드"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_daily_config(self, day_number: int) -> Dict:
        """일별 설정 가져오기"""
        if day_number not in DAILY_TOPICS:
            raise ValueError(f"Day {day_number} not found in DAILY_TOPICS")
        
        return DAILY_TOPICS[day_number]
    
    def generate_integration_patterns(self, day_number: int, config: Dict) -> str:
        """서비스 연계 패턴 생성"""
        patterns = []
        related_days = config.get("related_days", [])
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # 각 관련 일차에 대한 통합 패턴 생성
        for i, related_day in enumerate(related_days[:3], 1):  # 최대 3개 패턴
            if related_day in DAILY_TOPICS:
                related_config = DAILY_TOPICS[related_day]
                related_service = related_config["primary_services"][0] if related_config["primary_services"] else "AWS Service"
                
                pattern = f"""### 패턴 {i}: {primary_service} + {related_service} (Day {related_day} 연계)

**사용 사례**:
- {primary_service}와 {related_service}를 함께 사용하여 {self._get_integration_use_case(primary_service, related_service)}
- 실제 프로덕션 환경에서 자주 사용되는 통합 패턴
- {self._get_integration_benefit(primary_service, related_service)}

**구현 방법** (AWS Console 기반):

1. **{primary_service} 설정**
   - Console 경로: Services > {self._get_service_category(primary_service)} > {primary_service}
   - 주요 설정: {self._get_primary_config(primary_service)}

2. **{related_service} 통합**
   - Console 경로: Services > {self._get_service_category(related_service)} > {related_service}
   - 연결 설정: {self._get_integration_config(primary_service, related_service)}

3. **통합 검증**
   - 테스트 방법: {self._get_test_method(primary_service, related_service)}
   - 예상 결과: 정상적인 데이터 흐름 및 서비스 간 통신 확인

**장단점**:

✅ **장점**:
- 성능: {self._get_performance_benefit(primary_service, related_service)}
- 비용: {self._get_cost_benefit(primary_service, related_service)}
- 관리 용이성: AWS 관리형 서비스로 운영 부담 감소

⚠️ **단점**:
- 복잡성: 서비스 간 의존성 증가
- 제약사항: {self._get_constraints(primary_service, related_service)}
- 비용: 추가 서비스 사용에 따른 비용 발생

🔄 **대안**:
- 대안 1: {self._get_alternative_1(primary_service, related_service)}
- 대안 2: {self._get_alternative_2(primary_service, related_service)}

**실제 사례**:
- {self._get_real_world_example(primary_service, related_service)}
"""
                patterns.append(pattern)
        
        if not patterns:
            # 관련 일차가 없는 경우 기본 패턴
            patterns.append(f"""### 패턴 1: {primary_service} 단독 사용

**사용 사례**:
- {primary_service}를 독립적으로 사용하는 기본 구성
- 학습 및 프로토타입 단계에 적합
- 간단한 워크로드 처리

**구현 방법** (AWS Console 기반):

1. **{primary_service} 기본 설정**
   - Console 경로: Services > {self._get_service_category(primary_service)} > {primary_service}
   - 기본 구성으로 시작하여 점진적으로 확장

**장단점**:

✅ **장점**:
- 단순성: 빠른 구현 및 이해
- 비용: 최소한의 리소스 사용
- 학습: 서비스 핵심 기능 집중 학습

⚠️ **단점**:
- 제한적 기능: 고급 기능 활용 제한
- 확장성: 추가 서비스 통합 필요 시 재구성 필요
""")
        
        return "\n".join(patterns)

    
    def generate_evolution_paths(self, day_number: int, config: Dict) -> Dict[str, str]:
        """아키텍처 진화 경로 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        related_days = config.get("related_days", [])
        
        # Stage 1: 기본 구성
        stage1_diagram = self._generate_basic_architecture_diagram(primary_service)
        stage1_features = f"""- 단순한 구조로 빠른 구현 가능
- {primary_service}의 핵심 기능 활용
- 제한적인 확장성 (소규모 워크로드 적합)
- 최소한의 운영 복잡도"""
        
        stage1_use_cases = f"""- 프로토타입 및 개념 검증 (PoC) 단계
- 소규모 트래픽 (일 방문자 < 1,000명)
- 학습 및 실습 목적
- 빠른 시장 출시가 필요한 MVP"""
        
        # Stage 2: 서비스 추가
        stage2_days = ", ".join([f"Day {d}" for d in related_days[:2]]) if related_days else "추가 서비스"
        stage2_services = self._generate_stage2_services(primary_service, related_days)
        stage2_diagram = self._generate_integrated_architecture_diagram(primary_service, related_days)
        stage2_improvements = f"""- **성능**: 캐싱 및 로드 밸런싱으로 응답 시간 50% 개선
- **확장성**: 자동 스케일링으로 트래픽 변동 대응
- **안정성**: 다중 AZ 구성으로 가용성 99.9% 이상 달성
- **보안**: IAM 및 네트워크 격리로 보안 강화"""
        
        # Stage 3: 최적화
        stage3_diagram = self._generate_optimized_architecture_diagram(primary_service, related_days)
        stage3_optimizations = f"""- **비용 최적화**: 예약 인스턴스 및 스팟 인스턴스 활용으로 30-50% 비용 절감
- **성능 최적화**: CloudFront CDN 및 데이터베이스 읽기 복제본으로 글로벌 성능 향상
- **보안 강화**: WAF, Shield, GuardDuty 등 고급 보안 서비스 통합
- **운영 자동화**: CloudFormation/Terraform IaC 및 CI/CD 파이프라인 구축
- **모니터링 고도화**: 상세 메트릭, 로그 분석, 자동 알람 및 대응"""
        
        return {
            "evolution_stage1_diagram": stage1_diagram,
            "evolution_stage1_features": stage1_features,
            "evolution_stage1_use_cases": stage1_use_cases,
            "evolution_stage2_days": stage2_days,
            "evolution_stage2_services": stage2_services,
            "evolution_stage2_diagram": stage2_diagram,
            "evolution_stage2_improvements": stage2_improvements,
            "evolution_stage3_diagram": stage3_diagram,
            "evolution_stage3_optimizations": stage3_optimizations
        }
    
    def generate_cost_optimization(self, day_number: int, config: Dict) -> Dict[str, str]:
        """비용 최적화 전략 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # 현재 상태 분석
        current_analysis = f"""- **CloudWatch 메트릭 확인**: {primary_service} 리소스 사용률 모니터링
- **사용률 분석**: CPU, 메모리, 네트워크, 스토리지 사용 패턴 파악
- **낭비 요소 식별**: 과도하게 프로비저닝된 리소스, 미사용 리소스 발견
- **Cost Explorer 활용**: 서비스별, 태그별 비용 분석"""
        
        # 최적화 방법
        optimization_methods = self._generate_cost_optimization_methods(primary_service)
        
        # 예약 인스턴스 (해당되는 경우)
        reserved_strategy = self._generate_reserved_instances_strategy(primary_service)
        
        # 스팟 인스턴스 (해당되는 경우)
        spot_strategy = self._generate_spot_instances_strategy(primary_service)
        
        # 데이터 전송 최적화
        data_transfer = f"""- **리전 간 전송 최소화**: 동일 리전 내 리소스 배치로 데이터 전송 비용 절감
- **CloudFront 활용**: 정적 콘텐츠 캐싱으로 오리진 서버 부하 및 전송 비용 감소
- **VPC 엔드포인트 사용**: S3, DynamoDB 등 AWS 서비스 접근 시 인터넷 게이트웨이 우회
- **압축 활용**: 데이터 압축으로 전송량 감소"""
        
        return {
            "cost_current_analysis": current_analysis,
            "cost_optimization_methods": optimization_methods,
            "reserved_instances_strategy": reserved_strategy,
            "spot_instances_strategy": spot_strategy,
            "data_transfer_optimization": data_transfer
        }
    
    def generate_security_practices(self, day_number: int, config: Dict) -> Dict[str, str]:
        """보안 베스트 프랙티스 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # IAM 구현
        iam_implementation = f"""1. **{primary_service} 전용 역할 생성**
   - Console 경로: IAM > Roles > Create role
   - 신뢰 관계: {primary_service} 서비스
   - 정책: 필요한 최소 권한만 부여
   
2. **정기적 권한 검토**
   - IAM Access Analyzer 활용: 외부 액세스 검토
   - 불필요한 권한 제거: 90일 이상 미사용 권한 삭제
   - 권한 경계 설정: 최대 권한 제한"""
        
        # Security Group 설정
        security_group = f"""- **Console 경로**: VPC > Security Groups > Create security group
- **인바운드 규칙**: 필요한 포트만 최소한으로 개방
  - 예: HTTPS (443), SSH (22, 특정 IP만)
  - 소스: 신뢰할 수 있는 IP 범위 또는 Security Group
- **아웃바운드 규칙**: 필요한 대상만 허용
  - 기본 "모두 허용" 대신 특정 서비스/포트만 개방
- **명명 규칙**: `day{day_number}-{primary_service.lower()}-sg`"""
        
        # Network ACL
        network_acl = f"""- **서브넷 레벨 보안**: Security Group의 추가 방어 계층
- **Stateless 규칙**: 인바운드/아웃바운드 각각 명시적 허용 필요
- **번호 기반 우선순위**: 낮은 번호가 먼저 평가됨
- **사용 시나리오**: 특정 IP 범위 차단, 규정 준수 요구사항"""
        
        # 암호화
        encryption_transit = f"""- **HTTPS/TLS 사용**: 모든 데이터 전송에 암호화 적용
- **Certificate Manager 활용**: SSL/TLS 인증서 자동 관리 및 갱신
- **최신 프로토콜**: TLS 1.2 이상 사용, 구버전 프로토콜 비활성화"""
        
        encryption_rest = f"""- **Console에서 암호화 활성화**: {primary_service} 생성 시 암호화 옵션 선택
- **KMS 키 관리**: 
  - AWS 관리형 키 (기본): 간편한 관리
  - 고객 관리형 키: 세밀한 제어 및 감사
- **키 로테이션 정책**: 자동 연간 키 로테이션 활성화"""
        
        # 로깅
        cloudtrail = f"""- **Console 경로**: CloudTrail > Trails > Create trail
- **모든 리전 활성화**: 전체 계정 활동 추적
- **S3 버킷 로그 저장**: 장기 보관 및 분석
- **로그 파일 검증**: 무결성 확인 활성화
- **CloudWatch Logs 통합**: 실시간 모니터링 및 알람"""
        
        cloudwatch_logs = f"""- **서비스별 로그 그룹**: `/aws/{primary_service.lower()}/...`
- **로그 보관 기간 설정**: 규정 준수 요구사항에 따라 설정 (예: 90일, 1년)
- **로그 분석 쿼리**: CloudWatch Logs Insights로 패턴 분석
- **메트릭 필터**: 특정 로그 패턴 발생 시 알람 생성"""
        
        return {
            "iam_implementation": iam_implementation,
            "security_group_config": security_group,
            "network_acl_config": network_acl,
            "encryption_in_transit": encryption_transit,
            "encryption_at_rest": encryption_rest,
            "cloudtrail_config": cloudtrail,
            "cloudwatch_logs_config": cloudwatch_logs
        }

    
    def generate_operational_practices(self, day_number: int, config: Dict) -> Dict[str, str]:
        """운영 우수성 프랙티스 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # 자동화
        automation = f"""- **Infrastructure as Code (IaC)**: 
  - CloudFormation 템플릿으로 {primary_service} 리소스 정의
  - 버전 관리 및 재현 가능한 배포
  - 환경별 파라미터 관리 (dev, staging, prod)
  
- **배포 자동화**:
  - AWS CodePipeline으로 CI/CD 파이프라인 구축
  - 자동 테스트 및 승인 프로세스
  - 롤백 전략 수립
  
- **백업 자동화**:
  - AWS Backup으로 중앙 집중식 백업 관리
  - 백업 일정 및 보관 정책 설정
  - 정기적 복구 테스트"""
        
        # 모니터링
        monitoring = f"""- **핵심 메트릭 정의**:
  - {primary_service} 성능 지표 (응답 시간, 처리량, 오류율)
  - 리소스 사용률 (CPU, 메모리, 디스크, 네트워크)
  - 비즈니스 메트릭 (사용자 수, 트랜잭션 수)
  
- **알람 임계값 설정**:
  - 경고 (Warning): 80% 사용률
  - 위험 (Critical): 90% 사용률
  - 복합 알람: 여러 조건 조합
  
- **대시보드 구성**:
  - CloudWatch 대시보드로 실시간 모니터링
  - 서비스 상태 한눈에 파악
  - 팀 공유 및 협업"""
        
        # 문서화
        documentation = f"""- **아키텍처 문서**:
  - 현재 아키텍처 다이어그램 (Mermaid, draw.io)
  - 서비스 간 의존성 및 데이터 플로우
  - 정기적 업데이트 (변경 시마다)
  
- **운영 절차서 (Runbook)**:
  - 일상 운영 작업 (배포, 백업, 모니터링)
  - 장애 대응 절차
  - 에스컬레이션 경로
  
- **트러블슈팅 가이드**:
  - 일반적인 문제 및 해결 방법
  - 로그 분석 방법
  - AWS Support 활용 가이드"""
        
        return {
            "automation_practices": automation,
            "monitoring_practices": monitoring,
            "documentation_practices": documentation
        }
    
    def generate_related_days_content(self, day_number: int, config: Dict) -> str:
        """관련 학습 내용 생성"""
        related_days = config.get("related_days", [])
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        content_parts = []
        
        # 이전 학습 내용
        previous_days = [d for d in related_days if d < day_number]
        if previous_days:
            for prev_day in previous_days[:2]:
                if prev_day in DAILY_TOPICS:
                    prev_config = DAILY_TOPICS[prev_day]
                    prev_service = prev_config["primary_services"][0] if prev_config["primary_services"] else "AWS Service"
                    content_parts.append(
                        f"- **Day {prev_day}: {prev_service}** - {self._get_integration_description(prev_service, primary_service)}"
                    )
        
        # 현재 일차
        content_parts.append(f"- **Day {day_number}: {primary_service}** (현재 학습 중)")
        
        # 향후 학습 내용
        future_days = [d for d in related_days if d > day_number]
        if future_days:
            for future_day in future_days[:2]:
                if future_day in DAILY_TOPICS:
                    future_config = DAILY_TOPICS[future_day]
                    future_service = future_config["primary_services"][0] if future_config["primary_services"] else "AWS Service"
                    content_parts.append(
                        f"- **Day {future_day}: {future_service}** - {self._get_future_integration(primary_service, future_service)}"
                    )
        
        # 관련 문서 링크
        content_parts.extend([
            "",
            "### 관련 문서",
            "- [case-study.md](./case-study.md) - 실제 기업의 적용 사례",
            "- [hands-on-console/README.md](./hands-on-console/README.md) - 실습 가이드",
            "- [troubleshooting.md](./troubleshooting.md) - 문제 해결 방법"
        ])
        
        return "\n".join(content_parts)
    
    def generate_reference_links(self, day_number: int, config: Dict) -> Dict[str, str]:
        """참고 자료 링크 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        service_slug = primary_service.lower().replace(" ", "-")
        
        # AWS 공식 문서
        aws_docs = f"""- [{primary_service} 사용 설명서]({AWS_DOCS_BASE_URL}/ko_kr/{service_slug}/)
- [{primary_service} API 레퍼런스]({AWS_DOCS_BASE_URL}/ko_kr/{service_slug}/latest/APIReference/)
- [AWS Well-Architected Framework]({AWS_ARCHITECTURE_CENTER_URL}/well-architected/)"""
        
        # 아키텍처 및 베스트 프랙티스
        architecture = f"""- [AWS 아키텍처 센터]({AWS_ARCHITECTURE_CENTER_URL}/)
- [{primary_service} 베스트 프랙티스]({AWS_DOCS_BASE_URL}/ko_kr/{service_slug}/latest/userguide/best-practices.html)
- [보안 베스트 프랙티스]({AWS_DOCS_BASE_URL}/ko_kr/security/)"""
        
        # 비용 최적화
        cost_optimization = f"""- [AWS 요금 계산기](https://calculator.aws/)
- [{primary_service} 요금 안내]({AWS_PRICING_BASE_URL}/{service_slug}/)
- [비용 최적화 가이드]({AWS_DOCS_BASE_URL}/ko_kr/cost-management/)"""
        
        return {
            "aws_docs_links": aws_docs,
            "architecture_links": architecture,
            "cost_optimization_links": cost_optimization
        }
    
    def generate_summary_sections(self, day_number: int, config: Dict) -> Dict[str, str]:
        """핵심 요약 섹션 생성"""
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        related_days = config.get("related_days", [])
        
        # 통합 패턴 요약
        integration_summary = f"""1. **{primary_service} 단독 사용**: 기본 구성 및 학습
2. **다른 서비스와 통합**: {', '.join([f'Day {d}' for d in related_days[:3]])} 서비스 연계
3. **고급 통합 패턴**: 멀티 서비스 아키텍처 구성"""
        
        # 비용 최적화 체크리스트
        cost_checklist = f"""- [ ] CloudWatch 메트릭으로 리소스 사용률 분석
- [ ] 과도하게 프로비저닝된 리소스 식별 및 조정
- [ ] 예약 인스턴스/Savings Plans 검토 (해당 시)
- [ ] 스팟 인스턴스 활용 가능성 검토 (해당 시)
- [ ] 데이터 전송 비용 최적화 (CloudFront, VPC 엔드포인트)
- [ ] 불필요한 리소스 정리 (스냅샷, 로그, 미사용 리소스)
- [ ] 태그 기반 비용 추적 설정"""
        
        # 보안 체크리스트
        security_checklist = f"""- [ ] IAM 최소 권한 원칙 적용
- [ ] Security Group 규칙 최소화
- [ ] 전송 중 암호화 (HTTPS/TLS) 활성화
- [ ] 저장 시 암호화 활성화
- [ ] CloudTrail 로깅 활성화
- [ ] CloudWatch 로그 및 알람 설정
- [ ] 정기적 보안 검토 및 업데이트
- [ ] AWS Security Hub 활용 (선택사항)"""
        
        return {
            "integration_summary": integration_summary,
            "cost_checklist": cost_checklist,
            "security_checklist": security_checklist
        }

    
    def populate_template(self, day_number: int) -> str:
        """템플릿에 데이터 채우기 및 한국어 현지화 적용"""
        config = self.get_daily_config(day_number)
        
        # 현지화된 템플릿 변수 가져오기
        localized_vars = self.localization_processor.get_localized_template_vars(day_number)
        
        # primary_services를 문자열로 변환
        primary_services_str = ", ".join(config["primary_services"])
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        # 기본 정보
        replacements = {
            "{day_number}": str(day_number),
            "{day_title}": config["title"],
            "{service_name}": primary_service,
            "{primary_services}": primary_services_str,
            "{current_date}": datetime.now().strftime("%Y-%m-%d")
        }
        
        # 서비스 연계 패턴
        replacements["{integration_patterns}"] = self.generate_integration_patterns(day_number, config)
        
        # 아키텍처 진화 경로
        evolution_data = self.generate_evolution_paths(day_number, config)
        replacements.update(evolution_data)
        
        # 비용 최적화
        cost_data = self.generate_cost_optimization(day_number, config)
        replacements.update(cost_data)
        
        # 보안 베스트 프랙티스
        security_data = self.generate_security_practices(day_number, config)
        replacements.update(security_data)
        
        # 운영 우수성
        operational_data = self.generate_operational_practices(day_number, config)
        replacements.update(operational_data)
        
        # 관련 학습 내용
        replacements["{related_days_content}"] = self.generate_related_days_content(day_number, config)
        
        # 참고 자료
        reference_data = self.generate_reference_links(day_number, config)
        replacements.update(reference_data)
        
        # 핵심 요약
        summary_data = self.generate_summary_sections(day_number, config)
        replacements.update(summary_data)
        
        # 현지화된 변수 추가
        replacements.update(localized_vars)
        
        # 템플릿 치환
        content = self.template_content
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        # 한국어 현지화 적용 (AWS 서비스명 등에 한영 병기)
        content = self.localization_processor.localize_content(content, day_number)
        
        return content
    
    def generate_best_practices(self, day_number: int, output_path: Optional[Path] = None) -> str:
        """특정 일차의 베스트 프랙티스 생성
        
        Args:
            day_number: 일차 번호 (1-28)
            output_path: 출력 파일 경로 (선택사항)
            
        Returns:
            생성된 콘텐츠
        """
        # 설정 가져오기
        config = self.get_daily_config(day_number)
        week_number = config["week"]
        
        # 출력 경로 설정
        if output_path is None:
            output_path = (
                self.output_base_path / 
                f"week{week_number}" / 
                f"day{day_number}" / 
                "advanced" / 
                "best-practices.md"
            )
        
        # 콘텐츠 생성
        content = self.populate_template(day_number)
        
        # 디렉토리 생성
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 파일 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Generated best practices for Day {day_number}: {output_path}")
        
        return content
    
    def generate_all_best_practices(self, start_day: int = 1, end_day: int = 28) -> Dict[int, str]:
        """모든 일차의 베스트 프랙티스 생성
        
        Args:
            start_day: 시작 일차 (기본값: 1)
            end_day: 종료 일차 (기본값: 28)
            
        Returns:
            일차별 생성된 파일 경로 딕셔너리
        """
        results = {}
        
        print(f"\n{'='*60}")
        print(f"Best Practices Generator - Generating Days {start_day} to {end_day}")
        print(f"{'='*60}\n")
        
        for day in range(start_day, end_day + 1):
            try:
                config = self.get_daily_config(day)
                week_number = config["week"]
                output_path = (
                    self.output_base_path / 
                    f"week{week_number}" / 
                    f"day{day}" / 
                    "advanced" / 
                    "best-practices.md"
                )
                
                self.generate_best_practices(day, output_path)
                results[day] = str(output_path)
                
            except Exception as e:
                print(f"✗ Error generating best practices for Day {day}: {e}")
                results[day] = f"Error: {e}"
        
        print(f"\n{'='*60}")
        print(f"Generation Complete!")
        print(f"Successfully generated: {sum(1 for v in results.values() if not v.startswith('Error'))} / {end_day - start_day + 1}")
        print(f"{'='*60}\n")
        
        return results
    
    # Helper methods for content generation
    
    def _get_service_category(self, service: str) -> str:
        """서비스 카테고리 반환"""
        categories = {
            "EC2": "Compute",
            "Lambda": "Compute",
            "S3": "Storage",
            "EBS": "Storage",
            "RDS": "Database",
            "DynamoDB": "Database",
            "VPC": "Networking & Content Delivery",
            "CloudFront": "Networking & Content Delivery",
            "Route 53": "Networking & Content Delivery",
            "IAM": "Security, Identity, & Compliance",
            "CloudWatch": "Management & Governance",
            "CloudTrail": "Management & Governance",
            "ELB": "Networking & Content Delivery",
            "Auto Scaling": "Compute",
            "SNS": "Application Integration",
            "SQS": "Application Integration",
            "ElastiCache": "Database",
            "ECS": "Compute",
            "EKS": "Compute",
            "Fargate": "Compute"
        }
        return categories.get(service, "Services")

    
    def _get_integration_use_case(self, service1: str, service2: str) -> str:
        """통합 사용 사례 생성"""
        use_cases = {
            ("EC2", "S3"): "애플리케이션 데이터를 안전하게 저장하고 백업",
            ("EC2", "RDS"): "확장 가능한 데이터베이스 백엔드 구축",
            ("S3", "CloudFront"): "정적 콘텐츠를 전 세계에 빠르게 배포",
            ("Lambda", "S3"): "이벤트 기반 데이터 처리 자동화",
            ("Lambda", "DynamoDB"): "서버리스 API 백엔드 구축",
            ("ELB", "EC2"): "고가용성 웹 애플리케이션 구성",
            ("Route 53", "CloudFront"): "글로벌 DNS 및 CDN 통합",
            ("VPC", "EC2"): "격리된 네트워크 환경에서 안전한 리소스 운영"
        }
        return use_cases.get((service1, service2), f"{service1}와 {service2}를 통합하여 시너지 효과 창출")
    
    def _get_integration_benefit(self, service1: str, service2: str) -> str:
        """통합 이점 설명"""
        return f"{service1}의 강점과 {service2}의 장점을 결합하여 더 강력한 솔루션 구축"
    
    def _get_primary_config(self, service: str) -> str:
        """주요 설정 설명"""
        configs = {
            "EC2": "인스턴스 타입, AMI, 보안 그룹, 키 페어",
            "S3": "버킷 이름, 리전, 버전 관리, 암호화",
            "RDS": "엔진 유형, 인스턴스 클래스, 스토리지, 백업",
            "Lambda": "런타임, 메모리, 타임아웃, 환경 변수",
            "DynamoDB": "테이블 이름, 파티션 키, 읽기/쓰기 용량",
            "VPC": "CIDR 블록, 서브넷, 라우팅 테이블",
            "CloudFront": "오리진, 캐시 동작, SSL 인증서"
        }
        return configs.get(service, "기본 구성 설정")
    
    def _get_integration_config(self, service1: str, service2: str) -> str:
        """통합 설정 설명"""
        return f"{service1}에서 {service2} 리소스 선택 및 권한 설정"
    
    def _get_test_method(self, service1: str, service2: str) -> str:
        """테스트 방법 설명"""
        return f"{service1}에서 {service2}로 데이터 전송 또는 API 호출 테스트"
    
    def _get_performance_benefit(self, service1: str, service2: str) -> str:
        """성능 이점"""
        return "응답 시간 단축, 처리량 증가, 지연 시간 감소"
    
    def _get_cost_benefit(self, service1: str, service2: str) -> str:
        """비용 이점"""
        return "효율적인 리소스 사용으로 비용 최적화 가능"
    
    def _get_constraints(self, service1: str, service2: str) -> str:
        """제약사항"""
        return "서비스 간 데이터 전송 비용, 리전 제약, API 호출 제한"
    
    def _get_alternative_1(self, service1: str, service2: str) -> str:
        """대안 1"""
        return f"{service1} 단독 사용 (기능 제한적)"
    
    def _get_alternative_2(self, service1: str, service2: str) -> str:
        """대안 2"""
        return "다른 AWS 서비스 조합 검토"
    
    def _get_real_world_example(self, service1: str, service2: str) -> str:
        """실제 사례"""
        examples = {
            ("EC2", "S3"): "Netflix: EC2에서 처리한 비디오를 S3에 저장하고 CloudFront로 배포",
            ("Lambda", "DynamoDB"): "Airbnb: 서버리스 API로 예약 시스템 구축",
            ("S3", "CloudFront"): "Pinterest: 이미지를 S3에 저장하고 CloudFront로 전 세계 배포"
        }
        return examples.get((service1, service2), f"다양한 기업에서 {service1}와 {service2} 통합 활용")
    
    def _generate_basic_architecture_diagram(self, service: str) -> str:
        """기본 아키텍처 다이어그램 생성"""
        return f"""graph TB
    User[사용자] --> Service[{service}]
    Service --> Data[데이터 저장소]
    
    style Service fill:#FF9900
    style User fill:#232F3E
    style Data fill:#3F8624"""
    
    def _generate_integrated_architecture_diagram(self, primary_service: str, related_days: List[int]) -> str:
        """통합 아키텍처 다이어그램 생성"""
        services = [primary_service]
        for day in related_days[:2]:
            if day in DAILY_TOPICS:
                services.append(DAILY_TOPICS[day]["primary_services"][0] if DAILY_TOPICS[day]["primary_services"] else "AWS Service")
        
        diagram = "graph TB\n    User[사용자] --> Service1[" + services[0] + "]\n"
        for i, service in enumerate(services[1:], 2):
            diagram += f"    Service1 --> Service{i}[{service}]\n"
        
        diagram += "\n    style Service1 fill:#FF9900"
        for i in range(2, len(services) + 1):
            diagram += f"\n    style Service{i} fill:#3F8624"
        
        return diagram
    
    def _generate_optimized_architecture_diagram(self, primary_service: str, related_days: List[int]) -> str:
        """최적화된 아키텍처 다이어그램 생성"""
        return f"""graph TB
    subgraph "프론트엔드"
        User[사용자]
        CDN[CloudFront]
    end
    
    subgraph "애플리케이션 계층"
        LB[Load Balancer]
        Service[{primary_service}]
        Cache[ElastiCache]
    end
    
    subgraph "데이터 계층"
        DB[(Database)]
        Storage[S3]
    end
    
    subgraph "모니터링"
        CW[CloudWatch]
        CT[CloudTrail]
    end
    
    User --> CDN
    CDN --> LB
    LB --> Service
    Service --> Cache
    Service --> DB
    Service --> Storage
    Service --> CW
    Service --> CT
    
    style Service fill:#FF9900
    style CDN fill:#3F8624
    style LB fill:#3F8624"""
    
    def _generate_stage2_services(self, primary_service: str, related_days: List[int]) -> str:
        """Stage 2 추가 서비스 설명"""
        services = []
        for day in related_days[:2]:
            if day in DAILY_TOPICS:
                service = DAILY_TOPICS[day]["primary_services"][0] if DAILY_TOPICS[day]["primary_services"] else "AWS Service"
                services.append(f"- **{service}** (Day {day}): {self._get_service_role(service)}")
        
        return "\n".join(services) if services else "- 추가 서비스 통합 예정"
    
    def _get_service_role(self, service: str) -> str:
        """서비스 역할 설명"""
        roles = {
            "S3": "데이터 저장 및 백업",
            "RDS": "관계형 데이터베이스 관리",
            "DynamoDB": "NoSQL 데이터베이스",
            "Lambda": "서버리스 컴퓨팅",
            "CloudFront": "콘텐츠 배포 네트워크",
            "ELB": "로드 밸런싱",
            "IAM": "접근 제어 및 보안",
            "CloudWatch": "모니터링 및 로깅",
            "VPC": "네트워크 격리"
        }
        return roles.get(service, "추가 기능 제공")
    
    def _generate_cost_optimization_methods(self, service: str) -> str:
        """비용 최적화 방법 생성"""
        methods = {
            "EC2": """1. **인스턴스 타입 최적화**
   - 현재 설정: 과도하게 프로비저닝된 인스턴스
   - 권장 설정: CloudWatch 메트릭 기반 적절한 인스턴스 타입 선택
   - 예상 절감: 월 $100-500

2. **자동 스케일링 활용**
   - Console 경로: EC2 > Auto Scaling Groups
   - 정책 설정: CPU 사용률 기반 스케일링 (목표: 70%)
   - 예상 효과: 피크 시간 외 30-40% 비용 절감""",
            
            "S3": """1. **스토리지 클래스 최적화**
   - 현재 설정: 모든 데이터를 Standard 클래스에 저장
   - 권장 설정: Lifecycle 정책으로 자동 티어링
     - 30일 후: Standard-IA
     - 90일 후: Glacier
   - 예상 절감: 월 $50-200

2. **불필요한 데이터 정리**
   - 미완료 멀티파트 업로드 삭제
   - 이전 버전 데이터 정리
   - 예상 효과: 10-20% 스토리지 비용 절감""",
            
            "RDS": """1. **인스턴스 사이징**
   - 현재 설정: 과도한 인스턴스 클래스
   - 권장 설정: 실제 워크로드에 맞는 인스턴스 선택
   - 예상 절감: 월 $200-800

2. **읽기 복제본 활용**
   - 읽기 전용 쿼리를 복제본으로 분산
   - 마스터 인스턴스 부하 감소
   - 예상 효과: 성능 향상 및 비용 최적화"""
        }
        
        return methods.get(service, """1. **리소스 사이징**
   - CloudWatch 메트릭으로 실제 사용률 분석
   - 적절한 리소스 크기 선택
   - 예상 절감: 20-40%

2. **자동화 활용**
   - 사용하지 않는 시간에 리소스 중지
   - 스케줄 기반 자동화
   - 예상 효과: 추가 10-20% 절감""")
    
    def _generate_reserved_instances_strategy(self, service: str) -> str:
        """예약 인스턴스 전략"""
        if service in ["EC2", "RDS", "ElastiCache"]:
            return f"""**{service} 예약 인스턴스 활용**:

- **사용 패턴 분석**: 
  - Cost Explorer로 지난 3-6개월 사용 패턴 확인
  - 안정적으로 사용되는 인스턴스 식별
  
- **예약 옵션 비교**:
  - 1년 예약: 약 30-40% 할인
  - 3년 예약: 약 50-60% 할인
  - 전체 선결제 vs 부분 선결제 vs 선결제 없음
  
- **ROI 계산**:
  - 예상 사용 기간 및 비용 절감액 계산
  - 유연성 vs 비용 절감 트레이드오프 고려"""
        else:
            return "해당 서비스는 예약 인스턴스를 지원하지 않습니다."
    
    def _generate_spot_instances_strategy(self, service: str) -> str:
        """스팟 인스턴스 전략"""
        if service == "EC2":
            return """**EC2 스팟 인스턴스 활용**:

- **적합한 워크로드**:
  - 배치 처리, 데이터 분석
  - 상태 비저장(stateless) 애플리케이션
  - 중단 가능한 작업
  
- **중단 처리 방법**:
  - 2분 경고 알림 활용
  - 체크포인트 및 재시작 로직 구현
  - 스팟 + 온디맨드 혼합 사용
  
- **비용 절감 효과**:
  - 온디맨드 대비 최대 90% 할인
  - 실제 평균 절감: 60-70%"""
        else:
            return "해당 서비스는 스팟 인스턴스를 지원하지 않습니다."
    
    def _get_integration_description(self, service1: str, service2: str) -> str:
        """통합 설명"""
        return f"{service1}와 {service2}의 연계 방법 및 활용"
    
    def _get_future_integration(self, service1: str, service2: str) -> str:
        """향후 통합 설명"""
        return f"{service1}에 {service2}를 추가하여 기능 확장"


# CLI 실행을 위한 메인 함수
def main():
    """CLI 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS SAA Best Practices Generator")
    parser.add_argument(
        "--day",
        type=int,
        help="Generate best practices for specific day (1-28)"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start day for batch generation (default: 1)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=28,
        help="End day for batch generation (default: 28)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Custom output path (optional)"
    )
    
    args = parser.parse_args()
    
    generator = BestPracticesGenerator()
    
    if args.day:
        # 단일 일차 생성
        output_path = Path(args.output) if args.output else None
        generator.generate_best_practices(args.day, output_path)
    else:
        # 배치 생성
        generator.generate_all_best_practices(args.start, args.end)


if __name__ == "__main__":
    main()
