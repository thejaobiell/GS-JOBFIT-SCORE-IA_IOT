# Como usar a API de IA/IOT em Mobile

## 🛠️ Stack Tecnológica

### Frontend Mobile
- **React Native** com Expo SDK 53
- **TypeScript** para tipagem estática
- **React Navigation** para roteamento

### Backend
- **Java 21+** com Spring Boot
- **PostgreSQL 16+** como banco de dados
- **Flyway** para migrations
- **Spring Data JPA** para persistência

### Inteligência Artificial
- **Python 3.10+**
- **Ollama** com modelo Llama 3.2:3b
- API REST para integração

---

## 🚀 Instalação

### 📋 Pré-requisitos

Certifique-se de ter instalado:

- ☕ Java 21 ou superior
- 🐘 PostgreSQL 16 ou superior
- 📦 Node.js 18 ou superior
- 🐍 Python 3.10 ou superior
- 🦙 Ollama

---

## 🗄️ Parte 1: Configuração do Banco de Dados

### Instalação do PostgreSQL

<details>
<summary><b>🐧 Linux</b></summary>

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```
</details>

<details>
<summary><b>🪟 Windows</b></summary>

1. Baixe o instalador oficial: [postgresql.org/download](https://www.postgresql.org/download/)
2. Execute o instalador e siga as instruções
3. Defina uma senha forte para o usuário `postgres`
4. Mantenha a porta padrão `5432`
5. Finalize a instalação
</details>

<details>
<summary><b>🐳 Docker (Recomendado)</b></summary>

```bash
docker run --name jobfitscore-postgres \
  -e POSTGRES_PASSWORD=sua_senha \
  -e POSTGRES_DB=jobfitscore \
  -p 5432:5432 \
  -d postgres:16
```
</details>

### Criação do Banco de Dados

Acesse o PostgreSQL:

```bash
# Linux/Mac
sudo -u postgres psql

# Windows
psql -U postgres

# Docker
docker exec -it jobfitscore-postgres psql -U postgres
```

Execute os comandos SQL:

```sql
-- Criar o banco de dados
CREATE DATABASE jobfitscore;

-- Verificar criação
\l
```

---

## ⚙️ Parte 2: Configuração da API Backend

### 1. Clone o Repositório

Para usar a aplicação mobile no celular:
```bash
git clone -b mobile https://github.com/thejaobiell/GS-JOBFIT-SCORE-Java.git
cd GS-JOBFIT-SCORE-Java
```

Para usar a aplicação mobile na web:
```bash
git clone -b mobile-cors https://github.com/thejaobiell/GS-JOBFIT-SCORE-Java.git
cd GS-JOBFIT-SCORE-Java
```

### 2. Configure seu usuário

Edite o arquivo `src/main/resources/application.properties`:

```properties
spring.application.name=jobfitscore

spring.datasource.url=jdbc:postgresql://localhost:5432/jobfitscore
spring.datasource.username=<seu usuario>
spring.datasource.password=<sua senha>

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect

spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration
spring.flyway.repair=true
spring.flyway.repair-on-migrate=true

spring.main.allow-bean-definition-overriding=true

server.address=0.0.0.0
server.port=8080
```

### 3. Execute a API

**Linux/macOS/WSL:**
```bash
./mvnw spring-boot:run
```

**Windows:**
```powershell
.\mvnw.cmd spring-boot:run
```

### 4. Verifique a API

Acesse no navegador: `http://localhost:8080`

Você deve ver uma página HTML informando que a API está funcionando.

---

## 🤖 Parte 3: Configuração da API de IA

### 1. Clone o Repositório

```bash
git clone https://github.com/thejaobiell/GS-JOBFIT-SCORE-IA_IOT.git
cd GS-JOBFIT-SCORE-IA_IOT
```

### 2. Instale o Ollama

Visite [ollama.com](https://ollama.com/) e siga as instruções de instalação para seu sistema operacional.

### 3. Baixe o Modelo de IA

```bash
ollama pull llama3.2:3b
```

### 4. Execute a API de IA

```bash
# Torne o script executável
chmod +x run_api.sh

# Execute a API
./run_api.sh --host 0.0.0.0 --port 9001 --model llama3.2:3b
```

A API estará disponível em `http://localhost:9001`

---

## 📱 Parte 4: Configuração do App Mobile

### 1. Clone o Repositório

```bash
git clone https://github.com/thejaobiell/GS-JobFitScore-MOBILE.git
cd GS-JobFitScore-MOBILE
```

### 2. Instale as Dependências

```bash
npm install
```

### 3. Configure as Variáveis de Ambiente

#### Descubra seu IP Local

**Linux/Mac:**
```bash
hostname -I | awk '{print $1}'
```

**Windows:**
```powershell
ipconfig
```
> Procure por **Endereço IPv4** (ex: 192.168.1.100)

#### Crie o arquivo `.env`

Na raiz do projeto, crie o arquivo `.env`:

```env
EXPO_PUBLIC_IP=SEU_IP_AQUI
```

**Exemplo:**
```env
EXPO_PUBLIC_IP=192.168.1.100
```

### 4. Execute o Aplicativo

```bash
npm start
```

> ⚠️ **Importante**: Seu dispositivo deve estar na mesma rede Wi-Fi que seu computador.

---

## 🔍 Verificação e Troubleshooting

### ✅ Checklist de Verificação

- [ ] PostgreSQL rodando na porta 5432
- [ ] Banco `jobfitscore` criado
- [ ] API Backend Java rodando em `http://localhost:8080`
- [ ] Ollama instalado e modelo baixado
- [ ] API de IA rodando em `http://localhost:9001`
- [ ] Arquivo `.env` configurado corretamente
- [ ] Dispositivo na mesma rede Wi-Fi
