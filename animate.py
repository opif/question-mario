#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

def createAnimationBaseLayer(image, layer):
  pdb.gimp_image_undo_group_start(image)

  layer1 = layer.copy()
  layer1.visible = True
  layer2 = layer.copy()
  layer2.visible = True
  layer2.set_offsets(image.width, 0)
  image.add_layer(layer1)
  image.add_layer(layer2)
  new_layer = image.merge_visible_layers(0)
  new_layer.visible = False;
  new_layer.name = 'animation base layer'

  pdb.gimp_image_undo_group_end(image)
  pdb.gimp_displays_flush()

  return new_layer

def calculateDelay(frameNo, framerate):
  nextDelay = (frameNo + 1) * 1000 / framerate
  currentDelay = frameNo * 1000 / framerate
  return nextDelay - currentDelay

def createFrame(image, frameNo, backgroundLayer, animatedLayer, duration, framerate):
  pdb.gimp_image_undo_group_start(image)

  currentDelay = calculateDelay(frameNo, framerate)

  newBackgroundLayer = backgroundLayer.copy()
  newBackgroundLayer.visible = True
  newAnimatedLayer = animatedLayer.copy()
  newAnimatedLayer.visible = True
  newAnimatedLayer.set_offsets(frameNo * image.width / (duration * framerate / 1000) - image.width, 0)
  image.add_layer(newBackgroundLayer)
  image.add_layer(newAnimatedLayer)
  frameLayer = image.merge_down(newAnimatedLayer, 0)
  frameLayer.visible = False
  frameLayer.name = 'frame #{} ({}ms)'.format(frameNo, currentDelay)
  print(frameNo, framerate, 1000/framerate)

  pdb.gimp_image_undo_group_end(image)
  pdb.gimp_displays_flush()

  return frameLayer


def animateImage(image, drawable, backgroundLayer, framerate = 24, duration = 1000):
  for layer in image.layers:
    layer.visible = False;

  animationBaseLayer = createAnimationBaseLayer(image, drawable)

  for frame in range(duration * framerate / 1000):
    createFrame(image, frame, backgroundLayer, animationBaseLayer, duration, framerate)

  image.remove_layer(animationBaseLayer)

def registration():
  animateMenu='<Image>/Filters/Animation'

  animateHIDesc='Animated Foreground Slide'

  animateParms=[
    (PF_IMAGE, 'image', 'Input image', None),
    (PF_DRAWABLE, 'drawable', 'Selected layer', None),
    (PF_LAYER, 'backgroundLayer', 'Background layer', None),
    (PF_INT, 'framerate', 'Desired animation framerate', 24),
    (PF_INT, 'duration', 'Animation duration in miliseconds', 1000),
  ]

  register(
    'animate-layer-slide',
    animateHIDesc,animateHIDesc,
    'opif','opif',
    '2021',
    'Foreground Slide',
    '*',animateParms,[],
    animateImage,
    menu=animateMenu
  )

registration()
main()
