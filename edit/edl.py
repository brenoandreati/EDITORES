# Roteiro do vídeo de revelação de gravidez (v2)
# BPM 96 -> 1 batida = 0.625s. Durações de saída em múltiplos de batida.
# v2: abertura mais longa (40s sem teste), irmão maior removido/recortado,
#     nenhum frame com teste antes da revelação.
B = 0.625

# (take, inicio_no_take_s, duracao_saida_s, velocidade, efeito, nota)
#  efeito: "" | "punch" (zoom de impacto) | "dream" (câmera lenta com brilho) | "push" (zoom lento)
#          | "flash" (flash branco no fim) | "low" (corta céu)
#          | "crop:zoom:x:y" (reenquadra; x/y de 0 a 1 = posição do recorte)
EDL = [
    # ATO 1 - o casal (sem teste: 6597 só em janelas verificadas e com a parte de baixo cortada)
    ("6598", 0.3, 4*B, 1.0, "low",             "olhando um pro outro"),
    ("6597", 4.5, 3*B, 1.0, "crop:1.3:0.5:0.6", "ela rindo, mão no cabelo"),
    ("6598", 4.2, 3*B, 1.0, "low",             "beijo"),
    ("6597", 12.4, 3*B, 1.0, "crop:1.3:0.5:0.6", "beijo de nariz (close)"),
    ("6598", 6.4, 2*B, 1.0, "low",             "risada"),
    # (transição) pega o boné e gargalham
    ("6601", 4.0, 3*B, 1.0, "",                "ele pega o boné"),
    # ATO 2 - os bonés
    ("6601", 6.0, 3*B, 1.0, "",                "gargalhada no lençol"),
    ("6599", 4.3, 3*B, 1.0, "",                "ela coloca o boné nele"),
    ("6600", 0.0, 3*B, 1.0, "low",             "ajeita o boné dele (outro ângulo)"),
    ("6602", 3.8, 3*B, 1.0, "",                "ele coloca o boné nela"),
    ("6602", 8.0, 3*B, 1.0, "",                "ela ajeita o dele"),
    ("6599", 9.0, 3*B, 1.0, "",                "os dois de boné"),
    ("6602", 11.6, 2*B, 1.0, "punch",          "os dois sorrindo"),
    ("6605", 0.4, 4*B, 1.0, "",                "chamam o pequeno"),
    # ATO 3 - o menino pequeno (sem o irmão maior)
    ("6606", 5.9, 5*B, 0.75, "",               "ele chega correndo"),
    ("6606", 8.4, 3*B, 1.0, "",                "abraço na mãe"),
    ("6606", 10.6, 5*B, 1.0, "",               "colocam o boné nele"),
    ("6606", 14.0, 3*B, 1.0, "",               "os três sorrindo"),
    ("6611", 0.4, 3*B, 1.0, "crop:1.3:0.2:0.6", "abraço no colo do pai"),
    ("6606", 16.3, 3*B, 1.0, "flash",          "os três de boné"),
    # ATO 4 - REVELAÇÃO (começa no pequeno trazendo o teste)
    ("6610", 3.4, 4*B, 0.5, "dream",           "pequeno vem com o teste (lento)"),
    ("6610", 9.7, 3*B, 1.0, "punch",           "mostra o teste pra câmera"),
    ("6610", 19.0, 4*B, 1.0, "",               "segura o teste sorrindo"),
    ("6625", 9.0, 5*B, 1.0, "",                "casal mostra o teste"),
    ("6616", 11.6, 4*B, 0.5, "dream",          "pai beija a barriga (lento)"),
    ("6626", 4.3, 3*B, 1.0, "",                "beijo na barriga"),
    ("6629", 20.6, 5*B, 1.0, "crop:1.35:0.85:0.7", "pequeno beija a barriga"),
    ("6626", 6.8, 4*B, 0.5, "dream",           "ela joga o cabelo (lento)"),
    # ATO 5 - corrida em câmera lenta
    ("6619", 3.0, 6*B, 0.5, "dream",           "corrida e pulo no colo"),
    ("6618", 8.3, 4*B, 0.5, "dream",           "levanta ela"),
    ("6621", 5.2, 4*B, 0.5, "dream",           "giro"),
    ("6623", 5.3, 4*B, 0.5, "dream",           "abraço"),
    ("6627", 4.0, 3*B, 1.0, "",                "abraço rindo"),
    ("6624", 0.2, 11*B, 1.0, "push",           "coração na barriga - final"),
]

# compassos (4 batidas) usados pela trilha
REVEAL_BAR = 16   # início da revelação
DREAM_BAR = 24    # início da câmera lenta
