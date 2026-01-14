# Hands-On Console README Generator
"""
AWS Console 기반 실습 가이드 생성기
각 일별(Day 1-28) hands-on-console/README.md 파일을 템플릿 기반으로 생성
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.daily_topics import DAILY_TOPICS, get_topic_by_day
from src.config import (
    TEMPLATES_ROOT, STUDY_MATERIALS_ROOT, AWS_DOCS_BASE_URL
)


class HandsOnConsoleGenerator:
    """AWS Console 기반 실습 가이드 생성기"""
    
    def __init__(self):
        self.template_path = TEMPLATES_ROOT / "hands-on-console-template.md"
        self.output_base_path = STUDY_MATERIALS_ROOT
        self.prerequisites_base = "../../resources/prerequisites"
        
    def load_template(self) -> str:
        """템플릿 파일 로드"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_daily_config(self, day_number: int) -> Dict:
        """일별 주제 설정 가져오기"""
        return get_topic_by_day(day_number)
    
    def _get_prerequisite_links(self, day_number: int) -> str:
        """사전 요구사항 링크 생성"""
        # 기본 사전 요구사항 (모든 일차 공통)
        prerequisites = [
            f"- [ ] [AWS 계정 설정]({self.prerequisites_base}/aws-account-setup.md)",
            f"- [ ] [IAM 사용자 설정]({self.prerequisites_base}/iam-user-setup.md)",
            f"- [ ] [Console 탐색 기본]({self.prerequisites_base}/console-navigation.md)"
        ]
        
        # 일차별 추가 사전 요구사항
        if day_number >= 3:  # EC2 이후부터는 CLI 설정 필요
            prerequisites.append(
                f"- [ ] [CLI 구성]({self.prerequisites_base}/cli-configuration.md) (선택사항)"
            )
        
        return "\n".join(prerequisites)
    
    def _estimate_cost(self, day_number: int) -> Dict[str, str]:
        """예상 비용 계산"""
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        
        # 서비스별 비용 추정 (Free Tier 고려)
        free_tier_services = [
            "IAM", "CloudWatch", "CloudTrail", "VPC", "Route 53"
        ]
        
        # 주요 서비스가 Free Tier에 포함되는지 확인
        is_free_tier = any(
            any(free_service.lower() in service.lower() for free_service in free_tier_services)
            for service in services
        )
        
        if is_free_tier or day_number in [1, 2, 5, 6, 23]:
            return {
                "amount": "$0.00",
                "note": "Free Tier 범위 내",
                "warning": ""
            }
        elif day_number in [3, 4, 7]:  # EC2 관련
            return {
                "amount": "$0.50 - $2.00",
                "note": "t2.micro/t3.micro 인스턴스 사용 시",
                "warning": "⚠️ 실습 후 반드시 리소스를 삭제하세요"
            }
        elif day_number in [8, 9]:  # S3, EBS/EFS
            return {
                "amount": "$0.10 - $0.50",
                "note": "소량 데이터 저장 및 전송",
                "warning": "⚠️ 실습 후 반드시 리소스를 삭제하세요"
            }
        elif day_number in [10, 11, 12]:  # RDS, DynamoDB, ElastiCache
            return {
                "amount": "$1.00 - $5.00",
                "note": "최소 인스턴스 사용 시",
                "warning": "⚠️ 실습 후 반드시 리소스를 삭제하세요"
            }
        else:
            return {
                "amount": "$0.50 - $3.00",
                "note": "일반적인 실습 비용",
                "warning": "⚠️ 실습 후 반드시 리소스를 삭제하세요"
            }
    
    def _estimate_time(self, day_number: int) -> str:
        """예상 소요 시간 계산"""
        config = self.get_daily_config(day_number)
        services_count = len(config["primary_services"])
        
        # 서비스 복잡도에 따른 시간 추정
        if day_number in [1, 2]:  # 개념 중심
            return "20-30분"
        elif day_number in [3, 4, 8, 10]:  # 기본 서비스 실습
            return "30-45분"
        elif day_number in [5, 6, 13, 14]:  # 복잡한 네트워크/아키텍처
            return "45-60분"
        elif services_count >= 3:  # 여러 서비스 통합
            return "60-90분"
        else:
            return "30-45분"

    
    def _generate_exercises(self, day_number: int) -> List[Dict]:
        """실습 연습 문제 생성"""
        config = self.get_daily_config(day_number)
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        exercises = []
        
        # Exercise 1: 기본 리소스 생성
        exercises.append({
            "number": 1,
            "title": f"{primary_service} 생성 및 기본 설정",
            "objective": f"AWS Console을 통해 {primary_service}를 생성하고 기본 설정을 구성합니다.",
            "steps": [
                {
                    "step": 1,
                    "title": f"{primary_service} 생성",
                    "console_path": f"Services > [Category] > {primary_service}",
                    "action": f'"Create {primary_service.split()[0].lower()}" 버튼 클릭',
                    "config": {
                        "Name": f"day{day_number}-{primary_service.lower().replace(' ', '-')}",
                        "Region": "ap-northeast-2 (서울)",
                    }
                },
                {
                    "step": 2,
                    "title": "기본 설정 구성",
                    "action": "필수 설정 항목 입력",
                    "config": {}
                },
                {
                    "step": 3,
                    "title": "생성 확인",
                    "action": '"Create" 버튼 클릭 및 생성 완료 대기',
                    "verification": [
                        "리소스 상태가 'Available' 또는 'Active'로 표시되는지 확인",
                        "설정이 올바르게 적용되었는지 검증"
                    ]
                }
            ],
            "estimated_time": "10-15분"
        })
        
        # Exercise 2: 보안 및 접근 제어 (IAM 관련 일차가 아닌 경우)
        if day_number != 2:
            exercises.append({
                "number": 2,
                "title": "보안 및 접근 제어 설정",
                "objective": "리소스에 대한 보안 설정을 구성합니다.",
                "steps": [
                    {
                        "step": 1,
                        "title": "보안 그룹 구성",
                        "console_path": "VPC > Security Groups",
                        "action": "필요한 인바운드/아웃바운드 규칙 설정"
                    },
                    {
                        "step": 2,
                        "title": "IAM 역할 연결",
                        "console_path": "IAM > Roles",
                        "action": "최소 권한 원칙에 따른 역할 생성 및 연결"
                    }
                ],
                "estimated_time": "10-15분"
            })
        
        # Exercise 3: 모니터링 설정
        exercises.append({
            "number": len(exercises) + 1,
            "title": "모니터링 및 알람 설정",
            "objective": "CloudWatch를 통해 리소스를 모니터링하고 알람을 설정합니다.",
            "steps": [
                {
                    "step": 1,
                    "title": "CloudWatch 메트릭 확인",
                    "console_path": "CloudWatch > Metrics",
                    "action": f"{primary_service} 관련 메트릭 확인"
                },
                {
                    "step": 2,
                    "title": "알람 생성",
                    "console_path": "CloudWatch > Alarms > Create alarm",
                    "action": "임계값 기반 알람 설정"
                }
            ],
            "estimated_time": "10-15분"
        })
        
        return exercises
    
    def _generate_cleanup_steps(self, day_number: int) -> List[Dict]:
        """리소스 정리 단계 생성"""
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        
        cleanup_steps = []
        
        # 역순으로 리소스 삭제 (의존성 고려)
        for idx, service in enumerate(reversed(services), start=1):
            cleanup_steps.append({
                "step": idx,
                "resource": service,
                "console_path": f"Services > [Category] > {service}",
                "action": "리소스 선택 > Actions > Delete",
                "verification": f"{service} 리소스가 완전히 삭제되었는지 확인"
            })
        
        # CloudWatch 알람 정리
        cleanup_steps.append({
            "step": len(cleanup_steps) + 1,
            "resource": "CloudWatch 알람",
            "console_path": "CloudWatch > Alarms",
            "action": "생성한 알람 선택 > Actions > Delete",
            "verification": "모든 알람이 삭제되었는지 확인"
        })
        
        # 비용 확인
        cleanup_steps.append({
            "step": len(cleanup_steps) + 1,
            "resource": "비용 확인",
            "console_path": "Billing > Bills",
            "action": "현재 월 비용 확인",
            "verification": "예상 비용 범위 내인지 확인"
        })
        
        return cleanup_steps
    
    def _generate_learning_points(self, day_number: int) -> List[str]:
        """학습 포인트 생성"""
        config = self.get_daily_config(day_number)
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        
        learning_points = [
            f"{primary_service}의 핵심 기능 및 사용 사례 이해",
            "AWS Console을 통한 리소스 생성 및 관리 방법",
            "보안 그룹 및 IAM 역할을 통한 접근 제어",
            "CloudWatch를 활용한 모니터링 및 알람 설정",
            "비용 최적화를 위한 리소스 정리 중요성"
        ]
        
        # 일차별 특화 학습 포인트 추가
        if day_number in [1]:
            learning_points.append("AWS 글로벌 인프라 및 리전 선택의 중요성")
        elif day_number in [2]:
            learning_points.append("최소 권한 원칙 및 IAM 베스트 프랙티스")
        elif day_number in [3, 4]:
            learning_points.append("EC2 인스턴스 타입 선택 및 성능 최적화")
        elif day_number in [5, 6]:
            learning_points.append("VPC 네트워크 설계 및 보안 경계 구성")
        elif day_number in [8]:
            learning_points.append("S3 스토리지 클래스 및 수명 주기 정책")
        elif day_number in [10, 11]:
            learning_points.append("데이터베이스 백업 및 고가용성 구성")
        
        return learning_points
    
    def _generate_mermaid_diagram(self, day_number: int) -> str:
        """실습 아키텍처 다이어그램 생성"""
        config = self.get_daily_config(day_number)
        services = config["primary_services"]
        
        diagram = "```mermaid\ngraph TB\n"
        diagram += '    subgraph "사용자"\n'
        diagram += '        User[실습 참가자]\n'
        diagram += '    end\n\n'
        diagram += f'    subgraph "AWS Console - Day {day_number} 실습"\n'
        
        # 주요 서비스 노드 추가
        for idx, service in enumerate(services[:3], start=1):
            node_id = f"S{idx}"
            diagram += f'        {node_id}[{service}]\n'
        
        diagram += '    end\n\n'
        
        # 연결 추가
        diagram += '    User -->|Console 접속| S1\n'
        if len(services) > 1:
            for idx in range(1, min(3, len(services))):
                diagram += f'    S{idx} --> S{idx+1}\n'
        
        diagram += '```'
        
        return diagram

    
    def populate_template(self, day_number: int, template: str) -> str:
        """템플릿 플레이스홀더 치환"""
        config = self.get_daily_config(day_number)
        cost_estimate = self._estimate_cost(day_number)
        time_estimate = self._estimate_time(day_number)
        exercises = self._generate_exercises(day_number)
        cleanup_steps = self._generate_cleanup_steps(day_number)
        learning_points = self._generate_learning_points(day_number)
        architecture_diagram = self._generate_mermaid_diagram(day_number)
        
        primary_service = config["primary_services"][0] if config["primary_services"] else "AWS Service"
        service_name = primary_service
        
        # 기본 정보 치환
        replacements = {
            "{day_number}": str(day_number),
            "{day_title}": config["title"],
            "{primary_service}": primary_service,
            "{service_name}": service_name,
            "{service_description}": f"{config['title']}에서 학습한 내용을 실습합니다.",
            
            # 사전 요구사항
            "{prerequisites}": self._get_prerequisite_links(day_number),
            "{estimated_cost}": cost_estimate["amount"],
            "{cost_note}": cost_estimate["note"],
            "{cost_warning}": cost_estimate["warning"],
            "{estimated_time}": time_estimate,
            "{free_tier_status}": cost_estimate["note"],
            "{free_tier_resources}": primary_service if cost_estimate["amount"] == "$0.00" else "해당 없음",
            "{paid_resources}": "해당 없음" if cost_estimate["amount"] == "$0.00" else primary_service,
            "{recommended_region}": "ap-northeast-2",
            "{required_permissions}": f"{primary_service}FullAccess 또는 관리자 권한",
            
            # 아키텍처 다이어그램
            "{architecture_diagram}": architecture_diagram,
            "{architecture_description}": f"{primary_service}를 중심으로 한 실습 환경",
            "{main_components}": ", ".join(config["primary_services"][:3]),
            "{data_flow}": "사용자 → Console → AWS 서비스 → CloudWatch",
            "{related_service_1}": config["primary_services"][1] if len(config["primary_services"]) > 1 else "CloudWatch",
            "{related_service_2}": config["primary_services"][2] if len(config["primary_services"]) > 2 else "IAM",
            
            # 실습 목표
            "{objective_1}": f"{primary_service} 생성 및 구성",
            "{objective_2}": "보안 및 접근 제어 설정",
            "{objective_3}": "모니터링 및 알람 구성",
            "{goal_1}": f"{primary_service} 리소스 생성",
            "{goal_1_description}": f"AWS Console을 통해 {primary_service}를 생성하고 기본 설정을 구성합니다",
            "{goal_2}": "보안 설정 구성",
            "{goal_2_description}": "IAM 역할 및 보안 그룹을 통한 접근 제어를 설정합니다",
            "{goal_3}": "모니터링 구성",
            "{goal_3_description}": "CloudWatch를 통한 메트릭 수집 및 알람을 설정합니다",
            "{goal_4}": "실제 사용 시나리오 테스트",
            "{goal_4_description}": "구성한 리소스를 실제로 사용하고 동작을 확인합니다",
            
            # Exercise 관련
            "{exercise_1_goal}": f"AWS Console을 통해 {primary_service}를 생성하고 기본 설정을 구성합니다.",
            "{exercise_1_time}": "10-15",
            "{category}": "Compute" if "EC2" in primary_service else "Storage" if "S3" in primary_service else "Database" if any(db in primary_service for db in ["RDS", "DynamoDB"]) else "Networking",
            "{resource}": primary_service.split()[0].lower(),
            "{resource_name}": primary_service.lower().replace(" ", "-"),
            "{region_reason}": "낮은 지연시간 및 한국 사용자 대상",
            "{setting_1}": "Type",
            "{setting_1_value}": "Standard",
            "{setting_1_description}": "기본 설정 유형",
            "{setting_1_reason}": "일반적인 사용 사례에 적합",
            "{setting_2}": "Configuration",
            "{setting_2_value}": "Default",
            "{setting_2_description}": "기본 구성",
            "{setting_2_reason}": "학습 목적으로 충분",
            "{advanced_setting_1}": "High Availability",
            "{advanced_setting_1_value}": "Enabled",
            "{advanced_setting_1_description}": "고가용성 구성",
            "{advanced_setting_1_use_case}": "프로덕션 환경",
            "{advanced_setting_2}": "Backup",
            "{advanced_setting_2_value}": "Enabled",
            "{advanced_setting_2_description}": "자동 백업",
            "{advanced_setting_2_use_case}": "데이터 보호 필요 시",
            "{your_name}": "your-name",
            "{creation_time}": "2-5",
            "{status_check_method}": "리소스 목록에서 상태 컬럼 확인",
            "{common_creation_errors}": "권한 부족, 리전 제한, 리소스 한도 초과",
            
            # Exercise 2
            "{exercise_2_goal}": f"{primary_service}와 다른 서비스를 통합합니다.",
            "{exercise_2_time}": "10-15",
            "{category_2}": "Management",
            "{resource_2}": "monitoring",
            "{resource_2_name}": "monitoring",
            "{setting_3}": "Interval",
            "{setting_3_value}": "5 minutes",
            "{setting_4}": "Retention",
            "{setting_4_value}": "7 days",
            "{connection_setting_1}": "Auto-enable",
            "{connection_value_1}": "Yes",
            "{connection_setting_2}": "Detailed monitoring",
            "{connection_value_2}": "Enabled",
            "{existing_role_name}": "기존 역할 없음",
            "{service_role_name}": f"{primary_service.lower().replace(' ', '-')}-role",
            "{required_policies}": f"{primary_service}FullAccess, CloudWatchFullAccess",
            "{expected_test_result}": "Connection successful",
            
            # Exercise 3
            "{exercise_3_goal}": "CloudWatch를 통해 리소스를 모니터링하고 알람을 설정합니다.",
            "{exercise_3_time}": "10-15",
            "{metric_namespace}": f"AWS/{primary_service.split()[0]}",
            "{metric_name_1}": "CPUUtilization" if "EC2" in primary_service else "RequestCount",
            "{metric_dimensions}": f"{primary_service}Name",
            "{metric_display_name}": "CPU 사용률" if "EC2" in primary_service else "요청 수",
            "{metric_name_2}": "NetworkIn" if "EC2" in primary_service else "DataTransfer",
            "{metric_display_name_2}": "네트워크 입력" if "EC2" in primary_service else "데이터 전송",
            "{statistic}": "Average",
            "{alarm_metric_name}": "CPUUtilization" if "EC2" in primary_service else "ErrorCount",
            "{comparison_operator}": "Greater",
            "{threshold_value}": "80" if "EC2" in primary_service else "10",
            "{datapoints}": "2",
            "{evaluation_periods}": "2",
            "{your_email}": "your-email@example.com",
            "{alarm_description}": f"{primary_service} 성능 알람",
            
            # Exercise 4
            "{exercise_4_goal}": "구성한 리소스를 실제로 사용하고 동작을 확인합니다.",
            "{exercise_4_time}": "10-15",
            "{test_data_preparation_step_1}": "테스트 데이터 준비",
            "{test_data_preparation_step_2}": "테스트 환경 설정",
            "{test_action_1}": "기본 기능 테스트",
            "{test_action_1_steps}": "리소스 접근 및 기본 작업 수행",
            "{test_action_1_expected_result}": "정상 작동 확인",
            "{test_action_2}": "통합 기능 테스트",
            "{test_action_2_steps}": "다른 서비스와의 연동 확인",
            "{test_action_2_expected_result}": "통합 정상 작동",
            "{performance_metric_1}": "응답 시간",
            "{expected_value_1}": "< 100ms",
            "{performance_metric_2}": "처리량",
            "{expected_value_2}": "> 100 TPS",
            "{performance_metric_3}": "에러율",
            "{expected_value_3}": "< 1%",
            "{log_group_name}": f"/aws/{primary_service.lower().replace(' ', '/')}",
            
            # 정리
            "{deletion_time_1}": "2-5",
            "{deletion_time_2}": "1-3",
            "{estimated_total_cost}": cost_estimate["amount"],
            "{final_cost}": cost_estimate["amount"],
            "{service_cost}": cost_estimate["amount"],
            "{projected_cost}": cost_estimate["amount"],
            "{estimated_excess_cost}": cost_estimate["amount"],
            
            # 학습 포인트
            "{concept_1}": f"{primary_service} 아키텍처",
            "{concept_1_description}": f"{primary_service}의 기본 구조 및 동작 원리",
            "{concept_1_learning}": "Console을 통한 리소스 생성 및 구성 방법",
            "{concept_1_application}": "실제 프로젝트에서의 활용 방법",
            "{concept_2}": "보안 및 접근 제어",
            "{concept_2_description}": "IAM 및 보안 그룹을 통한 접근 제어",
            "{concept_2_learning}": "최소 권한 원칙 적용 방법",
            "{concept_2_application}": "프로덕션 환경 보안 설정",
            "{concept_3}": "모니터링 및 알람",
            "{concept_3_description}": "CloudWatch를 통한 리소스 모니터링",
            "{concept_3_learning}": "메트릭 수집 및 알람 설정 방법",
            "{concept_3_application}": "운영 환경 모니터링 전략",
            "{common_failure_reason}": "설정 오류 또는 권한 부족",
            "{common_failure_solution}": "설정 재확인 및 IAM 권한 검토",
            
            # 관련 자료
            "{previous_day}": str(max(1, day_number - 1)),
            "{next_day}": str(min(28, day_number + 1)),
            "{company_name}": config.get("case_study_company", "AWS 고객사"),
            "{user_guide_link}": f"{AWS_DOCS_BASE_URL}/{primary_service.lower().replace(' ', '-')}/latest/userguide/",
            "{api_reference_link}": f"{AWS_DOCS_BASE_URL}/{primary_service.lower().replace(' ', '-')}/latest/APIReference/",
            "{console_guide_link}": f"{AWS_DOCS_BASE_URL}/awsconsolehelpdocs/latest/gsg/",
            "{getting_started_link}": f"{AWS_DOCS_BASE_URL}/{primary_service.lower().replace(' ', '-')}/latest/gsg/",
            "{aws_tutorials_link}": "https://aws.amazon.com/getting-started/hands-on/",
            "{aws_workshops_link}": "https://workshops.aws/",
            "{skill_builder_link}": "https://skillbuilder.aws/",
            
            # FAQ
            "{free_tier_answer}": "Free Tier 한도를 초과하면 사용량에 따라 비용이 청구됩니다. Billing Dashboard에서 실시간으로 확인 가능합니다.",
            "{error_handling_answer}": "CloudWatch Logs 및 Events를 확인하고, AWS 공식 문서의 트러블슈팅 가이드를 참조하세요.",
            "{cleanup_forgotten_answer}": "리소스가 계속 실행되어 비용이 발생할 수 있습니다. Billing Dashboard에서 알람을 설정하는 것을 권장합니다.",
            "{region_compatibility_answer}": "대부분의 AWS 서비스는 모든 리전에서 동일하게 작동하지만, 일부 서비스는 특정 리전에서만 사용 가능합니다.",
            "{production_difference_answer}": "프로덕션 환경에서는 고가용성, 백업, 보안, 모니터링 등을 더 강화하여 구성합니다.",
            
            # 현재 날짜
            "{current_date}": datetime.now().strftime("%Y-%m-%d"),
            "{date}": datetime.now().strftime("%Y-%m-%d"),
            "{actual_time}": time_estimate.split("-")[0],
        }
        
        # 템플릿 치환
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, str(value))
        
        # 실습 연습 문제 섹션 생성
        exercises_section = ""
        for exercise in exercises:
            exercises_section += f"\n### Exercise {exercise['number']}: {exercise['title']}\n"
            exercises_section += f"**목표**: {exercise['objective']}\n\n"
            exercises_section += "**단계**:\n"
            
            for step in exercise['steps']:
                exercises_section += f"{step['step']}. **{step['title']}**\n"
                if 'console_path' in step:
                    exercises_section += f"   - Console 경로: `{step['console_path']}`\n"
                if 'action' in step:
                    exercises_section += f"   - 작업: {step['action']}\n"
                if 'config' in step and step['config']:
                    exercises_section += "   - 설정:\n"
                    for key, value in step['config'].items():
                        exercises_section += f"     - {key}: `{value}`\n"
                if 'verification' in step:
                    exercises_section += "   - 검증:\n"
                    for verify in step['verification']:
                        exercises_section += f"     - {verify}\n"
                exercises_section += "\n"
            
            exercises_section += f"**예상 소요 시간**: {exercise['estimated_time']}\n\n"
            
            # 검증 체크리스트
            exercises_section += "**검증 체크리스트**:\n"
            exercises_section += f"- [ ] Exercise {exercise['number']} 완료\n"
            exercises_section += "- [ ] 모든 설정이 올바르게 적용됨\n"
            exercises_section += "- [ ] 리소스가 정상 작동함\n\n"
        
        result = result.replace("{exercises_section}", exercises_section)
        
        # 리소스 정리 섹션 생성
        cleanup_section = "\n### 정리 순서:\n"
        for step in cleanup_steps:
            cleanup_section += f"{step['step']}. **{step['resource']} 삭제**\n"
            cleanup_section += f"   - Console 경로: `{step['console_path']}`\n"
            cleanup_section += f"   - 작업: {step['action']}\n"
            cleanup_section += f"   - 확인: {step['verification']}\n\n"
        
        cleanup_section += "### 정리 확인:\n"
        cleanup_section += "- [ ] 모든 리소스 삭제 완료\n"
        cleanup_section += "- [ ] Billing Dashboard에서 비용 확인\n"
        cleanup_section += f"- [ ] 예상 비용: {cost_estimate['amount']}\n"
        
        result = result.replace("{cleanup_section}", cleanup_section)
        
        # 학습 포인트 섹션 생성
        learning_section = ""
        for idx, point in enumerate(learning_points, start=1):
            learning_section += f"{idx}. {point}\n"
        
        result = result.replace("{learning_points}", learning_section)
        
        # 다음 단계 링크
        next_steps = f"""- [case-study.md](../case-study.md)에서 실제 기업 사례 확인
- [best-practices.md](../best-practices.md)에서 프로덕션 환경 고려사항 학습
- [troubleshooting.md](../troubleshooting.md)에서 문제 해결 방법 학습"""
        
        result = result.replace("{next_steps}", next_steps)
        
        return result
    
    def generate_hands_on_readme(self, day_number: int, output_path: Optional[Path] = None) -> str:
        """특정 일차의 Hands-On Console README 생성
        
        Args:
            day_number: 일차 번호 (1-28)
            output_path: 출력 파일 경로 (None이면 자동 생성)
            
        Returns:
            생성된 콘텐츠 문자열
        """
        # 템플릿 로드
        template = self.load_template()
        
        # 템플릿 치환
        content = self.populate_template(day_number, template)
        
        # 출력 경로 결정
        if output_path is None:
            config = self.get_daily_config(day_number)
            week_number = config["week"]
            output_path = (
                self.output_base_path / 
                f"week{week_number}" / 
                f"day{day_number}" / 
                "hands-on-console" / 
                "README.md"
            )
        
        # 디렉토리 생성
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 파일 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Generated hands-on console README for Day {day_number}: {output_path}")
        
        return content
    
    def generate_all_hands_on_readmes(self, start_day: int = 1, end_day: int = 28) -> Dict[int, str]:
        """모든 일차의 Hands-On Console README 생성
        
        Args:
            start_day: 시작 일차 (기본값: 1)
            end_day: 종료 일차 (기본값: 28)
            
        Returns:
            일차별 생성된 파일 경로 딕셔너리
        """
        results = {}
        
        print(f"\n{'='*60}")
        print(f"Hands-On Console README Generator - Generating Days {start_day} to {end_day}")
        print(f"{'='*60}\n")
        
        for day in range(start_day, end_day + 1):
            try:
                config = self.get_daily_config(day)
                week_number = config["week"]
                output_path = (
                    self.output_base_path / 
                    f"week{week_number}" / 
                    f"day{day}" / 
                    "hands-on-console" / 
                    "README.md"
                )
                
                self.generate_hands_on_readme(day, output_path)
                results[day] = str(output_path)
                
            except Exception as e:
                print(f"✗ Error generating hands-on README for Day {day}: {e}")
                results[day] = f"Error: {e}"
        
        print(f"\n{'='*60}")
        print(f"Generation Complete!")
        print(f"Successfully generated: {sum(1 for v in results.values() if not v.startswith('Error'))} / {end_day - start_day + 1}")
        print(f"{'='*60}\n")
        
        return results


# CLI 실행을 위한 메인 함수
def main():
    """CLI 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS SAA Hands-On Console README Generator")
    parser.add_argument(
        "--day",
        type=int,
        help="Generate hands-on README for specific day (1-28)"
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
    
    generator = HandsOnConsoleGenerator()
    
    if args.day:
        # 단일 일차 생성
        output_path = Path(args.output) if args.output else None
        generator.generate_hands_on_readme(args.day, output_path)
    else:
        # 배치 생성
        generator.generate_all_hands_on_readmes(args.start, args.end)


if __name__ == "__main__":
    main()
