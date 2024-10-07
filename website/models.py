from django.db import models

from email_login.models import User

class UserNickname(models.Model):
    nickname = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
    
    def random_nickname_generator():
        import random

        nicknames = [
        'RuneMaster', 'BladeOfDestiny', 'ShadowStriker', 'KnightOfValor', 'MysticMage', 
        'DragonSlayerX', 'ElvenArcher', 'DwarfSmith', 'NecroKnight', 'PhoenixRiderX', 
        'SilverSorcerer', 'WarlockLord', 'StormBringer', 'FrostKnight', 'DarkAssassin', 
        'FireWielder', 'ShadowHunter', 'IceMage', 'ThunderFist', 'GoldenWarrior', 
        'CrystalSeer', 'RuneWarrior', 'DragonTamer', 'ArcaneArcher', 'ShadowMage', 
        'SteelKnight', 'WindRider', 'BattleMage', 'GoblinCrusher', 'OrcBane', 
        'SilverRanger', 'RuneSlayer', 'MysticWarrior', 'DeathBringer', 'LightBearer', 
        'StormCaller', 'StoneGuardian', 'PhoenixKnight', 'DragonKnight', 'BladeDancer', 
        'IronClad', 'ShadowWalker', 'RuneHunter', 'StormWarrior', 'FlameWarden', 
        'RuneCraft', 'SpiritWalker', 'FireBlade', 'LightningStriker', 'IceRanger', 
        'RuneDefender', 'DuskMage', 'FrostGiant', 'StormWarden', 'ShadowFury', 
        'BladeMaster', 'WindWalker', 'RuneSentinel', 'StoneCrusher', 'IronGuard', 
        'PhoenixBlade', 'DragonWarden', 'ArcaneDefender', 'StormKnight', 'BlazeMage', 
        'RuneWarden', 'ShadowBlade', 'FrostWarden', 'LightningMage', 'WarriorMage', 
        'DarkRider', 'RuneWizard', 'DragonFury', 'ShadowKnight', 'StoneWarden', 
        'PhoenixWarden', 'IceKnight', 'StormRider', 'RuneBane', 'ShadowWizard', 
        'FlameKnight', 'LightningBlade', 'IronWarden', 'PhoenixMage', 'StormWizard', 
        'RuneWalker', 'FrostMage', 'BlazeKnight', 'ShadowWarden', 'RuneTamer', 
        'DragonWalker', 'WindKnight', 'IronMage', 'PhoenixRider', 'RuneRider', 
        'ShadowWalkerX', 'FrostKnightX', 'BlazeWarden', 'StormDefender', 'IronKnight'
        ]

        nickname = random.choice(nicknames) + str(random.randint(10,99))
        return nickname