# Copyright 2022 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import math,queue,asyncio

from PIL import ImageDraw
from .Generation import * 
from .FunctionsPill import imagSize,centrText,imgD
from .options import *
from . import openFile

async def characterBackground(rezFrame,person,imgs,adapt,splash = None):
    if imgs:
        frame = userImageTree(imgs, element = person.element.value, adaptation = adapt)
    else:
        if splash:
            banner = await imagSize(link = splash,size = (2351,1168))
        else:
            banner = await imagSize(link = person.images.banner.url,size = (2351,1168))
        frame = maskaAdd(person.element.value, banner, teample = 3)
    rezFrame.put_nowait(frame)

async def infoCharter(bg,characters,lvlName,nameRes):
    d = ImageDraw.Draw(bg)
    d.text((37,46), characters.name, font = t24, fill=(0,0,0,255))
    d.text((37,45), characters.name, font = t24, fill=coloring)
    d.text((37,99),f"{lvlName['lvl']}: {characters.level}/90",font = t24, fill=(0,0,0,255))
    d.text((37,98),f"{lvlName['lvl']}: {characters.level}/90",font = t24, fill=coloring)
    d.text((83,145), str(characters.friendship_level), font = t24, fill=(0,0,0,255))
    d.text((83,144), str(characters.friendship_level), font = t24, fill=coloring)
    bg.paste(FRENDS,(37,142),FRENDS)
    nameRes.put_nowait(bg)

async def talants(talatsRes,characters):
    count = 0
    tallantsRes = []
    for key in characters.skills:
        if key.level > 9:
            talantsBg = TalantsFrameT_GoldTeampleTree.copy()
        else:
            talantsBg = TalantsFrameTeampleTree.copy()
        d = ImageDraw.Draw(talantsBg)
        imagesIconTalants = await imgD(link = key.icon.url)
        imagesIconTalants = imagesIconTalants.resize((67,67))
        talantsBg.paste(imagesIconTalants, (16,0),imagesIconTalants)
        if len(str(key.level)) == 2:
            d.text((36,67), str(key.level), font = t24, fill=coloring)
        else:
            d.text((41,66), str(key.level), font = t24, fill=coloring)
        tallantsRes.append(talantsBg)
        count+=1
        if count == 3:
            break
    talatsRes.put_nowait(tallantsRes)

async def weapon(weaponRes,characters,lvlName):
    if characters.detail.artifact_name_set != "":
        return None
    WeaponBg = WeaponBgTeampleTree.copy()
    d = ImageDraw.Draw(WeaponBg)
    proc = False    
    name = characters.detail.name
    lvl = characters.level
    lvlUp = characters.refinement
    baseAtt = characters.detail.mainstats.value
    imageStats = None
    dopStat = 0

    for substate in characters.detail.substats:
        imageStats = getIconAdd(substate.prop_id, icon = True, size = (26,26))
        if not imageStats:
            continue
        dopStat = substate.value
        if str(substate.type) == "DigitType.PERCENT":
            proc = True
    if imageStats:
        WeaponBg.paste(imageStats,(318,66),imageStats)

    stars = star(characters.detail.rarity).resize((93,31))
    image = await imagSize(link = characters.detail.icon.url,size = (143,152))

    WeaponBg.paste(image,(6,0),image)
    WeaponBg.paste(WeaponLight,(0,143),WeaponLight)
    WeaponBg.paste(stars,(28,136),stars)
    
    position,font = centrText(name, witshRam = 329, razmer = 24, start = 170)
    d.text((position,10), str(name), font= font, fill=(0,0,0,255)) 
    d.text((position,9), str(name), font= font, fill=coloring) 
    d.text((185 ,114), f"R{lvlUp}", font= t24, fill=(248,199,135,255))

    position,font = centrText(f"{lvlName['lvl']}: {lvl}/90", witshRam = 240, razmer = 24, start = 245)
    d.text((position,114), f"{lvlName['lvl']}: {lvl}/90", font= font, fill=coloring) 

    position,font = centrText(baseAtt, witshRam = 79, razmer = 24, start = 214)    
    d.text((position,64), str(baseAtt), font= font, fill=coloring)

    if proc:
        position,font = centrText(f'{dopStat}%', witshRam = 97, razmer = 24, start = 350)
        d.text((position,64), f'{dopStat}%', font= font, fill=coloring)
    else:
        position,font = centrText(str(dopStat), witshRam = 97, razmer = 24, start = 350)
        d.text((position,64), str(dopStat), font= font, fill=coloring)
    
    weaponRes.put_nowait(WeaponBg)
    
async def constant(rezConstant,characters,person):
    constantRes = []  
    for key in characters.constellations:
        openConstBg,closedConstBg = openImageElementConstant(person.element.value, teampt = 3)
        
        openConstBg = openConstBg.resize((87,89))
        closedConstBg = closedConstBg.resize((87,89))
        imageIcon = await imgD(link = key.icon.url)
        imageIcon =  imageIcon.resize((52,52))
        
        if not key.unlocked:
            closedConstBg.paste(imageIcon, (18,19),imageIcon)
            closedConstBg.paste(ClosedConstTree, (20,21),ClosedConstTree)
            
            const = closedConstBg
        else:
            openConstBg.paste(imageIcon, (18,19),imageIcon)
            const = openConstBg
        constantRes.append(const)
    
    rezConstant.put_nowait(constantRes)


def appendTalat(bg,talantsL):
    position = (597,426)
    for key in talantsL:
        bg.paste(key, position,key)
        position = (position[0],position[1]+118)
    return bg

def appendConst(bg,constL):
    position = (22,284)
    for key in constL:
        bg.paste(key, position,key)
        position = (position[0],position[1]+72)
    return bg

def appendArt(bg,artif):
    position = (1327,19)
    for key in artif:
        bg.paste(key, position,key)
        position = (position[0],position[1]+156)
    return bg

async def stats(AttributeBg,statRes,characters,assets):
    g = characters.stats
    maxStat = 0
    elementUp = None
    dopval = {}
    pos = (752,239)
    for key in g:
        if key[0] in ["BASE_HP","FIGHT_PROP_BASE_ATTACK","FIGHT_PROP_BASE_DEFENSE"]:
            dopval[key[0]] = key[1].value

    for key in reversed(list(g)):
        if key[1].value == 0:
            continue
        if key[1].id in [40,41,42,43,44,45,46]:
            if key[1].value > maxStat:
                elementUp = key
                maxStat = key[1].value
            if key[1].id == 40:
                key = elementUp
            else:
                continue
        
        iconImg = getIconAdd(key[0])
        if not iconImg:
            continue
        txt = assets.get_hash_map(key[0])
        icon = await imagSize(image = iconImg,fixed_width = 23)
        AttributeBg.paste(icon,pos,icon)

        if not key[1].id in stat_perc:
            value = str(math.ceil(key[1].value))
        else:
            value = f"{round(key[1].value * 100, 1)}%"
        d = ImageDraw.Draw(AttributeBg)
        x,y = t24.getsize(value)
        d.text((pos[0]+520-x,pos[1]), value, font = t24, fill=coloring)
        d.text((pos[0]+41,pos[1]), str(txt), font = t18, fill=coloring)
        
        if key[0] in dopStatAtribute:
            dopStatVal = int(key[1].value)
            dopStatValArtifact = int(key[1].value - dopval[dopStatAtribute[key[0]]])
            if dopStatValArtifact != 0:
                xx,y = t15.getsize(f"+{dopStatValArtifact}")
                d.text((pos[0]+520-xx,pos[1]+30),f"+{dopStatValArtifact}", font = t15, fill=(141,231,141))
                x,y = t15.getsize(f"+{dopStatVal}")
                d.text((pos[0]+520-x-xx,pos[1]+30),str(dopStatVal), font = t15, fill=coloring)

        pos = (pos[0],pos[1]+62)
        
    statRes.put_nowait(AttributeBg)

async def naborArtifact(info,listArt,ArtifactNameBg):
    count = 0
    for key in info:
        if info[key] > 1:
            count += 1
    if count != 0:
        d = ImageDraw.Draw(ArtifactNameBg)
        ArtifactNameBg.paste(ArtifactSetIcon,(749,721),ArtifactSetIcon)
        position = (1250,722)
        for key in info:
            if info[key] > 1:
                if count == 1:
                    ArtifactNameBg.paste(ArtifactSetCount,(1234,738),ArtifactSetCount)
                    centrName,fonts = centrText(key, witshRam = 367 , razmer = 20, start = 840) 
                    d.text((centrName,740), str(key), font= fonts, fill=(141,231,141))
                    d.text((1248 ,739), str(info[key]), font= t24, fill=coloring)
                    break
                else:
                    ArtifactNameBg.paste(ArtifactSetCount,(1234,position[1]),ArtifactSetCount)
                    centrName,fonts = centrText(key, witshRam = 367 , razmer = 20, start = 840) 
                    d.text((centrName,position[1]), str(key), font= fonts, fill=(141,231,141))
                    d.text((1248 ,position[1]), str(info[key]), font= t24, fill=coloring)
                    position = (position[0],position[1]+28)
    listArt.put_nowait(ArtifactNameBg)

async def creatArtifact(artifacResSave,infpart,imageStats):
    ArtifactBg = ArtifactFrame.copy()
    ArtifactBgs = ArtifactBg.copy()
    ArtifactUp = ArtifactMaska.copy()

    artimg = await imagSize(link = infpart.detail.icon.url,size = (233,233))
    ArtifactBg.paste(artimg,(-57,-53),artimg)
    ArtifactBg = Image.composite(ArtifactBg, ArtifactBgs, ArtifactUp)

    d = ImageDraw.Draw(ArtifactBg)
    if str(infpart.detail.mainstats.type) == "DigitType.PERCENT":
        val = f"{infpart.detail.mainstats.value}%"
    else:
        val = infpart.detail.mainstats.value
    x,y = t32.getsize(str(val))
    d.text((174-x,56), str(val), font= t32, fill=coloring)
    ArtifactBg.paste(imageStats,(150,20),imageStats)
    d.text((136,100), f"+{infpart.level}", font= t17, fill=coloring)

    starsImg = star(infpart.detail.rarity).resize((83,29))
    ArtifactBg.paste(starsImg,(51,96),starsImg)
    cs = 0
    positionIcon = (221,26)
    for key in infpart.detail.substats:
        v = f"+{key.value}"
        if str(key.type) == "DigitType.PERCENT":
            v = f"{v}%"
        imageStats = getIconAdd(key.prop_id, icon = True)
        if not imageStats:
            continue
        imageStats= await imagSize(image = imageStats,fixed_width = 26) 
        ArtifactBg.paste(imageStats,positionIcon,imageStats)
        d.text((positionIcon[0]+32,positionIcon[1]), v, font= t24, fill=coloring)
        cs += 1
        positionIcon = (positionIcon[0]+143,positionIcon[1])
        if cs == 2:
            positionIcon = (221,86)
    artifacResSave.put_nowait(ArtifactBg)

async def artifacAdd(rezArt,naborSet,characters):
    artifactRes = {
        "art1": None,
        "art2": None,
        "art3": None,
        "art4": None,
        "art5": None
        }
    count = 0
    listArt = {}
    artifacRes = []
    for key in characters.equipments:
        if key.detail.artifact_name_set == "":
            continue
        if not key.detail.artifact_name_set in listArt:
            listArt[key.detail.artifact_name_set] = 1
        else:
            listArt[key.detail.artifact_name_set] += 1

        imageStats = getIconAdd(key.detail.mainstats.prop_id, icon = True, size = (22,27))
        if not imageStats:
            continue

        count += 1
        artifactRes[f"art{count}"] = queue.Queue()
        await creatArtifact(artifactRes[f"art{count}"],key,imageStats)

    for key in artifactRes:
        if artifactRes[key]:
            artifacRes.append(artifactRes[key].get())
    naborSet.put_nowait(listArt)
    rezArt.put_nowait(artifacRes)

async def itog(listArt,talansRes,rezConstant,weaponRes,rezArt,signatureRes):
    res = appendTalat(listArt,talansRes)
    res = appendConst(res,rezConstant)
    res = appendArt(res,rezArt)
    res.paste(weaponRes,(746,33),weaponRes)
    d = ImageDraw.Draw(res)
    d.text((31,757), signatureRes, font= t24, fill=coloring)

    return res

async def generationTree(characters,assets,img,adapt,signatureRes,lvl, splash):
    person = assets.character(characters.id)
    try:
        frame = queue.Queue()
        nameRes = queue.Queue()
        talansRes = queue.Queue()
        weaponRes = queue.Queue()
        rezConstant = queue.Queue()
        statRes = queue.Queue()
        rezArt = queue.Queue()
        rezArtSet = queue.Queue()
        listArt = queue.Queue()
        if splash:
            await asyncio.create_task(characterBackground(frame,person,img,adapt,characters.image.banner.url))
        else:
            await asyncio.create_task(characterBackground(frame,person,img,adapt))
        tal = asyncio.create_task(talants(talansRes,characters))
        con = asyncio.create_task(constant(rezConstant,characters,person))
        wea = asyncio.create_task(weapon(weaponRes,characters.equipments[-1],lvl))
        arti = asyncio.create_task(artifacAdd(rezArt,rezArtSet,characters))

        await asyncio.gather(arti,tal,con,wea)
        
        await infoCharter(frame.get(),characters,lvl,nameRes)
        await stats(nameRes.get(),statRes,characters,assets)
        await naborArtifact(rezArtSet.get(),listArt,statRes.get())
        return await itog(listArt.get(),talansRes.get(),rezConstant.get(),weaponRes.get(),rezArt.get(),signatureRes)
    except Exception as e:
        print("ERROR: ", e)