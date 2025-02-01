# Automação de Apontamento (Discovery/Leega)

Este projeto realiza a **automação de apontamento** em uma plataforma web específica (Discovery/Leega). A aplicação permite:

1. **Login automático** no sistema.
2. **Apontamento de dias úteis** de forma dinâmica, considerando feriados nacionais/municipais (estado de SP).
3. **Edição de horas, porcentagem e bloqueio** de determinado dia pelo usuário antes do envio.
4. **Modo headless** opcional, permitindo executar o processo em segundo plano (sem abrir a janela do navegador).

## Pré-requisitos

1. **Python 3.7+** (recomendado Python 3.8 ou superior).
2. **Bibliotecas Python** necessárias:
   - `customtkinter`
   - `tkinter` (já incluso na instalação padrão do Python em alguns sistemas)
   - `selenium`
   - `holidays`
3. **WebDriver do Microsoft Edge** (msedgedriver) compatível com a versão instalada do Edge:
   - É **fundamental** que o arquivo `msedgedriver.exe` esteja **na mesma pasta** do executável final ou em algum diretório presente no PATH do sistema.  
   - Exemplo de organização final:
     ```
     dist/
       |__ seu_programa.exe
       |__ msedgedriver.exe
     ```

## Instalação das Dependências

Crie ou ative um ambiente virtual (opcional, mas recomendado) e instale os pacotes. Exemplo no Windows:

```bash
# Cria um ambiente virtual
python -m venv venv

# Ativa o ambiente virtual
venv\Scripts\activate

# Instala as bibliotecas
pip install customtkinter selenium holidays
