#!/usr/bin/env python3
"""
LangGraph Template Deployment Script
===================================

Deploy the complete LangGraph multi-agent template to your project directory.

Usage:
    python copy_template.py /path/to/target/directory

This script copies the entire LangGraph template structure including:
- LangGraph-specific CLAUDE.md global rules
- Specialized PRP generation and execution commands  
- Progressive examples (basic to production-ready)
- AI documentation and architectural patterns
- All supporting files and configurations

The copied template will be immediately ready for multi-agent development.
"""

import os
import sys
import shutil
from pathlib import Path
import argparse
from datetime import datetime

class LangGraphTemplateDeployer:
    """Deploy LangGraph multi-agent template to target directory."""
    
    def __init__(self, source_dir: Path = None):
        self.source_dir = source_dir or Path(__file__).parent
        self.required_files = [
            "CLAUDE.md",
            ".claude/commands/generate-langgraph-prp.md",
            ".claude/commands/execute-langgraph-prp.md", 
            "PRPs/templates/prp_langgraph_base.md",
            "PRPs/INITIAL.md",
            "README.md"
        ]
        
    def validate_source(self) -> bool:
        """Validate that source directory has required template files."""
        print("🔍 Validating LangGraph template source...")
        
        missing_files = []
        for file_path in self.required_files:
            full_path = self.source_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ Missing required template files:")
            for file in missing_files:
                print(f"   - {file}")
            return False
            
        print("✅ All required LangGraph template files found")
        return True
    
    def create_target_structure(self, target_dir: Path) -> bool:
        """Create target directory structure."""
        print(f"📁 Creating LangGraph project structure in {target_dir}")
        
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            subdirs = [
                ".claude/commands",
                "PRPs/templates",
                "PRPs/ai_docs", 
                "PRPs/examples/basic_react_agent",
                "PRPs/examples/multi_agent_supervisor",
                "PRPs/examples/parallel_research_agents",
                "PRPs/examples/human_in_loop_agent",
            ]
            
            for subdir in subdirs:
                (target_dir / subdir).mkdir(parents=True, exist_ok=True)
            
            print(f"✅ Created directory structure with {len(subdirs)} subdirectories")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create directory structure: {e}")
            return False
    
    def copy_template_files(self, target_dir: Path) -> bool:
        """Copy all template files to target directory."""
        print("📋 Copying LangGraph template files...")
        
        try:
            copied_files = 0
            skipped_files = 0
            
            # Copy all files recursively, excluding __pycache__ and .pyc files
            for item in self.source_dir.rglob("*"):
                if item.is_file() and not self._should_exclude(item):
                    
                    # Calculate relative path from source
                    rel_path = item.relative_to(self.source_dir)
                    
                    # Special handling: rename README.md to README_TEMPLATE.md
                    if rel_path.name == "README.md":
                        target_file = target_dir / rel_path.parent / "README_TEMPLATE.md"
                        display_path = rel_path.parent / "README_TEMPLATE.md"
                    else:
                        target_file = target_dir / rel_path
                        display_path = rel_path
                    
                    # Create parent directory if needed
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    if not target_file.exists() or self._should_overwrite(rel_path):
                        shutil.copy2(item, target_file)
                        copied_files += 1
                        print(f"   ✅ {display_path}")
                    else:
                        skipped_files += 1
                        print(f"   ⏭️  {display_path} (exists, skipped)")
            
            print(f"📄 Copied {copied_files} files, skipped {skipped_files} existing files")
            return True
            
        except Exception as e:
            print(f"❌ Failed to copy template files: {e}")
            return False
    
    def _should_exclude(self, file_path: Path) -> bool:
        """Check if file should be excluded from copying."""
        exclude_patterns = [
            "__pycache__",
            ".pyc",
            ".git",
            ".DS_Store",
            "copy_template.py"  # Don't copy the deployment script itself
        ]
        
        return any(pattern in str(file_path) for pattern in exclude_patterns)
    
    def _should_overwrite(self, rel_path: Path) -> bool:
        """Check if existing file should be overwritten."""
        # Always overwrite template files to ensure latest version
        overwrite_patterns = [
            "CLAUDE.md",
            ".claude/commands/", 
            "PRPs/templates/",
            "PRPs/ai_docs/",
            "examples/",
            "README.md"
        ]
        
        return any(str(rel_path).startswith(pattern) for pattern in overwrite_patterns)
        
        # Create basic gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Jupyter
.ipynb_checkpoints

# Database
*.db
*.sqlite3

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# LangGraph specific
checkpoints/
graph_visualizations/
"""
        
        try:
            gitignore_file = target_dir / ".gitignore"
            with open(gitignore_file, "w") as f:
                f.write(gitignore_content)
            print("✅ Created project structure files")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create project files: {e}")
            return False
    
    def print_success_message(self, target_dir: Path):
        """Print success message with next steps."""
        print("\n" + "="*70)
        print("🎉 LangGraph Multi-Agent Template Deployed Successfully!")
        print("="*70)
        print(f"📍 Location: {target_dir.absolute()}")
        print()
        print("🚀 Next Steps:")
        print()
        print("1. Navigate to your new project:")
        print(f"   cd {target_dir}")
        print()
        print("2. Set up Python environment:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print()
        print("3. Install dependencies:")
        print("   pip install -r requirements.txt")
        print()
        print("4. Configure environment:")
        print("   cp .env.example .env")
        print("   # Edit .env with your API keys")
        print()
        print("5. Start building your multi-agent system:")
        print("   /generate-langgraph-prp PRPs/INITIAL.md")
        print()
        print("📚 Template Contents:")
        print("   • CLAUDE.md - LangGraph-specific global rules")
        print("   • .claude/commands/ - Specialized PRP generation commands")
        print("   • PRPs/templates/ - LangGraph base PRP template")
        print("   • examples/ - Progressive examples (basic → production)")
        print("   • PRPs/ai_docs/ - Comprehensive LangGraph documentation")
        print("   • README_TEMPLATE.md - Template documentation and usage guide")
        print()
        print("🎯 Ready for sophisticated multi-agent development!")
        print("="*70)
    
    def deploy(self, target_path: str) -> bool:
        """Main deployment method."""
        print("🚀 LangGraph Multi-Agent Template Deployment")
        print("=" * 60)
        
        target_dir = Path(target_path).resolve()
        
        # Validate source
        if not self.validate_source():
            return False
        
        # Create structure
        if not self.create_target_structure(target_dir):
            return False
        
        # Copy files
        if not self.copy_template_files(target_dir):
            return False
        
        # Success message
        self.print_success_message(target_dir)
        return True

def main():
    """Main entry point for template deployment."""
    parser = argparse.ArgumentParser(
        description="Deploy LangGraph Multi-Agent Template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python copy_template.py /path/to/my/project
  python copy_template.py ../my-langgraph-app
  python copy_template.py /home/user/langgraph-project

This will create a complete LangGraph multi-agent development environment
with all necessary files, examples, and documentation.
        """
    )
    
    parser.add_argument(
        "target_directory",
        help="Target directory where the LangGraph template will be deployed"
    )
    
    parser.add_argument(
        "--version",
        action="version", 
        version="LangGraph Template Deployer v1.0.0"
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    # Deploy template
    deployer = LangGraphTemplateDeployer()
    success = deployer.deploy(args.target_directory)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()