#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

'''
Title  : Estool
Version: 0.08
Author : Derrick Sobodash <derrick@sobodash.com>
Web    : https://github.com/sobodash/estool
License: BSD License

Copyright (c) 2008, Derrick Sobodash
All rights reserved

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of Derrick Sobodash nor the names of his contributors
  may be used to endorse or promote products derived from this software
  without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''

'''
-------------------------------------------------------------------------------
Program information
-------------------------------------------------------------------------------
'''
PROGRAM = "Estool"
VERSION = 0.08
AUTHOR  = "Derrick Sobodash"

# Import librariers
import wx                 # wxWidgets interface
import os
import sys

# Import functions
from string import atoi   # Convert binary string to int
from struct import pack   # Convert into to raw binary
from struct import unpack # Convert raw binary to int
from shutil import copy   # Copy files

# Menu triggers
ID_ABOUT     = 101        # Menu->Help->About
ID_OPEN      = 102        # Menu->File->Open
ID_SAVE      = 103        # Menu->File->Save
ID_SAVECOPY  = 104        # Menu->File->SaveCopy
ID_LICENSE   = 105        # Menu->Help->License
ID_EXIT      = 200        # Menu->File->Exit

# Action triggers
ID_CLASS     = 310

# Size of the header, changes on ROM load
OFFSET_HEAD  = 0

# Important locations within ROM
OFFSET_BASE   = 0x16cdc
OFFSET_CLASS  = 0x36240
OFFSET_ITEMS  = 0x14fb1
OFFSET_SPRITE = 0x17006
OFFSET_MOVE   = 0x17006
OFFSET_TDEFV  = 0x17260 # terrain defense, generic
OFFSET_UDEF   = 0x37d6a
OFFSET_UDEFV  = 0x37d8e
OFFSET_BATTLE = 0x2e316

# Terrain locations
OFFSET_TERR   = 0x28000
OFFSET_TERR00 = 0xfd8e
OFFSET_TERR01 = 0xfdab
OFFSET_TERR02 = 0xfdc8
OFFSET_TERR03 = 0xfde5
OFFSET_TERR04 = 0xfe02
OFFSET_TERR05 = 0xfe1f
OFFSET_TERR06 = 0xfe3c
OFFSET_TERR07 = 0xfe59
OFFSET_TERR08 = 0xfe76
OFFSET_TERR09 = 0xfe93
OFFSET_TERR10 = 0xfeb0
OFFSET_TERR11 = 0xfecd
OFFSET_TERR12 = 0xfeea

# Path to the current file
FILENAME     = ""

# A bigass list to grab ranges from, since it is more convenient than
# building a new list for each value.
NULL_255 = [
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None,
  None, None, None, None, None, None, None, None]


'''
-------------------------------------------------------------------------------
Globals

These are pre-formed global lists to store game data. They are made by taking
slices of the above Null list.
-------------------------------------------------------------------------------
'''
UNIT_FLYING  = NULL_255[:]
UNIT_TYPE    = NULL_255[:]
UNIT_TIER    = NULL_255[:]
UNIT_AT      = NULL_255[:]
UNIT_DF      = NULL_255[:]
UNIT_MV      = NULL_255[:]
UNIT_RANGE   = NULL_255[:]
UNIT_A       = NULL_255[:]
UNIT_D       = NULL_255[:]
UNIT_MP      = NULL_255[:]
UNIT_MDEF    = NULL_255[:]
UNIT_TROOPS  = NULL_255[:]
UNIT_COST    = NULL_255[:]
UNIT_VALUE   = NULL_255[:]
UNIT_AWARD   = NULL_255[:]
UNIT_EXP     = NULL_255[:]
UNIT_UNIT1   = NULL_255[:]
UNIT_UNIT2   = NULL_255[:]
UNIT_UNIT3   = NULL_255[:]
UNIT_SPELL1  = NULL_255[:]
UNIT_SPELL2  = NULL_255[:]
UNIT_SPELL3  = NULL_255[:]
UNIT_SPELL4  = NULL_255[:]
UNIT_PALETTE = NULL_255[:]
UNIT_SPRITE  = NULL_255[:]
UNIT_BATX    = NULL_255[:]
UNIT_BATY    = NULL_255[:]
UNIT_RIDER   = NULL_255[:]
UNIT_BLAND   = NULL_255[:]
UNIT_BAIR    = NULL_255[:]

BASE_CLASS   = NULL_255[:18]
BASE_MP      = NULL_255[:18]
BASE_A       = NULL_255[:18]
BASE_D       = NULL_255[:18]
BASE_AT      = NULL_255[:18]
BASE_DF      = NULL_255[:18]
BASE_TROOPS  = NULL_255[:18]
BASE_MARROW  = NULL_255[:18]
BASE_BLAST   = NULL_255[:18]
BASE_THUNDR  = NULL_255[:18]
BASE_FBALL   = NULL_255[:18]
BASE_METEOR  = NULL_255[:18]
BASE_BLIZZD  = NULL_255[:18]
BASE_TORNDO  = NULL_255[:18]
BASE_UNDEAD  = NULL_255[:18]
BASE_EQUAKE  = NULL_255[:18]
BASE_HEAL1   = NULL_255[:18]
BASE_HEAL2   = NULL_255[:18]
BASE_FHEAL1  = NULL_255[:18]
BASE_FHEAL2  = NULL_255[:18]
BASE_SLEEP   = NULL_255[:18]
BASE_MUTE    = NULL_255[:18]
BASE_PROTE1  = NULL_255[:18]
BASE_PROTE2  = NULL_255[:18]
BASE_ATTAK1  = NULL_255[:18]
BASE_ATTAK2  = NULL_255[:18]
BASE_ZONE    = NULL_255[:18]
BASE_TELEPT  = NULL_255[:18]
BASE_RESIST  = NULL_255[:18]
BASE_CHARM   = NULL_255[:18]
BASE_QUICK   = NULL_255[:18]
BASE_AGAIN   = NULL_255[:18]
BASE_DECRSE  = NULL_255[:18]
BASE_VALKYR  = NULL_255[:18]
BASE_FREYJA  = NULL_255[:18]
BASE_DRAGON  = NULL_255[:18]
BASE_SLMNDR  = NULL_255[:18]
BASE_GOLEM   = NULL_255[:18]
BASE_DEMON   = NULL_255[:18]
BASE_SEX     = NULL_255[:18]
BASE_PICTURE = NULL_255[:18]
BASE_UNIT    = NULL_255[:18]

ITEM_PROP1   = NULL_255[:36]
ITEM_VALUE1  = NULL_255[:36]
ITEM_PROP2   = NULL_255[:36]
ITEM_VALUE2  = NULL_255[:36]
ITEM_PROP3   = NULL_255[:36]
ITEM_VALUE3  = NULL_255[:36]
ITEM_PROP4   = NULL_255[:36]
ITEM_VALUE4  = NULL_255[:36]


'''
-------------------------------------------------------------------------------
Lists

Theses lists contain human-readable representations of all integer options.
-------------------------------------------------------------------------------
'''
# Unit types
UNITS    = [
  "000 - Null",
  "001 - Imperial Fighter",
  "002 - Light Fighter",
  "003 - Erwin/Light Fighter",
  "004 - Imperial Gladiator",
  "005 - Vampire",
  "006 - Imperial Knight",
  "007 - Erwin/Light Knight",
  "008 - Light Pirate",
  "009 - Imperial Hawk Knight",
  "010 - Light Hawk Knight",
  "011 - Sister",
  "012 - Imperial Shaman (Female)",
  "013 - Imperial Warlock (Female)",
  "014 - Light Warlock",
  "015 - Werewolf",
  "016 - Gelgazer",
  "017 - Ghost",
  "018 - Scylla",
  "019 - Roc",
  "020 - Imperial Lord",
  "021 - Light Lord",
  "022 - Erwin/Light Lord",
  "023 - Imperial Assassin",
  "024 - Light Assassin",
  "025 - Imperial Silver Knight",
  "026 - Light Silver Knight",
  "027 - Erwin/Light Silver Knight",
  "028 - Imperial Captain",
  "029 - Light Captain",
  "030 - Imperial Hawk Lord",
  "031 - Light Hawk Lord",
  "032 - Cleric",
  "033 - Imperial Necromancer (Male)",
  "034 - Imperial Sorcerer (Female)",
  "035 - Light Sorcerer A",
  "036 - Light Sorcerer B",
  "037 - Light Paladin",
  "038 - Imperial Paladin",
  "039 - Kerberos",
  "040 - Dullahan",
  "041 - Lich",
  "042 - Serpent",
  "043 - Wyvern",
  "044 - Imperial High Lord",
  "045 - Light High Lord",
  "046 - Erwin/Light High Lord",
  "047 - Imperial Swordsman",
  "048 - Light Swordsman",
  "049 - Imperial Highlander",
  "050 - Light Highlander",
  "051 - Erwin/Light Highlander",
  "052 - Imperial Serpent Knight",
  "053 - Erwin/Light Gladiator",
  "054 - Imperial Dragon Knight",
  "055 - Light Dragon Knight",
  "056 - Priest (Female)",
  "057 - Imperial Summoner (Male)",
  "058 - Imperial Mage (Female)",
  "059 - Light Mage A",
  "060 - Light Mage B",
  "061 - Saint A",
  "062 - Saint B",
  "063 - Cherie Unicorn Knight",
  "064 - Minotaur",
  "065 - Living Armour",
  "066 - Succubus",
  "067 - Kraken",
  "068 - Phoenix",
  "069 - Imperial General",
  "070 - Light General",
  "071 - Erwin/Light General",
  "072 - Imperial Sword Master",
  "073 - Erwin/Light Sword Master",
  "074 - Imperial Knight Master",
  "075 - Light Knight Master",
  "076 - Erwin/Light Knight Master",
  "077 - Imperial Serpent Lord",
  "078 - Erwin/Light Pirate",
  "079 - Dark Dragon Lord",
  "080 - Light Dragon Lord",
  "081 - High Priest (Female)",
  "082 - Imperial Zauberer (Male)",
  "083 - Dark Zauberer",
  "084 - Imperial Archmage (Female)",
  "085 - Light Archmage A",
  "086 - Light Archmage B",
  "087 - Sage",
  "088 - Erwin/Light Sage",
  "089 - Aaron Ranger",
  "090 - Rohga Ranger",
  "091 - Master Dino",
  "092 - Stone Golem",
  "093 - Vampire Lord",
  "094 - Jormungandr",
  "095 - Great Dragon",
  "096 - Erwin/Ledin King",
  "097 - Bernhardt Emperor",
  "098 - Erwin Hero",
  "099 - Erwin Hero",
  "100 - Erwin/Seighart Hero",
  "101 - Imelda Queen",
  "102 - Sonya Royal Guard",
  "103 - Leon Royal Guard",
  "104 - Scott Royal Guard",
  "105 - Erwin Royal Guard",
  "106 - Light Serpent Master",
  "107 - Light Dragon Master",
  "108 - Liana Agent",
  "109 - Boser Dark Master",
  "110 - Egbert Dark Master",
  "111 - Imperial Wizard (Male)",
  "112 - Imperial Wizard (Female)",
  "113 - Light Wizard A",
  "114 - Light Wizard B",
  "115 - Cherie Princess",
  "116 - Imperial Sorcerer (Male)",
  "117 - Aaron High Master",
  "118 - Rohga High Master",
  "119 - Monk",
  "120 - Barbarian",
  "121 - Imperial Soldier",
  "122 - Light Soldier",
  "123 - Soldier",
  "124 - Berserker",
  "125 - Imperial Grenadier",
  "126 - Light Grenadier",
  "127 - Grenadier",
  "128 - Dark Guard",
  "129 - Lancer",
  "130 - Light Trooper",
  "131 - Trooper",
  "132 - Hellhound",
  "133 - Royal Lancer",
  "134 - Light Dragoon",
  "135 - Dragoon",
  "136 - Bone Dino",
  "137 - Imperial Pike",
  "138 - Light Pike",
  "139 - Pike",
  "140 - Imperial Phalanx",
  "141 - Light Phalanx",
  "142 - Phalanx",
  "143 - Golem",
  "144 - Imperial Elf",
  "145 - Light Elf",
  "146 - Elf",
  "147 - Dark Elf",
  "148 - Imperial High Elf",
  "149 - Light High Elf",
  "150 - High Elf",
  "151 - Witch",
  "152 - Dark Ballista",
  "153 - Imperial Ballista",
  "154 - Light Ballista",
  "155 - Ballista",
  "156 - Ghost",
  "157 - Spectre",
  "158 - Demon",
  "159 - Archdemon",
  "160 - Light Merman",
  "161 - Merman",
  "162 - Dark Lizardman",
  "163 - Imperial Lizardman",
  "164 - Light Nixie",
  "165 - Nixie",
  "166 - Dark Leviathan",
  "167 - Imperial Leviathan",
  "168 - Imperial Harpy",
  "169 - Harpy",
  "170 - Fairy",
  "171 - Bat",
  "172 - Imperial Griffin",
  "173 - Griffin",
  "174 - Angel",
  "175 - Gargoyle",
  "176 - Light Monk",
  "177 - Imperial Barbarian",
  "178 - Light Crusader",
  "179 - Crusader",
  "180 - Imperial Barbarian",
  "181 - Barbarian",
  "182 - Imperial Bandit",
  "183 - Bandit",
  "184 - Zombie",
  "185 - Skeleton",
  "186 - Wolfman",
  "187 - Ogre",
  "188 - Gel",
  "189 - Elemental",
  "190 - Civilian",
  "191 - Valkyrie",
  "192 - Freyja",
  "193 - White Dragon",
  "194 - Salamander",
  "195 - Iron Golem",
  "196 - Demon Lord",
  "197 - Sleipnir",
  "198 - Fenrir",
  "199 - Aniki",
  "200 - Bodybuilder",
  "201 - Leon Knight Master",
  "202 - Rohga Emperor",
  "203 - Egbert Zauberer",
  "204 - Assassin",
  "205 - Lana Dark Princess",
  "206 - Lana Wizard",
  "207 - Lester Serpent Knight",
  "208 - Keith Dragon Knight",
  "209 - Keith Dragon Lord",
  "210 - Eliza and Emilia Noble",
  "211 - Cherie Dragon Knight",
  "212 - Imelda Royal Guard",
  "213 - Jessica Archmage",
  "214 - Aaron High Lord",
  "215 - Aaron Sword Master",
  "216 - Imperial Knight",
  "217 - Lester Serpent Lord",
  "218 - Scott Knight Master",
  "219 - Imperial Assassin",
  "220 - Rohga Ranger",
  "221 - Rohga High Master",
  "222 - Sonya Archmage",
  "223 - Sonya Wizard",
  "224 - Liana High Priest",
  "225 - Chaos",
  "226 - Erwin/Light Bishop",
  "227 - Lushiris",
  "228 - Imperial Sorcerer (Male)",
  "229 - Imperial Silver Knight",
  "230 - Imperial Necromancer (Male)",
  "231 - Imperial Saint",
  "232 - Imperial Mage (Male)",
  "233 - Imperial Swordsman",
  "234 - Imperial Highlander",
  "235 - Imperial Saint",
  "236 - Imperial Summoner (Male)",
  "237 - Light Swordsman",
  "238 - Light Serpent Knight",
  "239 - Priest",
  "240 - Erwin/Light Hawk Knight",
  "241 - Dark Dragon Lord",
  "242 - Dark Sage A",
  "243 - Dark Sage B",
  "244 - Imperial Archmage (Male)",
  "245 - Imperial General",
  "246 - Dark Sword Master",
  "247 - Imperial Serpent Lord",
  "248 - Light Sword Master",
  "249 - High Priest",
  "250 - Cherie Sage",
  "251 - Vargas General",
  "252 - Imperial Knight Master",
  "253 - Imperial Pirate ",
  "254 - Light Knight"]

# Unit Sprites
SPRITES = [
  "000 - Null",
  "001 - Imperial Soldier",
  "002 - Light Soldier",
  "003 - Imperial Grenadier",
  "004 - Light Grenadier",
  "005 - Lancer",
  "006 - Light Trooper",
  "007 - Hellhound",
  "008 - Royal Lancer",
  "009 - Light Dragoon",
  "010 - Bone Dino",
  "011 - Imperial Spearman",
  "012 - Light Spearman",
  "013 - Imperial Phalanx",
  "014 - Light Phalanx",
  "015 - Golem",
  "016 - Imperial Elf",
  "017 - Light Elf",
  "018 - Imperial High Elf",
  "019 - Light High Elf",
  "020 - Witch",
  "021 - Ghost",
  "022 - Spectre",
  "023 - Demon",
  "024 - Light Merman",
  "025 - Imperial Lizardman",
  "026 - Light Nixie",
  "027 - Imperial Leviathan",
  "028 - Harpie",
  "029 - Light Fairy",
  "030 - Bat",
  "031 - Griffin",
  "032 - Angel",
  "033 - Gargoyle",
  "034 - Monk",
  "035 - Crusader",
  "036 - Barbarian",
  "037 - Imperial Bandit",
  "038 - Zombie",
  "039 - Skeleton",
  "040 - Werewolf",
  "041 - Gel",
  "042 - Elemental",
  "043 - Civilian",
  "044 - Imperial Ballista",
  "045 - Light Ballista",
  "046 - Ogre",
  "047 - Light Gladiator",
  "048 - Light Fighter",
  "049 - Light Knight",
  "050 - Light Pirate",
  "051 - Light Serpent Knight",
  "052 - Light Hawk Knight",
  "053 - Light Dragon Knight",
  "054 - Light Sister",
  "055 - Light Priest",
  "056 - Light Warlock",
  "057 - Light Bishop",
  "058 - Bernhardt Fighter",
  "059 - Leon Gladiator",
  "060 - Leon Fighter",
  "061 - Leon Knight",
  "062 - Leon Dragon Knight",
  "063 - Vargas Gladiator",
  "064 - Vargas Fighter",
  "065 - Vargas Serpent Knight",
  "066 - Vargas Warlock",
  "067 - Imelda Warlock",
  "068 - Imelda Bishop",
  "069 - Imelda Shaman",
  "070 - Imelda Gladiator",
  "071 - Egbert Warlock",
  "072 - Egbert Shaman",
  "073 - Egbert Bishop",
  "074 - Egbert Fighter",
  "075 - Imperial Gladiator",
  "076 - Imperial Fighter",
  "077 - Imperial Knight",
  "078 - Imperial Pirate",
  "079 - Imperial Serpent Knight",
  "080 - Imperial Hawk Knight",
  "081 - Imperial Dragon Knight",
  "082 - Imperial Sister",
  "083 - Imperial Priest",
  "084 - Imperial Warlock (Female)",
  "085 - Imperial Warlock (Male)",
  "086 - Imperial Bishop",
  "087 - Boser Shaman",
  "088 - Dark Princess Shaman",
  "089 - Dark Princess Warlock",
  "090 - Dark Princess Bishop",
  "091 - Dark Princess Dragon Lord",
  "092 - Werewolf",
  "093 - Kerberos",
  "094 - Minotaur",
  "095 - Gelgazer",
  "096 - Master Dino",
  "097 - Dullahan",
  "098 - Living Armour",
  "099 - Stone Golem",
  "100 - Ghost",
  "101 - Lich",
  "102 - Succubus",
  "103 - Vampire Lord",
  "104 - Skylla",
  "105 - Serpent",
  "106 - Kraken",
  "107 - Jormungand",
  "108 - Roc",
  "109 - Phoenix",
  "110 - Wyvern",
  "111 - Great Dragon",
  "112 - Chaos",
  "113 - Ledin Gladiator",
  "114 - Sieghart Gladiator",
  "115 - Salamander",
  "116 - Iron Golem",
  "117 - Demon Lord",
  "118 - Freyja",
  "119 - White Dragon",
  "120 - Valkyrie",
  "121 - Sleipnir",
  "122 - Fenrir",
  "123 - Aniki",
  "124 - Erwin Gladiator",
  "125 - Erwin Knight",
  "126 - Erwin Fighter",
  "127 - Erwin Pirate",
  "128 - Erwin Hawk Knight",
  "129 - Erwin Warlock",
  "130 - Erwin Bishop",
  "131 - Hein Warlock",
  "132 - Hein Bishop",
  "133 - Hein Cleric",
  "134 - Hein Gladiator",
  "135 - Scott Fighter",
  "136 - Scott Gladiator",
  "137 - Scott Knight",
  "138 - Scott Dragon Knight",
  "139 - Lester Pirate",
  "140 - Lester Gladiator",
  "141 - Lester Knight",
  "142 - Lester Dragon Knight",
  "143 - Lester Serpent Knight",
  "144 - Cherie Gladiator",
  "145 - Cherie Knight",
  "146 - Cherie Hawk Knight",
  "147 - Cherie Dragon Knight",
  "148 - Cherie Bishop",
  "149 - Cherie Ranger",
  "150 - Keith Fighter",
  "151 - Keith Hawk Knight",
  "152 - Keith Dragon Knight",
  "153 - Keith Knight",
  "154 - Keith Serpent Knight",
  "155 - Aaron Gladiator",
  "156 - Aaron Fighter",
  "157 - Aaron Dragon Knight",
  "158 - Aaron Bishop",
  "159 - Aaron Ranger",
  "160 - Liana Sister",
  "161 - Liana Bishop",
  "162 - Liana Warlock",
  "163 - Liana Gladiator",
  "164 - Jessica Warlock",
  "165 - Rohga Gladiator",
  "166 - Rohga Fighter",
  "167 - Rohga Knight",
  "168 - Rohga Ranger",
  "169 - Sonya Gladiator",
  "170 - Sonya Fighter",
  "171 - Sonya Knight",
  "172 - Sonya Warlock",
  "173 - Lushiris",
  "174 - Noble"]

# Commander portraits
PORTRAIT = [
  "000 - None",
  "001 - Erwin (Normal)",
  "002 - Erwin (Hurt)",
  "003 - Erwin (Angry)",
  "004 - Erwin (Sad)",
  "005 - Liana (Normal)",
  "006 - Liana (Hurt)",
  "007 - Liana (Angry)",
  "008 - Liana (Sad)",
  "009 - Lana (Normal)",
  "010 - Lana (Hurt)",
  "011 - Lana (Angry)",
  "012 - Lana (Sad)",
  "013 - Cherie (Normal)",
  "014 - Cherie (Hurt)",
  "015 - Cherie (Angry)",
  "016 - Cherie (Sad)",
  "017 - Hein (Normal)",
  "018 - Hein (Hurt)",
  "019 - Hein (Angry)",
  "020 - Hein (Sad)",
  "021 - Scott (Normal)",
  "022 - Scott (Hurt)",
  "023 - Scott (Angry)",
  "024 - Scott (Sad)",
  "025 - Jessica (Normal)",
  "026 - Jessica (Hurt)",
  "027 - Jessica (Angry)",
  "028 - Jessica (Sad)",
  "029 - Lester (Normal)",
  "030 - Lester (Hurt)",
  "031 - Lester (Angry)",
  "032 - Lester (Sad)",
  "033 - Keith (Normal)",
  "034 - Keith (Hurt)",
  "035 - Keith (Angry)",
  "036 - Keith (Sad)",
  "037 - Aaron (Normal)",
  "038 - Aaron (Hurt)",
  "039 - Aaron (Angry)",
  "040 - Aaron (Sad)",
  "041 - Bernhardt (Normal)",
  "042 - Bernhardt (Hurt)",
  "043 - Bernhardt (Angry)",
  "044 - Egbert (Normal)",
  "045 - Egbert (Hurt)",
  "046 - Egbert (Angry)",
  "047 - Leon (Normal)",
  "048 - Leon (Hurt)",
  "049 - Leon (Angry)",
  "050 - Leon (Sad)",
  "051 - Leon (Hurt?)",
  "052 - Vargas (Normal)",
  "053 - Vargas (Hurt)",
  "054 - Vargas (Angry)",
  "055 - Imelda (Normal)",
  "056 - Imelda (Hurt)",
  "057 - Imelda (Angry)",
  "058 - Dark Princess (Normal)",
  "059 - Dark Princess (Hurt)",
  "060 - Dark Princess (Angry)",
  "061 - Boser (Normal)",
  "062 - Boser (Hurt)",
  "063 - Boser (Angry)",
  "064 - Lushiris (Normal)",
  "065 - Lushiris (Hurt)",
  "066 - Lushiris (Angry)",
  "067 - Chaos (Normal)",
  "068 - Chaos (Hurt)",
  "069 - Ledin (Normal)",
  "070 - Ledin (Hurt)",
  "071 - Sieghart (Normal)",
  "072 - Sieghart (Hurt)",
  "073 - Lauren (Normal)",
  "074 - Lauren (Hurt)",
  "075 - Laird (Normal)",
  "076 - Laird (Hurt)",
  "077 - Zorum (Normal)",
  "078 - Zorum (Hurt)",
  "079 - Morgan (Normal)",
  "080 - Morgan (Hurt)",
  "081 - Eliza (Normal)",
  "082 - Baldo (Normal)",
  "083 - Baldo (Hurt)",
  "084 - Silver Soldier 1 (Normal)",
  "085 - Brown Soldier 1 (Normal)",
  "086 - Green Soldier 1 (Normal)",
  "087 - Blue Soldier 1 (Normal)",
  "088 - Silver Soldier 2 (Normal)",
  "089 - Brown Soldier 2 (Normal)",
  "090 - Green Soldier 2 (Normal)",
  "091 - Blue Soldier 2 (Normal)",
  "092 - Blonde Civilian (Normal)",
  "093 - Blonde Civilian (Hurt)",
  "094 - Brunette Civilian (Normal)",
  "095 - Brunette Civilian (Hurt)",
  "096 - Redhead Civilian (Normal)",
  "097 - Redhead Civilian (Hurt)",
  "098 - Black Fighter (Normal)",
  "099 - Black Fighter (Hurt)",
  "100 - Red Fighter (Normal)",
  "101 - Red Fighter (Hurt)",
  "102 - Green Fighter (Normal)",
  "103 - Green Fighter (Hurt)",
  "104 - Blue Fighter (Normal)",
  "105 - Blue Fighter (Hurt)",
  "106 - Black Swordsman (Normal)",
  "107 - Black Swordsman (Hurt)",
  "108 - Red Swordsman (Normal)",
  "109 - Red Swordsman (Hurt)",
  "110 - Green Swordsman (Normal)",
  "111 - Green Swordsman (Hurt)",
  "112 - Blue Swordsman (Normal)",
  "113 - Blue Swordsman (Hurt)",
  "114 - Silver Saint (Normal)",
  "115 - Silver Saint (Hurt)",
  "116 - Purple Saint (Normal)",
  "117 - Purple Saint (Hurt)",
  "118 - Purple Pirate (Normal)",
  "119 - Purple Pirate (Hurt)",
  "120 - White Pirate (Normal)",
  "121 - White Pirate (Hurt)",
  "122 - White Priest (Normal)",
  "123 - White Priest (Hurt)",
  "124 - Yellow Priest (Normal)",
  "125 - Yellow Priest (Hurt)",
  "126 - Red Necromancer (Normal)",
  "127 - Red Necromancer (Hurt)",
  "128 - Green Necromancer (Normal)",
  "129 - Green Necromancer (Hurt)",
  "130 - Blue Necromancer (Normal)",
  "131 - Blue Necromancer (Hurt)",
  "132 - Red Gladiator (Normal)",
  "133 - Red Gladiator (Hurt)",
  "134 - Green Gladiator (Normal)",
  "135 - Green Gladiator (Hurt)",
  "136 - Blue Gladiator (Normal)",
  "137 - Blue Gladiator (Hurt)",
  "138 - Yellow Gladiator 1 (Normal)",
  "139 - Yellow Gladiator 1 (Hurt)",
  "140 - Yellow Gladiator 2 (Normal)",
  "141 - Yellow Gladiator 2 (Hurt)",
  "142 - Gray Mage (Normal)",
  "143 - Gray Mage (Hurt)",
  "144 - Red Mage (Normal)",
  "145 - Red Mage (Hurt)",
  "146 - Green Mage (Normal)",
  "147 - Green Mage (Hurt)",
  "148 - Blue Mage (Normal)",
  "149 - Blue Mage (Hurt)",
  "150 - Gray Sage (Normal)",
  "151 - Gray Sage (Hurt)",
  "152 - Red Sage (Normal)",
  "153 - Red Sage (Hurt)",
  "154 - Green Sage (Normal)",
  "155 - Green Sage (Hurt)",
  "156 - Blue Sage (Normal)",
  "157 - Blue Sage (Hurt)",
  "158 - White Priest (Normal)",
  "159 - White Priest (Hurt)",
  "160 - Red Priest (Normal)",
  "161 - Red Priest (Hurt)",
  "162 - Green Priest (Normal)",
  "163 - Green Priest (Hurt)",
  "164 - Blue Priest (Normal)",
  "165 - Blue Priest (Hurt)",
  "166 - Black Swordsman (Normal)",
  "167 - Black Swordsman (Hurt)",
  "168 - Red Swordsman (Normal)",
  "169 - Red Swordsman (Hurt)",
  "170 - Green Swordsman (Normal)",
  "171 - Green Swordsman (Hurt)",
  "172 - Blue Swordsman (Normal)",
  "173 - Blue Swordsman (Hurt)",
  "174 - Black Knight 1 (Normal)",
  "175 - Black Knight 1 (Hurt)",
  "176 - Red Knight 1 (Normal)",
  "177 - Red Knight 1 (Hurt)",
  "178 - Green Knight 1 (Normal)",
  "179 - Green Knight 1 (Hurt)",
  "180 - Blue Knight 1 (Normal)",
  "181 - Blue Knight 1 (Hurt)",
  "182 - Black High Lord (Normal)",
  "183 - Black High Lord (Hurt)",
  "184 - Red High Lord (Normal)",
  "185 - Red High Lord (Hurt)",
  "186 - Green High Lord (Normal)",
  "187 - Green High Lord (Hurt)",
  "188 - Blue High Lord (Normal)",
  "189 - Blue High Lord (Hurt)",
  "190 - Black Knight 2 (Normal)",
  "191 - Black Knight 2 (Hurt)",
  "192 - Red Knight 2 (Normal)",
  "193 - Red Knight 2 (Hurt)",
  "194 - Green Knight 2 (Normal)",
  "195 - Green Knight 2 (Hurt)",
  "196 - Blue Knight 2 (Normal)",
  "197 - Blue Knight 2 (Hurt)",
  "198 - Black Hawk Knight (Normal)",
  "199 - Black Hawk Knight (Hurt)",
  "200 - Red Hawk Knight (Normal)",
  "201 - Red Hawk Knight (Hurt)",
  "202 - Green Hawk Knight (Normal)",
  "203 - Green Hawk Knight (Hurt)",
  "204 - Black Serpent Knight (Normal)",
  "205 - Black Serpent Knight (Hurt)",
  "206 - Red Serpent Knight (Normal)",
  "207 - Red Serpent Knight (Hurt)",
  "208 - Green Serpent Knight (Normal)",
  "209 - Green Serpent Knight (Hurt)",
  "210 - Black Soldier 3 (Normal)",
  "211 - Black Soldier 3 (Hurt)",
  "212 - Green Soldier 3 (Normal)",
  "213 - Green Soldier 3 (Hurt)",
  "214 - Werewolf (Normal)",
  "215 - Gelgazer (Normal)",
  "216 - Cerberus (Normal)",
  "217 - Grey Scylla (Normal)",
  "218 - Pink Scylla (Normal)",
  "219 - Purple Scylla (Normal)",
  "220 - Ghost (Normal)",
  "221 - Serpent (Normal)",
  "222 - Master Dino (Normal)",
  "223 - Golem (Normal)",
  "224 - Red Lich (Normal)",
  "225 - Green Lich (Normal)",
  "226 - Purple Lich (Normal)",
  "227 - Gray Dullahan (Normal)",
  "228 - Bronze Dullahan (Normal)",
  "229 - Purple Dullahan (Normal)",
  "230 - Blue Succubus (Normal)",
  "231 - Pink Succubus (Normal)",
  "232 - Purple Succubus (Normal)",
  "233 - Minotaur 1 (Normal)",
  "234 - Minotaur 2 (Normal)",
  "235 - Wyvern (Normal)",
  "236 - Vampire (Normal)",
  "237 - Living Armour (Normal)",
  "238 - Great Dragon (Normal)",
  "239 - Kraken (Normal)",
  "240 - Red Phoenix (Normal)",
  "241 - Jormungand (Normal)",
  "242 - Sonya (Normal)",
  "243 - Sonya (Hurt)",
  "244 - Sonya (Angry)",
  "245 - Esto (Normal)",
  "246 - Esto (Hurt)",
  "247 - Osto (Normal)",
  "248 - Osto (Hurt)",
  "249 - Rohga (Normal)",
  "250 - Rohga (Hurt)",
  "251 - Rohga (Angry)",
  "252 - Pink Aniki (Normal)",
  "253 - Blue Aniki (Normal)",
  "254 - Purple Aniki (Normal)",
  "255 - Blue Phoenix (Normal)"]

# Magic list
MAGIC = [
  "000 - Magic Arrow",
  "001 - Blast",
  "002 - Thunder",
  "003 - Fireball",
  "004 - Meteor",
  "005 - Blizzard",
  "006 - Tornado",
  "007 - Turn Undead",
  "008 - Earthquake",
  "009 - Heal 1",
  "010 - Heal 2",
  "011 - Force Heal 1",
  "012 - Force Heal 2",
  "013 - Sleep",
  "014 - Mute",
  "015 - Protection 1",
  "016 - Protection 2",
  "017 - Attack 1",
  "018 - Attack 2",
  "019 - Zone",
  "020 - Teleport",
  "021 - Resist",
  "022 - Charm",
  "023 - Quick",
  "024 - Again",
  "025 - Decrease",
  "026 - Valkyrie",
  "027 - Freyja",
  "028 - White Dragon",
  "029 - Salamander",
  "030 - Iron Golem",
  "031 - Demon Lord",
  "255 - None"]

# Unit types
AFFINITY = [
  "000 - Soldier",
  "001 - Monk",
  "002 - Spearman",
  "003 - Cavalry",
  "004 - Dragoon",
  "005 - Flier",
  "006 - Bandit",
  "007 - Sailor",
  "008 - Gel",
  "009 - Demon",
  "010 - Monster",
  "011 - Barbarian",
  "012 - Magician",
  "013 - Ghost",
  "014 - Undead",
  "015 - Bowman",
  "016 - Ballista",
  "017 - Dragon"]

# Commander list
COMMANDERS = [
	"000 - Erwin",
	"001 - Liana",
	"002 - Lana",
	"003 - Cherie",
	"004 - Hein",
	"005 - Scott",
	"006 - Keith",
	"007 - Aaron",
	"008 - Lester",
	"009 - Lana",
	"010 - Rohga",
	"011 - Sonya",
	"012 - Leon",
	"013 - Vargas",
	"014 - Imelda",
	"015 - Egbert",
	"016 - Esto",
	"017 - Osto"]

# Item names
ITEMS = [
  "000 - Not Equipped",
  "001 - Dagger",
  "002 - War Hammer",
  "003 - Long Sword",
  "004 - Magic Wand",
  "005 - Inferno Lance",
  "006 - Devil Axe",
  "007 - Dragon Slayer",
  "008 - Langrisser",
  "009 - Langrisser (Unsealed)",
  "010 - Iron Dumbbell",
  "011 - Masayan Sword",
  "012 - Orb",
  "013 - Holy Rod",
  "014 - Holy Rod",
  "015 - Dark Rod",
  "016 - Long Bow",
  "017 - Arbalest",
  "018 - Alhazard",
  "019 - Alhazard (Unsealed)",
  "020 - Odin's Buckler",
  "021 - Buckler",
  "022 - Shield",
  "023 - Chainmail",
  "024 - Platemail",
  "025 - Assault Suit",
  "026 - Cloak",
  "027 - Dragon Scale",
  "028 - Wizard's Robe",
  "029 - Amulet",
  "030 - Cross",
  "031 - Necklace",
  "032 - Swift Boots",
  "033 - Crown",
  "034 - Gleipnir",
  "035 - Rune Stone"]

# Item Properties
IPROPS = [
	"000 - AT",
	"001 - DF",
	"002 - Movement",
	"003 - Range",
	"004 - A+",
	"005 - D+",
	"006 - Magic Range",
	"007 - Magic Damage",
	"008 - Magic Resist",
	"009 - Summon",
  "255 - None"]

# Summons for weapons
SUMMONS = [
  "000 - Valkyrie",
  "001 - Freyja",
  "002 - White Dragon",
  "003 - Salamander",
  "004 - Iron Golem",
  "005 - Demon Lord",
  "006 - Sleipnir",
  "007 - Fenrir",
  "008 - Aniki",
  "009 - Enemy Aniki"]

# Terrain types
TERRAIN = [
  "001 - Plains",
  "002 - Rough Ground",
  "003 - Road",
  "004 - Forest",
  "005 - Mountain A",
  "006 - Mountain B",
  "007 - Ocean",
  "008 - Raised Wall",
  "009 - Castle Wall",
  "010 - Castle Interior",
  "011 - Home Interior",
  "012 - Temple Interior",
  "013 - Throne Room",
  "014 - Fishing Bridge",
  "015 - Sky Bridge",
  "016 - Plains",
  "017 - Burning",
  "018 - Burning",
  "019 - Graveyard",
  "020 - Ship Deck",
  "021 - Riverside",
  "022 - City Streets",
  "023 - Ship Deck",
  "024 - Riverside",
  "025 - City Streets",
  "026 - Realm of the Gods",
  "027 - Ruined Castle",
  "028 - High Wall",
  "029 - Forbidden"]

# Attack Patterns
ATTACKS  = [
  "000 - None",
  "001 - Charge (Knight)",
  "002 - Charge (Soldier)",
  "003 - Charge (?)",
  "004 - Charge (Kraken)",
  "005 - Charge (Leviathan)",
  "006 - Charge (Golem)",
  "007 - Charge Through (?)",
  "008 - Charge Through (Roc)",
  "009 - Charge Through (Flier)",
  "010 - Unused Disappearing Charge",
  "011 - Unused Trailing Charge",
  "012 - Fighter Charge",
  "013 - Elf Fire Arrows",
  "014 - Ballista Fire Arrows",
  "015 - Unused Dust Throwing",
  "016 - Dagger Throw (Lancer)",
  "017 - Sword Throw ()",
  "018 - Axe Throw (?)",
  "019 - Dagger Throw (?)",
  "020 - Dagger Throw (Nixie)",
  "021 - Axe Throw (?)",
  "022 - Staff Throw (?)",
  "023 - Wand Throw (?)",
  "024 - Unused Feather Throwing",
  "025 - Unused Dust Throwing",
  "026 - Unused Axe Throwing",
  "027 - Gel Sprite Top-Left Throwing",
  "028 - Gelgazer Gel Throwing",
  "029 - Ogre Thing Throwing",
  "030 - Hellhound Green Rays",
  "031 - Unused Glitch Rays",
  "032 - Serpent Spinning Star Rays",
  "033 - Cross Throw",
  "034 - Unused Star Rays",
  "035 - Ranger Slash Rays",
  "036 - Kraken Red Blob Rays",
  "037 - Witch White Line Rays",
  "038 - Sword Energy",
  "039 - Boser Beam",
  "040 - Warlock Fire Bomb",
  "041 - Wizard Lightning Strikes",
  "042 - Holy Wrath",
  "043 - Succubus Lightning Ground Wave",
  "044 - Unused Lightning Ground Wave",
  "045 - Roc Feathers",
  "046 - Feather Storm",
  "047 - Princess Flash",
  "048 - Holy Flash",
  "049 - Salamander Fireball Spread",
  "050 - Warlock Fireball",
  "051 - Unused Charge",
  "052 - Unused White Line Rays",
  "053 - Serpent Charge Through",
  "054 - Wyvern Lightning Ground Wave",
  "055 - Dark Power",
  "056 - Ghost White Line Rays",
  "057 - Egbert DM Lightning Arc",
  "058 - Elemental Fly Through",
  "059 - Vampire Lightning Strike",
  "060 - Dullahan Trailing Charge Through",
  "061 - Dullahan Sword Throw",
  "062 - Vampire Fireball Strike",
  "063 - Unused Beam",
  "064 - Wolfman Rays",
  "065 - Dragon Lord Attack",
  "066 - Unused Trailing Charge Through",
  "067 - Charge Through (Phoenix)",
  "068 - White Line Rays (Leviathan)",
  "069 - Fireballs (Demon Lord)",
  "070 - Sprinkle Stars (Jormungandr)",
  "071 - White Line Rays (Lich)",
  "072 - Green Rays (Fenrir)",
  "073 - Ground Wave (Fenrir)"]

# Sexes
SEX = [
  "Male",
  "Female"]

# Palettes
PALETTE = [
  "Imperial/Light",
  "Independent/Chaos",
  "Inactive",
  "Alien Skin?"]

# Boolean options
BOOLEAN = [
  "False",
  "True"]


'''
-------------------------------------------------------------------------------
ClassForm()

A form that allows users to edit the properties of each unit type and
commander class in the game.
-------------------------------------------------------------------------------
'''
class ClassForm(wx.Panel):
  # Layout
  def __init__(self, parent, id):
    wx.Panel.__init__(self, parent, id)
    self.classlabel = wx.StaticText(self, -1, "Unit Type:", wx.Point(10,14))
    self.classdrop = wx.Choice(self, -1, wx.Point(100,10), None, UNITS)
    self.classdrop.SetSelection(0)
    self.classdrop.Bind(wx.EVT_CHOICE, self.LoadStats)
    
    self.statbox       = wx.StaticBox(self, -1, 'Stats', (10, 45), size=(264, 260))
    self.gainbox       = wx.StaticBox(self, -1, 'Units', (280, 45), size=(270, 114))
    self.spellbox      = wx.StaticBox(self, -1, 'Spells', (280, 165), size=(176, 140))
    self.unitbox       = wx.StaticBox(self, -1, 'Spoils', (556, 45), size=(170, 78))
    self.battlebox     = wx.StaticBox(self, -1, 'Battle', (462, 165), size=(264, 140))
    self.lookbox       = wx.StaticBox(self, -1, 'Appearance', (10, 310), size=(716, 56))
    
    self.atlabel       = wx.StaticText(self, -1, "AT:",wx.Point(20, 64))
    self.atspin        = wx.SpinCtrl(self, -1, "", wx.Point(70, 60), size=(64,24))
    self.atspin.SetRange(-128, 127)
    self.atspin.Bind(wx.EVT_TEXT, self.UpdateAT)
    self.dflabel       = wx.StaticText(self, -1, "DF:",wx.Point(150, 64))
    self.dfspin        = wx.SpinCtrl(self, -1, "", wx.Point(200, 60), size=(64,24))
    self.dfspin.SetRange(-128, 127)
    self.dfspin.Bind(wx.EVT_TEXT, self.UpdateDF)
    
    self.mvlabel       = wx.StaticText(self, -1, "MV:",wx.Point(20, 94))
    self.mvspin        = wx.SpinCtrl(self, -1, "", wx.Point(70, 90), size=(64,24))
    self.mvspin.SetRange(-128, 127)
    self.mvspin.Bind(wx.EVT_TEXT, self.UpdateMV)
    self.rangelabel    = wx.StaticText(self, -1, "Range:",wx.Point(150, 94))
    self.rangespin     = wx.SpinCtrl(self, -1, "", wx.Point(200, 90), size=(64,24))
    self.rangespin.SetRange(-128, 127)
    self.rangespin.Bind(wx.EVT_TEXT, self.UpdateRange)
    
    self.alabel        = wx.StaticText(self, -1, "A+:",wx.Point(20, 124))
    self.aspin         = wx.SpinCtrl(self, -1, "", wx.Point(70, 120), size=(64,24))
    self.aspin.SetRange(-128, 127)
    self.aspin.Bind(wx.EVT_TEXT, self.UpdateA)
    self.dlabel        = wx.StaticText(self, -1, "D+:",wx.Point(150, 124))
    self.dspin         = wx.SpinCtrl(self, -1, "", wx.Point(200, 120), size=(64,24))
    self.dspin.SetRange(-128, 127)
    self.dspin.Bind(wx.EVT_TEXT, self.UpdateD)
    
    self.mplabel       = wx.StaticText(self, -1, "MP:",wx.Point(20, 154))
    self.mpspin        = wx.SpinCtrl(self, -1, "", wx.Point(70, 150), size=(64,24))
    self.mpspin.SetRange(0, 255)
    self.mpspin.Bind(wx.EVT_TEXT, self.UpdateMP)
    self.mdeflabel     = wx.StaticText(self, -1, "M.Def:",wx.Point(150, 154))
    self.mdefspin      = wx.SpinCtrl(self, -1, "", wx.Point(200, 150), size=(64,24))
    self.mdefspin.SetRange(0, 255)
    self.mdefspin.Bind(wx.EVT_TEXT, self.UpdateMDef)
    
    self.troopslabel   = wx.StaticText(self, -1, "Troops:",wx.Point(20, 184))
    self.troopsspin    = wx.SpinCtrl(self, -1, "", wx.Point(70, 180), size=(64,24))
    self.troopsspin.SetRange(-128, 127)
    self.troopsspin.Bind(wx.EVT_TEXT, self.UpdateTroops)
    self.costlabel     = wx.StaticText(self, -1, "Cost:",wx.Point(150, 184))
    self.costspin      = wx.SpinCtrl(self, -1, "", wx.Point(200, 180), size=(64,24))
    self.costspin.SetRange(0, 2550)
    self.costspin.Bind(wx.EVT_TEXT, self.UpdateCost)
    
    self.explabel      = wx.StaticText(self, -1, "Meter:",wx.Point(20, 214))
    self.expspin       = wx.SpinCtrl(self, -1, "", wx.Point(70, 210), size=(64,24))
    self.expspin.SetRange(0, 10)
    self.expspin.Bind(wx.EVT_TEXT, self.UpdateEXP)
    self.tierlabel     = wx.StaticText(self, -1, "Tier:",wx.Point(150, 214))
    self.tierspin      = wx.SpinCtrl(self, -1, "", wx.Point(200, 210), size=(64,24))
    self.tierspin.SetRange(0, 4)
    self.tierspin.Bind(wx.EVT_TEXT, self.UpdateTier)
    
    self.affinitylabel = wx.StaticText(self, -1, "Affinity:",wx.Point(20, 244))
    self.affinitydrop  = wx.Choice(self, -1, wx.Point(70, 240), None, AFFINITY)
    self.affinitydrop.Bind(wx.EVT_CHOICE, self.UpdateAffinity)
    
    self.flyingcheck   = wx.CheckBox(self, -1, "Flying", wx.Point(20,270))
    self.flyingcheck.Bind(wx.EVT_CHECKBOX, self.UpdateFlying)
    
    self.unit1drop     = wx.Choice(self, -1, wx.Point(290, 60), None, UNITS)
    self.unit1drop.Bind(wx.EVT_CHOICE, self.UpdateUnit1)
    self.unit2drop     = wx.Choice(self, -1, wx.Point(290, 90), None, UNITS)
    self.unit2drop.Bind(wx.EVT_CHOICE, self.UpdateUnit2)
    self.unit3drop     = wx.Choice(self, -1, wx.Point(290, 120), None, UNITS)
    self.unit3drop.Bind(wx.EVT_CHOICE, self.UpdateUnit3)
    
    self.spell1drop    = wx.Choice(self, -1, wx.Point(290, 180), None, MAGIC)
    self.spell1drop.Bind(wx.EVT_CHOICE, self.UpdateSpell1)
    self.spell2drop    = wx.Choice(self, -1, wx.Point(290, 210), None, MAGIC)
    self.spell2drop.Bind(wx.EVT_CHOICE, self.UpdateSpell2)
    self.spell3drop    = wx.Choice(self, -1, wx.Point(290, 240), None, MAGIC)
    self.spell3drop.Bind(wx.EVT_CHOICE, self.UpdateSpell3)
    self.spell4drop    = wx.Choice(self, -1, wx.Point(290, 270), None, MAGIC)
    self.spell4drop.Bind(wx.EVT_CHOICE, self.UpdateSpell4)
    
    self.spritelabel   = wx.StaticText(self, -1, "Sprite:",wx.Point(20, 334))
    self.spritedrop    = wx.Choice(self, -1, wx.Point(70, 330), None, SPRITES)
    self.spritedrop.Bind(wx.EVT_CHOICE, self.UpdateSprite)
    
    self.palettelabel  = wx.StaticText(self, -1, "Color:",wx.Point(330, 334))
    self.palettedrop   = wx.Choice(self, -1, wx.Point(380, 330), None, PALETTE)
    self.palettedrop.Bind(wx.EVT_CHOICE, self.UpdatePalette)
    
    self.valuelabel    = wx.StaticText(self, -1, "EXP:",wx.Point(566, 64))
    self.valuespin     = wx.SpinCtrl(self, -1, "", wx.Point(616, 60), size=(64,24))
    self.valuespin.SetRange(0, 255)
    self.valuespin.Bind(wx.EVT_TEXT, self.UpdateValue)
    self.awardlabel    = wx.StaticText(self, -1, "Money:",wx.Point(566, 94))
    self.awardspin     = wx.SpinCtrl(self, -1, "", wx.Point(616, 90), size=(64,24))
    self.awardspin.SetRange(0, 2550)
    self.awardspin.Bind(wx.EVT_TEXT, self.UpdateAward)
    
    self.battlexlabel  = wx.StaticText(self, -1, "X:",wx.Point(472, 184))
    self.battlexspin   = wx.SpinCtrl(self, -1, "", wx.Point(502, 180), size=(64,24))
    self.battlexspin.SetRange(0, 255)
    self.battlexspin.Bind(wx.EVT_TEXT, self.UpdateAward)
    self.battleylabel  = wx.StaticText(self, -1, "Y:",wx.Point(586, 184))
    self.battleyspin   = wx.SpinCtrl(self, -1, "", wx.Point(616, 180), size=(64,24))
    self.battleyspin.SetRange(0, 255)
    self.battleyspin.Bind(wx.EVT_TEXT, self.UpdateAward)
    self.groundlabel   = wx.StaticText(self, -1, "Land:",wx.Point(472, 214))
    self.grounddrop    = wx.Choice(self, -1, wx.Point(522, 210), None, ATTACKS)
    self.grounddrop.Bind(wx.EVT_CHOICE, self.UpdateAward)
    self.airlabel      = wx.StaticText(self, -1, "Air:",wx.Point(472, 244))
    self.airdrop       = wx.Choice(self, -1, wx.Point(522, 240), None, ATTACKS)
    self.airdrop.Bind(wx.EVT_CHOICE, self.UpdateAward)
    self.mountedcheck  = wx.CheckBox(self, -1, "Mounted", wx.Point(472,270))
    self.mountedcheck.Bind(wx.EVT_CHECKBOX, self.UpdateFlying)
    
    if(UNIT_FLYING[0] != None): self.LoadStats(1)
  
  def UpdateAT(self, e):
    i = self.classdrop.GetSelection()
    temp = self.atspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_AT
    UNIT_AT[i] = s8bit(int(temp))
  
  def UpdateDF(self, e):
    i = self.classdrop.GetSelection()
    temp = self.dfspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_DF
    UNIT_DF[i] = s8bit(int(temp))
  
  def UpdateMV(self, e):
    i = self.classdrop.GetSelection()
    temp = self.mvspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_MV
    UNIT_MV[i] = s8bit(int(temp))
  
  def UpdateRange(self, e):
    i = self.classdrop.GetSelection()
    temp = self.rangespin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_RANGE
    UNIT_RANGE[i] = s8bit(int(temp))
  
  def UpdateA(self, e):
    i = self.classdrop.GetSelection()
    temp = self.aspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_A
    UNIT_A[i] = s8bit(int(temp))
  
  def UpdateD(self, e):
    i = self.classdrop.GetSelection()
    temp = self.dspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_D
    UNIT_D[i] = s8bit(int(temp))
  
  def UpdateMP(self, e):
    i = self.classdrop.GetSelection()
    temp = self.mpspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_MP
    UNIT_MP[i] = u8bit(int(temp))
  
  def UpdateMDef(self, e):
    i = self.classdrop.GetSelection()
    temp = self.mdefspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_MDEF
    UNIT_MDEF[i] = s8bit(int(temp))
  
  def UpdateTroops(self, e):
    i = self.classdrop.GetSelection()
    temp = self.troopsspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_TROOPS
    UNIT_TROOPS[i] = s8bit(int(temp))
  
  def UpdateCost(self, e):
    i = self.classdrop.GetSelection()
    temp = self.costspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_COST
    UNIT_COST[i] = u8bit(int(temp) / 10)
  
  def UpdateValue(self, e):
    i = self.classdrop.GetSelection()
    temp = self.valuespin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_VALUE
    UNIT_VALUE[i] = u8bit(int(temp))
  
  def UpdateFlying(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_FLYING
    UNIT_FLYING[i] = int(self.flyingdrop.GetValue())
  
  def UpdateAffinity(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_TYPE
    UNIT_TYPE[i] = int(self.affinitydrop.GetSelection())
  
  def UpdateTier(self, e):
    i = self.classdrop.GetSelection()
    temp = self.tierspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_TIER
    UNIT_TIER[i] = s8bit(int(temp))
  
  def UpdateEXP(self, e):
    i = self.classdrop.GetSelection()
    temp = self.expspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_EXP
    UNIT_EXP[i] = s8bit(int(temp))
  
  def UpdateAward(self, e):
    i = self.classdrop.GetSelection()
    temp = self.awardspin.GetValue()
    if(temp == '' or temp == 'None'): temp = "0"
    global UNIT_AWARD
    UNIT_AWARD[i] = u8bit(int(temp) / 10)
  
  def UpdateUnit1(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_UNIT1
    UNIT_UNIT1[i] = int(self.unit1drop.GetSelection())
  
  def UpdateUnit2(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_UNIT2
    UNIT_UNIT2[i] = int(self.unit2drop.GetSelection())
  
  def UpdateUnit3(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_UNIT3
    UNIT_UNIT3[i] = int(self.unit3drop.GetSelection())
  
  def UpdateSpell1(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_SPELL1
    temp = self.spell1drop.GetSelection
    if(UNIT_SPELL1[i] == 32):
      temp = 255
    UNIT_SPELL1[i] = int(temp())
  
  def UpdateSpell2(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_SPELL2
    temp = self.spell2drop.GetSelection
    if(UNIT_SPELL2[i] == 32):
      temp = 255
    UNIT_SPELL2[i] = int(temp())
  
  def UpdateSpell3(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_SPELL3
    temp = self.spell3drop.GetSelection
    if(UNIT_SPELL3[i] == 32):
      temp = 255
    UNIT_SPELL3[i] = int(temp())
  
  def UpdateSpell4(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_SPELL4
    temp = self.spell4drop.GetSelection
    if(UNIT_SPELL4[i] == 32):
      temp = 255
    UNIT_SPELL4[i] = int(temp())
  
  def UpdateSprite(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_SPRITE
    UNIT_SPRITE[i] = int(self.spritedrop.GetSelection())
  
  def UpdatePalette(self, e):
    i = self.classdrop.GetSelection()
    global UNIT_PALETTE
    if(int(self.palettedrop.GetSelection()) == 0):
      UNIT_PALETTE[i] = int(self.palettedrop.GetSelection())
    else:
      UNIT_PALETTE[i] = int(self.palettedrop.GetSelection()) * 4
  
  def LoadStats(self, e):
    i = self.classdrop.GetSelection()
    if(i == -1):
      self.classdrop.SetSelection(0)
      i = 0
    self.atspin.SetValue(UNIT_AT[i])
    self.dfspin.SetValue(UNIT_DF[i])
    self.mvspin.SetValue(UNIT_MV[i])
    self.rangespin.SetValue(UNIT_RANGE[i])
    self.aspin.SetValue(UNIT_A[i])
    self.dspin.SetValue(UNIT_D[i])
    self.mpspin.SetValue(UNIT_MP[i])
    self.mdefspin.SetValue(UNIT_MDEF[i])
    self.troopsspin.SetValue(UNIT_TROOPS[i])
    self.costspin.SetValue(UNIT_COST[i] * 10)
    self.valuespin.SetValue(UNIT_VALUE[i])
    self.flyingcheck.SetValue(UNIT_FLYING[i])
    self.affinitydrop.SetSelection(UNIT_TYPE[i])
    self.tierspin.SetValue(UNIT_TIER[i])
    self.expspin.SetValue(UNIT_EXP[i])
    self.awardspin.SetValue(UNIT_EXP[i] * 10)
    self.battlexspin.SetValue(UNIT_BATX[i])
    self.battleyspin.SetValue(UNIT_BATY[i])
    self.grounddrop.SetSelection(UNIT_BLAND[i])
    self.airdrop.SetSelection(UNIT_BAIR[i])
    self.mountedcheck.SetValue(UNIT_RIDER[i])
    self.unit1drop.SetSelection(UNIT_UNIT1[i])
    self.unit2drop.SetSelection(UNIT_UNIT2[i])
    self.unit3drop.SetSelection(UNIT_UNIT3[i])
    temp = UNIT_SPELL1[i]
    if(UNIT_SPELL1[i] == 255):
      temp = 32
    self.spell1drop.SetSelection(temp)
    temp = UNIT_SPELL2[i]
    if(UNIT_SPELL2[i] == 255):
      temp = 32
    self.spell2drop.SetSelection(temp)
    temp = UNIT_SPELL3[i]
    if(UNIT_SPELL3[i] == 255):
      temp = 32
    self.spell3drop.SetSelection(temp)
    temp = UNIT_SPELL4[i]
    if(UNIT_SPELL4[i] == 255):
      temp = 32
    self.spell4drop.SetSelection(temp)
    self.spritedrop.SetSelection(UNIT_SPRITE[i])
    if(UNIT_PALETTE[i] == 0):
      self.palettedrop.SetSelection(0)
    else:
      self.palettedrop.SetSelection(UNIT_PALETTE[i] / 4)


'''
-------------------------------------------------------------------------------
CommanderForm()

A form that allows users to edit the basic stats of each potential commander.
-------------------------------------------------------------------------------
'''
class CommanderForm(wx.Panel):
  def __init__(self, parent, id):
    wx.Panel.__init__(self, parent, id)
    self.commandlabel  = wx.StaticText(self, -1, "Commander:", wx.Point(10,14))
    self.commanddrop   = wx.Choice(self, -1, wx.Point(100,10), None, COMMANDERS)
    self.commanddrop.SetSelection(0)
    self.commanddrop.Bind(wx.EVT_CHOICE, self.LoadStats)
    
    self.portraitlabel = wx.StaticText(self, -1, "Portrait:",wx.Point(10, 54))
    self.portraitdrop  = wx.Choice(self, -1, wx.Point(100, 50), None, PORTRAIT)
    self.portraitdrop.Bind(wx.EVT_CHOICE, self.UpdatePortrait)
    
    self.atlabel       = wx.StaticText(self, -1, "AT:",wx.Point(10, 84))
    self.atspin        = wx.TextCtrl(self, -1, "", wx.Point(60, 80))
    self.atspin.Bind(wx.EVT_TEXT, self.UpdateAT)
    
    self.dflabel       = wx.StaticText(self, -1, "DF:",wx.Point(10, 114))
    self.dfspin        = wx.TextCtrl(self, -1, "", wx.Point(60, 110))
    self.dfspin.Bind(wx.EVT_TEXT, self.UpdateDF)
    
    self.troopslabel   = wx.StaticText(self, -1, "Troops:",wx.Point(10, 144))
    self.troopsspin    = wx.TextCtrl(self, -1, "", wx.Point(60, 140))
    self.troopsspin.Bind(wx.EVT_TEXT, self.UpdateTroops)
    
    self.sexlabel    = wx.StaticText(self, -1, "Sex:",wx.Point(170, 84))
    self.sexdrop     = wx.Choice(self, -1, wx.Point(220, 80), None, SEX)
    self.sexdrop.Bind(wx.EVT_CHOICE, self.UpdateSex)
    
    self.unitlabel    = wx.StaticText(self, -1, "Unit:",wx.Point(170, 114))
    self.unitdrop     = wx.Choice(self, -1, wx.Point(220, 110), None, UNITS)
    self.unitdrop.Bind(wx.EVT_CHOICE, self.UpdateUnit)
    
    self.marrowcheck   = wx.CheckBox(self, -1, "Magic Arrow", wx.Point(10,180))
    self.marrowcheck.Bind(wx.EVT_CHECKBOX, self.UpdateMArrow)
    self.blastcheck    = wx.CheckBox(self, -1, "Blast", wx.Point(10,200))
    self.blastcheck.Bind(wx.EVT_CHECKBOX, self.UpdateBlast)
    self.thundrcheck   = wx.CheckBox(self, -1, "Thunder", wx.Point(10,220))
    self.thundrcheck.Bind(wx.EVT_CHECKBOX, self.UpdateThundr)
    self.fballcheck    = wx.CheckBox(self, -1, "Fireball", wx.Point(10,240))
    self.fballcheck.Bind(wx.EVT_CHECKBOX, self.UpdateFBall)
    self.meteorcheck   = wx.CheckBox(self, -1, "Meteor", wx.Point(10,260))
    self.meteorcheck.Bind(wx.EVT_CHECKBOX, self.UpdateMeteor)
    self.blizzdcheck   = wx.CheckBox(self, -1, "Blizzard", wx.Point(10,280))
    self.blizzdcheck.Bind(wx.EVT_CHECKBOX, self.UpdateBlizzd)
    self.torndocheck   = wx.CheckBox(self, -1, "Tornado", wx.Point(10,300))
    self.torndocheck.Bind(wx.EVT_CHECKBOX, self.UpdateTorndo)
    self.undeadcheck   = wx.CheckBox(self, -1, "Turn Undead", wx.Point(10,320))
    self.undeadcheck.Bind(wx.EVT_CHECKBOX, self.UpdateUndead)
    self.equakecheck   = wx.CheckBox(self, -1, "Earthquake", wx.Point(10,340))
    self.equakecheck.Bind(wx.EVT_CHECKBOX, self.UpdateEquake)
    self.heal1check    = wx.CheckBox(self, -1, "Heal 1", wx.Point(10,360))
    self.heal1check.Bind(wx.EVT_CHECKBOX, self.UpdateHeal1)
    self.heal2check    = wx.CheckBox(self, -1, "Heal 2", wx.Point(10,380))
    self.heal2check.Bind(wx.EVT_CHECKBOX, self.UpdateHeal2)
    
    self.fheal1check   = wx.CheckBox(self, -1, "Force Heal 1", wx.Point(170,180))
    self.fheal1check.Bind(wx.EVT_CHECKBOX, self.UpdateFHeal1)
    self.fheal2check   = wx.CheckBox(self, -1, "Force Heal 2", wx.Point(170,200))
    self.fheal2check.Bind(wx.EVT_CHECKBOX, self.UpdateFHeal2)
    self.sleepcheck    = wx.CheckBox(self, -1, "Sleep", wx.Point(170,220))
    self.sleepcheck.Bind(wx.EVT_CHECKBOX, self.UpdateSleep)
    self.mutecheck     = wx.CheckBox(self, -1, "Mute", wx.Point(170,240))
    self.mutecheck.Bind(wx.EVT_CHECKBOX, self.UpdateMute)
    self.prote1check   = wx.CheckBox(self, -1, "Protection 1", wx.Point(170,260))
    self.prote1check.Bind(wx.EVT_CHECKBOX, self.UpdateProte1)
    self.prote2check   = wx.CheckBox(self, -1, "Protection 2", wx.Point(170,280))
    self.prote2check.Bind(wx.EVT_CHECKBOX, self.UpdateProte2)
    self.attak1check   = wx.CheckBox(self, -1, "Attack 1", wx.Point(170,300))
    self.attak1check.Bind(wx.EVT_CHECKBOX, self.UpdateAttak1)
    self.attak2check   = wx.CheckBox(self, -1, "Attack 2", wx.Point(170,320))
    self.attak2check.Bind(wx.EVT_CHECKBOX, self.UpdateAttak2)
    self.zonecheck     = wx.CheckBox(self, -1, "Zone", wx.Point(170,340))
    self.zonecheck.Bind(wx.EVT_CHECKBOX, self.UpdateZone)
    self.teleptcheck   = wx.CheckBox(self, -1, "Teleport", wx.Point(170,360))
    self.teleptcheck.Bind(wx.EVT_CHECKBOX, self.UpdateTelept)
    self.resistcheck   = wx.CheckBox(self, -1, "Resist", wx.Point(170,380))
    self.resistcheck.Bind(wx.EVT_CHECKBOX, self.UpdateResist)
    
    self.charmcheck    = wx.CheckBox(self, -1, "Charm", wx.Point(330,180))
    self.charmcheck.Bind(wx.EVT_CHECKBOX, self.UpdateCharm)
    self.quickcheck    = wx.CheckBox(self, -1, "Quick", wx.Point(330,200))
    self.quickcheck.Bind(wx.EVT_CHECKBOX, self.UpdateQuick)
    self.againcheck    = wx.CheckBox(self, -1, "Again", wx.Point(330,220))
    self.againcheck.Bind(wx.EVT_CHECKBOX, self.UpdateAgain)
    self.decrsecheck   = wx.CheckBox(self, -1, "Decrease", wx.Point(330,240))
    self.decrsecheck.Bind(wx.EVT_CHECKBOX, self.UpdateDecrse)
    self.valkyrcheck   = wx.CheckBox(self, -1, "Valkyrie", wx.Point(330,260))
    self.valkyrcheck.Bind(wx.EVT_CHECKBOX, self.UpdateValkyr)
    self.freyjacheck   = wx.CheckBox(self, -1, "Freyja", wx.Point(330,280))
    self.freyjacheck.Bind(wx.EVT_CHECKBOX, self.UpdateFreyja)
    self.dragoncheck   = wx.CheckBox(self, -1, "White Dragon", wx.Point(330,300))
    self.dragoncheck.Bind(wx.EVT_CHECKBOX, self.UpdateDragon)
    self.slmndrcheck   = wx.CheckBox(self, -1, "Salamander", wx.Point(330,320))
    self.slmndrcheck.Bind(wx.EVT_CHECKBOX, self.UpdateSlmndr)
    self.golemcheck    = wx.CheckBox(self, -1, "Iron Golem", wx.Point(330,340))
    self.golemcheck.Bind(wx.EVT_CHECKBOX, self.UpdateGolem)
    self.demoncheck    = wx.CheckBox(self, -1, "Demon Lord", wx.Point(330,360))
    self.demoncheck.Bind(wx.EVT_CHECKBOX, self.UpdateDemon)
    
    if(BASE_SEX[0] != None): self.LoadStats(1)
  
  def UpdateAT(self, e):
    i = self.commanddrop.GetSelection()
    temp = self.atspin.GetValue()
    if(temp == '' or temp == 'None'): temp = '0'
    global BASE_AT
    BASE_AT[i] = s8bit(int(temp))
  
  def UpdateDF(self, e):
    i = self.commanddrop.GetSelection()
    temp = self.dfspin.GetValue()
    if(temp == '' or temp == 'None'): temp = '0'
    global BASE_DF
    BASE_DF[i] = s8bit(int(temp))
  
  def UpdateTroops(self, e):
    i = self.commanddrop.GetSelection()
    temp = self.troopsspin.GetValue()
    if(temp == '' or temp == 'None'): temp = '0'
    global BASE_TROOPS
    BASE_TROOPS[i] = s8bit(int(temp))
  
  def UpdatePortrait(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_PICTURE
    BASE_PICTURE[i] = u8bit(int(self.portraitdrop.GetSelection()))
  
  def UpdateUnit(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_UNIT
    BASE_UNIT[i] = self.unitdrop.GetSelection()
  
  def UpdateSex(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_SEX
    BASE_SEX[i] = self.sexdrop.GetSelection()
  
  def UpdateMArrow(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_MARROW
    BASE_MARROW[i] = self.marrowcheck.GetValue()
  
  def UpdateBlast(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_BLAST
    BASE_BLAST[i] = self.blastcheck.GetValue()
  
  def UpdateThundr(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_THUNDR
    BASE_THUNDR[i] = self.thundrcheck.GetValue()
  
  def UpdateFBall(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_FBALL
    BASE_FBALL[i] = self.fballcheck.GetValue()
  
  def UpdateMeteor(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_METEOR
    BASE_METEOR[i] = self.meteorcheck.GetValue()
  
  def UpdateBlizzd(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_BLIZZD
    BASE_BLIZZD[i] = self.blizzdcheck.GetValue()
  
  def UpdateTorndo(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_TORNDO
    BASE_TORNDO[i] = self.torndocheck.GetValue()
  
  def UpdateUndead(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_UNDEAD
    BASE_UNDEAD[i] = self.undeadcheck.GetValue()
  
  def UpdateEquake(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_EQUAKE
    BASE_EQUAKE[i] = self.equakecheck.GetValue()
  
  def UpdateHeal1(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_HEAL1
    BASE_HEAL1[i] = self.heal1check.GetValue()
  
  def UpdateHeal2(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_HEAL2
    BASE_HEAL2[i] = self.heal2check.GetValue()
  
  def UpdateFHeal1(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_FHEAL1
    BASE_FHEAL1[i] = self.fheal1check.GetValue()
  
  def UpdateFHeal2(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_FHEAL2
    BASE_FHEAL2[i] = self.fheal2check.GetValue()
  
  def UpdateSleep(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_SLEEP
    BASE_SLEEP[i] = self.sleepcheck.GetValue()
  
  def UpdateMute(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_MUTE
    BASE_MUTE[i] = self.mutecheck.GetValue()
  
  def UpdateProte1(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_PROTE1
    BASE_PROTE1[i] = self.prote1check.GetValue()
  
  def UpdateProte2(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_PROTE2
    BASE_PROTE2[i] = self.prote2check.GetValue()
  
  def UpdateAttak1(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_ATTAK1
    BASE_ATTAK1[i] = self.attak1check.GetValue()
  
  def UpdateAttak2(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_ATTAK2
    BASE_ATTAK2[i] = self.attak2check.GetValue()
  
  def UpdateZone(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_ZONE
    BASE_ZONE[i] = self.zonecheck.GetValue()
  
  def UpdateTelept(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_TELEPT
    BASE_TELEPT[i] = self.teleptcheck.GetValue()
  
  def UpdateResist(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_RESIST
    BASE_RESIST[i] = self.resistcheck.GetValue()
  
  def UpdateCharm(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_CHARM
    BASE_CHARM[i] = self.charmcheck.GetValue()
  
  def UpdateQuick(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_QUICK
    BASE_QUICK[i] = self.quickcheck.GetValue()
  
  def UpdateAgain(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_AGAIN
    BASE_AGAIN[i] = self.againcheck.GetValue()
  
  def UpdateDecrse(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_DECRSE
    BASE_DECRSE[i] = self.decrsecheck.GetValue()
  
  def UpdateValkyr(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_VALKYR
    BASE_VALKYR[i] = self.valkyrcheck.GetValue()
  
  def UpdateFreyja(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_FREYJA
    BASE_FREYJA[i] = self.freyjacheck.GetValue()
  
  def UpdateDragon(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_DRAGON
    BASE_DRAGON[i] = self.dragoncheck.GetValue()
  
  def UpdateSlmndr(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_SLMNDR
    BASE_SLMNDR[i] = self.slmndrcheck.GetValue()
  
  def UpdateGolem(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_GOLEM
    BASE_GOLEM[i] = self.golemcheck.GetValue()
  
  def UpdateDemon(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_DEMON
    BASE_DEMON[i] = self.demoncheck.GetValue()
  
  def LoadStats(self, e):
    i = self.commanddrop.GetSelection()
    if(i == -1):
      self.commanddrop.SetSelection(0)
      i = 0
    self.atspin.SetValue(str(BASE_AT[i]))
    self.dfspin.SetValue(str(BASE_DF[i]))
    self.troopsspin.SetValue(str(BASE_TROOPS[i]))
    self.portraitdrop.SetSelection(BASE_PICTURE[i])
    self.unitdrop.SetSelection(BASE_UNIT[i])
    self.sexdrop.SetSelection(BASE_SEX[i])
    self.marrowcheck.SetValue(BASE_MARROW[i])
    self.blastcheck.SetValue(BASE_BLAST[i])
    self.thundrcheck.SetValue(BASE_THUNDR[i])
    self.fballcheck.SetValue(BASE_FBALL[i])
    self.meteorcheck.SetValue(BASE_METEOR[i])
    self.blizzdcheck.SetValue(BASE_BLIZZD[i])
    self.torndocheck.SetValue(BASE_TORNDO[i])
    self.undeadcheck.SetValue(BASE_UNDEAD[i])
    self.equakecheck.SetValue(BASE_EQUAKE[i])
    self.heal1check.SetValue(BASE_HEAL1[i])
    self.heal2check.SetValue(BASE_HEAL2[i])
    self.fheal1check.SetValue(BASE_FHEAL1[i])
    self.fheal2check.SetValue(BASE_FHEAL2[i])
    self.sleepcheck.SetValue(BASE_SLEEP[i])
    self.mutecheck.SetValue(BASE_MUTE[i])
    self.prote1check.SetValue(BASE_PROTE1[i])
    self.prote2check.SetValue(BASE_PROTE2[i])
    self.attak1check.SetValue(BASE_ATTAK1[i])
    self.attak2check.SetValue(BASE_ATTAK2[i])
    self.zonecheck.SetValue(BASE_ZONE[i])
    self.teleptcheck.SetValue(BASE_TELEPT[i])
    self.resistcheck.SetValue(BASE_RESIST[i])
    self.charmcheck.SetValue(BASE_CHARM[i])
    self.quickcheck.SetValue(BASE_QUICK[i])
    self.againcheck.SetValue(BASE_AGAIN[i])
    self.decrsecheck.SetValue(BASE_DECRSE[i])
    self.valkyrcheck.SetValue(BASE_VALKYR[i])
    self.freyjacheck.SetValue(BASE_FREYJA[i])
    self.dragoncheck.SetValue(BASE_DRAGON[i])
    self.slmndrcheck.SetValue(BASE_SLMNDR[i])
    self.golemcheck.SetValue(BASE_GOLEM[i])
    self.demoncheck.SetValue(BASE_DEMON[i])


'''
-------------------------------------------------------------------------------
ItemForm()

A form that allows users to edit the properties of each in-game item.
-------------------------------------------------------------------------------
'''
class ItemForm(wx.Panel):
  def __init__(self, parent, id):
    wx.Panel.__init__(self, parent, id)
    self.itemlabel  = wx.StaticText(self, -1, "Item:", wx.Point(10,14))
    self.itemdrop   = wx.Choice(self, -1, wx.Point(100,10), None, ITEMS)
    self.itemdrop.SetSelection(0)
    self.itemdrop.Bind(wx.EVT_CHOICE, self.LoadStats)
    
    self.prop1label    = wx.StaticText(self, -1, "Property:",wx.Point(10, 54))
    self.prop1drop     = wx.Choice(self, -1, wx.Point(80, 50), None, IPROPS)
    self.prop1drop.Bind(wx.EVT_CHOICE, self.UpdateProp1)
    self.prop1text     = wx.TextCtrl(self, -1, "", wx.Point(260, 50))
    self.prop1text.Bind(wx.EVT_TEXT, self.UpdateValue1)
    self.prop1summon   = wx.Choice(self, -1, wx.Point(260, 50), None, SUMMONS)
    self.prop1summon.Bind(wx.EVT_CHOICE, self.UpdateSummon1)
    self.prop1text.Hide()
    self.prop1summon.Hide()
    
    self.prop2label    = wx.StaticText(self, -1, "Property:",wx.Point(10, 84))
    self.prop2drop     = wx.Choice(self, -1, wx.Point(80, 80), None, IPROPS)
    self.prop2drop.Bind(wx.EVT_CHOICE, self.UpdateProp2)
    self.prop2text     = wx.TextCtrl(self, -1, "", wx.Point(260, 80))
    self.prop2text.Bind(wx.EVT_TEXT, self.UpdateValue2)
    self.prop2summon   = wx.Choice(self, -1, wx.Point(260, 80), None, SUMMONS)
    self.prop2summon.Bind(wx.EVT_CHOICE, self.UpdateSummon2)
    self.prop2text.Hide()
    self.prop2summon.Hide()
    
    self.prop3label    = wx.StaticText(self, -1, "Property:",wx.Point(10, 114))
    self.prop3drop     = wx.Choice(self, -1, wx.Point(80, 110), None, IPROPS)
    self.prop3drop.Bind(wx.EVT_CHOICE, self.UpdateProp3)
    self.prop3text     = wx.TextCtrl(self, -1, "", wx.Point(260, 110))
    self.prop3text.Bind(wx.EVT_TEXT, self.UpdateValue3)
    self.prop3summon   = wx.Choice(self, -1, wx.Point(260, 110), None, SUMMONS)
    self.prop3summon.Bind(wx.EVT_CHOICE, self.UpdateSummon3)
    self.prop3text.Hide()
    self.prop3summon.Hide()
    
    self.prop4label    = wx.StaticText(self, -1, "Property:",wx.Point(10, 144))
    self.prop4drop     = wx.Choice(self, -1, wx.Point(80, 140), None, IPROPS)
    self.prop4drop.Bind(wx.EVT_CHOICE, self.UpdateProp4)
    self.prop4text     = wx.TextCtrl(self, -1, "", wx.Point(260, 140))
    self.prop4text.Bind(wx.EVT_TEXT, self.UpdateValue4)
    self.prop4summon   = wx.Choice(self, -1, wx.Point(260, 140), None, SUMMONS)
    self.prop4summon.Bind(wx.EVT_CHOICE, self.UpdateSummon4)
    self.prop4text.Hide()
    self.prop4summon.Hide()
    
    if(ITEM_PROP1[0] != [0]): self.LoadStats(1)
  
  def UpdateProp1(self, e):
    i = self.itemdrop.GetSelection()
    temp = self.prop1drop.GetSelection()
    if(temp == 10): temp = 255
    global ITEM_PROP1
    ITEM_PROP1[i] = temp
    if(temp >= 0 and temp < 9):
      self.prop1text.SetValue("0")
      self.prop1text.Show()
      self.prop1summon.Hide()
    elif(temp == 9):
      self.prop1text.Hide()
      self.prop1summon.SetSelection(0)
      self.prop1summon.Show()
    else:
      self.prop1text.Hide()
      self.prop1summon.Hide()
  
  def UpdateProp2(self, e):
    i = self.itemdrop.GetSelection()
    temp = self.prop2drop.GetSelection()
    if(temp == 10): temp = 255
    global ITEM_PROP2
    ITEM_PROP2[i] = temp
    if(temp >= 0 and temp < 9):
      self.prop2text.SetValue("0")
      self.prop2text.Show()
      self.prop2summon.Hide()
    elif(temp == 9):
      self.prop2text.Hide()
      self.prop2summon.SetSelection(0)
      self.prop2summon.Show()
    else:
      self.prop2text.Hide()
      self.prop2summon.Hide()
  
  def UpdateProp3(self, e):
    i = self.itemdrop.GetSelection()
    temp = self.prop3drop.GetSelection()
    if(temp == 10): temp = 255
    global ITEM_PROP3
    ITEM_PROP3[i] = temp
    if(temp >= 0 and temp < 9):
      self.prop3text.SetValue("0")
      self.prop3text.Show()
      self.prop3summon.Hide()
    elif(temp == 9):
      self.prop3text.Hide()
      self.prop3summon.SetSelection(0)
      self.prop3summon.Show()
    else:
      self.prop3text.Hide()
      self.prop3summon.Hide()
  
  def UpdateProp4(self, e):
    i = self.itemdrop.GetSelection()
    temp = self.prop4drop.GetSelection()
    if(temp == 10): temp = 255
    global ITEM_PROP4
    ITEM_PROP4[i] = temp
    if(temp >= 0 and temp < 9):
      self.prop4text.SetValue("0")
      self.prop4text.Show()
      self.prop4summon.Hide()
    elif(temp == 9):
      self.prop4text.Hide()
      self.prop4summon.SetSelection(0)
      self.prop4summon.Show()
    else:
      self.prop4text.Hide()
      self.prop4summon.Hide()
  
  def UpdateSummon1(self, e):
    i = self.itemdrop.GetSelection()
    if(self.prop1drop.GetSelection() == 9):
      global ITEM_VALUE1
      ITEM_VALUE1[i] = self.prop1summon.GetSelection()
  
  def UpdateSummon2(self, e):
    i = self.itemdrop.GetSelection()
    if(self.prop2drop.GetSelection() == 9):
      global ITEM_VALUE2
      ITEM_VALUE2[i] = self.prop2summon.GetSelection()
  
  def UpdateSummon3(self, e):
    i = self.itemdrop.GetSelection()
    if(self.prop3drop.GetSelection() == 9):
      global ITEM_VALUE3
      ITEM_VALUE3[i] = self.prop3summon.GetSelection()
  
  def UpdateSummon4(self, e):
    i = self.itemdrop.GetSelection()
    if(self.prop4drop.GetSelection() == 9):
      global ITEM_VALUE4
      ITEM_VALUE4[i] = self.prop4summon.GetSelection()
  
  def UpdateValue1(self, e):
    i = self.itemdrop.GetSelection()
    temp = self.prop1text.GetValue()
    if(temp == '' or temp == 'None'): temp = '0'
    if(self.prop1drop.GetSelection() >= 0 and self.prop1drop.GetSelection() < 9):
      global ITEM_VALUE1
      ITEM_VALUE1[i] = s8bit(int(temp))
  
  def UpdateValue2(self, e):
    i = self.itemdrop.GetSelection()
    temp = self.prop2text.GetValue()
    if(temp == '' or temp == 'None'): temp = '0'
    if(self.prop2drop.GetSelection() >= 0 and self.prop2drop.GetSelection() < 9):
      global ITEM_VALUE2
      ITEM_VALUE2[i] = s8bit(int(temp))
  
  def UpdateValue3(self, e):
    i = self.itemdrop.GetSelection()
    temp = self.prop3text.GetValue()
    if(temp == '' or temp == 'None'): temp = '0'
    if(self.prop3drop.GetSelection() >= 0 and self.prop3drop.GetSelection() < 9):
      global ITEM_VALUE3
      ITEM_VALUE3[i] = s8bit(int(temp))
  
  def UpdateValue4(self, e):
    i = self.itemdrop.GetSelection()
    temp = self.prop4text.GetValue()
    if(temp == '' or temp == 'None'): temp = '0'
    if(self.prop4drop.GetSelection() >= 0 and self.prop4drop.GetSelection() < 9):
      global ITEM_VALUE4
      ITEM_VALUE4[i] = s8bit(int(temp))
  
  def LoadStats(self, e):
    i = self.itemdrop.GetSelection()
    if(i == -1):
      self.itemdrop.SetSelection(0)
      i = 0
    self.prop1text.Hide()
    self.prop1summon.Hide()
    self.prop2text.Hide()
    self.prop2summon.Hide()
    self.prop3text.Hide()
    self.prop3summon.Hide()
    self.prop4text.Hide()
    self.prop4summon.Hide()
    temp = ITEM_PROP1[i]
    if(temp == 255 or temp == None): temp = 10
    self.prop1drop.SetSelection(temp)
    if(temp >= 0 and temp < 9):
      self.prop1text.SetValue(str(ITEM_VALUE1[i]))
      self.prop1text.Show()
      self.prop1summon.Hide()
    elif(temp == 9):
      self.prop1summon.SetSelection(ITEM_VALUE1[i])
      self.prop1summon.Show()
      self.prop1text.Hide()
    temp = ITEM_PROP2[i]
    if(temp == 255 or temp == None): temp = 10
    self.prop2drop.SetSelection(temp)
    if(temp >= 0 and temp < 9):
      self.prop2text.SetValue(str(ITEM_VALUE2[i]))
      self.prop2text.Show()
      self.prop2summon.Hide()
    elif(temp == 9):
      self.prop2summon.SetSelection(ITEM_VALUE2[i])
      self.prop2summon.Show()
      self.prop2text.Hide()
    temp = ITEM_PROP3[i]
    if(temp == 255 or temp == None): temp = 10
    self.prop3drop.SetSelection(temp)
    if(temp >= 0 and temp < 9):
      self.prop3text.SetValue(str(ITEM_VALUE3[i]))
      self.prop3text.Show()
      self.prop3summon.Hide()
    elif(temp == 9):
      self.prop3summon.SetSelection(ITEM_VALUE3[i])
      self.prop3summon.Show()
      self.prop3text.Hide()
    temp = ITEM_PROP4[i]
    if(temp == 255 or temp == None): temp = 10
    self.prop4drop.SetSelection(temp)
    if(temp >= 0 and temp < 9):
      self.prop4text.SetValue(str(ITEM_VALUE4[i]))
      self.prop4text.Show()
      self.prop4summon.Hide()
    elif(temp == 9):
      self.prop4summon.SetSelection(ITEM_VALUE4[i])
      self.prop4summon.Show()
      self.prop4text.Hide()

  def UpdateBlizzd(self, e):
    i = self.commanddrop.GetSelection()
    global BASE_BLIZZD
    BASE_BLIZZD[i] = self.blizzdcheck.GetValue()


'''
-------------------------------------------------------------------------------
TerrainForm()

A form that allows users to edit the terrain bonuses or penalties for game
map tiles.
-------------------------------------------------------------------------------
'''
class TerrainForm(wx.Panel):
  def __init__(self, parent, id):
    wx.Panel.__init__(self, parent, id)
    self.terrainlabel  = wx.StaticText(self, -1, "Terrain:", wx.Point(10,14))
    self.terraindrop   = wx.Choice(self, -1, wx.Point(100,10), None, TERRAIN)
    self.terraindrop.SetSelection(0)
    #self.terraindrop.Bind(wx.EVT_CHOICE, self.LoadStats)


'''
-------------------------------------------------------------------------------
MainWindow()

A container window that stores each panel in a separate tabbed interface.
Its methods control menubar and statusbar actions.
-------------------------------------------------------------------------------
'''
class MainWindow(wx.Frame):
  def __init__(self, parent, id, title):
    self.dirname = ''
    # icon = wx.Icon(name=â€˜appsnap.icoâ€™, type=wx.BITMAP_TYPE_ICO)
    # frame.SetIcon(icon)
    wx.Frame.__init__(self, parent, id, title, size=(790,440))
    self.SetIcon(wx.Icon("ghost.ico", wx.BITMAP_TYPE_ICO))
    self.nb = wx.Notebook(self, -1)
    self.MakeNotebook()
    
    #self.CreateStatusBar()
    
    if(FILENAME != ''): self.Populate()
    filemenu = wx.Menu()
    filemenu.Append(ID_OPEN, "&Open ...", "Open a ROM")
    filemenu.AppendSeparator()
    filemenu.Append(ID_SAVE, "&Save", "Save data to ROM")
    filemenu.Append(ID_SAVECOPY, "Save &Copy ...", "Save data to copy of the ROM")
    filemenu.AppendSeparator()
    filemenu.Append(ID_EXIT, "E&xit", "Exit the editor")
    helpmenu = wx.Menu()
    helpmenu.Append(ID_LICENSE, "&License", "Read the BSD License agreement")
    helpmenu.Append(ID_ABOUT, "&About " + PROGRAM + " ...", "Information about the editor")
    menuBar = wx.MenuBar()
    menuBar.Append(filemenu, "&File")
    menuBar.Append(helpmenu, "&Help")
    self.SetMenuBar(menuBar)
    wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)
    wx.EVT_MENU(self, ID_LICENSE, self.OnLicense)
    wx.EVT_MENU(self, ID_OPEN, self.OnOpen)
    wx.EVT_MENU(self, ID_SAVE, self.OnSave)
    wx.EVT_MENU(self, ID_SAVECOPY, self.OnSaveCopy)
    wx.EVT_MENU(self, ID_EXIT, self.OnExit)
    self.Show(True)
  
  # Create the UI notebook
  def MakeNotebook(self):
    self.classes = ClassForm(self.nb, -1)
    self.nb.AddPage(self.classes, "Units")
    self.commanders = CommanderForm(self.nb, -1)
    self.nb.AddPage(self.commanders, "Commanders")
    self.items = ItemForm(self.nb, -1)
    self.nb.AddPage(self.items, "Items")
    self.terrain = TerrainForm(self.nb, -1)
    self.nb.AddPage(self.terrain, "Terrain")
  
  # Update all loaded notebook elements
  def UpdateNotebook(self):
    self.classes.LoadStats(0)
    self.commanders.LoadStats(0)
    self.items.LoadStats(0)
  
  # Display about dialog
  def OnAbout(self, e):
    d = wx.MessageDialog(self, PROGRAM + " Version " + str(VERSION) + "\nBy " + AUTHOR + "\n\nEsTool is an editor for the data structures present in Masaya's Der Langrisser for the Nintendo Super Famicom Entertainment System.\n\nThe structures it edits and the human readable values displayed in each drop-down are based entirely on original research.\n\nFor information on the structures this software edits, check the documents section of http://cinnamonpirate.com/.","About " + PROGRAM, wx.OK)
    d.ShowModal()
    d.Destroy()
  
  # Display the license in dialog
  def OnLicense(self, e):
    d = wx.MessageDialog(self, PROGRAM + " Version " + str(VERSION) + "\nCopyright (c) 2008, Derrick Sobodash\nAll rights reserved\n\nRedistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:\n\nâ€¢Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.\nâ€¢Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.\nâ€¢Neither the name of Derrick Sobodash nor the names of his contributors may be used to endorse or promote products derived from this software without specific prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.","License Agreement", wx.OK)
    d.ShowModal()
    d.Destroy()
  
  # Open a file
  def OnOpen(self, e):
    dlg = wx.FileDialog(self, "Choose a Der Langrisser ROM ...", self.dirname, "", "Super Famicom ROM (*.smc)|*.smc", wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
      global FILENAME
      FILENAME = dlg.GetPath()
    dlg.Destroy()
    self.Populate()
  
  # Save data into ROM
  def OnSave(self, e):
    if(FILENAME != ''):
      self.Record()
    else:
      d = wx.MessageDialog(self, "Error: You have not yet loaded a Der Langrisser ROM image. All data tables are currently blank.", "Error: ROM not loaded", wx.OK)
      d.ShowModal()
      d.Destroy()
  
  # Save a copy of the current ROM
  def OnSaveCopy(self, e):
    global FILENAME
    if(FILENAME != ''):
      dlg = wx.FileDialog(self, "Enter a new ROM name", self.dirname, "", "Super Famicom ROM (*.smc)|*.smc", wx.SAVE)
      if dlg.ShowModal() == wx.ID_OK:
        temp = dlg.GetPath()
        if(os.path.isfile(temp)):
          d = wx.MessageDialog(self, "Warning, you are about to write values into an existing ROM.\n\nAre you sure you want to do this?", "Warning: Overwrite alert", wx.YES_NO)
          if d.ShowModal() == wx.ID_YES:
            FILENAME = temp
            self.Record()
        else:
          copy(FILENAME, temp)
          FILENAME = temp
          self.Record()
      dlg.Destroy()
    else:
      d = wx.MessageDialog(self, "Error: You have not yet loaded a Der Langrisser ROM image. All data tables are currently blank.", "Error: ROM not loaded", wx.OK)
      d.ShowModal()
      d.Destroy()
  
  # Exit event
  def OnExit(self, e):
    self.Close(True)
  
  # Populate all internal variables from the current ROM
  def Populate(self):
    global OFFSET_HEAD
    # Check for the header
    if(os.path.getsize(FILENAME) % 0x400 == 0x200):
      OFFSET_HEAD = 0x200
    f = open(FILENAME, "rb")
    # Class table
    f.seek(OFFSET_CLASS + OFFSET_HEAD)
    for i in range(0, 255):
      f.seek(1, 1)
      UNIT_FLYING[i] = unpack("<b", f.read(1))[0]
      f.seek(1, 1)
      UNIT_TYPE[i]   = unpack("<b", f.read(1))[0]
      UNIT_TIER[i]   = unpack("<b", f.read(1))[0]
      UNIT_AT[i]     = unpack("<b", f.read(1))[0]
      UNIT_DF[i]     = unpack("<b", f.read(1))[0]
      UNIT_MV[i]     = unpack("<b", f.read(1))[0]
      UNIT_RANGE[i]  = unpack("<b", f.read(1))[0]
      UNIT_A[i]      = unpack("<b", f.read(1))[0]
      UNIT_D[i]      = unpack("<b", f.read(1))[0]
      UNIT_MP[i]     = unpack("<b", f.read(1))[0]
      UNIT_MDEF[i]   = unpack("<b", f.read(1))[0]
      UNIT_TROOPS[i] = unpack("<b", f.read(1))[0]
      UNIT_COST[i]   = unpack("<b", f.read(1))[0]
      f.seek(1, 1)
      UNIT_AWARD[i]  = unpack("<B", f.read(1))[0]
      UNIT_EXP[i]    = unpack("<B", f.read(1))[0]
      UNIT_VALUE[i]  = unpack("<B", f.read(1))[0]
      UNIT_UNIT1[i]  = unpack("<B", f.read(1))[0]
      UNIT_UNIT2[i]  = unpack("<B", f.read(1))[0]
      UNIT_UNIT3[i]  = unpack("<B", f.read(1))[0]
      UNIT_SPELL1[i] = unpack("<B", f.read(1))[0]
      UNIT_SPELL2[i] = unpack("<B", f.read(1))[0]
      UNIT_SPELL3[i] = unpack("<B", f.read(1))[0]
      UNIT_SPELL4[i] = unpack("<B", f.read(1))[0]
    # Sprites/Palettes
    f.seek(OFFSET_SPRITE + OFFSET_HEAD)
    for i in range(0, 255):
      UNIT_SPRITE[i] = unpack("<B", f.read(1))[0]
      UNIT_PALETTE[i]= unpack("<B", f.read(1))[0]
    # Battle Data
    f.seek(OFFSET_BATTLE + OFFSET_HEAD)
    for i in range(0, 255):
      f.seek(2, 1)
      UNIT_BATX[i]   = unpack("<B", f.read(1))[0]
      UNIT_BATY[i]   = unpack("<B", f.read(1))[0]
      UNIT_BLAND[i]  = unpack("<B", f.read(1))[0]
      UNIT_BAIR[i]   = unpack("<B", f.read(1))[0]
      UNIT_RIDER[i]  = unpack("<B", f.read(1))[0]
      f.seek(1, 1)
    # Commander base stats
    f.seek(OFFSET_BASE + OFFSET_HEAD)
    for i in range(0, 18):
      BASE_CLASS[i]  = unpack("<b", f.read(1))[0]
      BASE_MP[i]     = unpack("<b", f.read(1))[0]
      BASE_A[i]      = unpack("<b", f.read(1))[0]
      BASE_D[i]      = unpack("<b", f.read(1))[0]
      BASE_AT[i]     = unpack("<b", f.read(1))[0]
      BASE_DF[i]     = unpack("<b", f.read(1))[0]
      magic1         = decbin(unpack("<B", f.read(1))[0])
      magic2         = decbin(unpack("<B", f.read(1))[0])
      magic3         = decbin(unpack("<B", f.read(1))[0])
      magic4         = decbin(unpack("<B", f.read(1))[0])
      BASE_UNDEAD[i] = int(magic1[0])
      BASE_TORNDO[i] = int(magic1[1])
      BASE_BLIZZD[i] = int(magic1[2])
      BASE_METEOR[i] = int(magic1[3])
      BASE_FBALL[i]  = int(magic1[4])
      BASE_THUNDR[i] = int(magic1[5])
      BASE_BLAST[i]  = int(magic1[6])
      BASE_MARROW[i] = int(magic1[7])
      BASE_PROTE1[i] = int(magic2[0])
      BASE_MUTE[i]   = int(magic2[1])
      BASE_SLEEP[i]  = int(magic2[2])
      BASE_FHEAL2[i] = int(magic2[3])
      BASE_FHEAL1[i] = int(magic2[4])
      BASE_HEAL2[i]  = int(magic2[5])
      BASE_HEAL1[i]  = int(magic2[6])
      BASE_EQUAKE[i] = int(magic2[7])
      BASE_QUICK[i]  = int(magic3[0])
      BASE_CHARM[i]  = int(magic3[1])
      BASE_RESIST[i] = int(magic3[2])
      BASE_TELEPT[i] = int(magic3[3])
      BASE_ZONE[i]   = int(magic3[4])
      BASE_ATTAK2[i] = int(magic3[5])
      BASE_ATTAK1[i] = int(magic3[6])
      BASE_PROTE2[i] = int(magic3[7])
      BASE_DEMON[i]  = int(magic4[0])
      BASE_GOLEM[i]  = int(magic4[1])
      BASE_SLMNDR[i] = int(magic4[2])
      BASE_DRAGON[i] = int(magic4[3])
      BASE_FREYJA[i] = int(magic4[4])
      BASE_VALKYR[i] = int(magic4[5])
      BASE_DECRSE[i] = int(magic4[6])
      BASE_AGAIN[i]  = int(magic4[7])
      BASE_SEX[i]    = unpack("<B", f.read(1))[0]
      BASE_PICTURE[i]= unpack("<B", f.read(1))[0]
      BASE_TROOPS[i] = unpack("<b", f.read(1))[0]
      BASE_UNIT[i]   = unpack("<B", f.read(1))[0]
      f.seek(2, 1)
    # Items
    f.seek(OFFSET_ITEMS + OFFSET_HEAD)
    for i in range(0, 36):
      ITEM_PROP1[i]  = unpack("<B", f.read(1))[0]
      ITEM_VALUE1[i]  = unpack("<b", f.read(1))[0]
      ITEM_PROP2[i]  = unpack("<B", f.read(1))[0]
      ITEM_VALUE2[i]  = unpack("<b", f.read(1))[0]
      ITEM_PROP3[i]  = unpack("<B", f.read(1))[0]
      ITEM_VALUE3[i]  = unpack("<b", f.read(1))[0]
      ITEM_PROP4[i]  = unpack("<B", f.read(1))[0]
      ITEM_VALUE4[i]  = unpack("<b", f.read(1))[0]
    f.close()
    self.UpdateNotebook()
  
  # Writes out all data buffers into FILENAME.
  def Record(self):
    global OFFSET_HEAD
    # Check for the header
    if(os.path.getsize(FILENAME) % 0x400 == 0x200):
      OFFSET_HEAD = 0x200
    f = open(FILENAME, "rb+wb")
    # Class table
    f.seek(OFFSET_CLASS + OFFSET_HEAD)
    for i in range(0, 255):
      f.seek(1, 1)
      f.write(pack("<b", UNIT_FLYING[i]))
      f.seek(1, 1)
      f.write(pack("<b", UNIT_TYPE[i]))
      f.write(pack("<b", UNIT_TIER[i]))
      f.write(pack("<b", UNIT_AT[i]))
      f.write(pack("<b", UNIT_DF[i]))
      f.write(pack("<b", UNIT_MV[i]))
      f.write(pack("<b", UNIT_RANGE[i]))
      f.write(pack("<b", UNIT_A[i]))
      f.write(pack("<b", UNIT_D[i]))
      f.write(pack("<b", UNIT_MP[i]))
      f.write(pack("<b", UNIT_MDEF[i]))
      f.write(pack("<b", UNIT_TROOPS[i]))
      f.write(pack("<b", UNIT_COST[i]))
      f.seek(1, 1)
      f.write(pack("<B", UNIT_AWARD[i]))
      f.write(pack("<B", UNIT_EXP[i]))
      f.write(pack("<B", UNIT_VALUE[i]))
      f.write(pack("<B", UNIT_UNIT1[i]))
      f.write(pack("<B", UNIT_UNIT2[i]))
      f.write(pack("<B", UNIT_UNIT3[i]))
      f.write(pack("<B", UNIT_SPELL1[i]))
      f.write(pack("<B", UNIT_SPELL2[i]))
      f.write(pack("<B", UNIT_SPELL3[i]))
      f.write(pack("<B", UNIT_SPELL4[i]))
    # Sprites/Palettes
    f.seek(OFFSET_SPRITE + OFFSET_HEAD)
    for i in range(0, 255):
      f.write(pack("<B", UNIT_SPRITE[i]))
      f.write(pack("<B", UNIT_PALETTE[i]))
    # Commander base stats
    f.seek(OFFSET_BASE + OFFSET_HEAD)
    for i in range(0, 18):
      f.write(pack("<b", BASE_AT[i]))
      f.write(pack("<b", BASE_DF[i]))
      magic1 = str(int(BASE_UNDEAD[i])) + str(int(BASE_TORNDO[i])) + str(int(BASE_BLIZZD[i])) + str(int(BASE_METEOR[i])) + str(int(BASE_FBALL[i])) + str(int(BASE_THUNDR[i])) + str(int(BASE_BLAST[i])) + str(int(BASE_MARROW[i]))
      magic2 = str(int(BASE_PROTE1[i])) + str(int(BASE_MUTE[i])) + str(int(BASE_SLEEP[i])) + str(int(BASE_FHEAL2[i])) + str(int(BASE_FHEAL1[i])) + str(int(BASE_HEAL2[i])) + str(int(BASE_HEAL1[i])) + str(int(BASE_EQUAKE[i]))
      magic3 = str(int(BASE_QUICK[i])) + str(int(BASE_CHARM[i])) + str(int(BASE_RESIST[i])) + str(int(BASE_TELEPT[i])) + str(int(BASE_ZONE[i])) + str(int(BASE_ATTAK2[i])) + str(int(BASE_ATTAK1[i])) + str(int(BASE_PROTE2[i]))
      magic4 = str(int(BASE_DEMON[i])) + str(int(BASE_GOLEM[i])) + str(int(BASE_SLMNDR[i])) + str(int(BASE_DRAGON[i])) + str(int(BASE_FREYJA[i])) + str(int(BASE_VALKYR[i])) + str(int(BASE_DECRSE[i])) + str(int(BASE_AGAIN[i]))
      f.write(pack("<B", atoi(magic1, 2)))
      f.write(pack("<B", atoi(magic2, 2)))
      f.write(pack("<B", atoi(magic3, 2)))
      f.write(pack("<B", atoi(magic4, 2)))
      f.write(pack("<B", int(BASE_SEX[i])))
      f.write(pack("<B", int(BASE_PICTURE[i])))
      f.write(pack("<b", BASE_TROOPS[i]))
      f.write(pack("<B", BASE_UNIT[i]))
      f.seek(6, 1)
    # Items
    f.seek(OFFSET_ITEMS + OFFSET_HEAD)
    for i in range(0, 36):
      f.write(pack("<B", ITEM_PROP1[i]))
      f.write(pack("<b", ITEM_VALUE1[i]))
      f.write(pack("<B", ITEM_PROP2[i]))
      f.write(pack("<b", ITEM_VALUE2[i]))
      f.write(pack("<B", ITEM_PROP3[i]))
      f.write(pack("<b", ITEM_VALUE3[i]))
      f.write(pack("<B", ITEM_PROP4[i]))
      f.write(pack("<b", ITEM_VALUE4[i]))
    f.close()


'''
-------------------------------------------------------------------------------
decbin(number):

Converts a decimal (base-10) number to a binary (base-2) number and returns
the binary representation as a string.
-------------------------------------------------------------------------------
'''
def decbin(n):
  bStr = ''
  if n < 0: raise ValueError, "must be a positive integer"
  if n == 0: return '0'.rjust(8, "0")
  while n > 0:
    bStr = str(n % 2) + bStr
    n = n >> 1
  return bStr.rjust(8, "0")


'''
-------------------------------------------------------------------------------
8bit(number):

Forces number to be an 8-bit signed value. If the number is larger than
0xff, it will drop the upper bits and keep only the bottom 8 bits. If the
number is larger than 127, it will be interpreted as a negative number.
-------------------------------------------------------------------------------
'''
def s8bit(n):
  if(n > 0xff): n = n & 0xff
  if(n < -128): n = n & 0xff
  if(n > 127): n = n - 256
  return n


'''
-------------------------------------------------------------------------------
u8bit(number):

Forces number to be an 8-bit unsigned value. If the number is larger than
0xff, it will drop the upper bits and keep only the bottom 8 bits.
-------------------------------------------------------------------------------
'''
def u8bit(n):
  if(n > 0xff): n = n & 0xff
  return n


'''
-------------------------------------------------------------------------------
Main

Check command line variables, create the window and enter our main loop/
-------------------------------------------------------------------------------
'''
# Check if a FILENAME was specified on the command line
if(len(sys.argv) > 1):
  temp = os.path.realpath(sys.argv[1])
  if(os.path.exists(temp) == True):
    FILENAME = temp

# Print the copyright information
print PROGRAM + " " + str(VERSION)
print "Copyright (c) 2008 " + AUTHOR

# Initialization code and loop
app = wx.PySimpleApp()
frame = MainWindow(None, -1, PROGRAM + " " + str(VERSION))
frame.Show(1)
app.MainLoop()



