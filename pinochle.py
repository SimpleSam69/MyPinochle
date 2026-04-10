import random, time, os, sys

def clear(): 
    os.system('clear')

RESET = "\033[0m"
DARK_GREY = "\033[90m"
RED = "\033[91m"
PLAIN_SUITS = {'spades': '♠', 'hearts': '♥', 'diamonds': '♦', 'clubs': '♣'}
COLORED_SUITS = {
    'spades': DARK_GREY + '♠' + RESET,
    'hearts': RED + '♥' + RESET,
    'diamonds': RED + '♦' + RESET,
    'clubs': DARK_GREY + '♣' + RESET
}
RANKS = ['9', 'J', 'Q', 'K', '10', 'A']
VALUES = {'9': 0, '10': 10, 'J': 2, 'Q': 3, 'K': 4, 'A': 11}

class Card:
    def __init__(self, r, s): 
        self.rank, self.suit, self.value = r, s, VALUES[r]
    def __repr__(self): 
        return f"{self.rank}{COLORED_SUITS[self.suit]}"

class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for _ in range(2) for s in PLAIN_SUITS for r in RANKS]
        random.shuffle(self.cards)
    def deal(self, n): 
        return self.cards[:n]

def animate_shuffle():
    for _ in range(3):
        clear()
        print("\n" * 8)
        suits_str = DARK_GREY + "♠" + RED + "♥" + RED + "♦" + DARK_GREY + "♣" + RESET
        for i in range(4):
            rot = suits_str[i*5:] + suits_str[:i*5]
            print(" " * 15 + rot + "  Shuffling...")
            time.sleep(0.1)
            clear()
            print("\n" * 8)

def show_hand(h, n="Your"):
    print(f"\n{n} Hand:")
    by = {}
    for c in h: 
        by.setdefault(c.suit, []).append(c)
    for s in ['spades', 'hearts', 'diamonds', 'clubs']:
        if s in by: 
            cards = " ".join(f"{c.rank}{COLORED_SUITS[s]}" for c in sorted(by[s], key=lambda x: RANKS.index(x.rank)))
            print(f"  {COLORED_SUITS[s]} {cards}")

def get_meld(h, t):
    m, r = 0, {}
    for c in h: 
        r[c.rank] = r.get(c.rank, 0) + 1
    for x, p in [('A',10),('K',8),('Q',6),('J',4)]:
        if r.get(x, 0) >= 4: 
            m += p
    jd = sum(1 for c in h if c.rank == 'J' and c.suit == 'diamonds')
    qs = sum(1 for c in h if c.rank == 'Q' and c.suit == 'spades')
    m += min(jd, qs) * 4
    for s in PLAIN_SUITS:
        k = any(c.rank == 'K' and c.suit == s for c in h)
        q = any(c.rank == 'Q' and c.suit == s for c in h)
        if k and q: 
            m += 8 if s == t else 4
    return m
def play_trick(ph, ch, trump, leader):
    trick, led = [], None
    if leader == "player":
        show_hand(ph)
        while True:
            i = input("Play (e.g., A♠ or AS): ").upper()
            if i == 'Q':
                print("\nQuitting game...")
                sys.exit(0)
            matched = False
            for j, c in enumerate(ph):
                rank_match = i.startswith(c.rank)
                suit_match = c.suit[0].upper() in i or PLAIN_SUITS[c.suit] in i
                if rank_match and suit_match:
                    card = ph.pop(j)
                    trick.append(("player", card))
                    led = c.suit
                    print(f"You: {card}")
                    matched = True
                    break
            if not matched:
                print("Invalid")
                continue
            break
        v = [c for c in ch if c.suit == led] or ch
        cc = random.choice(v)
        ch.remove(cc)
        trick.append(("computer", cc))
        print(f"Computer: {cc}")
    else:
        cc = random.choice(ch)
        ch.remove(cc)
        trick.append(("computer", cc))
        led = cc.suit
        print(f"Computer leads: {cc}")
        show_hand(ph)
        v = [c for c in ph if c.suit == led]
        if v: 
            print(f"Must follow {COLORED_SUITS[led]}")
        while True:
            i = input("Play: ").upper()
            if i == 'Q':
                print("\nQuitting game...")
                sys.exit(0)
            matched = False
            for j, c in enumerate(ph):
                rank_match = i.startswith(c.rank)
                suit_match = c.suit[0].upper() in i or PLAIN_SUITS[c.suit] in i
                if rank_match and suit_match:
                    if v and c not in v: 
                        print("Follow suit!")
                        break
                    card = ph.pop(j)
                    trick.append(("player", card))
                    print(f"You: {card}")
                    matched = True
                    break
            if not matched:
                print("Invalid")
                continue
            break
    w, wc = trick[0]
    for p, c in trick[1:]:
        if c.suit == trump and wc.suit != trump: 
            w, wc = p, c
        elif c.suit == wc.suit and RANKS.index(c.rank) > RANKS.index(wc.rank): 
            w, wc = p, c
    print(f"Winner: {w}")
    time.sleep(0.5)
    return w
def main():
    print(DARK_GREY + "=" * 40 + RESET)
    print("  " + RED + "Samuels Badass Pinochle" + RESET)
    print("        " + DARK_GREY + "♠" + RESET + " " + RED + "♥♦" + RESET + " " + DARK_GREY + "♣" + RESET)
    print(DARK_GREY + "=" * 40 + RESET)
    ps, cs = 0, 0
    while True:
        animate_shuffle()
        d = Deck()
        ph = sorted(d.deal(12), key=lambda c: (list(PLAIN_SUITS).index(c.suit), RANKS.index(c.rank)))
        ch = sorted(d.deal(12), key=lambda c: (list(PLAIN_SUITS).index(c.suit), RANKS.index(c.rank)))
        
        print("\n--- Your Cards ---")
        show_hand(ph, "Your")
        
        print("\n--- Bidding ---")
        cb = random.choice([0, 20, 25, 30])
        print(f"Computer: {'Pass' if cb == 0 else cb}")
        while True:
            try:
                pb = input("Your bid (0=Pass, 20-50) or Q to quit: ").upper()
                if pb == 'Q':
                    print("\nQuitting game...")
                    sys.exit(0)
                pb = int(pb)
                if pb == 0 or 20 <= pb <= 50: 
                    break
            except: 
                pass
            print("Invalid")
        if pb == 0 and cb == 0: 
            print("Both passed")
            continue
        bidder = "player" if pb > cb else "computer"
        print(f"{bidder} wins bid")
        if bidder == "player":
            print(f"\n1.{DARK_GREY}♠{RESET}  2.{RED}♥{RESET}  3.{RED}♦{RESET}  4.{DARK_GREY}♣{RESET}")
            trump_choice = input("Trump (1-4) or Q to quit: ").upper()
            if trump_choice == 'Q':
                print("\nQuitting game...")
                sys.exit(0)
            trump = list(PLAIN_SUITS)[int(trump_choice) - 1]
        else: 
            trump = random.choice(list(PLAIN_SUITS))
        print(f"Trump: {COLORED_SUITS[trump]} {trump}")
        print("\n--- Meld ---")
        pm, cm = get_meld(ph, trump), get_meld(ch, trump)
        print(f"Your meld: {pm}, Computer meld: {cm}")
        ps, cs = ps + pm, cs + cm
        input("Press Enter for tricks...")
        leader, pt, ct = bidder, 0, 0
        while ph and ch:
            clear()
            print(f"Score: You {ps} | Comp {cs}")
            print(f"Tricks: You {pt} | Comp {ct}")
            w = play_trick(ph, ch, trump, leader)
            if w == "player": 
                pt += 1
            else: 
                ct += 1
            leader = w
            input("Continue...")
        ps, cs = ps + pt, cs + ct
        print(f"\nFinal: You {ps} | Comp {cs}")
        again = input("Again? (y/n/q): ").lower()
        if again == 'q' or again == 'n':
            break
    print("Thanks for playing!")

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt: 
        print("\nBye!")
