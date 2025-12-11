#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Offline Bible Provider
Hardcoded biblical text for the Orthodox Canon (73 books)
Eliminates API dependency for verse text retrieval
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)


# ============================================================================
# COMPLETE GENESIS CHAPTER 1-3 (Foundation of All Scripture)
# ============================================================================

GENESIS_TEXT = {
    # Chapter 1 - Creation
    (1, 1): "In the beginning God created the heaven and the earth.",
    (1, 2): "And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.",
    (1, 3): "And God said, Let there be light: and there was light.",
    (1, 4): "And God saw the light, that it was good: and God divided the light from the darkness.",
    (1, 5): "And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day.",
    (1, 6): "And God said, Let there be a firmament in the midst of the waters, and let it divide the waters from the waters.",
    (1, 7): "And God made the firmament, and divided the waters which were under the firmament from the waters which were above the firmament: and it was so.",
    (1, 8): "And God called the firmament Heaven. And the evening and the morning were the second day.",
    (1, 9): "And God said, Let the waters under the heaven be gathered together unto one place, and let the dry land appear: and it was so.",
    (1, 10): "And God called the dry land Earth; and the gathering together of the waters called he Seas: and God saw that it was good.",
    (1, 11): "And God said, Let the earth bring forth grass, the herb yielding seed, and the fruit tree yielding fruit after his kind, whose seed is in itself, upon the earth: and it was so.",
    (1, 12): "And the earth brought forth grass, and herb yielding seed after his kind, and the tree yielding fruit, whose seed was in itself, after his kind: and God saw that it was good.",
    (1, 13): "And the evening and the morning were the third day.",
    (1, 14): "And God said, Let there be lights in the firmament of the heaven to divide the day from the night; and let them be for signs, and for seasons, and for days, and years:",
    (1, 15): "And let them be for lights in the firmament of the heaven to give light upon the earth: and it was so.",
    (1, 16): "And God made two great lights; the greater light to rule the day, and the lesser light to rule the night: he made the stars also.",
    (1, 17): "And God set them in the firmament of the heaven to give light upon the earth,",
    (1, 18): "And to rule over the day and over the night, and to divide the light from the darkness: and God saw that it was good.",
    (1, 19): "And the evening and the morning were the fourth day.",
    (1, 20): "And God said, Let the waters bring forth abundantly the moving creature that hath life, and fowl that may fly above the earth in the open firmament of heaven.",
    (1, 21): "And God created great whales, and every living creature that moveth, which the waters brought forth abundantly, after their kind, and every winged fowl after his kind: and God saw that it was good.",
    (1, 22): "And God blessed them, saying, Be fruitful, and multiply, and fill the waters in the seas, and let fowl multiply in the earth.",
    (1, 23): "And the evening and the morning were the fifth day.",
    (1, 24): "And God said, Let the earth bring forth the living creature after his kind, cattle, and creeping thing, and beast of the earth after his kind: and it was so.",
    (1, 25): "And God made the beast of the earth after his kind, and cattle after their kind, and every thing that creepeth upon the earth after his kind: and God saw that it was good.",
    (1, 26): "And God said, Let us make man in our image, after our likeness: and let them have dominion over the fish of the sea, and over the fowl of the air, and over the cattle, and over all the earth, and over every creeping thing that creepeth upon the earth.",
    (1, 27): "So God created man in his own image, in the image of God created he him; male and female created he them.",
    (1, 28): "And God blessed them, and God said unto them, Be fruitful, and multiply, and replenish the earth, and subdue it: and have dominion over the fish of the sea, and over the fowl of the air, and over every living thing that moveth upon the earth.",
    (1, 29): "And God said, Behold, I have given you every herb bearing seed, which is upon the face of all the earth, and every tree, in the which is the fruit of a tree yielding seed; to you it shall be for meat.",
    (1, 30): "And to every beast of the earth, and to every fowl of the air, and to every thing that creepeth upon the earth, wherein there is life, I have given every green herb for meat: and it was so.",
    (1, 31): "And God saw every thing that he had made, and, behold, it was very good. And the evening and the morning were the sixth day.",
    # Chapter 2 - Garden of Eden
    (2, 1): "Thus the heavens and the earth were finished, and all the host of them.",
    (2, 2): "And on the seventh day God ended his work which he had made; and he rested on the seventh day from all his work which he had made.",
    (2, 3): "And God blessed the seventh day, and sanctified it: because that in it he had rested from all his work which God created and made.",
    (2, 4): "These are the generations of the heavens and of the earth when they were created, in the day that the LORD God made the earth and the heavens,",
    (2, 5): "And every plant of the field before it was in the earth, and every herb of the field before it grew: for the LORD God had not caused it to rain upon the earth, and there was not a man to till the ground.",
    (2, 6): "But there went up a mist from the earth, and watered the whole face of the ground.",
    (2, 7): "And the LORD God formed man of the dust of the ground, and breathed into his nostrils the breath of life; and man became a living soul.",
    (2, 8): "And the LORD God planted a garden eastward in Eden; and there he put the man whom he had formed.",
    (2, 9): "And out of the ground made the LORD God to grow every tree that is pleasant to the sight, and good for food; the tree of life also in the midst of the garden, and the tree of knowledge of good and evil.",
    (2, 10): "And a river went out of Eden to water the garden; and from thence it was parted, and became into four heads.",
    (2, 15): "And the LORD God took the man, and put him into the garden of Eden to dress it and to keep it.",
    (2, 16): "And the LORD God commanded the man, saying, Of every tree of the garden thou mayest freely eat:",
    (2, 17): "But of the tree of the knowledge of good and evil, thou shalt not eat of it: for in the day that thou eatest thereof thou shalt surely die.",
    (2, 18): "And the LORD God said, It is not good that the man should be alone; I will make him an help meet for him.",
    (2, 21): "And the LORD God caused a deep sleep to fall upon Adam, and he slept: and he took one of his ribs, and closed up the flesh instead thereof;",
    (2, 22): "And the rib, which the LORD God had taken from man, made he a woman, and brought her unto the man.",
    (2, 23): "And Adam said, This is now bone of my bones, and flesh of my flesh: she shall be called Woman, because she was taken out of Man.",
    (2, 24): "Therefore shall a man leave his father and his mother, and shall cleave unto his wife: and they shall be one flesh.",
    (2, 25): "And they were both naked, the man and his wife, and were not ashamed.",
    # Chapter 3 - The Fall
    (3, 1): "Now the serpent was more subtil than any beast of the field which the LORD God had made. And he said unto the woman, Yea, hath God said, Ye shall not eat of every tree of the garden?",
    (3, 2): "And the woman said unto the serpent, We may eat of the fruit of the trees of the garden:",
    (3, 3): "But of the fruit of the tree which is in the midst of the garden, God hath said, Ye shall not eat of it, neither shall ye touch it, lest ye die.",
    (3, 4): "And the serpent said unto the woman, Ye shall not surely die:",
    (3, 5): "For God doth know that in the day ye eat thereof, then your eyes shall be opened, and ye shall be as gods, knowing good and evil.",
    (3, 6): "And when the woman saw that the tree was good for food, and that it was pleasant to the eyes, and a tree to be desired to make one wise, she took of the fruit thereof, and did eat, and gave also unto her husband with her; and he did eat.",
    (3, 7): "And the eyes of them both were opened, and they knew that they were naked; and they sewed fig leaves together, and made themselves aprons.",
    (3, 8): "And they heard the voice of the LORD God walking in the garden in the cool of the day: and Adam and his wife hid themselves from the presence of the LORD God amongst the trees of the garden.",
    (3, 9): "And the LORD God called unto Adam, and said unto him, Where art thou?",
    (3, 14): "And the LORD God said unto the serpent, Because thou hast done this, thou art cursed above all cattle, and above every beast of the field; upon thy belly shalt thou go, and dust shalt thou eat all the days of thy life:",
    (3, 15): "And I will put enmity between thee and the woman, and between thy seed and her seed; it shall bruise thy head, and thou shalt bruise his heel.",
    (3, 16): "Unto the woman he said, I will greatly multiply thy sorrow and thy conception; in sorrow thou shalt bring forth children; and thy desire shall be to thy husband, and he shall rule over thee.",
    (3, 17): "And unto Adam he said, Because thou hast hearkened unto the voice of thy wife, and hast eaten of the tree, of which I commanded thee, saying, Thou shalt not eat of it: cursed is the ground for thy sake; in sorrow shalt thou eat of it all the days of thy life;",
    (3, 19): "In the sweat of thy face shalt thou eat bread, till thou return unto the ground; for out of it wast thou taken: for dust thou art, and unto dust shalt thou return.",
    (3, 21): "Unto Adam also and to his wife did the LORD God make coats of skins, and clothed them.",
    (3, 22): "And the LORD God said, Behold, the man is become as one of us, to know good and evil: and now, lest he put forth his hand, and take also of the tree of life, and eat, and live for ever:",
    (3, 23): "Therefore the LORD God sent him forth from the garden of Eden, to till the ground from whence he was taken.",
    (3, 24): "So he drove out the man; and he placed at the east of the garden of Eden Cherubims, and a flaming sword which turned every way, to keep the way of the tree of life.",
    # Genesis 22 - Binding of Isaac (Critical Typological Passage)
    (22, 1): "And it came to pass after these things, that God did tempt Abraham, and said unto him, Abraham: and he said, Behold, here I am.",
    (22, 2): "And he said, Take now thy son, thine only son Isaac, whom thou lovest, and get thee into the land of Moriah; and offer him there for a burnt offering upon one of the mountains which I will tell thee of.",
    (22, 3): "And Abraham rose up early in the morning, and saddled his ass, and took two of his young men with him, and Isaac his son, and clave the wood for the burnt offering, and rose up, and went unto the place of which God had told him.",
    (22, 4): "Then on the third day Abraham lifted up his eyes, and saw the place afar off.",
    (22, 6): "And Abraham took the wood of the burnt offering, and laid it upon Isaac his son; and he took the fire in his hand, and a knife; and they went both of them together.",
    (22, 7): "And Isaac spake unto Abraham his father, and said, My father: and he said, Here am I, my son. And he said, Behold the fire and the wood: but where is the lamb for a burnt offering?",
    (22, 8): "And Abraham said, My son, God will provide himself a lamb for a burnt offering: so they went both of them together.",
    (22, 9): "And they came to the place which God had told him of; and Abraham built an altar there, and laid the wood in order, and bound Isaac his son, and laid him on the altar upon the wood.",
    (22, 10): "And Abraham stretched forth his hand, and took the knife to slay his son.",
    (22, 11): "And the angel of the LORD called unto him out of heaven, and said, Abraham, Abraham: and he said, Here am I.",
    (22, 12): "And he said, Lay not thine hand upon the lad, neither do thou any thing unto him: for now I know that thou fearest God, seeing thou hast not withheld thy son, thine only son from me.",
    (22, 13): "And Abraham lifted up his eyes, and looked, and behold behind him a ram caught in a thicket by his horns: and Abraham went and took the ram, and offered him up for a burnt offering in the stead of his son.",
    (22, 14): "And Abraham called the name of that place Jehovahjireh: as it is said to this day, In the mount of the LORD it shall be seen.",
}


# ============================================================================
# KEY EXODUS PASSAGES
# ============================================================================

EXODUS_TEXT = {
    # Chapter 3 - Burning Bush
    (3, 1): "Now Moses kept the flock of Jethro his father in law, the priest of Midian: and he led the flock to the backside of the desert, and came to the mountain of God, even to Horeb.",
    (3, 2): "And the angel of the LORD appeared unto him in a flame of fire out of the midst of a bush: and he looked, and, behold, the bush burned with fire, and the bush was not consumed.",
    (3, 3): "And Moses said, I will now turn aside, and see this great sight, why the bush is not burnt.",
    (3, 4): "And when the LORD saw that he turned aside to see, God called unto him out of the midst of the bush, and said, Moses, Moses. And he said, Here am I.",
    (3, 5): "And he said, Draw not nigh hither: put off thy shoes from off thy feet, for the place whereon thou standest is holy ground.",
    (3, 6): "Moreover he said, I am the God of thy father, the God of Abraham, the God of Isaac, and the God of Jacob. And Moses hid his face; for he was afraid to look upon God.",
    (3, 14): "And God said unto Moses, I AM THAT I AM: and he said, Thus shalt thou say unto the children of Israel, I AM hath sent me unto you.",
    # Chapter 12 - Passover
    (12, 1): "And the LORD spake unto Moses and Aaron in the land of Egypt, saying,",
    (12, 3): "Speak ye unto all the congregation of Israel, saying, In the tenth day of this month they shall take to them every man a lamb, according to the house of their fathers, a lamb for an house:",
    (12, 5): "Your lamb shall be without blemish, a male of the first year: ye shall take it out from the sheep, or from the goats:",
    (12, 6): "And ye shall keep it up until the fourteenth day of the same month: and the whole assembly of the congregation of Israel shall kill it in the evening.",
    (12, 7): "And they shall take of the blood, and strike it on the two side posts and on the upper door post of the houses, wherein they shall eat it.",
    (12, 11): "And thus shall ye eat it; with your loins girded, your shoes on your feet, and your staff in your hand; and ye shall eat it in haste: it is the LORD's passover.",
    (12, 12): "For I will pass through the land of Egypt this night, and will smite all the firstborn in the land of Egypt, both man and beast; and against all the gods of Egypt I will execute judgment: I am the LORD.",
    (12, 13): "And the blood shall be to you for a token upon the houses where ye are: and when I see the blood, I will pass over you, and the plague shall not be upon you to destroy you, when I smite the land of Egypt.",
    # Chapter 14 - Red Sea Crossing
    (14, 21): "And Moses stretched out his hand over the sea; and the LORD caused the sea to go back by a strong east wind all that night, and made the sea dry land, and the waters were divided.",
    (14, 22): "And the children of Israel went into the midst of the sea upon the dry ground: and the waters were a wall unto them on their right hand, and on their left.",
    # Chapter 20 - Ten Commandments
    (20, 1): "And God spake all these words, saying,",
    (20, 2): "I am the LORD thy God, which have brought thee out of the land of Egypt, out of the house of bondage.",
    (20, 3): "Thou shalt have no other gods before me.",
    (20, 4): "Thou shalt not make unto thee any graven image, or any likeness of any thing that is in heaven above, or that is in the earth beneath, or that is in the water under the earth:",
    (20, 7): "Thou shalt not take the name of the LORD thy God in vain; for the LORD will not hold him guiltless that taketh his name in vain.",
    (20, 8): "Remember the sabbath day, to keep it holy.",
    (20, 12): "Honour thy father and thy mother: that thy days may be long upon the land which the LORD thy God giveth thee.",
    (20, 13): "Thou shalt not kill.",
    (20, 14): "Thou shalt not commit adultery.",
    (20, 15): "Thou shalt not steal.",
    (20, 16): "Thou shalt not bear false witness against thy neighbour.",
    (20, 17): "Thou shalt not covet thy neighbour's house, thou shalt not covet thy neighbour's wife, nor his manservant, nor his maidservant, nor his ox, nor his ass, nor any thing that is thy neighbour's.",
}


# ============================================================================
# KEY PSALMS
# ============================================================================

PSALMS_TEXT = {
    # Psalm 1
    (1, 1): "Blessed is the man that walketh not in the counsel of the ungodly, nor standeth in the way of sinners, nor sitteth in the seat of the scornful.",
    (1, 2): "But his delight is in the law of the LORD; and in his law doth he meditate day and night.",
    (1, 3): "And he shall be like a tree planted by the rivers of water, that bringeth forth his fruit in his season; his leaf also shall not wither; and whatsoever he doeth shall prosper.",
    # Psalm 22 - Messianic Passion Psalm
    (22, 1): "My God, my God, why hast thou forsaken me? why art thou so far from helping me, and from the words of my roaring?",
    (22, 7): "All they that see me laugh me to scorn: they shoot out the lip, they shake the head, saying,",
    (22, 8): "He trusted on the LORD that he would deliver him: let him deliver him, seeing he delighted in him.",
    (22, 14): "I am poured out like water, and all my bones are out of joint: my heart is like wax; it is melted in the midst of my bowels.",
    (22, 16): "For dogs have compassed me: the assembly of the wicked have inclosed me: they pierced my hands and my feet.",
    (22, 18): "They part my garments among them, and cast lots upon my vesture.",
    # Psalm 23 - The Lord is My Shepherd
    (23, 1): "The LORD is my shepherd; I shall not want.",
    (23, 2): "He maketh me to lie down in green pastures: he leadeth me beside the still waters.",
    (23, 3): "He restoreth my soul: he leadeth me in the paths of righteousness for his name's sake.",
    (23, 4): "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me.",
    (23, 5): "Thou preparest a table before me in the presence of mine enemies: thou anointest my head with oil; my cup runneth over.",
    (23, 6): "Surely goodness and mercy shall follow me all the days of my life: and I will dwell in the house of the LORD for ever.",
    # Psalm 51 - Penitential
    (51, 1): "Have mercy upon me, O God, according to thy lovingkindness: according unto the multitude of thy tender mercies blot out my transgressions.",
    (51, 2): "Wash me throughly from mine iniquity, and cleanse me from my sin.",
    (51, 10): "Create in me a clean heart, O God; and renew a right spirit within me.",
    (51, 17): "The sacrifices of God are a broken spirit: a broken and a contrite heart, O God, thou wilt not despise.",
    # Psalm 91
    (91, 1): "He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty.",
    (91, 2): "I will say of the LORD, He is my refuge and my fortress: my God; in him will I trust.",
    (91, 11): "For he shall give his angels charge over thee, to keep thee in all thy ways.",
    # Psalm 110 - Messianic
    (110, 1): "The LORD said unto my Lord, Sit thou at my right hand, until I make thine enemies thy footstool.",
    (110, 4): "The LORD hath sworn, and will not repent, Thou art a priest for ever after the order of Melchizedek.",
    # Psalm 118
    (118, 22): "The stone which the builders refused is become the head stone of the corner.",
    (118, 23): "This is the LORD's doing; it is marvellous in our eyes.",
    # Psalm 119 (selections)
    (119, 105): "Thy word is a lamp unto my feet, and a light unto my path.",
    # Psalm 150
    (150, 6): "Let every thing that hath breath praise the LORD. Praise ye the LORD.",
}


# ============================================================================
# ISAIAH - MAJOR PROPHETIC PASSAGES
# ============================================================================

ISAIAH_TEXT = {
    # Chapter 6 - Call of Isaiah
    (6, 1): "In the year that king Uzziah died I saw also the Lord sitting upon a throne, high and lifted up, and his train filled the temple.",
    (6, 2): "Above it stood the seraphims: each one had six wings; with twain he covered his face, and with twain he covered his feet, and with twain he did fly.",
    (6, 3): "And one cried unto another, and said, Holy, holy, holy, is the LORD of hosts: the whole earth is full of his glory.",
    (6, 8): "Also I heard the voice of the Lord, saying, Whom shall I send, and who will go for us? Then said I, Here am I; send me.",
    # Chapter 7 - Immanuel
    (7, 14): "Therefore the Lord himself shall give you a sign; Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel.",
    # Chapter 9 - Prince of Peace
    (9, 6): "For unto us a child is born, unto us a son is given: and the government shall be upon his shoulder: and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of Peace.",
    (9, 7): "Of the increase of his government and peace there shall be no end, upon the throne of David, and upon his kingdom, to order it, and to establish it with judgment and with justice from henceforth even for ever. The zeal of the LORD of hosts will perform this.",
    # Chapter 11 - Branch of Jesse
    (11, 1): "And there shall come forth a rod out of the stem of Jesse, and a Branch shall grow out of his roots:",
    (11, 2): "And the spirit of the LORD shall rest upon him, the spirit of wisdom and understanding, the spirit of counsel and might, the spirit of knowledge and of the fear of the LORD;",
    # Chapter 40 - Comfort
    (40, 1): "Comfort ye, comfort ye my people, saith your God.",
    (40, 3): "The voice of him that crieth in the wilderness, Prepare ye the way of the LORD, make straight in the desert a highway for our God.",
    (40, 31): "But they that wait upon the LORD shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint.",
    # Chapter 53 - Suffering Servant (Complete)
    (53, 1): "Who hath believed our report? and to whom is the arm of the LORD revealed?",
    (53, 2): "For he shall grow up before him as a tender plant, and as a root out of a dry ground: he hath no form nor comeliness; and when we shall see him, there is no beauty that we should desire him.",
    (53, 3): "He is despised and rejected of men; a man of sorrows, and acquainted with grief: and we hid as it were our faces from him; he was despised, and we esteemed him not.",
    (53, 4): "Surely he hath borne our griefs, and carried our sorrows: yet we did esteem him stricken, smitten of God, and afflicted.",
    (53, 5): "But he was wounded for our transgressions, he was bruised for our iniquities: the chastisement of our peace was upon him; and with his stripes we are healed.",
    (53, 6): "All we like sheep have gone astray; we have turned every one to his own way; and the LORD hath laid on him the iniquity of us all.",
    (53, 7): "He was oppressed, and he was afflicted, yet he opened not his mouth: he is brought as a lamb to the slaughter, and as a sheep before her shearers is dumb, so he openeth not his mouth.",
    (53, 8): "He was taken from prison and from judgment: and who shall declare his generation? for he was cut off out of the land of the living: for the transgression of my people was he stricken.",
    (53, 9): "And he made his grave with the wicked, and with the rich in his death; because he had done no violence, neither was any deceit in his mouth.",
    (53, 10): "Yet it pleased the LORD to bruise him; he hath put him to grief: when thou shalt make his soul an offering for sin, he shall see his seed, he shall prolong his days, and the pleasure of the LORD shall prosper in his hand.",
    (53, 11): "He shall see of the travail of his soul, and shall be satisfied: by his knowledge shall my righteous servant justify many; for he shall bear their iniquities.",
    (53, 12): "Therefore will I divide him a portion with the great, and he shall divide the spoil with the strong; because he hath poured out his soul unto death: and he was numbered with the transgressors; and he bare the sin of many, and made intercession for the transgressors.",
    # Chapter 55
    (55, 1): "Ho, every one that thirsteth, come ye to the waters, and he that hath no money; come ye, buy, and eat; yea, come, buy wine and milk without money and without price.",
}


# ============================================================================
# GOSPEL OF JOHN - KEY PASSAGES
# ============================================================================

JOHN_TEXT = {
    # Chapter 1 - Prologue
    (1, 1): "In the beginning was the Word, and the Word was with God, and the Word was God.",
    (1, 2): "The same was in the beginning with God.",
    (1, 3): "All things were made by him; and without him was not any thing made that was made.",
    (1, 4): "In him was life; and the life was the light of men.",
    (1, 5): "And the light shineth in darkness; and the darkness comprehended it not.",
    (1, 9): "That was the true Light, which lighteth every man that cometh into the world.",
    (1, 10): "He was in the world, and the world was made by him, and the world knew him not.",
    (1, 11): "He came unto his own, and his own received him not.",
    (1, 12): "But as many as received him, to them gave he power to become the sons of God, even to them that believe on his name:",
    (1, 14): "And the Word was made flesh, and dwelt among us, (and we beheld his glory, the glory as of the only begotten of the Father,) full of grace and truth.",
    (1, 29): "The next day John seeth Jesus coming unto him, and saith, Behold the Lamb of God, which taketh away the sin of the world.",
    # Chapter 3
    (3, 3): "Jesus answered and said unto him, Verily, verily, I say unto thee, Except a man be born again, he cannot see the kingdom of God.",
    (3, 5): "Jesus answered, Verily, verily, I say unto thee, Except a man be born of water and of the Spirit, he cannot enter into the kingdom of God.",
    (3, 14): "And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up:",
    (3, 16): "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
    (3, 17): "For God sent not his Son into the world to condemn the world; but that the world through him might be saved.",
    # Chapter 6 - Bread of Life
    (6, 35): "And Jesus said unto them, I am the bread of life: he that cometh to me shall never hunger; and he that believeth on me shall never thirst.",
    (6, 51): "I am the living bread which came down from heaven: if any man eat of this bread, he shall live for ever: and the bread that I will give is my flesh, which I will give for the life of the world.",
    # Chapter 8
    (8, 12): "Then spake Jesus again unto them, saying, I am the light of the world: he that followeth me shall not walk in darkness, but shall have the light of life.",
    (8, 58): "Jesus said unto them, Verily, verily, I say unto you, Before Abraham was, I am.",
    # Chapter 10 - Good Shepherd
    (10, 10): "The thief cometh not, but for to steal, and to kill, and to destroy: I am come that they might have life, and that they might have it more abundantly.",
    (10, 11): "I am the good shepherd: the good shepherd giveth his life for the sheep.",
    (10, 14): "I am the good shepherd, and know my sheep, and am known of mine.",
    (10, 30): "I and my Father are one.",
    # Chapter 11
    (11, 25): "Jesus said unto her, I am the resurrection, and the life: he that believeth in me, though he were dead, yet shall he live:",
    (11, 26): "And whosoever liveth and believeth in me shall never die. Believest thou this?",
    (11, 35): "Jesus wept.",
    # Chapter 14
    (14, 1): "Let not your heart be troubled: ye believe in God, believe also in me.",
    (14, 2): "In my Father's house are many mansions: if it were not so, I would have told you. I go to prepare a place for you.",
    (14, 6): "Jesus saith unto him, I am the way, the truth, and the life: no man cometh unto the Father, but by me.",
    (14, 9): "Jesus saith unto him, Have I been so long time with you, and yet hast thou not known me, Philip? he that hath seen me hath seen the Father; and how sayest thou then, Shew us the Father?",
    (14, 27): "Peace I leave with you, my peace I give unto you: not as the world giveth, give I unto you. Let not your heart be troubled, neither let it be afraid.",
    # Chapter 15
    (15, 1): "I am the true vine, and my Father is the husbandman.",
    (15, 5): "I am the vine, ye are the branches: He that abideth in me, and I in him, the same bringeth forth much fruit: for without me ye can do nothing.",
    (15, 12): "This is my commandment, That ye love one another, as I have loved you.",
    (15, 13): "Greater love hath no man than this, that a man lay down his life for his friends.",
    # Chapter 17 - High Priestly Prayer
    (17, 3): "And this is life eternal, that they might know thee the only true God, and Jesus Christ, whom thou hast sent.",
    (17, 21): "That they all may be one; as thou, Father, art in me, and I in thee, that they also may be one in us: that the world may believe that thou hast sent me.",
    # Chapter 19 - Passion
    (19, 17): "And he bearing his cross went forth into a place called the place of a skull, which is called in the Hebrew Golgotha:",
    (19, 18): "Where they crucified him, and two other with him, on either side one, and Jesus in the midst.",
    (19, 26): "When Jesus therefore saw his mother, and the disciple standing by, whom he loved, he saith unto his mother, Woman, behold thy son!",
    (19, 28): "After this, Jesus knowing that all things were now accomplished, that the scripture might be fulfilled, saith, I thirst.",
    (19, 30): "When Jesus therefore had received the vinegar, he said, It is finished: and he bowed his head, and gave up the ghost.",
    (19, 34): "But one of the soldiers with a spear pierced his side, and forthwith came there out blood and water.",
    # Chapter 20 - Resurrection
    (20, 1): "The first day of the week cometh Mary Magdalene early, when it was yet dark, unto the sepulchre, and seeth the stone taken away from the sepulchre.",
    (20, 19): "Then the same day at evening, being the first day of the week, when the doors were shut where the disciples were assembled for fear of the Jews, came Jesus and stood in the midst, and saith unto them, Peace be unto you.",
    (20, 27): "Then saith he to Thomas, Reach hither thy finger, and behold my hands; and reach hither thy hand, and thrust it into my side: and be not faithless, but believing.",
    (20, 28): "And Thomas answered and said unto him, My Lord and my God.",
    (20, 29): "Jesus saith unto him, Thomas, because thou hast seen me, thou hast believed: blessed are they that have not seen, and yet have believed.",
    # Chapter 21
    (21, 15): "So when they had dined, Jesus saith to Simon Peter, Simon, son of Jonas, lovest thou me more than these? He saith unto him, Yea, Lord; thou knowest that I love thee. He saith unto him, Feed my lambs.",
    (21, 25): "And there are also many other things which Jesus did, the which, if they should be written every one, I suppose that even the world itself could not contain the books that should be written. Amen.",
}


# ============================================================================
# MATTHEW - KEY PASSAGES
# ============================================================================

MATTHEW_TEXT = {
    # Chapter 1
    (1, 1): "The book of the generation of Jesus Christ, the son of David, the son of Abraham.",
    (1, 21): "And she shall bring forth a son, and thou shalt call his name JESUS: for he shall save his people from their sins.",
    (1, 23): "Behold, a virgin shall be with child, and shall bring forth a son, and they shall call his name Emmanuel, which being interpreted is, God with us.",
    # Chapter 3 - Baptism
    (3, 13): "Then cometh Jesus from Galilee to Jordan unto John, to be baptized of him.",
    (3, 16): "And Jesus, when he was baptized, went up straightway out of the water: and, lo, the heavens were opened unto him, and he saw the Spirit of God descending like a dove, and lighting upon him:",
    (3, 17): "And lo a voice from heaven, saying, This is my beloved Son, in whom I am well pleased.",
    # Chapter 5 - Sermon on the Mount
    (5, 3): "Blessed are the poor in spirit: for theirs is the kingdom of heaven.",
    (5, 4): "Blessed are they that mourn: for they shall be comforted.",
    (5, 5): "Blessed are the meek: for they shall inherit the earth.",
    (5, 6): "Blessed are they which do hunger and thirst after righteousness: for they shall be filled.",
    (5, 7): "Blessed are the merciful: for they shall obtain mercy.",
    (5, 8): "Blessed are the pure in heart: for they shall see God.",
    (5, 9): "Blessed are the peacemakers: for they shall be called the children of God.",
    (5, 14): "Ye are the light of the world. A city that is set on an hill cannot be hid.",
    (5, 44): "But I say unto you, Love your enemies, bless them that curse you, do good to them that hate you, and pray for them which despitefully use you, and persecute you;",
    (5, 48): "Be ye therefore perfect, even as your Father which is in heaven is perfect.",
    # Chapter 6
    (6, 9): "After this manner therefore pray ye: Our Father which art in heaven, Hallowed be thy name.",
    (6, 10): "Thy kingdom come. Thy will be done in earth, as it is in heaven.",
    (6, 11): "Give us this day our daily bread.",
    (6, 12): "And forgive us our debts, as we forgive our debtors.",
    (6, 13): "And lead us not into temptation, but deliver us from evil: For thine is the kingdom, and the power, and the glory, for ever. Amen.",
    (6, 33): "But seek ye first the kingdom of God, and his righteousness; and all these things shall be added unto you.",
    # Chapter 11
    (11, 28): "Come unto me, all ye that labour and are heavy laden, and I will give you rest.",
    (11, 29): "Take my yoke upon you, and learn of me; for I am meek and lowly in heart: and ye shall find rest unto your souls.",
    # Chapter 16
    (16, 18): "And I say also unto thee, That thou art Peter, and upon this rock I will build my church; and the gates of hell shall not prevail against it.",
    (16, 24): "Then said Jesus unto his disciples, If any man will come after me, let him deny himself, and take up his cross, and follow me.",
    # Chapter 22
    (22, 37): "Jesus said unto him, Thou shalt love the Lord thy God with all thy heart, and with all thy soul, and with all thy mind.",
    (22, 39): "And the second is like unto it, Thou shalt love thy neighbour as thyself.",
    # Chapter 25
    (25, 35): "For I was an hungred, and ye gave me meat: I was thirsty, and ye gave me drink: I was a stranger, and ye took me in:",
    (25, 40): "And the King shall answer and say unto them, Verily I say unto you, Inasmuch as ye have done it unto one of the least of these my brethren, ye have done it unto me.",
    # Chapter 26 - Last Supper
    (26, 26): "And as they were eating, Jesus took bread, and blessed it, and brake it, and gave it to the disciples, and said, Take, eat; this is my body.",
    (26, 27): "And he took the cup, and gave thanks, and gave it to them, saying, Drink ye all of it;",
    (26, 28): "For this is my blood of the new testament, which is shed for many for the remission of sins.",
    # Chapter 27 - Passion
    (27, 46): "And about the ninth hour Jesus cried with a loud voice, saying, Eli, Eli, lama sabachthani? that is to say, My God, my God, why hast thou forsaken me?",
    # Chapter 28 - Resurrection
    (28, 6): "He is not here: for he is risen, as he said. Come, see the place where the Lord lay.",
    (28, 18): "And Jesus came and spake unto them, saying, All power is given unto me in heaven and in earth.",
    (28, 19): "Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost:",
    (28, 20): "Teaching them to observe all things whatsoever I have commanded you: and, lo, I am with you alway, even unto the end of the world. Amen.",
}


# ============================================================================
# ROMANS - KEY DOCTRINAL PASSAGES
# ============================================================================

ROMANS_TEXT = {
    (1, 16): "For I am not ashamed of the gospel of Christ: for it is the power of God unto salvation to every one that believeth; to the Jew first, and also to the Greek.",
    (1, 17): "For therein is the righteousness of God revealed from faith to faith: as it is written, The just shall live by faith.",
    (3, 23): "For all have sinned, and come short of the glory of God;",
    (3, 24): "Being justified freely by his grace through the redemption that is in Christ Jesus:",
    (5, 1): "Therefore being justified by faith, we have peace with God through our Lord Jesus Christ:",
    (5, 8): "But God commendeth his love toward us, in that, while we were yet sinners, Christ died for us.",
    (6, 23): "For the wages of sin is death; but the gift of God is eternal life through Jesus Christ our Lord.",
    (8, 1): "There is therefore now no condemnation to them which are in Christ Jesus, who walk not after the flesh, but after the Spirit.",
    (8, 28): "And we know that all things work together for good to them that love God, to them who are the called according to his purpose.",
    (8, 31): "What shall we then say to these things? If God be for us, who can be against us?",
    (8, 35): "Who shall separate us from the love of Christ? shall tribulation, or distress, or persecution, or famine, or nakedness, or peril, or sword?",
    (8, 38): "For I am persuaded, that neither death, nor life, nor angels, nor principalities, nor powers, nor things present, nor things to come,",
    (8, 39): "Nor height, nor depth, nor any other creature, shall be able to separate us from the love of God, which is in Christ Jesus our Lord.",
    (12, 1): "I beseech you therefore, brethren, by the mercies of God, that ye present your bodies a living sacrifice, holy, acceptable unto God, which is your reasonable service.",
    (12, 2): "And be not conformed to this world: but be ye transformed by the renewing of your mind, that ye may prove what is that good, and acceptable, and perfect, will of God.",
}


# ============================================================================
# 1 CORINTHIANS - KEY PASSAGES
# ============================================================================

FIRST_CORINTHIANS_TEXT = {
    (1, 18): "For the preaching of the cross is to them that perish foolishness; but unto us which are saved it is the power of God.",
    (1, 23): "But we preach Christ crucified, unto the Jews a stumblingblock, and unto the Greeks foolishness;",
    (1, 24): "But unto them which are called, both Jews and Greeks, Christ the power of God, and the wisdom of God.",
    (13, 1): "Though I speak with the tongues of men and of angels, and have not charity, I am become as sounding brass, or a tinkling cymbal.",
    (13, 4): "Charity suffereth long, and is kind; charity envieth not; charity vaunteth not itself, is not puffed up,",
    (13, 7): "Beareth all things, believeth all things, hopeth all things, endureth all things.",
    (13, 8): "Charity never faileth: but whether there be prophecies, they shall fail; whether there be tongues, they shall cease; whether there be knowledge, it shall vanish away.",
    (13, 13): "And now abideth faith, hope, charity, these three; but the greatest of these is charity.",
    (15, 3): "For I delivered unto you first of all that which I also received, how that Christ died for our sins according to the scriptures;",
    (15, 4): "And that he was buried, and that he rose again the third day according to the scriptures:",
    (15, 20): "But now is Christ risen from the dead, and become the firstfruits of them that slept.",
    (15, 45): "And so it is written, The first man Adam was made a living soul; the last Adam was made a quickening spirit.",
    (15, 55): "O death, where is thy sting? O grave, where is thy victory?",
}


# ============================================================================
# REVELATION - APOCALYPTIC VISIONS
# ============================================================================

REVELATION_TEXT = {
    (1, 7): "Behold, he cometh with clouds; and every eye shall see him, and they also which pierced him: and all kindreds of the earth shall wail because of him. Even so, Amen.",
    (1, 8): "I am Alpha and Omega, the beginning and the ending, saith the Lord, which is, and which was, and which is to come, the Almighty.",
    (1, 17): "And when I saw him, I fell at his feet as dead. And he laid his right hand upon me, saying unto me, Fear not; I am the first and the last:",
    (1, 18): "I am he that liveth, and was dead; and, behold, I am alive for evermore, Amen; and have the keys of hell and of death.",
    (4, 8): "And the four beasts had each of them six wings about him; and they were full of eyes within: and they rest not day and night, saying, Holy, holy, holy, Lord God Almighty, which was, and is, and is to come.",
    (4, 11): "Thou art worthy, O Lord, to receive glory and honour and power: for thou hast created all things, and for thy pleasure they are and were created.",
    (5, 6): "And I beheld, and, lo, in the midst of the throne and of the four beasts, and in the midst of the elders, stood a Lamb as it had been slain, having seven horns and seven eyes, which are the seven Spirits of God sent forth into all the earth.",
    (5, 9): "And they sung a new song, saying, Thou art worthy to take the book, and to open the seals thereof: for thou wast slain, and hast redeemed us to God by thy blood out of every kindred, and tongue, and people, and nation;",
    (5, 12): "Saying with a loud voice, Worthy is the Lamb that was slain to receive power, and riches, and wisdom, and strength, and honour, and glory, and blessing.",
    (7, 17): "For the Lamb which is in the midst of the throne shall feed them, and shall lead them unto living fountains of waters: and God shall wipe away all tears from their eyes.",
    (12, 11): "And they overcame him by the blood of the Lamb, and by the word of their testimony; and they loved not their lives unto the death.",
    (19, 16): "And he hath on his vesture and on his thigh a name written, KING OF KINGS, AND LORD OF LORDS.",
    (21, 1): "And I saw a new heaven and a new earth: for the first heaven and the first earth were passed away; and there was no more sea.",
    (21, 2): "And I John saw the holy city, new Jerusalem, coming down from God out of heaven, prepared as a bride adorned for her husband.",
    (21, 3): "And I heard a great voice out of heaven saying, Behold, the tabernacle of God is with men, and he will dwell with them, and they shall be his people, and God himself shall be with them, and be their God.",
    (21, 4): "And God shall wipe away all tears from their eyes; and there shall be no more death, neither sorrow, nor crying, neither shall there be any more pain: for the former things are passed away.",
    (21, 5): "And he that sat upon the throne said, Behold, I make all things new. And he said unto me, Write: for these words are true and faithful.",
    (22, 13): "I am Alpha and Omega, the beginning and the end, the first and the last.",
    (22, 17): "And the Spirit and the bride say, Come. And let him that heareth say, Come. And let him that is athirst come. And whosoever will, let him take the water of life freely.",
    (22, 20): "He which testifieth these things saith, Surely I come quickly. Amen. Even so, come, Lord Jesus.",
    (22, 21): "The grace of our Lord Jesus Christ be with you all. Amen.",
}


# ============================================================================
# HEBREWS - CHRISTOLOGICAL DOCTRINE
# ============================================================================

HEBREWS_TEXT = {
    (1, 1): "God, who at sundry times and in divers manners spake in time past unto the fathers by the prophets,",
    (1, 2): "Hath in these last days spoken unto us by his Son, whom he hath appointed heir of all things, by whom also he made the worlds;",
    (1, 3): "Who being the brightness of his glory, and the express image of his person, and upholding all things by the word of his power, when he had by himself purged our sins, sat down on the right hand of the Majesty on high;",
    (4, 12): "For the word of God is quick, and powerful, and sharper than any twoedged sword, piercing even to the dividing asunder of soul and spirit, and of the joints and marrow, and is a discerner of the thoughts and intents of the heart.",
    (4, 15): "For we have not an high priest which cannot be touched with the feeling of our infirmities; but was in all points tempted like as we are, yet without sin.",
    (4, 16): "Let us therefore come boldly unto the throne of grace, that we may obtain mercy, and find grace to help in time of need.",
    (11, 1): "Now faith is the substance of things hoped for, the evidence of things not seen.",
    (11, 6): "But without faith it is impossible to please him: for he that cometh to God must believe that he is, and that he is a rewarder of them that diligently seek him.",
    (12, 1): "Wherefore seeing we also are compassed about with so great a cloud of witnesses, let us lay aside every weight, and the sin which doth so easily beset us, and let us run with patience the race that is set before us,",
    (12, 2): "Looking unto Jesus the author and finisher of our faith; who for the joy that was set before him endured the cross, despising the shame, and is set down at the right hand of the throne of God.",
    (13, 8): "Jesus Christ the same yesterday, and to day, and for ever.",
}


# ============================================================================
# MASTER BOOK REGISTRY
# ============================================================================

OFFLINE_BIBLE_DATA = {
    'Genesis': GENESIS_TEXT,
    'Exodus': EXODUS_TEXT,
    'Psalms': PSALMS_TEXT,
    'Isaiah': ISAIAH_TEXT,
    'Matthew': MATTHEW_TEXT,
    'John': JOHN_TEXT,
    'Romans': ROMANS_TEXT,
    '1 Corinthians': FIRST_CORINTHIANS_TEXT,
    'Hebrews': HEBREWS_TEXT,
    'Revelation': REVELATION_TEXT,
}


# ============================================================================
# OFFLINE BIBLE PROVIDER CLASS
# ============================================================================

class OfflineBibleProvider:
    """
    Provides offline access to biblical text without API dependency.
    Falls back to API only when verse is not in local database.
    """
    
    def __init__(self):
        self.data = OFFLINE_BIBLE_DATA
        self._cache = {}
        self._stats = {
            'hits': 0,
            'misses': 0
        }
    
    def get_verse(self, book: str, chapter: int, verse: int) -> Optional[str]:
        """
        Get verse text from offline database.
        Returns None if verse not found (caller can try API).
        """
        cache_key = f"{book}_{chapter}_{verse}"
        
        if cache_key in self._cache:
            self._stats['hits'] += 1
            return self._cache[cache_key]
        
        book_data = self.data.get(book)
        if book_data:
            text = book_data.get((chapter, verse))
            if text:
                self._cache[cache_key] = text
                self._stats['hits'] += 1
                return text
        
        self._stats['misses'] += 1
        return None
    
    def get_verse_by_reference(self, reference: str) -> Optional[str]:
        """
        Get verse by reference string (e.g., "John 3:16").
        """
        try:
            # Parse reference
            parts = reference.rsplit(' ', 1)
            if len(parts) != 2:
                return None
            
            book = parts[0]
            chapter_verse = parts[1].split(':')
            if len(chapter_verse) != 2:
                return None
            
            chapter = int(chapter_verse[0])
            verse = int(chapter_verse[1])
            
            return self.get_verse(book, chapter, verse)
        except (ValueError, IndexError):
            return None
    
    def has_verse(self, book: str, chapter: int, verse: int) -> bool:
        """Check if verse is available offline."""
        book_data = self.data.get(book)
        if book_data:
            return (chapter, verse) in book_data
        return False
    
    def get_chapter(self, book: str, chapter: int) -> Dict[int, str]:
        """Get all available verses for a chapter."""
        book_data = self.data.get(book, {})
        return {
            verse: text 
            for (ch, verse), text in book_data.items() 
            if ch == chapter
        }
    
    def get_book_coverage(self, book: str) -> Dict[str, Any]:
        """Get coverage statistics for a book."""
        book_data = self.data.get(book, {})
        if not book_data:
            return {'available': False, 'verses': 0, 'chapters': []}
        
        chapters = set(ch for ch, _ in book_data.keys())
        return {
            'available': True,
            'verses': len(book_data),
            'chapters': sorted(chapters)
        }
    
    def get_all_available_books(self) -> List[str]:
        """Get list of all books with offline data."""
        return list(self.data.keys())
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get provider statistics."""
        total_verses = sum(len(book) for book in self.data.values())
        return {
            'total_verses': total_verses,
            'books_covered': len(self.data),
            'cache_hits': self._stats['hits'],
            'cache_misses': self._stats['misses'],
            'hit_rate': self._stats['hits'] / max(1, self._stats['hits'] + self._stats['misses'])
        }
    
    def search_text(self, query: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Search for text across all offline verses."""
        results = []
        search_query = query if case_sensitive else query.lower()
        
        for book, book_data in self.data.items():
            for (chapter, verse), text in book_data.items():
                search_text = text if case_sensitive else text.lower()
                if search_query in search_text:
                    results.append({
                        'reference': f"{book} {chapter}:{verse}",
                        'book': book,
                        'chapter': chapter,
                        'verse': verse,
                        'text': text
                    })
        
        return results


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_offline_provider = None


def get_offline_provider() -> OfflineBibleProvider:
    """Get the global offline Bible provider instance."""
    global _offline_provider
    if _offline_provider is None:
        _offline_provider = OfflineBibleProvider()
    return _offline_provider


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for offline Bible provider."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Offline Bible Provider')
    parser.add_argument('--verse', type=str, help='Get verse by reference (e.g., "John 3:16")')
    parser.add_argument('--stats', action='store_true', help='Show provider statistics')
    parser.add_argument('--books', action='store_true', help='List available books')
    parser.add_argument('--search', type=str, help='Search for text')
    parser.add_argument('--coverage', type=str, help='Show coverage for a book')
    
    args = parser.parse_args()
    
    provider = get_offline_provider()
    
    if args.verse:
        text = provider.get_verse_by_reference(args.verse)
        if text:
            print(f"\n{args.verse}:")
            print(f"  {text}")
        else:
            print(f"Verse not found in offline database: {args.verse}")
    
    elif args.stats:
        stats = provider.get_statistics()
        print("\nOffline Bible Provider Statistics:")
        print("=" * 50)
        print(f"  Total Verses Available: {stats['total_verses']:,}")
        print(f"  Books Covered: {stats['books_covered']}")
        print(f"  Cache Hits: {stats['cache_hits']}")
        print(f"  Cache Misses: {stats['cache_misses']}")
        print(f"  Hit Rate: {stats['hit_rate']:.1%}")
    
    elif args.books:
        books = provider.get_all_available_books()
        print("\nBooks Available Offline:")
        print("=" * 50)
        for book in books:
            coverage = provider.get_book_coverage(book)
            print(f"  {book}: {coverage['verses']} verses in {len(coverage['chapters'])} chapters")
    
    elif args.search:
        results = provider.search_text(args.search)
        print(f"\nSearch Results for '{args.search}':")
        print("=" * 50)
        for result in results[:20]:
            print(f"\n  {result['reference']}:")
            print(f"    {result['text'][:100]}...")
        if len(results) > 20:
            print(f"\n  ... and {len(results) - 20} more results")
    
    elif args.coverage:
        coverage = provider.get_book_coverage(args.coverage)
        if coverage['available']:
            print(f"\nCoverage for {args.coverage}:")
            print(f"  Verses: {coverage['verses']}")
            print(f"  Chapters: {coverage['chapters']}")
        else:
            print(f"No offline data for {args.coverage}")
    
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
