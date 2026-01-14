"""
Integration tests for Week 1 (Day 1-7) complete workflow.

This test suite validates:
- All components work together correctly
- Content generation for all Week 1 days
- File structure integrity
- Cross-day service integrations
- Content quality and completeness
"""

import pytest
from pathlib import Path
import re


class TestWeek1Integration:
    """Integration tests for Week 1 complete workflow."""
    
    @pytest.fixture
    def week1_base_path(self):
        """Base path for Week 1 materials."""
        return Path("aws-saa-study-materials/week1")
    
    @pytest.fixture
    def week1_days(self):
        """List of all Week 1 days."""
        return [1, 2, 3, 4, 5, 6, 7]
    
    def test_week1_folder_structure_exists(self, week1_base_path, week1_days):
        """Verify all Week 1 day folders exist with correct structure."""
        assert week1_base_path.exists(), f"Week 1 base path does not exist: {week1_base_path}"
        
        for day in week1_days:
            day_path = week1_base_path / f"day{day}"
            assert day_path.exists(), f"Day {day} folder does not exist"
            
            # Check for required folders
            required_folders = ["advanced", "hands-on-console"]
            for folder in required_folders:
                folder_path = day_path / folder
                assert folder_path.exists(), f"Day {day} missing {folder} folder"
    
    def test_week1_advanced_content_exists(self, week1_base_path, week1_days):
        """Verify all advanced content files exist for Week 1."""
        required_files = [
            "case-study.md",
            "best-practices.md",
            "troubleshooting.md"
        ]
        
        for day in week1_days:
            advanced_path = week1_base_path / f"day{day}" / "advanced"
            
            for file in required_files:
                file_path = advanced_path / file
                assert file_path.exists(), f"Day {day} missing {file}"
                
                # Verify file is not empty
                content = file_path.read_text(encoding='utf-8')
                assert len(content) > 100, f"Day {day} {file} appears to be empty or too short"
    
    def test_week1_architecture_diagrams_exist(self, week1_base_path, week1_days):
        """Verify architecture diagrams exist for all Week 1 days."""
        for day in week1_days:
            diagrams_path = week1_base_path / f"day{day}" / "advanced" / "architecture-diagrams"
            assert diagrams_path.exists(), f"Day {day} missing architecture-diagrams folder"
            
            # Check for at least one diagram file (.mmd or .md)
            diagram_files = list(diagrams_path.glob("*.mmd")) + list(diagrams_path.glob("*.md"))
            assert len(diagram_files) > 0, f"Day {day} has no diagram files"
    
    def test_week1_hands_on_console_content(self, week1_base_path, week1_days):
        """Verify hands-on console content exists for Week 1."""
        for day in week1_days:
            hands_on_path = week1_base_path / f"day{day}" / "hands-on-console"
            
            # Check README exists
            readme_path = hands_on_path / "README.md"
            assert readme_path.exists(), f"Day {day} missing hands-on-console README.md"
            
            # Check for exercise files
            exercise_files = list(hands_on_path.glob("exercise-*.md"))
            assert len(exercise_files) > 0, f"Day {day} has no exercise files"
    
    def test_week1_case_study_structure(self, week1_base_path, week1_days):
        """Verify case study files have required sections."""
        required_sections = [
            "사례 개요",
            "비즈니스 도전과제",
            "AWS 솔루션 아키텍처",
            "구현 세부사항",
            "비즈니스 임팩트"
        ]
        
        for day in week1_days:
            case_study_path = week1_base_path / f"day{day}" / "advanced" / "case-study.md"
            content = case_study_path.read_text(encoding='utf-8')
            
            for section in required_sections:
                assert section in content, f"Day {day} case-study.md missing section: {section}"
    
    def test_week1_best_practices_structure(self, week1_base_path, week1_days):
        """Verify best practices files have required sections."""
        required_sections = [
            "서비스 연계 패턴",
            "아키텍처 진화 경로",
            "비용 최적화 전략",
            "보안 베스트 프랙티스"
        ]
        
        for day in week1_days:
            bp_path = week1_base_path / f"day{day}" / "advanced" / "best-practices.md"
            content = bp_path.read_text(encoding='utf-8')
            
            for section in required_sections:
                assert section in content, f"Day {day} best-practices.md missing section: {section}"
    
    def test_week1_troubleshooting_structure(self, week1_base_path, week1_days):
        """Verify troubleshooting files have required sections."""
        required_sections = [
            "일반적인 문제 상황",
            "진단 단계",
            "해결 방법",
            "예방 조치"
        ]
        
        for day in week1_days:
            ts_path = week1_base_path / f"day{day}" / "advanced" / "troubleshooting.md"
            content = ts_path.read_text(encoding='utf-8')
            
            # At least some of these sections should be present
            found_sections = sum(1 for section in required_sections if section in content)
            assert found_sections >= 2, f"Day {day} troubleshooting.md missing most required sections"
    
    def test_week1_mermaid_diagrams_valid(self, week1_base_path, week1_days):
        """Verify Mermaid diagrams have valid syntax."""
        for day in week1_days:
            diagrams_path = week1_base_path / f"day{day}" / "advanced" / "architecture-diagrams"
            
            # Check both .mmd and .md files
            diagram_files = list(diagrams_path.glob("*.mmd")) + list(diagrams_path.glob("*.md"))
            
            for diagram_file in diagram_files:
                content = diagram_file.read_text(encoding='utf-8')
                
                # For .mmd files, the entire content is the diagram
                # For .md files, look for Mermaid code blocks
                if diagram_file.suffix == '.mmd':
                    # Check if content starts with ```mermaid or is raw mermaid
                    if content.strip().startswith('```mermaid'):
                        mermaid_blocks = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)
                    else:
                        # Raw mermaid content
                        mermaid_blocks = [content]
                else:
                    # .md files - extract mermaid blocks
                    mermaid_blocks = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)
                
                assert len(mermaid_blocks) > 0, f"{diagram_file.name} has no Mermaid diagrams"
                
                # Basic syntax validation
                for block in mermaid_blocks:
                    # Check for common diagram types
                    valid_types = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 'stateDiagram']
                    has_valid_type = any(diagram_type in block for diagram_type in valid_types)
                    assert has_valid_type, f"{diagram_file.name} has invalid Mermaid diagram type"
    
    def test_week1_prerequisites_links(self, week1_base_path, week1_days):
        """Verify hands-on README files link to prerequisites."""
        prerequisites_pattern = r'\[.*?\]\(.*?/resources/prerequisites/.*?\)'
        
        for day in week1_days:
            readme_path = week1_base_path / f"day{day}" / "hands-on-console" / "README.md"
            content = readme_path.read_text(encoding='utf-8')
            
            # Check for at least one prerequisites link
            prereq_links = re.findall(prerequisites_pattern, content)
            assert len(prereq_links) > 0, f"Day {day} hands-on README missing prerequisites links"
    
    def test_week1_cross_day_references(self, week1_base_path, week1_days):
        """Verify case studies reference other days appropriately."""
        for day in week1_days:
            case_study_path = week1_base_path / f"day{day}" / "advanced" / "case-study.md"
            content = case_study_path.read_text(encoding='utf-8')
            
            # Check for "Day" references (indicating cross-day connections)
            day_references = re.findall(r'Day \d+', content)
            
            # Most days should reference other days (except maybe Day 1)
            if day > 1:
                assert len(day_references) > 0, f"Day {day} case-study.md has no cross-day references"
    
    def test_week1_aws_service_mentions(self, week1_base_path, week1_days):
        """Verify content mentions relevant AWS services."""
        # Expected primary services for each day
        expected_services = {
            1: ["Region", "Availability Zone", "CloudFront"],
            2: ["IAM", "User", "Role", "Policy"],
            3: ["EC2", "Instance"],
            4: ["Auto Scaling", "Load Balancer"],
            5: ["VPC", "Subnet"],
            6: ["NAT Gateway", "VPC Peering"],
            7: ["CloudWatch"]
        }
        
        for day in week1_days:
            case_study_path = week1_base_path / f"day{day}" / "advanced" / "case-study.md"
            content = case_study_path.read_text(encoding='utf-8')
            
            # Check for at least one expected service
            services = expected_services.get(day, [])
            found_service = any(service in content for service in services)
            assert found_service, f"Day {day} case-study.md missing expected AWS services: {services}"
    
    def test_week1_console_paths_format(self, week1_base_path, week1_days):
        """Verify console paths are properly formatted."""
        console_path_pattern = r'Console 경로:|Services\s*>\s*\w+'
        
        for day in week1_days:
            # Check in hands-on exercises
            hands_on_path = week1_base_path / f"day{day}" / "hands-on-console"
            
            for exercise_file in hands_on_path.glob("exercise-*.md"):
                content = exercise_file.read_text(encoding='utf-8')
                
                # Should have console path references
                console_paths = re.findall(console_path_pattern, content)
                assert len(console_paths) > 0, f"{exercise_file.name} missing console path references"
    
    def test_week1_resource_cleanup_sections(self, week1_base_path, week1_days):
        """Verify hands-on exercises include resource cleanup sections."""
        cleanup_keywords = ["리소스 정리", "삭제", "정리", "cleanup", "delete"]
        
        for day in week1_days:
            readme_path = week1_base_path / f"day{day}" / "hands-on-console" / "README.md"
            content = readme_path.read_text(encoding='utf-8').lower()
            
            # Check for cleanup-related content
            has_cleanup = any(keyword in content for keyword in cleanup_keywords)
            assert has_cleanup, f"Day {day} hands-on README missing resource cleanup section"
    
    def test_week1_content_completeness_summary(self, week1_base_path, week1_days):
        """Generate a summary of Week 1 content completeness."""
        summary = {
            "total_days": len(week1_days),
            "case_studies": 0,
            "best_practices": 0,
            "troubleshooting": 0,
            "diagrams": 0,
            "exercises": 0
        }
        
        for day in week1_days:
            day_path = week1_base_path / f"day{day}"
            
            # Count files
            if (day_path / "advanced" / "case-study.md").exists():
                summary["case_studies"] += 1
            if (day_path / "advanced" / "best-practices.md").exists():
                summary["best_practices"] += 1
            if (day_path / "advanced" / "troubleshooting.md").exists():
                summary["troubleshooting"] += 1
            
            diagrams_path = day_path / "advanced" / "architecture-diagrams"
            if diagrams_path.exists():
                # Count both .mmd and .md files
                diagram_count = len(list(diagrams_path.glob("*.mmd"))) + len(list(diagrams_path.glob("*.md")))
                summary["diagrams"] += diagram_count
            
            hands_on_path = day_path / "hands-on-console"
            if hands_on_path.exists():
                summary["exercises"] += len(list(hands_on_path.glob("exercise-*.md")))
        
        # Verify completeness
        assert summary["case_studies"] == len(week1_days), "Not all days have case studies"
        assert summary["best_practices"] == len(week1_days), "Not all days have best practices"
        assert summary["troubleshooting"] == len(week1_days), "Not all days have troubleshooting"
        assert summary["diagrams"] >= len(week1_days), "Insufficient diagrams for Week 1"
        assert summary["exercises"] >= len(week1_days), "Insufficient exercises for Week 1"
        
        print(f"\n✅ Week 1 Content Summary:")
        print(f"   - Days: {summary['total_days']}")
        print(f"   - Case Studies: {summary['case_studies']}")
        print(f"   - Best Practices: {summary['best_practices']}")
        print(f"   - Troubleshooting: {summary['troubleshooting']}")
        print(f"   - Diagrams: {summary['diagrams']}")
        print(f"   - Exercises: {summary['exercises']}")


class TestComponentIntegration:
    """Test integration between different components."""
    
    def test_daily_topics_integration(self):
        """Verify daily topics configuration is accessible."""
        from src.daily_topics import DAILY_TOPICS
        
        # Check Week 1 days are defined
        for day in range(1, 8):
            assert day in DAILY_TOPICS, f"Day {day} not defined in DAILY_TOPICS"
            
            # Verify required fields
            day_config = DAILY_TOPICS[day]
            assert "title" in day_config, f"Day {day} missing title"
            assert "primary_services" in day_config, f"Day {day} missing primary_services"
    
    def test_cross_service_integration_data(self):
        """Verify cross-service integration data is available."""
        from src.cross_service_integration import CROSS_DAY_INTEGRATIONS
        
        # Should have integration scenarios defined
        assert len(CROSS_DAY_INTEGRATIONS) > 0, "No cross-day integrations defined"
        
        # Verify structure
        for integration_id, integration in CROSS_DAY_INTEGRATIONS.items():
            assert "name" in integration, f"Integration {integration_id} missing name"
            assert "primary_days" in integration, f"Integration {integration_id} missing primary_days"
    
    def test_generators_importable(self):
        """Verify all generator modules can be imported."""
        generators = [
            "case_study_generator",
            "best_practices_generator",
            "troubleshooting_generator",
            "architecture_diagram_generator",
            "exercise_guide_generator",
            "aws_docs_link_generator",
            "content_validator"
        ]
        
        for generator in generators:
            try:
                __import__(f"src.generators.{generator}")
            except ImportError as e:
                pytest.fail(f"Failed to import {generator}: {e}")
    
    def test_prerequisites_documents_exist(self):
        """Verify prerequisites documents are in place."""
        prereq_path = Path("aws-saa-study-materials/resources/prerequisites")
        
        required_docs = [
            "aws-account-setup.md",
            "iam-user-setup.md",
            "cli-configuration.md",
            "console-navigation.md"
        ]
        
        for doc in required_docs:
            doc_path = prereq_path / doc
            assert doc_path.exists(), f"Prerequisites document missing: {doc}"
            
            # Verify not empty
            content = doc_path.read_text(encoding='utf-8')
            assert len(content) > 100, f"Prerequisites document too short: {doc}"
    
    def test_integration_scenarios_exist(self):
        """Verify integration scenario documents exist."""
        scenarios_path = Path("aws-saa-study-materials/integration-scenarios")
        
        if scenarios_path.exists():
            scenario_files = list(scenarios_path.glob("*.md"))
            assert len(scenario_files) > 0, "No integration scenario files found"
            
            # Verify README exists
            readme_path = scenarios_path / "README.md"
            assert readme_path.exists(), "Integration scenarios README missing"


class TestWorkflowValidation:
    """Test the complete workflow from generation to validation."""
    
    def test_content_generation_workflow(self, tmp_path):
        """Test that content can be generated programmatically."""
        from src.generators.case_study_generator import CaseStudyGenerator
        from src.daily_topics import DAILY_TOPICS
        
        # Test generating content for Day 1
        generator = CaseStudyGenerator()
        day_config = DAILY_TOPICS[1]
        
        # This should not raise an exception
        try:
            # Use correct method signature: generate_case_study(day_number, output_path)
            content = generator.generate_case_study(
                day_number=1,
                output_path=None  # Will use default path
            )
            assert len(content) > 0, "Generated content is empty"
        except Exception as e:
            pytest.fail(f"Content generation failed: {e}")
    
    def test_validation_workflow(self):
        """Test that content validation works."""
        from src.generators.content_validator import ContentValidator
        
        validator = ContentValidator()
        
        # Test validating an existing file
        test_file = Path("aws-saa-study-materials/week1/day1/advanced/case-study.md")
        if test_file.exists():
            content = test_file.read_text(encoding='utf-8')
            
            # Should not raise validation errors
            try:
                is_valid = validator.validate_case_study_content(content)
                assert is_valid, "Validation failed for existing content"
            except Exception as e:
                pytest.fail(f"Validation workflow failed: {e}")
