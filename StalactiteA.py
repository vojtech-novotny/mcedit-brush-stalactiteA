# Stalactite
# Made by Acaran
# acaran101.wordpress.com

from editortools.brush import createBrushMask, createTileEntities
from pymclevel.level import extractHeights
import itertools
import random

displayName = "Stalactite A"


def createInputs(self):
    self.inputs = (
    {'W': (3, 1, 4096), 'H': (3, 1, 4096), 'L': (3, 1, 4096)},
    {'Max Length': (5, 1, 256)},
    {'Chance to Start': (25, 0, 100)},
    {'Chance to Extend': (10, 0, 100)},
    {'a':'Place On:','blockToPlaceOn': materials.blockWithID(1, 0)},
    {'a':'Material:','block': materials.blockWithID(106, 1)},
    {'Place On Everything': False},
    {'Minimum Spacing': 1}
    )


def applyToChunkSlices(self, op, chunk, slices, brushBox, brushBoxThisChunk):

    block = op.options['block']
    blockToPlaceOn = op.options['blockToPlaceOn']
    chanceToStart = op.options['Chance to Start']
    chanceToExtend = op.options['Chance to Extend']
    maxLength = op.options['Max Length']
    placeOnEverything = op.options['Place On Everything']

    blocks = chunk.Blocks[slices]
    
    brushMask = createBrushMask(op.tool.getBrushSize(), op.options['Style'], brushBox.origin, brushBoxThisChunk, op.options['Noise'], op.options['Hollow'])
    blockMask = blocks == -1
    
    for x in range(0, blocks.shape[0]):
        for z in range(0, blocks.shape[1]):
            length = -1
            for y in range(blocks.shape[2] - 1, -1, -1):
                if (brushMask[x, z, y] == False):
                    length = -1
                elif (length == -1 and (blocks[x, z, y] == blockToPlaceOn.ID or (placeOnEverything and blocks[x, z, y] != 0))):
                    length = 0
                elif (blocks[x, z, y] == 0):
                    if (length == 0):
                        if (random.randint(1, 100) <= chanceToStart):
                            blockMask[x, z, y] = True
                            length = 1
                        else:
                            length = -1
                    elif (length > 0 and length < maxLength):
                        if (random.randint(1, 100) <= chanceToExtend):
                            blockMask[x, z, y] = True
                            length += 1
                        else:
                            length = -1
                    else:
                        length = -1
                else:
                    length = -1
                
    chunk.Blocks[slices][blockMask] = block.ID
    chunk.Data[slices][blockMask] = block.blockData
