import { vertex, feedback, ink, image, composite } from './feedback-shaders.js'

export function createRenderer(gl, canvas, attachColor) {
  const releases = new Map()
  const own = (handle, remove) => {
    if (!handle) throw new Error('WebGL resource allocation failed')
    releases.set(handle, () => remove.call(gl, handle))
    return handle
  }
  const release = handle => {
    releases.get(handle)?.()
    releases.delete(handle)
  }
  const dispose = () => {
    // WebGL invalidates old handles on loss. Drop JavaScript references as well.
    if (!gl.isContextLost()) {
      gl.bindFramebuffer(gl.FRAMEBUFFER, null)
      gl.bindVertexArray(null)
      gl.useProgram(null)
      for (const unit of [gl.TEXTURE0, gl.TEXTURE1]) {
        gl.activeTexture(unit)
        gl.bindTexture(gl.TEXTURE_2D, null)
      }
      for (const remove of releases.values()) remove()
    }
    releases.clear()
  }

  function compile(type, source) {
    const shader = own(gl.createShader(type), gl.deleteShader)
    gl.shaderSource(shader, source)
    gl.compileShader(shader)
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      throw new Error(gl.getShaderInfoLog(shader) || 'Shader compilation failed')
    }
    return shader
  }

  function program(shaderVertex, fragment, names) {
    const shaderFragment = compile(gl.FRAGMENT_SHADER, fragment)
    const linked = own(gl.createProgram(), gl.deleteProgram)
    gl.attachShader(linked, shaderVertex)
    gl.attachShader(linked, shaderFragment)
    gl.linkProgram(linked)
    if (!gl.getProgramParameter(linked, gl.LINK_STATUS)) {
      throw new Error(gl.getProgramInfoLog(linked) || 'Program link failed')
    }
    gl.detachShader(linked, shaderVertex)
    gl.detachShader(linked, shaderFragment)
    release(shaderFragment)
    return { linked, uniforms: Object.fromEntries(names.map(name =>
      [name, gl.getUniformLocation(linked, name)])) }
  }

  function target(label, width, height, format) {
    const texture = own(gl.createTexture(), gl.deleteTexture)
    gl.bindTexture(gl.TEXTURE_2D, texture)
    gl.texStorage2D(gl.TEXTURE_2D, 1, format, width, height)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE)
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE)
    const framebuffer = own(gl.createFramebuffer(), gl.deleteFramebuffer)
    gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer)
    attachColor(gl, texture, label)
    const status = gl.checkFramebufferStatus(gl.FRAMEBUFFER)
    if (status !== gl.FRAMEBUFFER_COMPLETE) {
      throw new Error(label + ' framebuffer incomplete (0x' + status.toString(16) + ')')
    }
    gl.clearBufferfv(gl.COLOR, 0, new Float32Array(4))
    return { framebuffer, texture, width, height }
  }

  let firstFrame = true
  let imagesDirty = true
  let read
  let write
  let from
  let to
  let step
  let display
  let scene
  let blend
  let vertexArray
  try {
    if (!gl.getExtension('EXT_color_buffer_float')) throw new Error('Float render targets unavailable')
    vertexArray = own(gl.createVertexArray(), gl.deleteVertexArray)
    const shader = compile(gl.VERTEX_SHADER, vertex)
    step = program(shader, feedback, ['lastState', 'cell', 'dt', 'impulse', 'strength'])
    display = program(shader, ink, ['lastState'])
    scene = program(shader, image, ['scene', 'aspect'])
    blend = program(shader, composite, ['fromImage', 'toImage', 'progress'])
    release(shader)
  } catch (error) {
    dispose()
    throw error
  }

  let currentWidth = 0
  let currentHeight = 0
  function resize() {
    const bounds = canvas.getBoundingClientRect()
    const density = Math.min(devicePixelRatio, 2, 960 / Math.max(bounds.width, bounds.height, 1))
    const width = Math.max(1, Math.round(bounds.width * density))
    const height = Math.max(1, Math.round(bounds.height * density))
    if (width === currentWidth && height === currentHeight) return false

    for (const previous of [read, write, from, to]) {
      if (!previous) continue
      release(previous.framebuffer)
      release(previous.texture)
    }
    canvas.width = currentWidth = width
    canvas.height = currentHeight = height
    const simulationScale = 128 / Math.max(width, height)
    const simWidth = Math.max(4, Math.round(width * simulationScale))
    const simHeight = Math.max(4, Math.round(height * simulationScale))
    read = target('dye-a', simWidth, simHeight, gl.RGBA16F)
    write = target('dye-b', simWidth, simHeight, gl.RGBA16F)
    from = target('image-a', width, height, gl.RGBA8)
    to = target('image-b', width, height, gl.RGBA8)
    imagesDirty = true
    return true
  }

  function use(pass, destination) {
    gl.bindFramebuffer(gl.FRAMEBUFFER, destination?.framebuffer ?? null)
    gl.viewport(0, 0, destination?.width ?? canvas.width, destination?.height ?? canvas.height)
    gl.useProgram(pass.linked)
    return pass.uniforms
  }

  function sample(location, unit, source) {
    gl.activeTexture(gl.TEXTURE0 + unit)
    gl.bindTexture(gl.TEXTURE_2D, source.texture)
    gl.uniform1i(location, unit)
  }

  function draw() {
    gl.drawArrays(gl.TRIANGLES, 0, 3)
  }

  function drawImage(id, destination) {
    const u = use(scene, destination)
    gl.uniform1i(u.scene, id)
    gl.uniform1f(u.aspect, canvas.width / canvas.height)
    draw()
  }

  function render({ mode, simulate, dt, impulse, progress }) {
    gl.bindVertexArray(vertexArray)
    let passes = 1
    if (mode === 'ink') {
      if (simulate) {
        const u = use(step, write)
        sample(u.lastState, 0, read)
        gl.uniform2f(u.cell, 1 / read.width, 1 / read.height)
        gl.uniform1f(u.dt, dt)
        gl.uniform4f(u.impulse, ...(impulse ?? [0, 0, 0, 0]))
        gl.uniform1f(u.strength, impulse ? 1 : 0)
        draw()
        ;[read, write] = [write, read]
        passes++
      }
      const u = use(display, null)
      sample(u.lastState, 0, read)
      draw()
    } else if (progress <= 0 || progress >= 1) {
      drawImage(progress >= 1 ? 1 : 0, null)
    } else {
      if (imagesDirty) {
        drawImage(0, from)
        drawImage(1, to)
        imagesDirty = false
        passes += 2
      }
      const u = use(blend, null)
      sample(u.fromImage, 0, from)
      sample(u.toImage, 1, to)
      gl.uniform1f(u.progress, progress)
      draw()
    }
    if (firstFrame) {
      firstFrame = false
      const error = gl.getError()
      if (error !== gl.NO_ERROR) throw new Error('First draw failed (0x' + error.toString(16) + ')')
    }
    return passes
  }

  return { resize, render, dispose, get read() { return read } }
}
