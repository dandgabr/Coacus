import { mountFeedback } from './feedback.js'

function assert(condition, message) {
  if (!condition) throw new Error(message)
}

const wait = ms => new Promise(resolve => setTimeout(resolve, ms))

async function until(predicate, label) {
  const deadline = performance.now() + 3000
  while (!predicate()) {
    if (performance.now() > deadline) throw new Error('Timed out: ' + label)
    await wait(15)
  }
}

function visible(element) {
  return getComputedStyle(element).visibility === 'visible'
}

function sampleScreen(gl, canvas, x, y) {
  const pixel = new Uint8Array(4)
  gl.readPixels(Math.floor(canvas.width * x), Math.floor(canvas.height * y),
    1, 1, gl.RGBA, gl.UNSIGNED_BYTE, pixel)
  return Array.from(pixel)
}

function sampleDye(gl, target) {
  const { framebuffer, width, height } = target
  const pixels = new Float32Array(width * height * 4)
  gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer)
  gl.readPixels(0, 0, width, height, gl.RGBA, gl.FLOAT, pixels)
  gl.bindFramebuffer(gl.FRAMEBUFFER, null)
  let mass = 0
  let weightedX = 0
  let wall = 0
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const index = 4 * (y * width + x)
      const dye = pixels[index + 2]
      mass += dye
      weightedX += dye * (x + 0.5) / width
      if (x === 0 || y === 0 || x === width - 1 || y === height - 1) {
        wall = Math.max(wall, Math.abs(pixels[index]), Math.abs(pixels[index + 1]), dye)
      }
    }
  }
  assert(gl.getError() === gl.NO_ERROR, 'float feedback readback must be valid')
  return { mass, x: weightedX / mass, wall }
}

export async function runChecks() {
  const stage = document.querySelector('#stage')
  const poster = stage.querySelector('.poster')
  const [leftColor, rightColor] = [[17, 35, 61], [61, 28, 51]]
  let controller
  const checks = []
  let probeCanvas
  let scrollMarker
  const start = options => {
    const canvas = document.createElement('canvas')
    canvas.setAttribute('aria-hidden', 'true')
    stage.append(canvas)
    probeCanvas = canvas
    controller = mountFeedback(stage, canvas, options)
    return canvas
  }
  const stop = canvas => {
    controller.destroy()
    canvas.remove()
  }

  try {
    let unblock
    let contextRequests = 0
    let canvas = start({
      beforeInitialize: () => new Promise(resolve => { unblock = resolve }),
      getContext: element => { contextRequests++; return element.getContext('webgl2') }
    })
    await until(() => unblock, 'delayed initialization')
    assert(visible(poster) && !visible(canvas), 'poster owns the first paint')
    stop(canvas)
    unblock()
    await wait(80)
    assert(contextRequests === 0 && !controller.snapshot().pending,
      'unmount during initialization invalidates the pending work')
    checks.push('first-frame poster and stale initialization')

    canvas = start({ getContext: () => null })
    await until(() => controller.snapshot().state === 'fallback', 'unavailable backend')
    assert(visible(poster) && !visible(canvas) && controller.snapshot().draws === 0,
      'unavailable backend must keep the usable poster')
    stop(canvas)
    checks.push('unavailable context via injected acquisition result')

    canvas = start({
      attachColor(gl, texture, label) {
        if (label === 'dye-b') return
        gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texture, 0)
      }
    })
    await until(() => controller.snapshot().state === 'fallback', 'incomplete framebuffer')
    assert(controller.snapshot().reason.includes('dye-b') &&
      visible(poster) && !visible(canvas) && controller.snapshot().draws === 0,
      'real incomplete second feedback target must fail before drawing')
    stop(canvas)
    checks.push('incomplete framebuffer rejected by WebGL')

    let frame
    let handle
    let readback = false
    let submissions = 0
    let lastTimestamp
    let duplicateTimestamp = false
    let paints = 0
    canvas = start({
      getContext(element) {
        const gl = element.getContext('webgl2', { alpha: false, antialias: false })
        const draw = gl.drawArrays.bind(gl)
        gl.drawArrays = (...arguments_) => {
          submissions++
          draw(...arguments_)
        }
        return gl
      },
      onFrame(gl, renderer, { timestamp }) {
        paints++
        duplicateTimestamp ||= lastTimestamp === timestamp
        lastTimestamp = timestamp
        handle = renderer.read.texture
        if (!readback) return
        frame = {
          left: sampleScreen(gl, canvas, 0.12, 0.91),
          right: sampleScreen(gl, canvas, 0.88, 0.91),
          dye: sampleDye(gl, renderer.read)
        }
      }
    })
    await until(() => controller.snapshot().state === 'ready', 'working GPU paint')
    assert(!visible(poster) && visible(canvas), 'first working frame reveals the canvas')
    controller.setMode('images')
    readback = true
    const expectRGB = (rgba, rgb) => rgb.every((n, index) => Math.abs(rgba[index] - n) <= 2)
    const seek = async (progress, expectedLeft, expectedRight, draws) => {
      const previous = submissions
      frame = null
      controller.seek(progress)
      await until(() => frame !== null, 'requested image frame')
      assert(expectRGB(frame.left, expectedLeft) && expectRGB(frame.right, expectedRight),
        'image mask must resolve the expected colors at progress ' + progress + ': ' + JSON.stringify(frame))
      assert(submissions - previous === draws,
        'transition must draw the expected endpoint, source or composite passes')
    }
    await seek(0, leftColor, leftColor, 1)
    await seek(0.5, rightColor, leftColor, 3)
    await seek(1, rightColor, rightColor, 1)
    await seek(0.5, rightColor, leftColor, 1)
    await seek(0, leftColor, leftColor, 1)
    controller.toggleScene()
    await until(() => controller.snapshot().progress > 0.12, 'transition advanced')
    const turningPoint = controller.snapshot().progress
    controller.toggleScene()
    assert(controller.snapshot().progress === turningPoint, 'reversal begins from current progress')
    await until(() => controller.snapshot().progress < turningPoint, 'interrupted animation reverses')
    await until(() => !controller.snapshot().pending, 'reversed transition settled')
    await seek(0.5, rightColor, leftColor, 1)
    const previousWidth = canvas.width
    const beforeResize = submissions
    stage.style.width = '60%'
    await until(() => previousWidth !== canvas.width && !controller.snapshot().pending, 'responsive resize')
    assert(controller.snapshot().progress === 0.5 && submissions - beforeResize === 3 &&
      expectRGB(frame.left, rightColor) && expectRGB(frame.right, leftColor),
      'resize rebuilds both image sources without changing the displayed mask')
    stage.style.width = ''
    await until(() => previousWidth === canvas.width && !controller.snapshot().pending, 'restore test width')
    checks.push('image pixels and pass counts at endpoints, midpoint, reversal and resize')

    controller.setMode('ink')
    await until(() => !controller.snapshot().pending, 'ink settled before known input')
    readback = true
    controller.burst(0.35, 0.5, 0.6, 0)
    await until(() => frame.dye.mass > 1, 'seeded dye')
    const seeded = frame.dye
    await until(() => frame.dye.x > seeded.x + 0.015 && frame.dye.mass < seeded.mass * 0.85,
      'dye transported and dissipated')
    const transported = frame.dye
    controller.burst(0.002, 0.5, -0.6, 0)
    await until(() => frame.dye.mass > transported.mass, 'impulse at wall')
    assert(frame.dye.wall === 0, 'wall cells must retain zero velocity and dye')
    controller.burst(0.6, 0.6, 0, 0)
    await until(() => frame.dye.mass > 1, 'known input after resize')
    checks.push({ name: 'feedback dye transport, dissipation and walls', seeded, transported })

    readback = false
    assert(controller.snapshot().pending, 'active ink provides a positive submission control')
    scrollMarker = document.createElement('div')
    scrollMarker.style.height = '120vh'
    document.body.append(scrollMarker)
    window.scrollTo(0, document.body.scrollHeight)
    await until(() => !controller.snapshot().visible, 'offscreen intersection')
    let draws = submissions
    await wait(120)
    assert(!controller.snapshot().pending && submissions === draws,
      'offscreen ink owns no frame and draws nothing')
    window.scrollTo(0, 0)
    await until(() => controller.snapshot().visible && submissions > draws, 'resumed ink')
    const paintsAtResume = paints
    for (let repeat = 0; repeat < 10; repeat++) controller.burst()
    await until(() => paints >= paintsAtResume + 3, 'active resumed frames')
    assert(controller.snapshot().pending && !duplicateTimestamp,
      'visible ink resumes with one callback per frame despite repeated input')
    scrollMarker.remove()
    checks.push('real IntersectionObserver suspension and single resume')

    const gl = canvas.getContext('webgl2')
    const extension = gl.getExtension('WEBGL_lose_context')
    assert(extension, 'WEBGL_lose_context required for this check')
    const oldHandle = handle
    extension.loseContext()
    await until(() => controller.snapshot().state === 'lost', 'context lost event')
    draws = submissions
    assert(visible(poster) && !visible(canvas) && !controller.snapshot().pending,
      'loss immediately relinquishes the image and frame')
    await wait(80)
    assert(submissions === draws, 'no GPU submission while lost')
    assert(controller.recover() && !controller.recover(), 'one restoration request per mount')
    await until(() => controller.snapshot().state === 'ready', 'real context restored event')
    assert(handle !== oldHandle && !gl.isTexture(oldHandle) && gl.isTexture(handle) &&
      submissions > draws, 'restoration draws with a new live WebGL texture')
    controller.burst()
    await until(() => controller.snapshot().pending, 'active loop before unmount')
    stop(canvas)
    draws = submissions
    await wait(80)
    assert(!controller.snapshot().pending && submissions === draws,
      'unmount of live renderer cancels frames and GPU submissions')

    canvas = start()
    await until(() => controller.snapshot().state === 'ready', 'second test mount')
    const secondLoss = canvas.getContext('webgl2').getExtension('WEBGL_lose_context')
    secondLoss.loseContext()
    await until(() => controller.snapshot().state === 'lost', 'new mount first loss')
    assert(controller.recover(), 'fresh mount owns a new recovery attempt')
    await until(() => controller.snapshot().state === 'ready', 'new mount restored')
    secondLoss.loseContext()
    await until(() => controller.snapshot().state === 'lost', 'second loss')
    assert(!controller.recover() && visible(poster), 'second loss stays on the poster')
    stop(canvas)
    assert(!controller.snapshot().pending, 'unmount clears the pending callback')
    checks.push('real context loss, new resources, one recovery and teardown')
    return { status: 'pass', checks }
  } finally {
    controller?.destroy()
    stage.style.width = ''
    probeCanvas?.remove()
    scrollMarker?.remove()
    window.scrollTo(0, 0)
  }
}
