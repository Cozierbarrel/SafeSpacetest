# 🌿 SafeSpace — Controle de Humor

Aplicação TUI (Terminal User Interface) de controle e acompanhamento de humor,
construída com **Python + Textual + MySQL**.

---

## 📁 Estrutura do Projeto

```
safespace/
├── main.py                    # Ponto de entrada da aplicação
├── requirements.txt           # Dependências Python
├── config/
│   └── database.py            # Conexão e inicialização do MySQL
├── models/
│   ├── user_model.py          # CRUD de usuários (registro, login)
│   └── mood_model.py          # CRUD de registros de humor
├── screens/
│   ├── home_screen.py         # Tela inicial (login / cadastro)
│   ├── login_screen.py        # Tela de autenticação
│   ├── register_screen.py     # Tela de cadastro com validações
│   ├── menu_screen.py         # Menu principal pós-login
│   ├── tracking_screen.py     # Registro de humor com emojis
│   ├── reports_screen.py      # Relatórios semanais/mensais em gráfico ASCII
│   └── emergency_screen.py    # Simulação de chamada de emergência
└── utils/
    ├── validators.py          # Validação de email, senha e telefone
    └── mood_utils.py          # Emojis, cálculo de médias, geração de gráficos
```

---

## ⚙️ Requisitos

- Python 3.10+
- MySQL 5.7+ ou 8.0+
- pip

---

## 🚀 Instalação e Execução

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Configure o banco de dados

Edite o arquivo `config/database.py` e preencha com suas credenciais MySQL:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",        # ← seu usuário MySQL
    "password": "",        # ← sua senha MySQL
    "database": "safespace_db",
}
```

> O banco de dados e as tabelas são criados automaticamente na primeira execução.

### 3. Certifique-se de que o MySQL está rodando

```bash
# Linux
sudo service mysql start

# macOS (Homebrew)
brew services start mysql
```

### 4. Execute a aplicação

```bash
python main.py
```

---

## 🎮 Controles e Navegação

| Tecla     | Ação                            |
|-----------|---------------------------------|
| `ESC`     | Voltar para a tela anterior     |
| `Q`       | Sair da aplicação               |
| `←` / `→` | Navegar entre períodos (relatórios) |
| `Enter`   | Submeter formulários            |
| `Tab`     | Navegar entre campos            |

---

## 🌟 Funcionalidades

### Tela Inicial
- Opções de Login e Cadastro

### Cadastro
- Validação de email (domínios aceitos: Gmail, Hotmail, Outlook, UFRPE, etc.)
- Validação de senha: mín. 8 chars, 1 maiúscula, 2 números, 1 caractere especial
- Confirmação de senha
- Contato de emergência opcional (formato telefone brasileiro)

### Tracking de Humor
- 6 níveis de humor representados por emojis:
  - 😭 Muito Triste (1)
  - 😢 Triste (2)
  - 😐 Neutro (3)
  - 🙂 Bem (4)
  - 😊 Feliz (5)
  - 😁 Muito Feliz (6)
- Campo de descrição opcional
- Múltiplos registros por dia com timestamp

### Relatórios
- Visualização por **semana** ou **mês**
- Navegação para períodos anteriores com dados
- Gráfico de barras ASCII com flutuação de humor
- Média diária (quando há múltiplos registros no dia)
- Média geral do período com emoji

### Emergência
- Simulação de ligação para o contato cadastrado
- Retorno automático ao menu após 3 segundos

---

## 🗄️ Banco de Dados

### Tabela `users`
| Campo              | Tipo         | Descrição                        |
|--------------------|--------------|----------------------------------|
| id                 | INT PK       | Identificador único              |
| email              | VARCHAR(255) | Email único do usuário           |
| password_hash      | VARCHAR(255) | Hash SHA-256 com salt            |
| emergency_contact  | VARCHAR(20)  | Telefone de emergência (opcional)|
| created_at         | TIMESTAMP    | Data de cadastro                 |

### Tabela `mood_entries`
| Campo       | Tipo      | Descrição                            |
|-------------|-----------|--------------------------------------|
| id          | INT PK    | Identificador único                  |
| user_id     | INT FK    | Referência ao usuário                |
| mood_level  | TINYINT   | Nível de humor (1–6)                 |
| description | TEXT      | Descrição opcional do estado         |
| recorded_at | TIMESTAMP | Data e hora exatas do registro       |
