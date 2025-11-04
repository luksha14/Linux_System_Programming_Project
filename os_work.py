import math, os, signal, threading, time, platform, traceback
from threading import Timer, Semaphore

# === GLOBALNE VARIJABLE ===
semafor = Semaphore(1)
brojac = 1
suma = 0
kraj = False

# === FUNKCIJE ===
def proc_extraction(pid_str):
    try:
        with open(f"/proc/{pid_str}/stat") as f:
            stat = f.read().split()
        with open(f"/proc/{pid_str}/status") as f:
            lines = f.readlines()
        uid = [l for l in lines if l.startswith("Uid:")][0].split()[1]
        return stat[0], stat[3], stat[17], uid
    except Exception:
        return None, None, None, None


def ispis(dijete_ispis, roditelj_ispis, grandparent_ispis, dijete_pid, roditelj_pid):
    print("PID\tPPID\tKorisnik\tPrioritet")
    for red in sorted([grandparent_ispis, roditelj_ispis, dijete_ispis]):
        print(red)


def upravljacHUP(signum, frame):
    print(f"Primljen signal SIGHUP ({signum})")
    home = os.path.expanduser("~")
    with open(f"{home}/Desktop/stacking.txt", "a") as f:
        f.write("".join(traceback.format_stack()))
        f.write("\n---\n")
    print("Stack zapisano na Desktop.")


def upravljacABRT(signum, frame):
    print(f"Primljen signal SIGABRT ({signum})")
    home = os.path.expanduser("~")
    with open(f"{home}/Desktop/stacking.txt", "a") as f:
        f.write("".join(traceback.format_stack()))
        f.write("\n---\n")
    print("Stack zapisano na Desktop.")


def korijen(prvi_dio, drugi_dio, treci_dio):
    global brojac, suma
    home = os.path.expanduser("~")
    with open(f"{home}/step_by_step.txt", "a") as f:
        while True:
            semafor.acquire()
            if brojac > prvi_dio + drugi_dio + treci_dio:
                semafor.release()
                break
            x = brojac
            suma += math.sqrt(x)
            f.write(f"{x} --> {suma}\n")
            brojac += 1
            semafor.release()


# --- NOVO: FUNKCIONALNOST 4 ---

division = []
lock = threading.Lock()
done_first_two = threading.Event()

def djelitelji_podrucje(start, end):
    """Računa sve djelitelje brojeva u intervalu i dodaje ih u zajedničku listu."""
    print(f"{threading.current_thread().name} započinje rad.")
    for broj in range(start, end + 1):
        for d in range(1, broj + 1):
            if broj % d == 0:
                with lock:
                    division.append(d)
    print(f"{threading.current_thread().name} završava rad.")


def neparni_brojevi():
    """Treća dretva – čeka prve dvije i zatim filtrira neparne brojeve."""
    print(f"{threading.current_thread().name} čeka dovršetak prethodnih dretvi...")
    done_first_two.wait()
    start_time = time.time()
    print(f"{threading.current_thread().name} započinje rad.")
    neparni = [x for x in division if x % 2 != 0]
    print(f"Neparni brojevi ({len(neparni)} ukupno):")
    print(neparni[:50], "...")  # ispis samo prvih 50 radi preglednosti
    trajanje = time.time() - start_time
    print(f"{threading.current_thread().name} završava rad (trajanje: {trajanje:.2f}s).")


# === PROGRAM START ===
print("Dobrodošli u Linux Python Program!")
print("OS:", platform.system(), platform.release())
print("Radni direktorij:", os.getcwd())

while not kraj:
    print("\n--- GLAVNI IZBORNIK ---")
    print("1 - Procesi")
    print("2 - Signali")
    print("3 - Dretve (korijeni)")
    print("4 - Djelitelji i neparni brojevi")
    print("stop / zaustavi - kraj")

    izbor = input("Odabir: ").strip().lower()

    # 1. PROCESI
    if izbor == "1":
        while True:
            n = input("Unesite broj (1-20): ").strip()
            if not n: continue
            try:
                n = int(n)
                if 1 <= n <= 20: break
            except: pass
            print("Pogrešan unos.")
        pid = os.fork()
        if pid == 0:
            home = os.path.expanduser("~")
            os.chdir(home)
            pid_d = os.getpid()
            dijete_pid, dijete_ppid, dijete_priority, dijete_uid = proc_extraction(str(pid_d))
            roditelj_pid, roditelj_ppid, roditelj_priority, roditelj_uid = proc_extraction(str(dijete_ppid))
            grandparent_pid, grandparent_ppid, grandparent_priority, grandparent_uid = proc_extraction(str(roditelj_ppid))
            ispis(f"{dijete_pid}\t{dijete_ppid}\t{dijete_uid}\t{dijete_priority}",
                  f"{roditelj_pid}\t{roditelj_ppid}\t{roditelj_uid}\t{roditelj_priority}",
                  f"{grandparent_pid}\t{grandparent_ppid}\t{grandparent_uid}\t{grandparent_priority}",
                  int(dijete_pid), int(roditelj_pid))
            Timer(n, lambda: None).start()
            os._exit(0)
        else:
            os.wait()
            print("Proces dijete završio.\n")

    # 2. SIGNALI
    elif izbor == "2":
        interpretor_pid = os.getpid()
        signal.signal(signal.SIGHUP, upravljacHUP)
        signal.signal(signal.SIGABRT, upravljacABRT)
        ignorirani = {10, 12, 18}
        while True:
            unos = input("Unesite naziv signala (npr. INT ili SIGTERM): ").upper().strip()
            if not unos: continue
            if not unos.startswith("SIG"):
                unos = "SIG" + unos
            try:
                br = signal.Signals[unos].value
                if br in ignorirani:
                    print("Signal se ignorira.")
                else:
                    os.kill(interpretor_pid, br)
                break
            except Exception:
                print("Nepoznat signal.")

    # 3. DRETVE - KORIJENI
    elif izbor == "3":
        while True:
            try:
                m = int(input("Unesite broj > 3000000: "))
                if m > 3000000: break
            except: pass
            print("Pogrešan unos.")
        open(os.path.expanduser("~/step_by_step.txt"), "w").close()
        d = [m//3, m//3, m - 2*(m//3)]
        t1 = threading.Thread(target=korijen, args=(d[0], d[1], d[2]))
        t2 = threading.Thread(target=korijen, args=(d[0], d[1], d[2]))
        t3 = threading.Thread(target=korijen, args=(d[0], d[1], d[2]))
        for t in (t1,t2,t3): t.start()
        for t in (t1,t2,t3): t.join()
        print("Gotovo, zapisano u step_by_step.txt")

    # 4. DJELITELJI + NEPARNI BROJEVI
    elif izbor == "4":
        while True:
            try:
                k = int(input("Unesite broj između 1300 i 130000: "))
                if 1300 <= k <= 130000: break
            except: pass
            print("Pogrešan unos.")
        polovica = k // 2
        t1 = threading.Thread(target=djelitelji_podrucje, args=(1, polovica))
        t2 = threading.Thread(target=djelitelji_podrucje, args=(polovica + 1, k))
        t3 = threading.Thread(target=neparni_brojevi)

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        done_first_two.set()  
        t3.join()

    elif izbor in ["stop", "zaustavi"]:
        kraj = True
        print("Doviđenja!")

    else:
        print("Neispravan unos.")
