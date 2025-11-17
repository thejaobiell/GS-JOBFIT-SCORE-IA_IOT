# ☕ Exemplos Práticos de Integração Java + API IA

## 📋 Índice

1. [Setup Completo](#1-setup-completo)
2. [Uso Básico no Service](#2-uso-básico-no-service)
3. [Integração com Candidaturas](#3-integração-com-candidaturas)
4. [Upload de Currículo](#4-upload-de-currículo)
5. [Endpoint REST no Controller](#5-endpoint-rest-no-controller)
6. [Tratamento de Erros](#6-tratamento-de-erros)
7. [Testes Unitários](#7-testes-unitários)

---

## 1. Setup Completo

### 1.1 Adicionar ao `pom.xml`

```xml
<dependencies>
    <!-- Spring WebFlux para chamadas HTTP reativas -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>
    
    <!-- Lombok -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

### 1.2 Configurar `application.properties`

```properties
# API de IA
ia.api.base-url=http://localhost:8000
ia.api.timeout.connection=5000
ia.api.timeout.response=180000
ia.api.use-model=true

# Logging
logging.level.com.gs.fiap.jobfitscore.domain.ia=DEBUG
```

### 1.3 Estrutura de Pacotes Recomendada

```
com.gs.fiap.jobfitscore.domain.ia/
├── client/
│   └── IAClient.java
├── dto/
│   ├── VagaIADTO.java
│   ├── CandidatoIADTO.java
│   ├── AvaliacaoDTO.java
│   ├── AvaliacoesResponseDTO.java
│   └── ...
├── service/
│   └── IAService.java
├── config/
│   └── IAConfig.java
└── exception/
    └── IAException.java
```

---

## 2. Uso Básico no Service

### 2.1 Calcular Score ao Criar Candidatura

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class CandidaturaService {

    private final CandidaturaRepository candidaturaRepository;
    private final UsuarioRepository usuarioRepository;
    private final VagaRepository vagaRepository;
    private final IAService iaService;

    @Transactional
    public Candidatura criarCandidatura(Long usuarioId, Long vagaId) {
        log.info("Criando candidatura: usuário={}, vaga={}", usuarioId, vagaId);

        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new EntityNotFoundException("Usuário não encontrado"));
        
        Vaga vaga = vagaRepository.findById(vagaId)
                .orElseThrow(() -> new EntityNotFoundException("Vaga não encontrada"));

        // Criar candidatura
        Candidatura candidatura = Candidatura.builder()
                .usuario(usuario)
                .vaga(vaga)
                .dataCandidatura(LocalDateTime.now())
                .status(StatusCandidatura.EM_ANALISE)
                .build();

        // Calcular score com IA (assíncrono)
        iaService.calcularScore(usuario, vaga)
                .subscribe(avaliacao -> {
                    candidatura.setScore(avaliacao.getScore().doubleValue());
                    candidatura.setFeedback(avaliacao.getFeedback());
                    candidaturaRepository.save(candidatura);
                    log.info("Score calculado: {}", avaliacao.getScore());
                }, error -> {
                    log.error("Erro ao calcular score", error);
                    // Score padrão em caso de erro
                    candidatura.setScore(50.0);
                    candidatura.setFeedback("Avaliação automática indisponível");
                    candidaturaRepository.save(candidatura);
                });

        return candidaturaRepository.save(candidatura);
    }
}
```

### 2.2 Calcular Score de Forma Síncrona

```java
@Transactional
public Candidatura criarCandidaturaSincrona(Long usuarioId, Long vagaId) {
    Usuario usuario = usuarioRepository.findById(usuarioId)
            .orElseThrow(() -> new EntityNotFoundException("Usuário não encontrado"));
    
    Vaga vaga = vagaRepository.findById(vagaId)
            .orElseThrow(() -> new EntityNotFoundException("Vaga não encontrada"));

    Candidatura candidatura = Candidatura.builder()
            .usuario(usuario)
            .vaga(vaga)
            .dataCandidatura(LocalDateTime.now())
            .status(StatusCandidatura.EM_ANALISE)
            .build();

    try {
        // Bloqueia até obter resposta (usar com cuidado!)
        AvaliacaoDTO avaliacao = iaService.calcularScore(usuario, vaga)
                .block(Duration.ofMinutes(3));
        
        if (avaliacao != null) {
            candidatura.setScore(avaliacao.getScore().doubleValue());
            candidatura.setFeedback(avaliacao.getFeedback());
        }
    } catch (Exception e) {
        log.error("Erro ao calcular score", e);
        candidatura.setScore(50.0);
        candidatura.setFeedback("Avaliação automática indisponível");
    }

    return candidaturaRepository.save(candidatura);
}
```

---

## 3. Integração com Candidaturas

### 3.1 Recalcular Scores em Lote

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class IAService {

    private final IAClient iaClient;
    private final CandidaturaRepository candidaturaRepository;

    /**
     * Recalcula scores de todas as candidaturas de uma vaga
     */
    public Mono<Void> recalcularScoresVaga(Long vagaId) {
        log.info("Recalculando scores para vaga {}", vagaId);

        List<Candidatura> candidaturas = candidaturaRepository.findByVagaId(vagaId);
        
        if (candidaturas.isEmpty()) {
            return Mono.empty();
        }

        Vaga vaga = candidaturas.get(0).getVaga();
        List<Usuario> usuarios = candidaturas.stream()
                .map(Candidatura::getUsuario)
                .collect(Collectors.toList());

        return avaliarCandidatos(vaga, usuarios)
                .doOnSuccess(avaliacoes -> {
                    for (int i = 0; i < avaliacoes.size(); i++) {
                        AvaliacaoDTO avaliacao = avaliacoes.get(i);
                        Candidatura candidatura = candidaturas.get(i);
                        
                        candidatura.setScore(avaliacao.getScore().doubleValue());
                        candidatura.setFeedback(avaliacao.getFeedback());
                        candidaturaRepository.save(candidatura);
                    }
                    log.info("Scores recalculados: {} candidaturas", avaliacoes.size());
                })
                .then();
    }
}
```

### 3.2 Listar Candidatos Ordenados por Score

```java
@RestController
@RequestMapping("/api/vagas")
@RequiredArgsConstructor
public class VagaController {

    private final CandidaturaRepository candidaturaRepository;

    @GetMapping("/{vagaId}/candidatos/ranking")
    public ResponseEntity<List<CandidaturaRankingDTO>> getRanking(
            @PathVariable Long vagaId) {
        
        List<Candidatura> candidaturas = candidaturaRepository
                .findByVagaIdOrderByScoreDesc(vagaId);

        List<CandidaturaRankingDTO> ranking = candidaturas.stream()
                .map(c -> CandidaturaRankingDTO.builder()
                        .id(c.getId())
                        .nomeUsuario(c.getUsuario().getNome())
                        .score(c.getScore())
                        .feedback(c.getFeedback())
                        .status(c.getStatus())
                        .dataCandidatura(c.getDataCandidatura())
                        .build())
                .collect(Collectors.toList());

        return ResponseEntity.ok(ranking);
    }
}

@Data
@Builder
class CandidaturaRankingDTO {
    private Long id;
    private String nomeUsuario;
    private Double score;
    private String feedback;
    private StatusCandidatura status;
    private LocalDateTime dataCandidatura;
}
```

---

## 4. Upload de Currículo

### 4.1 Endpoint de Upload

```java
@RestController
@RequestMapping("/api/usuarios")
@RequiredArgsConstructor
@Slf4j
public class UsuarioController {

    private final IAService iaService;
    private final UsuarioService usuarioService;

    @PostMapping("/upload-curriculo")
    public Mono<ResponseEntity<CandidatoExtraidoDTO>> uploadCurriculo(
            @RequestParam("file") MultipartFile file) {
        
        log.info("Upload de currículo: {}", file.getOriginalFilename());

        if (!file.getContentType().equals("application/pdf")) {
            return Mono.just(ResponseEntity
                    .badRequest()
                    .body(null));
        }

        try {
            byte[] pdfBytes = file.getBytes();
            
            return iaService.extrairCurriculo(pdfBytes, file.getOriginalFilename())
                    .map(candidato -> {
                        CandidatoExtraidoDTO dto = CandidatoExtraidoDTO.builder()
                                .nome(candidato.getNome())
                                .habilidades(candidato.getHabilidades())
                                .experiencia(candidato.getExperiencia())
                                .cursos(candidato.getCursos())
                                .build();
                        
                        return ResponseEntity.ok(dto);
                    })
                    .onErrorReturn(ResponseEntity.status(500).build());
            
        } catch (IOException e) {
            log.error("Erro ao ler arquivo", e);
            return Mono.just(ResponseEntity.status(500).build());
        }
    }

    @PostMapping("/criar-de-curriculo")
    public Mono<ResponseEntity<Usuario>> criarUsuarioDeCurriculo(
            @RequestParam("file") MultipartFile file,
            @RequestParam("email") String email,
            @RequestParam("senha") String senha) {
        
        try {
            byte[] pdfBytes = file.getBytes();
            
            return iaService.extrairCurriculo(pdfBytes, file.getOriginalFilename())
                    .map(candidato -> {
                        // Criar usuário com dados extraídos
                        Usuario usuario = usuarioService.criarDeExtracao(
                                candidato, email, senha);
                        
                        return ResponseEntity.ok(usuario);
                    })
                    .onErrorReturn(ResponseEntity.status(500).build());
            
        } catch (IOException e) {
            log.error("Erro ao processar currículo", e);
            return Mono.just(ResponseEntity.status(500).build());
        }
    }
}

@Data
@Builder
class CandidatoExtraidoDTO {
    private String nome;
    private List<String> habilidades;
    private String experiencia;
    private List<String> cursos;
}
```

### 4.2 Service para Criar Usuário

```java
@Service
@RequiredArgsConstructor
@Transactional
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;
    private final HabilidadeRepository habilidadeRepository;
    private final CursoRepository cursoRepository;
    private final PasswordEncoder passwordEncoder;

    public Usuario criarDeExtracao(CandidatoIADTO candidato, String email, String senha) {
        // Criar usuário
        Usuario usuario = Usuario.builder()
                .nome(candidato.getNome())
                .email(email)
                .senha(passwordEncoder.encode(senha))
                .role(Role.USUARIO)
                .build();
        
        usuario = usuarioRepository.save(usuario);

        // Adicionar habilidades
        for (String nomeHab : candidato.getHabilidades()) {
            Habilidade hab = habilidadeRepository.findByNomeIgnoreCase(nomeHab)
                    .orElseGet(() -> {
                        Habilidade nova = new Habilidade();
                        nova.setNome(nomeHab);
                        return habilidadeRepository.save(nova);
                    });
            
            UsuarioHabilidade uh = new UsuarioHabilidade();
            uh.setUsuario(usuario);
            uh.setHabilidade(hab);
            uh.setNivel(NivelHabilidade.INTERMEDIARIO);
            usuario.getUsuarioHabilidades().add(uh);
        }

        // Adicionar cursos
        for (String nomeCurso : candidato.getCursos()) {
            Curso curso = Curso.builder()
                    .nome(nomeCurso)
                    .instituicao("Não especificado")
                    .usuario(usuario)
                    .build();
            usuario.getCursos().add(curso);
        }

        return usuarioRepository.save(usuario);
    }
}
```

---

## 5. Endpoint REST no Controller

### 5.1 Controller de IA

```java
@RestController
@RequestMapping("/api/ia")
@RequiredArgsConstructor
@Slf4j
public class IAController {

    private final IAService iaService;
    private final UsuarioRepository usuarioRepository;
    private final VagaRepository vagaRepository;

    @GetMapping("/health")
    public Mono<ResponseEntity<HealthResponseDTO>> checkHealth() {
        return iaService.isAvailable()
                .map(available -> {
                    HealthResponseDTO dto = HealthResponseDTO.builder()
                            .status(available ? "online" : "offline")
                            .message(available 
                                    ? "IA API disponível" 
                                    : "IA API indisponível - usando fallback")
                            .timestamp(LocalDateTime.now())
                            .build();
                    
                    return ResponseEntity.ok(dto);
                });
    }

    @PostMapping("/avaliar")
    public Mono<ResponseEntity<AvaliacaoDTO>> avaliar(
            @RequestParam Long usuarioId,
            @RequestParam Long vagaId) {
        
        log.info("Avaliando usuário {} para vaga {}", usuarioId, vagaId);

        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new EntityNotFoundException("Usuário não encontrado"));
        
        Vaga vaga = vagaRepository.findById(vagaId)
                .orElseThrow(() -> new EntityNotFoundException("Vaga não encontrada"));

        return iaService.calcularScore(usuario, vaga)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @PostMapping("/avaliar-lote")
    public Mono<ResponseEntity<List<AvaliacaoDTO>>> avaliarLote(
            @RequestParam Long vagaId,
            @RequestBody List<Long> usuarioIds) {
        
        log.info("Avaliando {} usuários para vaga {}", usuarioIds.size(), vagaId);

        Vaga vaga = vagaRepository.findById(vagaId)
                .orElseThrow(() -> new EntityNotFoundException("Vaga não encontrada"));
        
        List<Usuario> usuarios = usuarioRepository.findAllById(usuarioIds);

        return iaService.avaliarCandidatos(vaga, usuarios)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @PostMapping("/extrair-texto")
    public Mono<ResponseEntity<CandidatoIADTO>> extrairTexto(
            @RequestBody ExtracaoTextoRequest request) {
        
        return iaService.extrairCandidatoDeTexto(
                request.getText(), 
                request.getUseModel())
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.badRequest().build());
    }
}

@Data
@Builder
class HealthResponseDTO {
    private String status;
    private String message;
    private LocalDateTime timestamp;
}

@Data
class ExtracaoTextoRequest {
    private String text;
    private Boolean useModel = true;
}
```

---

## 6. Tratamento de Erros

### 6.1 Exception Customizada

```java
package com.gs.fiap.jobfitscore.domain.ia.exception;

public class IAException extends RuntimeException {
    
    public IAException(String message) {
        super(message);
    }
    
    public IAException(String message, Throwable cause) {
        super(message, cause);
    }
}

public class IAUnavailableException extends IAException {
    public IAUnavailableException(String message) {
        super(message);
    }
}

public class IATimeoutException extends IAException {
    public IATimeoutException(String message) {
        super(message);
    }
}
```

### 6.2 Global Exception Handler

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(IAUnavailableException.class)
    public ResponseEntity<ErrorResponseDTO> handleIAUnavailable(
            IAUnavailableException ex) {
        
        log.warn("IA indisponível: {}", ex.getMessage());
        
        ErrorResponseDTO error = ErrorResponseDTO.builder()
                .timestamp(LocalDateTime.now())
                .status(503)
                .error("Service Unavailable")
                .message("Serviço de IA temporariamente indisponível. Usando fallback.")
                .build();
        
        return ResponseEntity.status(503).body(error);
    }

    @ExceptionHandler(IATimeoutException.class)
    public ResponseEntity<ErrorResponseDTO> handleIATimeout(
            IATimeoutException ex) {
        
        log.error("Timeout na IA: {}", ex.getMessage());
        
        ErrorResponseDTO error = ErrorResponseDTO.builder()
                .timestamp(LocalDateTime.now())
                .status(504)
                .error("Gateway Timeout")
                .message("Tempo limite excedido ao processar com IA. Tente novamente.")
                .build();
        
        return ResponseEntity.status(504).body(error);
    }

    @ExceptionHandler(IAException.class)
    public ResponseEntity<ErrorResponseDTO> handleIAException(
            IAException ex) {
        
        log.error("Erro na IA: {}", ex.getMessage(), ex);
        
        ErrorResponseDTO error = ErrorResponseDTO.builder()
                .timestamp(LocalDateTime.now())
                .status(500)
                .error("Internal Server Error")
                .message("Erro ao processar requisição com IA: " + ex.getMessage())
                .build();
        
        return ResponseEntity.status(500).body(error);
    }
}

@Data
@Builder
class ErrorResponseDTO {
    private LocalDateTime timestamp;
    private Integer status;
    private String error;
    private String message;
}
```

---

## 7. Testes Unitários

### 7.1 Teste do IAService

```java
@ExtendWith(MockitoExtension.class)
class IAServiceTest {

    @Mock
    private IAClient iaClient;

    @Mock
    private CandidaturaRepository candidaturaRepository;

    @InjectMocks
    private IAService iaService;

    private Usuario usuario;
    private Vaga vaga;

    @BeforeEach
    void setUp() {
        usuario = Usuario.builder()
                .id(1L)
                .nome("João Silva")
                .build();

        vaga = Vaga.builder()
                .id(1L)
                .titulo("Desenvolvedor Java")
                .build();
    }

    @Test
    void testCalcularScore_ComSucesso() {
        // Arrange
        AvaliacaoDTO avaliacaoEsperada = new AvaliacaoDTO(
                "João Silva", 85, "Boa compatibilidade");
        
        AvaliacoesResponseDTO response = new AvaliacoesResponseDTO(
                List.of(avaliacaoEsperada));

        when(iaClient.evaluate(any(EvaluateRequestDTO.class)))
                .thenReturn(Mono.just(response));

        // Act
        AvaliacaoDTO resultado = iaService.calcularScore(usuario, vaga)
                .block(Duration.ofSeconds(5));

        // Assert
        assertNotNull(resultado);
        assertEquals(85, resultado.getScore());
        assertEquals("Boa compatibilidade", resultado.getFeedback());
        
        verify(iaClient, times(1)).evaluate(any(EvaluateRequestDTO.class));
    }

    @Test
    void testCalcularScore_ComFallback() {
        // Arrange
        when(iaClient.evaluate(any(EvaluateRequestDTO.class)))
                .thenReturn(Mono.error(new RuntimeException("IA indisponível")));

        // Act
        AvaliacaoDTO resultado = iaService.calcularScore(usuario, vaga)
                .block(Duration.ofSeconds(5));

        // Assert
        assertNotNull(resultado);
        assertTrue(resultado.getScore() >= 0 && resultado.getScore() <= 100);
        assertNotNull(resultado.getFeedback());
    }

    @Test
    void testIsAvailable_QuandoDisponivel() {
        // Arrange
        when(iaClient.checkHealth()).thenReturn(Mono.just(true));

        // Act
        Boolean disponivel = iaService.isAvailable()
                .block(Duration.ofSeconds(5));

        // Assert
        assertTrue(disponivel);
    }

    @Test
    void testIsAvailable_QuandoIndisponivel() {
        // Arrange
        when(iaClient.checkHealth()).thenReturn(Mono.just(false));

        // Act
        Boolean disponivel = iaService.isAvailable()
                .block(Duration.ofSeconds(5));

        // Assert
        assertFalse(disponivel);
    }
}
```

### 7.2 Teste de Integração

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureWebTestClient
class IAControllerIntegrationTest {

    @Autowired
    private WebTestClient webTestClient;

    @MockBean
    private IAService iaService;

    @Test
    void testHealthEndpoint() {
        when(iaService.isAvailable()).thenReturn(Mono.just(true));

        webTestClient.get()
                .uri("/api/ia/health")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.status").isEqualTo("online")
                .jsonPath("$.message").isEqualTo("IA API disponível");
    }

    @Test
    void testAvaliarEndpoint() {
        AvaliacaoDTO avaliacao = new AvaliacaoDTO(
                "João Silva", 85, "Boa compatibilidade");

        when(iaService.calcularScore(any(), any()))
                .thenReturn(Mono.just(avaliacao));

        webTestClient.post()
                .uri(uriBuilder -> uriBuilder
                        .path("/api/ia/avaliar")
                        .queryParam("usuarioId", 1)
                        .queryParam("vagaId", 1)
                        .build())
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.nome").isEqualTo("João Silva")
                .jsonPath("$.score").isEqualTo(85)
                .jsonPath("$.feedback").isEqualTo("Boa compatibilidade");
    }
}
```

---

## 🎯 Resumo de Boas Práticas

1. **Sempre use Mono/Flux** para operações assíncronas
2. **Implemente fallback** para quando a IA estiver indisponível
3. **Configure timeouts adequados** (3-5min para operações com IA)
4. **Log todas as operações** para debugging
5. **Trate erros de forma robusta** com handlers globais
6. **Use DTOs separados** para comunicação com a API
7. **Teste com e sem IA disponível**
8. **Considere cache** para reduzir chamadas repetidas
9. **Monitore performance** das chamadas à IA
10. **Documente endpoints** com Swagger

---

## 📚 Recursos Adicionais

- **Documentação API**: [API_INTEGRATION.md](./API_INTEGRATION.md)
- **Spring WebFlux**: https://docs.spring.io/spring-framework/reference/web/webflux.html
- **Reactor**: https://projectreactor.io/docs/core/release/reference/

---

**Desenvolvido para Global Solution - FIAP 2025** ☕🤖
