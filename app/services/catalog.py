# Valores iniciais informados para o Studio AS. Revise antes de publicar.
SERVICES = [
 {"name":"Escova P","price":25,"duration_minutes":45},
 {"name":"Escova M","price":30,"duration_minutes":60},
 {"name":"Escova G","price":35,"duration_minutes":75},
 {"name":"Corte + escova","price":50,"duration_minutes":90},
 {"name":"Selagem P","price":150,"duration_minutes":180},
 {"name":"Selagem M","price":200,"duration_minutes":210},
 {"name":"Selagem G","price":250,"duration_minutes":240},
 {"name":"Mechas P","price":150,"duration_minutes":210},
 {"name":"Mechas M","price":200,"duration_minutes":240},
 {"name":"Mechas G","price":250,"duration_minutes":300},
 {"name":"Hidratação","price":25,"duration_minutes":45},
 {"name":"Reconstrução","price":50,"duration_minutes":60},
 {"name":"Sobrancelha","price":20,"duration_minutes":30},
 {"name":"Sobrancelha com henna","price":30,"duration_minutes":45},
 {"name":"Cílios","price":70,"duration_minutes":90},
 {"name":"Micropigmentação","price":250,"duration_minutes":150},
 {"name":"Depilação axila","price":20,"duration_minutes":20},
 {"name":"Depilação meia perna","price":20,"duration_minutes":30},
 {"name":"Depilação perna completa","price":40,"duration_minutes":45},
 {"name":"Depilação buço","price":10,"duration_minutes":15},
 {"name":"Depilação face","price":50,"duration_minutes":45},
 {"name":"Penteado","price":70,"duration_minutes":90},
 {"name":"Maquiagem","price":50,"duration_minutes":60}
]

def find_service(name: str):
    target = name.casefold().strip()
    return next((s for s in SERVICES if s["name"].casefold() == target), None)
