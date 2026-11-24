# Roteiro do vídeo de revelação de gravidez
# BPM 96 -> 1 batida = 0.625s. Durações de saída em múltiplos de batida.
B = 0.625

# (take, inicio_no_take_s, duracao_saida_s, velocidade, efeito, nota)
#  efeito: "" | "punch" (zoom de impacto) | "dream" (câmera lenta com brilho) | "push" (zoom lento) | "flash" (flash branco no fim)
EDL = [
    # ATO 1 - o casal (sem teste aparecendo)
    ("6598", 0.3, 4*B, 1.0, "low",  "olhando um pro outro"),
    ("6597", 12.1, 3*B, 1.0, "low",     "beijo de nariz (close)"),
    ("6598", 4.2, 3*B, 1.0, "low",      "beijo"),
    ("6598", 6.4, 2*B, 1.0, "low",      "risada"),
    # ATO 2 - os bonés
    ("6599", 4.3, 3*B, 1.0, "",      "ela coloca o boné nele"),
    ("6602", 3.8, 3*B, 1.0, "",      "ele coloca o boné nela"),
    ("6602", 8.0, 3*B, 1.0, "",      "ela ajeita o dele"),
    ("6602", 11.6, 2*B, 1.0, "punch", "os dois de boné"),
    ("6605", 0.4, 3*B, 1.0, "",      "chamam o pequeno"),
    # ATO 3 - o menino pequeno
    ("6606", 5.9, 3*B, 0.75, "",     "ele chega correndo e abraça"),
    ("6606", 10.6, 4*B, 1.0, "",     "colocam o boné nele"),
    ("6606", 14.0, 3*B, 1.0, "",     "os três sorrindo"),
    ("6611", 0.0, 3*B, 1.0, "",      "abraço no colo do pai"),
    ("6630", 1.6, 2*B, 1.0, "",      "irmãos (irmão maior, rápido)"),
    ("6606", 19.6, 3*B, 1.0, "flash", "família toda"),
    # ATO 4 - REVELAÇÃO
    ("6609", 2.0, 3*B, 1.0, "",      "pai entrega o teste ao pequeno"),
    ("6632", 3.4, 4*B, 0.75, "",     "boné BROTHER"),
    ("6610", 3.4, 4*B, 0.5, "dream", "pequeno vem com o teste (lento)"),
    ("6610", 9.7, 3*B, 1.0, "punch", "mostra o teste pra câmera"),
    ("6607", 4.9, 3*B, 1.0, "",      "mostra o teste"),
    ("6625", 9.0, 4*B, 1.0, "",      "casal mostra o teste"),
    ("6614", 2.5, 4*B, 1.0, "",      "família com o teste"),
    ("6616", 11.6, 4*B, 0.5, "dream", "pai beija a barriga (lento)"),
    ("6626", 4.3, 3*B, 1.0, "",      "beijo na barriga"),
    ("6629", 20.6, 4*B, 1.0, "",     "pequeno beija a barriga"),
    ("6628", 5.0, 4*B, 1.0, "",      "todos beijam a barriga"),
    ("6626", 6.8, 4*B, 0.5, "dream", "ela joga o cabelo (lento)"),
    # ATO 5 - corrida em câmera lenta
    ("6619", 3.0, 6*B, 0.5, "dream", "corrida e pulo no colo"),
    ("6618", 8.3, 4*B, 0.5, "dream", "levanta ela"),
    ("6621", 5.2, 4*B, 0.5, "dream", "giro"),
    ("6623", 5.3, 4*B, 0.5, "dream", "abraço"),
    ("6627", 4.0, 3*B, 1.0, "",      "abraço rindo"),
    ("6624", 0.4, 11*B, 1.0, "push",  "coração na barriga - final"),
]
