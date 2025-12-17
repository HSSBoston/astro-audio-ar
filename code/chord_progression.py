
def generateCho
    m1 = stream.Measure()
    m1.TimeSignature = meter.TimeSignature()
    m1.keySignature = key.Key(KEY_CHOICE)
    temp = tempo.MetronomeMark("adagio")
    m1.append(temp)
    m1.rightBarLine = bar.Barline("final")

    if numOfChords == 1:
        chord1 = random.choice(CHORD_CHOICES)
        print(romanToChordTones[chord1])

        c1 = chord.Chord(romanToChordTones[chord1])
        c1.quarterLength = 4
        m1.append(oneChord)

    if numOfChords == 2:
        chord1 = random.choice(CHORD_CHOICES)
        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])

        c1 = chord.Chord(romanToChordTones[chord1])
        c1.quarterLength = 2
        c2 = chord.Chord(romanToChordTones[chord2])
        c2.quarterLength = 2
        m1.append(c1)
        m1.append(c2)

    if numOfChords == 3:
        chord1 = random.choice(CHORD_CHOICES)
        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])
        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])

        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])

        randomInt = random.randint(0,1)
        if randomInt <= 0.33:
            c1.quarterLength = 2
            c2.quarterLength = 1
            c3.quarerLength = 1
        elif randomInt <= 0.66:
            c1.quarterLength = 1
            c2.quarterLength = 2
            c3.quarerLength = 1
        else:
            c1.quarterLength = 1
            c2.quarterLength = 1
            c3.quarerLength = 2

        m1.append(c1)
        m1.append(c2)
        m1.append(c3)

    if numOfChords == 4:

        chord1 = random.choice(CHORD_CHOICES)
        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])
        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])
        chord4 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord3]])

        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])
        c4 = chord.Chord(romanToChordTones[chord4])

        c1.quarterLength = 1
        c2.quarterLength = 1
        c3.quarterLength = 1
        c4.quarterLength = 1

        m1.append(c1)
        m1.append(c2)
        m1.append(c3)
        m1.append(c4)

    part.append(m1)