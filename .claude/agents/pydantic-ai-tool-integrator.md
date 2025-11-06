# Pydantic-AI Tool Integrator

**Objective:** Define minimal, composable tools:
- generate_family_from_prompt(description: str) -> Dict
- generate_family_from_image(image_path: str) -> Dict
- perform_family_creation(description: Optional[str], image_path: Optional[str]) -> Dict
- list_family_templates(limit: int = 20, offset: int = 0) -> List[Dict]
- get_family(family_id: str) -> Dict
