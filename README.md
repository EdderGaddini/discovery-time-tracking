# Automação de Apontamento (Discovery)

Este projeto realiza a **automação de apontamento** em uma plataforma web específica (Discovery). A aplicação permite:

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

# Instala as bibliotecas
pip python main.py

## Uso

1. Garanta que o msedgedriver.exe esteja na mesma pasta do script ou com o caminho apontado corretamente no código.
2. Execute o script (ex: python main.py).
3. Preencha as credenciais de login (usuário e senha).
4. Se desejar executar em modo headless (sem abrir janela), marque o checkbox correspondente.
5. Pressione Start para iniciar o processo de automação.

**Dica:** Clique duas vezes em qualquer célula de Horas ou % do Mês para editar, e na coluna “Bloquear” para pular determinado dia.

## Gerando um Executável (.exe) com PyInstaller

1. **Instale o PyInstaller** pip install pyinstaller
2. **Navegue** até a pasta do projeto (onde está main.py).
3. **Gere o executável** pyinstaller --onefile -w --name=leega_discovery_auto main.py
4. Ao terminar, na pasta dist/ estará o leega_discovery_auto.exe.
5. Copie o msedgedriver.exe para dentro de dist/, junto ao .exe.


