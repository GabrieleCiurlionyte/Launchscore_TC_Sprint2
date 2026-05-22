from pydantic import BaseModel, Field, field_validator, model_validator


class IdeaInput(BaseModel):
    one_sentence_pitch: str
    problem_solved: str
    target_users: str
    target_countries: list[str] = Field(default_factory=list)

    @field_validator("one_sentence_pitch", "problem_solved", "target_users")
    @classmethod
    def required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field is required.")
        return value

    @model_validator(mode="after")
    def validate_lengths(self):
        if len(self.one_sentence_pitch) < 10:
            raise ValueError("Please provide a more descriptive one-sentence pitch.")
        if len(self.problem_solved) < 15:
            raise ValueError("Please describe the problem in a bit more detail.")
        return self
