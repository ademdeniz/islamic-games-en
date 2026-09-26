"""Build work/ramazanski-put.en.html from work/ramazanski-put.bs.html.
Run from project root:  python3 tools/tr/ramazanski-put_build.py && python3 tools/skel.py build ramazanski-put"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'ramazanski-put'
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()

UI = [
    ('<title>Ramazanski put</title>', '<title>The Ramadan Path</title>'),
    ('<h1>🌙 RAMAZANSKI PUT</h1>', '<h1>🌙 THE RAMADAN PATH</h1>'),
    ('<div class="sub">Kviz znanja o ramazanu</div>', '<div class="sub">A quiz about Ramadan</div>'),
    ('⭐ Bodovi: <span', '⭐ Points: <span'),
    ('✅ Tačno: <span', '✅ Correct: <span'),
    ('❓ Pitanje: <span', '❓ Question: <span'),
    ('<h2>Stigao si do kraja Ramazanskog puta!</h2>', '<h2>You reached the end of the Ramadan Path!</h2>'),
    ('<p>Tačnih odgovora: <b id="fc"></b> od 20</p>', '<p>Correct answers: <b id="fc"></b> out of 20</p>'),
    ('<p>Osvojeno bodova: <b id="fs"></b></p>', '<p>Points earned: <b id="fs"></b></p>'),
    ('>Igraj ponovo</button>', '>Play again</button>'),
    ('Pri svakom pokretanju biraju se druga pitanja i miješaju odgovori.',
     'Every new game picks different questions and shuffles the answers.'),
    ('"✅ Tačno! +10 bodova"', '"✅ Correct! +10 points"'),
    ('"❌ Netačno! −5 bodova"', '"❌ Wrong! −5 points"'),
]
DELETE = ['<div class="author">Pripremio Abdo ef. Rekić</div>']

EN = [
    ("Which is the month of fasting in Islam?", ["Muharram", "Ramadan", "Rajab", "Shaʿban"]),
    ("Which fast is compulsory (fard) for Muslims who meet the conditions?", ["Fasting the month of Ramadan", "Fasting every Monday", "Fasting six days of Shawwal", "Fasting on the Day of Arafah"]),
    ("What is the meal eaten before the daily fast begins called?", ["Iftar", "Suhur", "Maghrib", "Sadaqah"]),
    ("What is the meal with which a fasting person ends the daily fast called?", ["Suhur", "Iftar", "Lunch", "Zakah"]),
    ("When does the daily Ramadan fast begin?", ["At sunrise", "After the Dhuhr prayer", "At the start of dawn (Fajr time)", "After the Fajr prayer"]),
    ("When does the daily Ramadan fast end?", ["At noon", "At sunset", "After Isha", "At midnight"]),
    ("What is the prayer specially prayed at night in Ramadan called?", ["Tarawih prayer", "Janazah (funeral) prayer", "Istikharah prayer", "Eid prayer"]),
    ("Which holy book began to be revealed in the month of Ramadan?", ["Tawrat", "Zabur", "Qur’an", "Injil"]),
    ("What is the night that is better than a thousand months called?", ["Laylat al-Bara’ah", "Laylat al-Qadr", "Laylat ar-Ragha’ib", "Laylat al-Miʿraj"]),
    ("Which surah talks especially about Laylat al-Qadr?", ["Al-Qadr", "Al-Fatihah", "An-Nas", "Al-Falaq"]),
    ("In which part of Ramadan do Muslims especially look for Laylat al-Qadr?", ["In the first ten nights", "In the middle of the month", "In the last ten nights", "Only on the first night"]),
    ("What does niyyah for fasting mean?", ["The intention to fast", "A special Ramadan meal", "Giving sadaqah (charity)", "Calling the Adhan"]),
    ("Which of these breaks the fast if done on purpose during fasting time?", ["Sleeping", "Eating on purpose", "Reciting the Qur’an", "Giving sadaqah (charity)"]),
    ("What should a fasting person do if they eat or drink something by forgetting?", ["Carry on fasting once they remember", "Break the fast straight away", "Not fast for the rest of Ramadan", "Give Zakah"]),
    ("What is the good practice at iftar?", ["Delaying iftar for no reason", "Breaking the fast as soon as the time comes", "Breaking the fast before sunset", "Skipping iftar"]),
    ("What is good to do about suhur?", ["Skip it completely", "Get up for suhur", "Eat after sunrise", "Eat only after noon"]),
    ("Which deed is especially praiseworthy in Ramadan?", ["Reciting the Qur’an", "Arguing", "Backbiting", "Wasting food"]),
    ("What is the compulsory giving to certain groups of people, when the conditions are met, called?", ["Zakah", "Iftar", "Suhur", "Takbir"]),
    ("What is the special charity linked to the end of Ramadan called?", ["Sadaqat al-Fitr (Zakat al-Fitr)", "Mahr", "Qurbani", "Kaffarah"]),
    ("Which Eid comes after the end of Ramadan?", ["Eid al-Adha (Qurban Bayram)", "Eid al-Fitr (Ramadan Bayram)", "The Islamic (Hijri) New Year", "Mawlid"]),
    ("Which prayer is prayed on the morning of the first day of Eid al-Fitr?", ["Tarawih prayer", "Eid prayer", "Witr prayer", "Janazah (funeral) prayer"]),
    ("Besides staying away from food and drink, what does fasting teach a believer?", ["Patience and self-control", "Wastefulness", "Anger", "Carelessness"]),
    ("How should we behave towards others while fasting?", ["Kindly and patiently", "Quarrelsomely", "Rudely", "Arrogantly"]),
    ("What is especially valuable to do for the poor and needy in Ramadan?", ["Help them and give sadaqah", "Avoid them", "Ask them for gifts", "Forget about them"]),
    ("Which dua and worship (ibadah) is especially important all through Ramadan?", ["Turning to Allah with dua", "Only talking about food", "Sleeping all day", "Giving up Salah"]),
    ("What is staying in the mosque for worship, especially in the last ten days of Ramadan, called?", ["Iʿtikaf", "Tayammum", "Iqamah", "Talbiyah"]),
    ("What does a Muslim try to do more of in Ramadan?", ["Good deeds", "Arguments", "Wasting time", "Bad language"]),
    ("Besides our stomach, what should we guard while fasting?", ["Our tongue and behaviour", "Only our clothes", "Only our shoes", "Only our sleeping time"]),
    ("Which prayers stay compulsory during Ramadan too?", ["The five daily prayers", "Only Tarawih", "Only the Eid prayer", "Only Witr"]),
    ("How does our “Ramadan Path” end after the month of fasting?", ["With Eid al-Fitr", "With the start of Rajab", "With Qurbani", "With the Hijrah"]),
    ("What is the ruling on fasting the month of Ramadan for a Muslim who meets the conditions?", ["Fard (compulsory)", "Sunnah", "Makruh (disliked)", "Mubah (allowed)"]),
    ("Who has to fast in Ramadan?", ["Every child, whatever their age", "A Muslim who is adult (baligh), sane and healthy", "Only the imam", "Only older people"]),
    ("Does a child who has not yet reached adulthood (baligh) have to fast like an adult?", ["Yes, always", "No, but they slowly get used to fasting", "Only on Fridays", "Only on the last day of Ramadan"]),
    ("Who may leave the fast for a while for a valid reason?", ["A sick person whom fasting would harm or make worse", "Anyone who doesn’t want to get up for suhur", "Someone who wants to sleep longer", "Someone who wants a rest"]),
    ("What does a sick person do who did not fast because of a short illness and later gets better?", ["They don’t need to do anything", "They make up the missed days", "They only pray two rakʿahs", "They give Qurbani"]),
    ("What is the fast that makes up missed days of Ramadan (for a valid reason) called?", ["Nafl", "Qada", "Tarawih", "Iʿtikaf"]),
    ("Must the qada of missed Ramadan days be fasted straight away, day after day?", ["It must always be without a break", "It doesn’t have to be in a row", "It can only be done in Ramadan", "It can never be made up"]),
    ("Who may put off the Ramadan fast because of travelling?", ["A musafir (traveller)", "Anyone who leaves the house", "Only a bus driver", "Nobody"]),
    ("What must a musafir do who, for a valid reason, does not fast some days of Ramadan?", ["Make them up later", "Nothing", "Give Qurbani", "Repeat their prayers"]),
    ("What does a person do who cannot fast because of old age or a lasting illness and has no hope of making it up later?", ["They give fidyah", "They must fast whatever the harm", "They do nothing", "They give Zakah instead of fasting"]),
    ("What is fidyah in connection with fasting?", ["A payment that, by the rules, feeds a poor person", "Another name for suhur", "A voluntary prayer", "A dua before iftar"]),
    ("Does a person who expects to be able to fast later replace the missed days with fidyah only?", ["Yes", "No, the missed days must be made up by fasting", "Only if they want to", "Only on Fridays"]),
    ("When a woman does not fast because of hayd or nifas, what does she do about the missed Ramadan fasts?", ["She makes them up after Ramadan", "She doesn’t make them up", "She only gives sadaqah", "She prays extra prayers instead of fasting"]),
    ("May a pregnant or breastfeeding woman leave the fast if there is a real worry for her health or her baby’s?", ["Yes, following the rules on making up the fast", "Never", "Only on the first day of Ramadan", "Only if she is travelling"]),
    ("What does kaffarah mean for a Ramadan fast broken on purpose, in the cases where kaffarah is required?", ["A special Shariʿah penalty (atonement), as well as having to make up that day", "A voluntary iftar", "Charity before suhur", "Eid prayer"]),
    ("According to the Hanafi madhhab, when can kaffarah become required?", ["When a person, with no valid excuse, breaks a Ramadan fast they have started on purpose", "When they drink water by forgetting", "When they sleep through suhur", "When they have a bath while fasting"]),
    ("Is kaffarah required if a fasting person eats or drinks by forgetting?", ["Yes", "No; once they remember, they carry on fasting", "Only if they drank water", "Only if they ate"]),
    ("What is the kaffarah for a Ramadan fast broken on purpose?", ["Fasting two months in a row", "Fasting only one day", "Praying two rakʿahs", "Giving one iftar to a family"]),
    ("With kaffarah, is the fasting day that was broken on purpose also made up?", ["Yes, that day is also made up", "No", "Only if it is a Friday", "Only if it is the last day of Ramadan"]),
    ("What should a person with a valid excuse for not fasting for a while do when the excuse ends?", ["Make up the missed days", "Forget the missed days", "Fast only six days of Shawwal", "Give Qurbani"]),
]

out = src
for bs in DELETE:
    assert out.count(bs) == 1, bs
    out = out.replace(bs, '')
for bs, en in UI:
    assert out.count(bs) == 1, (out.count(bs), bs)
    out = out.replace(bs, en)

i = out.index('const BANK=') + len('const BANK=')
bank, end = json.JSONDecoder().raw_decode(out[i:])
assert len(bank) == len(EN) == 50
assert json.dumps(bank, ensure_ascii=False) == out[i:i + end]
new = []
for x, (q, a) in zip(bank, EN):
    assert len(a) == len(x['a']) == 4 and len(set(a)) == 4, q
    for s in [q] + a:
        assert '"' not in s and '\\' not in s and "'" not in s, s
    new.append({'q': q, 'a': a, 'c': x['c']})
out = out[:i] + json.dumps(new, ensure_ascii=False) + out[i + end:]
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(out)
print('ok', len(new))
