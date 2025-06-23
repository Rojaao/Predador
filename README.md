# Predador de Padrões - Over 3 (1 tick)

Este robô implementa a estratégia "Predador de Padrões", apostando Over 3 com expiração de 1 tick na Deriv, baseada em reversão de comportamento emocional dos apostadores.

## Como usar

1. Crie um novo repositório no GitHub e envie estes arquivos para a raiz do repositório:
   - `app.py`
   - `bot_core.py`
   - `requirements.txt`
2. No Streamlit Cloud:
   - Conecte ao repositório no GitHub.
   - Configure Build Command: `pip install -r requirements.txt`
   - Configure Start Command: `streamlit run app.py`
   - Deploy e aguarde.
3. No Render.com:
   - Conecte ao mesmo repositório GitHub.
   - Configure Build Command: `pip install -r requirements.txt`
   - Configure Start Command: `streamlit run app.py`
   - Deploy e aguarde.

## Configurações
- Token da Deriv: insira na interface.
- Stake, Martingale, Stop Loss, Meta de Lucro, Delay e Analise de Ticks configuráveis.

## Logs
- Os logs de conexão e operações aparecerão no console do servidor (Render, local ou logs do Streamlit Cloud).
- Verifique se a conexão WebSocket está sendo estabelecida corretamente.

## Observação
- Em ambientes que bloqueiam WebSocket (Streamlit Cloud), o robô não funcionará. Use Render.com, Replit ou Hugging Face Spaces.