import { createRenderer } from './feedback-renderer.js'

const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value))

function attachColor(gl, texture) {
  gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texture, 0)
}

export function mountFeedback(stage, canvas, options = {}) {
  const poster = stage.querySelector('.poster')
  const motion = matchMedia('(prefers-reduced-motion: reduce)')
  const lifetime = new AbortController()
  const { signal } = lifetime
  let state = 'loading'
  let reason = ''
  let visible = false
  let gl
  let renderer
  let queued = null
  let previousTime = null
  let draws = 0
  let losses = 0
  let recoveryUsed = false
  let dirty = true
  let sizeDirty = true
  let pixelRatio
  let densityCheck
  let initializationReady = false
  let mode = 'ink'
  let progress = 0
  let destination = 0
  let remaining = 0
  let impulse
  let pointer
  updatePoster()

  function updatePoster() {
    stage.dataset.effect = mode
    stage.dataset.scene = destination >= 0.5 ? 'dawn' : 'tide'
    const ready = state === 'ready' && !motion.matches
    poster.style.visibility = ready ? 'hidden' : ''
    canvas.style.visibility = ready ? 'visible' : ''
    options.onInkAvailabilityChange?.(ready && mode === 'ink')
  }

  function stopDensityCheck() {
    if (densityCheck !== undefined) clearInterval(densityCheck)
    densityCheck = undefined
  }

  function stop() {
    stopDensityCheck()
    if (queued !== null) cancelAnimationFrame(queued)
    queued = null
    previousTime = null
  }

  function relinquish(nextState, message) {
    stop()
    renderer?.dispose()
    renderer = undefined
    state = nextState
    reason = message
    updatePoster()
  }

  function active() {
    return mode === 'ink' ? remaining > 0 : progress !== destination
  }

  function canWork() {
    return visible && !document.hidden && !motion.matches && !signal.aborted
  }

  function schedule() {
    if (!canWork()) {
      stop()
      return
    }
    if (initializationReady && !renderer && state === 'loading') build()
    if (!renderer) return
    if (densityCheck === undefined) {
      // Some environments change DPR without dispatching a resize or media event.
      densityCheck = setInterval(() => {
        if (pixelRatio !== devicePixelRatio) invalidateSize()
      }, 200)
    }
    if (queued === null && (dirty || active())) queued = requestAnimationFrame(frame)
  }

  function frame(timestamp) {
    queued = null
    if (!renderer || !canWork()) return
    if (gl.isContextLost()) return
    const dt = previousTime === null ? 1 / 60 : Math.min(0.033, (timestamp - previousTime) / 1000)
    const simulate = mode === 'ink' && remaining > 0
    const frameStarted = options.onFrame ? performance.now() : 0
    try {
      if (sizeDirty || pixelRatio !== devicePixelRatio) {
        renderer.resize()
        pixelRatio = devicePixelRatio
        sizeDirty = false
      }
      if (simulate) remaining = Math.max(0, remaining - dt)
      if (mode === 'images' && progress !== destination) {
        const advance = Math.sign(destination - progress) * dt / 0.65
        progress = Math.abs(destination - progress) <= Math.abs(advance)
          ? destination : progress + advance
      }
      draws += renderer.render({ mode, simulate, dt, impulse, progress })
    } catch (error) {
      if (!gl.isContextLost()) relinquish('fallback', error.message)
      return
    }
    impulse = undefined
    dirty = false
    if (state !== 'ready') {
      state = 'ready'
      updatePoster()
    }
    previousTime = active() ? timestamp : null
    options.onFrame?.(gl, renderer, { timestamp, submitMs: performance.now() - frameStarted })
    schedule()
  }

  function build() {
    if (signal.aborted) return
    try {
      gl ??= (options.getContext ?? (element =>
        element.getContext('webgl2', { alpha: false, antialias: false, depth: false })))(canvas)
      if (!gl) throw new Error('WebGL2 unavailable')
      if (gl.isContextLost()) return
      renderer = createRenderer(gl, canvas, options.attachColor ?? attachColor)
      state = 'loading'
      reason = ''
      dirty = sizeDirty = true
      lossExtension ??= gl.getExtension('WEBGL_lose_context')
    } catch (error) {
      if (!gl?.isContextLost()) relinquish('fallback', error.message)
    }
  }

  function onLost(event) {
    if (losses === 0) event.preventDefault()
    losses++
    remaining = 0
    impulse = undefined
    relinquish('lost', 'WebGL context lost')
  }

  function onRestored() {
    if (state !== 'lost' || losses !== 1) return
    recoveryUsed = true
    state = 'loading'
    schedule()
  }

  function recover() {
    if (state !== 'lost' || losses !== 1 || recoveryUsed) return false
    if (!lossExtension) return false
    recoveryUsed = true
    lossExtension.restoreContext()
    return true
  }

  // Query the test extension before any loss, since discovery itself fails while lost.
  let lossExtension
  const intersection = new IntersectionObserver(entries => {
    visible = entries.at(-1).isIntersecting
    schedule()
  })
  intersection.observe(stage)
  function invalidateSize() {
    dirty = sizeDirty = true
    schedule()
  }

  function watchResolution() {
    const resolution = matchMedia(`(resolution: ${devicePixelRatio}dppx)`)
    resolution.addEventListener('change', () => {
      watchResolution()
      invalidateSize()
    }, { signal, once: true })
  }

  const resize = new ResizeObserver(invalidateSize)
  resize.observe(stage)
  watchResolution()

  document.addEventListener('visibilitychange', schedule, { signal })
  addEventListener('resize', invalidateSize, { signal })
  motion.addEventListener('change', () => {
    if (motion.matches) {
      progress = destination
      remaining = 0
      impulse = undefined
    }
    dirty = true
    updatePoster()
    schedule()
  }, { signal })
  canvas.addEventListener('webglcontextlost', onLost, { signal })
  canvas.addEventListener('webglcontextrestored', onRestored, { signal })
  ;(async () => {
    try {
      await options.beforeInitialize?.(signal)
      if (signal.aborted) return
      initializationReady = true
      schedule()
    } catch (error) {
      if (!signal.aborted) relinquish('fallback', error.message)
    }
  })()

  function burst(x = 0.45, y = 0.5, dx = 0.42, dy = 0.18) {
    if (!renderer || !canWork() || mode !== 'ink') return
    impulse = [clamp(x), clamp(y), clamp(dx, -0.8, 0.8), clamp(dy, -0.8, 0.8)]
    remaining = 1.75
    schedule()
  }

  function position(event) {
    const rect = stage.getBoundingClientRect()
    return [(event.clientX - rect.left) / rect.width, 1 - (event.clientY - rect.top) / rect.height]
  }
  stage.addEventListener('pointerdown', event => {
    if (!event.isPrimary || event.button !== 0 || mode !== 'ink' ||
        state !== 'ready' || !canWork()) return
    const [x, y] = position(event)
    pointer = { id: event.pointerId, x, y }
    stage.setPointerCapture(event.pointerId)
    burst(x, y, 0, 0)
  }, { signal })
  stage.addEventListener('pointermove', event => {
    if (pointer?.id !== event.pointerId) return
    const [x, y] = position(event)
    burst(x, y, (x - pointer.x) * 12, (y - pointer.y) * 12)
    pointer = { id: event.pointerId, x, y }
  }, { signal })
  stage.addEventListener('lostpointercapture', () => { pointer = undefined }, { signal })

  function setMode(next) {
    if (mode === next) return
    mode = next
    remaining = 0
    impulse = undefined
    progress = destination
    previousTime = null
    dirty = true
    updatePoster()
    schedule()
  }

  function seek(next) {
    // A stationary scrub may intentionally display the intermediate mask.
    // Keep the DOM poster on the nearest complete image.
    destination = clamp(next)
    progress = destination
    dirty = true
    updatePoster()
    schedule()
  }

  function toggleScene() {
    destination = destination >= 0.5 ? 0 : 1
    if (motion.matches || !renderer) progress = destination
    dirty = true
    updatePoster()
    schedule()
  }

  function destroy() {
    if (signal.aborted) return
    lifetime.abort()
    if (pointer && stage.hasPointerCapture(pointer.id)) stage.releasePointerCapture(pointer.id)
    pointer = undefined
    intersection.disconnect()
    resize.disconnect()
    relinquish('unmounted', '')
    gl = undefined
    lossExtension = undefined
  }

  return {
    burst, setMode, toggleScene, seek, recover, destroy,
    snapshot: () => ({ state, reason, visible, draws, progress, destination, pending: queued !== null })
  }
}
