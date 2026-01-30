# UI Test Automation — SauceDemo (Desafio Técnico)

Implementação de testes automatizados de interface para o site https://www.saucedemo.com utilizando **Python**, **Selenium WebDriver** e **Pytest**, seguindo o padrão **Page Object Model**.

O projeto cobre fluxos críticos da aplicação, como login, manipulação de carrinho e checkout, priorizando clareza, robustez e facilidade de execução.

## Objetivos da Solução

- Validar os principais fluxos funcionais do sistema.
- Evitar testes frágeis (flaky) causados por timing e eventos de UI.
- Manter os testes legíveis e fáceis de manter.
- Separar claramente lógica de teste, páginas e infraestrutura.

## Decisões Técnicas

### - Page Object Model (POM)
Cada página da aplicação possui uma classe dedicada responsável por:
- mapear elementos,
- encapsular ações,
- expor uma API clara para os testes.

Isso reduz acoplamento e melhora manutenção.

### - Esperas explícitas (WebDriverWait)
Não são utilizados `sleep`.  
Toda sincronização é feita via **esperas explícitas**, garantindo maior estabilidade em diferentes ambientes.

### - Validação por efeito observável
Ações como “adicionar ao carrinho” são validadas pelo **efeito no sistema** (badge do carrinho / URL), e não apenas pelo clique em si.

Isso torna os testes mais próximos do comportamento real do usuário.

### - Evidências automáticas em falha
Quando um teste falha, são gerados automaticamente:
- screenshot (`.png`)
- snapshot do DOM (`.html`)

Facilitando análise e depuração.

## Arquitetura do Projeto

```bash
pages/
   base_page.py        # Classe base (driver, wait, helpers)
   login_page.py       # Página de login
   products_page.py    # Página de produtos
   cart_page.py        # Página do carrinho
   checkout_page.py    # Página de checkout
   menu_component.py   # Componentes compartilhados

fixtures/
   driver.py          # Fixtures de driver 
   session.py          # Fixtures de login

tests/
   test_login.py
   test_cart_behavior.py

utils/
   artifacts.py        # Geração de evidências em falha

artifacts/             # Gerado em runtime (ignorado no git)
README.md
```

## Como executar

Pré-requisitos:
- Python 3.11+ (recomendado)
- Google Chrome instalado

Criar e ativar ambiente virtual:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Instalar dependências:
```bash
pip install -r requirements.txt
```

Rodar os testes:
```bash
pytest -q
```

Rodar com logs:
```bash
pytest -vv -s
```

Execução paralela (opcional):
```bash
pytest -q -n auto
```