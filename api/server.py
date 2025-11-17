import os
import json
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from .models import (
    EvaluateRequest,
    AvaliacoesResponse,
    Avaliacao,
    Candidato,
    SelfTextRequest,
    EvaluateSelfRequest,
    Vaga,
    JobTextRequest,
    EvaluateTextsRequest,
)
from .services.ollama_client import generate_json, OllamaError
from .services.pdf_reader import extract_text_from_pdf_bytes

APP_NAME = os.getenv("APP_NAME", "GS-JobFitScore API")
APP_VERSION = "1.0.0"
USE_MODEL_DEFAULT = os.getenv("USE_MODEL", "true").lower() in ("1", "true", "yes")

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="API de avaliação de compatibilidade candidato-vaga usando IA (Ollama)",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
def root():
    """Informações básicas da API."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "online",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "evaluate": "POST /evaluate - Avalia candidatos vs vaga",
            "extract_resume": "POST /extract-resume - Extrai currículo PDF",
            "extract_self": "POST /extract-self - Extrai candidato de texto",
            "extract_job": "POST /extract-job - Extrai vaga de texto",
            "evaluate_self": "POST /evaluate-self - Avalia auto-descrição vs vaga",
            "evaluate_texts": "POST /evaluate-texts - Avalia textos livres",
        },
    }


@app.get("/health")
def health():
    """Verifica status e configurações da API."""
    return {
        "status": "ok",
        "version": APP_VERSION,
        "use_model_default": USE_MODEL_DEFAULT,
        "ollama_model": os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        "ollama_url": os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate"),
        "cors_enabled": True,
    }


def _fallback_score(vaga_requisitos: List[str], cand: Candidato) -> Avaliacao:
    req = {r.lower().strip() for r in vaga_requisitos}
    hab = {h.lower().strip() for h in (cand.habilidades or [])}
    cursos = {c.lower().strip() for c in (cand.cursos or [])}

    match = len(req & hab)
    cobertura = match / max(len(req), 1)

    bonus_cursos = len(req & cursos) * 0.05  # 5% por curso relevante
    penalidade_faltas = (len(req - hab)) * 0.04  # 4% por requisito ausente

    base = cobertura * 100
    score = max(0, min(100, round(base + bonus_cursos * 100 - penalidade_faltas * 100)))

    faltantes = ", ".join(sorted(req - hab))
    presentes = ", ".join(sorted(req & hab))
    feedback = (
        f"Habilidades presentes: {presentes or 'nenhuma'}. "
        f"Faltando: {faltantes or 'nenhuma'}. "
        f"Cursos relacionados: {len(req & cursos)}."
    )
    return Avaliacao(nome=cand.nome, score=score, feedback=feedback)


@app.post("/evaluate", response_model=AvaliacoesResponse)
def evaluate(payload: EvaluateRequest):
    """Avalia candidatos contra a vaga. Usa modelo (Ollama) se disponível, senão fallback local."""
    use_model = (
        payload.use_model if payload.use_model is not None else USE_MODEL_DEFAULT
    )

    prompt = (
        "Você é um avaliador técnico de compatibilidade entre candidatos e vagas de emprego.\n\n"
        "Analise os dados abaixo em formato JSON. Compare as habilidades, experiências e cursos dos candidatos"
        " com os requisitos da vaga.\n\nRetorne APENAS o JSON no seguinte formato:\n\n"
        '{\n  "avaliacoes": [\n    {\n      "nome": "Nome do candidato",\n      "score": numero,\n      "feedback": "breve explicação"\n    }\n  ]\n}\n\n'
        "Use os seguintes critérios:\n- + pontos para cada habilidade que coincidir\n- Considere experiência e cursos relacionados\n"
        "- Diminua pontos se faltar tecnologias essenciais\n- Score final de 0 a 100\n\nDados:\n"
        + json.dumps(payload.model_dump(), ensure_ascii=False)
    )

    if use_model:
        try:
            result = generate_json(prompt)
            # valida e normaliza
            avals = result.get("avaliacoes")
            if not isinstance(avals, list):
                raise OllamaError("Resposta do modelo não contém lista 'avaliacoes'.")
            avaliacoes = []
            for a in avals:
                try:
                    nome = str(a.get("nome", "")).strip()
                    score = int(round(float(a.get("score", 0))))
                    feedback = str(a.get("feedback", "")).strip()
                    score = max(0, min(100, score))
                    if not nome:
                        continue
                    avaliacoes.append(
                        Avaliacao(nome=nome, score=score, feedback=feedback)
                    )
                except Exception:
                    continue
            if not avaliacoes:
                raise OllamaError("Modelo retornou avaliações vazias.")
            return AvaliacoesResponse(avaliacoes=avaliacoes)
        except OllamaError:
            # fallback automático
            pass
        except Exception as e:
            # fallback em erro inesperado
            pass

    # Fallback local determinístico
    avaliacoes_fb = [
        _fallback_score(payload.vaga.requisitos, c) for c in payload.candidatos
    ]
    return AvaliacoesResponse(avaliacoes=avaliacoes_fb)


@app.post("/extract-resume")
def extract_resume(file: UploadFile = File(...)):
    """Recebe um PDF e retorna um candidato estruturado extraído via IA, com fallback simples."""
    if (file.content_type or "").lower() not in (
        "application/pdf",
        "application/octet-stream",
    ):
        raise HTTPException(status_code=400, detail="Envie um arquivo PDF.")

    content = file.file.read()
    text = extract_text_from_pdf_bytes(content)
    if not text:
        raise HTTPException(
            status_code=400, detail="Não foi possível extrair texto do PDF."
        )

    prompt = f"""
Analise o currículo abaixo e extraia as seguintes informações em JSON:
{{
  "nome": "nome completo",
  "habilidades": ["lista", "de", "habilidades"],
  "experiencia": "resumo breve",
  "cursos": ["lista", "de", "cursos"]
}}
IMPORTANTE: Retorne APENAS o JSON, sem markdown ou explicações.

Currículo:
{text}
"""
    try:
        data = generate_json(prompt)
        # validação mínima
        nome = str(data.get("nome", "")).strip()
        habilidades = [str(x) for x in data.get("habilidades", [])]
        experiencia = str(data.get("experiencia", "")).strip()
        cursos = [str(x) for x in data.get("cursos", [])]
        if not nome:
            raise ValueError("Nome vazio")
        return {
            "nome": nome,
            "habilidades": habilidades,
            "experiencia": experiencia,
            "cursos": cursos,
        }
    except Exception:
        # fallback muito simples
        first_line = text.splitlines()[0:3]
        nome_guess = " ".join(" ".join(first_line).split()[:4])
        return {
            "nome": nome_guess or "Candidato",
            "habilidades": [],
            "experiencia": "",
            "cursos": [],
            "observacao": "Fallback sem IA: preencha manualmente habilidades/cursos.",
        }


@app.post("/extract-self", response_model=Candidato)
def extract_self(req: SelfTextRequest):
    """Recebe um texto de auto-descrição e retorna um Candidato estruturado."""
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Campo 'text' é obrigatório.")

    prompt = f"""
Analise a auto-descrição abaixo e extraia as seguintes informações em JSON:
{{
  "nome": "nome completo",
  "habilidades": ["lista", "de", "habilidades"],
  "experiencia": "resumo breve",
  "cursos": ["lista", "de", "cursos"]
}}
IMPORTANTE: Retorne APENAS o JSON, sem markdown ou explicações.

Auto-descrição:
{text}
"""
    use_model = req.use_model if req.use_model is not None else USE_MODEL_DEFAULT
    try:
        if use_model:
            data = generate_json(prompt)
        else:
            raise OllamaError("IA desativada por solicitação.")
        nome = str(data.get("nome", "")).strip()
        habilidades = [str(x) for x in data.get("habilidades", [])]
        experiencia = str(data.get("experiencia", "")).strip()
        cursos = [str(x) for x in data.get("cursos", [])]
        if not nome:
            raise ValueError("Nome vazio")
        return Candidato(
            nome=nome, habilidades=habilidades, experiencia=experiencia, cursos=cursos
        )
    except Exception:
        # Fallback simples: usa primeiras palavras como nome e o restante como experiencia
        tokens = text.split()
        nome_guess = " ".join(tokens[:4])
        return Candidato(
            nome=nome_guess or "Candidato",
            habilidades=[],
            experiencia=text[:200],
            cursos=[],
        )


@app.post("/evaluate-self", response_model=AvaliacoesResponse)
def evaluate_self(req: EvaluateSelfRequest):
    """Extrai o candidato de uma auto-descrição e avalia contra a vaga."""
    # Extrai candidato
    cand = extract_self(SelfTextRequest(text=req.self_text, use_model=req.use_model))
    # Avalia candidato
    eval_req = EvaluateRequest(
        vaga=req.vaga, candidatos=[cand], use_model=req.use_model
    )
    return evaluate(eval_req)


@app.post("/extract-job", response_model=Vaga)
def extract_job(req: JobTextRequest):
    """Recebe descrição de vaga em texto livre e retorna Vaga estruturada."""
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Campo 'text' é obrigatório.")

    prompt = f"""
Analise a descrição da vaga abaixo e extraia as seguintes informações em JSON:
{{
  "titulo": "título da vaga",
  "empresa": "nome da empresa",
  "requisitos": ["lista", "de", "requisitos", "técnicos"],
  "descricao": "resumo breve da vaga"
}}
IMPORTANTE: Retorne APENAS o JSON, sem markdown ou explicações.

Descrição da vaga:
{text}
"""
    use_model = req.use_model if req.use_model is not None else USE_MODEL_DEFAULT
    try:
        if use_model:
            data = generate_json(prompt)
        else:
            raise OllamaError("IA desativada por solicitação.")
        titulo = str(data.get("titulo", "")).strip()
        empresa = str(data.get("empresa", "")).strip() or None
        requisitos = [str(x) for x in data.get("requisitos", [])]
        descricao = str(data.get("descricao", "")).strip() or None
        if not titulo:
            raise ValueError("Título vazio")
        return Vaga(
            titulo=titulo, empresa=empresa, requisitos=requisitos, descricao=descricao
        )
    except Exception:
        # Fallback simples: usa primeiras palavras como título
        tokens = text.split()
        titulo_guess = " ".join(tokens[:6])
        return Vaga(
            titulo=titulo_guess or "Vaga",
            empresa=None,
            requisitos=[],
            descricao=text[:200],
        )


@app.post("/evaluate-texts", response_model=AvaliacoesResponse)
def evaluate_texts(req: EvaluateTextsRequest):
    """Recebe job_text + self_text e retorna avaliação completa (extrai vaga e candidato via IA)."""
    # Extrai vaga
    vaga = extract_job(JobTextRequest(text=req.job_text, use_model=req.use_model))
    # Extrai candidato
    cand = extract_self(SelfTextRequest(text=req.self_text, use_model=req.use_model))
    # Avalia
    eval_req = EvaluateRequest(vaga=vaga, candidatos=[cand], use_model=req.use_model)
    return evaluate(eval_req)
