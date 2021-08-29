# convert .txt CSV style file into an LL json
import json

outputDict = dict()
rollData = list()

def parseName(line):
    #// NameIsHere
    return line[2:].strip()

def parseDescriptionAndTags(line):
    #//notes: balalahahlalha tags: (pve,mk)
    notesIndex = line.find('notes:')
    tagsIndex = line.find('tags:')

    desc = line[notesIndex+len('notes:'):tagsIndex].strip()
    tags = line[tagsIndex+len('tags:')].replace('(', '').replace(')', '')

    tag_l = tags.split(',')

    return desc, tag_l

def parseItemAndPerks(line):
    l = line.split(':')[1]
    ip = l.split('&')
    item = ip[0].split('=')[1]
    perks = ip[1].split('=')[1].split(',')

    return item, perks

with open('input.txt', 'r') as dimFile:
    title = dimFile.readline()[len('title:'):].strip()
    desc = dimFile.readline()[len('description:'):].strip()

    lines = dimFile.readlines()

    ## item parsing
    i = 0
    while i < len(lines):
        print(lines[i])

        if len(lines[i].strip()) == 0:
            i += 1
            continue
        print(lines[i+1])
        #item metadata
        itemName = parseName(lines[i].strip())
        itemDesc, itemTags = parseDescriptionAndTags(lines[i+1].strip())
        perkColumns = [set(), set(), set(), set()]
        itemHash = ""

        # now for perk rolls.
        i = i + 2
        while i < len(lines) and len(lines[i].strip()) > 0:
            print(lines[i])
            itemHash, perkList = parseItemAndPerks(lines[i].strip())

            for j in range(4):
                perkColumns[j].add(perkList[j])
            i = i + 1

        # END perk parsing. save it to the list and prepare for next item or EOF
        item = dict()
        item['name'] = itemName
        item['description'] = itemDesc
        item['hash'] = int(itemHash)
        item['plugs'] = list(map(list, perkColumns))
        item['tags'] = itemTags

        rollData.append(item)
        i += 1
        #END Item Parsing
    # END file/Wishlist parsing
    outputDict['name'] = title
    outputDict['description'] = desc
    outputDict['data'] = rollData

    with open('output.json', 'w') as outfile:
        outputJson = json.dumps(outputDict)
        outfile.write(outputJson)
