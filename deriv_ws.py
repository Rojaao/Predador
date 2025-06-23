def iniciar_conexao(token, stake, fator_martingale, estrategia, placeholder_log):
    import time
    placeholder_log.markdown("```text\n✅ Conectado (simulado)\n```")
    time.sleep(1)
    placeholder_log.markdown(f"```text\n📊 Estratégia selecionada: {estrategia}\n```")