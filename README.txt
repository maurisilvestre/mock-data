# Como instalar e rodar o app gerador de CSV

1. Instale o Python 3 (https://www.python.org/downloads/)
   - Marque a opção "Add Python to PATH" na instalação.

2. Instale o pip (se necessário)
   - Teste no terminal:  python3 -m pip --version
   - Se não funcionar, baixe https://bootstrap.pypa.io/get-pip.py e rode: python3 get-pip.py

3. Instale os pacotes necessários:
   - No terminal, execute:
     python3 -m pip install streamlit faker validate-docbr pandas wheel setuptools

4. Instale o arquivo .whl do app:
   - Navegue até a pasta onde está o arquivo:
     cd /caminho/da/pasta
   - Instale:
     python3 -m pip install mock_test_app-0.1.0-py3-none-any.whl

5. Rode o app:
   - Execute:
     python3 -m mock_test.main
   - O navegador abrirá o app (http://localhost:8501)

Se aparecer algum erro de pacote, repita o passo 3 para garantir que todos os pacotes estejam instalados.

Dúvidas? Basta pedir ajuda!
