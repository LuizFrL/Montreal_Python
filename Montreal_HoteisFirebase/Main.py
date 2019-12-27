from Montreal_HoteisFirebase.Firebase.Firebase import FirebaseHoteis
from Montreal_HoteisFirebase.Banco_Hoteis.Hoteis import HoteisInfDAO


firebase = FirebaseHoteis()
banco_hoteis = HoteisInfDAO()

dat = banco_hoteis.parceiros()
print(dat)
firebase.set_data('hoteis', dat)
