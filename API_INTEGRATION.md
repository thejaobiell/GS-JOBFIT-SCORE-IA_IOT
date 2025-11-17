# 🔌 API de IA - Documentação para Integração com Java

## 📋 Visão Geral

API REST desenvolvida em FastAPI para avaliação de compatibilidade entre candidatos e vagas usando IA (Ollama) com fallback determinístico.

**Base URL Local:** `http://localhost:8000`

---

## 🚀 Iniciando a API

### Windows (PowerShell)
```powershell
.\run_api.ps1
```

### Parar a API
```powershell
.\stop_api.ps1
```

---

## 📡 Endpoints Disponíveis

### 1. Health Check
Verifica o status da API e configurações.

```http
GET /health
```

**Resposta (200 OK):**
```json
{
  "status": "ok",
  "use_model_default": true,
  "ollama_model": "llama3.2:3b",
  "ollama_url": "http://127.0.0.1:11434/api/generate"
}
```

---

### 2. Avaliar Candidatos vs Vaga
Avalia múltiplos candidatos contra uma vaga específica.

```http
POST /evaluate
Content-Type: application/json
```

**Request Body:**
```json
{
  "vaga": {
    "titulo": "Desenvolvedor Java Sênior",
    "empresa": "Tech Corp",
    "requisitos": ["Java", "Spring Boot", "PostgreSQL", "Docker"],
    "descricao": "Desenvolvedor experiente para projetos enterprise"
  },
  "candidatos": [
    {
      "nome": "João Silva",
      "habilidades": ["Java", "Spring Boot", "MySQL", "Git"],
      "experiencia": "5 anos desenvolvendo aplicações enterprise",
      "cursos": ["Certificação Java", "Spring Framework"]
    },
    {
      "nome": "Maria Santos",
      "habilidades": ["Java", "Spring Boot", "PostgreSQL", "Docker", "Kubernetes"],
      "experiencia": "8 anos em desenvolvimento backend",
      "cursos": ["Java Advanced", "Microservices Architecture"]
    }
  ],
  "use_model": true
}
```

**Resposta (200 OK):**
```json
{
  "avaliacoes": [
    {
      "nome": "João Silva",
      "score": 75,
      "feedback": "Habilidades presentes: Java, Spring Boot. Faltando: PostgreSQL, Docker. Cursos relacionados: 2."
    },
    {
      "nome": "Maria Santos",
      "score": 95,
      "feedback": "Habilidades presentes: Java, Spring Boot, PostgreSQL, Docker. Faltando: nenhuma. Cursos relacionados: 2."
    }
  ]
}
```

---

### 3. Extrair Informações de Currículo PDF
Processa um PDF e extrai informações estruturadas do candidato.

```http
POST /extract-resume
Content-Type: multipart/form-data
```

**Parâmetros:**
- `file`: Arquivo PDF do currículo

**Resposta (200 OK):**
```json
{
  "nome": "João Gabriel Boaventura",
  "habilidades": ["Java", "Spring Boot", "PostgreSQL", "Docker", "Git"],
  "experiencia": "3 anos como desenvolvedor full-stack, focado em backend Java",
  "cursos": ["Análise e Desenvolvimento de Sistemas", "Spring Boot Avançado"]
}
```

---

### 4. Extrair Candidato de Texto
Converte texto de auto-descrição em estrutura de candidato.

```http
POST /extract-self
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Meu nome é Pedro Costa, tenho 5 anos de experiência com Java, Spring Boot e PostgreSQL. Fiz curso de Java Avançado na FIAP e certificação Oracle.",
  "use_model": true
}
```

**Resposta (200 OK):**
```json
{
  "nome": "Pedro Costa",
  "habilidades": ["Java", "Spring Boot", "PostgreSQL"],
  "experiencia": "5 anos de experiência com desenvolvimento backend",
  "cursos": ["Java Avançado", "Certificação Oracle"]
}
```

---

### 5. Extrair Vaga de Texto
Converte descrição textual em estrutura de vaga.

```http
POST /extract-job
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "Procuramos Desenvolvedor Java Sênior na XYZ Tech. Requisitos: Java 17+, Spring Boot 3.x, PostgreSQL, Docker, Kubernetes. Experiência mínima de 5 anos.",
  "use_model": true
}
```

**Resposta (200 OK):**
```json
{
  "titulo": "Desenvolvedor Java Sênior",
  "empresa": "XYZ Tech",
  "requisitos": ["Java 17+", "Spring Boot 3.x", "PostgreSQL", "Docker", "Kubernetes"],
  "descricao": "Experiência mínima de 5 anos em desenvolvimento backend"
}
```

---

### 6. Avaliar Auto-Descrição vs Vaga
Extrai candidato de texto e avalia contra vaga.

```http
POST /evaluate-self
Content-Type: application/json
```

**Request Body:**
```json
{
  "vaga": {
    "titulo": "Desenvolvedor Java",
    "requisitos": ["Java", "Spring Boot", "PostgreSQL"]
  },
  "self_text": "Sou João, programador Java há 3 anos, trabalho com Spring Boot e MySQL",
  "use_model": true
}
```

**Resposta (200 OK):**
```json
{
  "avaliacoes": [
    {
      "nome": "João",
      "score": 80,
      "feedback": "Forte experiência em Java e Spring Boot. PostgreSQL seria um diferencial."
    }
  ]
}
```

---

### 7. Avaliar Textos (Vaga + Candidato)
Extrai vaga e candidato de textos livres e avalia compatibilidade.

```http
POST /evaluate-texts
Content-Type: application/json
```

**Request Body:**
```json
{
  "job_text": "Vaga: Desenvolvedor Java na ABC Corp. Requisitos: Java, Spring Boot, PostgreSQL, Docker",
  "self_text": "João Silva, 5 anos de Java, Spring Boot, MySQL e Git",
  "use_model": true
}
```

**Resposta (200 OK):**
```json
{
  "avaliacoes": [
    {
      "nome": "João Silva",
      "score": 75,
      "feedback": "Boa compatibilidade. Considere aprender PostgreSQL e Docker."
    }
  ]
}
```

---

## 🔧 Modelos de Dados

### Vaga
```json
{
  "titulo": "string (obrigatório)",
  "empresa": "string (opcional)",
  "requisitos": ["array de strings"],
  "descricao": "string (opcional)"
}
```

### Candidato
```json
{
  "nome": "string (obrigatório)",
  "habilidades": ["array de strings"],
  "experiencia": "string (opcional)",
  "cursos": ["array de strings"]
}
```

### Avaliacao
```json
{
  "nome": "string",
  "score": "integer (0-100)",
  "feedback": "string"
}
```

---

## ☕ Exemplo de Integração com Java (Spring Boot)

### 1. Adicionar Dependência (Maven)

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

### 2. Criar DTOs

```java
package com.gs.fiap.jobfitscore.domain.ia.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class VagaIADTO {
    private String titulo;
    private String empresa;
    private List<String> requisitos;
    private String descricao;
}

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CandidatoIADTO {
    private String nome;
    private List<String> habilidades;
    private String experiencia;
    private List<String> cursos;
}

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AvaliacaoDTO {
    private String nome;
    private Integer score;
    private String feedback;
}

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AvaliacoesResponseDTO {
    private List<AvaliacaoDTO> avaliacoes;
}

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EvaluateRequestDTO {
    private VagaIADTO vaga;
    private List<CandidatoIADTO> candidatos;
    
    @JsonProperty("use_model")
    private Boolean useModel = true;
}

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExtractSelfRequestDTO {
    private String text;
    
    @JsonProperty("use_model")
    private Boolean useModel = true;
}

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExtractJobRequestDTO {
    private String text;
    
    @JsonProperty("use_model")
    private Boolean useModel = true;
}

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EvaluateTextsRequestDTO {
    @JsonProperty("job_text")
    private String jobText;
    
    @JsonProperty("self_text")
    private String selfText;
    
    @JsonProperty("use_model")
    private Boolean useModel = true;
}
```

### 3. Criar Cliente da API

```java
package com.gs.fiap.jobfitscore.domain.ia.client;

import com.gs.fiap.jobfitscore.domain.ia.dto.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.Duration;

@Slf4j
@Component
public class IAClient {

    private final WebClient webClient;

    public IAClient(@Value("${ia.api.base-url:http://localhost:8000}") String baseUrl) {
        this.webClient = WebClient.builder()
                .baseUrl(baseUrl)
                .defaultHeader("Content-Type", "application/json")
                .build();
    }

    /**
     * Verifica o status da API de IA
     */
    public Mono<Boolean> checkHealth() {
        return webClient.get()
                .uri("/health")
                .retrieve()
                .onStatus(HttpStatus::isError, response -> Mono.error(
                        new RuntimeException("API de IA indisponível")))
                .bodyToMono(String.class)
                .map(response -> true)
                .timeout(Duration.ofSeconds(5))
                .onErrorReturn(false);
    }

    /**
     * Avalia candidatos contra uma vaga
     */
    public Mono<AvaliacoesResponseDTO> evaluate(EvaluateRequestDTO request) {
        log.info("Avaliando {} candidatos para vaga: {}", 
                request.getCandidatos().size(), request.getVaga().getTitulo());
        
        return webClient.post()
                .uri("/evaluate")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(AvaliacoesResponseDTO.class)
                .timeout(Duration.ofMinutes(3))
                .doOnSuccess(response -> log.info("Avaliação concluída: {} resultados", 
                        response.getAvaliacoes().size()))
                .doOnError(error -> log.error("Erro ao avaliar candidatos", error));
    }

    /**
     * Extrai informações de currículo em PDF
     */
    public Mono<CandidatoIADTO> extractResume(byte[] pdfBytes, String filename) {
        log.info("Extraindo currículo: {}", filename);
        
        MultipartBodyBuilder builder = new MultipartBodyBuilder();
        builder.part("file", new ByteArrayResource(pdfBytes) {
            @Override
            public String getFilename() {
                return filename;
            }
        }).contentType(MediaType.APPLICATION_PDF);

        return webClient.post()
                .uri("/extract-resume")
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .body(BodyInserters.fromMultipartData(builder.build()))
                .retrieve()
                .bodyToMono(CandidatoIADTO.class)
                .timeout(Duration.ofMinutes(2))
                .doOnSuccess(candidato -> log.info("Currículo extraído: {}", candidato.getNome()))
                .doOnError(error -> log.error("Erro ao extrair currículo", error));
    }

    /**
     * Extrai candidato de texto livre
     */
    public Mono<CandidatoIADTO> extractSelf(String text, Boolean useModel) {
        log.info("Extraindo candidato de texto (useModel={})", useModel);
        
        ExtractSelfRequestDTO request = ExtractSelfRequestDTO.builder()
                .text(text)
                .useModel(useModel)
                .build();

        return webClient.post()
                .uri("/extract-self")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(CandidatoIADTO.class)
                .timeout(Duration.ofMinutes(1))
                .doOnSuccess(candidato -> log.info("Candidato extraído: {}", candidato.getNome()))
                .doOnError(error -> log.error("Erro ao extrair candidato", error));
    }

    /**
     * Extrai vaga de texto livre
     */
    public Mono<VagaIADTO> extractJob(String text, Boolean useModel) {
        log.info("Extraindo vaga de texto (useModel={})", useModel);
        
        ExtractJobRequestDTO request = ExtractJobRequestDTO.builder()
                .text(text)
                .useModel(useModel)
                .build();

        return webClient.post()
                .uri("/extract-job")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(VagaIADTO.class)
                .timeout(Duration.ofMinutes(1))
                .doOnSuccess(vaga -> log.info("Vaga extraída: {}", vaga.getTitulo()))
                .doOnError(error -> log.error("Erro ao extrair vaga", error));
    }

    /**
     * Avalia candidato (texto) vs vaga
     */
    public Mono<AvaliacoesResponseDTO> evaluateSelf(VagaIADTO vaga, String selfText, Boolean useModel) {
        log.info("Avaliando auto-descrição para vaga: {}", vaga.getTitulo());
        
        var request = new com.gs.fiap.jobfitscore.domain.ia.dto.EvaluateSelfRequestDTO(
                vaga, selfText, useModel
        );

        return webClient.post()
                .uri("/evaluate-self")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(AvaliacoesResponseDTO.class)
                .timeout(Duration.ofMinutes(2))
                .doOnSuccess(response -> log.info("Auto-avaliação concluída"))
                .doOnError(error -> log.error("Erro ao avaliar auto-descrição", error));
    }

    /**
     * Avalia textos livres (vaga + candidato)
     */
    public Mono<AvaliacoesResponseDTO> evaluateTexts(String jobText, String selfText, Boolean useModel) {
        log.info("Avaliando textos livres (useModel={})", useModel);
        
        EvaluateTextsRequestDTO request = EvaluateTextsRequestDTO.builder()
                .jobText(jobText)
                .selfText(selfText)
                .useModel(useModel)
                .build();

        return webClient.post()
                .uri("/evaluate-texts")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(AvaliacoesResponseDTO.class)
                .timeout(Duration.ofMinutes(3))
                .doOnSuccess(response -> log.info("Avaliação de textos concluída"))
                .doOnError(error -> log.error("Erro ao avaliar textos", error));
    }
}

// DTO adicional para evaluate-self
@Data
@AllArgsConstructor
@NoArgsConstructor
class EvaluateSelfRequestDTO {
    private VagaIADTO vaga;
    
    @JsonProperty("self_text")
    private String selfText;
    
    @JsonProperty("use_model")
    private Boolean useModel = true;
}
```

### 4. Criar Serviço de IA

```java
package com.gs.fiap.jobfitscore.domain.ia.service;

import com.gs.fiap.jobfitscore.domain.ia.client.IAClient;
import com.gs.fiap.jobfitscore.domain.ia.dto.*;
import com.gs.fiap.jobfitscore.domain.candidatura.Candidatura;
import com.gs.fiap.jobfitscore.domain.usuario.Usuario;
import com.gs.fiap.jobfitscore.domain.vaga.Vaga;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class IAService {

    private final IAClient iaClient;

    /**
     * Verifica se a API de IA está disponível
     */
    public Mono<Boolean> isAvailable() {
        return iaClient.checkHealth();
    }

    /**
     * Calcula score de compatibilidade entre candidato e vaga
     */
    public Mono<AvaliacaoDTO> calcularScore(Usuario usuario, Vaga vaga) {
        log.info("Calculando score para usuário {} na vaga {}", 
                usuario.getId(), vaga.getId());

        // Converter entidades para DTOs da IA
        VagaIADTO vagaDTO = convertVagaToDTO(vaga);
        CandidatoIADTO candidatoDTO = convertUsuarioToDTO(usuario);

        EvaluateRequestDTO request = EvaluateRequestDTO.builder()
                .vaga(vagaDTO)
                .candidatos(List.of(candidatoDTO))
                .useModel(true)
                .build();

        return iaClient.evaluate(request)
                .map(response -> response.getAvaliacoes().get(0))
                .doOnSuccess(avaliacao -> 
                    log.info("Score calculado: {} - {}", avaliacao.getScore(), avaliacao.getFeedback()))
                .onErrorResume(error -> {
                    log.error("Erro ao calcular score, usando fallback", error);
                    return Mono.just(calcularScoreFallback(usuario, vaga));
                });
    }

    /**
     * Avalia múltiplos candidatos de uma vez
     */
    public Mono<List<AvaliacaoDTO>> avaliarCandidatos(Vaga vaga, List<Usuario> usuarios) {
        log.info("Avaliando {} candidatos para vaga {}", usuarios.size(), vaga.getId());

        VagaIADTO vagaDTO = convertVagaToDTO(vaga);
        List<CandidatoIADTO> candidatosDTO = usuarios.stream()
                .map(this::convertUsuarioToDTO)
                .collect(Collectors.toList());

        EvaluateRequestDTO request = EvaluateRequestDTO.builder()
                .vaga(vagaDTO)
                .candidatos(candidatosDTO)
                .useModel(true)
                .build();

        return iaClient.evaluate(request)
                .map(AvaliacoesResponseDTO::getAvaliacoes)
                .doOnSuccess(avaliacoes -> 
                    log.info("Avaliação concluída: {} candidatos", avaliacoes.size()));
    }

    /**
     * Extrai informações de currículo em PDF
     */
    public Mono<CandidatoIADTO> extrairCurriculo(byte[] pdfBytes, String filename) {
        return iaClient.extractResume(pdfBytes, filename);
    }

    /**
     * Converte Vaga para DTO da IA
     */
    private VagaIADTO convertVagaToDTO(Vaga vaga) {
        List<String> requisitos = vaga.getVagaHabilidades().stream()
                .map(vh -> vh.getHabilidade().getNome())
                .collect(Collectors.toList());

        return VagaIADTO.builder()
                .titulo(vaga.getTitulo())
                .empresa(vaga.getEmpresa().getNomeEmpresa())
                .requisitos(requisitos)
                .descricao(vaga.getDescricao())
                .build();
    }

    /**
     * Converte Usuario para DTO da IA
     */
    private CandidatoIADTO convertUsuarioToDTO(Usuario usuario) {
        List<String> habilidades = usuario.getUsuarioHabilidades().stream()
                .map(uh -> uh.getHabilidade().getNome())
                .collect(Collectors.toList());

        List<String> cursos = usuario.getCursos().stream()
                .map(c -> c.getNome())
                .collect(Collectors.toList());

        return CandidatoIADTO.builder()
                .nome(usuario.getNome())
                .habilidades(habilidades)
                .experiencia(buildExperienciaText(usuario))
                .cursos(cursos)
                .build();
    }

    /**
     * Constrói texto de experiência do usuário
     */
    private String buildExperienciaText(Usuario usuario) {
        StringBuilder exp = new StringBuilder();
        
        if (!usuario.getCursos().isEmpty()) {
            exp.append("Formação: ")
               .append(usuario.getCursos().stream()
                       .map(c -> c.getNome() + " - " + c.getInstituicao())
                       .collect(Collectors.joining("; ")));
        }
        
        if (!usuario.getUsuarioHabilidades().isEmpty()) {
            if (exp.length() > 0) exp.append(". ");
            exp.append("Habilidades técnicas: ")
               .append(usuario.getUsuarioHabilidades().size())
               .append(" tecnologias dominadas");
        }
        
        return exp.toString();
    }

    /**
     * Calcula score simples sem IA (fallback)
     */
    private AvaliacaoDTO calcularScoreFallback(Usuario usuario, Vaga vaga) {
        List<String> habilidadesUsuario = usuario.getUsuarioHabilidades().stream()
                .map(uh -> uh.getHabilidade().getNome().toLowerCase())
                .collect(Collectors.toList());

        List<String> requisitosVaga = vaga.getVagaHabilidades().stream()
                .map(vh -> vh.getHabilidade().getNome().toLowerCase())
                .collect(Collectors.toList());

        long matches = requisitosVaga.stream()
                .filter(habilidadesUsuario::contains)
                .count();

        int score = (int) ((matches * 100.0) / Math.max(requisitosVaga.size(), 1));
        
        String feedback = String.format(
                "Compatibilidade: %d%%. Possui %d de %d habilidades requeridas.",
                score, matches, requisitosVaga.size()
        );

        return new AvaliacaoDTO(usuario.getNome(), score, feedback);
    }
}
```

### 5. Adicionar Configuração

```properties
# application.properties
ia.api.base-url=http://localhost:8000
```

### 6. Exemplo de Uso no Controller

```java
package com.gs.fiap.jobfitscore.controller;

import com.gs.fiap.jobfitscore.domain.ia.dto.AvaliacaoDTO;
import com.gs.fiap.jobfitscore.domain.ia.service.IAService;
import com.gs.fiap.jobfitscore.domain.usuario.Usuario;
import com.gs.fiap.jobfitscore.domain.vaga.Vaga;
import com.gs.fiap.jobfitscore.domain.usuario.UsuarioRepository;
import com.gs.fiap.jobfitscore.domain.vaga.VagaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/ia")
@RequiredArgsConstructor
public class IAController {

    private final IAService iaService;
    private final UsuarioRepository usuarioRepository;
    private final VagaRepository vagaRepository;

    @GetMapping("/health")
    public Mono<ResponseEntity<String>> checkHealth() {
        return iaService.isAvailable()
                .map(available -> available 
                        ? ResponseEntity.ok("IA API disponível")
                        : ResponseEntity.status(503).body("IA API indisponível"));
    }

    @PostMapping("/calcular-score")
    public Mono<ResponseEntity<AvaliacaoDTO>> calcularScore(
            @RequestParam Long usuarioId,
            @RequestParam Long vagaId) {
        
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado"));
        
        Vaga vaga = vagaRepository.findById(vagaId)
                .orElseThrow(() -> new RuntimeException("Vaga não encontrada"));

        return iaService.calcularScore(usuario, vaga)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }
}
```

---

## 🔐 Tratamento de Erros

### Códigos HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Requisição inválida (arquivo inválido, campo obrigatório ausente) |
| 500 | Erro interno (problema com Ollama ou processamento) |

### Exemplo de Erro
```json
{
  "detail": "Não foi possível extrair texto do PDF."
}
```

---

## ⚙️ Configuração de Ambiente

### Variáveis de Ambiente (.env)

```bash
# Aplicação
APP_NAME=GS-JobFitScore API
CORS_ORIGINS=*

# Ollama
OLLAMA_URL=http://127.0.0.1:11434/api/generate
OLLAMA_MODEL=llama3.2:3b
USE_MODEL=true

# Parâmetros do modelo
OLLAMA_NUM_CTX=4096
OLLAMA_TEMPERATURE=0.2
OLLAMA_NUM_PREDICT=800
```

---

## 🧪 Testando com cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Avaliar Candidatos
```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "vaga": {
      "titulo": "Desenvolvedor Java",
      "requisitos": ["Java", "Spring Boot"]
    },
    "candidatos": [
      {
        "nome": "João",
        "habilidades": ["Java", "Spring Boot", "PostgreSQL"]
      }
    ],
    "use_model": true
  }'
```

### Extrair Vaga
```bash
curl -X POST http://localhost:8000/extract-job \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Vaga para Desenvolvedor Java Sênior na ABC Tech",
    "use_model": true
  }'
```

---

## 📊 Desempenho

- **Health Check**: < 100ms
- **Evaluate (sem IA)**: 100-500ms
- **Evaluate (com IA)**: 5-30s (depende do modelo)
- **Extract Resume**: 10-60s
- **Extract Self/Job**: 3-15s

---

## 🛡️ Fallback Automático

A API possui fallback determinístico que é ativado automaticamente quando:
- Ollama não está disponível
- Timeout na resposta do modelo
- Erro ao processar resposta do modelo
- `use_model=false` na requisição

O fallback usa algoritmo simples baseado em:
- Matching de habilidades
- Bônus por cursos relacionados
- Penalidade por requisitos faltantes

---

## 📝 Notas Importantes

1. **Timeout**: Ajuste os timeouts no WebClient conforme necessário
2. **Memória**: Processamento de PDFs grandes pode consumir muita memória
3. **Concorrência**: API suporta múltiplas requisições simultâneas
4. **Cache**: Considere implementar cache para avaliações repetidas
5. **Monitoramento**: Use `/health` para health checks periódicos

---

## 🔄 Versionamento

**Versão Atual:** 1.0.0
- ✅ 7 endpoints funcionais
- ✅ Fallback automático
- ✅ Suporte a PDF
- ✅ Extração via IA
- ✅ CORS configurável

---

## 📞 Suporte

Para problemas ou dúvidas:
- Verifique logs da API: `logs/` ou console do PowerShell
- Teste endpoint `/health`
- Valide se Ollama está rodando: `http://localhost:11434`

---

## 🚀 Próximos Passos

1. Adicionar autenticação (JWT)
2. Implementar rate limiting
3. Cache de resultados
4. Métricas e observabilidade
5. Suporte a outros formatos (DOCX, TXT)
6. API de webhook para notificações
