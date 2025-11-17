from typing import List, Optional
from pydantic import BaseModel, Field


class Vaga(BaseModel):
    titulo: str
    empresa: Optional[str] = None
    requisitos: List[str] = Field(default_factory=list)
    descricao: Optional[str] = None


class Candidato(BaseModel):
    nome: str
    habilidades: List[str] = Field(default_factory=list)
    experiencia: Optional[str] = None
    cursos: List[str] = Field(default_factory=list)


class Avaliacao(BaseModel):
    nome: str
    score: int
    feedback: str


class AvaliacoesResponse(BaseModel):
    avaliacoes: List[Avaliacao]


class EvaluateRequest(BaseModel):
    vaga: Vaga
    candidatos: List[Candidato]
    use_model: Optional[bool] = True


class SelfTextRequest(BaseModel):
    text: str
    use_model: Optional[bool] = True


class EvaluateSelfRequest(BaseModel):
    vaga: Vaga
    self_text: str
    use_model: Optional[bool] = True


class JobTextRequest(BaseModel):
    text: str
    use_model: Optional[bool] = True


class EvaluateTextsRequest(BaseModel):
    job_text: str
    self_text: str
    use_model: Optional[bool] = True
